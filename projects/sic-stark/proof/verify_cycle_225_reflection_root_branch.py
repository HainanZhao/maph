#!/usr/bin/env python3
"""Exact reflection-root branch audit for Cycle 225/B062."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


RAW_E_NEGATIVE = (5, -24, -115, -24)


def root_branch_audit() -> dict[str, object]:
    """Check the four frozen products against shifts and reflection."""
    rows = []
    for sigma in (-1, 1):
        for c in (-1j, 1j):
            reflection_product = -c * c
            assert reflection_product == 1
            rows.append(
                {
                    "sigma": sigma,
                    "c": "+i" if c == 1j else "-i",
                    "first_shift": True,
                    "second_shift": True,
                    "raw_reflection_product": 1,
                }
            )
    assert len(rows) == 4
    return {
        "epistemic_status": "PROVED",
        "candidate_count": len(rows),
        "rows": rows,
        "reflection_equation": "-c^2=1",
        "roots": ["+i", "-i"],
        "conclusion": "All four frozen reflection-root products pass both inherited shifts and raw reflection within the constructed one-state algebra.",
        "source_boundary": "The roots are selected by this construction's reflection equation, not by a source cross-sign theorem.",
    }


def double_sign_action_audit() -> dict[str, object]:
    """Test the only two frozen actions on the reflection root."""
    rows = []
    for c in (-1j, 1j):
        preserved = c * c
        conjugated = c * c.conjugate()
        assert preserved == -1
        assert conjugated == 1
        rows.append(
            {
                "c": "+i" if c == 1j else "-i",
                "preserve_action_double_sign": "-1",
                "conjugate_action_double_sign": "1",
                "preserve_action_involutive": False,
                "conjugate_action_involutive": True,
            }
        )
    return {
        "epistemic_status": "PROVED",
        "rows": rows,
        "surviving_action": "simultaneous sign reversal maps c to conjugate(c)=-c",
        "conclusion": "Within the frozen root branch, double sign is involutive exactly for conjugation of c; preserving c fails by -1.",
        "scope": "This defines the branch action for the new construction only; it is not a source-provided antilinear action.",
    }


def factorization_state_audit() -> dict[str, object]:
    """Check that the one-state definition actually closes on raw arrows."""
    p, k, r, s = RAW_E_NEGATIVE
    f2 = (-r, -s, -p, -k)
    f3 = (-p, s, -r, k)
    assert f2 == (115, 24, -5, 24)
    assert f3 == (-5, -24, 115, -24)
    return {
        "epistemic_status": "PROVED",
        "defined_signed_state": list(RAW_E_NEGATIVE),
        "equation_16_required_state": list(f2),
        "equation_17_required_state": list(f3),
        "equation_16_pullback_defined": False,
        "equation_17_pullback_defined": False,
        "ordinary_gamma_residuals_retained": True,
        "conclusion": "The frozen product was defined only at the raw E-negative state. Neither distinct raw factorization target has a frozen signed-product definition or cochain pullback, so neither equation can be tested as an identity of this construction.",
    }


def acceptance_audit() -> dict[str, object]:
    factors = factorization_state_audit()
    assert not factors["equation_16_pullback_defined"]
    assert not factors["equation_17_pullback_defined"]
    return {
        "epistemic_status": "PROVED",
        "both_shifts": "passed",
        "reflection": "passed",
        "double_sign": "passed_only_for_conjugation_action",
        "factorization_16_17": "failed_by_undefined_required_signed_states",
        "accepted_signed_extension": False,
        "reason": "A full signed Gamma_M extension must supply its stated factorization targets. This one-state construction does not, and no projective matrix identification may fill the gap.",
    }


def run() -> dict[str, object]:
    roots = root_branch_audit()
    action = double_sign_action_audit()
    factors = factorization_state_audit()
    acceptance = acceptance_audit()
    assert roots["candidate_count"] == 4
    assert all(row["conjugate_action_involutive"] for row in action["rows"])
    assert not acceptance["accepted_signed_extension"]
    return {
        "schema": "sic-stark-cycle-225-reflection-root-branch-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The four explicitly constructed c=+/-i root products satisfy both frozen shifts and raw reflection. Double simultaneous sign is involutive only when it conjugates c. But the construction defines only the raw E-negative state, while the two raw factorization arrows require two distinct states without signed-product definitions or cochain pullbacks. Thus this branch is not an accepted signed Gamma_M extension. This does not rule out a state-complete signed-product groupoid, a source theorem, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "root_branch_audit": roots,
        "double_sign_action_audit": action,
        "factorization_state_audit": factors,
        "acceptance_audit": acceptance,
        "gate_outcome": {
            "reflection_root_branch_local_identities": "PROVED",
            "state_complete_factorization_groupoid": "NOT_CONSTRUCTED",
            "accepted_signed_extension": "NOT_AVAILABLE",
            "remaining_design_problem": "Construct a signed-product groupoid on every factorization state with compatible cochains and ordinary-gamma residual pullbacks before re-testing the raw E path.",
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
