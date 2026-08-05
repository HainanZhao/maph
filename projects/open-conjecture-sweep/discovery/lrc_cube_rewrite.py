"""Exact Möbius face tensors and triangular 2x2x2 cube repairs."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools


def clean(tensor):
    return {cell: value for cell, value in tensor.items() if value}


def pair_marginals(tensor):
    result = {}
    for left, right in itertools.combinations(range(3), 2):
        values = defaultdict(Fraction)
        for cell, coefficient in tensor.items():
            values[(cell[left], cell[right])] += coefficient
        result[(left, right)] = clean(values)
    return result


def mobius_tensor(pair_flows, distinguished):
    result = defaultdict(Fraction)
    d0, d1, d2 = distinguished
    for (a, b), value in pair_flows[(0, 1)].items():
        result[(a, b, d2)] += value
    for (a, c), value in pair_flows[(0, 2)].items():
        result[(a, d1, c)] += value
    for (b, c), value in pair_flows[(1, 2)].items():
        result[(d0, b, c)] += value
    result[(d0, d1, d2)] -= 2
    return clean(result)


def cell_allowed(types, cell, pair_deleted, triple_deleted):
    for left, right in itertools.combinations(range(3), 2):
        if cell[left] == cell[right] and pair_deleted[(left, right)] & (1 << cell[left]):
            return False
    return not (cell[0] == cell[1] == cell[2] and triple_deleted & (1 << cell[0]))


def normalized_cube(pivot, alternatives):
    pairs = [tuple(sorted((pivot[index], alternatives[index]))) for index in range(3)]
    if any(low == high for low, high in pairs):
        raise ValueError("degenerate cube")
    cube = {}
    for bits in itertools.product((0, 1), repeat=3):
        cell = tuple(pairs[index][bits[index]] for index in range(3))
        cube[cell] = Fraction((-1) ** sum(bits))
    return cube


def triangular_choices(pivot, supports, forbidden):
    choices = []
    for alternatives in itertools.product(*(tuple(owner for owner in supports[index] if owner != pivot[index]) for index in range(3))):
        cube = normalized_cube(pivot, alternatives)
        if all(cell == pivot or cell not in forbidden or cell > pivot for cell in cube):
            choices.append((tuple(alternatives), cube))
    return sorted(choices, key=lambda row: row[0])


def chosen_cubes(supports, forbidden):
    result = {}
    choice_counts = {}
    for pivot in sorted(forbidden):
        choices = triangular_choices(pivot, supports, forbidden)
        choice_counts[pivot] = len(choices)
        result[pivot] = choices[0][1] if choices else None
    return result, choice_counts


def normal_form(tensor, forbidden, reducers):
    state = defaultdict(Fraction, tensor)
    steps = []
    for pivot in sorted(forbidden):
        coefficient = state[pivot]
        if not coefficient:
            continue
        cube = reducers[pivot]
        if cube is None:
            return {"status": "UNREPAIRED", "tensor": clean(state), "first_missing": pivot, "steps": steps}
        scale = coefficient / cube[pivot]
        for cell, value in cube.items():
            state[cell] -= scale * value
        if state[pivot]:
            raise AssertionError("pivot not killed")
        if any(state[cell] for cell in forbidden if cell < pivot):
            raise AssertionError("earlier defect reintroduced")
        steps.append((pivot, scale))
    state = clean(state)
    if any(cell in forbidden for cell in state):
        raise AssertionError("forbidden normal-form support")
    return {"status": "REPAIRED", "tensor": state, "first_missing": None, "steps": steps}


def subtract_normalized(left, right, pivot):
    result = defaultdict(Fraction)
    for cell, value in left.items():
        result[cell] += value / left[pivot]
    for cell, value in right.items():
        result[cell] -= value / right[pivot]
    return clean(result)


def serialize_tensor(tensor):
    return [[list(cell), value.numerator, value.denominator] for cell, value in sorted(tensor.items())]
