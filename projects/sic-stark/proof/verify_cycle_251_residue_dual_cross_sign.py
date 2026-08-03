#!/usr/bin/env python3
"""Exact canonical residue-dual cross-sign audit for Cycle 251/B088."""
from __future__ import annotations

import json
from fractions import Fraction as F
from typing import TypeAlias

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks


RANK = 4
SCALE = 24
Pair: TypeAlias = tuple[F, F]
Word: TypeAlias = tuple[str, ...]
Polynomial: TypeAlias = dict[Word, F]
Matrix: TypeAlias = list[list[Polynomial]]


def p_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for word, coefficient in right.items():
        result[word] = result.get(word, F(0)) + coefficient
        if result[word] == 0:
            del result[word]
    return result


def p_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = left_word + right_word
            output[word] = output.get(word, F(0)) + left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in output.items() if coefficient}


def p_scale(poly: Polynomial, scalar: F) -> Polynomial:
    return {word: scalar * coefficient for word, coefficient in poly.items() if scalar * coefficient}


def matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    output: Matrix = [[{} for _ in range(RANK)] for _ in range(RANK)]
    for row in range(RANK):
        for col in range(RANK):
            for pivot in range(RANK):
                output[row][col] = p_add(output[row][col], p_mul(left[row][pivot], right[pivot][col]))
    return output


def transpose(matrix: Matrix) -> Matrix:
    return [[matrix[col][row] for col in range(RANK)] for row in range(RANK)]


def matrix_scale(matrix: Matrix, scalar: F) -> Matrix:
    return [[p_scale(entry, scalar) for entry in row] for row in matrix]


def scalar_matrix(entries: list[F]) -> Matrix:
    return [[{(): entries[row]} if row == col else {} for col in range(RANK)] for row in range(RANK)]


def residue_gram() -> Matrix:
    return [[{(): F(1)} if row + col == RANK - 1 else {} for col in range(RANK)] for row in range(RANK)]


def multiplication_matrix() -> Matrix:
    h = [{(f"h{degree}",): F(1)} for degree in range(RANK)]
    return [[h[row - col] if row >= col else {} for col in range(RANK)] for row in range(RANK)]


def pairing_audit() -> dict[str, object]:
    gram = residue_gram()
    multiplier = multiplication_matrix()
    assert matrix_mul(transpose(multiplier), gram) == matrix_mul(gram, multiplier)
    pull = scalar_matrix([F(SCALE**degree) for degree in range(RANK)])
    pull_inverse = scalar_matrix([F(1, SCALE**degree) for degree in range(RANK)])
    assert matrix_mul(transpose(pull), gram) == matrix_scale(matrix_mul(gram, pull_inverse), F(SCALE**3))
    return {
        "epistemic_status": "PROVED",
        "space": "V=C[mu]/(mu^4)",
        "pairing": "<f,g>=[mu^3]f*g",
        "gram": [[1 if row + col == RANK - 1 else 0 for col in range(RANK)] for row in range(RANK)],
        "multiplication_adjoint": "M_h^dagger=M_h",
        "pullback_adjoint": "P_24^dagger=24^3*P_24^(-1)",
        "graded_transfer": "T_e^(n)=24^(-2*n)*M_h*P_24",
        "derived_reverse": "T_e^sharp=(T_e^dagger)^(-1)=24^(2*n-3)*M_(h^(-1))*P_24",
        "inverse_jet_degree_0_to_3": [
            "h0^(-1)",
            "-h1*h0^(-2)",
            "h1^2*h0^(-3)-h2*h0^(-2)",
            "-h1^3*h0^(-4)+2*h1*h2*h0^(-3)-h3*h0^(-2)",
        ],
        "invertibility_source": "C249 proves the normalized leading coefficient h0 is nonzero for every positive edge.",
    }


def coefficients(item: dict[str, object]) -> tuple[F, Pair, Pair]:
    return (
        F(str(item["argument_mu"])),
        tuple(F(str(value)) for value in item["alpha"]),  # type: ignore[arg-type]
        tuple(F(str(value)) for value in item["beta"]),  # type: ignore[arg-type]
    )


def orient(pair: Pair) -> Pair:
    return (-pair[0], pair[1])


def negate(pair: Pair) -> Pair:
    return (-pair[0], -pair[1])


def orientation_audit() -> dict[str, object]:
    rows = []
    for source, target in (("A", "C"), ("C", "A")):
        for position, (source_item, target_item) in enumerate(zip(blocks()[source], blocks()[target]), 1):
            source_c, source_alpha, source_beta = coefficients(source_item)
            target_c, target_alpha, target_beta = coefficients(target_item)
            reflected_alpha = orient(source_alpha)
            reflected_beta = orient(source_beta)
            source_det = source_alpha[0] * source_beta[1] - source_alpha[1] * source_beta[0]
            reflected_det = reflected_alpha[0] * reflected_beta[1] - reflected_alpha[1] * reflected_beta[0]
            target_det = target_alpha[0] * target_beta[1] - target_alpha[1] * target_beta[0]
            assert source_c == target_c
            assert reflected_alpha == negate(target_alpha)
            assert reflected_beta == target_beta
            assert source_det > 0 and target_det == source_det
            assert reflected_det == -source_det < 0
            rows.append(
                {
                    "source_factor": f"{source}{position}",
                    "target_factor": f"{target}{position}",
                    "argument_slope_preserved": True,
                    "R_alpha": [str(value) for value in reflected_alpha],
                    "target_alpha": [str(value) for value in target_alpha],
                    "R_alpha_equals_minus_target_alpha": True,
                    "R_beta": [str(value) for value in reflected_beta],
                    "target_beta": [str(value) for value in target_beta],
                    "R_beta_equals_target_beta": True,
                    "source_determinant": str(source_det),
                    "reflected_determinant": str(reflected_det),
                    "target_determinant": str(target_det),
                    "reflected_q_domain": "|q_R|>1",
                    "reflected_qtilde_domain": "|qtilde_R|>1",
                    "target_q_domain": "|q_C249|<1 and |qtilde_C249|<1",
                    "source_state_match": False,
                }
            )
    assert len(rows) == 8
    return {
        "epistemic_status": "PROVED",
        "orientation": "R:(omega1,omega2)->(-omega1,omega2)",
        "rows": rows,
        "all_reflected_determinants_negative": True,
        "all_targets_in_C249_upper_chamber": True,
        "canonical_orientation_maps_outside_source_product_domain": True,
        "degree_0_to_3_contragredient_coefficients_compared": False,
        "stop_reason": "Every reflected factor exits the C249 q-product chamber and has R(alpha)=-alpha_target rather than alpha_target. The preregistered source-state prerequisite fails before coefficient comparison.",
    }


def audit() -> dict[str, object]:
    pairing = pairing_audit()
    orientation = orientation_audit()
    assert orientation["canonical_orientation_maps_outside_source_product_domain"]
    assert not orientation["degree_0_to_3_contragredient_coefficients_compared"]
    return {
        "epistemic_status": "PROVED",
        "status": "CANONICAL_RESIDUE_DUAL_CROSS_SIGN_FALSIFIED",
        "pairing_and_contragredient": pairing,
        "orientation_test": orientation,
        "conclusion": "The canonical residue pairing derives an algebraic reverse of every C250 transfer, but omega1 orientation reversal sends every retained factor out of the fixed source q-product chamber and differs from its A/C target by an additional alpha-period sign. Therefore this canonical dual cannot source-authorize the cross-sign edge.",
        "claim_boundary": "This excludes only the canonical residue-dual cross-sign candidate on C250's fixed rank-four chamber. It does not exclude another pairing, an analytically continued negative-period theorem with explicit monodromy, an enlarged jet rank, a Bernoulli-corrected orientation law, packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
