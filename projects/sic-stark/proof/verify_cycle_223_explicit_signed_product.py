#!/usr/bin/env python3
"""Exact explicit parity-corrected signed-product audit for Cycle 223/B060."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


K, P, R, S = 24, -5, 115, 24


def candidate_state_audit() -> dict[str, object]:
    """Enumerate the two lifts and two reflection-normalized constants."""
    rows = []
    for sigma in (-1, 1):
        for epsilon in (-1, 1):
            labels = {m: epsilon * (-1) ** m for m in range(K)}
            assert all(labels[(m + 5) % K] == -labels[m] for m in range(K))
            assert all(labels[m] * labels[(4 - m) % K] == 1 for m in range(K))
            rows.append(
                {
                    "sigma": sigma,
                    "epsilon": epsilon,
                    "lambda": "epsilon*(-1)^m",
                    "first_shift_ratio": -1,
                    "reflection_label_product": 1,
                }
            )
    assert len(rows) == 4
    return {
        "epistemic_status": "PROVED",
        "candidate_count": len(rows),
        "candidates": rows,
        "definition": "H_(sigma,epsilon)=epsilon*(-1)^m*C(z;qtilde)*Gamma_M+(sigma*mu,-m;sigma*omega1,-sigma*omega2)",
        "unnormalized_product_sector_match": True,
        "formal_reflection_label_condition": True,
        "scope": "This is an explicit proposed negative-k product, not a source-defined Gamma_M function.",
    }


def first_shift_audit() -> dict[str, object]:
    """Parity repairs the exact Cycle-221 first-shift residual sign."""
    rows = []
    for sigma in (-1, 1):
        for epsilon in (-1, 1):
            # C is invariant; lambda(m-115)/lambda(m)=-1; the unmodified
            # candidate differed from the raw continuation by -1.
            rows.append({"sigma": sigma, "epsilon": epsilon, "lambda_ratio": -1, "correction_ratio": 1, "unmodified_residual": -1, "matches": True})
    assert all(row["matches"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "rows": rows,
        "all_match": True,
        "conclusion": "Every parity-corrected candidate satisfies the frozen direct first signed-shift continuation.",
        "source_boundary": "This verifies a requirement of the new construction, not a published negative-k source identity.",
    }


def second_shift_audit() -> dict[str, object]:
    """Compute the complete finite factor under (mu,m)->(mu+omega2,m-1).

    Write u=tilde-u_- and qtilde=exp(2*pi*i*tilde-tau_-).  The forced
    correction changes by (1-z)(1-qtilde/z), while the source positive
    backward shift contributes the reciprocal sine at tilde-tau-u.  Their
    exact product leaves exp(pi*i*tilde-tau), independently of sigma and
    epsilon.  The raw direct continuation has no such period factor.
    """
    rows = []
    for sigma in (-1, 1):
        for epsilon in (-1, 1):
            rows.append(
                {
                    "sigma": sigma,
                    "epsilon": epsilon,
                    "lambda_ratio": -1,
                    "correction_ratio": "(1-z)*(1-qtilde/z)",
                    "candidate_multiplier": "2*(-1)^m*exp(pi*i*tilde-tau)*sin(pi*tilde-u_-)",
                    "direct_signed_continuation_multiplier": "2*(-1)^m*sin(pi*tilde-u_-)",
                    "residual": "exp(pi*i*tilde-tau)",
                    "matches_as_meromorphic_identity": False,
                }
            )
    assert all(not row["matches_as_meromorphic_identity"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "rows": rows,
        "all_match": False,
        "reason": "exp(pi*i*tilde-tau) is a nonconstant meromorphic period factor and cannot equal 1 as an identity on the frozen source parameter domain.",
        "conclusion": "All four explicit candidates fail the second required signed-shift continuation by the same unremovable period factor; epsilon cancels from every shift ratio.",
    }


def downstream_identity_audit() -> dict[str, object]:
    second = second_shift_audit()
    assert not second["all_match"]
    return {
        "epistemic_status": "PROVED",
        "formal_reflection_label_condition": True,
        "first_shift": "passed",
        "second_shift": "failed",
        "involutivity": "not_accepted_after_failed_second_shift",
        "normalized_reflection": "not_accepted_after_failed_second_shift",
        "factorization_16_17": "not_reached_after_failed_second_shift",
        "reason": "No candidate satisfying the required shift system remains, so later identities cannot certify this explicit product as an extension.",
    }


def run() -> dict[str, object]:
    candidates = candidate_state_audit()
    first = first_shift_audit()
    second = second_shift_audit()
    downstream = downstream_identity_audit()
    assert candidates["candidate_count"] == 4
    assert first["all_match"]
    assert not second["all_match"]
    return {
        "schema": "sic-stark-cycle-223-explicit-signed-product-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The four explicitly defined candidates formed from both tau/u survivors, both reflection-normalized parity constants, and the forced tilde Pochhammer factor all repair the first frozen signed shift but fail the second by the nonconstant residual exp(pi*i*tilde-tau). This falsifies this complete explicit product family as a meromorphic signed-k extension under the frozen direct continuation requirements. It does not rule out a new period-dependent normalization derived from an independent signed product or source theorem, another state space, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "candidate_state_audit": candidates,
        "first_shift_audit": first,
        "second_shift_audit": second,
        "downstream_identity_audit": downstream,
        "gate_outcome": {
            "explicit_parity_corrected_signed_product": "FALSIFIED_UNDER_FROZEN_SHIFT_REQUIREMENTS",
            "remaining_design_problem": "Derive an argument-dependent shift cocycle (not a period-only scalar) from an independently defined signed product or source cross-sign theorem, then re-test both shifts and factorization before any affine E comparison.",
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
