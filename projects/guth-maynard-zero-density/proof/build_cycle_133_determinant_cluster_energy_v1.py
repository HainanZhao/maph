#!/usr/bin/env python3
"""Seal Cycle 133 determinant-cluster energy compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-133-determinant-cluster-energy-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-133-determinant-cluster-energy-preregistration-v1.md", "71520f458ec5e9d24598fef0203858a73f5e4496c382485bfe0da6b867ef0284"),
    "document": (ROOT / "docs/cycle-133-determinant-cluster-energy-v1.md", "e4c70a61eb8c2eb966005f93a454375a279a8e7e3080298054eda55b7594447e"),
    "conventions": (ROOT / "conventions/determinant_cluster_energy_v1.py", "9d7ec8efbf61de098dc7ba779edac35c4f982d33e98f5c3c9181771bedfdeb88"),
    "tests": (ROOT / "tests/test_cycle_133_determinant_cluster_energy_v1.py", "50d4d5c8e43ca078b3d7fca1fd69431b538b7d61003af00abcb942e7814e6040"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle125": (ROOT / "artifacts/cycle-125-freiman-ray-web-v1.json", "28112cb9c4e676719d1637b5ca650c49917b28ddcd2f43f04f93b54288802785"),
    "cycle126": (ROOT / "artifacts/cycle-126-freiman-recurrence-v1.json", "c228988b1549f129522a68f5b10698768ae3581b367166a9253048b67aeb92e5"),
    "cycle132": (ROOT / "artifacts/cycle-132-unimodular-endpoint-lift-v1.json", "aeab0475962728918ab08c2b78e87dcef4bed7840c57e376557bcdcdfb434cee"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle125"][0], "SEALED_HIGH_MULTIPLICITY_FREIMAN_WEB_LOW_MULTIPLICITY_SEED_GATE_OPEN")
    validate_prior(INPUTS["cycle126"][0], "SEALED_COMMON_RATIONAL_MULTIPLIER_CHAIN_DEPTH_ANCHOR_OPEN")
    validate_prior(INPUTS["cycle132"][0], "SEALED_ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="determinant_cluster_energy_v1")
    module = __import__("conventions.determinant_cluster_energy_v1", fromlist=["energy_ledger"])
    left = module.energy_ledger(Fraction(16, 25), Fraction(0))
    require(left["extension_beyond_hs"] == Fraction(79, 900), "minimum exact-web extension")
    require(left["nonexact_width"] == Fraction(9, 100), "left nonexact width")
    edge = module.energy_ledger(Fraction(7, 10), Fraction(3, 40))
    require(edge["nonexact_width"] == 0, "maximal-multiplicity width")
    require("do not force" in theorem["missing_invariant"], "missing invariant boundary")
    return {
        "artifact_id": "cycle-133-determinant-cluster-energy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EXACT_DETERMINANT_FREIMAN_SUBRANGE_TRANSITION_CONCENTRATION_OPEN",
        "claim_boundary": (
            "This artifact proves exact multiplicative energy only for tau>3rho "
            "and identifies an integral transition cocycle. It proves no transition "
            "concentration, recurrence seed, endpoint or lower-moment closure, density, "
            "or prime intervals."
        ),
        "runtime": check_runtime("Cycle 133"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "determinant_cluster_theorem": {"epistemic_status": "PROVED", **theorem},
        "lower_endpoint_ledger": {
            "epistemic_status": "PROVED",
            "exact_ceiling": str(left["exact_ceiling"]),
            "extension_beyond_hs": str(left["extension_beyond_hs"]),
            "nonexact_width": str(left["nonexact_width"]),
            "threshold_energy_exponent": str(left["threshold_energy_exponent"]),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove concentration of repeated-difference GL_2(Z) transitions, "
                "or construct a phase-anchored invariant that forces Cycle-126 chain depth"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_133_determinant_cluster_energy_v1.py --write",
            "check_command": "python3 proof/build_cycle_133_determinant_cluster_energy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_133_determinant_cluster_energy_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 133 sealer", output=OUTPUT, payload_factory=seal))
