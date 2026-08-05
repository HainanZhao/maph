#!/usr/bin/env python3
"""Independent direct-mask replay of Cycle 35's product measure."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle35-local-product-measure/result.json"
OUTPUT = ROOT / "discovery/out/cycle35-local-product-measure/independent-replay.json"


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


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source["status"] != "PASS" or source["p199"]["status"] != "COVER":
        raise AssertionError("primary terminal status")
    selection = sorted(source["p199"]["selection"], key=lambda row: row["coordinate"])
    if [row["coordinate"] for row in selection] != list(range(13)):
        raise AssertionError("coordinate labels")
    normals = [tuple(map(int, row["normal"])) for row in selection]
    digit_rows = allowed(base4())
    if [len(row) for row in digit_rows] != [len(normal) for normal in normals]:
        raise AssertionError("local dimensions")
    masses = [sum(normal) for normal in normals]
    if masses != [1] * 13 or math.prod(masses) != 1:
        raise AssertionError("local/global mass")

    q = 2786
    representatives = tuple(point for point in range(q) if point <= (-point) % q)
    if len(representatives) != 1394:
        raise AssertionError("representative count")
    base = base4()
    option_covered = []
    for coordinate, digits in enumerate(digit_rows):
        options = []
        for digit in digits:
            direct = covered(13, q, base[coordinate] + 199 * digit)
            if any((point in direct) != ((-point % q) in direct) for point in representatives):
                raise AssertionError("negation invariance")
            options.append(direct)
        option_covered.append(options)

    coordinate_kill_counts = [0] * 13
    predicate_kill_counts = []
    first_killer_counts = [0] * 13
    single_killer_counts = [0] * 13
    for point in representatives:
        killers = []
        for coordinate in range(13):
            pattern = tuple(0 if point in direct else 1 for direct in option_covered[coordinate])
            dot = sum(left * right for left, right in zip(normals[coordinate], pattern))
            if dot == 0:
                killers.append(coordinate)
                coordinate_kill_counts[coordinate] += 1
        if not killers:
            raise AssertionError(f"unannihilated predicate {point}")
        predicate_kill_counts.append(len(killers))
        first_killer_counts[killers[0]] += 1
        if len(killers) == 1:
            single_killer_counts[killers[0]] += 1
    expected_cover_counts = [int(row["cover_count"]) for row in selection]
    if coordinate_kill_counts != expected_cover_counts:
        raise AssertionError("coordinate kill counts")
    if (min(predicate_kill_counts), max(predicate_kill_counts)) != (1, 13):
        raise AssertionError("predicate kill multiplicities")

    h11_options = [covered(3, 44, 1 + 11 * digit) for digit in range(4)]
    h11_pattern_12 = tuple(0 if 12 in direct else 1 for direct in h11_options)
    if h11_pattern_12 != (1, 1, 1, 1):
        raise AssertionError("H11 constant predicate")
    # Any local normal with nonzero mass has nonzero dot product with this
    # pattern, so no product measure can annihilate F_12=1.

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "p199": {
            "predicate_columns": len(representatives),
            "coordinate_dimensions": [len(row) for row in digit_rows],
            "local_masses": masses,
            "global_mass": 1,
            "coordinate_kill_counts": coordinate_kill_counts,
            "first_killer_counts": first_killer_counts,
            "single_killer_counts": single_killer_counts,
            "killing_coordinate_histogram": {str(count): predicate_kill_counts.count(count) for count in sorted(set(predicate_kill_counts))},
            "minimum_killing_coordinates": min(predicate_kill_counts),
            "maximum_killing_coordinates": max(predicate_kill_counts),
            "all_predicates_annihilated": True,
            "maximum_absolute_local_coefficient": max(abs(value) for normal in normals for value in normal),
        },
        "h11": {"constant_uncovered_time": 12, "local_pattern": list(h11_pattern_12), "product_measure": False},
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "p199_predicates": len(representatives), "all_annihilated": True, "local_masses": masses, "max_abs_coefficient": result["p199"]["maximum_absolute_local_coefficient"]}, sort_keys=True))


if __name__ == "__main__":
    main()
