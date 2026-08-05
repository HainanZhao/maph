#!/usr/bin/env python3
"""Cycle 47 outcome-blind overlap-dense connected patch selector."""
from __future__ import annotations

from collections import Counter, defaultdict, deque
import hashlib
import itertools
import json
from pathlib import Path
import time

import lrc_ownership_functional as c38

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle47-affine-descent"
SEED = "cycle47-affine-descent-v1"
TYPE_COUNT = 1318
TARGET = 256


def digest(label: str) -> bytes:
    return hashlib.sha256(label.encode("ascii")).digest()


def faces(types: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(types[index] for index in range(4) if index != omitted) for omitted in range(4))


def old_interfaces() -> set[tuple[int, ...]]:
    result = set()
    for path in (
        ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json",
        ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json",
    ):
        data = json.loads(path.read_text())
        result.update(tuple(sorted(row["types"])) for row in data["interface_records"])
    return result


def type_multiplicities() -> tuple[list[int], Counter]:
    c38.prepare()
    complete = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    assert len(complete) == TYPE_COUNT
    type_id = {value: index for index, value in enumerate(complete)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    raw = []
    for point in range(c38._COVERAGE.shape[0]):
        value = tuple(
            sum(1 << offset for offset, digit in enumerate(c38._ALLOWED[coordinate]) if c38._COVERAGE[point, coordinate, digit])
            for coordinate in range(13)
        )
        raw.append(type_id[value])
    return masks, Counter(raw)


def valid(types: tuple[int, ...], multiplicities: Counter, old: set[tuple[int, ...]]) -> bool:
    return types not in old and all(count <= multiplicities[value] for value, count in Counter(types).items())


def select_patch(multiplicities: Counter, old: set[tuple[int, ...]]):
    seeds = set()
    for counter in range(200_000):
        raw = digest(f"{SEED}:seed:{counter}")
        types = tuple(sorted(int.from_bytes(raw[2 * index:2 * index + 2], "big") % TYPE_COUNT for index in range(4)))
        if valid(types, multiplicities, old):
            seeds.add(types)
    if not seeds:
        raise RuntimeError("empty seed pool")
    seed = min(seeds, key=lambda types: (digest(f"{SEED}:choose:{','.join(map(str, types))}"), types))
    selected = [seed]
    selected_set = {seed}
    selected_faces = set(faces(seed))
    frontier = set()

    def add_neighbors(parent):
        joined = ",".join(map(str, parent))
        for position in range(4):
            for k in range(64):
                raw = digest(f"{SEED}:neighbor:{joined}:{position}:{k}")
                replacement = int.from_bytes(raw[:2], "big") % TYPE_COUNT
                values = list(parent)
                values[position] = replacement
                candidate = tuple(sorted(values))
                if candidate not in selected_set and valid(candidate, multiplicities, old):
                    frontier.add(candidate)

    add_neighbors(seed)
    records = [{"types": list(seed), "shared_faces_at_selection": 0, "parent": None}]
    while len(selected) < TARGET:
        eligible = []
        for candidate in frontier:
            score = sum(face in selected_faces for face in faces(candidate))
            if score:
                key = digest(f"{SEED}:frontier:{','.join(map(str, candidate))}")
                eligible.append((-score, key, candidate))
        if not eligible:
            raise RuntimeError("frontier exhausted")
        negative_score, _key, chosen = min(eligible)
        shared = [face for face in faces(chosen) if face in selected_faces]
        parent = min((row for row in selected if set(faces(row)) & set(shared)), default=None)
        frontier.remove(chosen)
        selected.append(chosen)
        selected_set.add(chosen)
        selected_faces.update(faces(chosen))
        records.append({"types": list(chosen), "shared_faces_at_selection": -negative_score, "parent": list(parent) if parent else None})
        add_neighbors(chosen)
    return records, len(seeds)


def incidence(records):
    quadruples = [tuple(row["types"]) for row in records]
    face_to_quadruples = defaultdict(list)
    for ordinal, types in enumerate(quadruples):
        for face in set(faces(types)):
            face_to_quadruples[face].append(ordinal)
    adjacency = defaultdict(set)
    for ordinals in face_to_quadruples.values():
        for left, right in itertools.combinations(ordinals, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = set()
    components = 0
    for start in range(len(quadruples)):
        if start in seen:
            continue
        components += 1
        queue = deque([start])
        seen.add(start)
        while queue:
            for nxt in adjacency[queue.popleft()]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    edge_count = sum(len(set(faces(types))) for types in quadruples)
    vertices = len(quadruples) + len(face_to_quadruples)
    return {
        "components": components,
        "quadruple_vertices": len(quadruples),
        "face_vertices": len(face_to_quadruples),
        "incidence_edges": edge_count,
        "cycle_rank": edge_count - vertices + components,
        "repeated_faces": sum(len(rows) > 1 for rows in face_to_quadruples.values()),
        "maximum_face_degree": max(map(len, face_to_quadruples.values())),
        "face_degree_counts": dict(sorted(Counter(map(len, face_to_quadruples.values())).items())),
    }


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    masks, multiplicities = type_multiplicities()
    old = old_interfaces()
    records, seed_candidates = select_patch(multiplicities, old)
    diagnostics = incidence(records)
    if diagnostics["components"] != 1 or diagnostics["cycle_rank"] <= 0:
        raise RuntimeError("selection incidence gate failed")
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage": "OUTCOME_BLIND_AFFINE_DESCENT_PATCH_SELECTION",
        "seed_candidates": seed_candidates,
        "old_interfaces": len(old),
        "selected_quadruples": len(records),
        "type_count": len(masks),
        "support_size_counts": dict(sorted(Counter(mask.bit_count() for mask in masks).items())),
        "incidence": diagnostics,
        "selected": records,
        "claim_boundary": "Deterministic structural selection only; no face, local-fill, or global affine outcome was inspected.",
        "wall_seconds": time.monotonic() - started,
    }
    target = OUT / "selection.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(target)
    print(json.dumps({key: result[key] for key in ("status", "seed_candidates", "old_interfaces", "selected_quadruples", "incidence", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
