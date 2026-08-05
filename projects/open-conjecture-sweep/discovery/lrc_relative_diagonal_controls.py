#!/usr/bin/env python3
"""Generic controls for Cycle 49's diagonal-fiber packet theorem."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path
import time

from lrc_cube_rewrite import normalized_cube, pair_marginals
from lrc_relative_diagonal import PAIRS, cell_allowed, contract, pair_buffer, serialize, triple_buffers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle49-relative-diagonal"


def add(*tensors):
    result = defaultdict(Fraction)
    for tensor in tensors:
        for cell, value in tensor.items():
            result[cell] += value
    return {cell: value for cell, value in result.items() if value}


def packet_support_controls():
    triple_checks = 0
    pair_checks = 0
    for size in (5, 6):
        owners = tuple(range(size))
        for w in owners:
            for alternatives in itertools.permutations([owner for owner in owners if owner != w], 3):
                cube = normalized_cube((w, w, w), alternatives)
                for flags in itertools.product((0, 1), repeat=4):
                    pair_deleted = {pair: (1 << w if flags[index] else 0) for index, pair in enumerate(PAIRS)}
                    triple_deleted = 1 << w if flags[3] else 0
                    actual = {cell for cell in cube if not cell_allowed(cell, pair_deleted, triple_deleted)}
                    expected = set()
                    if any(flags):
                        expected.add((w, w, w))
                    if flags[0]: expected.add((w, w, alternatives[2]))
                    if flags[1]: expected.add((w, alternatives[1], w))
                    if flags[2]: expected.add((alternatives[0], w, w))
                    assert actual == expected
                    triple_checks += 1
        for left, right in PAIRS:
            other = 3 - left - right
            for values in itertools.permutations(owners, 5):
                w, c, terminal, a, b = values
                pivot = tuple(w if index in (left, right) else c for index in range(3))
                alternatives = [None, None, None]
                alternatives[left], alternatives[right], alternatives[other] = a, b, terminal
                cube = normalized_cube(pivot, tuple(alternatives))
                pair_deleted = {pair: 0 for pair in PAIRS}
                pair_deleted[(left, right)] = 1 << w
                actual = {cell for cell in cube if not cell_allowed(cell, pair_deleted, 0)}
                terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
                assert actual == {pivot, terminal_cell}
                pair_checks += 1
    return triple_checks, pair_checks


def support_five_control():
    owners = set(range(6))
    supports = [tuple(sorted(values)) for size in (5, 6) for values in itertools.combinations(owners, size)]
    checks = 0
    for state in itertools.product(supports, repeat=3):
        common = set(state[0]) & set(state[1]) & set(state[2])
        for w in common:
            assert triple_buffers(w, state)
            for left, right in PAIRS:
                other = 3 - left - right
                for c in state[other]:
                    terminals = [t for t in state[other] if t != w and (t == c or pair_buffer(left, right, w, c, t, state) is not None)]
                    assert terminals
            checks += 1
    return checks


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    triple_checks, pair_checks = packet_support_controls()
    support_five_checks = support_five_control()

    supports = (tuple(range(5)),) * 3
    pair_deleted = {pair: (1 << 0) | (1 << 1) for pair in PAIRS}
    positive = add(
        normalized_cube((0, 0, 0), (1, 2, 3)),
        normalized_cube((1, 1, 2), (0, 3, 4)),
    )
    assert all(not values for values in pair_marginals(positive).values())
    repaired = contract(positive, supports, pair_deleted, 1 << 0)
    assert repaired["status"] == "CONTRACTED"

    negative = {(0, 0, 0): Fraction(1), (0, 0, 1): Fraction(-1)}
    negative_supports = ((0,), (0,), (0, 1))
    negative_deleted = {(0, 1): 1, (0, 2): 0, (1, 2): 0}
    blocked = contract(negative, negative_supports, negative_deleted, 0)
    assert blocked["status"] == "BUFFER_INCOMPLETE"
    kernel_dimension = (len(negative_supports[0]) - 1) * (len(negative_supports[1]) - 1) * (len(negative_supports[2]) - 1)
    assert kernel_dimension == 0

    repeated = normalized_cube((0, 0, 1), (1, 2, 0))
    spill_deleted = {(0, 1): 1, (0, 2): 1 << 1, (1, 2): 0}
    repeated_forbidden = {cell for cell in repeated if not cell_allowed(cell, spill_deleted, 0)}
    expected_pair_fiber = {(0, 0, 1), (0, 0, 0)}
    assert repeated_forbidden - expected_pair_fiber

    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "GENERIC_RELATIVE_DIAGONAL_CONTROLS",
        "triple_packet_support_checks": triple_checks,
        "pair_packet_support_checks": pair_checks,
        "support_five_buffer_checks": support_five_checks,
        "positive_three_strata": {"status": repaired["status"], "steps": len(repaired["steps"]), "output": serialize(repaired["tensor"])},
        "negative_terminal_class": {"status": blocked["status"], "kernel_dimension": kernel_dimension, "defect": serialize(negative)},
        "repeated_buffer_spill_detected": True,
        "claim_boundary": "Generic packet-support and buffer controls only; no p199 full-domain hypothesis has been checked.",
        "wall_seconds": time.monotonic() - started,
    }
    path = OUT / "generic-controls.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("positive_three_strata", "negative_terminal_class", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
