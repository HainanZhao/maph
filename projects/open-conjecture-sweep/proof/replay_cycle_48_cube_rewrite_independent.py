#!/usr/bin/env python3
"""Independent reverse-order full replay of Cycle 48 cube repairs."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle48-cube-rewrite"


def clean(values):
    return {key: value for key, value in values.items() if value}


def parse(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def serialize(values):
    return [[list(cell), value.numerator, value.denominator] for cell, value in sorted(values.items())]


def marginals(tensor):
    result = {}
    for left, right in ((2, 1), (2, 0), (1, 0)):
        values = defaultdict(Fraction)
        for cell, coefficient in reversed(sorted(tensor.items())):
            values[(cell[right], cell[left])] += coefficient
        result[(right, left)] = clean(values)
    return result


def mobius(flows, distinguished):
    values = defaultdict(Fraction)
    d0, d1, d2 = distinguished
    for (b, c), coefficient in reversed(sorted(flows[(1, 2)].items())):
        values[(d0, b, c)] += coefficient
    for (a, c), coefficient in reversed(sorted(flows[(0, 2)].items())):
        values[(a, d1, c)] += coefficient
    for (a, b), coefficient in reversed(sorted(flows[(0, 1)].items())):
        values[(a, b, d2)] += coefficient
    values[(d0, d1, d2)] -= 2
    return clean(values)


def allowed(cell, pair_deleted, triple_deleted):
    for left, right in itertools.combinations(range(3), 2):
        if cell[left] == cell[right] and pair_deleted[(left, right)] & (1 << cell[left]):
            return False
    return not (cell[0] == cell[1] == cell[2] and triple_deleted & (1 << cell[0]))


def cube(pivot, alternatives):
    pairs = [tuple(sorted((pivot[index], alternatives[index]))) for index in range(3)]
    return {tuple(pairs[index][bits[index]] for index in range(3)): Fraction((-1) ** sum(bits)) for bits in itertools.product((0, 1), repeat=3)}


def choices(pivot, supports, forbidden):
    found = []
    pools = [tuple(owner for owner in reversed(supports[index]) if owner != pivot[index]) for index in range(3)]
    for alternatives in itertools.product(*pools):
        candidate = cube(pivot, alternatives)
        if all(cell == pivot or cell not in forbidden or cell > pivot for cell in candidate):
            found.append((alternatives, candidate))
    return sorted(found, key=lambda row: row[0])


def reduce_tensor(source, forbidden, reducers):
    state = defaultdict(Fraction, source)
    steps = []
    for pivot in sorted(forbidden):
        coefficient = state[pivot]
        if not coefficient:
            continue
        candidate = reducers[pivot]
        if candidate is None:
            return "UNREPAIRED", clean(state), pivot, steps
        scale = coefficient / candidate[pivot]
        for cell, value in reversed(sorted(candidate.items())):
            state[cell] -= scale * value
        assert not state[pivot]
        steps.append((pivot, scale))
    state = clean(state)
    assert not (set(state) & forbidden)
    return "REPAIRED", state, None, steps


def difference(left, right, pivot):
    values = defaultdict(Fraction)
    for cell, value in left.items():
        values[cell] += value / left[pivot]
    for cell, value in right.items():
        values[cell] -= value / right[pivot]
    return clean(values)


def replay(source, expected):
    supports = tuple(tuple(row) for row in source["supports"])
    pair_deleted = {(left, right): deleted for left, right, deleted in source["pair_deleted"]}
    triple_deleted = source["triple_deleted"]
    flows = {(left, right): parse(rows) for left, right, rows in source["pair_flows"]}
    start = mobius(flows, tuple(source["distinguished"]))
    assert marginals(start) == flows
    forbidden = {cell for cell in itertools.product(*supports) if not allowed(cell, pair_deleted, triple_deleted)}
    choice_map = {pivot: choices(pivot, supports, forbidden) for pivot in sorted(forbidden, reverse=True)}
    reducers = {pivot: rows[0][1] if rows else None for pivot, rows in choice_map.items()}
    status, final, missing, steps = reduce_tensor(start, forbidden, reducers)
    repair_status = "UNREPAIRED" if status == "UNREPAIRED" else "STRONG_REPAIR" if all(reducers.values()) else "TARGETED_REPAIR"
    assert repair_status == expected["repair_status"]
    assert serialize(start) == expected["mobius"] and serialize(final) == expected["repaired_tensor"]
    assert (list(missing) if missing else None) == expected["first_missing"]
    assert len(steps) == expected["repair_steps"]
    if status == "REPAIRED":
        assert marginals(final) == flows

    first = None
    tested = 0
    if status == "REPAIRED":
        for pivot, _scale in steps:
            chosen = reducers[pivot]
            for alternatives, candidate in choice_map[pivot][1:]:
                tested += 1
                raw_difference = difference(candidate, chosen, pivot)
                dstatus, normal, dmissing, _ = reduce_tensor(raw_difference, forbidden, reducers)
                if dstatus == "UNREPAIRED" or normal:
                    assert all(not values for values in marginals(raw_difference).values())
                    assert all(not values for values in marginals(normal).values())
                    first = {
                        "pivot": list(pivot), "alternative_owners": list(alternatives),
                        "status": "UNJOINABLE" if dstatus == "REPAIRED" else "UNREPAIRED_BRANCH_DIFFERENCE",
                        "difference": serialize(raw_difference), "normal_form": serialize(normal),
                        "first_missing": list(dmissing) if dmissing else None,
                    }
                    break
            if first:
                break
    assert tested == expected["critical_diamonds_tested"] and first == expected["first_diamond"]
    assert ("NONCONFLUENT" if first else "NO_NONJOINABLE_REACHED_DIAMOND") == expected["confluence_status"]
    return repair_status, expected["confluence_status"], len(forbidden), sum(len(rows) for rows in choice_map.values()), len(steps), tested


def main():
    started = time.monotonic()
    selection = json.loads((OUT / "selection.json").read_text())
    actual = json.loads((OUT / "actual.json").read_text())
    assert len(selection["selected"]) == len(actual["records"]) == 512
    aggregates = Counter()
    records = []
    for ordinal in reversed(range(512)):
        source = selection["selected"][ordinal]
        expected = actual["records"][ordinal]
        outcome = replay(source, expected)
        aggregates[("repair", outcome[0])] += 1
        aggregates[("confluence", outcome[1])] += 1
        for label, value in zip(("forbidden", "cubes", "steps", "diamonds"), outcome[2:]):
            aggregates[("total", label)] += value
        records.append({"ordinal": ordinal, "types": source["types"], "repair_status": outcome[0], "confluence_status": outcome[1]})
        if ordinal % 32 == 0:
            print(json.dumps({"replayed": 512 - ordinal, "remaining": ordinal}), flush=True)
    assert dict(sorted((key[1], value) for key, value in aggregates.items() if key[0] == "repair")) == actual["repair_status_counts"]
    assert dict(sorted((key[1], value) for key, value in aggregates.items() if key[0] == "confluence")) == actual["confluence_status_counts"]
    assert aggregates[("total", "forbidden")] == actual["aggregate_forbidden_cells"]
    assert aggregates[("total", "cubes")] == actual["aggregate_cube_candidates"]
    assert aggregates[("total", "steps")] == actual["aggregate_repair_steps"]
    assert aggregates[("total", "diamonds")] == actual["aggregate_critical_diamonds"]
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "INDEPENDENT_FULL_CUBE_REWRITE_REPLAY",
        "faces": 512, "repair_status_counts": actual["repair_status_counts"],
        "confluence_status_counts": actual["confluence_status_counts"],
        "aggregate_forbidden_cells": actual["aggregate_forbidden_cells"],
        "aggregate_cube_candidates": actual["aggregate_cube_candidates"],
        "aggregate_repair_steps": actual["aggregate_repair_steps"],
        "aggregate_critical_diamonds": actual["aggregate_critical_diamonds"],
        "records": sorted(records, key=lambda row: row["ordinal"]),
        "claim_boundary": "Independent reverse-order full replay of the frozen 512-face material corpus only.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "independent-replay.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("records", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
