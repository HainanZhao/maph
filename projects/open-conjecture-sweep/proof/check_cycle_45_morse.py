#!/usr/bin/env python3
"""Cross-record and exact certificate audit for Cycle 45."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_morse_critical_projection import boundary, build_complex, lexicographic_matching, verify_basis_identity

OUT = ROOT / "discovery/out/cycle45-critical-projection"


def parse_chain(values):
    return {tuple((int(part), int(owner)) for part, owner in cell): Fraction(int(numerator), int(denominator)) for cell, numerator, denominator in values}


def check_dual(row):
    descriptor = row["descriptor"]
    supports = tuple(tuple(values) for values in descriptor["supports"])
    pairs = {pair: value for pair, value in zip(itertools.combinations(range(4), 2), descriptor["pair_deleted"])}
    triples = {parts: value for parts, value in zip(itertools.combinations(range(4), 3), descriptor["triple_deleted"])}
    cells, _all_cells = build_complex(supports, pairs, triples)
    projection = parse_chain(row["projection"])
    dual = parse_chain(row["projection_dual"])
    for tetrahedron in cells[3]:
        if sum(dual.get(face, 0) * incidence for face, incidence in boundary({tetrahedron: Fraction(1)}).items()):
            raise AssertionError("dual does not annihilate tetrahedral boundary")
    pairing = sum(dual.get(face, 0) * value for face, value in projection.items())
    assert [pairing.numerator, pairing.denominator] == row["projection_pairing"]
    assert pairing
    extended = parse_chain(row["extended_projection"])
    extended_dual = parse_chain(row["extended_projection_dual"])
    for tetrahedron in cells[3]:
        assert not sum(extended_dual.get(face, 0) * incidence for face, incidence in boundary({tetrahedron: Fraction(1)}).items())
    extended_pairing = sum(extended_dual.get(face, 0) * value for face, value in extended.items())
    assert [extended_pairing.numerator, extended_pairing.denominator] == row["extended_projection_pairing"]
    assert extended_pairing
    return {"counter": row["counter"], "cells": row["cells"], "projection_nonzero": row["projection_nonzero"], "pairing": row["projection_pairing"]}


def deterministic_controls():
    passed = 0
    for counter in range(200):
        raw = hashlib.sha256(f"cycle45-control:{counter}".encode("ascii")).digest()
        distinguished = tuple(raw[part] & 1 for part in range(4))
        supports = tuple(tuple(owner for owner in range(2) if ((1 << distinguished[part]) | (raw[4 + part] & 3)) & (1 << owner)) for part in range(4))
        pairs = {}
        for index, pair in enumerate(itertools.combinations(range(4), 2)):
            intersection = sum(1 << owner for owner in set(supports[pair[0]]) & set(supports[pair[1]]))
            value = (raw[8 + index] & 3) & intersection
            if distinguished[pair[0]] == distinguished[pair[1]]:
                value &= ~(1 << distinguished[pair[0]])
            pairs[pair] = value
        triples = {}
        for index, parts in enumerate(itertools.combinations(range(4), 3)):
            intersection = set(supports[parts[0]]) & set(supports[parts[1]]) & set(supports[parts[2]])
            triples[parts] = (raw[14 + index] & 3) & sum(1 << owner for owner in intersection)
        cells, all_cells = build_complex(supports, pairs, triples)
        matching = lexicographic_matching(cells, all_cells, distinguished)
        assert verify_basis_identity(cells, matching)["status"] == "PASS"
        passed += 1
    return passed


def raw_two_owner_descriptor_count():
    states = (((0,), 0), ((1,), 1), ((0, 1), 0), ((0, 1), 1))
    total = 0
    for parts in itertools.product(states, repeat=4):
        count = 1
        for left, right in itertools.combinations(range(4), 2):
            intersection = set(parts[left][0]) & set(parts[right][0])
            free = len(intersection) - int(parts[left][1] == parts[right][1] and parts[left][1] in intersection)
            count *= 1 << free
        for triple in itertools.combinations(range(4), 3):
            intersection = set(parts[triple[0]][0]) & set(parts[triple[1]][0]) & set(parts[triple[2]][0])
            count *= 1 << len(intersection)
        total += count
    return total


def audit():
    actual = json.loads((OUT / "actual-corpus-layered.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-actual-replay.json").read_text(encoding="utf-8"))
    abstract = json.loads((OUT / "abstract-models.json").read_text(encoding="utf-8"))
    signature = json.loads((OUT / "signature-abstract-models.json").read_text(encoding="utf-8"))
    c44 = json.loads((ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json").read_text(encoding="utf-8"))
    assert actual["status"] == replay["status"] == abstract["status"] == signature["status"] == "PASS"
    assert actual["actual_interfaces"] == replay["actual_interfaces"] == 5_954
    assert actual["aggregate_allowed_simplices"] == replay["aggregate_allowed_simplices"] == 30_212_057
    assert (actual["zero_projections"], actual["nonzero_projections"]) == (replay["initial_zero_projections"], replay["initial_nonzero_projections"]) == (5_484, 470)
    assert (actual["extended_zero_projections"], actual["extended_nonzero_projections"]) == (replay["extended_zero_projections"], replay["extended_nonzero_projections"]) == (5_497, 457)
    c43_records = [row for row in actual["records"] if row["source"] == "C43"]
    c44_records = [row for row in actual["records"] if row["source"] == "C44"]
    assert len(c43_records) == 3_954 and all(not row["projection_nonzero"] for row in c43_records)
    explicit = h2zero = h2zero_initial_zero = h2zero_extended_zero = 0
    for row in c44_records:
        prior = c44["interface_records"][row["ordinal"]]
        if prior["route"] == "EXPLICIT_CONE":
            explicit += 1
            assert row["projection_nonzero"] == row["extended_projection_nonzero"] == 0
        else:
            h2zero += 1
            assert prior["route"] == "GF2_H2_ZERO_EXISTENCE" and prior["h2_gf2"] == 0
            h2zero_initial_zero += not row["projection_nonzero"]
            h2zero_extended_zero += not row["extended_projection_nonzero"]
    assert (explicit, h2zero, h2zero_initial_zero, h2zero_extended_zero) == (1_528, 472, 2, 15)
    assert abstract["admissible_face_models"] == 41_641
    assert abstract["nonzero_projection_models"] == 3_083
    assert abstract["nonboundary_projection_models"] == abstract["extended_nonboundary_projection_models"] == 2_647
    assert abstract["rank3_free_nonboundary_projection_models"] == 96
    assert signature["admissible_face_models"] == 31_160
    assert signature["nonboundary_projection_models"] == signature["extended_nonboundary_projection_models"] == 649
    certificates = [check_dual(abstract["least_nonboundary_countermodel"]), check_dual(abstract["least_rank3_free_nonboundary_countermodel"]), check_dual(signature["least_nonboundary_countermodel"])]
    controls = deterministic_controls()
    raw_count = raw_two_owner_descriptor_count()
    assert controls == 200 and raw_count == 2_836_566 and raw_count > 2_000_000
    return {"status": "PASS", "actual_interfaces": 5_954, "initial_zero_projections": 5_484, "initial_nonzero_projections": 470, "extended_zero_projections": 5_497, "extended_nonzero_projections": 457, "arbitrary_nonboundary_models": 2_647, "signature_nonboundary_models": 649, "dual_certificates": certificates, "basis_controls": controls, "raw_two_owner_control_count": raw_count, "raw_control_status": "CAP"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
