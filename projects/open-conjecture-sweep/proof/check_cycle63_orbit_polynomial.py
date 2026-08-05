#!/usr/bin/env python3
"""Independent exact checks for the C63 S3 orbit polynomial."""

from __future__ import annotations

import csv
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle63-orbit-minimizer"
C62 = ROOT / "discovery" / "out" / "cycle62-kkt-exchange" / "exchange-derivatives.tsv"


def load_source() -> dict[tuple[int, ...], int]:
    result = {}
    with (OUT / "source-polynomial.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("a0", "a1", "a2", "a5", "a3", "a4"))
            result[exponent] = int(row["coefficient"])
    return result


def permute_source(source: dict[tuple[int, ...], int], trans: tuple[int, int, int],
                   swap_cycles: bool) -> dict[tuple[int, ...], int]:
    result = {}
    for exponent, coefficient in source.items():
        mapped = [0] * 6
        mapped[0] = exponent[0]
        for destination, source_index in enumerate(trans, start=1):
            mapped[destination] = exponent[source_index]
        mapped[4] = exponent[5] if swap_cycles else exponent[4]
        mapped[5] = exponent[4] if swap_cycles else exponent[5]
        result[tuple(mapped)] = coefficient
    return result


def derivative(source: dict[tuple[int, ...], int], positive: int,
               negative: int) -> dict[tuple[int, ...], int]:
    result: dict[tuple[int, ...], int] = {}
    for exponent, coefficient in source.items():
        if exponent[positive]:
            target = list(exponent)
            target[positive] -= 1
            key = tuple(target)
            result[key] = result.get(key, 0) + coefficient * exponent[positive]
        if exponent[negative]:
            target = list(exponent)
            target[negative] -= 1
            key = tuple(target)
            result[key] = result.get(key, 0) - coefficient * exponent[negative]
    return {key: value for key, value in result.items() if value}


def load_c62() -> dict[str, dict[tuple[int, ...], int]]:
    result: dict[str, dict[tuple[int, ...], int]] = {"trans": {}, "cycle": {}}
    with C62.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("a0", "a1", "a2", "a5", "a3", "a4"))
            result[row["class"]][exponent] = int(row["coefficient"])
    return result


def load_orbit() -> dict[tuple[int, ...], Fraction]:
    result = {}
    with (OUT / "orbit-polynomial.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("e", "t", "c", "r2", "u", "s2", "w"))
            result[exponent] = Fraction(int(row["numerator"]), int(row["denominator"]))
    return result


def evaluate(poly, values):
    total = 0
    for exponent, coefficient in poly.items():
        term = coefficient
        for value, power in zip(values, exponent):
            term *= value ** power
        total += term
    return total


def orbit_values(original: tuple[int, ...]) -> tuple[Fraction, ...]:
    e, a1, a2, a5, a3, a4 = map(Fraction, original)
    t = (a1 + a2 + a5) / 3
    x, y, z = a1 - t, a2 - t, a5 - t
    c = (a3 + a4) / 2
    s = (a3 - a4) / 2
    r2 = x * x + y * y + z * z
    u = x * y * z
    s2 = s * s
    w = s * (x - y) * (y - z) * (z - x)
    return e, t, c, r2, u, s2, w


def main() -> int:
    source = load_source()
    assert source
    assert {sum(exponent) for exponent in source} == {15}

    symmetry_checks = 0
    for trans in itertools.permutations((1, 2, 3)):
        for swap_cycles in (False, True):
            assert permute_source(source, trans, swap_cycles) == source
            symmetry_checks += 1

    previous = load_c62()
    assert derivative(source, 2, 1) == previous["trans"]
    assert derivative(source, 5, 4) == previous["cycle"]

    orbit = load_orbit()
    assert orbit
    assert all(exponent[6] == 0 for exponent in orbit)
    assert {exponent[0] + exponent[1] + exponent[2] + 2 * exponent[3]
            + 3 * exponent[4] + 2 * exponent[5] + 4 * exponent[6]
            for exponent in orbit} == {15}

    # Formal coefficient checks above carry the proof load.  Keep the
    # independent evaluator discriminating but cheap enough for routine replay.
    controls = list(itertools.product(range(2), repeat=6))
    generator = random.Random(630063)
    controls.extend(tuple(generator.randrange(-4, 8) for _ in range(6)) for _ in range(64))
    for original in controls:
        central = (
            original[0],
            Fraction(original[1] + original[2] + original[3], 3),
            Fraction(original[1] + original[2] + original[3], 3),
            Fraction(original[1] + original[2] + original[3], 3),
            Fraction(original[4] + original[5], 2),
            Fraction(original[4] + original[5], 2),
        )
        expected = evaluate(source, original) - evaluate(source, central)
        actual = evaluate(orbit, orbit_values(original))
        assert actual == expected, (original, actual, expected)

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "source_terms": len(source),
        "orbit_terms": len(orbit),
        "exact_symmetry_maps_checked": symmetry_checks,
        "c62_derivative_identities": 2,
        "exact_evaluation_controls": len(controls),
        "orientation_coupling_terms": sum(exponent[6] != 0 for exponent in orbit),
        "claim_boundary": "Formal source symmetry and derivative identities plus exact evaluation controls; invariant conversion is proved by the separate exact span reconstruction.",
    }
    (OUT / "orbit-audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
