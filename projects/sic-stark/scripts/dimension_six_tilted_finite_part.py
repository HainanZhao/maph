#!/usr/bin/env python3
"""Tilted finite parts and the exact d=6 fusion small divisor.

The symbolic part has no numerical dependency.  With ``--arb`` the script
also rehearses the primitive general-lens packet in rigorous complex balls.
The rehearsal is deliberately diagnostic: it records conditioning and does
not promote the still-open boundary-continuity assertion.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math


def centered_lift(value: int) -> int:
    """Lift modulo six to {-3,-2,-1,0,1,2}."""

    return (value + 3) % 6 - 3


def component_census() -> list[dict[str, object]]:
    records = []
    for first in range(6):
        for second in range(6):
            coefficient = centered_lift(4 * second - 5 * first)
            if coefficient == 0:
                kind = "PURELY_OSCILLATORY_FRESNEL"
            elif coefficient > 0:
                kind = "ONE_SIDED_GROWTH_NEGATIVE_END"
            else:
                kind = "ONE_SIDED_GROWTH_POSITIVE_END"
            records.append(
                {
                    "frequency": [first, second],
                    "centered_alpha_coefficient": coefficient,
                    "kind": kind,
                }
            )
    assert len(records) == 36
    assert sum(
        item["centered_alpha_coefficient"] == 0 for item in records
    ) == 6
    assert sum(
        item["centered_alpha_coefficient"] != 0 for item in records
    ) == 30
    return records


def arb_rehearsal() -> dict[str, object]:
    """Evaluate the normalized primitive RHS at approaching axis points."""

    from flint import ctx

    from dimension_six_cycle143_gate import algebraic_primitive_root
    from dimension_six_two_base_lens import (
        gamma_lens_factorized,
        geodesic_point,
    )

    ctx.dps = 90
    ctx.cap = 10
    tolerance = Fraction(1, 10**20)
    boundary = algebraic_primitive_root()
    records = []
    for parameter in (
        Fraction(1, 2),
        Fraction(1, 4),
        Fraction(1, 8),
        Fraction(1, 16),
        Fraction(1, 24),
    ):
        tau = geodesic_point(parameter)
        alpha = 4 * (4 * tau - 1) / 3
        first = gamma_lens_factorized(
            alpha, 2, tau, tolerance
        )
        second = gamma_lens_factorized(
            -alpha, 2, tau, tolerance
        )
        value = first * second
        defect = tau + 1 / tau - 5
        width = max(value.real.rad(), value.imag.rad())
        records.append(
            {
                "geodesic_parameter": str(parameter),
                "tau": str(tau),
                "fusion_defect": str(defect),
                "conditioning_proxy_inverse_fusion_defect": str(
                    1 / abs(defect)
                ),
                "primitive_oriented_rhs": str(value),
                "absolute_value": str(abs(value)),
                "absolute_value_minus_certified_x": str(
                    abs(value) - boundary
                ),
                "ball_radius": str(width),
            }
        )
    return {
        "backend": (
            "python-flint 0.9.0 / Arb via the 24-factor "
            "Sarkissian--Spiridonov continuation"
        ),
        "certified_boundary_x": str(boundary),
        "records": records,
        "interpretation": (
            "The balls are rigorous, but the unperiodized primitive "
            "factor is not the finite AFK overlap.  Its phase and size "
            "do not settle monotonically while the inverse-defect "
            "conditioning proxy grows.  Consequently these "
            "records are a rehearsal of the hard limit, not a proof or "
            "a disproof of fusion continuity."
        ),
        "enclosure_grade_boundary_convergence": "NOT_ESTABLISHED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arb", action="store_true")
    arguments = parser.parse_args()

    records = component_census()
    beta = (5 + math.sqrt(21)) / 2
    beta_inverse = 1 / beta
    leading_delta = 21 / beta
    leading_decay = (
        2 * math.pi * math.sqrt(21) * (1 - beta ** -6)
    )

    result: dict[str, object] = {
        "schema": "sic-stark-dimension-six-tilted-finite-part-v1",
        "tilted_integral": {
            "pole_free_strip": (
                "S_tau={y: 0<Re(y)<Re(Q_tau)}"
            ),
            "admissible_contour": (
                "C_h={c+h(t)+i*t:t in R}, with h C1, its graph "
                "and a homotopy to h=0 contained in S_tau, and the "
                "interior two-base kernel uniformly integrable on "
                "that homotopy"
            ),
            "value": (
                "I_tau,h(alpha,N)=sum_m integral_C_h F_tau,"
                "alpha,N(y,m) dy/(i*sqrt(omega1*omega2))"
            ),
            "tilt_independence_proof": [
                (
                    "truncate two admissible graphs at imaginary "
                    "height plus/minus T and join their endpoints"
                ),
                (
                    "the kernel is holomorphic in the closed region "
                    "between them because both pole cones lie outside "
                    "the pole-free strip"
                ),
                "Cauchy's theorem makes the integral around it zero",
                (
                    "the two cap integrals tend to zero by the common "
                    "interior exponential majorant"
                ),
                (
                    "letting T tend to infinity proves "
                    "I_tau,h0=I_tau,h1"
                ),
            ],
            "status": "PROVED_IN_INTERIOR_CONVERGENCE_CHAMBER",
            "boundary_definition": (
                "FP_beta(alpha,N)=lim_{s->0+} "
                "I_gamma(s),h(alpha,N), if the limit exists"
            ),
            "remaining_hypothesis": (
                "the tilted values extend continuously through the "
                "trace-five fusion locus and the extension is "
                "A6-flow invariant"
            ),
        },
        "components": {
            "records": records,
            "purely_oscillatory_count": 6,
            "one_sided_growing_count": 30,
            "zero_mode_method": (
                "Fresnel/Abel limit; no strip tilt is needed"
            ),
            "nonzero_mode_method": (
                "retain the two-base interior strip and take its "
                "tilted finite-part boundary value"
            ),
            "centered_lift_tie": (
                "residue three is lifted to -3; changing that tie "
                "reverses six growth orientations but not the 6/30 "
                "difficulty split"
            ),
        },
        "fusion_arithmetic": {
            "beta": "(5+sqrt(21))/2",
            "beta_decimal": beta,
            "minimal_polynomial": "X^2-5*X+1",
            "continued_fraction": "[4;overline{1,3}]",
            "geodesic": (
                "gamma(s)=(beta+beta^(-1)*s^2"
                "+i*sqrt(21)*s)/(1+s^2)"
            ),
            "fusion_defect": "Delta(tau)=tau+tau^(-1)-5",
            "exact_base_displacement": (
                "A6*tau-tau=-24*tau*Delta(tau)/(24*tau-5)"
            ),
            "geodesic_first_order": (
                "Delta(gamma(s))=i*(21/beta)*s+O(s^2)"
            ),
            "geodesic_first_order_numeric": leading_delta,
            "base_decay_parameter": (
                "kappa(s)=2*pi*abs(Im(A6*gamma(s)-gamma(s)))"
            ),
            "base_decay_first_order": (
                "kappa(s)=2*pi*sqrt(21)*(1-beta^(-6))*s+O(s^2)"
            ),
            "base_decay_first_order_numeric": leading_decay,
            "norm_identity": (
                "(n*beta-m)*(n*beta^(-1)-m)="
                "m^2-5*m*n+n^2 in Z\\{0}"
            ),
            "small_divisor_bound": (
                "||n*beta|| >= 1/(sqrt(21)*n+1/2), n>=1"
            ),
            "unit_circle_bound": (
                "|1-exp(2*pi*i*n*beta)| >= "
                "4/(sqrt(21)*n+1/2)"
            ),
            "difficulty_scale": (
                "exponential tail damping kappa(s)*n competes with "
                "quadratic-irrational divisors of size 1/n; the "
                "transition range is n asymptotic to 1/kappa(s), "
                "hence n asymptotic to 1/s"
            ),
        },
    }
    if arguments.arb:
        result["numerical_rehearsal"] = arb_rehearsal()
    else:
        result["numerical_rehearsal"] = {
            "status": "SKIPPED",
            "instruction": "rerun with --arb in the pinned environment",
        }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
