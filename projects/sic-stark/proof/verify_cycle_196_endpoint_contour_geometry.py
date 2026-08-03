#!/usr/bin/env python3
"""Exact finite-pole geometry for the B033 endpoint-contour attempt.

This is deliberately a contour *geometry* result.  It proves that the source
central contour has no finite Gamma_M crossings along the attracting A_6
segment and consequently no finite anti-residue jump.  It does not take the
truncation to imaginary infinity.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


LEVEL = 24
DIMENSION = 6
ODD_CANONICAL_LABELS = tuple(range(1, 12, 2))


def attracting_path_geometry() -> dict[str, object]:
    """Derive the uniform real-part gap for 0<=s<=1.

    beta+beta^(-1)=5.  Hence
      Re gamma(s)-5/2 = sqrt(21)(1-s^2)/(2(1+s^2)) >= 0,
    so Re omega_1>=55, Re Q>=56, and c=Re Q/2>=28.
    """

    omega_lower = 55
    q_lower = omega_lower + 1
    c_lower = Fraction(q_lower, 2)
    assert c_lower == 28
    return {
        "epistemic_status": "PROVED",
        "path": "gamma(s)=(beta+beta^(-1)s^2+i*sqrt(21)s)/(1+s^2), 0<=s<=1",
        "beta_relation": "beta+beta^(-1)=5",
        "real_part_identity": "Re(gamma(s))-5/2=sqrt(21)*(1-s^2)/(2*(1+s^2))>=0",
        "Re_omega_1_lower_bound": omega_lower,
        "Re_Q_lower_bound": q_lower,
        "central_contour": "C_s={Re(Q(s))/2+i*lambda:lambda in R}",
        "Re_contour_lower_bound": str(c_lower),
        "endpoint": {
            "omega_1_beta": "55+12*sqrt(21)",
            "Q_beta": "56+12*sqrt(21)",
            "central_real_coordinate": "28+6*sqrt(21)",
        },
    }


def source_pole_cone_record(discrete: int) -> dict[str, object]:
    """Separate the source's two true-pole cones from C_s.

    The true first-factor poles are -j*omega_1-l and the reflected ones are
    Q+j*omega_1+l, with j,l>=0.  The hidden congruence/true-pole condition
    only removes points from these cones, so the displayed real inequalities
    cover every true pole for this m.
    """

    assert 0 <= discrete < LEVEL
    return {
        "m_mod_24": discrete,
        "first_factor_true_poles": "y=-j*omega_1-l, j,l>=0; l=24*n+5*j+m>=0",
        "reflected_factor_true_poles": "y=Q+j*omega_1+l, j,l>=0; l=24*n+5*j-m>=0",
        "first_real_side": "Re(y)<=0<Re(Q)/2",
        "second_real_side": "Re(y)>=Re(Q)>Re(Q)/2",
        "central_contour_has_true_pole": False,
        "finite_crossing_count": 0,
    }


def all_kernel_cones() -> dict[str, object]:
    records = [source_pole_cone_record(discrete) for discrete in range(LEVEL)]
    assert len(records) == LEVEL
    assert all(not row["central_contour_has_true_pole"] for row in records)
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "all_24_labels_pole_free_on_C_s": True,
        "total_finite_kernel_crossings": 0,
    }


def anti_residue_jump_vector() -> dict[str, object]:
    """Place all six sealed anti principal parts on the left of C_s."""

    records = []
    for label in ODD_CANONICAL_LABELS:
        records.append(
            {
                "canonical_odd_N": label,
                "source_pole": f"y=-{label}",
                "side": "strictly left of C_s",
                "minimum_real_gap_to_C_s": f"at least {28 + label}",
                "finite_crossing": False,
                "residue_jump": 0,
            }
        )
    assert [row["residue_jump"] for row in records] == [0] * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "finite_anti_residue_jump_vector": [0] * DIMENSION,
        "finite_anti_residues_preserved_under_contour_motion": True,
    }


def regular_part_boundary() -> dict[str, object]:
    """State exactly what finite-pole geometry does not supply."""

    return {
        "epistemic_status": "PROVED",
        "truncation": "I_T(s;alpha,m)=integral_(c(s)-iT)^(c(s)+iT) Fourier_phase*K_Q(y,m)dy/(i*sqrt(omega_1(s)))",
        "finite_pole_obstruction": False,
        "source_endpoint_asymptotic": "At g=Q the two quadratic Gamma_M asymptotics cancel; the undeformed vertical integrand has no common absolute decay at imaginary infinity.",
        "T_to_infinity_limit": "OPEN",
        "distributional_or_Abel_rule": "OPEN: no regulator is selected by this finite-pole geometry result",
        "endpoint_continuation_claimed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "sic-stark-cycle-196-endpoint-contour-geometry-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Along the frozen attracting A_6 segment, the source central contour separates every true pole cone of the 24-label two-gamma kernel and has no finite crossings. The six nonzero finite anti-residue germs lie strictly on its left, so their finite residue-jump vector is zero. This proves no T->infinity limit, Abel/distributional finite part, endpoint continuation, AFK identity, boundary value, fusion, Stark, or TCC result.",
        "attracting_path_geometry": attracting_path_geometry(),
        "kernel_pole_cones": all_kernel_cones(),
        "anti_residue_jumps": anti_residue_jump_vector(),
        "regular_part_boundary": regular_part_boundary(),
        "next_unresolved_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": "A source-selected Abel, Fresnel, or other distributional rule may control the central-contour regular part at imaginary infinity and yield an RM endpoint continuation with the zero finite-jump vector; no such rule or limit is proved here.",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
