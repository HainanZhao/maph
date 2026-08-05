#!/usr/bin/env python3
"""Independent exact verifier for Cycle 18 pair-choice certificates."""

from __future__ import annotations

import csv
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle18-pair-choice"
OLD = ROOT / "discovery/out/cycle17-time-deficit"
BASES_PATH = ROOT / "discovery/out/cycle8-p199-strata.txt"
CNFS = {4: ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", 3: ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf"}
K, P, C = 13, 199, 14


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def time_clauses(path: Path) -> dict[int, tuple[frozenset[int], ...]]:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    retained: dict[frozenset[int], int] = {}
    result = {}
    for clause_index, line in enumerate(lines[1:], 1):
        if not 1197 <= clause_index <= 3982:
            continue
        values = frozenset(map(int, line.split()[:-1]))
        if values in retained:
            continue
        retained[values] = clause_index
        result[clause_index] = tuple(frozenset((literal - 1) % C for literal in values if (literal - 1) // C == coordinate) for coordinate in range(K))
    return result


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in range(K) for right in range(left + 1, K)]


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    result = {coordinate: True for coordinate in range(left)}
    result[left] = False
    result.update({coordinate: True for coordinate in range(left + 1, right)})
    result[right] = False
    return result


def allowed_digits(base: tuple[int, ...], ordinal: int) -> tuple[tuple[int, ...], ...]:
    req2, req7 = requirements(pairs()[ordinal // 78]), requirements(pairs()[ordinal % 78])
    result = []
    for coordinate in range(K):
        digits = []
        for digit in range(C):
            residue = (base[coordinate] + P * digit) % C
            if coordinate in req2 and ((residue % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((residue % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        result.append(tuple(digits))
    return tuple(result)


def integers(field: str) -> list[int]:
    return [] if not field else list(map(int, field.split(",")))


def parse_partition(field: str) -> tuple[tuple[int, ...], ...]:
    blocks = tuple(tuple(map(int, block.split("-"))) for block in field.split(","))
    if any(len(block) not in (1, 2) or tuple(sorted(block)) != block for block in blocks):
        raise AssertionError("bad block")
    if tuple(sorted(blocks)) != blocks or sorted(value for block in blocks for value in block) != list(range(K)):
        raise AssertionError("not a disjoint canonical partition")
    return blocks


def capacity(
    allowed: tuple[tuple[int, ...], ...], clauses: dict[int, tuple[frozenset[int], ...]],
    partition: tuple[tuple[int, ...], ...], indices: list[int], weights: list[int],
) -> tuple[int, list[int]]:
    maxima = []
    for block in partition:
        best = 0
        for option in itertools.product(*(allowed[coordinate] for coordinate in block)):
            score = 0
            for index, weight in zip(indices, weights, strict=True):
                if any(digit in clauses[index][coordinate] for coordinate, digit in zip(block, option, strict=True)):
                    score += weight
            best = max(best, score)
        maxima.append(best)
    return sum(maxima), maxima


def audit() -> dict[str, int]:
    bases = [tuple(map(int, line.split())) for line in BASES_PATH.read_text().splitlines() if line]
    clauses = {base: time_clauses(path) for base, path in CNFS.items()}
    old_lp = table(OLD / "lp-results.tsv")
    expected = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in old_lp if row["status"] == "NO_LP_DEFICIT"]
    rows = table(OUT / "results.tsv")
    actual = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows]
    if len(rows) != 80 or actual != expected:
        raise AssertionError("target set mismatch")
    certified = {4: 0, 3: 0}
    for row in rows:
        base, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        if row["status"] == "UNRESOLVED":
            continue
        if row["status"] != "CERTIFIED_DEFICIT":
            raise AssertionError("unexpected status")
        partition = parse_partition(row["partition"])
        indices, weights = integers(row["source_clauses"]), integers(row["weights"])
        if not 0 < len(indices) <= 256 or len(indices) != len(weights) or len(set(indices)) != len(indices):
            raise AssertionError("bad support")
        if any(index not in clauses[base] for index in indices) or any(weight <= 0 for weight in weights):
            raise AssertionError("bad clause/weight")
        upper, maxima = capacity(allowed_digits(bases[base], ordinal), clauses[base], partition, indices, weights)
        if sum(weights) != int(row["W"]) or upper != int(row["U"]) or maxima != integers(row["block_maxima"]):
            raise AssertionError("stored certificate mismatch")
        if upper >= sum(weights):
            raise AssertionError("non-strict pair deficit")
        certified[base] += 1
    result = {"rows": len(rows), "base4_certified": certified[4], "base3_certified": certified[3], "unresolved": len(rows) - sum(certified.values())}
    if result != {"rows": 80, "base4_certified": 0, "base3_certified": 4, "unresolved": 76}:
        raise AssertionError("headline mismatch")
    return result


if __name__ == "__main__":
    print("PASS " + " ".join(f"{key}={value}" for key, value in audit().items()))
