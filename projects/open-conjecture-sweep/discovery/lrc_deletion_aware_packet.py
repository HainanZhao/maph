"""Cycle 50's frozen deletion-aware triple-packet selector."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools

from lrc_cube_rewrite import clean, normalized_cube, pair_marginals
from lrc_relative_diagonal import PAIRS, apply_cube, cell_allowed, terminal_choice


def admissible_triple_packet(state, pivot, supports, pair_deleted, triple_deleted):
    """First cube that simultaneously discharges every forbidden cube vertex."""
    options = [tuple(owner for owner in support if owner != pivot[index]) for index, support in enumerate(supports)]
    for alternatives in itertools.product(*options):
        cube = normalized_cube(pivot, alternatives)
        scale = state[pivot] / cube[pivot]
        if all(
            cell_allowed(cell, pair_deleted, triple_deleted)
            or state[cell] - scale * value == 0
            for cell, value in cube.items()
        ):
            return alternatives, cube
    return None


def contract(source, supports, pair_deleted, triple_deleted):
    """Apply the frozen C50 triple rule, then the unchanged C49 pair stage."""
    supports = tuple(tuple(sorted(values)) for values in supports)
    state = defaultdict(Fraction, source)
    original_marginals = pair_marginals(clean(state))
    steps = []

    for w in sorted(set(supports[0]) & set(supports[1]) & set(supports[2])):
        pivot = (w, w, w)
        if not state[pivot] or cell_allowed(pivot, pair_deleted, triple_deleted):
            continue
        selected = admissible_triple_packet(state, pivot, supports, pair_deleted, triple_deleted)
        if selected is None:
            return {"status": "NO_ADMISSIBLE_PACKET", "stage": "TRIPLE", "pivot": pivot, "tensor": clean(state), "steps": steps}
        alternatives, cube = selected
        scale = apply_cube(state, cube, pivot)
        assert all(
            cell_allowed(cell, pair_deleted, triple_deleted) or not state[cell]
            for cell in cube
        )
        steps.append(("TRIPLE_DELETION_AWARE", pivot, alternatives, scale))

    if any(
        state[(w, w, w)] and not cell_allowed((w, w, w), pair_deleted, triple_deleted)
        for w in set(supports[0]) & set(supports[1]) & set(supports[2])
    ):
        raise AssertionError("triple stage left a triple coefficient")

    for left, right in PAIRS:
        other = 3 - left - right
        deleted = pair_deleted[(left, right)]
        for w in sorted(set(supports[left]) & set(supports[right])):
            if not deleted & (1 << w):
                continue
            if original_marginals[(left, right)].get((w, w), Fraction(0)):
                raise AssertionError("deleted pair marginal is nonzero")
            active_c = [
                c for c in supports[other]
                if state[tuple(w if index in (left, right) else c for index in range(3))]
            ]
            if not active_c:
                continue
            choice = terminal_choice(left, right, w, active_c, supports)
            if choice is None:
                pivot_c = next((c for c in active_c if c != w), w)
                pivot = tuple(w if index in (left, right) else pivot_c for index in range(3))
                return {"status": "BUFFER_INCOMPLETE", "stage": f"PAIR_{left}{right}", "pivot": pivot, "tensor": clean(state), "steps": steps}
            terminal, buffers = choice
            for c in sorted(active_c):
                pivot = tuple(w if index in (left, right) else c for index in range(3))
                if c in (w, terminal) or not state[pivot]:
                    continue
                a, b = buffers[c]
                alternatives = [None, None, None]
                alternatives[left], alternatives[right], alternatives[other] = a, b, terminal
                cube = normalized_cube(pivot, tuple(alternatives))
                terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
                forbidden = {cell for cell in cube if not cell_allowed(cell, pair_deleted, triple_deleted)}
                if forbidden - {pivot, terminal_cell}:
                    raise AssertionError("C49 pair stage spilled into another stratum")
                scale = apply_cube(state, cube, pivot)
                steps.append((f"PAIR_{left}{right}", pivot, tuple(alternatives), scale))
            terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
            if state[terminal_cell]:
                return {"status": "NONZERO_TERMINAL", "stage": f"PAIR_{left}{right}", "pivot": terminal_cell, "tensor": clean(state), "steps": steps}

    result = clean(state)
    if pair_marginals(result) != original_marginals:
        raise AssertionError("contraction changed pair marginals")
    forbidden = {cell for cell in result if not cell_allowed(cell, pair_deleted, triple_deleted)}
    if forbidden:
        raise AssertionError("contraction left forbidden support")
    return {"status": "CONTRACTED", "tensor": result, "steps": steps}
