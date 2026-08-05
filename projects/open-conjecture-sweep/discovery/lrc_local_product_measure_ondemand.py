#!/usr/bin/env python3
"""Cycle 35 optimized exact on-demand local-product search."""
from __future__ import annotations

import json
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source
import lrc_local_product_measure as common

OUT = ROOT / "discovery/out/cycle35-local-product-measure"
STATE_CAP = 1_000_000
DFS_CAP = 10_000_000
SECOND_WALL_SECONDS = 700

_JOBS = None
_VARIABLES = 0
_FULL = 0
_LABEL_PATTERN_IDS = None
_COUNTER = None
_DEADLINE = 0.0
_INFO_CACHE = None


def prepare(jobs, variables: int) -> None:
    global _JOBS, _VARIABLES, _FULL, _LABEL_PATTERN_IDS, _INFO_CACHE
    _JOBS = jobs
    _VARIABLES = variables
    _FULL = (1 << variables) - 1
    mappings = []
    for _coordinate, patterns, label_masks in jobs:
        label_ids = [-1] * variables
        for pattern_id, labels in enumerate(label_masks):
            bits = labels
            while bits:
                bit = bits & -bits
                label_ids[bit.bit_length() - 1] = pattern_id
                bits ^= bit
        if any(value < 0 for value in label_ids):
            raise AssertionError("local label partition")
        mappings.append(tuple(label_ids))
    _LABEL_PATTERN_IDS = tuple(mappings)
    _INFO_CACHE = {}


def reserve_node() -> bool:
    if time.monotonic() > _DEADLINE:
        return False
    with _COUNTER.get_lock():
        if _COUNTER.value >= STATE_CAP:
            return False
        _COUNTER.value += 1
        return True


def coordinate_info(coordinate: int, basis: common.Basis) -> tuple[int, frozenset[int]]:
    key = (coordinate, basis)
    cached = _INFO_CACHE.get(key)
    if cached is not None:
        return cached
    _index, patterns, label_masks = _JOBS[coordinate]
    ones = (1,) * len(patterns[0])
    killed = 0
    feasible = []
    for pattern_id, (pattern, labels) in enumerate(zip(patterns, label_masks)):
        if common.contains(basis, pattern):
            killed |= labels
        else:
            enlarged = common.add_vector(basis, pattern)
            if not common.contains(enlarged, ones):
                feasible.append(pattern_id)
    result = (killed, frozenset(feasible))
    _INFO_CACHE[key] = result
    return result


def minimum_feasible_label(uncovered: int, feasible_masks: list[int]) -> tuple[int, int]:
    planes = [0, 0, 0, 0]
    for mask in feasible_masks:
        carry = mask
        bit = 0
        while carry:
            new_carry = planes[bit] & carry
            planes[bit] ^= carry
            carry = new_carry
            bit += 1
    for count in range(len(feasible_masks) + 1):
        equal = _FULL
        for bit, plane in enumerate(planes):
            equal &= plane if count & (1 << bit) else (_FULL ^ plane)
        candidates = equal & uncovered
        if candidates:
            least = candidates & -candidates
            return least.bit_length() - 1, count
    raise AssertionError("feasible-count partition")


def analyze_state(bases: tuple[common.Basis, ...]) -> tuple[int, list[tuple[int, frozenset[int]]], int, int]:
    infos = [coordinate_info(coordinate, basis) for coordinate, basis in enumerate(bases)]
    killed = 0
    feasible_masks = []
    for coordinate, (coordinate_killed, feasible_ids) in enumerate(infos):
        killed |= coordinate_killed
        mask = 0
        for pattern_id in feasible_ids:
            mask |= _JOBS[coordinate][2][pattern_id]
        feasible_masks.append(mask)
    if killed == _FULL:
        return killed, infos, -1, -1
    predicate, count = minimum_feasible_label(_FULL ^ killed, feasible_masks)
    return killed, infos, predicate, count


def search(bases: tuple[common.Basis, ...], memo: set[tuple[common.Basis, ...]]) -> tuple[str, tuple[common.Basis, ...] | None]:
    if bases in memo:
        return "NO_COVER", None
    if not reserve_node():
        return "CAP", None
    killed, infos, predicate, feasible_count = analyze_state(bases)
    if killed == _FULL:
        return "COVER", bases
    if feasible_count == 0:
        memo.add(bases)
        return "NO_COVER", None
    branches = []
    for coordinate, (_coordinate_killed, feasible_ids) in enumerate(infos):
        pattern_id = _LABEL_PATTERN_IDS[coordinate][predicate]
        if pattern_id not in feasible_ids:
            continue
        enlarged = common.add_vector(bases[coordinate], _JOBS[coordinate][1][pattern_id])
        new_killed, _new_feasible = coordinate_info(coordinate, enlarged)
        gain = (new_killed & (_FULL ^ killed)).bit_count()
        branches.append((-gain, coordinate, enlarged))
    if len(branches) != feasible_count:
        raise AssertionError("feasible branch count")
    branches.sort(key=lambda row: (row[0], row[1]))
    saw_cap = False
    for _negative_gain, coordinate, enlarged in branches:
        child = list(bases)
        child[coordinate] = enlarged
        status, witness = search(tuple(child), memo)
        if status == "COVER":
            return status, witness
        if status == "CAP":
            saw_cap = True
    if saw_cap:
        return "CAP", None
    memo.add(bases)
    return "NO_COVER", None


def root_branches(empty: tuple[common.Basis, ...]) -> tuple[int, list[tuple[int, common.Basis]]]:
    killed, infos, predicate, feasible_count = analyze_state(empty)
    branches = []
    for coordinate, (_coordinate_killed, feasible_ids) in enumerate(infos):
        pattern_id = _LABEL_PATTERN_IDS[coordinate][predicate]
        if pattern_id in feasible_ids:
            enlarged = common.add_vector(empty[coordinate], _JOBS[coordinate][1][pattern_id])
            new_killed, _new_feasible = coordinate_info(coordinate, enlarged)
            branches.append((-(new_killed & (_FULL ^ killed)).bit_count(), coordinate, enlarged))
    if len(branches) != feasible_count:
        raise AssertionError("root branch count")
    branches.sort(key=lambda row: (row[0], row[1]))
    return predicate, [(coordinate, enlarged) for _negative_gain, coordinate, enlarged in branches]


def run_root(branch: tuple[int, common.Basis]) -> dict[str, object]:
    global _INFO_CACHE
    _INFO_CACHE = {}
    coordinate, enlarged = branch
    bases = [()] * len(_JOBS)
    bases[coordinate] = enlarged
    memo: set[tuple[common.Basis, ...]] = set()
    status, witness = search(tuple(bases), memo)
    return {"root_coordinate": coordinate, "status": status, "memoized_no_cover_states": len(memo), "witness": witness}


def selection_from_bases(bases: tuple[common.Basis, ...]) -> list[dict[str, object]]:
    selection = []
    for coordinate, basis in enumerate(bases):
        normal = common.mass_normal(basis, len(_JOBS[coordinate][1][0]))
        killed, _feasible = coordinate_info(coordinate, basis)
        normal_killed = 0
        for pattern, labels in zip(_JOBS[coordinate][1], _JOBS[coordinate][2]):
            if sum(left * right for left, right in zip(normal, pattern)) == 0:
                normal_killed |= labels
        selection.append({"coordinate": coordinate, "normal": list(normal), "cover_count": normal_killed.bit_count(), "span_guaranteed_cover_count": killed.bit_count(), "span_rank": len(basis)})
    common.verify_selection(selection, _JOBS, _VARIABLES)
    return selection


def run_family(jobs, variables: int, parallel: bool, counter, deadline: float) -> dict[str, object]:
    global _COUNTER, _DEADLINE
    prepare(jobs, variables)
    _COUNTER = counter
    _DEADLINE = deadline
    empty = tuple(() for _ in jobs)
    if not reserve_node():
        return {"status": "CAP", "reason": "state/wall cap before root"}
    killed, _infos, predicate, feasible_count = analyze_state(empty)
    if killed == _FULL:
        raise AssertionError("empty spans kill all predicates")
    if feasible_count == 0:
        return {"status": "NO_COVER", "root_predicate": predicate, "root_feasible_coordinates": 0, "root_branches": []}
    root_predicate, branches = root_branches(empty)
    if parallel:
        with multiprocessing.Pool(3) as pool:
            outcomes = pool.map(run_root, branches, chunksize=1)
    else:
        outcomes = [run_root(branch) for branch in branches]
    witness = next((row["witness"] for row in outcomes if row["status"] == "COVER"), None)
    if witness is not None:
        selection = selection_from_bases(witness)
        verification = common.verify_selection(selection, jobs, variables)
        return {"status": "COVER", "root_predicate": root_predicate, "root_feasible_coordinates": len(branches), "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes], "selection": selection, "verification": verification}
    status = "CAP" if any(row["status"] == "CAP" for row in outcomes) else "NO_COVER"
    return {"status": status, "root_predicate": root_predicate, "root_feasible_coordinates": len(branches), "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes]}


def main() -> None:
    global _COUNTER, _DEADLINE
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    deadline = started + SECOND_WALL_SECONDS
    counter = multiprocessing.Value("q", 0)
    h11_jobs = common.h11_jobs()
    h11 = run_family(h11_jobs, 23, parallel=False, counter=counter, deadline=deadline)
    if h11["status"] != "NO_COVER":
        raise AssertionError("H11 on-demand negative control")
    prepared = source.p199_prepare()
    jobs = common.pattern_jobs(prepared["option_masks"], 1394)
    p199 = run_family(jobs, 1394, parallel=True, counter=counter, deadline=deadline)
    epistemic = "PROVED" if p199["status"] in {"COVER", "NO_COVER"} else "OBSERVED"
    result = {
        "status": "PASS",
        "epistemic_status": epistemic,
        "first_tranche": {"status": "CAP", "flat_states": 1000000, "wall_seconds": 428.98},
        "second_tranche_states": counter.value,
        "h11": h11,
        "p199": p199,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "h11": h11["status"], "p199": p199["status"], "second_tranche_states": counter.value, "root_branches": p199.get("root_feasible_coordinates"), "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
