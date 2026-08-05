#!/usr/bin/env python3
"""Cycle 29: exact ownership/blocker semantic-primal controls and prototype."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import itertools
import json
import math
import multiprocessing
import os
from pathlib import Path
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle29-ownership-blocker"
PATTERN_CAP = 2_000_000
NODE_CAP = 20_000_000

import sys
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4


def subset(left: int, right: int) -> bool:
    return left & ~right == 0


def local_blockers(masks: tuple[int, ...], full: int) -> tuple[int, ...]:
    legal = [any(subset(cell, mask) for mask in masks) for cell in range(full + 1)]
    blockers = []
    for cell in range(1, full + 1):
        if legal[cell]:
            continue
        if all(legal[cell ^ bit] for bit in (1 << index for index in range(full.bit_length())) if cell & bit):
            blockers.append(cell)
    for cell in range(full + 1):
        avoids = all(cell & blocker != blocker for blocker in blockers)
        if legal[cell] != avoids:
            raise AssertionError("local blocker characterization")
    return tuple(blockers)


def signature_patterns(masks: tuple[int, ...], times: int) -> tuple[dict[int, list[int]], tuple[tuple[int, ...], ...]]:
    classes: dict[int, list[int]] = {}
    for point in range(times):
        signature = sum(1 << digit for digit, mask in enumerate(masks) if mask & (1 << point))
        classes.setdefault(signature, []).append(point)
    present = sorted(classes)
    patterns = []
    for size in range(1, len(present) + 1):
        for pattern in itertools.combinations(present, size):
            intersection = (1 << len(masks)) - 1
            for signature in pattern:
                intersection &= signature
            if intersection:
                continue
            minimal = True
            for omitted in range(size):
                witness = (1 << len(masks)) - 1
                for index, signature in enumerate(pattern):
                    if index != omitted:
                        witness &= signature
                if witness == 0:
                    minimal = False
                    break
            if minimal:
                patterns.append(pattern)
    concrete = set()
    for pattern in patterns:
        for points in itertools.product(*(classes[signature] for signature in pattern)):
            concrete.add(sum(1 << point for point in points))
    blockers = set(local_blockers(masks, (1 << times) - 1))
    if concrete != blockers:
        raise AssertionError("signature quotient mismatch")
    return classes, tuple(patterns)


def decode_masks(code: int, coordinates: int, times: int) -> tuple[tuple[int, int], ...]:
    full = (1 << times) - 1
    result = []
    for _coordinate in range(coordinates):
        left = code & full
        code >>= times
        right = code & full
        code >>= times
        result.append((left, right))
    return tuple(result)


@lru_cache(maxsize=None)
def synthetic_local_control(masks: tuple[int, int], times: int) -> int:
    blockers = local_blockers(masks, (1 << times) - 1)
    classes, patterns = signature_patterns(masks, times)
    represented = sum(math.prod(len(classes[signature]) for signature in pattern) for pattern in patterns)
    if represented != len(blockers):
        raise AssertionError("synthetic multiplicity")
    return len(blockers)


def synthetic_interface(code: int, coordinates: int, times: int) -> tuple[bool, int, int]:
    masks = decode_masks(code, coordinates, times)
    full = (1 << times) - 1
    direct_feasible = False
    map_checks = 0
    for digits in itertools.product(range(2), repeat=coordinates):
        chosen = tuple(masks[index][digit] for index, digit in enumerate(digits))
        covered = 0
        for mask in chosen:
            covered |= mask
        if covered != full:
            continue
        direct_feasible = True
        cells = [0] * coordinates
        for point in range(times):
            bit = 1 << point
            owner = next(index for index, mask in enumerate(chosen) if mask & bit)
            cells[owner] |= bit
        reconstructed = 0
        for coordinate, cell in enumerate(cells):
            witness = next(digit for digit, mask in enumerate(masks[coordinate]) if subset(cell, mask))
            reconstructed |= masks[coordinate][witness]
        if reconstructed != full:
            raise AssertionError("synthetic map reconstruction")
        map_checks += 1

    ownership_feasible = False
    for owners in itertools.product(range(coordinates), repeat=times):
        cells = [0] * coordinates
        for point, owner in enumerate(owners):
            cells[owner] |= 1 << point
        if all(any(subset(cells[index], mask) for mask in masks[index]) for index in range(coordinates)):
            ownership_feasible = True
            reconstructed = 0
            for index, cell in enumerate(cells):
                witness = next(digit for digit, mask in enumerate(masks[index]) if subset(cell, mask))
                reconstructed |= masks[index][witness]
            if reconstructed != full:
                raise AssertionError("synthetic reverse reconstruction")
            break
    if direct_feasible != ownership_feasible:
        raise AssertionError("synthetic feasibility equivalence")

    blocker_count = sum(synthetic_local_control(coordinate_masks, times) for coordinate_masks in masks)
    return direct_feasible, map_checks, blocker_count


def synthetic_shard(job: tuple[int, int, int, int]) -> dict[str, int]:
    coordinates, times, start, stop = job
    feasible = map_checks = blockers = 0
    for code in range(start, stop):
        found, checks, count = synthetic_interface(code, coordinates, times)
        feasible += found
        map_checks += checks
        blockers += count
    return {"interfaces": stop - start, "feasible_interfaces": feasible, "map_checks": map_checks, "blockers_checked": blockers}


def complete_synthetic() -> dict[str, object]:
    jobs = []
    corpora = ((2, 4, 1 << 16), (3, 3, 1 << 18))
    for coordinates, times, total in corpora:
        for shard in range(3):
            start = total * shard // 3
            stop = total * (shard + 1) // 3
            jobs.append((coordinates, times, start, stop))
    with multiprocessing.Pool(processes=3) as pool:
        rows = pool.map(synthetic_shard, jobs, chunksize=1)
    totals = {key: sum(row[key] for row in rows) for key in rows[0]}
    if totals["interfaces"] != 327_680:
        raise AssertionError("synthetic interface census")
    return {"status": "PASS", **totals, "corpora": [{"coordinates": 2, "digits": 2, "times": 4, "interfaces": 1 << 16}, {"coordinates": 3, "digits": 2, "times": 3, "interfaces": 1 << 18}]}


def bad_masks(k: int, q: int) -> tuple[int, ...]:
    return tuple(sum(1 << point for point in range(q) if (k + 1) * min((point * speed) % q, q - ((point * speed) % q)) < q) for speed in range(q))


def gcd_admissible(speeds: tuple[int, ...], c: int) -> bool:
    return all(math.gcd(c, *(value for index, value in enumerate(speeds) if index != omitted)) == 1 for omitted in range(len(speeds)))


def h11_control() -> dict[str, object]:
    base_bad = bad_masks(3, 11)
    lift_bad = bad_masks(3, 44)
    base_full = (1 << 11) - 1
    lift_full = (1 << 44) - 1
    assignments = raw_full_covers = raw_map_checks = gcd_admissible_count = 0
    retained = set()
    signatures = Counter()
    for base in itertools.product(range(1, 11), repeat=3):
        base_cover = 0
        for value in base:
            base_cover |= base_bad[value]
        base_improper = base_cover == base_full
        coordinate_masks = tuple(tuple(lift_bad[value + 11 * digit] for digit in range(4)) for value in base)
        for digits in itertools.product(range(4), repeat=3):
            assignments += 1
            speeds = tuple(value + 11 * digit for value, digit in zip(base, digits, strict=True))
            chosen = tuple(coordinate_masks[index][digit] for index, digit in enumerate(digits))
            covered = chosen[0] | chosen[1] | chosen[2]
            if covered == lift_full:
                raw_full_covers += 1
                cells = [0, 0, 0]
                for point in range(44):
                    bit = 1 << point
                    owner = next(index for index, mask in enumerate(chosen) if mask & bit)
                    cells[owner] |= bit
                reconstructed = 0
                for index, cell in enumerate(cells):
                    witness = next(digit for digit, mask in enumerate(coordinate_masks[index]) if subset(cell, mask))
                    reconstructed |= coordinate_masks[index][witness]
                if reconstructed != lift_full:
                    raise AssertionError("H11 raw ownership map")
                raw_map_checks += 1
            admissible = gcd_admissible(speeds, 4)
            even = tuple(index for index, speed in enumerate(speeds) if speed % 2 == 0)
            expected = len(even) <= 1
            if admissible != expected:
                raise AssertionError("H11 parity decomposition")
            if admissible:
                gcd_admissible_count += 1
                signature = "none_even" if not even else f"coordinate_{even[0]}_even"
                signatures[signature] += 1
            if base_improper and admissible and covered == lift_full:
                retained.add(base)
    if assignments != 64_000 or retained:
        raise AssertionError("H11 retained control")
    return {
        "status": "PASS", "lifted_assignments": assignments,
        "raw_full_cover_assignments": raw_full_covers, "raw_ownership_map_checks": raw_map_checks,
        "gcd_admissible_assignments": gcd_admissible_count,
        "parity_signature_counts": dict(sorted(signatures.items())),
        "retained_improper_bases": 0,
    }


class SearchCap(RuntimeError):
    pass


def minimal_signature_patterns(signatures: list[int], digit_count: int, counters: dict[str, int]) -> list[tuple[int, ...]]:
    full = (1 << digit_count) - 1
    result: list[tuple[int, ...]] = []

    def visit(start: int, chosen: tuple[int, ...], intersection: int) -> None:
        counters["nodes"] += 1
        if counters["nodes"] > NODE_CAP:
            raise SearchCap("transversal node cap")
        for index in range(start, len(signatures)):
            signature = signatures[index]
            reduced = intersection & signature
            if reduced == intersection:
                continue
            candidate = chosen + (signature,)
            if reduced == 0:
                minimal = True
                for omitted in range(len(candidate)):
                    witness = full
                    for position, value in enumerate(candidate):
                        if position != omitted:
                            witness &= value
                    if witness == 0:
                        minimal = False
                        break
                if minimal:
                    result.append(candidate)
                    counters["patterns"] += 1
                    if counters["patterns"] > PATTERN_CAP:
                        raise SearchCap("signature pattern cap")
                continue
            visit(index + 1, candidate, reduced)

    visit(0, (), full)
    if len(result) != len(set(result)):
        raise AssertionError("duplicate signature pattern")
    return result


def p199_prototype() -> dict[str, object]:
    target_rows = direct.rows(ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv") if hasattr(direct, "rows") else []
    if target_rows:
        matches = [row for row in target_rows if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]
    else:
        import csv
        with (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv").open(newline="", encoding="utf-8") as handle:
            matches = [row for row in csv.DictReader(handle, delimiter="\t") if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]
    if len(matches) != 1:
        raise AssertionError("p199 target")
    base = coupled.read_bases()[4]
    allowed = direct.allowed_digits(base, 78)
    coverage = width4.raw_coverage(direct.CNFS[4])
    if coverage.shape != (coupled.P * coupled.C, coupled.K, coupled.C):
        raise AssertionError("p199 coverage shape")

    color_witness = None
    for coordinate in range(coupled.K):
        for left_index, left in enumerate(allowed[coordinate]):
            left_speed = (base[coordinate] + coupled.P * left) % coupled.C
            left_color = (left_speed % 2 == 0, left_speed % 7 == 0)
            for right in allowed[coordinate][left_index + 1:]:
                right_speed = (base[coordinate] + coupled.P * right) % coupled.C
                right_color = (right_speed % 2 == 0, right_speed % 7 == 0)
                if left_color != right_color:
                    continue
                difference = np.flatnonzero(coverage[:, coordinate, left] != coverage[:, coordinate, right])
                if len(difference):
                    point = int(difference[0])
                    color_witness = {
                        "coordinate": coordinate, "left_digit": left, "right_digit": right,
                        "color": [int(left_color[0]), int(left_color[1])],
                        "distinguishing_time": point,
                        "left_covers": bool(coverage[point, coordinate, left]),
                        "right_covers": bool(coverage[point, coordinate, right]),
                    }
                    break
            if color_witness is not None:
                break
        if color_witness is not None:
            break
    if color_witness is None:
        raise AssertionError("same-color distinct-mask witness")

    counters = {"nodes": 0, "patterns": 0}
    coordinates = []
    total_concrete = 0
    aggregate_symbolic_ranks = Counter()
    aggregate_concrete_ranks = Counter()
    for coordinate in range(coupled.K):
        digits = allowed[coordinate]
        class_counts: Counter[int] = Counter()
        class_first: dict[int, int] = {}
        for point in range(len(coverage)):
            signature = sum(1 << index for index, digit in enumerate(digits) if coverage[point, coordinate, digit])
            class_counts[signature] += 1
            class_first.setdefault(signature, point)
        patterns = minimal_signature_patterns(sorted(class_counts), len(digits), counters)
        pattern_rows = []
        concrete = 0
        for pattern in patterns:
            intersection = (1 << len(digits)) - 1
            for signature in pattern:
                intersection &= signature
            if intersection != 0:
                raise AssertionError("nonempty blocker intersection")
            for omitted in range(len(pattern)):
                witness = (1 << len(digits)) - 1
                for index, signature in enumerate(pattern):
                    if index != omitted:
                        witness &= signature
                if witness == 0:
                    raise AssertionError("nonminimal blocker pattern")
            multiplicity = math.prod(class_counts[signature] for signature in pattern)
            concrete += multiplicity
            aggregate_symbolic_ranks[len(pattern)] += 1
            aggregate_concrete_ranks[len(pattern)] += multiplicity
            pattern_rows.append({"signatures": list(pattern), "rank": len(pattern), "concrete_multiplicity": multiplicity})
        total_concrete += concrete
        coordinates.append({
            "coordinate": coordinate, "allowed_digits": list(digits),
            "signature_classes": [{"signature": signature, "count": class_counts[signature], "least_time": class_first[signature]} for signature in sorted(class_counts)],
            "signature_class_count": len(class_counts), "patterns": pattern_rows,
            "symbolic_pattern_count": len(patterns), "concrete_blocker_count": concrete,
            "max_rank": max((len(pattern) for pattern in patterns), default=0),
        })
    if not aggregate_symbolic_ranks or max(aggregate_symbolic_ranks) > 14 or not any(rank >= 2 for rank in aggregate_symbolic_ranks):
        raise AssertionError("proper blocker rank")
    return {
        "status": "COMPLETE", "base_index": 4, "leaf_ordinal": 78,
        "times": len(coverage), "coordinates": coordinates,
        "same_color_distinct_mask_witness": color_witness,
        "transversal_nodes": counters["nodes"], "symbolic_pattern_count": counters["patterns"],
        "concrete_blocker_count": total_concrete,
        "symbolic_rank_counts": {str(rank): count for rank, count in sorted(aggregate_symbolic_ranks.items())},
        "concrete_rank_counts": {str(rank): count for rank, count in sorted(aggregate_concrete_ranks.items())},
        "max_rank": max(aggregate_symbolic_ranks),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result = {
        "epistemic_status": "OBSERVED",
        "synthetic": complete_synthetic(),
        "h11": h11_control(),
        "p199": p199_prototype(),
    }
    result["status"] = "PASS"
    result["wall_seconds"] = time.monotonic() - started
    temporary = (OUT / "result.json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    summary = (
        f"status=PASS synthetic={result['synthetic']['interfaces']} "
        f"h11_assignments={result['h11']['lifted_assignments']} "
        f"p199_patterns={result['p199']['symbolic_pattern_count']} "
        f"p199_concrete={result['p199']['concrete_blocker_count']} "
        f"max_rank={result['p199']['max_rank']} wall_seconds={result['wall_seconds']:.6f}"
    )
    (OUT / "summary.txt").write_text(summary + "\n", encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
