#!/usr/bin/env python3
"""Seal Cycle 166 massed beta-anchored terminal-web inverse."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-166-terminal-bank-entropy-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-166-terminal-bank-entropy-preregistration-v1.md", "677a57583b9c082a1ef5d52b72320fdb0a931b6eed49d13a5fe4eaa99b8c5aa8"),
    "document": (ROOT / "docs/cycle-166-terminal-bank-entropy-v1.md", "807a3cd3ff50b2258457ac322741c744270f5efdec561805d70736204830a4d7"),
    "conventions": (ROOT / "conventions/terminal_bank_entropy_v1.py", "5cf711d212b2b94daf73a140500a5625427ffed2866a84f0e428ebc0fa0d4a01"),
    "tests": (ROOT / "tests/test_cycle_166_terminal_bank_entropy_v1.py", "413e964615c3d585f5798c3899b24edb6a26f81aab276b141ba054f3dada0c59"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle165": (ROOT / "artifacts/cycle-165-anchored-fibre-product-determinant-v1.json", "506035a1ecc01b50df74926cdffbe32fc081d4140d889f4cb34d9e9951ee5ee9"),
}


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.terminal_bank_entropy_v1", fromlist=["verify_all"])
    checked = module.verify_all()
    ledger = checked["state_ledger"]
    require(ledger["rank_or_plane_forced_fibre_exponent"] == module.Q(1, 25), "rank/plane fibre")
    require(ledger["packet_forced_fibre_exponent"] == module.Q(2, 25), "packet fibre")
    require(ledger["subcritical_rank_or_plane_bound"] < ledger["registered_target"], "rank/plane margin")
    require(ledger["subcritical_packet_bound"] < ledger["registered_target"], "packet margin")
    return {key: str(value) for key, value in ledger.items()}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle165"][0], "SEALED_BETA_ANCHORED_FOUR_ANCHOR_PACKET_OR_RESONANCE_PLANE_CLASSIFICATION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="terminal_bank_entropy_v1")
    return {
        "artifact_id": "cycle-166-terminal-bank-entropy-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_MASSED_BETA_ANCHORED_SHIFT_OR_SEEDED_PACKET_WEB",
        "claim_boundary": "Conditional on a critical fixed-beta Cycle-63 census through Cycle 165, this forces one massed labelled terminal web. It does not bound the census or a web, prove E7/E9, density, or intervals.",
        "runtime": check_runtime("Cycle 166"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle165_role": "provides the labelled rank-one/high-packet/low-plane terminal partition at X^(38/25-o(1))",
        },
        "terminal_entropy_inverse": {"epistemic_status": "PROVED", **theorem},
        "massed_web_output": {
            "epistemic_status": "PROVED",
            "statement": "A rank-one or plane-induced shift state has X^(1/25-o(1)) parents, or a beta-seeded packet state has X^(2/25-o(1)) parents.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_checks(),
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Control one massed web, or turn a seeded packet/shift web into a strict E7/E9 skeleton margin while retaining beta, divisibility, and h-range labels.",
        },
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_166_terminal_bank_entropy_v1.py --write",
            "check_command": "python3 proof/build_cycle_166_terminal_bank_entropy_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_166_terminal_bank_entropy_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 166", output=OUTPUT, payload_factory=seal))
