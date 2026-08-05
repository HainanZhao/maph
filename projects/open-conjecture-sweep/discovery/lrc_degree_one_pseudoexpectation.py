#!/usr/bin/env python3
"""Cycle 36 exact degree-one product-pseudoexpectation search."""
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

OUT = ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation"
STATE_CAP = 1_000_000
DFS_CAP = 10_000_000
SIGNATURE_CAP = 250_000
WALL_CAP = 820

_JOBS = None
_PATTERNS_BY_LABEL = None
_SIGNATURES = None
_RAW_COUNTS = None
_COUNTER = None
_CALL_COUNTER = None
_DEADLINE = 0.0


Alternative = tuple[int, tuple[int, ...]]
Signature = tuple[Alternative, ...]


def prepare_patterns(option_masks, variables: int):
    jobs = common.pattern_jobs(option_masks, variables)
    patterns_by_label = []
    for _coordinate, patterns, label_masks in jobs:
        rows = [None] * variables
        for pattern, labels in zip(patterns, label_masks):
            bits = labels
            while bits:
                bit = bits & -bits
                rows[bit.bit_length() - 1] = pattern
                bits ^= bit
        if any(row is None for row in rows):
            raise AssertionError("pattern label partition")
        patterns_by_label.append(tuple(rows))
    return jobs, tuple(patterns_by_label)


def build_signatures(patterns_by_label, variables: int):
    signatures: dict[Signature, dict[str, object]] = {}
    automatic = 0
    degree_zero = 0
    raw_degree_one = 0

    def record(signature: Signature, label: tuple[int, ...]) -> None:
        row = signatures.setdefault(signature, {"raw_count": 0, "first_label": label})
        row["raw_count"] = int(row["raw_count"]) + 1

    for predicate in range(variables):
        degree_zero_signature = tuple(sorted({(coordinate, tuple(patterns_by_label[coordinate][predicate])) for coordinate in range(len(patterns_by_label))}))
        record(degree_zero_signature, (predicate, -1, -1))
        degree_zero += 1
        for multiplier_coordinate, pattern in enumerate(patterns_by_label):
            local = pattern[predicate]
            dimension = len(local)
            for option in range(dimension):
                raw_degree_one += 1
                if local[option] == 0:
                    automatic += 1
                    continue
                unit = tuple(1 if index == option else 0 for index in range(dimension))
                alternatives = {(multiplier_coordinate, unit)}
                for coordinate in range(len(patterns_by_label)):
                    if coordinate != multiplier_coordinate:
                        alternatives.add((coordinate, tuple(patterns_by_label[coordinate][predicate])))
                record(tuple(sorted(alternatives)), (predicate, multiplier_coordinate, option))
    if raw_degree_one != 221646 or degree_zero != 1394:
        raise AssertionError("raw generator census")
    if len(signatures) > SIGNATURE_CAP:
        return None, {"status": "CAP", "reason": "deduplicated signature cap", "signatures": len(signatures), "raw_degree_one": raw_degree_one, "automatic_degree_one": automatic}
    ordered = sorted(signatures)
    rows = [signatures[signature] for signature in ordered]
    return ordered, {"status": "PASS", "degree_zero": degree_zero, "raw_degree_one": raw_degree_one, "automatic_degree_one": automatic, "deduplicated_signatures": len(ordered), "raw_counts": [int(row["raw_count"]) for row in rows], "first_labels": [list(row["first_label"]) for row in rows]}


def evaluate_normals(normals, patterns_by_label, variables: int) -> dict[str, object]:
    masses = [sum(normal) for normal in normals]
    degree_zero_nonzero = []
    degree_one_nonzero = []
    automatic = 0
    for predicate in range(variables):
        dots = [sum(left * right for left, right in zip(normals[coordinate], patterns_by_label[coordinate][predicate])) for coordinate in range(len(normals))]
        value = 1
        for dot in dots:
            value *= dot
        if value:
            degree_zero_nonzero.append(predicate)
        for coordinate, local in enumerate(patterns_by_label):
            pattern = local[predicate]
            other = 1
            for other_coordinate, dot in enumerate(dots):
                if other_coordinate != coordinate:
                    other *= dot
            for option, bit in enumerate(pattern):
                if bit == 0:
                    automatic += 1
                    continue
                generator_value = normals[coordinate][option] * other
                if generator_value:
                    degree_one_nonzero.append((predicate, coordinate, option, generator_value))
    return {
        "local_masses": masses,
        "global_mass": str(__import__("math").prod(masses)),
        "degree_zero_nonzero": degree_zero_nonzero,
        "degree_one_nonzero_count": len(degree_one_nonzero),
        "degree_one_nonzero_labels": [list(row[:3]) for row in degree_one_nonzero],
        "automatic_degree_one": automatic,
    }


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


def alternative_status(bases, alternative: Alternative) -> tuple[bool, common.Basis | None]:
    coordinate, vector = alternative
    basis = bases[coordinate]
    if common.contains(basis, vector):
        return True, basis
    enlarged = common.add_vector(basis, vector)
    ones = (1,) * len(vector)
    if common.contains(enlarged, ones):
        return False, None
    return False, enlarged


def state_analysis(bases):
    unsatisfied = []
    for index, signature in enumerate(_SIGNATURES):
        feasible = []
        satisfied = False
        for alternative in signature:
            already, enlarged = alternative_status(bases, alternative)
            if already:
                satisfied = True
                break
            if enlarged is not None:
                feasible.append((alternative, enlarged))
        if not satisfied:
            unsatisfied.append((len(feasible), signature, index, feasible))
    if not unsatisfied:
        return None, []
    feasible_count, signature, index, feasible = min(unsatisfied, key=lambda row: (row[0], row[1]))
    return (index, signature, feasible_count, feasible), unsatisfied


def satisfied_raw_weight(bases) -> int:
    total = 0
    for signature, raw_count in zip(_SIGNATURES, _RAW_COUNTS):
        if any(common.contains(bases[coordinate], vector) for coordinate, vector in signature):
            total += raw_count
    return total


def search(bases, memo):
    if not reserve_call():
        return "CAP", None
    if bases in memo:
        return "NO_COVER", None
    if not reserve_state():
        return "CAP", None
    chosen, _unsatisfied = state_analysis(bases)
    if chosen is None:
        return "COVER", bases
    _index, _signature, feasible_count, feasible = chosen
    if feasible_count == 0:
        memo.add(bases)
        return "NO_COVER", None
    branches = []
    current_weight = satisfied_raw_weight(bases)
    for alternative, enlarged in feasible:
        coordinate, vector = alternative
        child = list(bases)
        child[coordinate] = enlarged
        gain = satisfied_raw_weight(tuple(child)) - current_weight
        branches.append((-gain, coordinate, vector, enlarged))
    branches.sort(key=lambda row: (row[0], row[1], row[2]))
    saw_cap = False
    for _negative_gain, coordinate, _vector, enlarged in branches:
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


def root_alternatives(empty):
    chosen, _unsatisfied = state_analysis(empty)
    if chosen is None:
        raise AssertionError("empty degree-one constraints")
    index, signature, feasible_count, feasible = chosen
    branches = [(alternative[0], alternative[1], enlarged) for alternative, enlarged in feasible]
    if len(branches) != feasible_count:
        raise AssertionError("root feasibility")
    return index, signature, branches


def run_root(branch):
    coordinate, vector, enlarged = branch
    bases = [()] * len(_JOBS)
    bases[coordinate] = enlarged
    memo = set()
    status, witness = search(tuple(bases), memo)
    return {"root_coordinate": coordinate, "root_vector": list(vector), "status": status, "memoized_no_cover_states": len(memo), "witness": witness}


def normals_from_bases(bases):
    return [common.mass_normal(basis, len(_JOBS[coordinate][1][0])) for coordinate, basis in enumerate(bases)]


def main() -> None:
    global _JOBS, _PATTERNS_BY_LABEL, _SIGNATURES, _RAW_COUNTS, _COUNTER, _CALL_COUNTER, _DEADLINE
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    _DEADLINE = started + WALL_CAP
    prepared = source.p199_prepare()
    _JOBS, _PATTERNS_BY_LABEL = prepare_patterns(prepared["option_masks"], 1394)
    signatures, census = build_signatures(_PATTERNS_BY_LABEL, 1394)
    if signatures is None:
        result = {"status": "PASS", "epistemic_status": "OBSERVED", "census": census, "p199": {"status": "CAP", "reason": census["reason"]}, "wall_seconds": time.monotonic() - started}
    else:
        _SIGNATURES = signatures
        _RAW_COUNTS = census.pop("raw_counts")
        first_labels = census.pop("first_labels")
        sealed = json.loads((ROOT / "artifacts/cycle-35-b035-lrc-local-product-measure-v1.json").read_text(encoding="utf-8"))
        cycle35_normals = [tuple(map(int, row)) for row in sealed["breakthrough"]["local_normals_by_allowed_option_offset"]]
        control = evaluate_normals(cycle35_normals, _PATTERNS_BY_LABEL, 1394)
        if control["degree_zero_nonzero"] or control["local_masses"] != [1] * 13:
            raise AssertionError("Cycle 35 functional control")
        h11_pattern = tuple(0 if 12 in {point for point in range(44) if 4 * min((1 + 11 * digit) * point % 44, (-(1 + 11 * digit) * point) % 44) < 44} else 1 for digit in range(4))
        if h11_pattern != (1, 1, 1, 1):
            raise AssertionError("H11 F12 control")
        _COUNTER = multiprocessing.Value("q", 0)
        _CALL_COUNTER = multiprocessing.Value("q", 0)
        empty = tuple(() for _ in _JOBS)
        root_index, root_signature, branches = root_alternatives(empty)
        with multiprocessing.Pool(3) as pool:
            outcomes = pool.map(run_root, branches, chunksize=1)
        witness = next((row["witness"] for row in outcomes if row["status"] == "COVER"), None)
        if witness is not None:
            normals = normals_from_bases(witness)
            verification = evaluate_normals(normals, _PATTERNS_BY_LABEL, 1394)
            if verification["degree_zero_nonzero"] or verification["degree_one_nonzero_count"] or verification["local_masses"] != [1] * 13:
                raise AssertionError("degree-one product functional")
            p199 = {"status": "COVER", "root_signature_index": root_index, "root_signature": [[coordinate, list(vector)] for coordinate, vector in root_signature], "root_first_label": first_labels[root_index], "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes], "local_normals": [list(row) for row in normals], "span_ranks": [len(basis) for basis in witness], "verification": verification}
            epistemic = "PROVED"
        else:
            pstatus = "CAP" if any(row["status"] == "CAP" for row in outcomes) else "NO_COVER"
            p199 = {"status": pstatus, "root_signature_index": root_index, "root_signature": [[coordinate, list(vector)] for coordinate, vector in root_signature], "root_first_label": first_labels[root_index], "root_branches": [{key: value for key, value in row.items() if key != "witness"} for row in outcomes]}
            epistemic = "PROVED" if pstatus == "NO_COVER" else "OBSERVED"
        result = {"status": "PASS", "epistemic_status": epistemic, "census": census, "cycle35_control": control, "h11": {"status": "NO_PRODUCT_FUNCTIONAL", "constant_uncovered_time": 12, "local_pattern": list(h11_pattern)}, "search_states": _COUNTER.value, "dfs_calls": _CALL_COUNTER.value, "p199": p199, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "p199": result["p199"]["status"], "signatures": result["census"].get("deduplicated_signatures"), "cycle35_escapes": result.get("cycle35_control", {}).get("degree_one_nonzero_count"), "search_states": result.get("search_states"), "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
