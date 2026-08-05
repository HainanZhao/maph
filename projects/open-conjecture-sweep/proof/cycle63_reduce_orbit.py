#!/usr/bin/env python3
"""Convert the exact C63 S3 source polynomial to joint orbit invariants."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = defaultdict(Fraction, left)
    for exponent, coefficient in right.items():
        result[exponent] += coefficient
        if result[exponent] == 0:
            del result[exponent]
    return dict(result)


def scale(poly: Polynomial, factor: Fraction) -> Polynomial:
    return {exponent: coefficient * factor for exponent, coefficient in poly.items()
            if coefficient * factor}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: dict[Exponent, Fraction] = defaultdict(Fraction)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            result[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def power(poly: Polynomial, exponent: int, variables: int) -> Polynomial:
    result: Polynomial = {(0,) * variables: Fraction(1)}
    base = poly
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        exponent //= 2
        if exponent:
            base = multiply(base, base)
    return result


def variable(index: int, variables: int = 6) -> Polynomial:
    exponent = [0] * variables
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def substitute_source(source_path: Path) -> Polynomial:
    # Target order: e,t,c,x,y,s.
    e, t, c, x, y, s = (variable(i) for i in range(6))
    forms = [
        e,
        add(t, x),
        add(t, y),
        add(add(t, scale(x, -1)), scale(y, -1)),
        add(c, s),
        add(c, scale(s, -1)),
    ]
    powers = [[power(form, degree, 6) for degree in range(16)] for form in forms]
    result: Polynomial = {}
    with source_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponents = [int(row[name]) for name in ("a0", "a1", "a2", "a5", "a3", "a4")]
            term: Polynomial = {(0,) * 6: Fraction(int(row["coefficient"]))}
            for form_index, exponent in enumerate(exponents):
                term = multiply(term, powers[form_index][exponent])
            result = add(result, term)

    # N(P_cl a) is exactly the x=y=s=0 part of N(a).
    central = {exponent: coefficient for exponent, coefficient in result.items()
               if exponent[3] == exponent[4] == exponent[5] == 0}
    return add(result, scale(central, -1))


def xy_polynomial(poly: Polynomial, x_index: int = 0, y_index: int = 1) -> dict[tuple[int, int], Fraction]:
    result: dict[tuple[int, int], Fraction] = {}
    for exponent, coefficient in poly.items():
        key = (exponent[x_index], exponent[y_index])
        result[key] = result.get(key, Fraction()) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def xy_multiply(left: dict[tuple[int, int], Fraction],
                right: dict[tuple[int, int], Fraction]) -> dict[tuple[int, int], Fraction]:
    result: dict[tuple[int, int], Fraction] = defaultdict(Fraction)
    for (lx, ly), lc in left.items():
        for (rx, ry), rc in right.items():
            result[(lx + rx, ly + ry)] += lc * rc
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def xy_power(poly: dict[tuple[int, int], Fraction], exponent: int) -> dict[tuple[int, int], Fraction]:
    result = {(0, 0): Fraction(1)}
    base = poly
    while exponent:
        if exponent & 1:
            result = xy_multiply(result, base)
        exponent //= 2
        if exponent:
            base = xy_multiply(base, base)
    return result


def solve_span(target: dict[tuple[int, int], Fraction],
               candidates: list[dict[tuple[int, int], Fraction]], degree: int) -> list[Fraction]:
    rows: list[list[Fraction]] = []
    for x_degree in range(degree + 1):
        monomial = (x_degree, degree - x_degree)
        rows.append([candidate.get(monomial, Fraction()) for candidate in candidates]
                    + [target.get(monomial, Fraction())])

    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(candidates)):
        selected = next((row for row in range(pivot_row, len(rows)) if rows[row][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [entry - factor * pivot_entry
                         for entry, pivot_entry in zip(rows[row], rows[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1

    for row in rows:
        if all(entry == 0 for entry in row[:-1]) and row[-1] != 0:
            raise ValueError("coefficient is not in the frozen invariant span")
    if len(pivot_columns) != len(candidates):
        raise ValueError("frozen invariant basis is linearly dependent")
    solution = [Fraction() for _ in candidates]
    for row, column in enumerate(pivot_columns):
        solution[column] = rows[row][-1]
    return solution


def invariant_reduce(deficit: Polynomial) -> Polynomial:
    # Orbit output order: e,t,c,r2,u,s2,w.
    grouped: dict[tuple[int, int, int, int], dict[tuple[int, int], Fraction]] = defaultdict(dict)
    for exponent, coefficient in deficit.items():
        e_degree, t_degree, c_degree, x_degree, y_degree, s_degree = exponent
        key = (e_degree, t_degree, c_degree, s_degree)
        xy_key = (x_degree, y_degree)
        grouped[key][xy_key] = grouped[key].get(xy_key, Fraction()) + coefficient

    r2 = {(2, 0): Fraction(2), (1, 1): Fraction(2), (0, 2): Fraction(2)}
    u = {(2, 1): Fraction(-1), (1, 2): Fraction(-1)}
    delta = xy_multiply(
        xy_multiply({(1, 0): Fraction(1), (0, 1): Fraction(-1)},
                    {(1, 0): Fraction(1), (0, 1): Fraction(2)}),
        {(1, 0): Fraction(-2), (0, 1): Fraction(-1)},
    )
    output: dict[Exponent, Fraction] = defaultdict(Fraction)

    for (e_degree, t_degree, c_degree, s_degree), target in grouped.items():
        target = {key: value for key, value in target.items() if value}
        if not target:
            continue
        xy_degrees = {sum(key) for key in target}
        if len(xy_degrees) != 1:
            raise ValueError("source coefficient is not homogeneous in x,y")
        xy_degree = xy_degrees.pop()
        alternating = s_degree % 2
        residual_degree = xy_degree - 3 * alternating
        if residual_degree < 0:
            raise ValueError("odd sign coefficient lacks alternating degree")

        basis_indices: list[tuple[int, int]] = []
        candidates = []
        for u_degree in range(residual_degree // 3 + 1):
            remainder = residual_degree - 3 * u_degree
            if remainder % 2:
                continue
            r2_degree = remainder // 2
            candidate = xy_multiply(xy_power(r2, r2_degree), xy_power(u, u_degree))
            if alternating:
                candidate = xy_multiply(delta, candidate)
            basis_indices.append((r2_degree, u_degree))
            candidates.append(candidate)
        coefficients = solve_span(target, candidates, xy_degree)
        for (r2_degree, u_degree), coefficient in zip(basis_indices, coefficients):
            if not coefficient:
                continue
            exponent = (
                e_degree,
                t_degree,
                c_degree,
                r2_degree,
                u_degree,
                s_degree // 2,
                alternating,
            )
            output[exponent] += coefficient
    return {exponent: coefficient for exponent, coefficient in output.items() if coefficient}


def lcm(left: int, right: int) -> int:
    return left // gcd(left, right) * right


def write_outputs(output_dir: Path, deficit: Polynomial, orbit: Polynomial) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    denominator_lcm = 1
    for coefficient in orbit.values():
        denominator_lcm = lcm(denominator_lcm, coefficient.denominator)

    with (output_dir / "orbit-polynomial.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("e", "t", "c", "r2", "u", "s2", "w", "numerator", "denominator"))
        for exponent, coefficient in sorted(orbit.items()):
            writer.writerow((*exponent, coefficient.numerator, coefficient.denominator))

    summary = {
        "epistemic_status": "PROVED",
        "source_coordinate_terms_after_subtraction": len(deficit),
        "orbit_terms": len(orbit),
        "orbit_coefficient_denominator_lcm": denominator_lcm,
        "source_total_degrees": sorted({sum(exponent) for exponent in deficit}),
        "orbit_weighted_degrees": sorted({
            exponent[0] + exponent[1] + exponent[2] + 2 * exponent[3]
            + 3 * exponent[4] + 2 * exponent[5] + 4 * exponent[6]
            for exponent in orbit
        }),
        "invariant_span_reconstruction": "PASS",
        "claim_boundary": "Exact S3 orbit-polynomial conversion only; no sign or minimizer conclusion.",
    }
    (output_dir / "orbit-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    deficit = substitute_source(args.source)
    orbit = invariant_reduce(deficit)
    write_outputs(args.output_dir, deficit, orbit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
