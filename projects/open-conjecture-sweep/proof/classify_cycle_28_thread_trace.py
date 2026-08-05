#!/usr/bin/env python3
"""Targeted one-thread classification of Cycle 28 base 3 / leaf 91."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time

if os.environ.get("OMP_NUM_THREADS") != "1" or os.environ.get("OPENBLAS_NUM_THREADS") != "1":
    raise SystemExit("OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1 are required")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import replay_cycle_28_portfolio_independent as independent

OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"
OUTPUT = OUT / "thread-trace-control.json"


def main() -> None:
    matches = [
        row for row in independent.read(independent.RESULTS)
        if (int(row["base_index"]), int(row["leaf_ordinal"])) == (3, 91)
    ]
    if len(matches) != 1:
        raise AssertionError("named row")
    started = time.monotonic()
    base, leaf, objective, rounds, cuts = independent.solve((matches[0], started + 300))
    value = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "base_index": base,
        "leaf_ordinal": leaf,
        "objective": objective,
        "rounds": rounds,
        "cuts": cuts,
        "primary_trace": {"objective": 1.0, "rounds": 28, "cuts": 80},
        "unpinned_independent_trace": {"objective": 1.0, "rounds": 26, "cuts": 74},
        "matches_primary_trace": (objective, rounds, cuts) == (1.0, 28, 80),
        "matches_unpinned_independent_trace": (objective, rounds, cuts) == (1.0, 26, 74),
        "wall_seconds": time.monotonic() - started,
        "environment": {"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"},
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
