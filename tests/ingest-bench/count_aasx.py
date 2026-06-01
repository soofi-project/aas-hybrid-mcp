"""Aggregate structural counts over the ingest-bench source JSON files.

Counts shells / submodels / conceptDescriptions per file, flags files that
fail to parse, and applies a vendor heuristic (substring match on the raw
text). Prints only aggregates -- never file contents.
"""
import json
import sys
from pathlib import Path

src = Path(r"C:\repo\soofi\aas-hybrid-mcp\tests\ingest-bench\aasx")

files = sorted(src.glob("*.json"))
n_files = len(files)

tot_shells = tot_sm = tot_cd = 0
corrupt = []
vendor_shells = {"wago": 0, "festo": 0, "both": 0, "neither": 0}
files_with_cd = 0

for f in files:
    try:
        raw = f.read_text(encoding="utf-8")
        doc = json.loads(raw)
    except Exception as e:  # noqa: BLE001
        corrupt.append((f.name, type(e).__name__))
        continue

    shells = doc.get("assetAdministrationShells") or []
    sms = doc.get("submodels") or []
    cds = doc.get("conceptDescriptions") or []
    tot_shells += len(shells)
    tot_sm += len(sms)
    tot_cd += len(cds)
    if cds:
        files_with_cd += 1

    low = raw.lower()
    has_w = "wago" in low
    has_f = "festo" in low
    key = ("both" if has_w and has_f else
           "wago" if has_w else
           "festo" if has_f else "neither")
    vendor_shells[key] += len(shells)

print(f"files on disk        : {n_files}")
print(f"corrupt/unparseable  : {len(corrupt)}")
for name, err in corrupt:
    print(f"    - {name}: {err}")
print(f"total shells         : {tot_shells}")
print(f"total submodels      : {tot_sm}")
print(f"total conceptDescr.  : {tot_cd}")
print(f"files with >=1 CD    : {files_with_cd}")
print("vendor split (by shells, raw-text heuristic):")
for k, v in vendor_shells.items():
    print(f"    {k:8s}: {v}")
