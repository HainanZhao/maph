#!/usr/bin/env python3
"""Exact direct-E parameter and packet audit for Cycle 215/B052."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
A6 = ((115, -24), (24, -5))
E = ((0, 1), (1, 0))


def matrix_multiply(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(sum(left[row][index] * right[index][column] for index in range(2)) for column in range(2))
        for row in range(2)
    )


def inverse(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    assert determinant == 1
    return ((matrix[1][1], -matrix[0][1]), (-matrix[1][0], matrix[0][0]))


def negate(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(tuple(-entry for entry in row) for row in matrix)


def extract_lens_parameters(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int, int, int]:
    """M=((-p,-s),(k,-r)) for the S--S equation-(66) convention."""
    p = -matrix[0][0]
    s = -matrix[0][1]
    k = matrix[1][0]
    r = -matrix[1][1]
    return p, k, r, s


def direct_parameter_audit() -> dict[str, object]:
    original = extract_lens_parameters(A6)
    assert original == (-115, 24, 5, 24)
    transformed_inverse = matrix_multiply(matrix_multiply(E, A6), E)
    assert transformed_inverse == inverse(A6)
    canonical = negate(transformed_inverse)
    transformed = extract_lens_parameters(canonical)
    assert canonical == ((5, -24), (24, -115))
    assert transformed == (-5, 24, 115, 24)
    p, k, r, s = original
    p_e, k_e, r_e, s_e = transformed
    assert p * r + k * s == 1
    assert p_e * r_e + k_e * s_e == 1
    original_phase = p - k * (1 - s)
    transformed_phase = p_e - k_e * (1 - s_e)
    assert original_phase == 437
    assert transformed_phase == 547
    # beta_E=5-beta.  In the basis 1,beta, omega1=k*beta-r.
    original_omega = (-r, k)
    transformed_omega = (5 * k_e - r_e, -k_e)
    assert original_omega == (-5, 24)
    assert transformed_omega == (5, -24)
    assert transformed_omega == tuple(-entry for entry in original_omega)
    return {
        "epistemic_status": "PROVED",
        "original_matrix_A6": [list(row) for row in A6],
        "original_lens_parameters_p_k_r_s": list(original),
        "original_phase_coefficient": original_phase,
        "E_A6_E_inverse": [list(row) for row in transformed_inverse],
        "k_positive_canonicalization_minus_A6_inverse": [list(row) for row in canonical],
        "transformed_lens_parameters_p_k_r_s": list(transformed),
        "transformed_bezout_pr_plus_ks": p_e * r_e + k_e * s_e,
        "transformed_phase_coefficient": transformed_phase,
        "beta_E": "beta^-1=5-beta",
        "omega1_original_in_Q_beta_basis": list(original_omega),
        "omega1_E_in_Q_beta_basis": list(transformed_omega),
        "omega1_E_equals_minus_omega1": True,
        "frozen_positive_period_hypothesis_for_E": False,
        "conclusion": "THE_DIRECT_E_MATRIX_DOES_NOT_PRESERVE_THE_FROZEN_POSITIVE_PERIOD_EQUATION66_SPECIALIZATION",
    }


def packet_exponent(first: int, second: int) -> int:
    return 4 * second - 5 * first


def bare_packet_inversion_audit() -> dict[str, object]:
    """Rule out every channel-global scalar by the label-dependent t power."""
    records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            source_exponent = packet_exponent(first, second)
            target_after_t_inverse = -packet_exponent(second, first) - 12
            ratio_exponent = source_exponent - target_after_t_inverse
            assert ratio_exponent == 12 - first - second
            records.append({
                "characteristic": [first, second],
                "source_t_exponent": source_exponent,
                "conjugate_E_image_after_t_inverse_exponent": target_after_t_inverse,
                "ratio_t_exponent": ratio_exponent,
            })
    ratio_exponents = sorted({record["ratio_t_exponent"] for record in records})
    assert ratio_exponents == list(range(2, 13))
    # The exponent formula contains no h or h-prime.  Thus its nonconstancy
    # disproves a scalar for every global channel image at once, without
    # inventing a channel-specific or label-specific correction.
    return {
        "epistemic_status": "PROVED",
        "candidate": "P_(a,b;h)(t)=kappa_h(t)*conjugate(P_(b,a;h_prime)(t^-1))",
        "global_channel_scope": "The t-ratio exponent 12-a-b is independent of h and h_prime, so the all-channel conclusion is symbolic rather than a channel-selected enumeration.",
        "label_count": len(records),
        "records": records,
        "ratio_t_exponents": ratio_exponents,
        "label_independent_kappa_h_possible": False,
        "reason": "The required t power 12-a-b varies on the complete label grid; no scalar depending only on h and t can cancel it.",
        "phase_note": "Any proposed label-dependent phase or t correction lies outside this bare candidate unless derived separately from an equation-(66) transformation law.",
    }


def run() -> dict[str, object]:
    parameters = direct_parameter_audit()
    packet = bare_packet_inversion_audit()
    assert not parameters["frozen_positive_period_hypothesis_for_E"]
    assert not packet["label_independent_kappa_h_possible"]
    return {
        "schema": "sic-stark-cycle-215-equation66-e-transport-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the frozen equation-(66) A6 specialization, direct E conjugacy canonicalizes to -A6^-1 with different lens parameters and phase coefficient, and its beta^-1 period is exactly the negative of the frozen positive omega1. Therefore the cited positive-period specialization supplies no direct E-transformed equation. Independently, the bare conjugate t-inversion of the complete source packet requires a label-dependent t^(12-a-b) correction, so no channel-global scalar cocycle realizes it. This does not exclude a new analytic continuation theorem for the changed Gamma_M data, a source-derived label-dependent cocycle, C198 comparison, fusion, Stark, or TCC statement.",
        "direct_parameter_audit": parameters,
        "bare_packet_inversion_audit": packet,
        "gate_outcome": {
            "direct_E_equation66_positive_period_transport": "FALSIFIED_FOR_THE_FROZEN_SPECIALIZATION",
            "bare_conjugate_t_inversion_with_channel_global_scalar": "FALSIFIED_ALL36",
            "remaining_design_problem": "Derive a new analytic continuation or changed-parameter Gamma_M transformation that supplies the required label-dependent cocycle and valid period/contour control before claiming an E-induced packet duality.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
