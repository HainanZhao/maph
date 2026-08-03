#!/usr/bin/env python3
"""Exact product-domain audit for Cycle 218/B055's signed-period cover."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


K = 24
RAW_ENDPOINT = (5, -24, -115, -24)  # -S_E from Cycle 217
E_TARGET = (-5, 24, 115, 24)


def positive_scaling_audit() -> dict[str, object]:
    """Equation (5)--(8) are invariant under a positive common scale."""
    # u=(mu+m*omega2)/(k*omega2),
    # tau=(omega1+r*omega2)/(k*omega2), and their tilde counterparts have
    # homogeneous numerator/denominator.  B_2,2 in (27) is degree zero, so
    # normalized Gamma_M in (29) has the same law wherever it is defined.
    scale = 576
    assert scale > 0
    return {
        "epistemic_status": "PROVED",
        "law": "Gamma_M(c*mu,m;c*omega1,c*omega2)=Gamma_M(mu,m;omega1,omega2) for c>0 within the source-defined k>0 domain",
        "scale": scale,
        "product_parameter_check": {
            "u": "homogeneous degree zero",
            "tau": "homogeneous degree zero",
            "tilde_u": "homogeneous degree zero",
            "tilde_tau": "homogeneous degree zero",
            "B_2_2": "homogeneous degree zero",
        },
        "raw_endpoint_formal_reduction": "576*(omega2,omega1; mu+m*omega2) -> (omega2,omega1; mu+m*omega2)",
        "scope_warning": "This law cannot by itself change a negative-k raw representative into the source-defined k>0 domain.",
    }


def swap_reindexing_audit() -> dict[str, object]:
    """Check the finite Delta-set relabeling that a swap would require."""
    p, k, r, _s = E_TARGET
    assert p * r % k == 1
    rows = []
    for m in range(k):
        original = {(gamma, delta) for gamma in range(k) for delta in range(k) if (p * gamma - delta - p * m) % k == 0}
        # After exchanging gamma/delta, the target Delta uses p'=r and
        # m'=-p*m: r*delta-gamma == r*(-p*m) == -m mod k.
        target_m = (-p * m) % k
        swapped = {(delta, gamma) for gamma, delta in original}
        target = {(gamma, delta) for gamma in range(k) for delta in range(k) if (r * gamma - delta - r * target_m) % k == 0}
        assert len(original) == k
        assert swapped == target
        rows.append({"m": m, "swap_label": target_m})
    return {
        "epistemic_status": "PROVED",
        "scope": "Finite Delta(k,p,m) index relabeling in equation (15), for the positive-k E target parameters only.",
        "parameter_transition": {"p": p, "r": r, "k": k, "label_map": "m -> -p*m mod k"},
        "rows_checked": len(rows),
        "all_delta_sets_reindexed": True,
        "conclusion": "A period-swap comparison would require p<->r and m->-p*m at the finite product-index level. This is not yet a normalized Gamma_M swap law: ordinary-gamma ordering, Z(m), and the signed matrix representative still require a source-defined comparison.",
    }


def signed_representative_domain_audit() -> dict[str, object]:
    raw_p, raw_k, raw_r, raw_s = RAW_ENDPOINT
    target_p, target_k, target_r, target_s = E_TARGET
    assert tuple(-entry for entry in RAW_ENDPOINT) == E_TARGET
    assert raw_k == -K and target_k == K
    return {
        "epistemic_status": "PROVED",
        "source_definition_domain": "Equations (3), (5), and (15) fix k>0 and m in Z_k before defining the rarefied product.",
        "raw_endpoint": list(RAW_ENDPOINT),
        "target": list(E_TARGET),
        "raw_k_in_source_product_domain": raw_k > 0,
        "target_k_in_source_product_domain": target_k > 0,
        "simultaneous_sign_candidate": "(p,k,r,s)->(-p,-k,-r,-s)",
        "source_provided_Gamma_M_sign_law": False,
        "conclusion": "The frozen product definition does not define the negative-k raw endpoint as a member of the same Gamma_M domain, so it supplies no simultaneous-sign bridge from -S_E to S_E. A sign law would require a new extension/construction, not a projective convention.",
    }


def legal_lift_audit() -> dict[str, object]:
    scaling = positive_scaling_audit()
    swap = swap_reindexing_audit()
    sign = signed_representative_domain_audit()
    assert scaling["scale"] == 576
    assert swap["all_delta_sets_reindexed"]
    assert not sign["raw_k_in_source_product_domain"]
    return {
        "epistemic_status": "PROVED",
        "positive_scaling_law_available": True,
        "finite_swap_reindexing_available": True,
        "simultaneous_sign_law_available": False,
        "complete_raw_to_E_lift_available": False,
        "packet_cocycle_test_performed": False,
        "reason": "The required sign step is outside the frozen source product domain; composing scaling or a finite index relabeling around that missing step would be an unproved extension.",
    }


def run() -> dict[str, object]:
    scaling = positive_scaling_audit()
    swap = swap_reindexing_audit()
    sign = signed_representative_domain_audit()
    lift = legal_lift_audit()
    return {
        "schema": "sic-stark-cycle-218-signed-period-cover-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Within the frozen S--S product-definition domain, positive common scaling is exact and the finite Delta index sets admit the specified swap reindexing. But the Cycle-217 raw endpoint has k=-24, outside that domain, and the source formulas audited here provide no simultaneous-sign Gamma_M law. Hence these partial laws cannot be composed into a legal raw-to-E lift. This does not disprove a newly constructed signed-k extension, another source theorem, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "positive_scaling_audit": scaling,
        "swap_reindexing_audit": swap,
        "signed_representative_domain_audit": sign,
        "legal_lift_audit": lift,
        "gate_outcome": {
            "positive_576_scaling": "PROVED_WITHIN_SOURCE_DOMAIN",
            "finite_swap_index_relabeling": "PROVED_PARTIAL",
            "source_defined_simultaneous_sign_bridge": "NOT_AVAILABLE",
            "complete_raw_to_E_cover_lift": "NOT_AVAILABLE",
            "remaining_design_problem": "Construct and validate a signed-k rarefied-Gamma extension compatible with the product, reflection, and factorization formulas before reattempting the affine E lift.",
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
