#!/usr/bin/env python3
"""Independent selection and cone/acyclic replay for Cycle 44."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38

OUT = ROOT / "discovery/out/cycle44-nonanchor-coupling"
SEED = "cycle44-nonanchor-v1"
ANCHORS = {(2, 5, 14), (14, 68, 71), (80, 1306, 1307)}

MASKS = []
TYPE_ID = {}
TARGET_FACES = set()
ORIGINAL = {}
RANK3 = {}


def digest(value):
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def low_pivot_rank(columns):
    basis = {}
    for value in reversed(columns):
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def rank2_owner(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    found = set()
    raw = 0
    for pattern in reversed(c38._COORDINATES[owner]["patterns"]):
        if int(pattern["rank"]) != 2:
            continue
        groups = [tuple(reversed(c38._TYPE_ROWS[owner][int(signature)])) for signature in reversed(pattern["signatures"])]
        for rows in itertools.product(*groups):
            raw += 1
            found.add(tuple(sorted(TYPE_ID[row[0]] for row in rows)))
    return owner, raw, tuple(sorted(found, reverse=True))


def rank3_owner(owner):
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    found = set()
    raw = 0
    for pattern in reversed(c38._COORDINATES[owner]["patterns"]):
        if int(pattern["rank"]) != 3:
            continue
        groups = [tuple(reversed(c38._TYPE_ROWS[owner][int(signature)])) for signature in reversed(pattern["signatures"])]
        for rows in itertools.product(*groups):
            raw += 1
            triple = tuple(sorted(TYPE_ID[row[0]] for row in rows))
            if triple in TARGET_FACES:
                found.add(triple)
    return owner, raw, tuple(sorted(found, reverse=True))


def complex_data(types):
    supports = [tuple(owner for owner in range(12, -1, -1) if MASKS[value] & (1 << owner)) for value in types]
    edges = []
    for left, right in reversed(tuple(itertools.combinations(range(4), 2))):
        deleted = ORIGINAL.get(tuple(sorted((types[left], types[right]))), 0)
        for a in supports[left]:
            for b in supports[right]:
                if a != b or not deleted & (1 << a):
                    edges.append(((left, a), (right, b)))
    edge_id = {edge: index for index, edge in enumerate(edges)}
    triangles = []
    d2 = []
    for parts in reversed(tuple(itertools.combinations(range(4), 3))):
        deleted3 = RANK3.get(tuple(sorted(types[part] for part in parts)), 0)
        for owners in itertools.product(*(supports[part] for part in parts)):
            if owners[0] == owners[1] == owners[2] and deleted3 & (1 << owners[0]):
                continue
            vertices = tuple(zip(parts, owners))
            boundary = tuple((vertices[x], vertices[y]) for x, y in itertools.combinations(range(3), 2))
            if not all(edge in edge_id for edge in boundary):
                continue
            triangles.append(vertices)
            value = 0
            for edge in boundary:
                value ^= 1 << edge_id[edge]
            d2.append(value)
    triangle_id = {triangle: index for index, triangle in enumerate(triangles)}
    d3 = []
    tetrahedra = 0
    for owners in itertools.product(*supports):
        faces = [tuple((part, owners[part]) for part in range(4) if part != omitted) for omitted in range(4)]
        if all(face in triangle_id for face in faces):
            tetrahedra += 1
            value = 0
            for face in faces:
                value ^= 1 << triangle_id[face]
            d3.append(value)
    h2 = len(triangles) - low_pivot_rank(d2) - low_pivot_rank(d3)
    if h2 < 0:
        raise AssertionError("negative independent H2")
    return h2, (sum(map(len, supports)), len(edges), len(triangles), tetrahedra)


def h2_worker(types):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    h2, census = complex_data(types)
    return tuple(types), h2, census


def allowed_tetrahedron(types, owners):
    for left, right in itertools.combinations(range(4), 2):
        if owners[left] == owners[right] and ORIGINAL.get(tuple(sorted((types[left], types[right]))), 0) & (1 << owners[left]):
            return False
    for parts in itertools.combinations(range(4), 3):
        face_owners = tuple(owners[part] for part in parts)
        if len(set(face_owners)) == 1 and RANK3.get(tuple(sorted(types[part] for part in parts)), 0) & (1 << face_owners[0]):
            return False
    return True


def fill_boundary(fill):
    result = defaultdict(Fraction)
    for owners, coefficient in fill.items():
        for omitted in reversed(range(4)):
            parts = tuple(part for part in range(4) if part != omitted)
            result[(parts, tuple(owners[part] for part in parts))] += Fraction((-1) ** omitted) * coefficient
    return {key: value for key, value in result.items() if value}


def cycle_boundary(cycle):
    result = defaultdict(Fraction)
    for (parts, owners), coefficient in cycle.items():
        for omitted in reversed(range(3)):
            edge_parts = tuple(parts[index] for index in range(3) if index != omitted)
            edge_owners = tuple(owners[index] for index in range(3) if index != omitted)
            result[(edge_parts, edge_owners)] += Fraction((-1) ** omitted) * coefficient
    return {key: value for key, value in result.items() if value}


def main():
    global MASKS, TYPE_ID, TARGET_FACES, ORIGINAL, RANK3
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for owner_rows in c38._TYPE_ROWS for rows in owner_rows.values() for row in rows})
    TYPE_ID = {value: index for index, value in enumerate(complete_types)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    raw_types = []
    for point in reversed(range(c38._COVERAGE.shape[0])):
        value = tuple(sum(1 << offset for offset, digit in enumerate(c38._ALLOWED[coordinate]) if c38._COVERAGE[point, coordinate, digit]) for coordinate in range(13))
        raw_types.append(TYPE_ID[value])
    multiplicities = Counter(raw_types)
    with multiprocessing.Pool(3) as pool:
        rank2_rows = pool.map(rank2_owner, reversed(range(13)), chunksize=1)
    if sum(row[1] for row in rank2_rows) != 6_684_938:
        raise AssertionError("independent rank-two census")
    original = defaultdict(int)
    for owner, _raw, pairs in reversed(rank2_rows):
        for pair in pairs:
            original[pair] |= 1 << owner
    ORIGINAL = dict(original)

    def valid(types):
        if any(count > multiplicities[value] for value, count in Counter(types).items()):
            return False
        return all(tuple(sorted(types[index] for index in positions)) not in ANCHORS for positions in itertools.combinations(range(4), 3))

    candidates = {}
    for counter in reversed(range(100_000)):
        raw = hashlib.sha256(f"{SEED}:{counter}".encode("ascii")).digest()
        types = tuple(sorted(int.from_bytes(raw[2 * index:2 * index + 2], "big") % 1318 for index in range(4)))
        if valid(types):
            source = f"hash:{counter:06d}"
            if types not in candidates or source < candidates[types]:
                candidates[types] = source
    for t in reversed(range(1318)):
        families = (
            ("distinct", tuple(sorted((t, (t + 1) % 1318, (t + 17) % 1318, (t + 257) % 1318)))),
            ("two-pair", tuple(sorted((t, t, (t + 659) % 1318, (t + 659) % 1318)))),
            ("pair", tuple(sorted((t, t, (t + 1) % 1318, (t + 659) % 1318)))),
        )
        for family, types in families:
            if valid(types):
                source = f"constructed:{family}:{t:04d}"
                if types not in candidates or source < candidates[types]:
                    candidates[types] = source

    rows = {}
    strata = defaultdict(list)
    for types, source in reversed(tuple(candidates.items())):
        profile = tuple(sorted(MASKS[value].bit_count() for value in types))
        repeats = tuple(sorted(Counter(types).values(), reverse=True))
        pair_masks = [ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)]
        product = 1
        for value in types:
            product *= MASKS[value].bit_count()
        density = 0 if product <= 256 else 1 if product <= 2048 else 2 if product <= 8192 else 3
        selection_hash = digest(f"{SEED}:select:{','.join(map(str, types))}")
        descriptor = (profile, repeats, sum(bool(mask) for mask in pair_masks), sum(mask.bit_count() for mask in pair_masks), density)
        row = {"types": list(types), "source": source, "selection_hash": selection_hash, "support_profile": list(profile), "repeat_partition": list(repeats), "nonzero_deleted_pairs": descriptor[2], "deleted_owner_total": descriptor[3], "density_bin": density}
        rows[types] = row
        strata[descriptor].append((selection_hash, types))
    preliminary_types = set()
    for values in reversed(tuple(strata.values())):
        preliminary_types.update(types for _hash, types in sorted(values, reverse=True)[-4:])
    if len(preliminary_types) > 10_000:
        reserves = set()
        for getter in (lambda t: tuple(rows[t]["repeat_partition"]), lambda t: rows[t]["density_bin"]):
            groups = defaultdict(list)
            for types in preliminary_types:
                groups[getter(types)].append(types)
            for values in groups.values():
                reserves.add(min(values, key=lambda value: (rows[value]["selection_hash"], value)))
        remainder = sorted(preliminary_types - reserves, key=lambda value: (rows[value]["selection_hash"], value))
        preliminary_types = reserves | set(remainder[:10_000 - len(reserves)])
    preliminary = sorted(preliminary_types, key=lambda value: (rows[value]["selection_hash"], value))
    TARGET_FACES = {tuple(sorted(types[part] for part in parts)) for types in preliminary for parts in itertools.combinations(range(4), 3)}
    with multiprocessing.Pool(3) as pool:
        rank3_rows = pool.map(rank3_owner, reversed(range(13)), chunksize=1)
    if sum(row[1] for row in rank3_rows) != 19_661_454:
        raise AssertionError("independent rank-three census")
    rank3 = defaultdict(int)
    for owner, _raw, triples in reversed(rank3_rows):
        for triple in triples:
            rank3[triple] |= 1 << owner
    RANK3 = dict(rank3)

    structural = {}
    members = defaultdict(list)
    for types in reversed(preliminary):
        key = (tuple(MASKS[value] for value in types), tuple(ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)), tuple(RANK3.get(tuple(sorted(types[part] for part in parts)), 0) for parts in itertools.combinations(range(4), 3)))
        structural.setdefault(key, types)
        members[key].append(types)
    with multiprocessing.Pool(3) as pool:
        h2_rows = pool.map(h2_worker, list(reversed(tuple(structural.values()))), chunksize=1)
    h2_by_types = {types: h2 for types, h2, _census in h2_rows}
    for key, values in members.items():
        h2 = h2_by_types[structural[key]]
        h2_bin = 0 if h2 == 0 else 1 if h2 <= 3 else 2 if h2 <= 15 else 3
        for types in values:
            rows[types]["h2_gf2"] = h2
            rows[types]["h2_bin"] = h2_bin
    refined = defaultdict(list)
    for types in reversed(preliminary):
        row = rows[types]
        descriptor = (tuple(row["support_profile"]), tuple(row["repeat_partition"]), row["nonzero_deleted_pairs"], row["deleted_owner_total"], row["density_bin"], row["h2_bin"])
        refined[descriptor].append((row["selection_hash"], types))
    selected_types = set()
    for values in reversed(tuple(refined.values())):
        selected_types.update(types for _hash, types in sorted(values, reverse=True)[-2:])
    if len(selected_types) > 2000:
        reserves = set()
        for getter in (lambda t: rows[t]["h2_bin"], lambda t: rows[t]["density_bin"], lambda t: tuple(rows[t]["repeat_partition"])):
            groups = defaultdict(list)
            for types in selected_types:
                groups[getter(types)].append(types)
            for values in groups.values():
                reserves.add(min(values, key=lambda value: (rows[value]["selection_hash"], value)))
        remainder = sorted(selected_types - reserves, key=lambda value: (rows[value]["selection_hash"], value))
        selected_types = reserves | set(remainder[:2000 - len(reserves)])
    independent_selected = [rows[types] for types in sorted(selected_types, key=lambda value: (rows[value]["selection_hash"], value))]

    selection = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
    if independent_selected != selection["selected"]:
        raise AssertionError("independent selected-list mismatch")
    expected_counts = (len(candidates), len(strata), len(preliminary), len(structural), len(TARGET_FACES), len(RANK3), len(refined), len(independent_selected))
    recorded_counts = tuple(selection[key] for key in ("deduplicated_candidate_pool", "preselection_strata", "preliminary_interfaces", "preliminary_structural_complexes", "target_face_classes", "rank_three_target_classes", "refined_strata", "selected_interfaces"))
    if expected_counts != recorded_counts:
        raise AssertionError("independent selection census")

    coupling = json.loads((OUT / "coupling.json").read_text(encoding="utf-8"))
    face_tensors = {}
    pair_flows = {}
    face_coefficients = 0
    for row in reversed(coupling["face_tensors"]):
        triple = tuple(row["triple"])
        coefficients = {tuple(owners): Fraction(numerator, denominator) for owners, numerator, denominator in row["coefficients"]}
        if triple != tuple(sorted(triple)) or triple in face_tensors:
            raise AssertionError("independent face identity")
        face_coefficients += len(coefficients)
        supports = [MASKS[value] for value in triple]
        for owners in coefficients:
            if any(not supports[index] & (1 << owner) for index, owner in enumerate(owners)):
                raise AssertionError("face rank-one support")
            if any(owners[a] == owners[b] and ORIGINAL.get(tuple(sorted((triple[a], triple[b]))), 0) & (1 << owners[a]) for a, b in itertools.combinations(range(3), 2)):
                raise AssertionError("face rank-two support")
            if len(set(owners)) == 1 and RANK3.get(triple, 0) & (1 << owners[0]):
                raise AssertionError("face rank-three support")
        stabilizer = [permutation for permutation in itertools.permutations(range(3)) if tuple(triple[permutation[index]] for index in range(3)) == triple]
        for owners, value in coefficients.items():
            if any(coefficients.get(tuple(owners[permutation[index]] for index in range(3)), 0) != value for permutation in stabilizer):
                raise AssertionError("face stabilizer")
        for a, b in itertools.combinations(range(3), 2):
            observed = defaultdict(Fraction)
            for owners, value in coefficients.items():
                observed[(owners[a], owners[b])] += value
            observed = {key: value for key, value in observed.items() if value}
            pair = (triple[a], triple[b])
            if pair in pair_flows and pair_flows[pair] != observed:
                raise AssertionError("shared pair flow")
            pair_flows[pair] = observed
        face_tensors[triple] = coefficients
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(numerator, denominator) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    for (left, right), flow in pair_flows.items():
        for owner in range(13):
            if sum(value for (a, _b), value in flow.items() if a == owner) != marginals[left].get(owner, 0):
                raise AssertionError("left singleton marginal")
            if sum(value for (_a, b), value in flow.items() if b == owner) != marginals[right].get(owner, 0):
                raise AssertionError("right singleton marginal")

    selected = [tuple(row["types"]) for row in independent_selected]
    if [tuple(row["types"]) for row in coupling["interface_records"]] != selected:
        raise AssertionError("coupling interface order")
    cone_count = acyclic_count = total_cycle = total_fill = 0
    h2_cache = {}
    controls = []
    control_ordinals = {0, len(selected) // 2, len(selected) - 1}
    for ordinal, (selection_row, record) in enumerate(zip(independent_selected, coupling["interface_records"])):
        types = tuple(selection_row["types"])
        expected_cycle = defaultdict(Fraction)
        for omitted in reversed(range(4)):
            parts = tuple(part for part in range(4) if part != omitted)
            ordered_types = tuple(types[part] for part in parts)
            sorted_types = tuple(sorted(ordered_types))
            permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
            for owners, value in face_tensors[sorted_types].items():
                ordered_owners = tuple(owners[permutation[index]] for index in range(3))
                expected_cycle[(parts, ordered_owners)] += Fraction((-1) ** omitted) * value
        expected_cycle = {key: value for key, value in expected_cycle.items() if value}
        recorded_cycle = {(tuple(parts), tuple(owners)): Fraction(numerator, denominator) for (parts, owners), numerator, denominator in record["cycle"]}
        if expected_cycle != recorded_cycle or cycle_boundary(recorded_cycle):
            raise AssertionError("independent cycle reconstruction")
        total_cycle += len(recorded_cycle)
        key = (tuple(MASKS[value] for value in types), tuple(ORIGINAL.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)), tuple(RANK3.get(tuple(sorted(types[part] for part in parts)), 0) for parts in itertools.combinations(range(4), 3)))
        if key not in h2_cache:
            h2_cache[key] = complex_data(types)[0]
        if h2_cache[key] != selection_row["h2_gf2"] or record["h2_gf2"] != selection_row["h2_gf2"]:
            raise AssertionError("selected H2 replay")
        if record["route"] == "EXPLICIT_CONE":
            cone_count += 1
            part = int(record["cone_part"])
            owner = int(record["cone_owner"])
            if marginals[types[part]] != {owner: Fraction(1)}:
                raise AssertionError("cone vertex marginal")
            fill = {tuple(owners): Fraction(numerator, denominator) for owners, numerator, denominator in record["fill"]}
            if any(not allowed_tetrahedron(types, owners) for owners in fill) or fill_boundary(fill) != recorded_cycle:
                raise AssertionError("explicit cone identity")
            opposite = tuple(index for index in range(4) if index != part)
            for owners, coefficient in fill.items():
                face_owners = tuple(owners[index] for index in opposite)
                ordered_types = tuple(types[index] for index in opposite)
                sorted_types = tuple(sorted(ordered_types))
                permutation = next(permutation for permutation in itertools.permutations(range(3)) if tuple(sorted_types[permutation[index]] for index in range(3)) == ordered_types)
                canonical_owner = tuple(face_owners[permutation.index(index)] for index in range(3))
                if face_tensors[sorted_types].get(canonical_owner, 0) != coefficient:
                    raise AssertionError("cone is not the opposite canonical face")
            total_fill += len(fill)
        elif record["route"] == "GF2_H2_ZERO_EXISTENCE":
            acyclic_count += 1
            if record["status"] != "FILLED_EXISTENCE" or record["fill"] or h2_cache[key] != 0:
                raise AssertionError("invalid H2-zero existence route")
        else:
            raise AssertionError("unexpected fill route")
        if ordinal in control_ordinals:
            controls.append({"ordinal": ordinal, "types": list(types), "h2_gf2": h2_cache[key], "route": record["route"], "cycle_nonzero": len(recorded_cycle), "fill_nonzero": len(record["fill"])})
    if any(row["h2_gf2"] and row["route"] != "EXPLICIT_CONE" for row in coupling["interface_records"]):
        raise AssertionError("nonzero-H2 interface without explicit cone")
    expected_summary = (len(face_tensors), len(pair_flows), face_coefficients, len(selected), cone_count, acyclic_count)
    recorded_summary = (coupling["face_classes"], coupling["pair_classes"], coupling["face_coefficients"], coupling["canonical_fills"], coupling["cone_explained"], coupling["h2_zero_existence_fills"])
    if expected_summary != recorded_summary or coupling["canonical_failures"] != 0:
        raise AssertionError("coupling census mismatch")
    payload = {"status": "PASS", "epistemic_status": "PROVED", "selection_replayed": True, "candidate_pool": len(candidates), "preliminary_interfaces": len(preliminary), "selected_interfaces": len(selected), "selected_structural_complexes": len(h2_cache), "face_classes": len(face_tensors), "pair_classes": len(pair_flows), "face_coefficients_checked": face_coefficients, "cycle_coefficients_checked": total_cycle, "cone_coefficients_checked": total_fill, "cone_explained": cone_count, "h2_zero_existence_fills": acyclic_count, "nonzero_h2_without_cone": 0, "controls": controls, "wall_seconds": time.monotonic() - started}
    temporary = OUT / "independent-replay.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "independent-replay.json")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
