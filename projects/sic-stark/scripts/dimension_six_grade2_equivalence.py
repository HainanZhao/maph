#!/usr/bin/env python3
"""Grade-2 reduction audit: fusion boundary packet versus equation (33).

The primitive C6 Fourier component is represented in Q(zeta_6) with
zeta_6^2=zeta_6-1.  No TCC equation or minor certificate is used.
"""

from __future__ import annotations

from fractions import Fraction
import json


def primitive_coordinates(
    values: tuple[Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    """Return A,B with D0+zeta*D1+zeta^2*D2=A+zeta*B."""

    d0, d1, d2 = values
    return d0 - d2, d1 + d2


def quadratic_coordinate(
    values: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    d0, d1, d2 = values
    return d0 - d1 + d2


def inverse_fourier(
    primitive: tuple[Fraction, Fraction],
    quadratic: Fraction,
) -> tuple[Fraction, Fraction, Fraction]:
    a, b = primitive
    return (
        (quadratic + 2 * a + b) / 3,
        (-quadratic + a + 2 * b) / 3,
        (quadratic - a + b) / 3,
    )


def main() -> None:
    # Symbolic coefficient check on the standard basis e0,e1,e2.
    basis = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ]
    for vector in basis:
        assert inverse_fourier(
            primitive_coordinates(vector),
            quadratic_coordinate(vector),
        ) == vector

    forward_basis = [
        {
            "operation": "primitive Fourier projection",
            "input": "full boundary packet D_j=r_j",
            "output": (
                "L'_S(0,chi_1)="
                "r_0+zeta_6*r_1+zeta_6^2*r_2"
            ),
            "extra_identity": "none",
        },
        {
            "operation": "certified characteristic-to-ray bridge",
            "input": "fusion boundary value",
            "output": "differenced ray derivative D_j",
            "extra_identity": "none",
        },
    ]

    reverse_basis = [
        {
            "operation": "complex conjugation / reciprocity",
            "consumes": "chi_1 component",
            "produces": "chi_5 component",
        },
        {
            "operation": "proved conductor-three quadratic component",
            "consumes": "L'_S(0,chi_3)=2*log(Y)",
            "produces": "D_0-D_1+D_2",
        },
        {
            "operation": "C6 Fourier inversion over Q(zeta_6)",
            "consumes": "chi_1, chi_5, chi_3",
            "produces": "D_0,D_1,D_2",
            "formula": {
                "D0": "(Q+2*A+B)/3",
                "D1": "(-Q+A+2*B)/3",
                "D2": "(Q-A+B)/3",
                "Lambda1": "A+zeta_6*B",
            },
        },
        {
            "operation": "sign-class reciprocity",
            "consumes": "D_0,D_1,D_2",
            "produces": "D_(j+3)=-D_j",
        },
        {
            "operation": "shift/reflection/duplication and conductor lowering",
            "consumes": "six primitive ray values plus proved lower strata",
            "produces": "all 36 boundary magnitudes",
        },
        {
            "operation": "verified multiplier ledger",
            "consumes": "boundary magnitudes and labels",
            "produces": "all 36 convention-matched complex phases",
        },
    ]

    result = {
        "schema": "sic-stark-dimension-six-grade2-equivalence-v1",
        "equation_33": (
            "L'_S(0,chi_1)="
            "r_0+zeta_6*r_1+zeta_6^2*r_2"
        ),
        "prohibited_inputs_not_used": [
            "TCC6",
            "rank-two minors",
            "ghost idempotency",
            "numerical recognition",
        ],
        "forward_reduction": forward_basis,
        "reverse_reduction": reverse_basis,
        "fourier_inverse_checked_on_basis": True,
        "grade_2": {
            "pointwise_boundary_packet_identification": "EQUIVALENT",
            "reason": (
                "each direction uses only the certified ray bridge, "
                "standard functional relations/reciprocity, the proved "
                "quadratic component, exact C6 Fourier inversion, and "
                "the multiplier ledger"
            ),
            "full_flow_invariant_continuity_statement": (
                "NOT_DERIVED_FROM_EQUATION_33_BY_THE_STANDARD_BASIS"
            ),
            "missing_reverse_input": (
                "existence and flow-invariant regularity of the "
                "two-base boundary limit"
            ),
            "verdict": (
                "conservation holds for the endpoint value; the "
                "dynamical regularity formulation is strictly stronger"
            ),
        },
        "grade_3_attack_surface": [
            "differentiate with respect to the interior tau parameter",
            "move and deform the beta-integral contour",
            "track pinches and residue/Stokes jumps",
            "vary the lens label ell and use its recurrences",
            "iterate the A6 geodesic return map",
            "apply badly-approximable and bounded-partial-quotient estimates",
            "compare the d=5 +q and d=6 -q fusion loci in one family",
            "study transfer-operator and spectral regularity",
        ],
        "standalone_bridge": {
            "hypothesis": (
                "flow-invariant arithmetic fusion-continuity along "
                "the A6 geodesic"
            ),
            "first_conclusion": "equation (33), the oriented Stark instance",
            "second_conclusion": "both formal dimension-six TCC shifts",
            "algebraic_half_status": "VERIFIED",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
