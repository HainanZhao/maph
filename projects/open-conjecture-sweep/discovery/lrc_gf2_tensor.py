#!/usr/bin/env python3
"""Cycle 32 degree-zero GF(2) uncovered-tensor CEGAR."""
from __future__ import annotations

import csv
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import random
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle32-gf2-tensor"
SEED = 320032
EQUATION_CAP = 8192
ROUND_CAP = 64
NODE_CAP = 20_000_000


def mask(k: int, q: int, speed: int) -> int:
    return sum(1 << point for point in range(q) if (k + 1) * min(speed * point % q, (-speed * point) % q) < q)


def representatives(q: int) -> tuple[int, ...]:
    return tuple(point for point in range(q) if point <= (-point) % q)


def compress_mask(value: int, reps: tuple[int, ...], q: int) -> int:
    result = 0
    for index, point in enumerate(reps):
        if ((value >> point) & 1) != ((value >> (-point % q)) & 1):
            raise AssertionError("negation mask mismatch")
        if value & (1 << point):
            result |= 1 << index
    return result


def equation(digits: tuple[int, ...], option_masks: tuple[tuple[int, ...], ...], variables: int) -> int:
    covered = 0
    for coordinate, digit in enumerate(digits):
        covered |= option_masks[coordinate][digit]
    uncovered = ((1 << variables) - 1) ^ covered
    return uncovered | (1 << variables)


def solve(equations: list[int], variables: int) -> dict[str, object]:
    coefficient_mask = (1 << variables) - 1
    basis: dict[int, tuple[int, int]] = {}
    for index, source in enumerate(equations):
        row = source
        provenance = 1 << index
        while row & coefficient_mask:
            pivot_bit = (row & coefficient_mask) & -(row & coefficient_mask)
            pivot = pivot_bit.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (row, provenance)
                break
            row ^= basis[pivot][0]
            provenance ^= basis[pivot][1]
        else:
            if row >> variables:
                indices = [offset for offset in range(len(equations)) if provenance & (1 << offset)]
                return {"status": "INCONSISTENT", "rank": len(basis), "contradiction_indices": indices}
    solution = 0
    for pivot in sorted(basis, reverse=True):
        row = basis[pivot][0]
        rhs = (row >> variables) & 1
        higher = (row & coefficient_mask) & ~((1 << (pivot + 1)) - 1)
        value = rhs ^ ((higher & solution).bit_count() & 1)
        if value:
            solution |= 1 << pivot
    for row in equations:
        if ((row & coefficient_mask & solution).bit_count() & 1) != ((row >> variables) & 1):
            raise AssertionError("GF2 solution replay")
    return {"status": "CONSISTENT", "rank": len(basis), "solution": solution}


def h11_control() -> dict[str, object]:
    q, k = 44, 3
    reps = representatives(q)
    if len(reps) != 23:
        raise AssertionError("H11 negation reps")
    full_masks = tuple(mask(k, q, speed) for speed in range(q))
    chosen = None
    chosen_rows = None
    scanned = 0
    for base in itertools.product(range(1, 11), repeat=3):
        scanned += 1
        rows = []
        has_cover = False
        for digits in itertools.product(range(4), repeat=3):
            speeds = tuple(base[index] + 11 * digits[index] for index in range(3))
            selected = tuple(full_masks[speed] for speed in speeds)
            has_cover |= (selected[0] | selected[1] | selected[2]) == (1 << q) - 1
            rows.append((digits, speeds))
        if not has_cover:
            chosen, chosen_rows = base, rows
            break
    if chosen is None or chosen_rows is None:
        raise AssertionError("H11 infeasible base selector")
    option_masks = tuple(tuple(compress_mask(full_masks[chosen[i] + 11 * digit], reps, q) for digit in range(4)) for i in range(3))
    equations = [equation(digits, option_masks, len(reps)) for digits, _speeds in chosen_rows]
    outcome = solve(equations, len(reps))
    result = {
        "selected_base": list(chosen),
        "bases_scanned": scanned,
        "assignments": len(equations),
        "predicate_columns": len(reps),
        "matrix_status": outcome["status"],
        "rank": outcome["rank"],
    }
    if outcome["status"] == "INCONSISTENT":
        indices = outcome["contradiction_indices"]
        xor = 0
        for index in indices:
            xor ^= equations[index]
        if xor != 1 << len(reps):
            raise AssertionError("H11 contradiction replay")
        result["contradiction_assignments"] = [list(chosen_rows[index][0]) for index in indices]
    else:
        solution = outcome["solution"]
        result["coefficient_indices"] = [index for index in range(len(reps)) if solution & (1 << index)]
        result["coefficient_times"] = [reps[index] for index in result["coefficient_indices"]]
        result["coefficient_weight"] = solution.bit_count()
    return result


def p199_base() -> tuple[int, ...]:
    return tuple(map(int, (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines()[4].split()))


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    return {coordinate: coordinate not in (left, right) for coordinate in range(right + 1)}


def p199_allowed(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    req2, req7 = requirements(pairs[1]), requirements(pairs[0])
    rows = []
    for coordinate in range(13):
        digits = []
        for digit in range(14):
            speed = (base[coordinate] + 199 * digit) % 14
            if coordinate in req2 and ((speed % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        rows.append(tuple(digits))
    return tuple(rows)


def cnf_masks() -> list[list[int]]:
    path = ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf"
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    clauses = [tuple(map(int, line.split()[:-1])) for line in lines[1:]]
    time_clauses = clauses[1196:1196 + 2786]
    result = [[0 for _digit in range(14)] for _coordinate in range(13)]
    for point, clause in enumerate(time_clauses):
        for literal in clause:
            variable = literal - 1
            result[variable // 14][variable % 14] |= 1 << point
    return result


def p199_prepare() -> dict[str, object]:
    with (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv").open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]
    if len(rows) != 1:
        raise AssertionError("p199 target")
    q, k = 2786, 13
    reps = representatives(q)
    if len(reps) != 1394 or len(reps) > 2048:
        raise AssertionError("p199 monomial benchmark")
    base = p199_base()
    allowed = p199_allowed(base)
    frozen = cnf_masks()
    option_masks = []
    for coordinate, digits in enumerate(allowed):
        row = []
        for digit in digits:
            direct = mask(k, q, base[coordinate] + 199 * digit)
            if direct != frozen[coordinate][digit]:
                raise AssertionError("p199 formula/CNF mask")
            row.append(compress_mask(direct, reps, q))
        option_masks.append(tuple(row))
    return {"base": base, "allowed": allowed, "reps": reps, "option_masks": tuple(option_masks)}


def initial_assignments(allowed: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    baseline = tuple(0 for _row in allowed)
    rows = [baseline]
    seen = {baseline}
    for coordinate, digits in enumerate(allowed):
        for offset in range(len(digits)):
            candidate = list(baseline)
            candidate[coordinate] = offset
            value = tuple(candidate)
            if value not in seen:
                rows.append(value)
                seen.add(value)
    rng = random.Random(SEED)
    while len(rows) < 147 + 4096:
        value = tuple(rng.randrange(len(digits)) for digits in allowed)
        if value not in seen:
            rows.append(value)
            seen.add(value)
    return rows


def tensor_counterexample(solution: int, bad_terms: tuple[tuple[int, ...], ...], node_state: dict[str, int]) -> tuple[int, ...] | None:
    coordinates = len(bad_terms)
    memo: set[tuple[int, int]] = set()

    def search(coordinate: int, active: int, prefix: tuple[int, ...]) -> tuple[int, ...] | None:
        node_state["nodes"] += 1
        if node_state["nodes"] > NODE_CAP:
            raise RuntimeError("tensor verifier node cap")
        if active == 0:
            return prefix + (0,) * (coordinates - coordinate)
        if coordinate == coordinates:
            return None if active.bit_count() & 1 else prefix
        key = (coordinate, active)
        if key in memo:
            return None
        for digit, bad in enumerate(bad_terms[coordinate]):
            found = search(coordinate + 1, active & bad, prefix + (digit,))
            if found is not None:
                return found
        memo.add(key)
        return None

    return search(0, solution, ())


def p199_cegar(prepared: dict[str, object]) -> dict[str, object]:
    allowed = prepared["allowed"]
    reps = prepared["reps"]
    option_masks = prepared["option_masks"]
    variables = len(reps)
    assignments = initial_assignments(allowed)
    equations = [equation(row, option_masks, variables) for row in assignments]
    bad_terms = tuple(tuple(((1 << variables) - 1) ^ covered for covered in row) for row in option_masks)
    nodes = {"nodes": 0}
    rounds = 0
    while rounds < ROUND_CAP:
        rounds += 1
        outcome = solve(equations, variables)
        if outcome["status"] == "INCONSISTENT":
            indices = outcome["contradiction_indices"]
            xor = 0
            for index in indices:
                xor ^= equations[index]
            if xor != 1 << variables:
                raise AssertionError("p199 contradiction replay")
            return {
                "status": "INCONSISTENT_EVALUATION_SUBSYSTEM",
                "predicate_columns": variables,
                "initial_equations": 4243,
                "equations": len(equations),
                "rounds": rounds,
                "rank": outcome["rank"],
                "tensor_verifier_nodes": nodes["nodes"],
                "contradiction_size": len(indices),
                "contradiction_assignments": [list(assignments[index]) for index in indices],
            }
        solution = outcome["solution"]
        counterexample = tensor_counterexample(solution, bad_terms, nodes)
        if counterexample is None:
            return {
                "status": "CERTIFICATE_PENDING_INDEPENDENT_REPLAY",
                "predicate_columns": variables,
                "initial_equations": 4243,
                "equations": len(equations),
                "rounds": rounds,
                "rank": outcome["rank"],
                "tensor_verifier_nodes": nodes["nodes"],
                "coefficient_indices": [index for index in range(variables) if solution & (1 << index)],
                "coefficient_times": [reps[index] for index in range(variables) if solution & (1 << index)],
                "coefficient_weight": solution.bit_count(),
            }
        if counterexample in assignments:
            raise AssertionError("repeated tensor counterexample")
        if len(equations) >= EQUATION_CAP:
            return {"status": "CAP", "reason": "equation cap", "equations": len(equations), "rounds": rounds, "tensor_verifier_nodes": nodes["nodes"]}
        assignments.append(counterexample)
        equations.append(equation(counterexample, option_masks, variables))
    return {"status": "CAP", "reason": "round cap", "equations": len(equations), "rounds": rounds, "tensor_verifier_nodes": nodes["nodes"]}


def prepare(name: str) -> dict[str, object]:
    return h11_control() if name == "h11" else p199_prepare()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with multiprocessing.Pool(2) as pool:
        h11, p199 = pool.map(prepare, ("h11", "p199"))
    p199_result = p199_cegar(p199)
    result = {"status": "PASS", "epistemic_status": "OBSERVED", "h11": h11, "p199": p199_result, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "h11_status": h11["matrix_status"], "p199_status": p199_result["status"], "p199_equations": p199_result["equations"], "rounds": p199_result["rounds"], "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
