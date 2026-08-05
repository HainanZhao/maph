#!/usr/bin/env python3
"""Independent direct-set replay of Cycle 37's degree-two functional."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle37-degree-two-product/result.json"
OUTPUT = ROOT / "discovery/out/cycle37-degree-two-product/independent-replay.json"


def covered(k: int, q: int, speed: int) -> set[int]:
    return {point for point in range(q) if (k + 1) * min(speed * point % q, (-speed * point) % q) < q}


def base4() -> tuple[int, ...]:
    line = (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text(encoding="utf-8").splitlines()[4]
    return tuple(map(int, line.split()))


def requirement(pair: tuple[int, int]) -> dict[int, bool]:
    return {coordinate: coordinate not in pair for coordinate in range(pair[1] + 1)}


def allowed(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    req2, req7 = requirement(pairs[1]), requirement(pairs[0])
    rows = []
    for coordinate, residue in enumerate(base):
        digits = []
        for digit in range(14):
            speed = (residue + 199 * digit) % 14
            if coordinate in req2 and ((speed % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        rows.append(tuple(digits))
    return tuple(rows)


def histogram(values: list[int]) -> dict[str, int]:
    return {str(value): values.count(value) for value in sorted(set(values))}


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source["status"] != "PASS" or source["p199"]["status"] != "COVER":
        raise AssertionError("primary terminal status")
    normals = [tuple(map(int, row)) for row in source["p199"]["local_normals"]]
    base = base4()
    digit_rows = allowed(base)
    if [len(row) for row in digit_rows] != [len(row) for row in normals]:
        raise AssertionError("normal dimensions")
    masses = [sum(row) for row in normals]
    if masses != [1] * 13 or math.prod(masses) != 1:
        raise AssertionError("functional mass")

    q = 2786
    representatives = tuple(point for point in range(q) if point <= (-point) % q)
    option_covered = []
    for coordinate, digits in enumerate(digit_rows):
        options = []
        for digit in digits:
            direct = covered(13, q, base[coordinate] + 199 * digit)
            if any((point in direct) != ((-point % q) in direct) for point in representatives):
                raise AssertionError("negation invariance")
            options.append(direct)
        option_covered.append(options)

    degree_zero_nonzero = 0
    degree_one_nonzero = 0
    degree_two_nonzero = 0
    raw_degree_one = 0
    raw_degree_two = 0
    ordinary_counts = []
    strong_counts = []
    for point in representatives:
        patterns = [tuple(0 if point in direct else 1 for direct in options) for options in option_covered]
        dots = [sum(left * right for left, right in zip(normal, pattern)) for normal, pattern in zip(normals, patterns)]
        factors = [[normal[option] * bit for option, bit in enumerate(pattern)] for normal, pattern in zip(normals, patterns)]
        if math.prod(dots):
            degree_zero_nonzero += 1
        ordinary = sum(dot == 0 for dot in dots)
        strong = sum(all(value == 0 for value in row) for row in factors)
        ordinary_counts.append(ordinary)
        strong_counts.append(strong)
        if not (ordinary >= 3 or strong >= 1):
            raise AssertionError(f"three-or-strong compression {point}")
        for coordinate in range(13):
            other = math.prod(dot for index, dot in enumerate(dots) if index != coordinate)
            for value in factors[coordinate]:
                raw_degree_one += 1
                if value * other:
                    degree_one_nonzero += 1
        for left in range(13):
            for right in range(left + 1, 13):
                other = math.prod(dot for index, dot in enumerate(dots) if index not in (left, right))
                for left_value in factors[left]:
                    for right_value in factors[right]:
                        raw_degree_two += 1
                        if left_value * right_value * other:
                            degree_two_nonzero += 1
    if (raw_degree_one, raw_degree_two) != (221646, 16170400):
        raise AssertionError("raw generator census")
    if degree_zero_nonzero or degree_one_nonzero or degree_two_nonzero:
        raise AssertionError("nonzero raw contraction")
    classification = source["p199"]["predicate_classification"]
    if histogram(ordinary_counts) != classification["ordinary_kill_histogram"]:
        raise AssertionError("ordinary histogram")
    if histogram(strong_counts) != classification["strong_kill_histogram"]:
        raise AssertionError("strong histogram")

    h11_options = [covered(3, 44, 1 + 11 * digit) for digit in range(4)]
    h11_pattern = tuple(0 if 12 in direct else 1 for direct in h11_options)
    if h11_pattern != (1, 1, 1, 1):
        raise AssertionError("H11 F12")

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "p199": {
            "predicate_columns": 1394,
            "coordinate_dimensions": [len(row) for row in digit_rows],
            "local_masses": masses,
            "global_mass": 1,
            "degree_zero_generators": 1394,
            "degree_zero_nonzero": degree_zero_nonzero,
            "raw_degree_one_generators": raw_degree_one,
            "degree_one_nonzero": degree_one_nonzero,
            "raw_degree_two_generators": raw_degree_two,
            "degree_two_nonzero": degree_two_nonzero,
            "ordinary_kill_histogram": histogram(ordinary_counts),
            "strong_kill_histogram": histogram(strong_counts),
            "predicates_with_strong_kill": sum(value > 0 for value in strong_counts),
            "three_or_strong_equivalence_pass": True,
            "maximum_absolute_local_coefficient": max(abs(value) for row in normals for value in row),
        },
        "h11": {"constant_uncovered_time": 12, "local_pattern": list(h11_pattern), "product_functional": False},
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "degree_zero_nonzero": 0, "degree_one_nonzero": 0, "degree_two_nonzero": 0, "raw_degree_two": raw_degree_two, "local_masses": masses, "max_abs_coefficient": result["p199"]["maximum_absolute_local_coefficient"]}, sort_keys=True))


if __name__ == "__main__":
    main()
