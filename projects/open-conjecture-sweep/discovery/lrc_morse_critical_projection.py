#!/usr/bin/env python3
"""Exact distinguished-owner algebraic-Morse flow for Cycle 45."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import heapq
import itertools


def clean(chain):
    return {cell: value for cell, value in chain.items() if value}


def add(left, right, scale=Fraction(1)):
    result = defaultdict(Fraction, left)
    for cell, value in right.items():
        result[cell] += scale * value
    return clean(result)


def boundary_cell(cell):
    if not cell:
        return {}
    return {cell[:index] + cell[index + 1:]: Fraction((-1) ** index) for index in range(len(cell))}


def boundary(chain):
    result = defaultdict(Fraction)
    for cell, coefficient in chain.items():
        for face, incidence in boundary_cell(cell).items():
            result[face] += coefficient * incidence
    return clean(result)


def build_complex(supports, pair_deleted, triple_deleted):
    """Return the augmented downward-closed four-partite complex."""
    cells = {dimension: [] for dimension in range(-1, 4)}
    cells[-1] = [()]
    all_cells = {()}
    for size in range(1, 5):
        for parts in itertools.combinations(range(4), size):
            for owners in itertools.product(*(supports[part] for part in parts)):
                cell = tuple(zip(parts, owners))
                allowed = True
                for left, right in itertools.combinations(range(size), 2):
                    a, b = parts[left], parts[right]
                    if owners[left] == owners[right] and pair_deleted.get((a, b), 0) & (1 << owners[left]):
                        allowed = False
                        break
                if not allowed:
                    continue
                for positions in itertools.combinations(range(size), 3):
                    chosen_parts = tuple(parts[index] for index in positions)
                    chosen_owners = tuple(owners[index] for index in positions)
                    if len(set(chosen_owners)) == 1 and triple_deleted.get(chosen_parts, 0) & (1 << chosen_owners[0]):
                        allowed = False
                        break
                if allowed:
                    cells[size - 1].append(cell)
                    all_cells.add(cell)
    for dimension in cells:
        cells[dimension].sort()
    if any(face not in all_cells for cell in all_cells for face in boundary_cell(cell)):
        raise AssertionError("complex is not downward closed")
    return cells, all_cells


def lexicographic_matching(cells, all_cells, distinguished, vertex_schedule=None):
    """Frozen greedy matching and its reversed-arrow acyclicity certificate."""
    unmatched = set(all_cells)
    lower_to_upper = {}
    upper_to_lower = {}
    schedule = vertex_schedule or tuple((part, distinguished[part]) for part in range(4))
    for part, owner in schedule:
        vertex = (part, owner)
        for dimension in range(-1, 3):
            for lower in cells[dimension]:
                if lower not in unmatched or any(item[0] == part for item in lower):
                    continue
                upper = tuple(sorted(lower + (vertex,)))
                if upper in unmatched and upper in all_cells:
                    lower_to_upper[lower] = upper
                    upper_to_lower[upper] = lower
                    unmatched.remove(lower)
                    unmatched.remove(upper)
    arrows = defaultdict(set)
    indegree = {cell: 0 for cell in all_cells}
    for upper in all_cells:
        for lower in boundary_cell(upper):
            if lower_to_upper.get(lower) == upper:
                source, target = lower, upper
            else:
                source, target = upper, lower
            if target not in arrows[source]:
                arrows[source].add(target)
                indegree[target] += 1
    ready = sorted(cell for cell, degree in indegree.items() if degree == 0)
    heapq.heapify(ready)
    order = []
    while ready:
        cell = heapq.heappop(ready)
        order.append(cell)
        for target in sorted(arrows[cell]):
            indegree[target] -= 1
            if indegree[target] == 0:
                heapq.heappush(ready, target)
    cycle_cells = sorted(cell for cell, degree in indegree.items() if degree)
    return {"lower_to_upper": lower_to_upper, "upper_to_lower": upper_to_lower, "critical": sorted(unmatched), "acyclic": not cycle_cells, "topological_order": order, "cycle_cells": cycle_cells}


def vector(chain, matching):
    result = defaultdict(Fraction)
    for lower, coefficient in chain.items():
        upper = matching["lower_to_upper"].get(lower)
        if upper is None:
            continue
        incidence = boundary_cell(upper)[lower]
        result[upper] -= coefficient / incidence
    return clean(result)


def flow(chain, matching):
    # Phi = I + dV + Vd.
    return add(add(chain, boundary(vector(chain, matching))), vector(boundary(chain), matching))


def stabilize(chain, matching, maximum_steps=None):
    if not matching["acyclic"]:
        return {"status": "MATCHING_CYCLE", "cycle_cells": matching["cycle_cells"]}
    maximum_steps = maximum_steps or (len(matching["topological_order"]) + 1)
    current = clean(chain)
    seen = set()
    vector_sum = defaultdict(Fraction)
    for step in range(maximum_steps + 1):
        key = tuple(sorted(current.items()))
        if key in seen:
            return {"status": "FLOW_CYCLE", "step": step, "chain": current}
        seen.add(key)
        moved = vector(current, matching)
        for cell, value in moved.items():
            vector_sum[cell] += value
        following = flow(current, matching)
        if following == current:
            # Phi^N - I = d(V sum Phi^i) + (V sum Phi^i)d.
            return {"status": "STABLE", "projection": current, "positive_homotopy": clean(vector_sum), "steps": step}
        current = following
    return {"status": "STEP_CAP", "chain": current, "steps": maximum_steps}


def verify_basis_identity(cells, matching):
    projections = {}
    positive_homotopies = {}
    maximum_steps = 0
    for dimension in range(-1, 4):
        for cell in cells[dimension]:
            outcome = stabilize({cell: Fraction(1)}, matching)
            if outcome["status"] != "STABLE":
                return {"status": outcome["status"], "cell": cell, "detail": outcome}
            projections[cell] = outcome["projection"]
            positive_homotopies[cell] = outcome["positive_homotopy"]
            maximum_steps = max(maximum_steps, outcome["steps"])
    for dimension in range(-1, 4):
        for cell in cells[dimension]:
            left = add({cell: Fraction(1)}, projections[cell], scale=Fraction(-1))
            # I - pi = -(dH + Hd) for H = V sum Phi^i.
            right = boundary(positive_homotopies[cell])
            lower_h = defaultdict(Fraction)
            for face, incidence in boundary_cell(cell).items():
                for target, value in positive_homotopies[face].items():
                    lower_h[target] += incidence * value
            right = add(right, lower_h)
            if left != {key: -value for key, value in right.items()}:
                return {"status": "IDENTITY_FAILURE", "cell": cell, "left": left, "positive_rhs": right}
        # Chain-map identity d pi = pi d.
        for cell in cells[dimension]:
            left = boundary(projections[cell])
            right = defaultdict(Fraction)
            for face, incidence in boundary_cell(cell).items():
                for target, value in projections[face].items():
                    right[target] += incidence * value
            if left != clean(right):
                return {"status": "CHAIN_MAP_FAILURE", "cell": cell, "left": left, "right": clean(right)}
    return {"status": "PASS", "basis_cells": sum(len(values) for values in cells.values()), "matched_pairs": len(matching["lower_to_upper"]), "critical_cells": len(matching["critical"]), "maximum_flow_steps": maximum_steps}
