#!/usr/bin/env python3
"""Build the twelve exact C68 secant equality blow-up charts."""

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
        expected = ("x", "y", "z", "v", "lambda", "numerator", "denominator")
        if tuple(rows.fieldnames or ()) != expected:
            raise ValueError(f"unexpected header in {path}")
        for row in rows:
            exponent = tuple(int(row[name]) for name in expected[:5])
            result[exponent] += Fraction(int(row["numerator"]), int(row["denominator"]))
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def linear_power(constant: int, linear: int, degree: int) -> dict[int, int]:
    return {
        power: math.comb(degree, power) * constant ** (degree - power) * linear**power
        for power in range(degree + 1)
    }


def convolve(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    result: defaultdict[int, int] = defaultdict(int)
    for a, ac in left.items():
        for b, bc in right.items():
            result[a + b] += ac * bc
    return dict(result)


def relative_exponents(scales: tuple[int, int, int], dominant: int) -> tuple[int, int, int]:
    relatives = tuple(scales[index] for index in range(3) if index != dominant)
    return sum(scales), relatives[0], relatives[1]


def transform_low(polynomial: Polynomial, side: str, dominant: int) -> tuple[Polynomial, int, int]:
    degree_x = max(exponent[0] for exponent in polynomial)
    one_minus = [linear_power(1, -1, degree) for degree in range(degree_x + 1)]
    three_minus = [linear_power(3, -1, degree) for degree in range(degree_x + 1)]
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for (ix, iy, iz, iv, il), coefficient in polynomial.items():
        for s_power in range(ix + 1):
            if side == "below":
                s_coefficient = math.comb(ix, s_power) * (-1) ** s_power
                y_numerator = one_minus[ix]
            elif side == "above":
                s_coefficient = math.comb(ix, s_power) * 2**s_power
                y_numerator = one_minus[ix - s_power]
            else:
                raise ValueError(side)
            y_factor = convolve(y_numerator, three_minus[degree_x - ix])
            rho_power, first_relative, second_relative = relative_exponents(
                (s_power, iz, iv), dominant
            )
            for y_added, y_coefficient in y_factor.items():
                exponent = (
                    iy + y_added,
                    il,
                    rho_power,
                    first_relative,
                    second_relative,
                )
                result[exponent] += coefficient * s_coefficient * y_coefficient
    result = defaultdict(Fraction, {e: c for e, c in result.items() if c})
    radial_order = min(exponent[2] for exponent in result)
    if radial_order < 1:
        raise AssertionError("low equality chart has no common radial factor")
    quotient = {
        (e[0], e[1], e[2] - radial_order, e[3], e[4]): coefficient
        for e, coefficient in result.items()
    }
    return quotient, radial_order, degree_x


def transform_high(polynomial: Polynomial, side: str, dominant: int) -> tuple[Polynomial, int, int]:
    degree_x = max(exponent[0] for exponent in polynomial)
    linear = -1 if side == "below" else 2
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for (ix, iy, iz, iv, il), coefficient in polynomial.items():
        for s_power in range(ix + 1):
            multiplier = math.comb(ix, s_power) * linear**s_power * 3 ** (degree_x - ix)
            rho_power, first_relative, second_relative = relative_exponents(
                (s_power, iy, iv), dominant
            )
            exponent = (iz, il, rho_power, first_relative, second_relative)
            result[exponent] += coefficient * multiplier
    result = defaultdict(Fraction, {e: c for e, c in result.items() if c})
    radial_order = min(exponent[2] for exponent in result)
    if radial_order < 1:
        raise AssertionError("high equality chart has no common radial factor")
    quotient = {
        (e[0], e[1], e[2] - radial_order, e[3], e[4]): coefficient
        for e, coefficient in result.items()
    }
    return quotient, radial_order, degree_x


def evaluate(polynomial: Polynomial, point: tuple[Fraction, ...]) -> Fraction:
    return sum(
        coefficient * math.prod(value**power for value, power in zip(point, exponent, strict=True))
        for exponent, coefficient in polynomial.items()
    )


def source_point(
    regime: str,
    side: str,
    dominant: int,
    output_point: tuple[Fraction, ...],
) -> tuple[tuple[Fraction, ...], Fraction]:
    retained, lam, rho, first_relative, second_relative = output_point
    relatives = iter((first_relative, second_relative))
    scales = tuple(rho if index == dominant else rho * next(relatives) for index in range(3))
    if regime == "low":
        distance, z, v = scales
        y = retained
        denominator = 3 - y
        x = (
            (1 - y) * (1 - distance) / denominator
            if side == "below"
            else (1 - y + 2 * distance) / denominator
        )
        return (x, y, z, v, lam), denominator
    distance, y, v = scales
    z = retained
    x = (1 - distance) / 3 if side == "below" else (1 + 2 * distance) / 3
    return (x, y, z, v, lam), Fraction(3)


def write(path: Path, polynomial: Polynomial) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        # The exact tensor engine uses positional coordinates.  Their semantic
        # meanings are frozen in the report's output_coordinate_order field.
        writer.writerow(("x", "y", "z", "v", "lambda", "numerator", "denominator"))
        for exponent, coefficient in sorted(polynomial.items()):
            writer.writerow((*exponent, coefficient.numerator, coefficient.denominator))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stripped_secant_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    control = (Fraction(2, 5), Fraction(3, 7), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2))
    report = {}
    dominant_names = ("distance", "second_scale", "cycle")
    for regime in ("low", "high"):
        original = load(args.stripped_secant_dir / f"secant-{regime}.tsv")
        for side in ("below", "above"):
            for dominant in range(3):
                if regime == "low":
                    quotient, radial_order, degree_x = transform_low(original, side, dominant)
                    scale_names = ("curve_distance", "transposition_radius_z", "cycle_radius_v")
                    retained_name = "class_mass_y"
                else:
                    quotient, radial_order, degree_x = transform_high(original, side, dominant)
                    scale_names = ("x_distance", "transposition_mass_y", "cycle_radius_v")
                    retained_name = "transposition_shape_z"
                source, denominator = source_point(regime, side, dominant, control)
                expected = denominator**degree_x * evaluate(original, source)
                observed = control[2] ** radial_order * evaluate(quotient, control)
                if expected != observed:
                    raise AssertionError(f"exact blow-up control failed: {regime}/{side}/{dominant}")
                name = f"{regime}-{side}-{dominant_names[dominant]}-dominant"
                write(args.output_dir / f"{name}.tsv", quotient)
                report[name] = {
                    "source_regime": regime,
                    "side": side,
                    "dominant_scale": scale_names[dominant],
                    "all_scales": scale_names,
                    "output_coordinate_order": [
                        retained_name,
                        "lambda",
                        "rho",
                        "relative_scale_1",
                        "relative_scale_2",
                    ],
                    "clearing_factor": (
                        f"(3-y)^{degree_x}" if regime == "low" else f"3^{degree_x}"
                    ),
                    "removed_radial_factor": f"rho^{radial_order}",
                    "terms": len(quotient),
                    "degrees": [max(exponent[axis] for exponent in quotient) for axis in range(5)],
                    "exact_rational_control": "PASS",
                }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "coverage": {
            "low_sides": ["x=(1-y)*(1-s)/(3-y)", "x=(1-y+2*s)/(3-y)"],
            "low_scales": ["s", "z", "v"],
            "high_sides": ["x=(1-s)/3", "x=(1+2*s)/3"],
            "high_scales": ["s", "y", "v"],
            "dominant_rule": "rho=max(scales), other scales=rho*relative; three charts per side",
        },
        "charts": report,
        "claim_boundary": "Exact complete blow-up construction and radial division only; quotient signs remain open.",
    }
    (args.output_dir / "blowup-summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
