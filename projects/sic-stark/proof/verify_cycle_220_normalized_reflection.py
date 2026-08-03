#!/usr/bin/env python3
"""Exact normalized-reflection reduction audit for Cycle 220/B057."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_cycle_219_signed_k_extension import coordinate_sign_census


def reflection_reduction_audit() -> dict[str, object]:
    """Use the source normalized reflection before comparing coordinates.

    For Q_cd=c*omega1+d*omega2, equation (33) gives
    Gamma_M(Q_cd-x, r-1-y)^(-1)=Gamma_M(x,y).  Substitution
    x=a*mu and y=b*m reduces every frozen reflection-plus-sign candidate to
    exactly the diagonal candidate already enumerated in Cycle 219.  This is
    an identity only wherever that source meromorphic reflection is defined;
    it never defines a negative-k product by itself.
    """
    return {
        "epistemic_status": "PROVED",
        "source_identity": "Gamma_M(Q-x,r-1-y)^(-1)=Gamma_M(x,y)",
        "substitution": {"x": "a*mu", "y": "b*m", "Q": "c*omega1+d*omega2"},
        "candidate_before_reduction": "H_abcd=Gamma_M(Q_cd-a*mu,r-1-b*m;c*omega1,d*omega2)^(-1)",
        "candidate_after_reduction": "H_abcd=Gamma_M(a*mu,b*m;c*omega1,d*omega2)",
        "reduction_target": "Cycle-219 frozen diagonal sign-lift family",
        "source_scope": "The equality is used only as the published normalized reflection identity for a positive-k M_+ and its meromorphic period domain; it does not assert that the negative-k raw representative is source-defined.",
    }


def reflected_coordinate_census() -> dict[str, object]:
    """Transport the exact Cycle-219 exhaustive census through reflection."""
    diagonal = coordinate_sign_census()
    assert diagonal["candidate_count"] == 16
    assert diagonal["survivor_count"] == 0
    return {
        "epistemic_status": "PROVED",
        "candidate_count": diagonal["candidate_count"],
        "survivor_count": diagonal["survivor_count"],
        "tau_and_u_candidates": diagonal["tau_and_u_candidates"],
        "symbolic_conflict": diagonal["symbolic_conflict"],
        "conclusion": "Because normalized reflection reduces each H_abcd exactly to its diagonal counterpart, no reflection-plus-sign candidate preserves raw tau, u, and tilde-u simultaneously.",
    }


def downstream_axiom_audit() -> dict[str, object]:
    census = reflected_coordinate_census()
    assert census["survivor_count"] == 0
    return {
        "epistemic_status": "PROVED",
        "involutivity_tested": False,
        "reflection_tested": True,
        "shift_tested": False,
        "factorization_tested": False,
        "reason": "Reflection itself collapses to the already falsified diagonal family; no candidate enters the raw product-coordinate state on which the remaining axioms could define a signed-k extension.",
    }


def run() -> dict[str, object]:
    reduction = reflection_reduction_audit()
    census = reflected_coordinate_census()
    axioms = downstream_axiom_audit()
    assert census["survivor_count"] == 0
    return {
        "schema": "sic-stark-cycle-220-normalized-reflection-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Within the preregistered family consisting only of the published normalized reflection composed with 16 diagonal sign lifts, source reflection reduces every candidate exactly to the sealed Cycle-219 diagonal family. Its exhaustive zero-survivor coordinate census therefore excludes this reflection-plus-sign construction. This does not exclude a candidate with a new non-reflection correction factor, theta/Pochhammer term, additive shift, period swap, label redefinition, new source theorem, packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "reflection_reduction_audit": reduction,
        "reflected_coordinate_census": census,
        "downstream_axiom_audit": axioms,
        "gate_outcome": {
            "normalized_reflection_plus_sign_extension": "FALSIFIED_WITHIN_FROZEN_FAMILY",
            "remaining_design_problem": "Construct a genuinely new non-diagonal correction, beginning with an explicit theta/Pochhammer factor or source theorem, and prove all product and functional-identity compatibility before any affine E comparison.",
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
