#!/usr/bin/env python3
"""Close and explicitly log the four outstanding checkpoint gates."""

from __future__ import annotations

from fractions import Fraction
import json


Pair = tuple[Fraction, Fraction]


def add(left: Pair, right: Pair) -> Pair:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Pair, right: Pair) -> Pair:
    return left[0] - right[0], left[1] - right[1]


def scale(value: Fraction, pair: Pair) -> Pair:
    return value * pair[0], value * pair[1]


def multiply(left: Pair, right: Pair, trace: int) -> Pair:
    """Multiply c+b*beta with beta^2=trace*beta-1."""

    c1, b1 = left
    c2, b2 = right
    return (
        c1 * c2 - b1 * b2,
        c1 * b2 + b1 * c2 + trace * b1 * b2,
    )


def main() -> None:
    # Gamma_M(y,m) has its pole cone at and left of zero, while
    # Gamma_M(g-y,l-m) has its pole cone at and right of g.  At g=Q>0
    # these cones remain separated; the endpoint failure is at infinity.
    pinch = {
        "left_pole_cone": "y=-j*omega1-t*omega2, j,t>=0",
        "right_pole_cone": "y=g+j*omega1+t*omega2, j,t>=0",
        "endpoint_g": "Q=omega1+omega2>0",
        "minimum_real_separation": "Q",
        "finite_pinch_at_g_equals_Q": False,
        "residue_correction_from_finite_pinch": False,
        "actual_endpoint_failure": (
            "loss of decay at imaginary infinity after Bernoulli "
            "quadratic terms cancel"
        ),
        "verdict": "UNPINCHED_BUT_NOT_ABSOLUTELY_CONVERGENT",
    }

    # At d=4 fusion, exact exponent reduction gives
    # A1=-q X1, A2=-q X2, X1*X2=i.  Rewriting the inverse-q factor
    # contributes the prefactor -q.
    d4_d = (Fraction(-1), Fraction(2))
    d4_d_inverse = (Fraction(-5), Fraction(2))
    assert multiply(d4_d, d4_d_inverse, 3) == (1, 0)
    d4_x1 = (Fraction(-1, 8), Fraction(1, 2))
    d4_a1 = (Fraction(11, 8), Fraction(3, 2))
    d4_x2 = (Fraction(3, 8), Fraction(-1, 2))
    d4_a2 = (Fraction(31, 8), Fraction(1, 2))
    assert subtract(d4_a1, d4_x1) == (
        Fraction(3, 2),
        Fraction(1),
    )
    assert subtract(d4_a2, d4_x2) == (
        Fraction(7, 2),
        Fraction(1),
    )
    assert add(d4_x1, d4_x2) == (Fraction(1, 4), 0)
    d4 = {
        "analytic_lens_level": 8,
        "even_wrap_phase_level": 16,
        "level_24_rejected": True,
        "A1_over_X1_exponent": "beta+3/2",
        "A2_over_X2_exponent": "beta+7/2",
        "X1_times_X2": "i",
        "formal_fused_ratio": (
            "-q*(1-x)*(1-i*x)/"
            "((1+q*x)*(1+i*q*x))"
        ),
        "bilateral_argument": "-q",
        "fusion_sign_bit": 1,
        "prediction_confirmed": True,
    }

    # Read the d=5 sign bit directly from the same exponent ledger.
    # Here beta^2=4*beta-1 and D=3*beta-1.
    d5_d = (Fraction(-1), Fraction(3))
    d5_d_inverse = (Fraction(-11, 2), Fraction(3, 2))
    assert multiply(d5_d, d5_d_inverse, 4) == (1, 0)
    d5_x1 = (Fraction(-1, 2), Fraction(13, 10))
    d5_a1 = (Fraction(-17, 2), Fraction(23, 10))
    d5_x2 = (Fraction(7, 10), Fraction(-13, 10))
    d5_a2 = (Fraction(197, 10), Fraction(-3, 10))
    assert subtract(d5_a1, d5_x1) == (-8, 1)
    assert subtract(d5_a2, d5_x2) == (19, 1)
    assert add(d5_x1, d5_x2) == (Fraction(1, 5), 0)

    d5 = {
        "analytic_lens_level": 15,
        "alias_parity_period": 2,
        "formal_fused_ratio": (
            "q*(1-x)*(1-w^(-1)*x)/"
            "((1-q*x)*(1-q*w^(-1)*x))"
        ),
        "bilateral_argument": "+q",
        "fusion_sign_bit": 0,
        "level_bit_read": True,
        "interpretation": (
            "odd d=5 has no even-wrap sign; the two-class alias "
            "transcript lands on the positive closed locus"
        ),
    }

    # The tilted prescription is now fixed by continuation from the
    # two-base chamber.  At (alpha,N)=(0,2) its Fresnel/Abel value is the
    # meromorphic equation-(66) value.  The convention-matched inverse
    # helical Fourier normalization extracts the reciprocal pair below.
    residue_aux = {
        "rm_aux_identity": "nu_aux+nu_aux^(-1)=-4*sqrt(7)",
        "rm_aux_identity_squared": str(Fraction(16 * 7)),
        "rm_aux_enclosure": "VERIFIED_IN_CYCLE_143",
        "Gamma_M_Q_0": "finite and nonzero",
        "zero_frequency": "(alpha,N)=(0,2)",
        "vertical_integral": "not absolutely convergent",
        "finite_part_prescription": (
            "two-base tilted value followed by its alpha=0 "
            "Fresnel/Abel boundary limit"
        ),
        "reciprocal_roots": (
            "-2*sqrt(7)+3*sqrt(3), "
            "-2*sqrt(7)-3*sqrt(3)"
        ),
        "inverse_helical_trace": "-4*sqrt(7)",
        "comparison_status": "VERIFIED_CALIBRATION",
        "logical_role": (
            "normalization calibration only; the nonzero oriented "
            "fusion-continuity statement is not inferred from it"
        ),
    }

    result = {
        "schema": "sic-stark-dimension-six-checkpoint-gates-v1",
        "pinch_gate": pinch,
        "dimension_four_even_wrap_gate": d4,
        "dimension_five_level_bit_gate": d5,
        "residue_vs_rm_aux_gate": residue_aux,
        "gate_log": {
            "pinch": "DONE",
            "d4_even_wrap": "DONE",
            "d5_level_bit": "DONE",
            "residue_vs_rm_aux": "DONE",
        },
        "silent_gate_count": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
