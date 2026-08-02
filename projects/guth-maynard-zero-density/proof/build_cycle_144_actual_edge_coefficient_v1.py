#!/usr/bin/env python3
"""Seal Cycle 144 coefficient-faithful edge interface."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-144-actual-edge-coefficient-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-144-actual-edge-coefficient-preregistration-v1.md", "2b2118ec1a57ec910cabe22bbf0c686712252db4d1a15d4782bed68e178964d6"),
    "document": (ROOT / "docs/cycle-144-actual-edge-coefficient-v1.md", "35300d3e9811ace5af209f2b777292700a76557ceedfde8b7b3923984450a4a3"),
    "conventions": (ROOT / "conventions/actual_edge_coefficient_v1.py", "219046b5f01a0f48387ba98059a83b1ec2493ba304561a0da21d5ac06f7fa0c3"),
    "tests": (ROOT / "tests/test_cycle_144_actual_edge_coefficient_v1.py", "674ba000e2e07dbf2165c6c45f59ff7569942a9447302aaf37c5e20da2657d94"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle123": (ROOT / "artifacts/cycle-123-joint-radial-alias-v1.json", "e700c21a422413abb6f35882d8d5a67b4ae4095b23c157da6397417b08f4da79"),
    "cycle124": (ROOT / "artifacts/cycle-124-bilinear-self-duality-v1.json", "d057acb6807a58be37e42a5bb1869de62e33e873dd0aebdb6033aad6b2e1f2b8"),
    "cycle132": (ROOT / "artifacts/cycle-132-unimodular-endpoint-lift-v1.json", "aeab0475962728918ab08c2b78e87dcef4bed7840c57e376557bcdcdfb434cee"),
    "cycle143": (ROOT / "artifacts/cycle-143-sparse-path-fourier-v1.json", "364083fc16cfa7591afd69dd3df6c83c292f4efcea9f1077db3531ee61330937"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle123"][0], "SEALED_JOINT_ALIAS_AMPLITUDE_PHASE_FACTORIZATION_BILINEAR_OPEN")
    validate_prior(INPUTS["cycle124"][0], "SEALED_TENSOR_CAUCHY_NORM_SELF_DUAL_COLLISION_INVERSE_OPEN")
    validate_prior(INPUTS["cycle132"][0], "SEALED_ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN")
    validate_prior(INPUTS["cycle143"][0], "SEALED_SPARSE_PATH_NORM_SELF_DUAL_SIGNED_MOMENT_HIERARCHY_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="actual_edge_coefficient_v1")
    module = __import__("conventions.actual_edge_coefficient_v1", fromlist=["correlation_weights"])
    weights = module.correlation_weights((1 + 2j,), (3 - 1j,))
    require(weights == ((3 - 1j) * (1 - 2j),), "oriented correlation coefficient")
    require("no sealed coefficient-preserving" in theorem["typed_boundary"], "typed interface gap")
    require("M_m(d;ell)" in theorem["cycle143_correction"], "frequency-dependent moments")
    require("not a signed-moment" in theorem["boundary"], "claim boundary")
    return {
        "artifact_id": "cycle-144-actual-edge-coefficient-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COEFFICIENT_PRESERVING_WEIGHTED_COLLISION_INVERSE_OPEN",
        "claim_boundary": (
            "This artifact proves the correlation-coefficient type and identifies "
            "a missing coefficient-preserving interface between the alias operator "
            "and the arithmetic collision inverse. It corrects the description of "
            "Cycle 143's scalar hierarchy but proves no signed-moment estimate, "
            "paired norm, endpoint, complete moment, density, or intervals."
        ),
        "runtime": check_runtime("Cycle 144"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "actual_edge_coefficient_theorem": {"epistemic_status": "PROVED", **theorem},
        "correction": {
            "epistemic_status": "PROVED",
            "affected_claim": "Cycle 143 actual signed moment hierarchy",
            "replacement": (
                "the scalar hierarchy is conditional on a frequency-independent "
                "coefficient pushforward; the actual formal hierarchy is ell-dependent"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "transport the complex frequency-dependent edge measure through a "
                "weighted collision inverse, or prove a controlled scalar factorization"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_144_actual_edge_coefficient_v1.py --write",
            "check_command": "python3 proof/build_cycle_144_actual_edge_coefficient_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_144_actual_edge_coefficient_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 144 sealer", output=OUTPUT, payload_factory=seal))
