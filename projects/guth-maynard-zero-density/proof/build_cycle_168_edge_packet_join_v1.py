#!/usr/bin/env python3
"""Seal Cycle 168 edge/local-packet compatibility calculus."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-168-edge-packet-join-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-168-edge-packet-join-preregistration-v1.md", "aaa05a69f126e807b8a6acebd392d58b717df576a96bd838efd809062d383fdc"),
    "document": (ROOT / "docs/cycle-168-edge-packet-join-v1.md", "c7f0340f7e3f4c83889d815ab4cbe60e48ffd2631e0edcaf524bc9f61c887b34"),
    "conventions": (ROOT / "conventions/edge_packet_join_v1.py", "3cabd49847031829460d8de73732e82a44cb7eac1564b0b1662c0f918335a262"),
    "tests": (ROOT / "tests/test_cycle_168_edge_packet_join_v1.py", "b403ec67b09fd42b0a0a2aebbd9e0fcc9c96b3b286347170386d15508ea192b8"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle167_correction": (ROOT / "artifacts/cycle-167-affine-fibre-transport-v1-scope-correction.json", "e2173286dd40f32f19fb1ba433bb2242c929f1eb2150de7e754ba1209fdeb00b"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.edge_packet_join_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("bipartite form" in checked["overlap"], "compatibility ledger")
    require("trivial integer holonomy" in checked["loop"], "loop containment")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle167_correction"][0], "SEALED_REDUCED_RATIONAL_SCOPE_CORRECTION")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="edge_packet_join_v1")
    return {
        "artifact_id": "cycle-168-edge-packet-join-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_EDGE_PACKET_COMPATIBILITY_OR_TYPED_SUPPORT_SEPARATION",
        "claim_boundary": "This proves an exact edge/local-packet compatibility calculus and typed nonjoin partition. It does not lower-bound overlap for actual populations or prove a recurrence, skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 168"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle167_role": "provides only reduced-rational cross-label edges, not target-local packets",
            "cycle67_role": "supplies propagation after one genuine target seed is joined to a local packet",
        },
        "join_calculus": {"epistemic_status": "PROVED", **theorem},
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a label-faithful lower bound for the bipartite edge/packet compatibility form, or establish a typed support-separation inverse for the actual Cycle-165--167 populations.",
        },
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_168_edge_packet_join_v1.py --write",
            "check_command": "python3 proof/build_cycle_168_edge_packet_join_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_168_edge_packet_join_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 168", output=OUTPUT, payload_factory=seal))
