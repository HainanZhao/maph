#!/usr/bin/env python3
"""Seal Cycle 203/B040's ordinary inverse-normal-line obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_203_inverse_normal_line import run as line_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-203-b040-inverse-normal-line-v1.json"
INPUTS = {
    "prior_normal_target_weight": (
        ROOT / "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json",
        "09f860f92611a953538d7dcd32a1040be92e15e412ce712a01bc538287c1c426",
    ),
    "prior_two_scale_germ": (
        ROOT / "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
        "4a0e02ae9bc419add49a49ac0de88a2e33524a94fa5cfaed24e2d52139b03204",
    ),
    "prior_full_phase_poles": (
        ROOT / "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json",
        "97e0100205df7e0ea73e9b61ab8e6278a146afe05d3000300ae57788be2c253e",
    ),
    "prior_axis_geometry": (
        ROOT / "artifacts/cycle-196-b033-endpoint-contour-geometry-v1.json",
        "086d85549c39c385724c5f3709236b783e6c0ba568b758467b9c5e445774b26f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-203-b040-inverse-normal-line-preregistration-v1.md",
        "2c4f67eab67174136424c761175a9dc0c9b558fb907501556c465fb5d0e8833f",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_203_inverse_normal_line.py",
        "76a569b5812d64e13e3c0a2533442a5765c40fa2c0535026bdf60e1e9b0d9b71",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_203_inverse_normal_line.py",
        "ae256f9ea0158053ea262e1b4fa19df342796376d6e3ed6957fa364931f492a4",
    ),
    "prototype": (
        ROOT / "discovery/cycle-203-b040-inverse-normal-line-prototype-v1.json",
        "7bac748fc6ea8b7fbb14e9a89b7d6ac34f822f8535cd4766368b1cec05af9fee",
    ),
    "cycle202_replay": (
        ROOT / "proof/verify_cycle_202_normal_derivative_target_weight.py",
        "00da578ee6c67b1cbf67b8c8802804dd5af560bf29e67ba7aeb4d18b92c16116",
    ),
    "cycle199_pole_replay": (
        ROOT / "proof/verify_cycle_199_abel_pole_geometry.py",
        "b92e7d3512b289fb411ecbd4ff65d5ed0c5af9c242f5223f44bd08c947555e3d",
    ),
    "cycle196_axis_replay": (
        ROOT / "proof/verify_cycle_196_endpoint_contour_geometry.py",
        "aa8a98e94b19738040ae7ead70615b53c9e16a760fd67383b9d61de3a3107577",
    ),
    "two_base_axis": (
        ROOT / "scripts/dimension_six_two_base_lens.py",
        "72a4e0d9b577f661c89a84132f450c209f1f57a6131ba175b2a238f5bb197f79",
    ),
    "preregistration_validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 203 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = line_run()
    multiplier = result["a6_axis_multiplier"]
    rescaling = result["rescaling_symmetry"]
    line = result["normal_line_obstruction"]

    require(multiplier["mobius_derivative_at_beta"].endswith("beta^(-6)"), "A6 multiplier drift")
    require(multiplier["cross_ratio_coordinate"].endswith("=i*s"), "axis coordinate drift")
    require(rescaling["not_fixed_by_source_data"] == "a nonzero scale for s", "scale freedom drift")
    require(line["only_invariant_inverse_vector"] == "0", "line obstruction drift")
    require("not a nonzero element" in line["logarithmic_form_failure"], "logarithmic category drift")

    return {
        "artifact_id": "cycle-203-b040-inverse-normal-line-v1",
        "cycle": 203,
        "budget_ordinal": "B040",
        "epistemic_status": "PROVED",
        "status": "SEALED_ORDINARY_INTRINSIC_INVERSE_NORMAL_LINE_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "The declared A_6 axis data fixes an oriented ordinary normal "
                "line with contraction beta^(-6), but no nonzero inverse-line "
                "trivialization: positive coordinate rescaling preserves all "
                "source data and rescales every candidate."
            ),
        },
        "a6_axis_multiplier": multiplier,
        "rescaling_symmetry": rescaling,
        "normal_line_obstruction": line,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C203 as PROVED only for nonexistence of an intrinsic "
                "nonzero ordinary inverse-normal-line trivialization from the "
                "declared axis data."
            ),
            "known_flaw": (
                "The obstruction is category-dependent: ds/s is singular in the "
                "ordinary cotangent bundle but canonical in a logarithmic/b-"
                "cotangent compactification, and covariant targets remain open."
            ),
            "falsifier": (
                "Any A6 derivative, cross-ratio scaling, preservation-under-s_c, "
                "pulled-back-family, inverse-line transformation, or replay "
                "discrepancy."
            ),
            "next_action": (
                "Open B041 with a logarithmic normal-bundle engine: treat "
                "s*d/ds and ds/s as regular invariant b-geometric objects, then "
                "test whether the 36 weight-one packets define a canonical line-"
                "valued endpoint map and a flow-invariant fusion statement."
            ),
            "adopted": True,
            "reason": (
                "The ordinary-line claim is fully settled by exact scale symmetry, "
                "while the different logarithmic category remains explicitly open."
            ),
        },
        "preregistration_preflight": {
            "cycle": 203,
            "manifest_sha256": sha256(ROOT / "docs/cycle-203-b040-inverse-normal-line-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-203-b040-inverse-normal-line-preregistration-v1.md "
                "--expected-cycle 203 --allow-head-drift"
            ),
            "prototype_command": (
                "python3 proof/verify_cycle_203_inverse_normal_line.py "
                "--output discovery/cycle-203-b040-inverse-normal-line-prototype-v1.json"
            ),
            "test_command": "python3 -m unittest tests/test_cycle_203_inverse_normal_line.py",
            "write_command": "python3 proof/build_cycle_203_inverse_normal_line_v1.py --write",
            "check_command": "python3 proof/build_cycle_203_inverse_normal_line_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_203_inverse_normal_line_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
