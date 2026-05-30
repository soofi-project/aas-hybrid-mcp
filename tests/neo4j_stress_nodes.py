#!/usr/bin/env python3
"""Bulk-create plain nodes in Neo4j to stress the unbounded read-path.

Purpose: provision a large node population (default: 1,000,000 ``:Submodel``
nodes carrying only an ``id``) so an agent-style unbounded query such as

    MATCH (n:Submodel) RETURN n        // no LIMIT

can be run against a realistic node count, to observe whether the Neo4j
transaction timeout aborts the traversal and whether the MCP endpoint
surfaces a clean structured error (cf. the "Unbounded Read-Path Queries"
limitation in the ETFA 2026 paper).

Connection defaults match the docker-compose stack: bolt://localhost:7687,
no auth (NEO4J_AUTH=none), database "neo4j". Override via env if needed:
    NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE

Requires the official driver:  pip install neo4j

Usage:
    python neo4j_stress_nodes.py                     # 1,000,000 :Submodel nodes
    python neo4j_stress_nodes.py --count 2000000     # more nodes
    python neo4j_stress_nodes.py --wipe              # delete stress nodes first
    python neo4j_stress_nodes.py --wipe-only         # just clean up, create nothing

To exercise the unbounded query afterwards (set a short timeout first), e.g.:
    CALL dbms.setConfigValue('db.transaction.timeout', '5s');
    MATCH (n:Submodel) RETURN n;
"""
from __future__ import annotations

import argparse
import os
import time

from neo4j import GraphDatabase

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--count", type=int, default=1_000_000, help="number of nodes to create (default: 1,000,000)")
    p.add_argument("--batch", type=int, default=10_000, help="nodes per UNWIND transaction (default: 10,000)")
    p.add_argument("--label", default="Submodel", help="node label to create (default: Submodel)")
    p.add_argument("--wipe", action="store_true", help="delete existing stress nodes (by id prefix) before creating")
    p.add_argument("--wipe-only", action="store_true", help="delete stress nodes and exit without creating")
    args = p.parse_args()

    # A distinct id prefix keeps these throwaway nodes separable from real
    # ingested data, so --wipe never touches the Benchmark A graph.
    id_prefix = "urn:stress:submodel:"

    auth = (NEO4J_USER, NEO4J_PASSWORD) if NEO4J_PASSWORD else None
    driver = GraphDatabase.driver(NEO4J_URI, auth=auth)
    try:
        driver.verify_connectivity()
        with driver.session(database=NEO4J_DATABASE) as session:
            if args.wipe or args.wipe_only:
                print(f"Wiping existing :{args.label} stress nodes (id prefix {id_prefix!r}) ...")
                # Batched delete to avoid one huge transaction.
                while True:
                    summary = session.run(
                        f"MATCH (n:{args.label}) WHERE n.id STARTS WITH $pfx "
                        "WITH n LIMIT 50000 DETACH DELETE n RETURN count(n) AS deleted",
                        pfx=id_prefix,
                    ).single()
                    deleted = summary["deleted"] if summary else 0
                    if not deleted:
                        break
                    print(f"  deleted {deleted}")
                if args.wipe_only:
                    print("Wipe-only done.")
                    return 0

            print(f"Creating {args.count:,} :{args.label} nodes in batches of {args.batch:,} ...")
            t0 = time.time()
            created = 0
            for start in range(0, args.count, args.batch):
                n = min(args.batch, args.count - start)
                ids = [f"{id_prefix}{start + i}" for i in range(n)]
                session.run(
                    f"UNWIND $ids AS sid CREATE (:{args.label} {{id: sid}})",
                    ids=ids,
                )
                created += n
                if created % (args.batch * 10) == 0 or created == args.count:
                    rate = created / max(time.time() - t0, 1e-9)
                    print(f"  {created:,}/{args.count:,}  ({rate:,.0f} nodes/s)")

            elapsed = time.time() - t0
            print(f"Done: {created:,} nodes in {elapsed:.1f}s ({created / max(elapsed, 1e-9):,.0f} nodes/s).")
            print(
                "\nNow stress the unbounded read-path, e.g. in the Neo4j browser:\n"
                "    CALL dbms.setConfigValue('db.transaction.timeout', '5s');\n"
                f"    MATCH (n:{args.label}) RETURN n;\n"
            )
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
