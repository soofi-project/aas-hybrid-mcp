"""Benchmark A: Neo4j Ingestion v2 (Bolt+UNWIND).

Measures ingestion drain time during BaSyx AASX auto-ingestion and Cypher p95
query latency for the v2 Bolt-based Kafka Connect Neo4j plugin.

BaSyx auto-ingests AASX files from the ./aasx/ directory on startup.
The benchmark monitors the connector's consumer group lag via KafkaAdminClient.
Drain is complete when lag=0. Aborts if lag has not decreased for 30 minutes
(indicates a crashed connector).

Usage:
  python bench_ingest.py                         # Full run
  python bench_ingest.py --cypher-only           # Only run Cypher queries on running stack
  python bench_ingest.py --poll-interval 10      # Lag check interval in seconds
  python bench_ingest.py --query-repetitions 200 # 200 Cypher query repetitions
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
COMPOSE_FILE = SCRIPT_DIR / "docker-compose.bench.yml"
ENV_FILE = SCRIPT_DIR / ".env.bench"
AASX_DIR = SCRIPT_DIR / "aasx"
RESULTS_DIR = SCRIPT_DIR / "results"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""

KAFKA_BOOTSTRAP = "localhost:9093"
KAFKA_TOPICS = ["aas-events", "submodel-events"]

CYPHER_COUNT_SHELLS    = "MATCH (n:AssetAdministrationShell) RETURN count(n) AS c"
CYPHER_COUNT_SUBMODELS = "MATCH (n:Submodel) RETURN count(n) AS c"
CYPHER_COUNT_ELEMENTS  = "MATCH (n:SubmodelElement) RETURN count(n) AS c"

CYPHER_2HOP = """
MATCH (s:AssetAdministrationShell)-[:HAS_SUBMODEL]->(m:Submodel)
      -[:HAS_SME|HAS_PROPERTY]->(p)
RETURN s.id AS shell_id, m.id AS sm_id, p.idShort AS prop
LIMIT 1
"""

CYPHER_4HOP = """
MATCH (s:AssetAdministrationShell)-[:HAS_SUBMODEL]->(m:Submodel)
      -[:HAS_SME]->(sme)-[:HAS_SEMANTIC_ID]->(cd:ConceptDescription)
RETURN s.id AS shell_id, m.id AS sm_id, sme.idShort AS sme_name, cd.idShort AS cd_name
LIMIT 1
"""

log = logging.getLogger("bench_ingest")


def _compose_cmd(extra: list[str]) -> list[str]:
    return [
        "docker", "compose",
        "-f", str(COMPOSE_FILE),
        "--env-file", str(ENV_FILE),
        *extra,
    ]


def stack_up() -> None:
    log.info("Starting stack...")
    result = subprocess.run(_compose_cmd(["up", "-d"]), timeout=600)
    if result.returncode != 0:
        raise RuntimeError("docker compose up failed")
    log.info("Stack started")


def stack_down(wipe: bool = True) -> None:
    log.info("Stopping stack (wipe=%s)", wipe)
    extra = ["down", "-v"] if wipe else ["down"]
    subprocess.run(_compose_cmd(extra), text=True, timeout=120)
    log.info("Stack stopped")


def count_input_files() -> int:
    return sum(1 for f in AASX_DIR.iterdir() if f.is_file())


def _find_connect_group(admin) -> str | None:
    try:
        groups = admin.list_consumer_groups()
        names = [g[0] if isinstance(g, tuple) else str(g) for g in groups]
    except Exception as e:
        log.warning("Failed to list consumer groups: %s", e)
        return None
    log.debug("All consumer groups: %s", names)
    for name in names:
        if "connect" in name.lower() or "neo4j" in name.lower():
            return name
    return None


def _kafka_lag(admin, meta_consumer, group: str) -> dict:
    """Return total lag for the connector group across KAFKA_TOPICS."""
    from kafka import TopicPartition

    tps = []
    for topic in KAFKA_TOPICS:
        parts = meta_consumer.partitions_for_topic(topic) or set()
        tps.extend(TopicPartition(topic, p) for p in parts)
    if not tps:
        return {"current_offset": 0, "log_end_offset": 0, "lag": 0}

    meta_consumer.assign(tps)
    end = meta_consumer.end_offsets(tps)
    total_end = sum(end.values())

    try:
        committed = admin.list_consumer_group_offsets(group)
        total_committed = sum(
            om.offset for om in committed.values() if om.offset >= 0
        )
    except Exception:
        total_committed = 0

    return {
        "current_offset": total_committed,
        "log_end_offset": total_end,
        "lag": max(0, total_end - total_committed),
    }


def measure_lag(poll_interval_s: int = 5) -> list[dict]:
    """Monitor connector consumer group lag via KafkaAdminClient.

    Exits when lag=0. Aborts if lag has not decreased for 30 minutes.
    """
    try:
        from kafka import KafkaAdminClient, KafkaConsumer
    except ImportError:
        log.error("kafka-python not installed. Run: pip install kafka-python")
        return []

    STUCK_TIMEOUT_S = 1800

    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP)
    meta_consumer = KafkaConsumer(bootstrap_servers=KAFKA_BOOTSTRAP, group_id=None)

    try:
        log.info("Waiting for Kafka Connect consumer group...")
        group = None
        t_init = time.monotonic()
        while group is None:
            group = _find_connect_group(admin)
            if group:
                break
            if time.monotonic() - t_init > 300:
                log.error("No connector consumer group appeared within 5 min")
                return []
            time.sleep(3)
        log.info("Consumer group: %s", group)

        log.info("Monitoring lag (abort if no decrease for %ds)...", STUCK_TIMEOUT_S)
        samples: list[dict] = []
        t_start: float | None = None
        prev_lag: int | None = None
        last_decrease_t: float | None = None

        while True:
            info = _kafka_lag(admin, meta_consumer, group)
            lag = info["lag"]
            log_end = info["log_end_offset"]

            if t_start is None and log_end > 0:
                t_start = time.monotonic()
                last_decrease_t = t_start
                log.info("First event detected (log_end=%d) — drain timer starts", log_end)

            elapsed = time.monotonic() - t_start if t_start is not None else 0

            if t_start is not None:
                samples.append({
                    "t_s": round(elapsed, 3),
                    "lag": lag,
                    "current_offset": info["current_offset"],
                    "log_end_offset": log_end,
                })
                log.info("  t=%.1fs  lag=%d  offset=%d  end=%d",
                         elapsed, lag, info["current_offset"], log_end)

            if prev_lag is not None and lag < prev_lag:
                last_decrease_t = time.monotonic()
            prev_lag = lag

            if lag == 0 and log_end > 0:
                log.info("Lag=0 — ingestion complete (%.1fs)", elapsed)
                break

            if last_decrease_t is not None:
                stuck_for = time.monotonic() - last_decrease_t
                if stuck_for > STUCK_TIMEOUT_S:
                    log.error(
                        "Lag has not decreased in %ds (lag=%d) — connector likely crashed",
                        STUCK_TIMEOUT_S, lag,
                    )
                    break

            time.sleep(poll_interval_s)

    finally:
        try:
            meta_consumer.close()
            admin.close()
        except Exception:
            pass

    if samples:
        log.info("Drain done: %.1fs, samples=%d", samples[-1]["t_s"], len(samples))
    return samples


def count_neo4j_nodes() -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError:
        log.error("neo4j driver not installed. Run: pip install neo4j")
        return {}

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD) if NEO4J_USER else None)
    counts = {}
    try:
        with driver.session() as session:
            counts["shells"] = session.run(CYPHER_COUNT_SHELLS).single()["c"]
            counts["submodels"] = session.run(CYPHER_COUNT_SUBMODELS).single()["c"]
            counts["elements"] = session.run(CYPHER_COUNT_ELEMENTS).single()["c"]
    finally:
        driver.close()

    log.info("[EVAL: a_shells] AAS shells in Neo4j: %d", counts["shells"])
    log.info("[EVAL: a_submodels] Submodels in Neo4j: %d", counts["submodels"])
    log.info("[EVAL: a_elements] SMEs in Neo4j: %d", counts["elements"])
    return counts


def run_cypher_benchmark(repetitions: int = 100) -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError:
        log.error("neo4j driver not installed. Run: pip install neo4j")
        return {}

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD) if NEO4J_USER else None)

    results = {}
    for label, query in [("2hop", CYPHER_2HOP), ("4hop_semID", CYPHER_4HOP)]:
        latencies = []
        log.info("Running Cypher %s benchmark (%d repetitions)...", label, repetitions)
        for i in range(repetitions):
            t0 = time.perf_counter()
            with driver.session() as session:
                session.run(query)
            latencies.append((time.perf_counter() - t0) * 1000)

        latencies.sort()
        results[label] = {
            "repetitions": repetitions,
            "mean_ms": round(sum(latencies) / len(latencies), 2),
            "p50_ms": round(latencies[len(latencies) // 2], 2),
            "p95_ms": round(latencies[int(len(latencies) * 0.95)], 2),
            "p99_ms": round(latencies[int(len(latencies) * 0.99)], 2),
            "min_ms": round(latencies[0], 2),
            "max_ms": round(latencies[-1], 2),
        }
        log.info("  %s: mean=%.1fms  p50=%.1fms  p95=%.1fms  p99=%.1fms",
                 label, results[label]["mean_ms"], results[label]["p50_ms"],
                 results[label]["p95_ms"], results[label]["p99_ms"])

    driver.close()
    return results


def compute_derived_metrics(lag_samples: list[dict], n_shells: int) -> dict:
    if not lag_samples:
        return {}
    drain_time = lag_samples[-1]["t_s"]
    total_events = lag_samples[-1].get("log_end_offset", 0)
    if total_events == 0:
        total_events = n_shells
    throughput = total_events / drain_time if drain_time > 0 else 0
    mean_latency_ms = (drain_time * 1000 / total_events) if total_events > 0 else 0
    peak_lag = max(s["lag"] for s in lag_samples)
    return {
        "n_shells": n_shells,
        "total_events": total_events,
        "drain_time_s": round(drain_time, 2),
        "throughput_events_per_s": round(throughput, 2),
        "mean_latency_ms": round(mean_latency_ms, 2),
        "peak_lag": peak_lag,
    }


def print_results(metrics: dict, cypher: dict, neo4j_counts: dict) -> None:
    print("\n" + "=" * 60)
    print("BENCHMARK A RESULTS — v2 (Bolt + UNWIND)")
    print("=" * 60)

    if metrics:
        print(f"\nIngestion:")
        print(f"  [EVAL: b1] Mean latency/event:  {metrics.get('mean_latency_ms', '?')} ms")
        print(f"  [EVAL: b2] Full-load wall-clock: {metrics.get('drain_time_s', '?')} s")
        print(f"  Throughput:                      {metrics.get('throughput_events_per_s', '?')} ev/s")
        print(f"  Peak Kafka lag:                  {metrics.get('peak_lag', '?')} events")

    if neo4j_counts:
        print(f"\nNeo4j:")
        print(f"  [EVAL: a_shells]   Shells:    {neo4j_counts.get('shells', '?')}")
        print(f"  [EVAL: a_submodels] Submodels: {neo4j_counts.get('submodels', '?')}")
        print(f"  [EVAL: a_elements]  Elements:  {neo4j_counts.get('elements', '?')}")

    if cypher:
        print(f"\nCypher:")
        print(f"  [EVAL: b3] p95 2-hop:       {cypher.get('2hop', {}).get('p95_ms', '?')} ms")
        print(f"  [EVAL: b4] p95 4-hop+semID: {cypher.get('4hop_semID', {}).get('p95_ms', '?')} ms")

    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark A: Neo4j Ingestion v2")
    parser.add_argument("--poll-interval", type=int, default=5,
                        help="Lag polling interval in seconds (default: 5)")
    parser.add_argument("--query-repetitions", type=int, default=100,
                        help="Cypher query repetitions (default: 100)")
    parser.add_argument("--cypher-only", action="store_true",
                        help="Only run Cypher queries on a running stack")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-5s %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("kafka").setLevel(logging.WARNING)

    n_aasx = count_input_files()
    log.info("Input files in ./aasx/: %d", n_aasx)
    if n_aasx == 0:
        log.error("No input files found in %s — place files and re-run", AASX_DIR)
        sys.exit(1)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.cypher_only:
        cypher = run_cypher_benchmark(args.query_repetitions)
        print(json.dumps(cypher, indent=2))
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_path = RESULTS_DIR / f"bench_ingest_{ts}.json"

    stack_down(wipe=True)
    stack_up()

    lag_samples = measure_lag(poll_interval_s=args.poll_interval)
    neo4j_counts = count_neo4j_nodes()
    metrics = compute_derived_metrics(lag_samples, n_aasx)
    cypher = run_cypher_benchmark(args.query_repetitions)

    result = {
        "timestamp": ts,
        "aasx_count": n_aasx,
        "poll_interval_s": args.poll_interval,
        "query_repetitions": args.query_repetitions,
        "metrics": metrics,
        "neo4j_counts": neo4j_counts,
        "cypher": cypher,
        "lag_samples": lag_samples,
    }
    result_path.write_text(json.dumps(result, indent=2))
    log.info("Results written to %s", result_path)

    stack_down(wipe=True)

    print_results(metrics, cypher, neo4j_counts)


if __name__ == "__main__":
    main()
