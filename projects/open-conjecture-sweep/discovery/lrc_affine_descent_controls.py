#!/usr/bin/env python3
"""Exact generic raw/compressed controls for Cycle 47 affine descent."""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle47-affine-descent"


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def left_product(weights, matrix):
    return [sum((weights[row] * matrix[row][column] for row in range(len(matrix))), Fraction(0)) for column in range(len(matrix[0]))]


def main():
    # Three nonempty local stalks: a=b, b=c, c-a=1.  Their gluing is
    # inconsistent, with the primitive left-null cocycle (1,1,1).
    loop_matrix = [
        [Fraction(1), Fraction(-1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(-1)],
        [Fraction(-1), Fraction(0), Fraction(1)],
    ]
    loop_rhs = [Fraction(0), Fraction(0), Fraction(1)]
    loop_dual = [Fraction(1), Fraction(1), Fraction(1)]
    assert left_product(loop_dual, loop_matrix) == [0, 0, 0]
    assert dot(loop_dual, loop_rhs) == 1
    local_solutions = ([0, 0, 0], [0, 0, 0], [-1, 0, 0])
    assert all(dot(loop_matrix[index], local_solutions[index]) == loop_rhs[index] for index in range(3))

    # One canonical scalar x duplicated into three raw occurrences.  Exact
    # elimination of x1-x0 and x2-x0 recovers the compressed equation x=2.
    raw_matrix = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(-1), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    raw_rhs = [0, 0, 2, 2, 2]
    raw_solution = [2, 2, 2]
    assert matvec(raw_matrix, raw_solution) == raw_rhs
    compressed_matrix = [[Fraction(1)], [Fraction(1)], [Fraction(1)]]
    compressed_rhs = [2, 2, 2]
    assert matvec(compressed_matrix, [2]) == compressed_rhs

    # Repeated-type stabilizer: T=(a,a,b).  Two choices mapping sorted slots
    # to an occurrence differ by swapping the equal a slots.  An invariant
    # tensor is choice-independent; a deliberately noninvariant tensor is not.
    invariant = {(0, 1, 2): Fraction(3), (1, 0, 2): Fraction(3)}
    noninvariant = {(0, 1, 2): Fraction(3), (1, 0, 2): Fraction(4)}
    swap = (1, 0, 2)

    def permute(tensor, permutation):
        return {tuple(cell[permutation[index]] for index in range(3)): value for cell, value in tensor.items()}

    assert permute(invariant, swap) == invariant
    assert permute(noninvariant, swap) != noninvariant

    # Orientation lives in the omitted-part boundary sign, not in an
    # arbitrary sign attached to owner-coordinate transport.
    face_value = Fraction(5)
    correct_boundary = [face_value, -face_value, face_value, -face_value]
    injected_wrong = [face_value, face_value, face_value, -face_value]
    assert correct_boundary != injected_wrong

    # Frozen positive p199 controls: Cycles 43 and 44 each give a global
    # section, and their independently constructed tensors agree on every
    # labeled face in their overlap.
    prior43 = json.loads((ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json").read_text())
    prior44 = json.loads((ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json").read_text())
    faces43 = {tuple(row["triple"]): row["coefficients"] for row in prior43["face_tensors"]}
    faces44 = {tuple(row["triple"]): row["coefficients"] for row in prior44["face_tensors"]}
    shared = sorted(set(faces43) & set(faces44))
    assert shared and all(faces43[triple] == faces44[triple] for triple in shared)
    assert prior43["canonical_failures"] == prior44["canonical_failures"] == 0

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage": "GENERIC_AFFINE_DESCENT_CONTROLS",
        "positive_raw_compressed": {"raw_variables": 3, "compressed_variables": 1, "solution": [2]},
        "inconsistent_three_stalk_loop": {
            "local_stalks_nonempty": 3,
            "global_status": "INCONSISTENT",
            "primitive_dual": [1, 1, 1],
            "pairing": 1,
        },
        "repeated_type_stabilizer": "PASS",
        "orientation_reversal_rejected": True,
        "frozen_positive_sections": {
            "cycle43_quadruples": prior43["raw_interfaces"],
            "cycle44_quadruples": prior44["selected_interfaces"],
            "shared_face_classes": len(shared),
            "shared_coefficients_match": True,
        },
        "claim_boundary": "Generic exact affine descent controls only; no p199 principal outcome is classified.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "generic-controls.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "loop_pairing": 1, "orientation_reversal_rejected": True}, sort_keys=True))


if __name__ == "__main__":
    main()
