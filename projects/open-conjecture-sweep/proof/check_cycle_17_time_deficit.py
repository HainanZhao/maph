#!/usr/bin/env python3
"""Independent exact verifier for Cycle 17 weighted deficit certificates."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "discovery/out/cycle17-time-deficit/results.tsv"
LP_RESULTS = ROOT / "discovery/out/cycle17-time-deficit/lp-results.tsv"
BASES = ROOT / "discovery/out/cycle8-p199-strata.txt"
CNFS = {
    4: ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf",
    3: ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf",
    7: ROOT / "discovery/out/cycle11-certified-sat/p199/007.cnf",
}
K, P, C = 13, 199, 14


def read_bases() -> list[tuple[int, ...]]:
    rows = [tuple(map(int, line.split())) for line in BASES.read_text().splitlines() if line]
    if len(rows) != 100 or any(len(row) != K for row in rows):
        raise AssertionError("base table mismatch")
    return rows


def time_clauses(path: Path) -> dict[int, tuple[frozenset[int], ...]]:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    header = lines[0].split()
    if header != ["p", "cnf", "208", "4151"]:
        raise AssertionError("CNF header mismatch")
    retained: dict[frozenset[int], int] = {}
    source: dict[int, tuple[frozenset[int], ...]] = {}
    for clause_index, line in enumerate(lines[1:], 1):
        if not 1197 <= clause_index <= 3982:
            continue
        values = tuple(map(int, line.split()))
        if values[-1] != 0 or any(value <= 0 or value > K * C for value in values[:-1]):
            raise AssertionError("coverage clause mismatch")
        clause = frozenset(values[:-1])
        if clause in retained:
            continue
        retained[clause] = clause_index
        masks = []
        for coordinate in range(K):
            masks.append(frozenset((value - 1) % C for value in clause if (value - 1) // C == coordinate))
        source[clause_index] = tuple(masks)
    return source


def pair_list() -> list[tuple[int, int]]:
    return [(left, right) for left in range(K) for right in range(left + 1, K)]


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    result = {coordinate: True for coordinate in range(left)}
    result[left] = False
    result.update({coordinate: True for coordinate in range(left + 1, right)})
    result[right] = False
    return result


def allowed_digits(base: tuple[int, ...], ordinal: int) -> tuple[frozenset[int], ...]:
    pairs = pair_list()
    req2, req7 = requirements(pairs[ordinal // 78]), requirements(pairs[ordinal % 78])
    allowed = []
    for coordinate in range(K):
        digits = set()
        for digit in range(C):
            residue = (base[coordinate] + P * digit) % C
            if coordinate in req2 and ((residue % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((residue % 7 == 0) != req7[coordinate]):
                continue
            digits.add(digit)
        allowed.append(frozenset(digits))
    return tuple(allowed)


def integers(field: str) -> list[int]:
    return [] if not field else list(map(int, field.split(",")))


def recompute(
    allowed: tuple[frozenset[int], ...],
    clauses: dict[int, tuple[frozenset[int], ...]],
    indices: list[int],
    weights: list[int],
) -> tuple[int, list[int]]:
    if not indices or len(indices) != len(weights) or len(set(indices)) != len(indices):
        raise AssertionError("malformed support")
    if any(index not in clauses for index in indices) or any(weight <= 0 for weight in weights):
        raise AssertionError("invalid clause or weight")
    maxima = []
    for coordinate in range(K):
        maxima.append(max(
            sum(weight for index, weight in zip(indices, weights, strict=True) if digit in clauses[index][coordinate])
            for digit in allowed[coordinate]
        ))
    return sum(maxima), maxima


def audit() -> dict[str, int]:
    bases = read_bases()
    clauses = {index: time_clauses(path) for index, path in CNFS.items()}
    with RESULTS.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    expected = [(base, ordinal) for base in (4, 3) for ordinal in range(6084)]
    actual = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows]
    if actual != expected:
        raise AssertionError("result order/coverage mismatch")
    counts = {4: 0, 3: 0}
    for row in rows:
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        allowed = allowed_digits(bases[base_index], ordinal)
        status = row["status"]
        if status == "EMPTY_DOMAIN":
            if all(allowed):
                raise AssertionError("false empty-domain certificate")
            counts[base_index] += 1
        elif status == "CERTIFIED_DEFICIT":
            if not all(allowed):
                raise AssertionError("deficit used instead of empty domain")
            indices, weights = integers(row["source_clauses"]), integers(row["weights"])
            if len(indices) > 3 or sum(weights) > 6:
                raise AssertionError("out-of-grammar certificate")
            upper, maxima = recompute(allowed, clauses[base_index], indices, weights)
            if sum(weights) != int(row["W"]) or upper != int(row["U"]):
                raise AssertionError("stored deficit mismatch")
            if maxima != integers(row["coordinate_maxima"]) or upper >= sum(weights):
                raise AssertionError("invalid strict deficit")
            counts[base_index] += 1
        elif status != "UNCOVERED":
            raise AssertionError("unknown status")
    control_allowed = allowed_digits(bases[7], 74)
    if not any(recompute(control_allowed, clauses[7], [index], [1])[0] == 0 for index in clauses[7]):
        raise AssertionError("positive control absent")
    uncovered = {(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows if row["status"] == "UNCOVERED"}
    with LP_RESULTS.open(newline="") as handle:
        lp_rows = list(csv.DictReader(handle, delimiter="\t"))
    if [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in lp_rows] != [
        item for item in expected if item in uncovered
    ]:
        raise AssertionError("LP continuation row mismatch")
    lp_certified = {4: 0, 3: 0}
    no_lp = {4: 0, 3: 0}
    for row in lp_rows:
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        if row["status"] == "CERTIFIED_DEFICIT":
            indices, weights = integers(row["source_clauses"]), integers(row["weights"])
            if not 0 < len(indices) <= 192 or int(row["support"]) != len(indices):
                raise AssertionError("LP support mismatch")
            if int(row["denominator"]) not in (4096, 65536, 1048576, 16777216):
                raise AssertionError("LP denominator mismatch")
            allowed = allowed_digits(bases[base_index], ordinal)
            upper, maxima = recompute(allowed, clauses[base_index], indices, weights)
            if sum(weights) != int(row["W"]) or upper != int(row["U"]) or maxima != integers(row["coordinate_maxima"]):
                raise AssertionError("LP exact reconstruction mismatch")
            if upper >= sum(weights):
                raise AssertionError("LP proposal is not an exact deficit")
            lp_certified[base_index] += 1
        elif row["status"] == "NO_LP_DEFICIT":
            no_lp[base_index] += 1
        else:
            raise AssertionError("unexpected LP continuation status")
    result = {
        "rows": len(rows),
        "base4_certified": counts[4],
        "base4_uncovered": 6084 - counts[4],
        "base3_certified": counts[3],
        "base3_uncovered": 6084 - counts[3],
        "lp_certified": sum(lp_certified.values()),
        "post_lp_base4_uncovered": 6084 - counts[4] - lp_certified[4],
        "post_lp_base3_uncovered": 6084 - counts[3] - lp_certified[3],
        "no_lp_rows_observed": sum(no_lp.values()),
        "control": 1,
    }
    if result != {"rows": 12168, "base4_certified": 5908, "base4_uncovered": 176, "base3_certified": 5783, "base3_uncovered": 301, "lp_certified": 397, "post_lp_base4_uncovered": 40, "post_lp_base3_uncovered": 40, "no_lp_rows_observed": 80, "control": 1}:
        raise AssertionError("headline counts mismatch")
    return result


if __name__ == "__main__":
    print("PASS " + " ".join(f"{key}={value}" for key, value in audit().items()))
