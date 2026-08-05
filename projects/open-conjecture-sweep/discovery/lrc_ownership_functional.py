#!/usr/bin/env python3
"""Cycle 38: exact rooted ownership pushforwards of the Cycle 37 functional."""
from __future__ import annotations

from collections import Counter, defaultdict
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import resource
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4
import lrc_ownership_blocker as ownership

OUT = ROOT / "discovery/out/cycle38-ownership-functional"
TUPLE_CAP = 50_000_000
MOMENT_CAP = 50_000_000
WALL_CAP = 1800

_COVERAGE: np.ndarray
_ALLOWED: tuple[tuple[int, ...], ...]
_NORMALS: tuple[tuple[int, ...], ...]
_COORDINATES: list[dict[str, object]]
_TYPE_ROWS: list[dict[int, tuple[tuple[tuple[int, ...], int, int], ...]]]


def factorized_moment(root: int, types: tuple[tuple[int, ...], ...]) -> int:
    """Exact moment that every time of a root blocker is owned by root."""
    rank = len(types)
    total = 0
    for subset in range(1 << rank):
        root_factor = 0
        for option, weight in enumerate(_NORMALS[root]):
            good = True
            for index, global_type in enumerate(types):
                covered = bool(global_type[root] & (1 << option))
                if covered == bool(subset & (1 << index)):
                    good = False
                    break
            if good:
                root_factor += weight
        if not root_factor:
            continue
        value = root_factor
        for coordinate, normal in enumerate(_NORMALS):
            if coordinate == root:
                continue
            local = 0
            for option, weight in enumerate(normal):
                if all(not (types[index][coordinate] & (1 << option)) for index in range(rank) if subset & (1 << index)):
                    local += weight
            value *= local
            if not value:
                break
        total += value
    return total


def direct_pushforward_moment(root: int, points: tuple[int, ...]) -> int:
    """Independent full enumeration of the 24,576-point signed support."""
    supports = [tuple((option, weight) for option, weight in enumerate(normal) if weight) for normal in _NORMALS]
    total = 0
    for assignment in itertools.product(*supports):
        options = tuple(row[0] for row in assignment)
        weight = math.prod(row[1] for row in assignment)
        owns_all = True
        order = tuple(range(root, 13)) + tuple(range(root))
        for point in points:
            owner = root
            for coordinate in order:
                digit = _ALLOWED[coordinate][options[coordinate]]
                if _COVERAGE[point, coordinate, digit]:
                    owner = coordinate
                    break
            if owner != root:
                owns_all = False
                break
        if owns_all:
            total += weight
    return total


def synthetic_controls() -> dict[str, int]:
    checks = interfaces = 0
    normals = ((2, -1), (1, 0))
    full = (1 << 3) - 1
    for code in range(1 << 12):
        masks = []
        value = code
        for _coordinate in range(2):
            masks.append((value & full, (value >> 3) & full))
            value >>= 6
        interfaces += 1
        for root in range(2):
            blockers = ownership.local_blockers(masks[root], full)
            order = (root, 1 - root)
            for blocker in blockers:
                points = tuple(index for index in range(3) if blocker & (1 << index))
                direct_value = 0
                for assignment in itertools.product(range(2), repeat=2):
                    weight = normals[0][assignment[0]] * normals[1][assignment[1]]
                    if not weight:
                        continue
                    good = True
                    for point in points:
                        owner = root
                        for coordinate in order:
                            if masks[coordinate][assignment[coordinate]] & (1 << point):
                                owner = coordinate
                                break
                        if owner != root:
                            good = False
                            break
                    if good:
                        direct_value += weight
                types = tuple(tuple(sum(1 << option for option, mask in enumerate(masks[c]) if mask & (1 << point)) for c in range(2)) for point in points)
                formula_value = 0
                for subset in range(1 << len(types)):
                    root_factor = sum(normals[root][option] for option in range(2) if all(bool(types[index][root] & (1 << option)) != bool(subset & (1 << index)) for index in range(len(types))))
                    other = 1 - root
                    other_factor = sum(normals[other][option] for option in range(2) if all(not (types[index][other] & (1 << option)) for index in range(len(types)) if subset & (1 << index)))
                    formula_value += root_factor * other_factor
                if formula_value != direct_value:
                    raise AssertionError("synthetic rooted moment")
                checks += 1
    return {"interfaces": interfaces, "root_blocker_moments": checks}


def worker_init() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (1_258_291_200, 1_258_291_200))


def evaluate_root(root: int) -> dict[str, object]:
    started = time.monotonic()
    coordinate = _COORDINATES[root]
    nonzero_by_rank: Counter[int] = Counter()
    zero_by_rank: Counter[int] = Counter()
    tuple_by_rank: Counter[int] = Counter()
    concrete_by_rank: Counter[int] = Counter()
    moment_histogram: Counter[int] = Counter()
    first_nonzero = None
    selected: dict[int, list[tuple[tuple[int, ...], tuple[int, ...], int]]] = defaultdict(list)
    concrete_total = 0
    tuples_total = 0
    moments_total = 0
    patterns = sorted(coordinate["patterns"], key=lambda row: (row["rank"], row["signatures"]))
    for pattern in patterns:
        signatures = tuple(map(int, pattern["signatures"]))
        groups = [_TYPE_ROWS[root][signature] for signature in signatures]
        pattern_concrete = 0
        row_count = math.prod(len(group) for group in groups)
        selected_ordinals = {0, row_count // 2, row_count - 1}
        for ordinal, type_rows in enumerate(itertools.product(*groups)):
            types = tuple(row[0] for row in type_rows)
            multiplicity = math.prod(row[1] for row in type_rows)
            points = tuple(row[2] for row in type_rows)
            moment = factorized_moment(root, types)
            rank = len(types)
            pattern_concrete += multiplicity
            concrete_by_rank[rank] += multiplicity
            tuple_by_rank[rank] += 1
            tuples_total += 1
            moments_total += 1
            if moment:
                nonzero_by_rank[rank] += 1
                moment_histogram[moment] += 1
                if first_nonzero is None:
                    first_nonzero = {"signatures": list(signatures), "global_types": [list(row) for row in types], "representative_times": list(points), "multiplicity": multiplicity, "moment": moment, "rank": rank}
            else:
                zero_by_rank[rank] += 1
            bucket = selected[rank]
            if ordinal in selected_ordinals:
                bucket.append((types, points, moment))
        if pattern_concrete != int(pattern["concrete_multiplicity"]):
            raise AssertionError("complete-type pattern multiplicity")
        concrete_total += pattern_concrete
        if tuples_total > TUPLE_CAP or moments_total > MOMENT_CAP or time.monotonic() - started > WALL_CAP:
            raise RuntimeError("CAP")
    if concrete_total != int(coordinate["concrete_blocker_count"]):
        raise AssertionError("root concrete blocker count")
    controls = []
    for rank in sorted(selected):
        unique = []
        seen = set()
        for types, points, expected in selected[rank]:
            key = (types, points)
            if key in seen:
                continue
            seen.add(key)
            actual = direct_pushforward_moment(root, points)
            if actual != expected:
                raise AssertionError("p199 direct pushforward moment")
            unique.append({"representative_times": list(points), "moment": actual})
        controls.append({"rank": rank, "rows": unique})
    return {
        "root": root,
        "status": "ALL_ZERO" if first_nonzero is None else "OBSTRUCTED",
        "symbolic_patterns": len(patterns),
        "complete_type_tuples": tuples_total,
        "concrete_blockers": concrete_total,
        "tuple_counts_by_rank": {str(k): v for k, v in sorted(tuple_by_rank.items())},
        "concrete_counts_by_rank": {str(k): v for k, v in sorted(concrete_by_rank.items())},
        "zero_type_tuples_by_rank": {str(k): v for k, v in sorted(zero_by_rank.items())},
        "nonzero_type_tuples_by_rank": {str(k): v for k, v in sorted(nonzero_by_rank.items())},
        "moment_histogram": {str(k): v for k, v in sorted(moment_histogram.items())},
        "first_nonzero": first_nonzero,
        "direct_controls": controls,
        "wall_seconds": time.monotonic() - started,
    }


def prepare() -> dict[str, object]:
    global _COVERAGE, _ALLOWED, _NORMALS, _COORDINATES, _TYPE_ROWS
    c29 = json.loads((ROOT / "discovery/out/cycle29-ownership-blocker/result.json").read_text(encoding="utf-8"))["p199"]
    c37 = json.loads((ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json").read_text(encoding="utf-8"))
    _COORDINATES = c29["coordinates"]
    _NORMALS = tuple(tuple(map(int, row)) for row in c37["breakthrough"]["local_normals_by_allowed_option_offset"])
    if [sum(row) for row in _NORMALS] != [1] * 13:
        raise AssertionError("Cycle 37 local masses")
    base = coupled.read_bases()[4]
    _ALLOWED = tuple(tuple(row) for row in direct.allowed_digits(base, 78))
    _COVERAGE = width4.raw_coverage(direct.CNFS[4])
    if _COVERAGE.shape != (2786, 13, 14) or tuple(map(len, _ALLOWED)) != tuple(map(len, _NORMALS)):
        raise AssertionError("p199 interface shape")
    global_types = []
    for point in range(2786):
        global_types.append(tuple(sum(1 << offset for offset, digit in enumerate(_ALLOWED[coordinate]) if _COVERAGE[point, coordinate, digit]) for coordinate in range(13)))
    _TYPE_ROWS = []
    for root in range(13):
        grouped: dict[int, dict[tuple[int, ...], list[int]]] = defaultdict(lambda: defaultdict(list))
        for point, global_type in enumerate(global_types):
            grouped[global_type[root]][global_type].append(point)
        frozen = {}
        for signature, types in grouped.items():
            frozen[signature] = tuple((global_type, len(points), min(points)) for global_type, points in sorted(types.items()))
        expected = {int(row["signature"]): int(row["count"]) for row in _COORDINATES[root]["signature_classes"]}
        actual = {signature: sum(row[1] for row in rows) for signature, rows in frozen.items()}
        if actual != expected:
            raise AssertionError("complete-type local signature projection")
        _TYPE_ROWS.append(frozen)
    return {"times": len(global_types), "distinct_complete_global_types": len(set(global_types)), "nonzero_support_assignments": math.prod(sum(value != 0 for value in row) for row in _NORMALS)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    interface = prepare()
    synthetic = synthetic_controls()
    with multiprocessing.Pool(3, initializer=worker_init) as pool:
        roots = pool.map(evaluate_root, range(13), chunksize=1)
    total_tuples = sum(int(row["complete_type_tuples"]) for row in roots)
    total_moments = total_tuples
    if total_tuples > TUPLE_CAP or total_moments > MOMENT_CAP:
        raise RuntimeError("CAP")
    if sum(int(row["concrete_blockers"]) for row in roots) != 190_867_444:
        raise AssertionError("global concrete blocker count")
    good = [int(row["root"]) for row in roots if row["status"] == "ALL_ZERO"]
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "interface": interface,
        "synthetic_controls": synthetic,
        "roots": roots,
        "span": {"all_zero_roots": good, "mass_one_extension_exists": bool(good), "rank_of_nonzero_root_columns": sum(row["status"] == "OBSTRUCTED" for row in roots), "criterion": "a mass-one combination exists iff at least one root column is zero"},
        "complete_type_tuples": total_tuples,
        "exact_moment_evaluations": total_moments,
        "concrete_blockers": 190_867_444,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "all_zero_roots": good, "type_tuples": total_tuples, "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
