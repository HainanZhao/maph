#!/usr/bin/env python3
"""Exact formal two-ended-completion audit for Cycle 213/B050."""
from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dimension_six_stabilizer_ledger import A6, afk_phase_exponent_mod_48


DIMENSION = 6
ROOT_OF_UNITY_ORDER = 48
CUSP_LABELS = ((0, 5), (5, 0))
IOTA = ((0, 1), (1, 0))
CROSS_PAIRING = ((0, 1), (1, 0))


def matrix_multiply(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(sum(left[row][index] * right[index][column] for index in range(2)) for column in range(2))
        for row in range(2)
    )


def transpose(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(tuple(matrix[column][row] for column in range(2)) for row in range(2))


def a6_cusp_multiplier_audit() -> dict[str, object]:
    records = []
    for first, second in CUSP_LABELS:
        image = (
            (A6[0][0] * first + A6[0][1] * second) % DIMENSION,
            (A6[1][0] * first + A6[1][1] * second) % DIMENSION,
        )
        exponent = afk_phase_exponent_mod_48(first, second)
        assert image == (first, second)
        assert exponent == 8
        records.append({"label": [first, second], "A6_image": list(image), "zeta_48_exponent": exponent})
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "common_multiplier": "chi=zeta_48^8",
        "common_multiplier_exponent_mod_48": 8,
    }


def formal_completion_audit() -> dict[str, object]:
    assert matrix_multiply(IOTA, IOTA) == ((1, 0), (0, 1))
    return {
        "epistemic_status": "PROVED",
        "state_space": "W=C*u_infinity direct_sum C*u_zero",
        "basis": {
            "u_infinity": "formal representative of [e_(0,5)]",
            "u_zero": "formal representative of [e_(5,0)]",
        },
        "exchange_involution": {"matrix": [list(row) for row in IOTA], "square": "identity"},
        "A6_action": "u_infinity->chi*u_infinity and u_zero->chi*u_zero",
        "scope": "FORMAL_COMPLETION_ONLY_NOT_A_PROVED_ANALYTIC_OR_ARITHMETIC_GLUE",
    }


def scalar_pairing_audit() -> dict[str, object]:
    chi_exponent = 8
    squared_exponent = (2 * chi_exponent) % ROOT_OF_UNITY_ORDER
    squared_order = ROOT_OF_UNITY_ORDER // gcd(squared_exponent, ROOT_OF_UNITY_ORDER)
    assert squared_exponent == 16
    assert squared_exponent != 0
    assert squared_order == 3
    return {
        "epistemic_status": "PROVED",
        "strict_scalar_condition": "B(A6*u,A6*v)=B(u,v)",
        "coefficient_equation": "(zeta_48^16-1)*B_ij=0 for each of the four pairing-matrix entries",
        "zeta_48_squared_exponent_mod_48": squared_exponent,
        "zeta_48_squared_order": squared_order,
        "nonzero_scalar_pairing_dimension": 0,
        "conclusion": "NO_NONZERO_STRICTLY_A6_INVARIANT_SCALAR_BILINEAR_PAIRING_ON_W",
    }


def cross_pairing_audit() -> dict[str, object]:
    iota_conjugate = matrix_multiply(matrix_multiply(transpose(IOTA), CROSS_PAIRING), IOTA)
    assert iota_conjugate == CROSS_PAIRING
    fixed_vector = (1, 1)
    restriction = sum(
        fixed_vector[row] * CROSS_PAIRING[row][column] * fixed_vector[column]
        for row in range(2)
        for column in range(2)
    )
    quotient_relation = (1, -1)
    left_relation = tuple(sum(quotient_relation[row] * CROSS_PAIRING[row][column] for row in range(2)) for column in range(2))
    right_relation = tuple(sum(CROSS_PAIRING[row][column] * quotient_relation[column] for column in range(2)) for row in range(2))
    assert restriction == 2
    assert left_relation != (0, 0)
    assert right_relation != (0, 0)
    return {
        "epistemic_status": "PROVED",
        "coefficient_line": "M with A6 action q->zeta_48^16*q",
        "pairing_matrix_in_u_infinity_u_zero_basis": [list(row) for row in CROSS_PAIRING],
        "definition": "B(u_infinity,u_zero)=B(u_zero,u_infinity)=q; same-end values are zero",
        "A6_equivariance": "B(A6*u,A6*v)=zeta_48^16*B(u,v)=A6_M*B(u,v)",
        "exchange_invariant": True,
        "fixed_line": "W^iota=span(u_infinity+u_zero)",
        "fixed_line_restriction_in_units_of_q": restriction,
        "iota_coinvariant_quotient": "W/span(u_infinity-u_zero)",
        "descends_to_iota_coinvariant_quotient": False,
        "quotient_failure": {
            "left_relation_pairing_in_units_of_q": list(left_relation),
            "right_relation_pairing_in_units_of_q": list(right_relation),
        },
        "conclusion": "NONZERO_EXCHANGE_INVARIANT_CHARACTER_VALUED_PAIRING_RESTRICTS_TO_THE_FIXED_LINE_BUT_DOES_NOT_DESCEND_TO_THE_NATURAL_IOTA_COINVARIANT_QUOTIENT",
    }


def run() -> dict[str, object]:
    multiplier = a6_cusp_multiplier_audit()
    completion = formal_completion_audit()
    scalar = scalar_pairing_audit()
    cross = cross_pairing_audit()
    assert multiplier["common_multiplier_exponent_mod_48"] == 8
    assert scalar["nonzero_scalar_pairing_dimension"] == 0
    assert cross["exchange_invariant"]
    assert not cross["descends_to_iota_coinvariant_quotient"]
    return {
        "schema": "sic-stark-cycle-213-two-ended-completion-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the declared formal two-cusp completion W and its constructed exchange involution, the frozen common A6 multiplier forbids every nonzero strictly scalar A6-invariant bilinear pairing. The declared exchange-symmetric cross pairing is exactly A6-equivariant only after retaining its multiplier-character coefficient line; it restricts nontrivially to the iota-fixed line but does not descend to the formal iota-coinvariant quotient. This proves neither an analytic gluing, a source quotient, a density/orientation theorem, C198 comparison, AFK identity, fusion-continuity theorem, Stark relation, nor TCC statement.",
        "a6_cusp_multiplier_audit": multiplier,
        "formal_completion_audit": completion,
        "scalar_pairing_audit": scalar,
        "cross_pairing_audit": cross,
        "gate_outcome": {
            "formal_two_ended_completion": "PROVED_WITH_CONSTRUCTED_EXCHANGE_ONLY",
            "strict_scalar_sign_independent_pairing": "FALSIFIED_IN_DECLARED_COMPLETION",
            "character_valued_fixed_line_pairing": "PROVED_BUT_NOT_A_SCALAR_FUSION_INVARIANT",
            "coinvariant_descent_of_declared_cross_pairing": "FALSIFIED",
            "remaining_design_problem": "Construct a source-authorized analytic/arithmetic completion or a multiplier trivialization derived from source data, then test a genuine fusion invariant without C198 fitting.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
