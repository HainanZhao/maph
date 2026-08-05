#!/usr/bin/env python3
"""Cycle 37 exact degree-two product-functional search."""
from __future__ import annotations

import json
import math
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source
import lrc_local_product_measure as common
import lrc_degree_one_pseudoexpectation as raw
import lrc_degree_one_predicate_compressed as base

OUT = ROOT / "discovery/out/cycle37-degree-two-product"
WALL_CAP = 620


def analyze3(bases):
    infos = [base.coordinate_info(coordinate, basis) for coordinate, basis in enumerate(bases)]
    seen_once = 0
    seen_twice = 0
    seen_thrice = 0
    strong = 0
    for ordinary, coordinate_strong, _ordinary_children, _strong_children in infos:
        seen_thrice |= seen_twice & ordinary
        seen_twice |= seen_once & ordinary
        seen_once |= ordinary
        strong |= coordinate_strong
    return seen_thrice | strong, infos


def choose_predicate3(bases, satisfied, infos):
    unsatisfied = base._FULL ^ satisfied
    best = None
    bits = unsatisfied
    while bits:
        bit = bits & -bits
        predicate = bit.bit_length() - 1
        children = base.alternatives_for(predicate, bases, infos)
        candidate = (len(children), predicate, children)
        if best is None or (candidate[0], candidate[1]) < (best[0], best[1]):
            best = candidate
            if candidate[0] == 0:
                break
        bits ^= bit
    return best


def search3(bases, memo):
    if not base.reserve_call():
        return "CAP", None
    if bases in memo:
        return "NO_COVER", None
    if not base.reserve_state():
        return "CAP", None
    satisfied, infos = analyze3(bases)
    if satisfied == base._FULL:
        return "COVER", bases
    feasible_count, _predicate, children = choose_predicate3(bases, satisfied, infos)
    if feasible_count == 0:
        memo.add(bases)
        return "NO_COVER", None
    branches = []
    for child, description in children.items():
        child_satisfied, _child_infos = analyze3(child)
        gain = (child_satisfied & (base._FULL ^ satisfied)).bit_count()
        coordinate, kind, vector = description
        branches.append((-gain, coordinate, kind, vector, child))
    branches.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    saw_cap = False
    for _negative_gain, _coordinate, _kind, _vector, child in branches:
        status, witness = search3(child, memo)
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
    base._INFO_CACHE = {}
    memo = set()
    status, witness = search3(child, memo)
    return {"root_coordinate": coordinate, "root_kind": kind, "root_vector": list(vector), "status": status, "memoized_no_cover_states": len(memo), "witness": witness}


def classify3(normals):
    ordinary_counts = []
    strong_counts = []
    for predicate in range(base._VARIABLES):
        ordinary = 0
        strong = 0
        for coordinate, normal in enumerate(normals):
            pattern = base._PATTERNS_BY_LABEL[coordinate][predicate]
            if sum(left * right for left, right in zip(normal, pattern)) == 0:
                ordinary += 1
            if all(normal[option] * bit == 0 for option, bit in enumerate(pattern)):
                strong += 1
        ordinary_counts.append(ordinary)
        strong_counts.append(strong)
    satisfied = [ordinary >= 3 or strong >= 1 for ordinary, strong in zip(ordinary_counts, strong_counts)]
    return {
        "all_predicates_satisfy_three_or_strong": all(satisfied),
        "escaping_predicates": [index for index, value in enumerate(satisfied) if not value],
        "ordinary_kill_histogram": {str(count): ordinary_counts.count(count) for count in sorted(set(ordinary_counts))},
        "strong_kill_histogram": {str(count): strong_counts.count(count) for count in sorted(set(strong_counts))},
        "minimum_ordinary_kills": min(ordinary_counts),
        "predicates_with_strong_kill": sum(count > 0 for count in strong_counts),
    }


def evaluate_degree_two(normals):
    nonzero_count = 0
    first_nonzero = []
    raw_count = 0
    for predicate in range(base._VARIABLES):
        patterns = [base._PATTERNS_BY_LABEL[coordinate][predicate] for coordinate in range(13)]
        dots = [sum(left * right for left, right in zip(normal, pattern)) for normal, pattern in zip(normals, patterns)]
        point_factors = [[normal[option] * bit for option, bit in enumerate(pattern)] for normal, pattern in zip(normals, patterns)]
        for left in range(13):
            for right in range(left + 1, 13):
                other = math.prod(dots[coordinate] for coordinate in range(13) if coordinate not in (left, right))
                raw_count += len(point_factors[left]) * len(point_factors[right])
                if other == 0:
                    continue
                left_nonzero = [(option, value) for option, value in enumerate(point_factors[left]) if value]
                right_nonzero = [(option, value) for option, value in enumerate(point_factors[right]) if value]
                nonzero_count += len(left_nonzero) * len(right_nonzero)
                if len(first_nonzero) < 100:
                    for left_option, left_value in left_nonzero:
                        for right_option, right_value in right_nonzero:
                            first_nonzero.append([predicate, left, left_option, right, right_option, left_value * right_value * other])
                            if len(first_nonzero) == 100:
                                break
                        if len(first_nonzero) == 100:
                            break
    if raw_count != 16170400:
        raise AssertionError("degree-two raw census")
    return {"raw_degree_two_generators": raw_count, "degree_two_nonzero_count": nonzero_count, "first_nonzero_labels": first_nonzero}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    prepared = source.p199_prepare()
    base.prepare(prepared["option_masks"], 1394)
    base._DEADLINE = started + WALL_CAP
    sealed = json.loads((ROOT / "artifacts/cycle-36-b036-lrc-degree-one-pseudoexpectation-v1.json").read_text(encoding="utf-8"))
    cycle36_normals = [tuple(map(int, row)) for row in sealed["breakthrough"]["local_normals_by_allowed_option_offset"]]
    lower_control = raw.evaluate_normals(cycle36_normals, base._PATTERNS_BY_LABEL, 1394)
    if lower_control["degree_zero_nonzero"] or lower_control["degree_one_nonzero_count"] or lower_control["local_masses"] != [1] * 13:
        raise AssertionError("Cycle 36 lower-degree control")
    cycle36_control = {"predicate_classification": classify3(cycle36_normals), "raw_degree_two": evaluate_degree_two(cycle36_normals)}
    h11_pattern = (1, 1, 1, 1)
    if not common.contains(common.add_vector((), h11_pattern), h11_pattern):
        raise AssertionError("H11 control")

    base._COUNTER = multiprocessing.Value("q", 0)
    base._CALL_COUNTER = multiprocessing.Value("q", 0)
    empty = tuple(() for _ in base._JOBS)
    if not base.reserve_call() or not base.reserve_state():
        raise AssertionError("root cap")
    satisfied, infos = analyze3(empty)
    root_feasible, root_predicate, root_children = choose_predicate3(empty, satisfied, infos)
    root_jobs = [(child, description[0], description[1], description[2]) for child, description in root_children.items()]
    with multiprocessing.Pool(3, initializer=base.worker_init) as pool:
        outcomes = pool.map(run_root, root_jobs, chunksize=1)
    witness = next((row["witness"] for row in outcomes if row["status"] == "COVER"), None)
    if witness is not None:
        normals = [common.mass_normal(basis, len(base._JOBS[coordinate][1][0])) for coordinate, basis in enumerate(witness)]
        lower = raw.evaluate_normals(normals, base._PATTERNS_BY_LABEL, 1394)
        classification = classify3(normals)
        degree_two = evaluate_degree_two(normals)
        if lower["degree_zero_nonzero"] or lower["degree_one_nonzero_count"] or lower["local_masses"] != [1] * 13 or not classification["all_predicates_satisfy_three_or_strong"] or degree_two["degree_two_nonzero_count"]:
            raise AssertionError("degree-two product functional")
        p199 = {"status": "COVER", "root_predicate": root_predicate, "root_alternatives": root_feasible, "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes], "local_normals": [list(row) for row in normals], "span_ranks": [len(basis) for basis in witness], "predicate_classification": classification, "lower_degree_verification": lower, "degree_two_verification": degree_two}
        epistemic = "PROVED"
    else:
        status = "CAP" if any(row["status"] == "CAP" for row in outcomes) else "NO_COVER"
        p199 = {"status": status, "root_predicate": root_predicate, "root_alternatives": root_feasible, "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes]}
        epistemic = "PROVED" if status == "NO_COVER" else "OBSERVED"
    result = {"status": "PASS", "epistemic_status": epistemic, "cycle36_control": cycle36_control, "h11": {"status": "NO_PRODUCT_FUNCTIONAL", "constant_uncovered_time": 12, "local_pattern": list(h11_pattern)}, "search_states": base._COUNTER.value, "dfs_calls": base._CALL_COUNTER.value, "p199": p199, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "p199": p199["status"], "cycle36_degree_two_escapes": cycle36_control["raw_degree_two"]["degree_two_nonzero_count"], "root_predicate": root_predicate, "root_alternatives": root_feasible, "search_states": base._COUNTER.value, "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
