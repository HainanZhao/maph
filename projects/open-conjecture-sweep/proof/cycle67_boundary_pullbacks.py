#!/usr/bin/env python3
"""Derive the four exact C67 endpoint-simplex Zhao deficit polynomials."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

Exponent = tuple[int, ...]
Poly = dict[Exponent, Fraction]
Form = dict[int, Fraction]

NVAR = 5
FAMILIES: dict[str, list[Form]] = {
    # Source order: a0,a1,a2,a5,a3,a4.
    "cycle_equal": [{0: Fraction(1)}, {1: Fraction(1)}, {2: Fraction(1)},
                    {3: Fraction(1)}, {4: Fraction(1, 2)}, {4: Fraction(1, 2)}],
    "cycle_zero": [{0: Fraction(1)}, {1: Fraction(1)}, {2: Fraction(1)},
                   {3: Fraction(1)}, {4: Fraction(1)}, {}],
    "trans_equal": [{0: Fraction(1)}, {1: Fraction(1, 2)}, {1: Fraction(1, 2)},
                    {2: Fraction(1)}, {3: Fraction(1)}, {4: Fraction(1)}],
    "trans_zero": [{0: Fraction(1)}, {1: Fraction(1)}, {2: Fraction(1)},
                   {}, {3: Fraction(1)}, {4: Fraction(1)}],
}


def add_form(*forms: Form) -> Form:
    result: dict[int, Fraction] = defaultdict(Fraction)
    for form in forms:
        for index, coefficient in form.items():
            result[index] += coefficient
    return {index: value for index, value in result.items() if value}


def scale_form(form: Form, scale: Fraction) -> Form:
    return {index: value * scale for index, value in form.items() if value * scale}


def multiply(left: Poly, right: Poly) -> Poly:
    result: dict[Exponent, Fraction] = defaultdict(Fraction)
    for le, lc in left.items():
        for re, rc in right.items():
            result[tuple(a+b for a, b in zip(le, re))] += lc*rc
    return {exponent: value for exponent, value in result.items() if value}


def powers(form: Form) -> list[Poly]:
    result: list[Poly] = [{(0,)*NVAR: Fraction(1)}]
    linear = {}
    for index, coefficient in form.items():
        exponent = [0]*NVAR
        exponent[index] = 1
        linear[tuple(exponent)] = coefficient
    for _ in range(15):
        result.append(multiply(result[-1], linear))
    return result


def substitute_source(rows: list[tuple[Exponent, int]], forms: list[Form]) -> Poly:
    form_powers = [powers(form) for form in forms]
    result: dict[Exponent, Fraction] = defaultdict(Fraction)
    for exponents, coefficient in rows:
        term: Poly = {(0,)*NVAR: Fraction(coefficient)}
        for index, exponent in enumerate(exponents):
            if exponent:
                term = multiply(term, form_powers[index][exponent])
                if not term:
                    break
        for key, value in term.items():
            result[key] += value
    return {exponent: value for exponent, value in result.items() if value}


def class_average(forms: list[Form]) -> list[Form]:
    trans = scale_form(add_form(forms[1], forms[2], forms[3]), Fraction(1, 3))
    cycles = scale_form(add_form(forms[4], forms[5]), Fraction(1, 2))
    return [forms[0], trans, trans, trans, cycles, cycles]


def evaluate(poly: Poly, point: tuple[Fraction, ...]) -> Fraction:
    powers_by_variable = [[value**degree for degree in range(16)] for value in point]
    return sum(coefficient * __import__("math").prod(
        powers_by_variable[index][degree] for index, degree in enumerate(exponent)
    ) for exponent, coefficient in poly.items())


def orbit_value(path: Path, values: tuple[Fraction, ...]) -> Fraction:
    e, a1, a2, a5, a3, a4 = values
    t = (a1+a2+a5)/3
    c = (a3+a4)/2
    x, y, z = a1-t, a2-t, a5-t
    invariants = (e, t, c, x*x+y*y+z*z, x*y*z, ((a3-a4)/2)**2)
    total = Fraction()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            coefficient = Fraction(int(row["numerator"]), int(row["denominator"]))
            term = coefficient
            for name, value in zip(("e","t","c","r2","u","s2"), invariants):
                term *= value**int(row[name])
            total += term
    return total


def source_values(forms: list[Form], point: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(coefficient*point[index] for index, coefficient in form.items())
                 for form in forms)


def load_source(path: Path) -> list[tuple[Exponent, int]]:
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            rows.append((tuple(int(row[name]) for name in ("a0","a1","a2","a5","a3","a4")),
                         int(row["coefficient"])))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source = load_source(args.source)
    controls = (
        (Fraction(1,5), Fraction(1,10), Fraction(1,4), Fraction(1,8), Fraction(13,40)),
        (Fraction(0), Fraction(1,7), Fraction(2,7), Fraction(1,7), Fraction(3,7)),
        (Fraction(1,3), Fraction(1,6), Fraction(0), Fraction(1,4), Fraction(1,4)),
    )
    summaries = {}
    for name, forms in FAMILIES.items():
        raw = substitute_source(source, forms)
        central = substitute_source(source, class_average(forms))
        deficit = dict(raw)
        for exponent, coefficient in central.items():
            deficit[exponent] = deficit.get(exponent, Fraction()) - coefficient
            if not deficit[exponent]:
                del deficit[exponent]
        assert {sum(exponent) for exponent in deficit} == {15}
        with (args.output_dir/f"{name}.tsv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(("z0","z1","z2","z3","z4","numerator","denominator"))
            for exponent, coefficient in sorted(deficit.items()):
                writer.writerow((*exponent, coefficient.numerator, coefficient.denominator))
        checked = 0
        for point in controls:
            direct = evaluate(deficit, point)
            invariant = orbit_value(args.orbit, source_values(forms, point))
            assert direct == invariant
            checked += 1
        summaries[name] = {
            "terms": len(deficit),
            "positive_coefficients": sum(value>0 for value in deficit.values()),
            "negative_coefficients": sum(value<0 for value in deficit.values()),
            "independent_invariant_controls": checked,
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "source_rows": len(source),
        "families": summaries,
        "claim_boundary": "Exact endpoint pullbacks and source/invariant agreement; no sign conclusion.",
    }
    (args.output_dir/"pullback-summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8"
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
