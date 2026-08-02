#!/usr/bin/env python3
"""Seal Cycle 115 local weak-turnover trichotomy."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-115-local-turnover-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-115-local-turnover-preregistration-v1.md", "7f78ce52ebc6b8081e41ea63b84edcce8e7a2d59adce10dc1dbe10f15adf1298"),
    "document": (ROOT / "docs/cycle-115-local-turnover-v1.md", "7dc1556f1594f4a62de7e2a1d8c178ab011b6d323307dd2ada8676cfb55a29d4"),
    "conventions": (ROOT / "conventions/local_turnover_v1.py", "8509a6da2a94c01227fc26e1e9ffe9037c1c472afb8cdf2e3448837dea3949c2"),
    "tests": (ROOT / "tests/test_cycle_115_local_turnover_v1.py", "4e48cc347dacba9e6a5d3402c39e8cccb4d8c5f102d259f59d8b745337c175af"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle97": (ROOT / "artifacts/cycle-97-projective-algebraic-root-v1.json", "5af4394e8a8f48b70cff4f1b32e9a213640df499f273f701bc0ffe5ffd0d2644"),
    "cycle114": (ROOT / "artifacts/cycle-114-coupled-anchor-scale-v1.json", "bec19431e36affe22633ce2095db8537205b5dcd2525e29abb7a0ab79271d596"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle97"][0], "SEALED_ALGEBRAIC_ROOT_OR_NEAR_DOUBLE_INVERSE_EFFECTIVE_SEPARATION_OPEN")
    validate_prior(INPUTS["cycle114"][0], "SEALED_ALL_SMOOTH_STRONG_CORES_WEIGHTED_X13_30_WEAK_SIMPLE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="local_turnover_v1")
    require("ell_x^2" in theorem["transition_floor"], "transition floor")
    require("S2/D^2" in theorem["entropy_specialization"], "entropy scale")
    require("tolerance" in theorem["boundary"], "remaining comparison")
    return {
        "artifact_id": "cycle-115-local-turnover-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_LOCAL_SIMPLE_OR_CRITICAL_BELOW_S2_D2_TOLERANCE_COMPARISON_OPEN",
        "claim_boundary": (
            "This artifact replaces the global weak-turnover ledger by a local Newton/critical "
            "trichotomy. Below an explicit constant times S2/D^2, no weak middle remains. "
            "The actual stationary tolerance comparison and simple-root average remain open."
        ),
        "runtime": check_runtime("Cycle 115"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "local_turnover_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "compare the exact stationary tolerance to c_abs*S2/D^2 and aggregate the simple-root output",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_115_local_turnover_v1.py --write",
            "check_command": "python3 proof/build_cycle_115_local_turnover_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_115_local_turnover_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 115 sealer", output=OUTPUT, payload_factory=seal))
