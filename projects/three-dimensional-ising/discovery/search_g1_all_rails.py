#!/usr/bin/env python3
"""Exact common-independent extension after forcing all longitudinal rails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_lifted_matroids import _incidence_columns  # noqa: E402
from discovery.search_g1_paired_fundamental_cycles import (  # noqa: E402
    _labels,
    _matroid_intersection,
)
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def _basis(vectors):
    basis = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return basis


def _reduce(vector, basis):
    for pivot in sorted(basis, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= basis[pivot]
    return vector


def search(width, length, handle_cut):
    structural = _case(width, length)["length_rows"][-1]
    genus = structural["genus"]
    vertices, edges = cubic_box((length, width, width))
    incidence = _incidence_columns(vertices, edges)
    labels = _labels(structural, edges)
    incidence_bits = len(vertices) - 1
    left_bits = 2 * handle_cut
    shift = incidence_bits + left_bits
    mask = (1 << shift) - 1
    columns = []
    for index, (boundary, label) in enumerate(zip(incidence, labels)):
        left = boundary | ((label & ((1 << left_bits) - 1)) << incidence_bits)
        right = boundary | ((label >> left_bits) << incidence_bits)
        columns.append((index, left, right))
    rails = [index for index, edge in enumerate(edges) if edge.u[0] != edge.v[0]]
    left_basis = _basis([columns[index][1] for index in rails])
    right_basis = _basis([columns[index][2] for index in rails])
    if len(left_basis) != len(rails) or len(right_basis) != len(rails):
        raise AssertionError("longitudinal rails are not common-independent")
    quotient = []
    for index, left, right in columns:
        if index in set(rails):
            continue
        quotient.append((index, _reduce(left, left_basis) | (_reduce(right, right_basis) << shift)))
    certificate = _matroid_intersection(quotient, mask, shift, True)
    selected = [index for index, _ in certificate["selected"]]
    target_extension = 2 * (width * width - 1)
    return {
        "status": "OBSERVED exact GF(2) all-rails restriction",
        "shape": [length, width, width],
        "genus": genus,
        "handle_cut": handle_cut,
        "rail_count": len(rails),
        "target_transverse_extension": target_extension,
        "maximum_transverse_extension": len(selected),
        "criterion_met": len(selected) >= target_extension,
        "selected_transverse_edges": selected[:target_extension],
        "min_max_partition": [
            certificate["rank_M1_on_complement"],
            certificate["rank_M2_on_reachable"],
        ],
        "claim_boundary": (
            "Failure rejects only the all-longitudinal-rails specialization. "
            "Success at finitely many widths is not an arbitrary-width proof."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--handle-cut", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(search(**vars(args)), indent=2, sort_keys=True))
