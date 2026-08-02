#!/usr/bin/env python3
"""Preregistered Cycle 88 finite-scale signed-moment profiler."""
from __future__ import annotations

import argparse
import json
import math
import platform
from fractions import Fraction
from pathlib import Path

import numpy as np


D_VALUES = (64, 96, 128, 192, 256, 384)
ANCHORS = (Fraction(3, 2), Fraction(5, 3), Fraction(8, 5))
XI_VALUES = (
    Fraction(16, 25),
    Fraction(7, 10),
    Fraction(58, 75),
    Fraction(9, 10),
    Fraction(83, 75),
)
OUTPUT = Path(__file__).with_name("cycle-88-signed-moment-profiler-v1.json")


def geometric_block(x: np.ndarray, q_length: int) -> np.ndarray:
    """sum_{q=Q}^{2Q-1} exp(2 pi i q x), with Q=q_length."""
    nearest = np.rint(x)
    singular = np.abs(x - nearest) < 1e-12
    denominator = np.sin(np.pi * x)
    phase = np.exp(2j * np.pi * (q_length + (q_length - 1) / 2) * x)
    with np.errstate(divide="ignore", invalid="ignore"):
        values = phase * np.sin(np.pi * q_length * x) / denominator
    values[singular] = q_length
    return values


def one_row(D: int, anchor: Fraction, xi: Fraction) -> dict[str, object]:
    q_length = max(2, round(D ** (5 / 9)))
    K = max(2, round(D ** (float(xi) / (3 / 5))))
    d = np.arange(math.ceil(D / 4), math.ceil(3 * D / 4), dtype=np.float64)
    y = float(anchor) * np.exp(2 * np.pi * d / D)
    values = np.empty(K, dtype=np.complex128)
    chunk = 2048
    for start in range(0, K, chunk):
        stop = min(K, start + chunk)
        k = np.arange(K + start, K + stop, dtype=np.float64)[:, None]
        x = np.remainder(k * y[None, :], 1.0)
        values[start:stop] = geometric_block(x, q_length).sum(axis=1)
    if not np.all(np.isfinite(values)):
        raise RuntimeError("nonfinite signed moment row")
    atom_count = len(d) * q_length
    abs_values = np.abs(values)
    order = np.argsort(abs_values)[-5:][::-1]
    return {
        "D": D,
        "Q": q_length,
        "K": K,
        "anchor": f"{anchor.numerator}/{anchor.denominator}",
        "xi": f"{xi.numerator}/{xi.denominator}",
        "d_count": len(d),
        "atom_count": atom_count,
        "m2_over_KN": float(np.sum(abs_values**2) / (K * atom_count)),
        "l1_over_KsqrtN": float(np.sum(abs_values) / (K * math.sqrt(atom_count))),
        "max_over_sqrtN": float(np.max(abs_values) / math.sqrt(atom_count)),
        "top5": [
            {
                "k": int(K + index),
                "over_sqrtN": float(abs_values[index] / math.sqrt(atom_count)),
            }
            for index in order
        ],
    }


def slope_classification(rows: list[dict[str, object]]) -> dict[str, object]:
    x = np.log(np.array([row["D"] for row in rows], dtype=np.float64))
    y = np.log(np.array([row["m2_over_KN"] for row in rows], dtype=np.float64))
    slope = float(np.polyfit(x, y, 1)[0])
    if slope > 0.15:
        label = "OBSERVED_GROWING"
    elif slope < -0.15:
        label = "OBSERVED_DECAYING"
    else:
        label = "OBSERVED_FLAT"
    return {"slope": slope, "classification": label}


def build_payload() -> dict[str, object]:
    rows = [
        one_row(D, anchor, xi)
        for anchor in ANCHORS
        for xi in XI_VALUES
        for D in D_VALUES
    ]
    summaries = []
    for anchor in ANCHORS:
        for xi in XI_VALUES:
            selected = [
                row
                for row in rows
                if row["anchor"] == f"{anchor.numerator}/{anchor.denominator}"
                and row["xi"] == f"{xi.numerator}/{xi.denominator}"
            ]
            summaries.append(
                {
                    "anchor": f"{anchor.numerator}/{anchor.denominator}",
                    "xi": f"{xi.numerator}/{xi.denominator}",
                    **slope_classification(selected),
                }
            )
    payload = {
        "epistemic_status": "OBSERVED",
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
        "rows": rows,
        "summaries": summaries,
        "claim_boundary": "Finite-scale deterministic discovery only; no proof promotion.",
    }
    return payload


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
