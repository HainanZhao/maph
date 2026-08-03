#!/usr/bin/env python3
"""Exact source-normalization label-cocycle audit for Cycle 222/B059."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


K, P, R, S = 24, -5, 115, 24


def first_shift_coboundary_audit() -> dict[str, object]:
    """Solve lambda(m+5)=-lambda(m) on the complete mod-24 orbit."""
    values: dict[int, int] = {0: 1}  # lambda(m)/lambda(0), represented by +/-1.
    current = 0
    for _ in range(K - 1):
        nxt = (current + 5) % K
        values[nxt] = -values[current]
        current = nxt
    assert len(values) == K
    assert (current + 5) % K == 0
    assert -values[current] == values[0]
    assert all(values[(m + 5) % K] == -values[m] for m in range(K))
    closed_form = {m: (-1) ** m for m in range(K)}
    assert values == closed_form
    return {
        "epistemic_status": "PROVED",
        "step": 5,
        "orbit_size": K,
        "normalized_solution": {str(m): values[m] for m in range(K)},
        "solution_torsor": "lambda(m)=lambda(0)*(-1)^m, with lambda(0) an arbitrary nonzero root of unity before reflection normalization",
        "conclusion": "The first-shift defect has a one-dimensional finite label-cocycle torsor; it is not inconsistent and it is not yet source-selected.",
    }


def formal_reflection_constraint_audit() -> dict[str, object]:
    """Check the natural raw label involution without treating it as source law."""
    normalized = {m: (-1) ** m for m in range(K)}
    involution = {m: ((-R - 1 - m) % K) for m in range(K)}
    assert all(involution[involution[m]] == m for m in range(K))
    # -R-1 = -116 = 4 mod 24, so the normalized solution is reflection-even.
    assert all(normalized[m] * normalized[involution[m]] == 1 for m in range(K))
    return {
        "epistemic_status": "PROVED",
        "raw_label_involution": "m -> 4-m (mod 24)",
        "normalized_cocycle_product": "lambda(m)*lambda(4-m)=1",
        "compatibility": True,
        "scope": "This is a formal compatibility condition for a proposed signed continuation. It is not a source-provided reflection law at k=-24.",
    }


def source_z_phase_audit() -> dict[str, object]:
    """Extract exactly what positive-k source normalization does and does not say."""
    numerator = (1 - S) * K - P
    assert numerator == -547
    # Equation (34): xi(m)=exp(pi*i*numerator*(K+2m-R+1)/2).
    # For this tuple its exponent is -547*(m-45), hence xi(m)=(-1)^(m+1).
    xi = {m: (-1) ** (m + 1) for m in range(K)}
    normalized = {m: (-1) ** m for m in range(K)}
    assert all(normalized[m] == -xi[m] for m in range(K))
    return {
        "epistemic_status": "PROVED",
        "source_matrix": {"p": P, "k": K, "r": R, "s": S},
        "z_quadratic_phase_coefficient": "((1-s)k-p)/(2k)=-547/48",
        "source_quasiperiodicity": "Gamma_M(mu,m+24)=xi(m)*Gamma_M(mu,m), xi(m)=(-1)^(m+1)",
        "relation_to_normalized_cocycle": "lambda(m)/lambda(0)=(-1)^m=-xi(m)",
        "cross_sign_relation_supplied": False,
        "selection_conclusion": "Positive-k Z(m) exhibits the same parity character but supplies no identity relating it to a multiplier at the negative-k raw representative; it therefore does not select lambda(0) or license adjoining lambda across the sign boundary.",
    }


def source_bridge_audit() -> dict[str, object]:
    """Keep factorization and product-domain scope distinct from phase algebra."""
    return {
        "epistemic_status": "PROVED",
        "negative_k_product_defined_by_source": False,
        "source_defined_Z_minus": False,
        "factorization_lambda_pullback_available": False,
        "evidence": [
            "Cycle 218: the raw k=-24 representative lies outside source product definitions.",
            "Cycle 217: the raw factorization word carries a swapped/scaled period pair and fixed label, not the E state; matrix-only canonicalization is not a source Gamma_M arrow.",
        ],
        "conclusion": "Neither positive-domain Z phases nor the cited factorization arrows provide the missing inter-representative map needed to select or test the cocycle as a signed-k normalization.",
    }


def run() -> dict[str, object]:
    coboundary = first_shift_coboundary_audit()
    reflection = formal_reflection_constraint_audit()
    z_phase = source_z_phase_audit()
    bridge = source_bridge_audit()
    assert coboundary["orbit_size"] == K
    assert reflection["compatibility"]
    assert not z_phase["cross_sign_relation_supplied"]
    assert not bridge["factorization_lambda_pullback_available"]
    return {
        "schema": "sic-stark-cycle-222-z-label-cocycle-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The first-shift repair equation has the exact mod-24 torsor lambda(m)=lambda(0)(-1)^m, and its normalized parity representative is formally compatible with the proposed raw reflection involution. Source positive-k Z(m) has the related quasiperiodic parity but supplies no cross-sign identity, no Z_-, and no factorization pullback selecting lambda(0) or defining a signed-k normalization. This does not rule out an independently constructed signed product or a new source theorem, and proves no Gamma_M extension, packet cocycle, AFK covariance, fusion, Stark, or TCC statement.",
        "first_shift_coboundary_audit": coboundary,
        "formal_reflection_constraint_audit": reflection,
        "source_z_phase_audit": z_phase,
        "source_bridge_audit": bridge,
        "gate_outcome": {
            "abstract_mod24_label_cocycle": "PROVED_UNDERDETERMINED_TORSOR",
            "source_selected_signed_normalization": "NOT_AVAILABLE",
            "remaining_design_problem": "Construct an independent signed product or prove a new source cross-sign theorem that supplies Z_- and factorization pullbacks, then test the explicit parity cocycle without fitting.",
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
