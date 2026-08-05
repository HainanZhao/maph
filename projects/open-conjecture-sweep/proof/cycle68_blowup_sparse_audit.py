#!/usr/bin/env python3
"""Independent sparse-rational coefficient audit for all C68 blow-up charts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import multiprocessing
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def load(path: Path) -> Polynomial:
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("x", "y", "z", "v", "lambda"))
            result[exponent] += Fraction(int(row["numerator"]), int(row["denominator"]))
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def add(*polynomials: Polynomial) -> Polynomial:
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] += coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {exponent: coefficient * scalar for exponent, coefficient in polynomial.items() if coefficient * scalar}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent, strict=True))
            result[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def power(polynomial: Polynomial, exponent: int, variables: int) -> Polynomial:
    result: Polynomial = {(0,) * variables: Fraction(1)}
    base = polynomial
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        exponent //= 2
        if exponent:
            base = multiply(base, base)
    return result


def bivariate_forms(side: str, degree_x: int, degree_mass: int) -> tuple[list[Polynomial], list[Polynomial], list[Polynomial]]:
    # Generic two-variable arithmetic in (retained mass, signed distance).
    one = {(0, 0): Fraction(1)}
    mass = {(1, 0): Fraction(1)}
    distance = {(0, 1): Fraction(1)}
    one_minus_mass = add(one, scale(mass, Fraction(-1)))
    denominator = add(scale(one, Fraction(3)), scale(mass, Fraction(-1)))
    numerator = (
        multiply(one_minus_mass, add(one, scale(distance, Fraction(-1))))
        if side == "below"
        else add(one_minus_mass, scale(distance, Fraction(2)))
    )
    return (
        [power(numerator, exponent, 2) for exponent in range(degree_x + 1)],
        [power(denominator, exponent, 2) for exponent in range(degree_x + 1)],
        [power(mass, exponent, 2) for exponent in range(degree_mass + 1)],
    )


def map_scales(scales: tuple[int, int, int], dominant: int) -> tuple[int, int, int]:
    relatives = tuple(scales[index] for index in range(3) if index != dominant)
    return sum(scales), relatives[0], relatives[1]


def quotient(transformed: Polynomial) -> tuple[Polynomial, int]:
    radial_order = min(exponent[2] for exponent in transformed)
    if radial_order < 1:
        raise AssertionError("missing common radial factor")
    return {
        (e[0], e[1], e[2] - radial_order, e[3], e[4]): coefficient
        for e, coefficient in transformed.items()
    }, radial_order


def audit_primary(task: tuple[str, str, str]) -> dict:
    source_dir, candidate_dir, name = task
    regime, side, dominant_name, _ = name.split("-")
    dominant = {"distance": 0, "second_scale": 1, "cycle": 2}[dominant_name]
    source = load(Path(source_dir) / f"secant-{regime}.tsv")
    degree_x = max(exponent[0] for exponent in source)
    transformed: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    if regime == "low":
        degree_y = max(exponent[1] for exponent in source)
        numerator_powers, denominator_powers, mass_powers = bivariate_forms(side, degree_x, degree_y)
        cache: dict[tuple[int, int], Polynomial] = {}
        for (ix, iy, iz, iv, il), coefficient in source.items():
            key = (ix, iy)
            if key not in cache:
                cache[key] = multiply(
                    multiply(numerator_powers[ix], denominator_powers[degree_x - ix]),
                    mass_powers[iy],
                )
            for (retained_power, distance_power), value in cache[key].items():
                rho_power, first_relative, second_relative = map_scales((distance_power, iz, iv), dominant)
                transformed[(retained_power, il, rho_power, first_relative, second_relative)] += coefficient * value
    else:
        one = {(0,): Fraction(1)}
        distance = {(1,): Fraction(1)}
        x_form = add(one, scale(distance, Fraction(-1) if side == "below" else 2))
        powers = [power(x_form, exponent, 1) for exponent in range(degree_x + 1)]
        for (ix, iy, iz, iv, il), coefficient in source.items():
            for (distance_power,), value in powers[ix].items():
                rho_power, first_relative, second_relative = map_scales((distance_power, iy, iv), dominant)
                transformed[(iz, il, rho_power, first_relative, second_relative)] += coefficient * value * 3 ** (degree_x - ix)
    rebuilt, radial_order = quotient({e: c for e, c in transformed.items() if c})
    candidate_path = Path(candidate_dir) / f"{name}.tsv"
    candidate = load(candidate_path)
    if rebuilt != candidate:
        raise AssertionError(f"primary sparse mismatch: {name}")
    return {"name": name, "route": "primary_sparse", "terms": len(candidate), "radial_order": radial_order,
            "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest()}


def audit_secondary(task: tuple[str, str, str]) -> dict:
    source_path, candidate_dir, name = task
    _, side, dominant_name, _ = name.split("-")
    dominant = {"ratio_distance": 0, "primary_rho": 1, "cycle_relative": 2}[dominant_name]
    source = load(Path(source_path)
    )
    degree_ratio = max(exponent[3] for exponent in source)
    one = {(0,): Fraction(1)}
    distance = {(1,): Fraction(1)}
    ratio_form = add(scale(one, Fraction(2, 3)), scale(distance, Fraction(-2, 3) if side == "below" else Fraction(1, 3)))
    powers = [power(ratio_form, exponent, 1) for exponent in range(degree_ratio + 1)]
    transformed: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    for (iz, il, irho, ia, ib), coefficient in source.items():
        for (distance_power,), value in powers[ia].items():
            eta_power, first_relative, second_relative = map_scales((distance_power, irho, ib), dominant)
            transformed[(iz, il, eta_power, first_relative, second_relative)] += coefficient * value * 3**degree_ratio
    rebuilt, radial_order = quotient({e: c for e, c in transformed.items() if c})
    candidate_path = Path(candidate_dir) / f"{name}.tsv"
    candidate = load(candidate_path)
    if rebuilt != candidate:
        raise AssertionError(f"secondary sparse mismatch: {name}")
    return {"name": name, "route": "secondary_sparse", "terms": len(candidate), "radial_order": radial_order,
            "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stripped_secant_dir", type=Path)
    parser.add_argument("primary_dir", type=Path)
    parser.add_argument("secondary_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.workers <= 3:
        raise ValueError("workers must reserve one of four CPUs")
    primary = [(str(args.stripped_secant_dir), str(args.primary_dir), p.stem) for p in sorted(args.primary_dir.glob("*.tsv"))]
    source = args.primary_dir / "high-below-second_scale-dominant.tsv"
    secondary = [(str(source), str(args.secondary_dir), p.stem) for p in sorted(args.secondary_dir.glob("*.tsv"))]
    context = multiprocessing.get_context("spawn")
    with context.Pool(args.workers, maxtasksperchild=1) as pool:
        primary_results = list(pool.imap(audit_primary, primary, chunksize=1))
        secondary_results = list(pool.imap(audit_secondary, secondary, chunksize=1))
    results = sorted(primary_results + secondary_results, key=lambda row: row["name"])
    if len(primary_results) != 12 or len(secondary_results) != 6:
        raise AssertionError("terminal chart count changed")
    payload = {
        "status": "PASS", "epistemic_status": "PROVED", "workers": args.workers,
        "route": "independent generic sparse rational polynomial multiplication", "primary_charts": 12,
        "secondary_charts": 6, "charts": {row.pop("name"): row for row in results},
        "claim_boundary": "Independent coefficientwise terminal-chart audit; Bernstein signs are certified separately.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
