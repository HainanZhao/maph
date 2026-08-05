#!/usr/bin/env python3
"""Independent exact replay of Cycle 29 ownership/blocker controls."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import csv
import itertools
import json
import math
import multiprocessing
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle29-ownership-blocker/result.json"
OUTPUT = ROOT / "discovery/out/cycle29-ownership-blocker/independent-replay.json"
K, P, C = 13, 199, 14


def inside(cell: int, mask: int) -> bool:
    return cell | mask == mask


def unpack(code: int, k: int, times: int) -> tuple[tuple[int, int], ...]:
    unit = (1 << times) - 1
    result = []
    for _ in range(k):
        result.append((code & unit, (code >> times) & unit))
        code >>= 2 * times
    return tuple(result)


@lru_cache(maxsize=None)
def blocker_count(pair: tuple[int, int], times: int) -> int:
    full = (1 << times) - 1
    legal = tuple(any(inside(cell, mask) for mask in pair) for cell in range(full + 1))
    blockers = []
    for cell in range(1, full + 1):
        if not legal[cell] and all(legal[cell & ~(1 << point)] for point in range(times) if cell & (1 << point)):
            blockers.append(cell)
    for cell in range(full + 1):
        if legal[cell] != all(cell & blocker != blocker for blocker in blockers):
            raise AssertionError("independent blocker characterization")
    return len(blockers)


def synthetic_row(code: int, k: int, times: int) -> tuple[int, int, int]:
    masks = unpack(code, k, times)
    full = (1 << times) - 1
    covers = 0
    for digits in itertools.product((0, 1), repeat=k):
        union = 0
        for coordinate, digit in enumerate(digits):
            union |= masks[coordinate][digit]
        covers += union == full
    owners_exist = False
    for owners in itertools.product(range(k), repeat=times):
        cells = [0] * k
        for point, owner in enumerate(owners):
            cells[owner] |= 1 << point
        if all(any(inside(cells[coordinate], mask) for mask in masks[coordinate]) for coordinate in range(k)):
            owners_exist = True
            break
    if bool(covers) != owners_exist:
        raise AssertionError("independent synthetic equivalence")
    return int(bool(covers)), covers, sum(blocker_count(pair, times) for pair in masks)


def synthetic_shard(job: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    k, times, start, stop = job
    feasible = maps = blockers = 0
    for code in range(start, stop):
        found, cover_count, local = synthetic_row(code, k, times)
        feasible += found
        maps += cover_count
        blockers += local
    return stop - start, feasible, maps, blockers


def synthetic() -> dict[str, int]:
    jobs = []
    for k, times, total in ((2, 4, 1 << 16), (3, 3, 1 << 18)):
        for shard in range(3):
            jobs.append((k, times, total * shard // 3, total * (shard + 1) // 3))
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(synthetic_shard, jobs, chunksize=1)
    values = tuple(sum(row[index] for row in rows) for index in range(4))
    return {"interfaces": values[0], "feasible_interfaces": values[1], "map_checks": values[2], "blockers_checked": values[3]}


def masks(k: int, q: int) -> tuple[int, ...]:
    answer = []
    for speed in range(q):
        mask = 0
        for point in range(q):
            residue = point * speed % q
            if (k + 1) * min(residue, q - residue) < q:
                mask |= 1 << point
        answer.append(mask)
    return tuple(answer)


def h11() -> dict[str, object]:
    low, high = masks(3, 11), masks(3, 44)
    low_full, high_full = (1 << 11) - 1, (1 << 44) - 1
    assignments = raw_covers = admissible_count = 0
    retained = set()
    parity = Counter()
    for base in itertools.product(range(1, 11), repeat=3):
        base_union = low[base[0]] | low[base[1]] | low[base[2]]
        for digits in itertools.product(range(4), repeat=3):
            assignments += 1
            speeds = tuple(base[index] + 11 * digits[index] for index in range(3))
            union = high[speeds[0]] | high[speeds[1]] | high[speeds[2]]
            raw_covers += union == high_full
            admissible = True
            for omitted in range(3):
                divisor = 4
                for index, speed in enumerate(speeds):
                    if index != omitted:
                        divisor = math.gcd(divisor, speed)
                admissible &= divisor == 1
            even = tuple(index for index, speed in enumerate(speeds) if speed % 2 == 0)
            if admissible != (len(even) <= 1):
                raise AssertionError("independent parity decomposition")
            if admissible:
                admissible_count += 1
                parity["none_even" if not even else f"coordinate_{even[0]}_even"] += 1
            if base_union == low_full and admissible and union == high_full:
                retained.add(base)
    return {
        "lifted_assignments": assignments, "raw_full_cover_assignments": raw_covers,
        "raw_ownership_map_checks": raw_covers, "gcd_admissible_assignments": admissible_count,
        "parity_signature_counts": dict(sorted(parity.items())), "retained_improper_bases": len(retained),
    }


def read_base4() -> tuple[int, ...]:
    rows = [tuple(map(int, line.split())) for line in (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines() if line]
    return rows[4]


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in range(K) for right in range(left + 1, K)]


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    value = {coordinate: True for coordinate in range(left)}
    value[left] = False
    value.update({coordinate: True for coordinate in range(left + 1, right)})
    value[right] = False
    return value


def allowed(base: tuple[int, ...], ordinal: int) -> tuple[tuple[int, ...], ...]:
    ordered = pairs()
    req2, req7 = requirements(ordered[ordinal // 78]), requirements(ordered[ordinal % 78])
    answer = []
    for coordinate in range(K):
        digits = []
        for digit in range(C):
            speed = (base[coordinate] + P * digit) % C
            if coordinate in req2 and ((speed % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        answer.append(tuple(digits))
    return tuple(answer)


def raw_coverage() -> list[list[set[int]]]:
    path = ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf"
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    clauses = [tuple(map(int, line.split()[:-1])) for line in lines[1:]]
    time_clauses = clauses[1197 - 1:1197 - 1 + P * C]
    if len(time_clauses) != P * C:
        raise AssertionError("independent time clauses")
    result = [[set() for _digit in range(C)] for _coordinate in range(K)]
    for point, clause in enumerate(time_clauses):
        for literal in clause:
            variable = literal - 1
            result[variable // C][variable % C].add(point)
    return result


def reverse_patterns(signatures: list[int], digits: int) -> set[tuple[int, ...]]:
    full = (1 << digits) - 1
    result: set[tuple[int, ...]] = set()

    def search(limit: int, selected: tuple[int, ...], intersection: int) -> None:
        for index in range(limit - 1, -1, -1):
            signature = signatures[index]
            reduced = intersection & signature
            if reduced == intersection:
                continue
            candidate = (signature,) + selected
            if reduced:
                search(index, candidate, reduced)
                continue
            for omitted in range(len(candidate)):
                witness = full
                for position, value in enumerate(candidate):
                    if position != omitted:
                        witness &= value
                if witness == 0:
                    break
            else:
                result.add(candidate)

    search(len(signatures), (), full)
    return result


def p199(source: dict[str, object]) -> dict[str, object]:
    with (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv").open(newline="", encoding="utf-8") as handle:
        targets = list(csv.DictReader(handle, delimiter="\t"))
    if len([row for row in targets if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]) != 1:
        raise AssertionError("independent target")
    base = read_base4()
    digit_sets = allowed(base, 78)
    coverage = raw_coverage()
    source_coordinates = source["coordinates"]
    symbolic_ranks = Counter()
    concrete_ranks = Counter()
    symbolic_total = concrete_total = 0
    for coordinate in range(K):
        digits = digit_sets[coordinate]
        classes = Counter()
        first = {}
        for point in range(P * C):
            signature = sum(1 << index for index, digit in enumerate(digits) if point in coverage[coordinate][digit])
            classes[signature] += 1
            first.setdefault(signature, point)
        patterns = reverse_patterns(sorted(classes), len(digits))
        expected = source_coordinates[coordinate]
        if expected["allowed_digits"] != list(digits):
            raise AssertionError("independent allowed digits")
        observed_classes = [{"signature": signature, "count": classes[signature], "least_time": first[signature]} for signature in sorted(classes)]
        if expected["signature_classes"] != observed_classes:
            raise AssertionError("independent signature classes")
        expected_patterns = {tuple(row["signatures"]): row["concrete_multiplicity"] for row in expected["patterns"]}
        observed_patterns = {pattern: math.prod(classes[value] for value in pattern) for pattern in patterns}
        if expected_patterns != observed_patterns:
            raise AssertionError("independent signature patterns")
        for pattern, multiplicity in observed_patterns.items():
            symbolic_ranks[len(pattern)] += 1
            concrete_ranks[len(pattern)] += multiplicity
            concrete_total += multiplicity
        symbolic_total += len(patterns)

    witness = None
    for coordinate in range(K):
        for left_index, left in enumerate(digit_sets[coordinate]):
            left_speed = (base[coordinate] + P * left) % C
            color = (left_speed % 2 == 0, left_speed % 7 == 0)
            for right in digit_sets[coordinate][left_index + 1:]:
                right_speed = (base[coordinate] + P * right) % C
                if color != (right_speed % 2 == 0, right_speed % 7 == 0):
                    continue
                difference = sorted(coverage[coordinate][left] ^ coverage[coordinate][right])
                if difference:
                    point = difference[0]
                    witness = {"coordinate": coordinate, "left_digit": left, "right_digit": right, "color": [int(color[0]), int(color[1])], "distinguishing_time": point, "left_covers": point in coverage[coordinate][left], "right_covers": point in coverage[coordinate][right]}
                    break
            if witness is not None:
                break
        if witness is not None:
            break
    if witness != source["same_color_distinct_mask_witness"]:
        raise AssertionError("independent color witness")
    return {
        "symbolic_pattern_count": symbolic_total, "concrete_blocker_count": concrete_total,
        "symbolic_rank_counts": {str(rank): count for rank, count in sorted(symbolic_ranks.items())},
        "concrete_rank_counts": {str(rank): count for rank, count in sorted(concrete_ranks.items())},
        "max_rank": max(symbolic_ranks), "same_color_distinct_mask_witness": witness,
    }


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    synthetic_result = synthetic()
    h11_result = h11()
    p199_result = p199(source["p199"])
    for key, value in synthetic_result.items():
        if source["synthetic"][key] != value:
            raise AssertionError(f"synthetic metric {key}")
    for key, value in h11_result.items():
        if source["h11"][key] != value:
            raise AssertionError(f"H11 metric {key}")
    for key, value in p199_result.items():
        if source["p199"][key] != value:
            raise AssertionError(f"p199 metric {key}")
    result = {"status": "PASS", "epistemic_status": "OBSERVED", "synthetic": synthetic_result, "h11": h11_result, "p199": p199_result}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "synthetic_interfaces": synthetic_result["interfaces"], "h11_assignments": h11_result["lifted_assignments"], "p199_patterns": p199_result["symbolic_pattern_count"], "max_rank": p199_result["max_rank"]}, sort_keys=True))


if __name__ == "__main__":
    main()
