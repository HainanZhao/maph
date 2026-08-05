#!/usr/bin/env python3
"""Cycle 41 exploratory chain-filling probe for the first delta conflict."""
from __future__ import annotations

from collections import defaultdict, deque
from fractions import Fraction
import itertools
import json
from pathlib import Path
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"


def transport(left: int, right: int, diagonal: int, marginals, masks):
    component_rows, adjacency = c40.graph_components(masks[left], masks[right], diagonal)
    remaining = {}
    for owner in range(13):
        if masks[left] & (1 << owner):
            remaining[owner] = marginals[left].get(owner, Fraction(0))
        if masks[right] & (1 << owner):
            remaining[13 + owner] = marginals[right].get(owner, Fraction(0))
    flows = defaultdict(Fraction)
    for component in component_rows:
        if len(component) == 1:
            if remaining[component[0]]:
                raise AssertionError("isolated imbalance")
            continue
        tree = {vertex: set() for vertex in component}
        seen = {component[0]}
        queue = deque([component[0]])
        while queue:
            vertex = queue.popleft()
            for neighbor in sorted(adjacency[vertex]):
                if neighbor in component and neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
                    tree[vertex].add(neighbor)
                    tree[neighbor].add(vertex)
        active = set(component)
        while len(active) > 1:
            leaf = min(vertex for vertex in active if len(tree[vertex] & active) == 1)
            neighbor = next(iter(tree[leaf] & active))
            value = remaining[leaf]
            edge = (leaf, neighbor) if leaf < 13 else (neighbor, leaf)
            flows[(edge[0], edge[1] - 13)] += value
            remaining[neighbor] -= value
            remaining[leaf] = 0
            active.remove(leaf)
        if remaining[next(iter(active))]:
            raise AssertionError("terminal imbalance")
    return {key: value for key, value in flows.items() if value}


def oriented_transport(left, right, combined_deleted, marginals, masks):
    if left <= right:
        return transport(left, right, combined_deleted.get((left, right), 0), marginals, masks)
    return {(column, row): value for (row, column), value in transport(right, left, combined_deleted.get((right, left), 0), marginals, masks).items()}


def relation_components(left_mask, right_mask, deleted_cells):
    vertices = [owner for owner in range(13) if left_mask & (1 << owner)] + [13 + owner for owner in range(13) if right_mask & (1 << owner)]
    adjacency = {vertex: [] for vertex in vertices}
    for i in range(13):
        if not left_mask & (1 << i):
            continue
        for j in range(13):
            if right_mask & (1 << j) and not deleted_cells & (1 << (13 * i + j)):
                adjacency[i].append(13 + j)
                adjacency[13 + j].append(i)
    result = []
    unseen = set(vertices)
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        result.append(tuple(sorted(component)))
    return result, adjacency


def relation_transport(left, right, deleted_cells, marginals, masks):
    component_rows, adjacency = relation_components(masks[left], masks[right], deleted_cells)
    remaining = {}
    for owner in range(13):
        if masks[left] & (1 << owner):
            remaining[owner] = marginals[left].get(owner, Fraction(0))
        if masks[right] & (1 << owner):
            remaining[13 + owner] = marginals[right].get(owner, Fraction(0))
    flows = defaultdict(Fraction)
    for component in component_rows:
        tree = {vertex: set() for vertex in component}
        seen = {component[0]}
        queue = deque([component[0]])
        while queue:
            vertex = queue.popleft()
            for neighbor in sorted(adjacency[vertex]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
                    tree[vertex].add(neighbor)
                    tree[neighbor].add(vertex)
        active = set(component)
        while len(active) > 1:
            leaf = min(vertex for vertex in active if len(tree[vertex] & active) == 1)
            neighbor = next(iter(tree[leaf] & active))
            value = remaining[leaf]
            edge = (leaf, neighbor) if leaf < 13 else (neighbor, leaf)
            flows[(edge[0], edge[1] - 13)] += value
            remaining[neighbor] -= value
            remaining[leaf] = 0
            active.remove(leaf)
        if remaining[next(iter(active))]:
            raise AssertionError("relation component imbalance")
    return {key: value for key, value in flows.items() if value}


def oriented_relation_transport(left, right, deleted_by_pair, marginals, masks):
    if left <= right:
        flow = relation_transport(left, right, deleted_by_pair.get((left, right), 0), marginals, masks)
        if left == right:
            keys = set(flow) | {(column, row) for row, column in flow}
            return {key: (flow.get(key, Fraction(0)) + flow.get((key[1], key[0]), Fraction(0))) / 2 for key in keys if flow.get(key, Fraction(0)) + flow.get((key[1], key[0]), Fraction(0))}
        return flow
    return {(column, row): value for (row, column), value in relation_transport(right, left, deleted_by_pair.get((right, left), 0), marginals, masks).items()}


def fill_residual(types, original_deleted, relation_deleted, marginals, original_masks, transport_masks, rank_three_deleted=0):
    s, t, u = types
    pair_rows = [oriented_relation_transport(s, t, relation_deleted, marginals, transport_masks), oriented_relation_transport(s, u, relation_deleted, marginals, transport_masks), oriented_relation_transport(t, u, relation_deleted, marginals, transport_masks)]
    keys = []
    rhs = []
    for pair_index, pair in enumerate(((s, t), (s, u), (t, u))):
        left_mask, right_mask = original_masks[pair[0]], original_masks[pair[1]]
        for i in range(13):
            if not left_mask & (1 << i):
                continue
            for j in range(13):
                if right_mask & (1 << j):
                    keys.append((pair_index, i, j))
                    rhs.append(float(pair_rows[pair_index].get((i, j), 0)))
    row_id = {key: index for index, key in enumerate(keys)}
    rows = []
    columns = []
    values = []
    cell_count = 0
    d_st = original_deleted.get(tuple(sorted((s, t))), 0)
    d_su = original_deleted.get(tuple(sorted((s, u))), 0)
    d_tu = original_deleted.get(tuple(sorted((t, u))), 0)
    for i, j, k in itertools.product(range(13), repeat=3):
        if not (original_masks[s] & (1 << i) and original_masks[t] & (1 << j) and original_masks[u] & (1 << k)):
            continue
        if (i == j and d_st & (1 << i)) or (i == k and d_su & (1 << i)) or (j == k and d_tu & (1 << j)):
            continue
        if i == j == k and rank_three_deleted & (1 << i):
            continue
        for key in ((0, i, j), (1, i, k), (2, j, k)):
            rows.append(row_id[key])
            columns.append(cell_count)
            values.append(1.0)
        cell_count += 1
    matrix = coo_matrix((values, (rows, columns)), shape=(len(keys), cell_count)).tocsr()
    solved = lsqr(matrix, np.asarray(rhs), atol=1e-12, btol=1e-12, iter_lim=10000)
    return {"cells": cell_count, "equations": len(keys), "residual_norm": float(solved[3]), "iterations": int(solved[2]), "numerically_fillable": float(solved[3]) <= 1e-9}


def gf2_rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def homology_dimension(types, original_deleted, masks, rank_three_deleted=0):
    s, t, u = types
    supports = [[owner for owner in range(13) if masks[index] & (1 << owner)] for index in types]
    deleted = [original_deleted.get(tuple(sorted(pair)), 0) for pair in ((s, t), (s, u), (t, u))]
    vertices = [(part, owner) for part in range(3) for owner in supports[part]]
    vertex_id = {value: index for index, value in enumerate(vertices)}
    edges = []
    for pair_index, (a, b) in enumerate(((0, 1), (0, 2), (1, 2))):
        for i in supports[a]:
            for j in supports[b]:
                if not (i == j and deleted[pair_index] & (1 << i)):
                    edges.append(((a, i), (b, j)))
    edge_id = {edge: index for index, edge in enumerate(edges)}
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = 0
    unseen = set(vertices)
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    triangle_boundaries = []
    for i, j, k in itertools.product(*supports):
        if i == j == k and rank_three_deleted & (1 << i):
            continue
        candidate = [((0, i), (1, j)), ((0, i), (2, k)), ((1, j), (2, k))]
        if all(edge in edge_id for edge in candidate):
            boundary = 0
            for edge in candidate:
                boundary ^= 1 << edge_id[edge]
            triangle_boundaries.append(boundary)
    boundary_one_rank = len(vertices) - components
    boundary_two_rank = gf2_rank(triangle_boundaries)
    return len(edges) - boundary_one_rank - boundary_two_rank


def main():
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << coordinate for coordinate, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    prior = json.loads((OUT / "zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in rows} for rows in prior["singleton_marginals_by_complete_type"]]

    original = defaultdict(int)
    rank3_induced = defaultdict(int)
    for coordinate in range(13):
        row = c40.coordinate_classes(coordinate)
        for pair in row["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << coordinate
        for pair in row["induced_pair_deletions"]:
            rank3_induced[tuple(pair)] |= 1 << coordinate

    small_types = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in original.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in small_types:
                    blocked[(left, owner)].append(right)
                if right in small_types:
                    blocked[(right, owner)].append(left)
    transport_masks = list(masks)
    for mediator in small_types:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                transport_masks[neighbor] &= ~(1 << owners[0])
    relation_deleted = defaultdict(int)
    for pair in set(original) | set(rank3_induced):
        for owner in range(13):
            if (original.get(pair, 0) | rank3_induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in small_types:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) != 2:
            continue
        a, b = owners
        for left in blocked[(mediator, a)]:
            for right in blocked[(mediator, b)]:
                if left <= right:
                    relation_deleted[(left, right)] |= 1 << (13 * a + b)
                    if left == right:
                        relation_deleted[(left, right)] |= 1 << (13 * b + a)
                else:
                    relation_deleted[(right, left)] |= 1 << (13 * b + a)
    first = primary["first_violations"][0]
    selected = [next(iter(row)) for row in marginals]
    interface_pairs = {}
    for (left, right), deleted in sorted(original.items()):
        owner = selected[left]
        if owner == selected[right] and deleted & (1 << owner):
            key = (masks[left], masks[right], deleted, owner)
            interface_pairs.setdefault(key, (left, right))
    chosen_pairs = list(interface_pairs.values())[:100]
    representatives = {}
    for type_index, mask in enumerate(masks):
        representatives.setdefault(mask, type_index)
    tested = failed_count = nonzero_h1_count = 0
    maximum_residual = 0.0
    maximum_h1 = 0
    first_failed = first_nonzero = None
    for left, right in chosen_pairs:
        for third in representatives.values():
            row = fill_residual((left, right, third), original, relation_deleted, marginals, masks, transport_masks)
            row["h1_dimension_gf2"] = homology_dimension((left, right, third), original, masks)
            row.update({"left_type": left, "right_type": right, "third_type": third, "third_mask": masks[third]})
            tested += 1
            maximum_residual = max(maximum_residual, row["residual_norm"])
            maximum_h1 = max(maximum_h1, row["h1_dimension_gf2"])
            if not row["numerically_fillable"]:
                failed_count += 1
                first_failed = first_failed or row
            if row["h1_dimension_gf2"]:
                nonzero_h1_count += 1
                first_nonzero = first_nonzero or row
    result = {"status": "PASS", "epistemic_status": "OBSERVED", "stage": "CHAIN_FILLING_INTERFACE_PROBE", "first_conflict": first, "available_violated_pair_interfaces": len(interface_pairs), "tested_violated_pair_interfaces": len(chosen_pairs), "owner_mask_representatives": len(representatives), "tested_triple_interfaces": tested, "numerically_unfillable": failed_count, "first_unfillable": first_failed, "maximum_residual_norm": maximum_residual, "nonzero_h1_gf2": nonzero_h1_count, "maximum_h1_dimension_gf2": maximum_h1, "first_nonzero_h1": first_nonzero, "claim_boundary": "The filling residual is floating; the GF(2) boundary ranks are exact. This tests at most 100 lexicographic violated pair interfaces crossed with all 116 third-owner masks, not the complete interface."}
    temporary = OUT / "fill-probe.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "fill-probe.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
