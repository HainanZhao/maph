#!/usr/bin/env python3
"""Seal Cycle 105 perfect-power ray compiler."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import (
    check_runtime,
    freeze_inputs,
    load_record,
    require,
    run_cli,
    sha256,
    validate_prior,
)


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-105-powered-ray-compiler-v1.json"
INPUTS = {
    "discovery_candidate": (ROOT / "discovery/cycle-105-powered-ray-candidate-v1.md", "6ab604537243be099a7581474a7e97ed8a93f80b1414be31bbeb4b926cd688d4"),
    "preregistration": (ROOT / "docs/cycle-105-powered-ray-preregistration-v1.md", "80ca7e355e6cf80d6afcccd8459870746704f727bc9ec7c6809d59ec976bb026"),
    "document": (ROOT / "docs/cycle-105-powered-ray-compiler-v1.md", "0a35f1c1e1f356c19c2fe756185465b4c72400b90607f140801fe29107862998"),
    "conventions": (ROOT / "conventions/powered_ray_compiler_v1.py", "83cd7576f495fb8b40506810c24fb33c33f1a099ee4685d35661ef9e76374484"),
    "tests": (ROOT / "tests/test_cycle_105_powered_ray_compiler_v1.py", "5ed236e4bee8a437be094eedb9345f23cd0a614e4a803363fd90f89f1310d84e"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle104": (ROOT / "artifacts/cycle-104-radical-alias-separation-v1.json", "be9acdb96e8d8708ccdc1625e273f9fd092ad505125b058f6162ceae0715ed5b"),
}


def seal() -> dict[str, Any]:
    validate_prior(
        INPUTS["cycle104"][0],
        "SEALED_SINGLE_RADICAL_RATIONAL_CLASSIFICATION_AND_NORM_SECTOR",
    )
    theorem = load_record(
        root=ROOT,
        path=INPUTS["conventions"][0],
        module_name="powered_ray_compiler_v1",
    )
    require("w=h*d" in theorem["powered_ray"], "powered ray")
    require("delta/(d*min" in theorem["root_error"], "root error")
    require("missing exponents" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-105-powered-ray-compiler-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PERFECT_POWER_ALIAS_TO_ANCHORED_POWERED_RAY",
        "claim_boundary": (
            "This artifact compiles perfect-power aliases to anchored powered rays with "
            "a root-error and exponent budget. It neither fills missing exponents nor "
            "produces a realized packet seed, complete moment, density, or interval gain."
        ),
        "runtime": check_runtime("Cycle 105"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {"epistemic_status": "PROVED", "cycle104_role": "classify rational aliases as perfect-power labels"},
        "powered_ray_theorem": {"epistemic_status": "PROVED", **theorem},
        "e16_interface": {
            "epistemic_status": "PROVED",
            "statement": "repeated bases retain exact exponent set, arithmetic mode multiples, geometric labels, phase error, and payloads",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "turn repeated powered rays into realized packet seeds and pack singleton/large-degree cores",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_105_powered_ray_compiler_v1.py --write",
            "check_command": "python3 proof/build_cycle_105_powered_ray_compiler_v1.py --check",
            "test_command": (
                "python3 -m unittest tests/test_cycle_105_powered_ray_compiler_v1.py "
                "tests/test_cycle_seal_v1.py"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 105 sealer", output=OUTPUT, payload_factory=seal))
