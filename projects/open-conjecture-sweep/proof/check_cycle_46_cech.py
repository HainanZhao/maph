#!/usr/bin/env python3
"""Audit Cycle 46's serialized owner-star Cech quotient result."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_morse_critical_projection import boundary
from lrc_cech_total import clean, total_chain_boundary

OUT = ROOT / "discovery/out/cycle46-global-cech-quotient"


def parse_simplicial(serialized):
    return {tuple(tuple(vertex) for vertex in cell): Fraction(numerator, denominator) for cell, numerator, denominator in serialized}


def parse_total(serialized):
    return {(tuple(indices), tuple(tuple(vertex) for vertex in cell)): Fraction(numerator, denominator) for indices, cell, numerator, denominator in serialized}


def audit():
    source = json.loads((ROOT / "discovery/out/cycle45-critical-projection/actual-corpus-layered.json").read_text())
    result = json.loads((OUT / "actual-quotient-localized.json").read_text())
    controls = json.loads((OUT / "generic-controls.json").read_text())
    cache = json.loads((OUT / "target-structure-cache.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    expected = sorted((row for row in source["records"] if row["extended_projection_nonzero"]), key=lambda row: (row["source"], row["ordinal"]))
    assert len(expected) == 457 and result["selected_residuals"] == 457
    assert [(row["source"], row["ordinal"]) for row in result["records"]] == [(row["source"], row["ordinal"]) for row in expected]
    assert controls["status"] == "PASS"
    assert controls["tetrahedron_controls"]["full_simplex"]["status"] == "BOUNDARY"
    assert controls["tetrahedron_controls"]["tetrahedron_boundary"]["status"] == "UNCOVERED"
    assert controls["covered_nonboundary"]["injected"]["status"] == "NONBOUNDARY"
    assert len(cache["masks"]) == len(cache["distinguished"]) == 1318
    assert independent["status"] == "PASS" and independent["selected_records"] == 6 and independent["selection_classes"] == 3

    outcomes = Counter()
    pivots = Counter()
    witness_sizes = Counter()
    maximum_bits = 1
    for source_row, row in zip(expected, result["records"], strict=True):
        outcomes[row["status"]] += 1
        assert row["status"] == row["direct_status"] == row["total"]["status"]
        cycle = parse_simplicial(source_row["extended_projection"])
        assert not boundary(cycle)
        pivot = int(row["selected_pivot"])
        pivots[pivot] += 1
        coverage = row["coverage"]
        assert [entry["pivot"] for entry in coverage] == [0, 1, 2, 3]
        assert coverage[pivot]["uncovered_nonzero"] == 0
        assert all(coverage[index]["uncovered_nonzero"] for index in range(pivot))
        total = parse_total(row["total"]["lift"])
        assert not total_chain_boundary(total)
        augmentation = defaultdict(Fraction)
        for (indices, cell), coefficient in total.items():
            if len(indices) == 1 and len(cell) == 3:
                augmentation[cell] += coefficient
        assert clean(augmentation) == cycle
        if row["status"] == "BOUNDARY":
            witness = parse_simplicial(row["total"]["witness"])
            assert boundary(witness) == cycle
            assert len(witness) == row["total"]["witness_nonzero"]
            witness_sizes[len(witness)] += 1
            for value in witness.values():
                maximum_bits = max(maximum_bits, abs(value.numerator).bit_length(), value.denominator.bit_length())
        elif row["status"] == "NONBOUNDARY":
            assert row["total"]["dual_nonzero"] == len(row["total"]["dual"])
        else:
            assert row["status"].startswith("UNCOVERED")
    source_by_key = {(row["source"], row["ordinal"]): row for row in expected}
    for row in independent["records"]:
        source_row = source_by_key[(row["source"], row["ordinal"])]
        cycle = parse_simplicial(source_row["extended_projection"])
        assert row["status"] == "BOUNDARY"
        witness = parse_simplicial(row["witness"])
        assert boundary(witness) == cycle and len(witness) == row["witness_nonzero"]
    return {
        "status": "PASS", "records": len(result["records"]),
        "outcomes": dict(sorted(outcomes.items())), "pivot_counts": {str(key): value for key, value in sorted(pivots.items())},
        "witness_size_classes": len(witness_sizes), "minimum_witness_nonzero": min(witness_sizes) if witness_sizes else None,
        "maximum_witness_nonzero": max(witness_sizes) if witness_sizes else None, "maximum_coefficient_bits": maximum_bits,
        "independent_records": independent["selected_records"], "independent_classes": independent["selection_classes"],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
