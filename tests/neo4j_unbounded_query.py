#!/usr/bin/env python3
"""Run an unbounded / expensive Cypher query and report how it terminates.

Companion to ``neo4j_stress_nodes.py``. After provisioning ~1M nodes, this
script runs a deliberately heavy query and FULLY materialises the result
(``list(result)``) -- reproducing what the MCP endpoint does when it
serialises every record to JSON. The Neo4j browser hides this effect because
it streams and caps the displayed rows; consuming all records here does not.

A transaction-level timeout is set via the driver, so no server-side config
(``db.transaction.timeout`` / ``dbms.setConfigValue``) is required. This
demonstrates the timeout mechanism itself; the deployed MCP endpoint would
enforce the same guard via the server setting ``NEO4J_db_transaction_timeout``.

Modes:
    cartesian   MATCH (a:L),(b:L) RETURN count(*)   -> time-based timeout
    return_all  MATCH (n:L) RETURN n                -> serialisation/transfer load
    collect     MATCH (n:L) RETURN collect(n)       -> heap materialisation

Connection defaults match docker-compose: bolt://localhost:7687, no auth.
Override via NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD / NEO4J_DATABASE.

Usage:
    python neo4j_unbounded_query.py                       # cartesian, 5s timeout
    python neo4j_unbounded_query.py --mode return_all
    python neo4j_unbounded_query.py --timeout 10
    python neo4j_unbounded_query.py --query "MATCH (n) RETURN n"
"""
from __future__ import annotations

import argparse
import os
import time

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")

MODES = {
    "cartesian": "MATCH (a:{label}),(b:{label}) RETURN count(*) AS c",
    "return_all": "MATCH (n:{label}) RETURN n",
    "collect": "MATCH (n:{label}) RETURN collect(n) AS all",
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=list(MODES), default="cartesian", help="preset query (default: cartesian)")
    p.add_argument("--query", default=None, help="explicit Cypher, overrides --mode")
    p.add_argument("--label", default="Submodel", help="node label for preset modes (default: Submodel)")
    p.add_argument("--timeout", type=float, default=5.0, help="transaction timeout in seconds (default: 5)")
    args = p.parse_args()

    query = args.query or MODES[args.mode].format(label=args.label)

    auth = (NEO4J_USER, NEO4J_PASSWORD) if NEO4J_PASSWORD else None
    driver = GraphDatabase.driver(NEO4J_URI, auth=auth)
    print(f"Query   : {query}")
    print(f"Timeout : {args.timeout}s (transaction-level)\n")

    t0 = time.time()
    try:
        driver.verify_connectivity()
        with driver.session(database=NEO4J_DATABASE) as session:
            with session.begin_transaction(timeout=args.timeout) as tx:
                result = tx.run(query)
                records = list(result)  # full materialisation -- the saturating step
            elapsed = time.time() - t0
            print(f"COMPLETED in {elapsed:.2f}s -- {len(records):,} record(s) returned.")
            print("No timeout fired: the unbounded query was NOT contained at this scale/timeout.")
    except Neo4jError as e:
        elapsed = time.time() - t0
        print(f"ABORTED after {elapsed:.2f}s")
        print(f"  code   : {e.code}")
        print(f"  message: {str(e).splitlines()[0]}")
        print("\nThis is the desired outcome: the database aborts the runaway query and")
        print("surfaces a structured error -- a deterministic read-path guard.")
    except Exception as e:  # transport/other
        elapsed = time.time() - t0
        print(f"FAILED after {elapsed:.2f}s with non-Neo4j error: {type(e).__name__}: {e}")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
