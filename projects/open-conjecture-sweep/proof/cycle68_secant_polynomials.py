#!/usr/bin/env python3
"""Construct the exact C68 cycle-face secant quotient on both cube charts."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


OrbitExponent = tuple[int, int, int, int, int, int]
CubeExponent = tuple[int, int, int, int, int]
ZLambdaExponent = tuple[int, int]


def load_orbit(path: Path) -> dict[OrbitExponent, Fraction]:
    result: defaultdict[OrbitExponent, Fraction] = defaultdict(Fraction)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if int(row["w"]) != 0:
                raise ValueError("nonzero w exponent in frozen orbit polynomial")
            exponent = tuple(int(row[name]) for name in ("e", "t", "c", "r2", "u", "s2"))
            result[exponent] += Fraction(int(row["numerator"]), int(row["denominator"]))
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def secant_invariant(orbit: dict[OrbitExponent, Fraction]) -> dict[OrbitExponent, Fraction]:
    quotient: defaultdict[OrbitExponent, Fraction] = defaultdict(Fraction)
    reconstructed: defaultdict[OrbitExponent, Fraction] = defaultdict(Fraction)
    for exponent, coefficient in orbit.items():
        if exponent[5] == 0:
            reconstructed[exponent] += coefficient
            continue
        shifted = exponent[:5] + (exponent[5] - 1,)
        quotient[shifted] += coefficient
        reconstructed[shifted[:5] + (shifted[5] + 1,)] += coefficient
    if {e: c for e, c in reconstructed.items() if c} != orbit:
        raise AssertionError("coefficientwise secant reconstruction failed")
    return {exponent: coefficient for exponent, coefficient in quotient.items() if coefficient}


def add2(*polynomials: dict[ZLambdaExponent, Fraction]) -> dict[ZLambdaExponent, Fraction]:
    result: defaultdict[ZLambdaExponent, Fraction] = defaultdict(Fraction)
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] += coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def scale2(polynomial: dict[ZLambdaExponent, Fraction], scalar: Fraction) -> dict[ZLambdaExponent, Fraction]:
    return {exponent: coefficient * scalar for exponent, coefficient in polynomial.items() if coefficient * scalar}


def mul2(left: dict[ZLambdaExponent, Fraction], right: dict[ZLambdaExponent, Fraction]) -> dict[ZLambdaExponent, Fraction]:
    result: defaultdict[ZLambdaExponent, Fraction] = defaultdict(Fraction)
    for (az, al), ac in left.items():
        for (bz, bl), bc in right.items():
            result[(az + bz, al + bl)] += ac * bc
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def power2(polynomial: dict[ZLambdaExponent, Fraction], exponent: int) -> dict[ZLambdaExponent, Fraction]:
    result = {(0, 0): Fraction(1)}
    base = polynomial
    while exponent:
        if exponent & 1:
            result = mul2(result, base)
        exponent //= 2
        if exponent:
            base = mul2(base, base)
    return result


def zlambda_forms(regime: str) -> tuple[dict[ZLambdaExponent, Fraction], dict[ZLambdaExponent, Fraction]]:
    if regime == "low":
        Z = {(1, 0): Fraction(1, 2)}
    elif regime == "high":
        Z = {(0, 0): Fraction(1, 2), (1, 0): Fraction(1, 2)}
    else:
        raise ValueError(regime)
    z2 = power2(Z, 2)
    z3 = mul2(z2, Z)
    u_minus = scale2(z3, 2) if regime == "low" else add2(scale2(z2, 3), {(0, 0): Fraction(-1)})
    if regime == "low":
        u_minus = scale2(u_minus, -1)
    u_plus = scale2(z3, 2)
    difference = add2(u_plus, scale2(u_minus, -1))
    interpolation = {(z_power, lambda_power + 1): coefficient for (z_power, lambda_power), coefficient in difference.items()}
    U = add2(u_minus, interpolation)
    return Z, U


def cube_secant(
    quotient: dict[OrbitExponent, Fraction], regime: str
) -> dict[CubeExponent, Fraction]:
    Z, U = zlambda_forms(regime)
    zlambda_cache: dict[tuple[int, int], dict[ZLambdaExponent, Fraction]] = {}
    result: defaultdict[CubeExponent, Fraction] = defaultdict(Fraction)
    for (e_power, t_power0, c_power0, r_power, u_power, s_power), coefficient in quotient.items():
        t_power = t_power0 + 2 * r_power + 3 * u_power
        c_power = c_power0 + 2 * s_power
        total_one_minus_x = t_power + c_power
        key = (r_power, u_power)
        if key not in zlambda_cache:
            zlambda_cache[key] = mul2(power2(Z, 2 * r_power), power2(U, u_power))
        scalar = coefficient * Fraction(6**r_power, 3**t_power * 2**c_power)
        for x_added in range(total_one_minus_x + 1):
            x_coefficient = Fraction(((-1) ** x_added) * math.comb(total_one_minus_x, x_added))
            for y_added in range(c_power + 1):
                xy_coefficient = x_coefficient * ((-1) ** y_added) * math.comb(c_power, y_added)
                for (z_power, lambda_power), zl_coefficient in zlambda_cache[key].items():
                    exponent = (
                        e_power + x_added,
                        t_power + y_added,
                        z_power,
                        s_power,
                        lambda_power,
                    )
                    result[exponent] += scalar * xy_coefficient * zl_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def orbit_value(polynomial: dict[OrbitExponent, Fraction], point: tuple[Fraction, ...]) -> Fraction:
    return sum(
        coefficient * math.prod(value**power for value, power in zip(point, exponent, strict=True))
        for exponent, coefficient in polynomial.items()
    )


def cube_value(polynomial: dict[CubeExponent, Fraction], point: tuple[Fraction, ...]) -> Fraction:
    return sum(
        coefficient * math.prod(value**power for value, power in zip(point, exponent, strict=True))
        for exponent, coefficient in polynomial.items()
    )


def invariant_point(regime: str, point: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    x, y, z, v, lam = point
    Z = z / 2 if regime == "low" else (1 + z) / 2
    e = x
    t = (1 - x) * y / 3
    c = (1 - x) * (1 - y) / 2
    r2 = 6 * t**2 * Z**2
    s2 = c**2 * v
    u_plus = 2 * t**3 * Z**3
    u_minus = -u_plus if regime == "low" else t**3 * (3 * Z**2 - 1)
    u = (1 - lam) * u_minus + lam * u_plus
    return e, t, c, r2, u, s2


def write_polynomial(path: Path, polynomial: dict[CubeExponent, Fraction]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("x", "y", "z", "v", "lambda", "numerator", "denominator"))
        for exponent, coefficient in sorted(polynomial.items()):
            writer.writerow((*exponent, coefficient.numerator, coefficient.denominator))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    orbit = load_orbit(args.orbit)
    quotient = secant_invariant(orbit)
    controls = (
        (Fraction(1, 5), Fraction(2, 5), Fraction(3, 7), Fraction(4, 9), Fraction(5, 11)),
        (Fraction(2, 7), Fraction(3, 8), Fraction(5, 9), Fraction(1, 3), Fraction(7, 13)),
    )
    summaries = {}
    for regime in ("low", "high"):
        polynomial = cube_secant(quotient, regime)
        for control in controls:
            point = invariant_point(regime, control)
            point_zero = point[:5] + (Fraction(),)
            source_difference = orbit_value(orbit, point) - orbit_value(orbit, point_zero)
            quotient_value = cube_value(polynomial, control)
            if source_difference != point[5] * quotient_value:
                raise AssertionError(f"secant control identity failed in {regime}")
            if quotient_value != orbit_value(quotient, point):
                raise AssertionError(f"invariant/cube quotient mismatch in {regime}")
        write_polynomial(args.output_dir / f"secant-{regime}.tsv", polynomial)
        summaries[regime] = {
            "terms": len(polynomial),
            "degrees": [max((exponent[axis] for exponent in polynomial), default=0) for axis in range(5)],
            "positive_coefficients": sum(coefficient > 0 for coefficient in polynomial.values()),
            "negative_coefficients": sum(coefficient < 0 for coefficient in polynomial.values()),
            "exact_rational_controls": len(controls),
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "invariant_orbit_terms": len(orbit),
        "invariant_secant_terms": len(quotient),
        "coefficientwise_identity": "P=P|s2=0+s2*G",
        "charts": summaries,
        "claim_boundary": "Exact secant construction and identities only; no sign conclusion.",
    }
    (args.output_dir / "secant-summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
