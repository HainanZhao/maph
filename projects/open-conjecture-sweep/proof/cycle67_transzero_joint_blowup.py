#!/usr/bin/env python3
"""Build exact joint charts around the trans-zero line x=1/3, r=0."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path


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
    result: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    for (ix, iy, ir, ih), coefficient in polynomial.items():
        for s_power in range(ix + 1):
            linear = -1 if side == "below" else 2
            s_coefficient = comb(ix, s_power) * linear**s_power * 3 ** (x_degree - ix)
            rho_power = s_power + ir
            k_power = ir if mode == "curve_dominant" else s_power
            result[(iy, ih, rho_power, k_power)] += coefficient * s_coefficient
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
    for path in sorted(args.chart_dir.glob("trans_zero*.tsv")):
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
                source_x = (1 - curve_distance) / 3 if side == "below" else (1 + 2 * curve_distance) / 3
                expected = 3**x_degree * evaluate(original, (source_x, mass_y, radial, shape)) / rho**radial_order
                assert evaluate(quotient, control) == expected, name
                report[name] = {
                    "radial_factor": f"rho^{radial_order}",
                    "clearing_factor": f"3^{x_degree}",
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
                    "below: x=(1-s)/3",
                    "above: x=(1+2s)/3",
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
