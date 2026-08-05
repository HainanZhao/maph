#!/usr/bin/env python3
"""Explore the C68 normalized gradient on the frozen 11^5 grid.

Floating evaluation selects a proof engine; it never certifies exclusion.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


VARIABLES = ("x", "y", "z", "v", "lambda")


def load_dense(path: Path) -> np.ndarray:
    terms = []
    degrees = [0] * 5
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in VARIABLES)
            coefficient = int(row["numerator"]) / int(row["denominator"])
            terms.append((exponent, coefficient))
            degrees = [max(a, b) for a, b in zip(degrees, exponent, strict=True)]
    coefficients = np.zeros(tuple(degree + 1 for degree in degrees), dtype=np.longdouble)
    for exponent, coefficient in terms:
        coefficients[exponent] += coefficient
    return coefficients


def evaluate_grid(coefficients: np.ndarray, grid: np.ndarray) -> np.ndarray:
    powers = [np.power.outer(grid, np.arange(degree, dtype=int)) for degree in coefficients.shape]
    return np.einsum(
        "abcde,ia,jb,kc,ld,me->ijklm",
        coefficients,
        *powers,
        optimize=True,
        dtype=np.longdouble,
    )


def summarize(values: np.ndarray) -> dict[str, float | int]:
    return {
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "negative": int(np.count_nonzero(values < 0)),
        "zero": int(np.count_nonzero(values == 0)),
        "positive": int(np.count_nonzero(values > 0)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("polynomial_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    grid = np.arange(11, dtype=np.longdouble) / 10
    interior = np.s_[1:10, 1:10, 1:10, 1:10, 1:10]

    X = grid[:, None, None, None, None]
    Y = grid[None, :, None, None, None]
    Z0 = grid[None, None, :, None, None]
    t = (1 - X) * Y / 3
    c2 = ((1 - X) * (1 - Y) / 2) ** 2
    payload = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "grid_denominator": 10,
        "rows": 2 * 11**5,
        "claim_boundary": "Floating grid engine selection only; not an exclusion or sign certificate.",
        "regimes": {},
    }
    for regime in ("low", "high"):
        pu = evaluate_grid(load_dense(args.polynomial_dir / f"P_u-{regime}.tsv"), grid)
        ps = evaluate_grid(load_dense(args.polynomial_dir / f"P_s2-{regime}.tsv"), grid)
        Z = Z0 / 2 if regime == "low" else (1 + Z0) / 2
        du = 4 * t**3 * Z**3 if regime == "low" else t**3 * (2 * Z**3 - 3 * Z**2 + 1)
        plambda = pu * du
        pv = ps * c2
        pl_i = plambda[interior]
        pv_i = pv[interior]
        scale = np.maximum(np.abs(pl_i), np.abs(pv_i))
        near = np.hypot(pl_i, pv_i) <= np.maximum(scale * np.longdouble("1e-8"), np.longdouble("1e-30"))

        # A fixed positive combination is a cheap candidate only if all sampled
        # values have one sign.  Search frozen small integer slopes.
        combinations = []
        for a in range(-8, 9):
            for b in range(-8, 9):
                if not a and not b:
                    continue
                value = a * pl_i + b * pv_i
                if np.all(value > 0) or np.all(value < 0):
                    combinations.append({"a": a, "b": b, "sign": 1 if np.all(value > 0) else -1})
        payload["regimes"][regime] = {
            "P_lambda_full": summarize(plambda),
            "P_v_full": summarize(pv),
            "P_lambda_interior": summarize(pl_i),
            "P_v_interior": summarize(pv_i),
            "near_stationary_interior": int(np.count_nonzero(near)),
            "fixed_integer_separators": combinations,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
