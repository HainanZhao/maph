#!/usr/bin/env python3
"""Seal Cycle 111 correction of the k-stationary location."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-111-k-stationary-correction-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-111-k-stationary-correction-preregistration-v1.md", "5f06836e61d784fee39b9ec23b3149f22fd97bcd1920cb9181030303859a000c"),
    "document": (ROOT / "docs/cycle-111-k-stationary-correction-v1.md", "d9dec8d9318ee53b8716917f02572bed72da837405d9b0cd8c00a4bb30182b59"),
    "conventions": (ROOT / "conventions/k_stationary_correction_v1.py", "f337ae0f8124230a4dd0734a46e0ada951199b76d8b9297dcdbec7cbae9ac9d9"),
    "tests": (ROOT / "tests/test_cycle_111_k_stationary_correction_v1.py", "ff2dd11f77807222d754726689bae9b76ce3ed097460c9ea1c4500de06d020b6"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle81": (ROOT / "artifacts/cycle-81-exact-q-transform-v1.json", "0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4"),
    "cycle87": (ROOT / "artifacts/cycle-87-mellin-alias-atlas-v1.json", "68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca"),
    "cycle94": (ROOT / "artifacts/cycle-94-triple-b-entropy-v1.json", "9b6fc5021af3622821729f72966fcb15a4c9b74d0ef668d14ccc6f32349266a5"),
    "cycle108": (ROOT / "artifacts/cycle-108-triple-b-jacobian-v1.json", "c030327447462241e056c593bc799e7fec472d6663faf17d5f8a9dbab8424813"),
    "cycle109": (ROOT / "artifacts/cycle-109-uniform-triple-b-v1.json", "da481a16c7a9e027d53104282410e2bad73fcaf6157a9ea3fe61ffeb8d74f432"),
    "cycle110": (ROOT / "artifacts/cycle-110-perfect-power-split-sum-v1.json", "cfcedf8145cf6ef70fb88b1a722067460236dfb7a04061d75db325e093746c42"),
}


def seal() -> dict[str, Any]:
    expected = {
        "cycle81": "SEALED_EXACT_Q_TRANSFORM_LOG_RESONANCE_PROJECTOR_OPEN",
        "cycle87": "SEALED_MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN",
        "cycle94": "SEALED_CENTRAL_ANCHOR_DIFFERENCE_WEB_PROJECTIVE_ENTROPY_ALIASES_OPEN",
        "cycle108": "SEALED_LEADING_PERFECT_POWER_SCALE_SUMMABLE_PAYLOAD_REMAINDERS_OPEN",
        "cycle109": "SEALED_FULL_SMOOTH_PERFECT_POWER_SCALE_RAY_SUMMABLE",
        "cycle110": "SEALED_PERFECT_POWER_SPLIT_WEIGHT_UNIFORMLY_SUMMABLE",
    }
    for label, status in expected.items():
        validate_prior(INPUTS[label][0], status)
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="k_stationary_correction_v1")
    require(theorem["stationary_point"] == "k*=c*Delta/m", "correct stationary point")
    require("Cycle 108" in theorem["corrected_record"], "affected artifact")
    require("cutoff" in theorem["reaudit_required"], "containment scope")
    return {
        "artifact_id": "cycle-111-k-stationary-correction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CORRECTION_K_LOCATION_ENTROPY_AND_SCALE_LAWS_SURVIVE",
        "claim_boundary": (
            "This versioned correction replaces Cycle 108's k*=c*c0*Delta/m by "
            "k*=c*Delta/m. The anchor-bearing stationary value, Hessian amplitude, "
            "entropy, and scale laws survive; cutoff evaluations at the old point are withheld."
        ),
        "runtime": check_runtime("Cycle 111"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "correction": {"epistemic_status": "PROVED", **theorem},
        "affected_artifact": {
            "path": "artifacts/cycle-108-triple-b-jacobian-v1.json",
            "disposition": "immutable; stationary-point display superseded by this artifact",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "complete the corrected outer-prefactor, symbol-norm, and anchor normalization ledger",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_111_k_stationary_correction_v1.py --write",
            "check_command": "python3 proof/build_cycle_111_k_stationary_correction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_111_k_stationary_correction_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 111 correction sealer", output=OUTPUT, payload_factory=seal))
