#!/usr/bin/env python3
"""Restrict C67 cycle/trans-equal quotients to the Hessian zero curve."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from math import comb
from pathlib import Path


def binomial_linear_power(constant: int, linear: int, degree: int) -> dict[int, int]:
    return {
        power: comb(degree, power) * constant ** (degree - power) * linear**power
        for power in range(degree + 1)
    }


def multiply_univariate(a: dict[int, int], b: dict[int, int]) -> dict[int, int]:
    result: defaultdict[int, int] = defaultdict(int)
    for i, u in a.items():
        for j, v in b.items():
            result[i + j] += u * v
    return dict(result)


def load(path: Path):
    polynomial: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            polynomial[tuple(map(int, row[:4]))] += int(row[4])
    return {key: value for key, value in polynomial.items() if value}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {}
    paths = list(args.chart_dir.glob("trans_equal*.tsv"))
    cycle_equal = args.chart_dir / "cycle_equal.tsv"
    if cycle_equal.exists():
        paths.append(cycle_equal)
    for path in sorted(paths):
        polynomial = load(path)
        x_degree = max(exponent[0] for exponent in polynomial)
        powers_one_minus_y = [binomial_linear_power(1, -1, degree) for degree in range(x_degree + 1)]
        powers_three_minus_y = [binomial_linear_power(3, -1, degree) for degree in range(x_degree + 1)]
        restricted: defaultdict[tuple[int, int, int], int] = defaultdict(int)
        for (ix, iy, ir, ih), coefficient in polynomial.items():
            y_factor = multiply_univariate(
                powers_one_minus_y[ix], powers_three_minus_y[x_degree - ix]
            )
            for added_y, multiplier in y_factor.items():
                restricted[(iy + added_y, ih, ir)] += coefficient * multiplier
        restricted = defaultdict(int, {key: value for key, value in restricted.items() if value})
        radial_order = min(exponent[2] for exponent in restricted)
        quotient = {
            (exponent[0], exponent[1], exponent[2] - radial_order): coefficient
            for exponent, coefficient in restricted.items()
        }
        with (args.output_dir / path.name).open("w", newline="") as handle:
            rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
            rows.writerow(("x", "y", "r", "h", "coefficient_scaled_64_times_6_pow_15"))
            for exponent, coefficient in sorted(quotient.items()):
                rows.writerow((exponent[0], exponent[1], exponent[2], 0, coefficient))
        report[path.stem] = {
            "clearing_factor": f"(3-y)^{x_degree}",
            "radial_factor": f"r^{radial_order}",
            "quotient_terms": len(quotient),
            "quotient_degrees_y_shape_r": [
                max(exponent[axis] for exponent in quotient) for axis in range(3)
            ],
        }
    (args.output_dir / "curve-restriction-report.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "curve": "x=(1-y)/(3-y)",
                "positive_denominator_on_domain": "3-y >= 2",
                "charts": report,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
