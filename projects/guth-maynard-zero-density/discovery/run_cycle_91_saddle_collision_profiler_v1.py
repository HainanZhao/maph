#!/usr/bin/env python3
"""Preregistered Cycle 91 finite equal-height saddle-collision profiler."""
from __future__ import annotations

import argparse
import json
import math
import platform
from fractions import Fraction
from pathlib import Path

import numpy as np


D_VALUES = (512, 1024, 2048, 4096, 8192, 16384, 32768)
XI_VALUES = (Fraction(16, 25), Fraction(7, 10), Fraction(3, 4))
OUTPUT = Path(__file__).with_name("cycle-91-saddle-collision-profiler-v1.json")


def one_scale(D: int) -> dict[str, object]:
    q_length = max(2, round(D ** (5 / 9)))
    a_ceiling = math.floor(D * math.log(2) / (4 * math.pi))
    n = np.arange(q_length, 2 * q_length, dtype=np.float64)
    candidates: list[tuple[float, int, int, int]] = []
    for a in range(-a_ceiling, a_ceiling + 1):
        y = n * math.exp(2 * math.pi * a / D)
        n_prime = np.rint(y)
        if not np.all(np.isfinite(y)):
            raise RuntimeError("nonfinite collision row")
        valid = (n_prime >= q_length) & (n_prime < 2 * q_length)
        for index in np.nonzero(valid)[0]:
            nn = int(n[index])
            pp = int(n_prime[index])
            if a == 0 and pp == nn:
                continue
            candidates.append((float(abs(pp - y[index])), a, nn, pp))
    return {
        "D": D,
        "Q": q_length,
        "a_ceiling": a_ceiling,
        "diagonal_count": q_length,
        "candidates": candidates,
    }


def one_row(base: dict[str, object], xi: Fraction) -> dict[str, object]:
    D = int(base["D"])
    q_length = int(base["Q"])
    K = max(2, round(D ** (float(xi) / (3 / 5))))
    threshold = 1 / K
    retained = [row for row in base["candidates"] if row[0] <= threshold]
    by_a: dict[int, int] = {}
    by_n: dict[int, int] = {}
    for _, a, n, _ in retained:
        by_a[a] = by_a.get(a, 0) + 1
        by_n[n] = by_n.get(n, 0) + 1
    retained.sort()
    count = len(retained)
    safe_count = max(count, 1)
    volume = D * q_length / K
    return {
        "D": D,
        "Q": q_length,
        "K": K,
        "xi": f"{xi.numerator}/{xi.denominator}",
        "a_ceiling": base["a_ceiling"],
        "diagonal_count": base["diagonal_count"],
        "off_diagonal_count": count,
        "count_for_log": safe_count,
        "volume_model": volume,
        "count_over_volume": count / volume,
        "count_over_Q": count / q_length,
        "occupied_nonzero_a": len(by_a),
        "max_per_a": max(by_a.values(), default=0),
        "max_per_n": max(by_n.values(), default=0),
        "smallest_scaled_errors": [
            {
                "scaled_error": K * error,
                "a": a,
                "n": n,
                "n_prime": n_prime,
            }
            for error, a, n, n_prime in retained[:10]
        ],
    }


def slope(rows: list[dict[str, object]], key: str) -> float:
    x = np.log(np.array([row["D"] for row in rows], dtype=np.float64))
    y = np.log(np.array([row[key] for row in rows], dtype=np.float64))
    return float(np.polyfit(x, y, 1)[0])


def build_payload() -> dict[str, object]:
    bases = [one_scale(D) for D in D_VALUES]
    rows = [one_row(base, xi) for xi in XI_VALUES for base in bases]
    summaries = []
    for xi in XI_VALUES:
        label = f"{xi.numerator}/{xi.denominator}"
        selected = [row for row in rows if row["xi"] == label]
        count_slope = slope(selected, "count_for_log")
        volume_ratio_slope = slope(
            [
                {**row, "ratio_for_log": max(float(row["count_over_volume"]), 1e-300)}
                for row in selected
            ],
            "ratio_for_log",
        )
        q_ratio_slope = slope(
            [
                {**row, "ratio_for_log": max(float(row["count_over_Q"]), 1e-300)}
                for row in selected
            ],
            "ratio_for_log",
        )
        if q_ratio_slope > 0.15:
            classification = "OBSERVED_GROWING"
        elif q_ratio_slope < -0.15:
            classification = "OBSERVED_DECAYING"
        else:
            classification = "OBSERVED_FLAT"
        summaries.append(
            {
                "xi": label,
                "count_slope": count_slope,
                "count_over_volume_slope": volume_ratio_slope,
                "count_over_Q_slope": q_ratio_slope,
                "count_over_Q_classification": classification,
            }
        )
    return {
        "epistemic_status": "OBSERVED",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "rows": rows,
        "summaries": summaries,
        "claim_boundary": "Finite-scale deterministic discovery only; no proof promotion.",
    }


def encoded_payload() -> bytes:
    return (json.dumps(build_payload(), indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = encoded_payload()
    if args.write:
        if OUTPUT.exists():
            raise SystemExit(f"refusing to overwrite frozen output: {OUTPUT}")
        OUTPUT.write_bytes(encoded)
        print(OUTPUT)
    else:
        if not OUTPUT.exists():
            raise SystemExit(f"missing frozen output: {OUTPUT}")
        if OUTPUT.read_bytes() != encoded:
            raise SystemExit("frozen output differs from deterministic replay")
        print(f"replay matched: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

