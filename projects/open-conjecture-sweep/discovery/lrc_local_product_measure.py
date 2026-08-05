#!/usr/bin/env python3
"""Cycle 35 exact local-product signed-measure search."""
from __future__ import annotations

from collections import deque
from fractions import Fraction
import itertools
import json
import math
import multiprocessing
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source

OUT = ROOT / "discovery/out/cycle35-local-product-measure"
LOCAL_STATE_CAP = 200_000
AGGREGATE_STATE_CAP = 1_000_000
RETAINED_CAP = 200_000
DFS_CAP = 10_000_000
HEIGHT_CAP = 65_536
_STATE_COUNTER = None


Basis = tuple[tuple[Fraction, ...], ...]


def reduce_vector(basis: Basis, vector: tuple[int | Fraction, ...]) -> list[Fraction]:
    result = [Fraction(value) for value in vector]
    for row in basis:
        pivot = next(index for index, value in enumerate(row) if value)
        factor = result[pivot]
        if factor:
            result = [left - factor * right for left, right in zip(result, row)]
    return result


def contains(basis: Basis, vector: tuple[int | Fraction, ...]) -> bool:
    return not any(reduce_vector(basis, vector))


def add_vector(basis: Basis, vector: tuple[int | Fraction, ...]) -> Basis:
    reduced = reduce_vector(basis, vector)
    if not any(reduced):
        return basis
    pivot = next(index for index, value in enumerate(reduced) if value)
    scale = reduced[pivot]
    new_row = [value / scale for value in reduced]
    rows = []
    for row in basis:
        factor = row[pivot]
        rows.append(tuple(left - factor * right for left, right in zip(row, new_row)))
    rows.append(tuple(new_row))
    rows.sort(key=lambda row: next(index for index, value in enumerate(row) if value))
    return tuple(rows)


def mass_normal(basis: Basis, dimension: int) -> tuple[int, ...]:
    equations = [list(row) + [Fraction(0)] for row in basis]
    equations.append([Fraction(1)] * dimension + [Fraction(1)])
    pivot_row = 0
    pivots = []
    for column in range(dimension):
        selected = next((row for row in range(pivot_row, len(equations)) if equations[row][column]), None)
        if selected is None:
            continue
        equations[pivot_row], equations[selected] = equations[selected], equations[pivot_row]
        factor = equations[pivot_row][column]
        equations[pivot_row] = [value / factor for value in equations[pivot_row]]
        for row in range(len(equations)):
            if row == pivot_row or not equations[row][column]:
                continue
            factor = equations[row][column]
            equations[row] = [left - factor * right for left, right in zip(equations[row], equations[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(equations):
            break
    for row in equations:
        if not any(row[:-1]) and row[-1]:
            raise AssertionError("mass-normal system inconsistent")
    solution = [Fraction(0)] * dimension
    for row, pivot in enumerate(pivots):
        solution[pivot] = equations[row][-1]
    denominator = 1
    for value in solution:
        denominator = math.lcm(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator) for value in solution]
    divisor = 0
    for value in integers:
        divisor = math.gcd(divisor, abs(value))
    integers = [value // divisor for value in integers]
    if sum(integers) < 0:
        integers = [-value for value in integers]
    if sum(integers) == 0 or max(abs(value).bit_length() for value in integers) > HEIGHT_CAP:
        raise AssertionError("mass-normal normalization")
    for row in basis:
        if sum(value * coefficient for value, coefficient in zip(integers, row)):
            raise AssertionError("mass-normal basis dot product")
    return tuple(integers)


def reserve_state() -> bool:
    if _STATE_COUNTER is None:
        return True
    with _STATE_COUNTER.get_lock():
        if _STATE_COUNTER.value >= AGGREGATE_STATE_CAP:
            return False
        _STATE_COUNTER.value += 1
        return True


def enumerate_coordinate(job: tuple[int, list[tuple[int, ...]], list[int]]) -> dict[str, object]:
    coordinate, patterns, label_masks = job
    dimension = len(patterns[0])
    ones = (1,) * dimension
    zero: Basis = ()
    queue = deque([zero])
    visited = {zero}
    maximal: list[Basis] = []
    if not reserve_state():
        return {"coordinate": coordinate, "status": "CAP", "reason": "aggregate flat-state cap", "states": 0}
    while queue:
        basis = queue.popleft()
        can_extend = False
        for pattern in patterns:
            if contains(basis, pattern):
                continue
            enlarged = add_vector(basis, pattern)
            if contains(enlarged, ones):
                continue
            can_extend = True
            if enlarged not in visited:
                if len(visited) >= LOCAL_STATE_CAP:
                    return {"coordinate": coordinate, "status": "CAP", "reason": "coordinate flat-state cap", "states": len(visited)}
                if not reserve_state():
                    return {"coordinate": coordinate, "status": "CAP", "reason": "aggregate flat-state cap", "states": len(visited)}
                visited.add(enlarged)
                queue.append(enlarged)
        if not can_extend:
            maximal.append(basis)
            if len(maximal) > RETAINED_CAP:
                return {"coordinate": coordinate, "status": "CAP", "reason": "retained-flat cap", "states": len(visited)}

    candidates_by_cover: dict[int, tuple[int, ...]] = {}
    for basis in maximal:
        normal = mass_normal(basis, dimension)
        cover = 0
        for pattern, labels in zip(patterns, label_masks):
            if sum(left * right for left, right in zip(normal, pattern)) == 0:
                cover |= labels
        prior = candidates_by_cover.get(cover)
        if prior is None or normal < prior:
            candidates_by_cover[cover] = normal
    candidates = [{"cover": cover, "normal": normal} for cover, normal in candidates_by_cover.items()]
    candidates.sort(key=lambda row: (row["normal"], row["cover"]))
    return {
        "coordinate": coordinate,
        "status": "COMPLETE",
        "dimension": dimension,
        "distinct_patterns": len(patterns),
        "states": len(visited),
        "maximal_flats": len(maximal),
        "candidates": candidates,
    }


def pattern_jobs(option_covered: tuple[tuple[int, ...], ...], variables: int) -> list[tuple[int, list[tuple[int, ...]], list[int]]]:
    jobs = []
    for coordinate, options in enumerate(option_covered):
        grouped: dict[tuple[int, ...], int] = {}
        for predicate in range(variables):
            pattern = tuple(0 if covered & (1 << predicate) else 1 for covered in options)
            grouped[pattern] = grouped.get(pattern, 0) | (1 << predicate)
        ordered = sorted(grouped.items())
        jobs.append((coordinate, [row[0] for row in ordered], [row[1] for row in ordered]))
    return jobs


def cover_search(coordinates: list[dict[str, object]], variables: int) -> dict[str, object]:
    full = (1 << variables) - 1
    candidate_rows = {int(row["coordinate"]): row["candidates"] for row in coordinates}
    nodes = 0

    def search(remaining: tuple[int, ...], covered: int, selection: dict[int, dict[str, object]]) -> dict[int, dict[str, object]] | None:
        nonlocal nodes
        nodes += 1
        if nodes > DFS_CAP:
            raise RuntimeError("cover DFS node cap")
        if covered == full:
            for coordinate in remaining:
                selection[coordinate] = candidate_rows[coordinate][0]
            return selection
        suffix = covered
        for coordinate in remaining:
            for candidate in candidate_rows[coordinate]:
                suffix |= int(candidate["cover"])
        if suffix != full:
            return None
        uncovered = full ^ (covered & full)
        scored_coordinates = []
        for coordinate in remaining:
            useful = [candidate for candidate in candidate_rows[coordinate] if int(candidate["cover"]) & uncovered]
            scored_coordinates.append((len(useful), coordinate, useful))
        useful_count, coordinate, useful = min(scored_coordinates, key=lambda row: (row[0], row[1]))
        if useful_count == 0:
            selection[coordinate] = candidate_rows[coordinate][0]
            found = search(tuple(value for value in remaining if value != coordinate), covered, selection)
            if found is not None:
                return found
            selection.pop(coordinate, None)
            return None
        useful.sort(key=lambda candidate: (-(int(candidate["cover"]) & uncovered).bit_count(), tuple(candidate["normal"])))
        next_remaining = tuple(value for value in remaining if value != coordinate)
        for candidate in useful:
            selection[coordinate] = candidate
            found = search(next_remaining, covered | int(candidate["cover"]), selection)
            if found is not None:
                return found
        selection.pop(coordinate, None)
        return None

    try:
        found = search(tuple(sorted(candidate_rows)), 0, {})
    except RuntimeError:
        return {"status": "CAP", "reason": "cover DFS node cap", "nodes": nodes}
    if found is None:
        return {"status": "NO_COVER", "nodes": nodes}
    return {
        "status": "COVER",
        "nodes": nodes,
        "selection": [{"coordinate": coordinate, "normal": list(found[coordinate]["normal"]), "cover_count": int(found[coordinate]["cover"]).bit_count()} for coordinate in sorted(found)],
    }


def verify_selection(selection: list[dict[str, object]], jobs: list[tuple[int, list[tuple[int, ...]], list[int]]], variables: int) -> dict[str, object]:
    normals = {int(row["coordinate"]): tuple(map(int, row["normal"])) for row in selection}
    if set(normals) != set(range(len(jobs))):
        raise AssertionError("one normal per coordinate")
    masses = [sum(normals[index]) for index in range(len(jobs))]
    if any(mass == 0 for mass in masses):
        raise AssertionError("zero local mass")
    killed = [False] * variables
    kill_counts = [0] * variables
    for coordinate, patterns, labels in jobs:
        normal = normals[coordinate]
        for pattern, label_mask in zip(patterns, labels):
            dot = sum(left * right for left, right in zip(normal, pattern))
            if dot == 0:
                bits = label_mask
                while bits:
                    bit = bits & -bits
                    index = bit.bit_length() - 1
                    killed[index] = True
                    kill_counts[index] += 1
                    bits ^= bit
    if not all(killed):
        raise AssertionError("unannihilated predicate")
    total_mass = math.prod(masses)
    if total_mass == 0:
        raise AssertionError("global mass")
    return {"local_masses": masses, "global_mass": str(total_mass), "minimum_killing_coordinates": min(kill_counts), "maximum_killing_coordinates": max(kill_counts)}


def h11_jobs() -> list[tuple[int, list[tuple[int, ...]], list[int]]]:
    q = 44
    reps = source.representatives(q)
    options = tuple(tuple(source.compress_mask(source.mask(3, q, 1 + 11 * digit), reps, q) for digit in range(4)) for _ in range(3))
    return pattern_jobs(options, len(reps))


def run_family(jobs: list[tuple[int, list[tuple[int, ...]], list[int]]], variables: int, parallel: bool) -> dict[str, object]:
    global _STATE_COUNTER
    _STATE_COUNTER = multiprocessing.Value("q", 0)
    if parallel:
        with multiprocessing.Pool(3) as pool:
            coordinates = pool.map(enumerate_coordinate, jobs, chunksize=1)
    else:
        coordinates = [enumerate_coordinate(job) for job in jobs]
    if any(row["status"] != "COMPLETE" for row in coordinates):
        return {"status": "CAP", "coordinates": coordinates, "flat_states": _STATE_COUNTER.value}
    if sum(int(row["maximal_flats"]) for row in coordinates) > RETAINED_CAP:
        return {"status": "CAP", "reason": "aggregate retained-flat cap", "coordinates": coordinates, "flat_states": _STATE_COUNTER.value}
    cover = cover_search(coordinates, variables)
    result = {
        "status": cover["status"],
        "flat_states": _STATE_COUNTER.value,
        "coordinates": [{key: value for key, value in row.items() if key != "candidates"} | {"candidate_count": len(row["candidates"])} for row in coordinates],
        "cover": cover,
    }
    if cover["status"] == "COVER":
        result["verification"] = verify_selection(cover["selection"], jobs, variables)
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    h11 = run_family(h11_jobs(), 23, parallel=False)
    if h11["status"] != "NO_COVER":
        raise AssertionError("H11 negative control")
    prepared = source.p199_prepare()
    if len(prepared["reps"]) != 1394 or len(prepared["option_masks"]) != 13:
        raise AssertionError("p199 interface")
    jobs = pattern_jobs(prepared["option_masks"], 1394)
    p199 = run_family(jobs, 1394, parallel=True)
    epistemic = "PROVED" if p199["status"] in {"COVER", "NO_COVER"} else "OBSERVED"
    result = {"status": "PASS", "epistemic_status": epistemic, "h11": h11, "p199": p199, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": "PASS", "h11": h11["status"], "p199": p199["status"], "flat_states": p199.get("flat_states"), "cover_nodes": p199.get("cover", {}).get("nodes"), "wall_seconds": result["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
