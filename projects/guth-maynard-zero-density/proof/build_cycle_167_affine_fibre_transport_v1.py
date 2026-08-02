#!/usr/bin/env python3
"""Seal Cycle 167 affine-fibre cross-label transport classifier."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-167-affine-fibre-transport-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-167-affine-fibre-transport-preregistration-v1.md", "4d22d86453ab226cef0905750ecabea1dda4926bd232ab765c306b14e7739eb9"),
    "document": (ROOT / "docs/cycle-167-affine-fibre-transport-v1.md", "2577f4931165ed66ce71d656cdd252c16fc93e19cb0f8324bb6aedcc8bc285ca"),
    "conventions": (ROOT / "conventions/affine_fibre_transport_v1.py", "b2c06be11b0d2f80b25097e75e19d48c1eef9de28ad39acb32a316c9fab131f5"),
    "tests": (ROOT / "tests/test_cycle_167_affine_fibre_transport_v1.py", "ef5e2f6898537ffb72a508138d577ea085b4f96d5bf7ea046a786879f7cce3ba"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle166": (ROOT / "artifacts/cycle-166-terminal-bank-entropy-v1.json", "9bc9b95a2ccd7e675681f8f1e5f771394a4ab82b359104f6d1259163a6bfa6eb"),
    "cycle67": (ROOT / "artifacts/cycle-67-seeded-packet-recurrence-v1.json", "85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.affine_fibre_transport_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    require("single cross-label edge" in checked["boundary"], "cross-label boundary")
    require(module.eligible_parameters((0, 1, 2, 3), h0=26, r=1, a=5, q=4, h_scale=20) == (), "residue obstruction")
    require(module.eligible_parameters((0, 1, 2, 3), h0=21, r=3, a=3, q=2, h_scale=21) == (), "range obstruction")
    edge = module.transport_edge(h=10, j=5, beta=module.Q(0), y=module.Q(3, 2), q=3, a=5, shift_error=module.Q(0))
    require(edge["target_residual"] == 0, "beta transport identity")
    return checked


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle166"][0], "SEALED_MASSED_BETA_ANCHORED_SHIFT_OR_SEEDED_PACKET_WEB")
    validate_prior(INPUTS["cycle67"][0], "SEALED_SEEDED_X6_25_AP_RECURRENCE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="affine_fibre_transport_v1")
    return {
        "artifact_id": "cycle-167-affine-fibre-transport-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_AFFINE_CROSS_LABEL_TRANSPORT_OR_OBSTRUCTION_CLASSIFIER",
        "claim_boundary": "Within the one-step affine multiplicative architecture, this classifies beta-preserving cross-label edges. It proves no eligible actual Cycle-166 fibre, target-local packet, recurrence, E7/E9 skeleton, density, or interval gain.",
        "runtime": check_runtime("Cycle 167"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle166_role": "provides conditional massed beta-anchored shift/packet webs but not distinct-anchor eligibility",
            "cycle67_role": "requires a genuine target-local packet and seed; a cross-label edge alone is insufficient",
        },
        "affine_transport_classifier": {"epistemic_status": "PROVED", **theorem},
        "independence_countermodels": {
            "epistemic_status": "PROVED",
            "statement": "Finite exact affine fibres separately realize residue failure, transformed-range failure, and unbounded balance; parent multiplicity alone cannot force direct transport in this architecture.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Join an eligible cross-label edge to a retained target-local packet, or construct a labelled closed transport loop that yields an equivalent local relation while preserving beta and all range labels.",
        },
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_167_affine_fibre_transport_v1.py --write",
            "check_command": "python3 proof/build_cycle_167_affine_fibre_transport_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_167_affine_fibre_transport_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 167", output=OUTPUT, payload_factory=seal))
