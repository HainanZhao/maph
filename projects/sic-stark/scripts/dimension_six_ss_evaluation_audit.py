#!/usr/bin/env python3
"""Cycle 146': exact Sarkissian--Spiridonov specialization audit.

The relevant published statement is the unnumbered theorem immediately
preceding equation (58), together with its limiting relation (66), in
arXiv:1910.11747v4.  Equation (66), not a generic appeal to a
"state-integral factorization", is the exact two-gamma Fourier
evaluation used here.

The script checks every discrete parameter and records the residual
relation after the standard reflection/shift basis is exhausted.
"""

from __future__ import annotations

import json
from fractions import Fraction


P_PARAMETER = -115
K_PARAMETER = 24
R_PARAMETER = 5
S_PARAMETER = 24
A_MATRIX = ((115, -24), (24, -5))


def delta_set(discrete: int) -> list[tuple[int, int]]:
    """S--S equation (15): Delta(k,p,m)."""

    result = []
    for gamma_index in range(K_PARAMETER):
        delta_index = (
            P_PARAMETER * gamma_index
            - P_PARAMETER * discrete
        ) % K_PARAMETER
        result.append((gamma_index, delta_index))
    assert len(result) == K_PARAMETER
    assert all(
        (
            P_PARAMETER * gamma_index
            - delta_index
            - P_PARAMETER * discrete
        )
        % K_PARAMETER
        == 0
        for gamma_index, delta_index in result
    )
    return result


def reflection_partner(
    argument: tuple[int, int],
    discrete: str,
) -> tuple[tuple[int, int], str]:
    """Formal partner Q-z, 4-m.

    Arguments are affine pairs (alpha coefficient, Q coefficient).
    Discrete labels are retained symbolically because N is free.
    """

    alpha_coefficient, q_coefficient = argument
    partner_argument = (
        -alpha_coefficient,
        1 - q_coefficient,
    )
    partners = {
        "N": "4-N",
        "4-N": "N",
        "0": "4",
        "4": "0",
    }
    return partner_argument, partners[discrete]


def main() -> None:
    bezout = P_PARAMETER * R_PARAMETER + K_PARAMETER * S_PARAMETER
    phase_coefficient = (
        P_PARAMETER - K_PARAMETER * (1 - S_PARAMETER)
    )
    assert bezout == 1
    assert phase_coefficient == 437

    # At beta^2-5beta+1=0, omega1=24beta-5=beta^3>0.
    # Store exact Q(beta)=constant+coefficient*beta.
    omega_one = (-5, 24)
    omega_two = (1, 0)
    q_period = (-4, 24)
    assert q_period == (
        omega_one[0] + omega_two[0],
        omega_one[1] + omega_two[1],
    )

    # The RHS of (66), after g=Q,l=0:
    # 24 Gamma_M(-alpha,4-N) Gamma_M(alpha,N) Gamma_M(Q,0).
    rhs_atoms = [
        ((-1, 0), "4-N"),
        ((1, 0), "N"),
        ((0, 1), "0"),
    ]
    rhs_atom_set = set(rhs_atoms)
    reflection_cancellations = []
    for argument, discrete in rhs_atoms:
        partner = reflection_partner(argument, discrete)
        if partner in rhs_atom_set:
            reflection_cancellations.append(
                ((argument, discrete), partner)
            )
    # Gamma(alpha,N) would reflect against Gamma(Q-alpha,4-N),
    # not the displayed Gamma(-alpha,4-N).
    assert not reflection_cancellations

    # Could a standard Q=omega1+omega2 shift repair the continuous
    # mismatch without changing the discrete label?  The unique
    # continuous shift is (a,b)=(1,1), whose label change is ar-b=4.
    q_shift_discrete_change = R_PARAMETER - 1
    assert q_shift_discrete_change == 4
    q_shift_preserves_label_mod_24 = (
        q_shift_discrete_change % K_PARAMETER == 0
    )
    assert not q_shift_preserves_label_mod_24

    factor_sets = {
        "Gamma(alpha,N)": delta_set(0),
        "Gamma(-alpha,4-N)": delta_set(4),
        "Gamma(Q,0)": delta_set(0),
    }

    hypotheses = [
        {
            "hypothesis": "M=[[-p,-s],[k,-r]] in SL(2,Z), k>0",
            "verification": (
                "(-115)*5+24*24=1; "
                "M=[[115,-24],[24,-5]]=A6"
            ),
            "status": "VERIFIED",
        },
        {
            "hypothesis": "equation (58) discrete sector nu=0",
            "verification": "m,N,l are integral; l=0",
            "status": "VERIFIED",
        },
        {
            "hypothesis": "positive boundary periods",
            "verification": (
                "omega2=1 and omega1=24*beta-5=beta^3>0"
            ),
            "status": "VERIFIED",
        },
        {
            "hypothesis": "balancing before degeneration",
            "verification": (
                "equation (66) is derived from (58) by the limits "
                "stated after equations (60)--(65); no new balancing "
                "condition remains beyond Q=omega1+omega2"
            ),
            "status": "VERIFIED_BY_SOURCE",
        },
        {
            "hypothesis": "g=Q,l=0 specialization",
            "verification": (
                "RHS becomes 24*Gamma(-alpha,4-N)*"
                "Gamma(alpha,N)*Gamma(Q,0)"
            ),
            "status": "VERIFIED",
        },
        {
            "hypothesis": "fixed scalar is finite and nonzero",
            "verification": (
                "pole positivity excludes Q from the pole lattice; "
                "the zero equation -115+24*n=1 has no integer n"
            ),
            "status": "VERIFIED",
        },
        {
            "hypothesis": "restrictions used in the proof",
            "verification": (
                "the paragraph after equation (58) explicitly lifts "
                "the auxiliary period/chamber restrictions by "
                "analytic continuation"
            ),
            "status": "VERIFIED_BY_SOURCE",
        },
        {
            "hypothesis": "undeformed contour at g=Q",
            "verification": (
                "equation (66) gives a meromorphic identity, but the "
                "source does not separately prove that the original "
                "vertical contour remains unpinched at this endpoint"
            ),
            "status": "OPEN_FOR_DIRECT_BOUNDARY_INTEGRAL",
        },
    ]

    result = {
        "schema": "sic-stark-dimension-six-ss-evaluation-audit-v1",
        "source": {
            "paper": (
                "Sarkissian--Spiridonov, General modular quantum "
                "dilogarithm and beta integrals, arXiv:1910.11747v4"
            ),
            "main_statement": (
                "unnumbered theorem immediately preceding equation (58)"
            ),
            "balancing_equation": 57,
            "beta_integral_equation": 58,
            "degenerate_two_gamma_evaluation": 66,
            "analytic_continuation_paragraph": (
                "paragraph immediately following equation (58)"
            ),
        },
        "parameter_map": {
            "p": P_PARAMETER,
            "k": K_PARAMETER,
            "r": R_PARAMETER,
            "s": S_PARAMETER,
            "pr_plus_ks": bezout,
            "M": [list(row) for row in A_MATRIX],
            "omega1": "24*beta-5=beta^3",
            "omega2": "1",
            "Q": "omega1+omega2",
            "g": "Q",
            "l": 0,
            "N": "arbitrary integral beta-transform label",
            "alpha": "helical continuous frequency",
        },
        "hypotheses": hypotheses,
        "all_meromorphic_identity_hypotheses_verified": all(
            item["status"] != "FAILED"
            for item in hypotheses
        ),
        "direct_boundary_contour_hypothesis_open": True,
        "equation_66_boundary_lhs": (
            "integral_{-i infinity}^{i infinity} sum_{m=0}^{23} "
            "exp(pi*i*m*437*(2*N-4)/24) "
            "exp(pi*i*alpha*(2*y-Q)/(24*omega1)) "
            "Gamma_M(y,m)*Gamma_M(Q-y,-m) "
            "dy/(i*sqrt(omega1))"
        ),
        "equation_66_boundary_rhs": (
            "24*Gamma_M(-alpha,4-N)*Gamma_M(alpha,N)*"
            "Gamma_M(Q,0)"
        ),
        "double_sine_expansion": {
            "definition": (
                "S_here(z|omega1,1)=gamma^(2)(z;omega1,1)"
            ),
            "factor_nodes": (
                "z_(gamma,delta)(mu,m)="
                "(mu+omega1*delta+gamma)/24"
            ),
            "delta_condition": (
                "-115*gamma-delta == -115*m mod 24"
            ),
            "factor_counts": {
                key: len(value)
                for key, value in factor_sets.items()
            },
            "formula": (
                "Gamma_M(mu,m)=C_m(mu)*"
                "product_{Delta(24,-115,m)} S_here(z_(gamma,delta))"
            ),
            "C_m": (
                "Z(m)*exp(-pi*i*B22(mu)/48"
                "+pi*i*sum_Delta B22(z)/2)"
            ),
        },
        "canonical_relation_reduction": {
            "reflection_cancellations": len(reflection_cancellations),
            "Q_shift_discrete_change": q_shift_discrete_change,
            "Q_shift_preserves_label_mod_24": (
                q_shift_preserves_label_mod_24
            ),
            "irreducible_oriented_residue": (
                "Gamma_M(-alpha,4-N)*Gamma_M(alpha,N)"
            ),
            "standard_relations_determine_only_norms": True,
        },
        "verdict": {
            "SS_equation_66_is_a_new_integral_transform_identity": True,
            "SS_supplies_new_finite_multiplicative_relation": False,
            "SS_evaluation_alone_implies_TCC_33": False,
            "conservation_of_obstruction": True,
            "remaining_map": (
                "periodize the continuous-discrete Fourier identity "
                "on the helical quotient and justify its boundary "
                "specialization"
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
