#!/usr/bin/env python3
"""Independent exact replay of Cycle 40's signed moment construction."""
from __future__ import annotations

from collections import defaultdict, deque
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

SOURCE = ROOT / "discovery/out/cycle40-signed-moments/result.json"
OUTPUT = ROOT / "discovery/out/cycle40-signed-moments/independent-replay.json"
TYPE_ID = {}
TYPE_MASKS = []


def kernel_surjective(masks):
    common = masks[0] & masks[1] & masks[2]
    if not common:
        return True
    if min(mask.bit_count() for mask in masks) == 1:
        return False
    return not (common.bit_count() == 2 and masks[0] == masks[1] == masks[2] == common)


def enumerate_coordinate(coordinate):
    resource.setrlimit(resource.RLIMIT_AS, (1_258_291_200, 1_258_291_200))
    pairs = set()
    induced = set()
    triple_masks = set()
    binary = set()
    counts = {2: 0, 3: 0}
    for pattern in prior._COORDINATES[coordinate]["patterns"]:
        rank = int(pattern["rank"])
        if rank not in counts:
            continue
        groups = [prior._TYPE_ROWS[coordinate][int(signature)] for signature in pattern["signatures"]]
        for rows in itertools.product(*groups):
            counts[rank] += 1
            ids = tuple(TYPE_ID[row[0]] for row in rows)
            if rank == 2:
                pairs.add(tuple(sorted(ids)))
                continue
            masks = tuple(TYPE_MASKS[index] for index in ids)
            triple_masks.add(tuple(sorted(masks)))
            if not kernel_surjective(tuple(sorted(masks))):
                for index, mask in enumerate(masks):
                    if mask == 1 << coordinate:
                        induced.add(tuple(sorted(ids[position] for position in range(3) if position != index)))
                if masks[0] == masks[1] == masks[2] and masks[0].bit_count() == 2:
                    binary.add(tuple(sorted(ids)))
    return {"coordinate": coordinate, "rank2": counts[2], "rank3": counts[3], "pairs": pairs, "induced": induced, "triple_masks": triple_masks, "binary": binary}


def components(left_mask, right_mask, deleted):
    vertices = [i for i in range(13) if left_mask & (1 << i)] + [13 + j for j in range(13) if right_mask & (1 << j)]
    adjacency = {vertex: set() for vertex in vertices}
    for i in range(13):
        if not left_mask & (1 << i):
            continue
        for j in range(13):
            if right_mask & (1 << j) and not (i == j and deleted & (1 << i)):
                adjacency[i].add(13 + j)
                adjacency[13 + j].add(i)
    result = []
    unseen = set(vertices)
    while unseen:
        start = min(unseen)
        queue = [start]
        unseen.remove(start)
        component = []
        while queue:
            vertex = queue.pop()
            component.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        result.append(tuple(sorted(component)))
    return tuple(sorted(result)), adjacency


def transport(left, right, deleted, marginals, masks):
    component_rows, adjacency = components(masks[left], masks[right], deleted)
    flows = defaultdict(Fraction)
    remaining = {}
    for i in range(13):
        if masks[left] & (1 << i):
            remaining[i] = marginals[left].get(i, Fraction(0))
        if masks[right] & (1 << i):
            remaining[13 + i] = marginals[right].get(i, Fraction(0))
    for component in component_rows:
        if len(component) == 1:
            if remaining[component[0]]:
                raise AssertionError("isolated component balance")
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
        last = next(iter(active))
        if remaining[last]:
            raise AssertionError("tree terminal balance")
    for i in range(13):
        if sum(value for (row, _column), value in flows.items() if row == i) != marginals[left].get(i, Fraction(0)):
            raise AssertionError("transport row marginal")
        if sum(value for (_row, column), value in flows.items() if column == i) != marginals[right].get(i, Fraction(0)):
            raise AssertionError("transport column marginal")
        if deleted & (1 << i) and flows.get((i, i), 0):
            raise AssertionError("deleted diagonal flow")
    return len(flows)


def main():
    global TYPE_ID, TYPE_MASKS
    started = time.monotonic()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    prior.prepare()
    types = sorted({row[0] for root in prior._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(types)}
    TYPE_MASKS = [sum(1 << coordinate for coordinate, signature in enumerate(value) if signature) for value in types]
    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(enumerate_coordinate, range(13), chunksize=1)
    if sum(row["rank2"] for row in coordinate_rows) != 6_684_938 or sum(row["rank3"] for row in coordinate_rows) != 19_661_454:
        raise AssertionError("tuple census")
    deleted = defaultdict(int)
    induced = defaultdict(int)
    triple_masks = set()
    binary = set()
    for row in coordinate_rows:
        coordinate = row["coordinate"]
        for pair in row["pairs"]:
            deleted[pair] |= 1 << coordinate
        for pair in row["induced"]:
            induced[pair] |= 1 << coordinate
            deleted[pair] |= 1 << coordinate
        triple_masks.update(row["triple_masks"])
        binary.update(row["binary"])
    if len(deleted) != source["rank_two_pair_classes"] or len(induced) != source["triple_completion"]["induced_pair_deletion_classes"] or binary:
        raise AssertionError("pair/triple class census")

    marginals = []
    for type_id, rows in enumerate(source["singleton_marginals_by_complete_type"]):
        values = {int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in rows}
        if sum(values.values(), Fraction(0)) != 1 or any(not TYPE_MASKS[type_id] & (1 << owner) for owner in values):
            raise AssertionError("singleton marginal")
        marginals.append(values)

    disconnected = 0
    graph_classes = set()
    pair_rows = sorted(deleted.items())
    for (left, right), diagonal in pair_rows:
        component_rows, _adjacency = components(TYPE_MASKS[left], TYPE_MASKS[right], diagonal)
        graph_classes.add((TYPE_MASKS[left], TYPE_MASKS[right], diagonal, component_rows))
        if len(component_rows) > 1:
            disconnected += 1
        for component in component_rows:
            left_mass = sum(marginals[left].get(vertex, 0) for vertex in component if vertex < 13)
            right_mass = sum(marginals[right].get(vertex - 13, 0) for vertex in component if vertex >= 13)
            if left_mass != right_mass:
                raise AssertionError("component balance")
    if disconnected != source["disconnected_pair_classes"] or len(graph_classes) != source["deduplicated_graph_classes"]:
        raise AssertionError("component census")
    controls = []
    for index in sorted({0, len(pair_rows) // 2, len(pair_rows) - 1}):
        (left, right), diagonal = pair_rows[index]
        controls.append({"pair_index": index, "left_type": left, "right_type": right, "deleted_diagonal": diagonal, "nonzero_tree_flows": transport(left, right, diagonal, marginals, TYPE_MASKS)})

    failing = {values for values in triple_masks if not kernel_surjective(values)}
    unresolved = {values for values in failing if values[0] == values[1] == values[2] and values[0].bit_count() == 2}
    if len(triple_masks) != 693 or len(failing) != 36 or unresolved or len(binary):
        raise AssertionError("triple kernel classification")
    for row in coordinate_rows:
        coordinate = row["coordinate"]
        for pair in row["induced"]:
            if not deleted[pair] & (1 << coordinate):
                raise AssertionError("missing induced diagonal")

    replay = {"status": "PASS", "epistemic_status": "PROVED", "complete_types": len(types), "pair_classes": len(deleted), "disconnected_pair_classes": disconnected, "graph_classes": len(graph_classes), "induced_pair_deletion_classes": len(induced), "triple_mask_classes": len(triple_masks), "initial_nonsurjective_triple_classes": len(failing), "unresolved_triple_classes": 0, "binary_triple_type_classes": 0, "transport_controls": controls, "mass_one_signed_degree_three_moment_family_exists": True, "wall_seconds": time.monotonic() - started}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "pairs": len(deleted), "induced": len(induced), "triple_classes": len(triple_masks), "unresolved": 0, "wall_seconds": replay["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
