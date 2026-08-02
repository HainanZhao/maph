#!/usr/bin/env python3
"""Seal the exact Cycle-163 fixed-full-ray selector result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-163-spectral-ray-interface-v1.json"

FROZEN_INPUTS = {
    "project_instructions": (
        ROOT / "AGENTS.md",
        "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2",
    ),
    "preregistration": (
        ROOT / "docs/cycle-163-spectral-ray-interface-preregistration-v1.md",
        "c09fd5abdab877553efd3456e5ee1db09fb6d470feca24546aaf0eb27e202f46",
    ),
    "decision_record": (
        ROOT / "docs/cycle-163-spectral-ray-interface-v1.md",
        "24ab14474a2104d1ad85ddc1f817ec28d8caa54c2ba1e1d397872c67080f9c21",
    ),
    "selector_replay": (
        ROOT / "proof/verify_cycle_163_fixed_full_ray_selector.py",
        "4a5f07439f7e47545fc3cb4f5b5d43228f8f045ab0a97bc321140d9143f30c3b",
    ),
    "selector_output": (
        ROOT / "discovery/cycle-163-fixed-full-ray-selector-prototype-v1.json",
        "bc20b72a5ef5a1db5711c2caac9687db09d3d7158c8651a502ad2befaf587dd4",
    ),
    "test": (
        ROOT / "tests/test_cycle_163_fixed_full_ray_selector.py",
        "50f6e87938cf689e35e0f61fa72d0884fb38e736851bcff95a75dda7db481e4a",
    ),
    "sealing_scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 163 selector seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads(
        (ROOT / "discovery/cycle-163-fixed-full-ray-selector-prototype-v1.json").read_text()
    )
    summary = prototype["summary"]
    require(summary["rows_checked"] == 36, "wrong row count")
    require(summary["eligible_rows"] == 18, "eligible-row count changed")
    require(summary["ineligible_rows"] == 18, "ineligible-row count changed")
    require(not summary["fixed_full_ray_total"], "selector totality unexpectedly passed")
    require(
        summary["orientation_anchors"]["3,5"] == {"eligible": True, "frozen_ray_log": 1},
        "first orientation anchor changed",
    )
    require(
        summary["orientation_anchors"]["3,4"] == {"eligible": True, "frozen_ray_log": 2},
        "second orientation anchor changed",
    )
    require(
        prototype["gate_outcome"]["fixed_full_ray_direct_selector"]
        == "FALSIFIED_BY_NONCOPRIME_ROWS",
        "selector outcome changed",
    )
    return {
        "artifact_id": "cycle-163-spectral-ray-interface-v1",
        "cycle": 163,
        "budget_ordinal": "B001",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_FULL_RAY_SELECTOR_FALSIFIED",
        "claim_boundary": (
            "This exact finite result falsifies only the positive-lift, "
            "fixed-full-modulus direct-selector class. It proves no "
            "logarithm, finite part, AFK-cocycle identification, "
            "ray-monoid lift, Stark identity, fusion theorem, or "
            "dimension-six TCC identity."
        ),
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "Exactly 18 of 36 frozen characteristics are eligible for "
                "a fixed (6)infinity_2 ray label; fixed-full-ray totality "
                "therefore fails."
            ),
            "orientation_anchors": {
                "(3,5)": "eligible with frozen ray log 1",
                "(3,4)": "eligible with frozen ray log 2",
            },
        },
        "gate_outcome": {
            "d6_interface": "ACTIVE_NEW_ENGINE_REQUIRED",
            "falsified_construction_class": "positive_lift_fixed_full_ray_direct_selector",
            "next_authorized_action": (
                "Cycle 164/B002: preregister an orientation-preserving "
                "characteristic-dependent conductor-lowering/ray-monoid "
                "state space with an explicit common primitive-target map."
            ),
            "disallowed_pseudo_progress": [
                "treating the 18 noncoprime rows as a global interface or TCC no-go",
                "using lowered absolute values without an oriented common-target map",
                "returning to undefined packet numerics",
            ],
        },
        "exact_prototype": {
            "rows_checked": summary["rows_checked"],
            "eligible_rows": summary["eligible_rows"],
            "ineligible_rows": summary["ineligible_rows"],
            "ineligible_characteristics": summary["ineligible_characteristics"],
            "fixed_full_ray_total": summary["fixed_full_ray_total"],
            "orientation_anchors": summary["orientation_anchors"],
            "source_output": "discovery/cycle-163-fixed-full-ray-selector-prototype-v1.json",
        },
        "preregistration_preflight": {
            "cycle": 163,
            "manifest_sha256": sha256(
                ROOT / "docs/cycle-163-spectral-ray-interface-preregistration-v1.md"
            ),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "mentor_checkpoint": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal Cycle 163/B001 as an exact obstruction to the fixed "
                "positive full-ray selector; authorize the conductor-lowering/ray-monoid engine."
            ),
            "known_flaw": (
                "The result does not exclude characteristic-dependent lifts, "
                "conductor changes, or an analytic coefficient-to-cocycle interface."
            ),
            "falsifier": (
                "Any sealed claim extending the 18 noncoprime rows beyond "
                "the preregistered positive-lift construction class."
            ),
            "next_action": (
                "Preregister a convention-pinned conductor-lowering state "
                "space and invariant preserving both orientation anchors."
            ),
            "resolution": "ADOPTED",
        },
        "frozen_hashes": frozen_hashes,
        "replay": {
            "preflight_command": (
                "research prereg check "
                "docs/cycle-163-spectral-ray-interface-preregistration-v1.md "
                "--expected-cycle 163 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_163_fixed_full_ray_selector.py "
                "--output discovery/cycle-163-fixed-full-ray-selector-prototype-v1.json"
            ),
            "check_command": "python3 proof/build_cycle_163_spectral_ray_interface_v1.py --check",
            "test_command": "python3 -m unittest tests.test_cycle_163_fixed_full_ray_selector -v",
            "write_command": "python3 proof/build_cycle_163_spectral_ray_interface_v1.py --write",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_163_spectral_ray_interface_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            description=__doc__,
            output=OUTPUT,
            payload_factory=payload,
        )
    )
