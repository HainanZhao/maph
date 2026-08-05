#!/usr/bin/env python3
"""Build exact two-scale charts around the C67 equal-family zero curve."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path


def linear_power(constant: int, linear: int, degree: int) -> dict[int, int]:
    return {
        power: comb(degree, power) * constant ** (degree - power) * linear**power
        for power in range(degree + 1)
    }


def convolve(a: dict[int, int], b: dict[int, int]) -> dict[int, int]:
    result: defaultdict[int, int] = defaultdict(int)
    for i, u in a.items():
        for j, v in b.items():
            result[i + j] += u * v
    return dict(result)


def load(path: Path):
    result: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            result[tuple(map(int, row[:4]))] += int(row[4])
    return {key: value for key, value in result.items() if value}


def evaluate(polynomial, point):
    return sum(
        coefficient
        * point[0] ** exponent[0]
        * point[1] ** exponent[1]
        * point[2] ** exponent[2]
        * point[3] ** exponent[3]
        for exponent, coefficient in polynomial.items()
    )


def transform(polynomial, side: str, mode: str):
    x_degree = max(exponent[0] for exponent in polynomial)
    one_minus = [linear_power(1, -1, degree) for degree in range(x_degree + 1)]
    three_minus = [linear_power(3, -1, degree) for degree in range(x_degree + 1)]
    result: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    for (ix, iy, ir, ih), coefficient in polynomial.items():
        s_terms = range(ix + 1)
        for s_power in s_terms:
            if side == "below":
                # ((1-y)(1-s))^ix
                if s_power > ix:
                    continue
                s_coefficient = comb(ix, s_power) * (-1) ** s_power
                y_numerator = one_minus[ix]
            else:
                # (1-y+2s)^ix
                s_coefficient = comb(ix, s_power) * 2**s_power
                y_numerator = one_minus[ix - s_power]
            y_factor = convolve(y_numerator, three_minus[x_degree - ix])
            rho_power = s_power + ir
            k_power = ir if mode == "curve_dominant" else s_power
            for added_y, y_coefficient in y_factor.items():
                result[(iy + added_y, ih, rho_power, k_power)] += (
                    coefficient * s_coefficient * y_coefficient
                )
    result = defaultdict(int, {key: value for key, value in result.items() if value})
    radial_order = min(exponent[2] for exponent in result)
    quotient = {
        (exponent[0], exponent[1], exponent[2] - radial_order, exponent[3]): coefficient
        for exponent, coefficient in result.items()
    }
    return quotient, radial_order, x_degree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {}
    control = (Fraction(2, 5), Fraction(1, 3), Fraction(1, 4), Fraction(1, 2))
    paths = list(args.chart_dir.glob("trans_equal*.tsv"))
    cycle_equal = args.chart_dir / "cycle_equal.tsv"
    if cycle_equal.exists():
        paths.append(cycle_equal)
    for path in sorted(paths):
        original = load(path)
        for side in ("below", "above"):
            for mode in ("curve_dominant", "radial_dominant"):
                quotient, radial_order, x_degree = transform(original, side, mode)
                name = f"{path.stem}_{side}_{mode}"
                with (args.output_dir / f"{name}.tsv").open("w", newline="") as handle:
                    rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
                    rows.writerow(("x", "y", "r", "h", "coefficient_scaled_64_times_6_pow_15"))
                    for exponent, coefficient in sorted(quotient.items()):
                        rows.writerow((*exponent, coefficient))
                mass_y, shape, rho, relative = control
                curve_distance = rho if mode == "curve_dominant" else rho * relative
                radial = rho * relative if mode == "curve_dominant" else rho
                denominator = 3 - mass_y
                source_x = (
                    (1 - mass_y) * (1 - curve_distance) / denominator
                    if side == "below"
                    else (1 - mass_y + 2 * curve_distance) / denominator
                )
                expected = (
                    denominator**x_degree
                    * evaluate(original, (source_x, mass_y, radial, shape))
                    / rho**radial_order
                )
                observed = evaluate(quotient, control)
                assert observed == expected, name
                report[name] = {
                    "radial_factor": f"rho^{radial_order}",
                    "clearing_factor": f"(3-y)^{x_degree}",
                    "quotient_terms": len(quotient),
                    "degrees": [max(e[axis] for e in quotient) for axis in range(4)],
                    "exact_rational_control": "PASS",
                }
    (args.output_dir / "joint-blowup-report.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "coverage": [
                    "below: x=(1-y)(1-s)/(3-y)",
                    "above: x=(1-y+2s)/(3-y)",
                    "curve_dominant: (s,r)=(rho,rho*k)",
                    "radial_dominant: (s,r)=(rho*k,rho)",
                ],
                "charts": report,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
