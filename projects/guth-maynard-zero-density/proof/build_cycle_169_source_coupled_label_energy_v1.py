#!/usr/bin/env python3
"""Seal Cycle 169 source-coupled label-energy no-go."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-169-source-coupled-label-energy-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-169-source-coupled-label-energy-preregistration-v1.md", "5c743dd327a69800fae3de9e65a602464f390343059dfb1ea764400dac768a37"),
    "document": (ROOT / "docs/cycle-169-source-coupled-label-energy-v1.md", "562e9ab168fca10f047c236d5a6451af7891cafee2be718c26c6426ebddce342"),
    "conventions": (ROOT / "conventions/source_coupled_label_energy_v1.py", "3492582887a8d64b383c85a9a0cd057965c17cd119e356d4e4fa3aa51fded2f7"),
    "tests": (ROOT / "tests/test_cycle_169_source_coupled_label_energy_v1.py", "e06230448fb8746f804c5dc4255d64cca087041ecf903740d6881e2bea75a66d"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle168": (ROOT / "artifacts/cycle-168-edge-packet-join-v1.json", "d0f914b7fb00b968ba76195862ccdf248dcdce08904b43fac2ebf1c3939f50d4"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.source_coupled_label_energy_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    model = module.anticorrelated_model(7, 11)
    edges, packets = module.pushforwards(model)
    require(module.mixed_label_energy(edges, packets) == 0, "anticorrelated marginals")
    require(module.pair_sum_identity(model) == 0, "pair identity")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle168"][0], "SEALED_EDGE_PACKET_COMPATIBILITY_OR_TYPED_SUPPORT_SEPARATION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="source_coupled_label_energy_v1")
    return {
        "artifact_id": "cycle-169-source-coupled-label-energy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_SOURCE_MARGINALS_DO_NOT_FORCE_TARGET_LABEL_ENERGY",
        "claim_boundary": "This proves a source-pushforward label-energy identity and sharp anticorrelation no-go. It does not use actual exponential geometry or prove overlap, compatibility, recurrence, skeleton, density, or intervals.",
        "runtime": check_runtime("Cycle 169"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {"epistemic_status": "PROVED", "cycle168_role": "defines the compatibility form whose label-overlap precondition is now shown not to follow from marginals"},
        "label_energy_no_go": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Use an actual exponential/fibre invariant to force common target labels, or convert the realized labelled separator into a quantitative structural inverse."},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_169_source_coupled_label_energy_v1.py --write",
            "check_command": "python3 proof/build_cycle_169_source_coupled_label_energy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_169_source_coupled_label_energy_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 169", output=OUTPUT, payload_factory=seal))
