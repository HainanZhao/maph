#!/usr/bin/env python3
"""Build the six secondary C68 tangent-equality blow-up charts."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


Exponent = tuple[int, int, int, int, int]
Polynomial = dict[Exponent, Fraction]


def load(path: Path) -> Polynomial:
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    with path.open(newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        for row in rows:
            exponent = tuple(int(row[name]) for name in ("x", "y", "z", "v", "lambda"))
            result[exponent] += Fraction(int(row["numerator"]), int(row["denominator"]))
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def relative_exponents(scales: tuple[int, int, int], dominant: int) -> tuple[int, int, int]:
    relatives = tuple(scales[index] for index in range(3) if index != dominant)
    return sum(scales), relatives[0], relatives[1]


def transform(polynomial: Polynomial, side: str, dominant: int) -> tuple[Polynomial, int, int]:
    # Input positional coordinates are (retained_z, lambda, rho, a, b).
    degree_a = max(exponent[3] for exponent in polynomial)
    constant, linear = (2, -2) if side == "below" else (2, 1)
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for (iz, il, irho, ia, ib), coefficient in polynomial.items():
        for s_power in range(ia + 1):
            multiplier = (
                math.comb(ia, s_power)
                * constant ** (ia - s_power)
                * linear**s_power
                * 3 ** (degree_a - ia)
            )
            eta_power, first_relative, second_relative = relative_exponents(
                (s_power, irho, ib), dominant
            )
            result[(iz, il, eta_power, first_relative, second_relative)] += coefficient * multiplier
    result = defaultdict(Fraction, {exponent: coefficient for exponent, coefficient in result.items() if coefficient})
    radial_order = min(exponent[2] for exponent in result)
    if radial_order < 1:
        raise AssertionError("secondary tangent chart has no common radial factor")
    quotient = {
        (e[0], e[1], e[2] - radial_order, e[3], e[4]): coefficient
        for e, coefficient in result.items()
    }
    return quotient, radial_order, degree_a


def evaluate(polynomial: Polynomial, point: tuple[Fraction, ...]) -> Fraction:
    return sum(
        coefficient * math.prod(value**power for value, power in zip(point, exponent, strict=True))
        for exponent, coefficient in polynomial.items()
    )


def source_point(side: str, dominant: int, output: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    retained_z, lam, eta, first_relative, second_relative = output
    relatives = iter((first_relative, second_relative))
    s, rho, b = tuple(eta if index == dominant else eta * next(relatives) for index in range(3))
    a = 2 * (1 - s) / 3 if side == "below" else (2 + s) / 3
    return retained_z, lam, rho, a, b


def write(path: Path, polynomial: Polynomial) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("x", "y", "z", "v", "lambda", "numerator", "denominator"))
        for exponent, coefficient in sorted(polynomial.items()):
            writer.writerow((*exponent, coefficient.numerator, coefficient.denominator))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary_chart", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    original = load(args.primary_chart)
    control = (Fraction(2, 5), Fraction(3, 7), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2))
    scale_names = ("ratio_distance", "primary_rho", "cycle_relative")
    report = {}
    for side in ("below", "above"):
        for dominant in range(3):
            quotient, radial_order, degree_a = transform(original, side, dominant)
            source = source_point(side, dominant, control)
            expected = 3**degree_a * evaluate(original, source)
            observed = control[2] ** radial_order * evaluate(quotient, control)
            if expected != observed:
                raise AssertionError(f"secondary exact control failed: {side}/{dominant}")
            name = f"tangent-{side}-{scale_names[dominant]}-dominant"
            write(args.output_dir / f"{name}.tsv", quotient)
            report[name] = {
                "side": side,
                "dominant_scale": scale_names[dominant],
                "all_scales": scale_names,
                "output_coordinate_order": [
                    "retained_transposition_shape_z",
                    "lambda",
                    "eta",
                    "relative_scale_1",
                    "relative_scale_2",
                ],
                "clearing_factor": f"3^{degree_a}",
                "removed_radial_factor": f"eta^{radial_order}",
                "terms": len(quotient),
                "degrees": [max(exponent[axis] for exponent in quotient) for axis in range(5)],
                "exact_rational_control": "PASS",
            }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "source_chart": args.primary_chart.name,
        "coverage": {
            "below": "a=2*(1-s)/3 covers 0<=a<=2/3",
            "above": "a=(2+s)/3 covers 2/3<=a<=1",
            "scales": ["s", "primary_rho", "cycle_relative_b"],
            "dominant_rule": "eta=max(scales), other scales=eta*relative",
        },
        "charts": report,
        "claim_boundary": "Exact secondary blow-up construction and radial division only; signs remain open.",
    }
    (args.output_dir / "secondary-blowup-summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
