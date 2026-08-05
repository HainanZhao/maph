"""Exact two-stage contraction of forbidden diagonal fibers."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools

from lrc_cube_rewrite import clean, normalized_cube, pair_marginals

PAIRS = ((0, 1), (0, 2), (1, 2))


def cell_allowed(cell, pair_deleted, triple_deleted):
    for left, right in PAIRS:
        if cell[left] == cell[right] and pair_deleted[(left, right)] & (1 << cell[left]):
            return False
    return not (cell[0] == cell[1] == cell[2] and triple_deleted & (1 << cell[0]))


def apply_cube(state, cube, pivot):
    coefficient = state[pivot]
    if not coefficient:
        return Fraction(0)
    scale = coefficient / cube[pivot]
    for cell, value in cube.items():
        state[cell] -= scale * value
    if state[pivot]:
        raise AssertionError("packet failed to kill pivot")
    return scale


def triple_buffers(w, supports):
    """Lexicographically ordered SDRs in S_i minus w."""
    return [
        values for values in itertools.product(*(tuple(owner for owner in support if owner != w) for support in supports))
        if len(set(values)) == 3
    ]


def pair_buffer(left, right, w, c, terminal, supports):
    """Least two buffers making w,c,t,a,b pairwise distinct."""
    forbidden = {w, c, terminal}
    for a in supports[left]:
        if a in forbidden:
            continue
        for b in supports[right]:
            if b not in forbidden and b != a:
                return a, b
    return None


def terminal_choice(left, right, w, active_c, supports):
    other = 3 - left - right
    if not any(c != w for c in active_c):
        return w, {}
    for terminal in supports[other]:
        if terminal == w:
            continue
        choices = {}
        for c in active_c:
            if c in (w, terminal):
                continue
            buffers = pair_buffer(left, right, w, c, terminal, supports)
            if buffers is None:
                break
            choices[c] = buffers
        else:
            return terminal, choices
    return None


def contract(source, supports, pair_deleted, triple_deleted):
    """Run the frozen triple-intersection then pair-fiber contraction."""
    supports = tuple(tuple(sorted(values)) for values in supports)
    state = defaultdict(Fraction, source)
    original_marginals = pair_marginals(clean(state))
    steps = []

    # Move each active triple intersection into its incident pair fibers.
    for w in sorted(set(supports[0]) & set(supports[1]) & set(supports[2])):
        pivot = (w, w, w)
        if not state[pivot] or cell_allowed(pivot, pair_deleted, triple_deleted):
            continue
        choices = triple_buffers(w, supports)
        if not choices:
            return {"status": "BUFFER_INCOMPLETE", "stage": "TRIPLE", "pivot": pivot, "tensor": clean(state), "steps": steps}
        alternatives = choices[0]
        cube = normalized_cube(pivot, alternatives)
        before_forbidden = {cell for cell in cube if not cell_allowed(cell, pair_deleted, triple_deleted)}
        if any(cell != pivot and len(set(cell)) != 2 for cell in before_forbidden):
            raise AssertionError("triple packet has unexpected forbidden support")
        scale = apply_cube(state, cube, pivot)
        steps.append(("TRIPLE", pivot, alternatives, scale))

    if any(
        state[(w, w, w)] and not cell_allowed((w, w, w), pair_deleted, triple_deleted)
        for w in set(supports[0]) & set(supports[1]) & set(supports[2])
    ):
        raise AssertionError("triple stage left a triple coefficient")

    # Each remaining forbidden cell belongs to exactly one pair stratum.
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
                if c in (w, terminal) or not state[tuple(w if index in (left, right) else c for index in range(3))]:
                    continue
                a, b = buffers[c]
                pivot = tuple(w if index in (left, right) else c for index in range(3))
                alternatives = [None, None, None]
                alternatives[left] = a
                alternatives[right] = b
                alternatives[other] = terminal
                cube = normalized_cube(pivot, tuple(alternatives))
                forbidden = {cell for cell in cube if not cell_allowed(cell, pair_deleted, triple_deleted)}
                terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
                if forbidden - {pivot, terminal_cell}:
                    raise AssertionError("pair packet spilled into another stratum")
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


def serialize(tensor):
    return [[list(cell), value.numerator, value.denominator] for cell, value in sorted(tensor.items())]
