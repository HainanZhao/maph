#!/usr/bin/env python3
"""Independent semantic/census replay of Cycle 41's multiplied-ideal result."""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as prior

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal/independent-replay.json"
TYPE_ID = {}
TYPE_MASKS = []
SMALL = set()


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    pairs = set()
    induced = set()
    small_rank3 = set()
    counts = {2: 0, 3: 0}
    for pattern in reversed(prior._COORDINATES[owner]["patterns"]):
        rank = int(pattern["rank"])
        if rank not in counts:
            continue
        groups = [prior._TYPE_ROWS[owner][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            counts[rank] += 1
            ids_ordered = tuple(TYPE_ID[row[0]] for row in rows)
            ids = tuple(sorted(ids_ordered))
            if rank == 2:
                pairs.add(ids)
                continue
            if sum(value in SMALL for value in ids) >= 2:
                small_rank3.add(ids)
            masks = tuple(TYPE_MASKS[value] for value in ids_ordered)
            for position, mask in enumerate(masks):
                if mask == 1 << owner:
                    induced.add(tuple(sorted(ids_ordered[index] for index in range(3) if index != position)))
    return {"owner": owner, "rank2_count": counts[2], "rank3_count": counts[3], "pairs": pairs, "induced": induced, "small_rank3": small_rank3}


def gf2_h1(owner_masks, deleted):
    supports = [[owner for owner in range(13) if mask & (1 << owner)] for mask in owner_masks]
    vertices = [(part, owner) for part in range(3) for owner in supports[part]]
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
    basis = {}
    for i, j, k in itertools.product(*supports):
        boundary = 0
        candidate = (((0, i), (1, j)), ((0, i), (2, k)), ((1, j), (2, k)))
        if not all(edge in edge_id for edge in candidate):
            continue
        for edge in candidate:
            boundary ^= 1 << edge_id[edge]
        while boundary:
            pivot = (boundary & -boundary).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = boundary
                break
            boundary ^= basis[pivot]
    return len(edges) - (len(vertices) - components) - len(basis)


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
        stack = [start]
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in reversed(adjacency[vertex]):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        result.append(tuple(sorted(component)))
    return result, adjacency


def transport(left, right, relation_deleted, marginals, masks):
    deleted = relation_deleted.get((left, right), 0)
    components, adjacency = relation_components(masks[left], masks[right], deleted)
    remaining = {owner: marginals[left].get(owner, Fraction(0)) for owner in range(13) if masks[left] & (1 << owner)}
    remaining.update({13 + owner: marginals[right].get(owner, Fraction(0)) for owner in range(13) if masks[right] & (1 << owner)})
    flow = defaultdict(Fraction)
    for component in components:
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
            flow[(edge[0], edge[1] - 13)] += value
            remaining[neighbor] -= value
            remaining[leaf] = 0
            active.remove(leaf)
        if remaining[next(iter(active))]:
            raise AssertionError("pair component balance")
    if left == right:
        keys = set(flow) | {(j, i) for i, j in flow}
        flow = defaultdict(Fraction, {key: (flow[key] + flow[(key[1], key[0])]) / 2 for key in keys if flow[key] + flow[(key[1], key[0])]})
    return flow


def exact_fill_control(triple, original, relation_deleted, marginals, masks, transport_masks):
    a, b, c = triple
    flows = [transport(a, b, relation_deleted, marginals, transport_masks), transport(a, c, relation_deleted, marginals, transport_masks), transport(b, c, relation_deleted, marginals, transport_masks)]
    supports = [[owner for owner in range(13) if masks[value] & (1 << owner)] for value in triple]
    deleted = [original.get((a, b), 0), original.get((a, c), 0), original.get((b, c), 0)]
    row_keys = []
    for pair_index, (x, y) in enumerate(((0, 1), (0, 2), (1, 2))):
        for i in supports[x]:
            for j in supports[y]:
                if not (i == j and deleted[pair_index] & (1 << i)):
                    row_keys.append((pair_index, i, j))
    row_id = {key: index for index, key in enumerate(row_keys)}
    equations = [dict() for _ in row_keys]
    variable_count = 0
    for i, j, k in itertools.product(*supports):
        if (i == j and deleted[0] & (1 << i)) or (i == k and deleted[1] & (1 << i)) or (j == k and deleted[2] & (1 << j)):
            continue
        for key in ((0, i, j), (1, i, k), (2, j, k)):
            equations[row_id[key]][variable_count] = Fraction(1)
        variable_count += 1
    rhs = [flows[pair_index].get((i, j), Fraction(0)) for pair_index, i, j in row_keys]
    basis = {}
    for coefficients, target in reversed(list(zip(equations, rhs))):
        row = dict(coefficients)
        value = target
        while row:
            pivot = max(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = ({index: coefficient / scale for index, coefficient in row.items()}, value / scale)
                break
            base_row, base_value = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base_row.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            value -= factor * base_value
        else:
            if value:
                return False
    return True


def main():
    global TYPE_ID, TYPE_MASKS, SMALL
    started = time.monotonic()
    prior.prepare()
    types = sorted({row[0] for root in prior._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(types)}
    TYPE_MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in types]
    SMALL = {index for index, mask in enumerate(TYPE_MASKS) if mask.bit_count() <= 6}
    raw = []
    for point in range(prior._COVERAGE.shape[0]):
        value = tuple(sum(1 << offset for offset, digit in enumerate(prior._ALLOWED[coordinate_index]) if prior._COVERAGE[point, coordinate_index, digit]) for coordinate_index in range(13))
        raw.append(TYPE_ID[value])
    multiplicities = Counter(raw)
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(coordinate, reversed(range(13)), chunksize=1)
    original = defaultdict(int)
    induced = defaultdict(int)
    small_rank3 = set()
    for row in rows:
        owner = row["owner"]
        for pair in row["pairs"]:
            original[pair] |= 1 << owner
        for pair in row["induced"]:
            induced[pair] |= 1 << owner
        small_rank3.update(row["small_rank3"])
    if sum(row["rank2_count"] for row in rows) != 6_684_938 or sum(row["rank3_count"] for row in rows) != 19_661_454 or small_rank3:
        raise AssertionError("raw blocker census")

    zero = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values} for values in zero["singleton_marginals_by_complete_type"]]
    binary = {index for index, mask in enumerate(TYPE_MASKS) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for (left, right), owner_mask in original.items():
        for owner in range(13):
            if owner_mask & (1 << owner):
                if left in binary:
                    blocked[(left, owner)].append(right)
                if right in binary:
                    blocked[(right, owner)].append(left)
    transport_masks = list(TYPE_MASKS)
    owner_deletions = 0
    for mediator in binary:
        owners = [owner for owner in range(13) if TYPE_MASKS[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]:
                if transport_masks[neighbor] & (1 << owners[0]):
                    transport_masks[neighbor] &= ~(1 << owners[0])
                    owner_deletions += 1
    relation_deleted = defaultdict(int)
    for pair in set(original) | set(induced):
        for owner in range(13):
            if (original.get(pair, 0) | induced.get(pair, 0)) & (1 << owner):
                relation_deleted[pair] |= 1 << (13 * owner + owner)
    offdiag_pairs = set()
    for mediator in binary:
        owners = [owner for owner in range(13) if TYPE_MASKS[mediator] & (1 << owner)]
        if len(owners) != 2:
            continue
        x, y = owners
        for left in blocked[(mediator, x)]:
            for right in blocked[(mediator, y)]:
                if left <= right:
                    pair, bit = (left, right), 1 << (13 * x + y)
                    if left == right:
                        bit |= 1 << (13 * y + x)
                else:
                    pair, bit = (right, left), 1 << (13 * y + x)
                relation_deleted[pair] |= bit
                offdiag_pairs.add(pair)
    if owner_deletions != 52 or len(offdiag_pairs) != 1811:
        raise AssertionError("forced-zero closure census")
    for type_index, values in enumerate(marginals):
        if sum(values.values(), Fraction(0)) != 1 or any(not transport_masks[type_index] & (1 << owner) for owner in values):
            raise AssertionError("candidate singleton")
    disconnected = 0
    for pair in set(original) | set(induced) | set(offdiag_pairs):
        components, _adjacency = relation_components(transport_masks[pair[0]], transport_masks[pair[1]], relation_deleted[pair])
        if len(components) > 1:
            disconnected += 1
        for component in components:
            left_mass = sum(marginals[pair[0]].get(vertex, 0) for vertex in component if vertex < 13)
            right_mass = sum(marginals[pair[1]].get(vertex - 13, 0) for vertex in component if vertex >= 13)
            if left_mass != right_mass:
                raise AssertionError("candidate component balance")
    if disconnected != 58:
        raise AssertionError("disconnected pair census")

    small_types = sorted(SMALL)
    interface_cache = {}
    triples = nonzero = 0
    controls = []
    targets = {0, 34963, 69926}
    for small_index, left in enumerate(small_types):
        for right in small_types[small_index:]:
            for third in range(len(types)):
                triple = tuple(sorted((left, right, third)))
                values = [value for value in triple if value in SMALL]
                if tuple(values[:2]) != (left, right):
                    continue
                if any(multiplicities[value] < count for value, count in Counter(triple).items()):
                    continue
                a, b, c = triple
                deleted = (original.get((a, b), 0), original.get((a, c), 0), original.get((b, c), 0))
                key = (TYPE_MASKS[a], TYPE_MASKS[b], TYPE_MASKS[c], *deleted)
                h1 = interface_cache.get(key)
                if h1 is None:
                    h1 = gf2_h1(key[:3], deleted)
                    interface_cache[key] = h1
                triples += 1
                if h1:
                    if nonzero in targets:
                        if not exact_fill_control(triple, original, relation_deleted, marginals, TYPE_MASKS, transport_masks):
                            raise AssertionError("exact filling control")
                        controls.append({"nonzero_ordinal": nonzero, "types": list(triple), "h1": h1})
                    nonzero += 1
    if (triples, len(interface_cache), sum(bool(value) for value in interface_cache.values()), nonzero) != (11_279_048, 352_495, 7_892, 69_927):
        raise AssertionError("small boundary census")
    payload = {"status": "PASS", "epistemic_status": "PROVED", "rank_two_type_tuples": 6_684_938, "rank_three_type_tuples": 19_661_454, "small_rank_three_type_classes": 0, "owner_deletions": owner_deletions, "offdiagonal_zero_pair_classes": len(offdiag_pairs), "disconnected_pair_classes": disconnected, "small_type_triples": triples, "small_interfaces": len(interface_cache), "nonzero_h1_interfaces": 7_892, "nonzero_h1_type_triples": nonzero, "exact_reversed_pivot_controls": controls, "dense_support_minimum_large_size": 9, "dense_pair_intersection_minimum_side": 7, "dense_triple_intersection_minimum_side": 6, "wall_seconds": time.monotonic() - started}
    temporary = OUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT)
    print(json.dumps({key: payload[key] for key in ("status", "small_type_triples", "small_interfaces", "nonzero_h1_interfaces", "nonzero_h1_type_triples", "exact_reversed_pivot_controls", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
