#!/usr/bin/env python3
"""Frozen finite falsifier for Cycle 113; floating output has no proof role."""
from __future__ import annotations

import argparse
import json
from math import gcd, sqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from conventions.irrational_weighted_split_v1 import floating_split_sum

OUTPUT = ROOT / "discovery/cycle-113-irrational-weighted-falsifier-v1.json"


def run() -> dict[str, object]:
    best = (-1.0, None)
    best_scaled = (-1.0, None)
    rows = 0
    for d in range(2, 121):
        for N in range(1, 121):
            for R in range(1, 121):
                if gcd(N, R) != 1 or not 0.5 <= N / R <= 2.0:
                    continue
                value = floating_split_sum(d=d, N=N, R=R)
                rows += 1
                if value > best[0]:
                    best = (value, [d, N, R])
                if sqrt(d) * value > best_scaled[0]:
                    best_scaled = (sqrt(d) * value, [d, N, R, value])
    return {
        "epistemic_status": "OBSERVED", "proof_role": "none", "rows": rows,
        "box": {"max_degree": 120, "max_label_coordinate": 120, "ratio": [0.5, 2.0]},
        "maximum": best[0], "maximum_witness": best[1],
        "scaled_maximum": best_scaled[0], "scaled_witness": best_scaled[1],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = run()
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        if OUTPUT.exists():
            raise SystemExit("refusing to overwrite discovery output")
        OUTPUT.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
