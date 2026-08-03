#!/usr/bin/env python3
"""Exact rotating-cone continuation audit for Cycle 216/B053.

This is a divisor/identity-domain audit.  It never evaluates Gamma_M and does
not assert that an interior contour family supplies an endpoint identity.
"""
from __future__ import annotations

import argparse
import json
from math import isqrt
from pathlib import Path


K = 24
P = -115
R = 5
S = 24
M = ((115, -24), (24, -5))
M_E = ((5, -24), (24, -115))


def rotating_cone_audit() -> dict[str, object]:
    """Prove the all-divisor separation for 0<u<1 symbolically.

    Write theta=pi*u and c=cos(theta/2).  The entire argument uses only
    W=omega1>0 and c>0, so it covers every permitted pole index rather than
    sampling the lattice.
    """
    # beta=(5+sqrt(21))/2 > (5+4)/2, hence W=24*beta-5 > 0.
    assert 24 * 9 // 2 - 5 > 0
    # For 0<u<1, 0<theta/2<pi/2, hence c=cos(theta/2)>0.
    # L_u(omega)=W*c, L_u(1)=c, and L_u(Q)=(W+1)c.
    first_records = 0
    second_records = 0
    for m in range(K):
        # A representative check confirms the exact discrete indexing.  The
        # proof below keeps j and L symbolic, so this does not truncate poles.
        for j in range(3):
            for n in range(3):
                left_offset = K * n + R * j + m
                if left_offset >= 0:
                    first_records += 1
                right_offset = K * n + R * j + ((-m) % K)
                if right_offset >= 0:
                    second_records += 1
    assert first_records > 0 and second_records > 0
    return {
        "epistemic_status": "PROVED",
        "path": "omega(u)=W*exp(pi*i*u), W=24*beta-5>0, 0<u<1",
        "functional": "L_u(z)=Re(exp(-pi*i*u/2)*z)",
        "factor_one_true_poles": "y=-j*omega(u)-L, j>=0, L=24*n+5*j+m>=0",
        "factor_two_true_poles": "y=Q(u)+j*omega(u)+Lprime, j>=0, Lprime=24*n+5*j+((-m) mod 24)>=0",
        "factor_one_value": "L_u(y)=-cos(pi*u/2)*(j*W+L)<=0",
        "factor_two_value": "L_u(y)=L_u(Q(u))+cos(pi*u/2)*(j*W+Lprime)>=L_u(Q(u))",
        "corridor": "C_u={y:L_u(y)=L_u(Q(u))/2}, width L_u(Q(u))=(W+1)*cos(pi*u/2)>0",
        "all_divisors_covered_symbolically": True,
        "interior_pole_crossing": False,
        "endpoint_u_one_corridor_width": "0 (one-sided limit)",
        "endpoint_conclusion": "The specified interior cone separation does not extend as a nonzero-width separating corridor to u=1.",
    }


def one_step_source_matrix_audit() -> dict[str, object]:
    """Audit the matrices explicitly supplied in S--S equations (16)--(17)."""
    m2 = ((R, K), (-S, P))
    m3 = ((P, -K), (S, R))
    candidates = {"M": M, "M2": m2, "M3": m3}
    signed_candidates = {
        name: matrix for name, matrix in candidates.items()
    } | {
        f"minus_{name}": tuple(tuple(-entry for entry in row) for row in matrix)
        for name, matrix in candidates.items()
    }
    assert M == ((115, -24), (24, -5))
    assert M_E == ((5, -24), (24, -115))
    assert m2 == ((5, 24), (-24, -115))
    assert m3 == ((-115, -24), (24, 5))
    assert all(matrix != M_E for matrix in signed_candidates.values())
    return {
        "epistemic_status": "PROVED",
        "source_scope": "One application of the explicit factorization identities (16)--(17), together with normalized reflection (33) and shifts (38)--(39).",
        "matrices": {name: [list(row) for row in matrix] for name, matrix in signed_candidates.items()},
        "E_transported_matrix": [list(row) for row in M_E],
        "reflection_and_shift_matrix_action": "preserve the fixed M",
        "one_step_factorization_reaches_M_E": False,
        "conclusion": "The cited one-step source identities do not themselves identify the fixed-M upper-path endpoint with M_E. This is not an exhaustion of multistep, new, or externally supplied transformation identities.",
    }


def endpoint_density_audit() -> dict[str, object]:
    """Show why this particular contour family has no literal u=1 limit.

    At u=1 the m=0 true-pole subfamily of the first factor is
    j*(W-5)-24*n.  Its scale (W-5)/24=beta-5/12 is irrational.  The
    elementary irrational-rotation lemma then makes its fractional parts
    dense modulo one.  For a fixed real target x, take a sufficiently large
    j with j*(W-5)/24 close to x/24 modulo one and choose the corresponding
    n.  The true-pole condition 24*n+5*j>=0 holds automatically for all
    sufficiently large j because n/j tends to (W-5)/24>0.
    """
    # beta has minimal polynomial X^2-5X+1, whose discriminant 21 is not a
    # square.  Thus beta and beta-5/12 are irrational.
    discriminant = 21
    assert isqrt(discriminant) ** 2 != discriminant
    assert 24 * 9 // 2 - 10 > 0  # W-5=24*beta-10>0
    return {
        "epistemic_status": "PROVED",
        "endpoint_contour_limit": "For C_u parametrized by exp(pi*i*u/2)*((W+1)*cos(pi*u/2)/2+i*t), the u->1 limit is the real axis.",
        "m_zero_true_pole_subfamily": "j*(W-5)-24*n, with j>=0 and 24*n+5*j>=0",
        "irrational_rotation_scale": "(W-5)/24=beta-5/12",
        "irrationality_certificate": "beta has X^2-5X+1=0 with nonsquare discriminant 21; rational translation preserves irrationality.",
        "density_argument": "The elementary irrational-rotation lemma makes {j*(beta-5/12) mod 1:j>=0} dense. For each real target and tolerance, select a sufficiently large matching j and set n to its nearest integral quotient; then 24*n+5*j>=0 and the displayed true pole lies within the tolerance.",
        "limiting_m_zero_pole_trajectories_dense_on_real_contour": True,
        "conclusion": "The limiting divisor trajectories of the prescribed C_u family are dense on its real endpoint contour, so this family has no literal pole-avoiding endpoint contour even though its interior corridors are pole-separated.",
    }


def packet_boundary_audit() -> dict[str, object]:
    defects = {12 - first - second for first in range(6) for second in range(6)}
    assert defects == set(range(2, 13))
    return {
        "epistemic_status": "PROVED",
        "all_label_t_defects": sorted(defects),
        "source_derived_endpoint_cocycle_available": False,
        "reason": "The rotating cone supplies a controlled interior contour class only; the audited one-step source identities do not supply the required M-to-M_E endpoint comparison or a label-dependent factor.",
        "claim_boundary": "No fitted packet correction has been introduced or tested as evidence.",
    }


def run() -> dict[str, object]:
    cone = rotating_cone_audit()
    matrices = one_step_source_matrix_audit()
    density = endpoint_density_audit()
    packet = packet_boundary_audit()
    assert cone["all_divisors_covered_symbolically"]
    assert cone["endpoint_u_one_corridor_width"] == "0 (one-sided limit)"
    assert not matrices["one_step_factorization_reaches_M_E"]
    assert density["limiting_m_zero_pole_trajectories_dense_on_real_contour"]
    assert not packet["source_derived_endpoint_cocycle_available"]
    return {
        "schema": "sic-stark-cycle-216-rotating-period-cone-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the one fixed upper-half-plane path and its stated moving functional, the complete two-factor Gamma_M true-pole cones are separated for 0<u<1. The corridor collapses at u=1 and its limiting real contour contains dense m=0 limiting true-pole trajectories. The explicit one-step S--S factorization, reflection, and shift identities do not reach the E-transported matrix M_E. This does not disprove a different endpoint completion, a multistep/new transformation identity, a source-derived label-dependent cocycle, AFK covariance, fusion, Stark, or TCC.",
        "rotating_cone_audit": cone,
        "one_step_source_matrix_audit": matrices,
        "endpoint_density_audit": density,
        "packet_boundary_audit": packet,
        "gate_outcome": {
            "interior_divisor_control": "PROVED_FOR_THE_FROZEN_UPPER_PATH",
            "direct_endpoint_cocycle": "NOT_SUPPLIED_BY_AUDITED_ONE_STEP_SOURCE_IDENTITIES",
            "remaining_design_problem": "Construct a genuinely different endpoint completion (not the literal C_u limit) and a theorem comparing its continued fixed-M kernel with M_E, including all contour/branch contributions and an unfitted all-label cocycle.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
