#!/usr/bin/env python3
"""Cycle 36 predicate-compressed exact degree-one product search."""
from __future__ import annotations

import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source
import lrc_local_product_measure as common
import lrc_degree_one_pseudoexpectation as raw

OUT = ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation"
STATE_CAP = 1_000_000
DFS_CAP = 10_000_000
SECOND_WALL_CAP = 400
WORKER_AS_CAP = 1_258_291_200  # 1200 MiB; three workers plus parent remain below 4 GiB.

_JOBS = None
_PATTERNS_BY_LABEL = None
_LABEL_PATTERN_IDS = None
_VARIABLES = 0
_FULL = 0
_COUNTER = None
_CALL_COUNTER = None
_DEADLINE = 0.0
_INFO_CACHE = None


def worker_init() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (WORKER_AS_CAP, WORKER_AS_CAP))


def prepare(option_masks, variables: int) -> None:
    global _JOBS, _PATTERNS_BY_LABEL, _LABEL_PATTERN_IDS, _VARIABLES, _FULL, _INFO_CACHE
    jobs, patterns_by_label = raw.prepare_patterns(option_masks, variables)
    label_ids = []
    for _coordinate, patterns, label_masks in jobs:
        rows = [-1] * variables
        for pattern_id, labels in enumerate(label_masks):
            bits = labels
            while bits:
                bit = bits & -bits
                rows[bit.bit_length() - 1] = pattern_id
                bits ^= bit
        if any(value < 0 for value in rows):
            raise AssertionError("pattern IDs")
        label_ids.append(tuple(rows))
    _JOBS = jobs
    _PATTERNS_BY_LABEL = patterns_by_label
    _LABEL_PATTERN_IDS = tuple(label_ids)
    _VARIABLES = variables
    _FULL = (1 << variables) - 1
    _INFO_CACHE = {}


def add_package(basis: common.Basis, pattern: tuple[int, ...]) -> common.Basis:
    result = basis
    for option, bit in enumerate(pattern):
        if bit:
            unit = tuple(1 if index == option else 0 for index in range(len(pattern)))
            result = common.add_vector(result, unit)
    return result


def coordinate_info(coordinate: int, basis: common.Basis):
    key = (coordinate, basis)
    cached = _INFO_CACHE.get(key)
    if cached is not None:
        return cached
    _index, patterns, label_masks = _JOBS[coordinate]
    ones = (1,) * len(patterns[0])
    ordinary_mask = 0
    strong_mask = 0
    ordinary_children = []
    strong_children = []
    for pattern, labels in zip(patterns, label_masks):
        ordinary = common.contains(basis, pattern)
        if ordinary:
            ordinary_mask |= labels
            ordinary_child = basis
        else:
            candidate = common.add_vector(basis, pattern)
            ordinary_child = None if common.contains(candidate, ones) else candidate
        support_units_contained = True
        for option, bit in enumerate(pattern):
            if not bit:
                continue
            unit = tuple(1 if index == option else 0 for index in range(len(pattern)))
            if not common.contains(basis, unit):
                support_units_contained = False
                break
        if support_units_contained:
            strong_mask |= labels
            strong_child = basis
        else:
            candidate = add_package(basis, pattern)
            strong_child = None if common.contains(candidate, ones) else candidate
        ordinary_children.append(ordinary_child)
        strong_children.append(strong_child)
    result = (ordinary_mask, strong_mask, tuple(ordinary_children), tuple(strong_children))
    _INFO_CACHE[key] = result
    return result


def reserve_call() -> bool:
    if time.monotonic() > _DEADLINE:
        return False
    with _CALL_COUNTER.get_lock():
        if _CALL_COUNTER.value >= DFS_CAP:
            return False
        _CALL_COUNTER.value += 1
    return True


def reserve_state() -> bool:
    with _COUNTER.get_lock():
        if _COUNTER.value >= STATE_CAP:
            return False
        _COUNTER.value += 1
    return True


def analyze(bases):
    infos = [coordinate_info(coordinate, basis) for coordinate, basis in enumerate(bases)]
    seen_once = 0
    seen_twice = 0
    strong = 0
    for ordinary, coordinate_strong, _ordinary_children, _strong_children in infos:
        seen_twice |= seen_once & ordinary
        seen_once |= ordinary
        strong |= coordinate_strong
    satisfied = seen_twice | strong
    return satisfied, infos


def alternatives_for(predicate: int, bases, infos):
    children = {}
    for coordinate, info in enumerate(infos):
        ordinary_mask, strong_mask, ordinary_children, strong_children = info
        pattern_id = _LABEL_PATTERN_IDS[coordinate][predicate]
        if not (ordinary_mask & (1 << predicate)):
            child_basis = ordinary_children[pattern_id]
            if child_basis is not None:
                child = list(bases)
                child[coordinate] = child_basis
                children[tuple(child)] = (coordinate, "ORDINARY", _JOBS[coordinate][1][pattern_id])
        if not (strong_mask & (1 << predicate)):
            child_basis = strong_children[pattern_id]
            if child_basis is not None:
                child = list(bases)
                child[coordinate] = child_basis
                children[tuple(child)] = (coordinate, "STRONG", _JOBS[coordinate][1][pattern_id])
    return children


def choose_predicate(bases, satisfied, infos):
    unsatisfied = _FULL ^ satisfied
    best = None
    bits = unsatisfied
    while bits:
        bit = bits & -bits
        predicate = bit.bit_length() - 1
        children = alternatives_for(predicate, bases, infos)
        candidate = (len(children), predicate, children)
        if best is None or (candidate[0], candidate[1]) < (best[0], best[1]):
            best = candidate
            if candidate[0] == 0:
                break
        bits ^= bit
    return best


def search(bases, memo):
    if not reserve_call():
        return "CAP", None
    if bases in memo:
        return "NO_COVER", None
    if not reserve_state():
        return "CAP", None
    satisfied, infos = analyze(bases)
    if satisfied == _FULL:
        return "COVER", bases
    feasible_count, _predicate, children = choose_predicate(bases, satisfied, infos)
    if feasible_count == 0:
        memo.add(bases)
        return "NO_COVER", None
    branches = []
    for child, description in children.items():
        child_satisfied, _child_infos = analyze(child)
        gain = (child_satisfied & (_FULL ^ satisfied)).bit_count()
        coordinate, kind, vector = description
        branches.append((-gain, coordinate, kind, vector, child))
    branches.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    saw_cap = False
    for _negative_gain, _coordinate, _kind, _vector, child in branches:
        status, witness = search(child, memo)
        if status == "COVER":
            return status, witness
        if status == "CAP":
            saw_cap = True
    if saw_cap:
        return "CAP", None
    memo.add(bases)
    return "NO_COVER", None


def run_root(job):
    child, coordinate, kind, vector = job
    global _INFO_CACHE
    _INFO_CACHE = {}
    memo = set()
    status, witness = search(child, memo)
    return {"root_coordinate": coordinate, "root_kind": kind, "root_vector": list(vector), "status": status, "memoized_no_cover_states": len(memo), "witness": witness}


def classify_normals(normals) -> dict[str, object]:
    ordinary_counts = []
    strong_counts = []
    satisfied = []
    for predicate in range(_VARIABLES):
        ordinary = 0
        strong = 0
        for coordinate, normal in enumerate(normals):
            pattern = _PATTERNS_BY_LABEL[coordinate][predicate]
            if sum(left * right for left, right in zip(normal, pattern)) == 0:
                ordinary += 1
            if all(normal[option] * bit == 0 for option, bit in enumerate(pattern)):
                strong += 1
        ordinary_counts.append(ordinary)
        strong_counts.append(strong)
        satisfied.append(ordinary >= 2 or strong >= 1)
    return {
        "all_predicates_satisfy_ordinary_or_strong": all(satisfied),
        "ordinary_kill_histogram": {str(count): ordinary_counts.count(count) for count in sorted(set(ordinary_counts))},
        "strong_kill_histogram": {str(count): strong_counts.count(count) for count in sorted(set(strong_counts))},
        "minimum_ordinary_kills": min(ordinary_counts),
        "predicates_with_strong_kill": sum(count > 0 for count in strong_counts),
    }


def main() -> None:
    global _COUNTER, _CALL_COUNTER, _DEADLINE
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    _DEADLINE = started + SECOND_WALL_CAP
    prepared = source.p199_prepare()
    prepare(prepared["option_masks"], 1394)
    sealed = json.loads((ROOT / "artifacts/cycle-35-b035-lrc-local-product-measure-v1.json").read_text(encoding="utf-8"))
    cycle35_normals = [tuple(map(int, row)) for row in sealed["breakthrough"]["local_normals_by_allowed_option_offset"]]
    control = raw.evaluate_normals(cycle35_normals, _PATTERNS_BY_LABEL, 1394)
    if control["degree_zero_nonzero"] or control["local_masses"] != [1] * 13:
        raise AssertionError("Cycle 35 control")
    control["ordinary_or_strong"] = classify_normals(cycle35_normals)
    h11_pattern = (1, 1, 1, 1)
    h11_basis = common.add_vector((), h11_pattern)
    if not common.contains(h11_basis, (1, 1, 1, 1)):
        raise AssertionError("H11 span control")

    _COUNTER = multiprocessing.Value("q", 0)
    _CALL_COUNTER = multiprocessing.Value("q", 0)
    empty = tuple(() for _ in _JOBS)
    if not reserve_call() or not reserve_state():
        raise AssertionError("root cap")
    satisfied, infos = analyze(empty)
    root_feasible, root_predicate, root_children = choose_predicate(empty, satisfied, infos)
    root_jobs = [(child, description[0], description[1], description[2]) for child, description in root_children.items()]
    if len(root_jobs) != root_feasible:
        raise AssertionError("root alternatives")
    with multiprocessing.Pool(3, initializer=worker_init) as pool:
        outcomes = pool.map(run_root, root_jobs, chunksize=1)
    witness = next((row["witness"] for row in outcomes if row["status"] == "COVER"), None)
    if witness is not None:
        normals = [common.mass_normal(basis, len(_JOBS[coordinate][1][0])) for coordinate, basis in enumerate(witness)]
        verification = raw.evaluate_normals(normals, _PATTERNS_BY_LABEL, 1394)
        classification = classify_normals(normals)
        if verification["degree_zero_nonzero"] or verification["degree_one_nonzero_count"] or verification["local_masses"] != [1] * 13 or not classification["all_predicates_satisfy_ordinary_or_strong"]:
            raise AssertionError("degree-one functional verification")
        p199 = {"status": "COVER", "root_predicate": root_predicate, "root_alternatives": root_feasible, "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes], "local_normals": [list(row) for row in normals], "span_ranks": [len(basis) for basis in witness], "predicate_classification": classification, "raw_generator_verification": verification}
        epistemic = "PROVED"
    else:
        status = "CAP" if any(row["status"] == "CAP" for row in outcomes) else "NO_COVER"
        p199 = {"status": status, "root_predicate": root_predicate, "root_alternatives": root_feasible, "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes]}
        epistemic = "PROVED" if status == "NO_COVER" else "OBSERVED"
    result = {
        "status": "PASS",
        "epistemic_status": epistemic,
        "first_tranche": json.loads((OUT / "first-tranche.json").read_text(encoding="utf-8")),
        "cycle35_control": control,
        "h11": {"status": "NO_PRODUCT_FUNCTIONAL", "constant_uncovered_time": 12, "local_pattern": list(h11_pattern)},
        "search_states": _COUNTER.value,
        "dfs_calls": _CALL_COUNTER.value,
        "p199": p199,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "p199": p199["status"], "cycle35_escapes": control["degree_one_nonzero_count"], "root_predicate": root_predicate, "root_alternatives": root_feasible, "search_states": _COUNTER.value, "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
