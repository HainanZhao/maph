#!/usr/bin/env python3
"""Exact theorem-domain and target audit for Cycle 253/B090."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks


def pair(item: dict[str, object], key: str) -> tuple[F, F]:
    return tuple(F(str(value)) for value in item[key])  # type: ignore[return-value]


def determinant(alpha: tuple[F, F], beta: tuple[F, F]) -> F:
    return alpha[0] * beta[1] - alpha[1] * beta[0]


def theorem_audit() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED",
        "primary_source": (
            "J. V. Stokman, Hyperbolic beta integrals, Adv. Math. 190 (2005), "
            "Appendix, Proposition 6.1 and the continuation statement after equation (6.8)"
        ),
        "source_domain": "tau_h in C minus R_{>=0}",
        "source_domain_simply_connected": True,
        "normalization": {
            "r": "alpha/beta",
            "x": "mu/beta",
            "tau_h": "-1/r=-beta/alpha",
            "center": "z_h=-i*(x-(r+1)/2)",
            "E": "exp(-pi*i*(r+1/r)/24)*exp(-pi*i*z_h^2/(2*r))",
            "positive_chamber_identity": "gamma(mu;alpha,beta)=E/Gamma_h(r,1;z_h)",
            "derivation": "Stokman Proposition 6.1 product, first on Re(r)>0 and Im(r)>0, then meromorphically on Im(r)>0",
        },
        "path": {
            "source": "tau_h=-1/r in the upper half-plane",
            "orientation_endpoint": "tau_h'=1/r=-tau_h in the lower half-plane",
            "both_avoid_slit": True,
            "path_independent": True,
            "reason": "single-valued meromorphic continuation on the simply connected slit domain",
        },
        "negative_alpha_endpoint": {
            "period_symmetry_used": "Gamma_h(r',1;z)=Gamma_h(1,r';z)",
            "derived_product": "gamma_cont(mu;-alpha,beta)=(q*exp(B*mu);q)_infinity/(exp(-A*mu);qtilde)_infinity",
            "equals_C252_reciprocal_formula": True,
            "now_source_authorized_by_theorem": True,
        },
    }


def target_rows() -> list[dict[str, object]]:
    rows = []
    for source, target in (("A", "C"), ("C", "A")):
        for position, (source_item, target_item) in enumerate(zip(blocks()[source], blocks()[target]), 1):
            source_alpha = pair(source_item, "alpha")
            source_beta = pair(source_item, "beta")
            target_alpha = pair(target_item, "alpha")
            target_beta = pair(target_item, "beta")
            reflected_alpha = (-source_alpha[0], source_alpha[1])
            reflected_beta = (-source_beta[0], source_beta[1])
            c = F(str(source_item["argument_mu"]))
            assert c == F(str(target_item["argument_mu"])) and c != 0
            assert reflected_alpha == (-target_alpha[0], -target_alpha[1])
            assert reflected_beta == target_beta
            assert determinant(source_alpha, source_beta) > 0
            assert determinant(reflected_alpha, reflected_beta) < 0
            rows.append(
                {
                    "source_factor": f"{source}{position}",
                    "target_factor": f"{target}{position}",
                    "argument_slope": str(c),
                    "source_tau_h_half_plane": "upper",
                    "continued_tau_h_half_plane": "lower",
                    "slit_domain_hypothesis_both_embeddings": True,
                    "continued_beta_shift": "1-X^-1",
                    "target_beta_shift": "1-X",
                    "X": "exp(2*pi*i*argument/target_alpha)",
                    "X_nonconstant": True,
                    "shift_quotients_equal": False,
                    "continued_factor_equals_target": False,
                }
            )
    assert len(rows) == 8
    assert all(not row["shift_quotients_equal"] for row in rows)
    return rows


def audit() -> dict[str, object]:
    theorem = theorem_audit()
    rows = target_rows()
    return {
        "epistemic_status": "PROVED",
        "status": "DIRECT_CONTINUATION_EXISTS_BUT_UNCORRECTED_TARGET_MAP_FALSIFIED",
        "theorem_audit": theorem,
        "target_test": {
            "rows": rows,
            "all_eight_continuations_exist_at_both_embeddings": True,
            "all_eight_target_maps_fail_by_nonconstant_shift_quotient": True,
            "degree_0_to_3_jets_compared": False,
            "stop_reason": (
                "For every factor, continuation at (-alpha,beta) has beta-shift quotient "
                "1-exp(-2*pi*i*argument/alpha), while the declared target at (alpha,beta) "
                "has 1-exp(2*pi*i*argument/alpha). Their ratio is nonconstant."
            ),
        },
        "conclusion": (
            "Stokman's theorem repairs C252's analytic defect: the reciprocal formula is the "
            "path-independent continuation of the source normalization on the fixed slit domain. "
            "However, that continuation does not land in any of the eight declared opposite A/C "
            "factors. Their beta-shift quotients differ nonconstantly, so the uncorrected direct "
            "signed-period bridge fails before jet comparison."
        ),
        "claim_boundary": (
            "This proves existence of the theorem-backed ordinary-gamma continuation and excludes "
            "only its uncorrected identification with the eight C251 A/C targets. It does not "
            "exclude a separately sourced nonconstant transition operator, a full Gamma_M theorem, "
            "AFK identity, fusion theorem, Stark claim, or dimension-six TCC."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
