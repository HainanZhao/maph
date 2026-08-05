#!/usr/bin/env python3
"""Build exact x/r blow-up charts for the final C67 cycle-zero corner."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
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


def transform(polynomial, mode: str):
    result: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    for (ix, iy, ir, ih), coefficient in polynomial.items():
        rho_power = ix + ir
        relative_power = ir if mode == "x_dominant" else ix
        result[(iy, ih, rho_power, relative_power)] += coefficient
    result = defaultdict(int, {key: value for key, value in result.items() if value})
    radial_order = min(exponent[2] for exponent in result)
    quotient = {
        (exponent[0], exponent[1], exponent[2] - radial_order, exponent[3]): coefficient
        for exponent, coefficient in result.items()
    }
    return quotient, radial_order


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    original = load(args.source)
    report = {}
    control = (Fraction(2, 5), Fraction(1, 3), Fraction(1, 4), Fraction(1, 2))
    for mode in ("x_dominant", "r_dominant"):
        quotient, radial_order = transform(original, mode)
        name = f"cycle_zero_cycle_dominant_corner_{mode}"
        with (args.output_dir / f"{name}.tsv").open("w", newline="") as handle:
            rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
            rows.writerow(("x", "y", "r", "h", "coefficient_scaled_64_times_6_pow_15"))
            for exponent, coefficient in sorted(quotient.items()):
                rows.writerow((*exponent, coefficient))
        mass_y, shape_h, rho, relative = control
        source_x = rho if mode == "x_dominant" else rho * relative
        source_r = rho * relative if mode == "x_dominant" else rho
        expected = evaluate(original, (source_x, mass_y, source_r, shape_h)) / rho**radial_order
        assert evaluate(quotient, control) == expected
        report[name] = {
            "radial_factor": f"rho^{radial_order}",
            "quotient_terms": len(quotient),
            "degrees": [max(e[axis] for e in quotient) for axis in range(4)],
            "exact_rational_control": "PASS",
        }
    (args.output_dir / "corner-blowup-report.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "coverage": [
                    "x_dominant: (x,r)=(rho,rho*k)",
                    "r_dominant: (x,r)=(rho*k,rho)",
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
