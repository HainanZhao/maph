#!/usr/bin/env python3
"""Divide the cycle/trans-equal r=0 Hessian faces by their zero curve."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import sympy


def load_r_zero(path: Path, x, y, h):
    terms: defaultdict[tuple[int, int, int], int] = defaultdict(int)
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            exponent = tuple(map(int, row[:4]))
            if exponent[2] == 0:
                terms[(exponent[0], exponent[1], exponent[3])] += int(row[4])
    return sympy.Poly(
        sum(c * x**e[0] * y**e[1] * h**e[2] for e, c in terms.items() if c),
        x,
        y,
        h,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    x, y, h = sympy.symbols("x y h")
    curve = sympy.Poly((1 - y - 3 * x + x * y) ** 2, x, y, h)
    report = {}
    paths = list(args.chart_dir.glob("trans_equal*.tsv"))
    cycle_equal = args.chart_dir / "cycle_equal.tsv"
    if cycle_equal.exists():
        paths.append(cycle_equal)
    for path in sorted(paths):
        face = load_r_zero(path, x, y, h)
        quotient, remainder = sympy.div(face, curve)
        assert remainder.is_zero
        target = args.output_dir / path.name
        with target.open("w", newline="") as handle:
            rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
            rows.writerow(("x", "y", "r", "h", "coefficient_scaled_64_times_6_pow_15"))
            for exponent, coefficient in sorted(quotient.terms()):
                assert coefficient.q == 1
                rows.writerow((exponent[0], exponent[1], 0, exponent[2], int(coefficient)))
        report[path.stem] = {
            "input_terms": len(face.terms()),
            "quotient_terms": len(quotient.terms()),
            "quotient_degrees_x_y_h": quotient.degree_list(),
            "exact_zero_remainder": True,
        }
    (args.output_dir / "hessian-factor-report.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "scope": "exact r=0 restrictions",
                "factor": "(1-y-3*x+x*y)^2",
                "sympy_version": sympy.__version__,
                "charts": report,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
