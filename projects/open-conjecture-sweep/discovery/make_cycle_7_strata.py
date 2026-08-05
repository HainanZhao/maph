#!/usr/bin/env python3
"""Write the frozen 10-by-100 lexicographic strata from Cycle 6's prefix."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "discovery/out/triple-sample-p199.txt"
target = ROOT / "discovery/out/cycle7-stratified-p199.txt"
rows = source.read_text().splitlines()
if len(rows) != 100_000:
    raise SystemExit("expected the Cycle-6 100000-row prefix")
chosen = [row for decile in range(10) for row in rows[decile * 10_000:decile * 10_000 + 100]]
if len(chosen) != 1_000:
    raise SystemExit("stratum construction failed")
target.write_text("\n".join(chosen) + "\n")
print(f"stratified_rows={len(chosen)}")
