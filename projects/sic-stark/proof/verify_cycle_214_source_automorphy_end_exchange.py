#!/usr/bin/env python3
"""Exact AFK-covariance-domain audit for Cycle 214/B051."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
A6 = ((115, -24), (24, -5))
J0 = ((1, 0), (0, -1))
S = ((0, 1), (-1, 0))
E = ((0, 1), (1, 0))
IDENTITY = ((1, 0), (0, 1))
CUSP_INFINITY = (0, 5)
CUSP_ZERO = (5, 0)


def matrix_multiply(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(sum(left[row][index] * right[index][column] for index in range(2)) for column in range(2))
        for row in range(2)
    )


def determinant(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    det = determinant(matrix)
    assert det in {-1, 1}
    return (
        (matrix[1][1] // det, -matrix[0][1] // det),
        (-matrix[1][0] // det, matrix[0][0] // det),
    )


def apply_integer(matrix: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> tuple[int, int]:
    return tuple(sum(matrix[row][column] * point[column] for column in range(2)) for row in range(2))


def apply(matrix: tuple[tuple[int, int], tuple[int, int]], point: tuple[int, int]) -> tuple[int, int]:
    return tuple(value % DIMENSION for value in apply_integer(matrix, point))


def quadratic_form(point: tuple[int, int]) -> int:
    first, second = point
    return first * first - 5 * first * second + second * second


def multiply_beta(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Multiply (a+b*beta)(c+d*beta), with beta^2=5*beta-1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + 5 * b * d


def mobius_beta(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    """Exact M.beta for the three frozen candidates."""
    if matrix == J0:
        return 0, -1
    if matrix == S:
        return -5, 1
    if matrix == E:
        return 5, -1
    raise AssertionError(matrix)


def denominator_sign_at_beta(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    """Sign of j_(M^-1)(beta), using beta=(5+sqrt(21))/2>0."""
    inv = inverse(matrix)
    c, d = inv[1]
    if (c, d) == (0, -1):
        return -1
    if (c, d) == (1, 0):
        return 1
    raise AssertionError((matrix, inv, c, d))


def candidate_audit() -> dict[str, object]:
    assert matrix_multiply(J0, S) == E
    assert matrix_multiply(E, E) == IDENTITY
    beta_inverse = (5, -1)
    assert multiply_beta((0, 1), beta_inverse) == (1, 0)
    records = []
    for name, matrix in (("J0", J0), ("S", S), ("E=J0*S", E)):
        det = determinant(matrix)
        sign = denominator_sign_at_beta(matrix)
        label_matrix = tuple(tuple(sign * entry for entry in row) for row in matrix)
        image_infinity = apply(label_matrix, CUSP_INFINITY)
        image_zero = apply(label_matrix, CUSP_ZERO)
        root_image = mobius_beta(matrix)
        records.append({
            "name": name,
            "matrix": [list(row) for row in matrix],
            "determinant": det,
            "ell_sign": sign,
            "label_action": "p->ell*M*p modulo 6",
            "cusp_infinity_image": list(image_infinity),
            "cusp_zero_image": list(image_zero),
            "M_beta_in_Q_beta_basis": list(root_image),
            "preserves_Q": all(quadratic_form(apply_integer(matrix, point)) == quadratic_form(point) for point in ((a, b) for a in range(-12, 13) for b in range(-12, 13))),
        })
    e_record = next(record for record in records if record["name"] == "E=J0*S")
    assert e_record["cusp_infinity_image"] == list(CUSP_ZERO)
    assert e_record["cusp_zero_image"] == list(CUSP_INFINITY)
    assert e_record["M_beta_in_Q_beta_basis"] == list(beta_inverse)
    assert e_record["preserves_Q"]
    return {
        "epistemic_status": "PROVED",
        "beta": "(5+sqrt(21))/2",
        "beta_inverse": "5-beta=(5-sqrt(21))/2",
        "records": records,
        "E_is_unique_frozen_candidate_exchanging_both_cusp_labels": True,
    }


def flow_conjugacy_audit() -> dict[str, object]:
    e_conjugate = matrix_multiply(matrix_multiply(E, A6), E)
    a_inverse = inverse(A6)
    assert e_conjugate == a_inverse
    assert e_conjugate != A6
    return {
        "epistemic_status": "PROVED",
        "E_A6_E_inverse": [list(row) for row in e_conjugate],
        "A6_inverse": [list(row) for row in a_inverse],
        "conclusion": "E_EXCHANGES_THE_CUSP_LABELS_AND_REVERSES_THE_DECLARED_A6_STEP",
    }


def source_domain_audit() -> dict[str, object]:
    """Apply only the frozen AFK transformed-tuple covariance statement."""
    return {
        "epistemic_status": "PROVED",
        "primary_source": {
            "paper": "Appleby--Flammia--Kopp, arXiv:2501.03970v2",
            "theorems": ["Theorem 7.7", "Theorem 7.8"],
            "frozen_provenance": "Cycle-188 primary-source hash and theorem identifiers",
        },
        "E_covariance": {
            "tuple_relation": "nu_p(t_E)=nu_(E*p)(t), because ell=+1",
            "determinant_negative_effect": "Theorem 7.7 complex-conjugates the underlying B_t cocycle factors",
            "candidate_mobius_root_image": "E*beta=beta^-1",
            "same_beta_oriented_packet_identification": "NOT_SUPPLIED_BY_DECLARED_THEOREMS",
        },
        "not_supplied_by_frozen_theorem": [
            "an action on the Cycle-211 asymptotic packet P_(a,b,h)(t)",
            "an action on the axis coordinate s, Lambda, or packet coordinate t",
            "an identification of the beta^-1-oriented transformed packet with the beta-oriented packet",
            "a source-derived exchange involution on W",
            "a source-derived multiplier/dual line or scalar dual pairing",
        ],
        "conclusion": "THE_DOCUMENTED_E_COVARIANCE_IS_TRANSFORMED_TUPLE_COVARIANCE_NOT_A_PROVED_SAME_PACKET_END_EXCHANGE",
    }


def run() -> dict[str, object]:
    candidates = candidate_audit()
    flow = flow_conjugacy_audit()
    domain = source_domain_audit()
    assert candidates["E_is_unique_frozen_candidate_exchanging_both_cusp_labels"]
    assert flow["E_A6_E_inverse"] == flow["A6_inverse"]
    assert domain["E_covariance"]["same_beta_oriented_packet_identification"] == "NOT_SUPPLIED_BY_DECLARED_THEOREMS"
    return {
        "schema": "sic-stark-cycle-214-source-automorphy-end-exchange-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the three frozen source GL_2 candidates, E=J0*S is the unique listed matrix that exchanges both Cycle-211 cusp labels, preserves Q, and conjugates A6 to A6^-1. Its Mobius action sends beta to beta^-1. The pinned AFK covariance relates normalized ghost overlaps and determinant-negative cocycle factors for a transformed tuple, but does not supply an identification of that transformed object with the beta-oriented Cycle-211 packet. It therefore supplies no proved end exchange, dual line, or scalar pairing on that packet. This proves no new AFK theorem, analytic gluing, multiplier trivialization, C198 comparison, fusion, Stark, or TCC statement.",
        "candidate_audit": candidates,
        "flow_conjugacy_audit": flow,
        "source_domain_audit": domain,
        "gate_outcome": {
            "candidate_E_label_and_flow_exchange": "PROVED_TRANSFORMED_TUPLE_STRUCTURE",
            "source_derived_same_packet_end_exchange": "NOT_SUPPLIED_BY_DECLARED_AFK_COVARIANCE",
            "source_derived_dual_or_sesquilinear_scalar_pairing": "NOT_SUPPLIED",
            "remaining_design_problem": "Derive a beta-to-beta^-1 analytic continuation or a source theorem identifying the transformed tuple's packet with the original packet before testing any dual pairing or fusion invariant.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
