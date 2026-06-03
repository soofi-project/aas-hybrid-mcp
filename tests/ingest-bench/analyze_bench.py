"""Extract paper-relevant values from a bench_ingest result JSON.

Usage:
  python analyze_bench.py                       # latest result in results/
  python analyze_bench.py results/bench_*.json  # specific file
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _fmt(v, unit: str = "") -> str:
    if v is None or v == "?":
        return "?"
    return f"{v}{unit}"


def _print_version(label: str, vd: dict) -> None:
    m = vd.get("metrics") or {}
    c = vd.get("cypher") or {}
    n = vd.get("neo4j_counts") or {}

    print(f"\n{'=' * 52}")
    print(f" {label}")
    print(f"{'=' * 52}")
    print(f"  Total events:        {_fmt(m.get('total_events'))}")
    print(f"  Drain time:          {_fmt(m.get('drain_time_s'), ' s')}")
    print(f"  Throughput:          {_fmt(m.get('throughput_events_per_s'), ' ev/s')}")
    print(f"  Mean latency/event:  {_fmt(m.get('mean_latency_ms'), ' ms')}")
    print(f"  Peak lag:            {_fmt(m.get('peak_lag'))}")

    if n.get("elements") and m.get("drain_time_s"):
        rate = n["elements"] / m["drain_time_s"]
        print(f"  Element write rate:  {_fmt(round(rate, 1), ' elem/s')}")

    if n:
        print(f"\n  Neo4j node counts:")
        print(f"    Shells:     {n.get('shells', '?')}")
        print(f"    Submodels:  {n.get('submodels', '?')}")
        print(f"    Elements:   {n.get('elements', '?')}")

    for qkey, qlabel in [("2hop", "2-hop"), ("4hop_semID", "4-hop+semID")]:
        q = c.get(qkey) or {}
        if q:
            print(f"\n  Cypher {qlabel}:")
            print(f"    mean={_fmt(q.get('mean_ms'), 'ms')}  "
                  f"p50={_fmt(q.get('p50_ms'), 'ms')}  "
                  f"p95={_fmt(q.get('p95_ms'), 'ms')}  "
                  f"p99={_fmt(q.get('p99_ms'), 'ms')}")


def analyze(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    print(f"\nFile:       {path.name}")
    print(f"Timestamp:  {data.get('timestamp', '?')}")
    print(f"AASX files: {data.get('aasx_count', '?')}")

    # Result JSON nests each plugin version under a "v1"/"v2" key; older flat
    # files put metrics/cypher/neo4j_counts at the top level.
    versions = [(f"{k}  (Bolt+UNWIND)" if k == "v2" else k, data[k])
                for k in ("v1", "v2") if isinstance(data.get(k), dict)]
    if not versions:
        versions = [("v2  (Bolt+UNWIND)", data)]

    for label, vd in versions:
        _print_version(label, vd)

    print()


def main() -> None:
    if len(sys.argv) >= 2:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        results_dir = Path(__file__).parent / "results"
        paths = sorted(results_dir.glob("bench_ingest_*.json"))
        if not paths:
            print("No result files found in results/")
            sys.exit(1)
        paths = [paths[-1]]
        print("(using latest result -- pass a path to override)")

    for p in paths:
        analyze(p)


if __name__ == "__main__":
    main()
