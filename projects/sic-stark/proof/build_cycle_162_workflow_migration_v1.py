#!/usr/bin/env python3
"""Seal Cycle 162's workflow migration and dimension-six interface gate."""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
from tools.preregistration_check import validate_preregistration  # noqa: E402


SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-162-workflow-migration-v1.json"
PREFLIGHT_VALIDATOR = REPOSITORY_ROOT / "tools/preregistration_check.py"
PREFLIGHT_VALIDATOR_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS: dict[str, tuple[Path, str]] = {
    "project_instructions": (ROOT / "AGENTS.md", "aa401cd319bb93be3b94f492b4d965b08a32c39019197296751da35ec3f61c64"),
    "plan": (ROOT / "PLAN.md", "ae8db126b09cd5851a98c15ad9b1831f2437e16d16c605f2ba39f6078210fa72"),
    "profile": (ROOT / "research-records.json", "c0fd4838bbed20125cfa7f0732f82888e81fa98b18251b28500811409b09eeab"),
    "legacy_exceptions": (ROOT / "research_index_legacy_exceptions.json", "3a7f6e5f379b67d1f59264f82a8536ab24a0ce85ecf2fedf7f9e1c0979cc5f3c"),
    "research_requirements": (ROOT / "requirements-research.txt", "d4b7c20a4b076937df679a59bb5aaca739995ee14bf29d550b1c31118c173b22"),
    "preregistration": (ROOT / "docs/cycle-162-workflow-migration-preregistration-v1.md", "899a3e9d6526aaa2f2ba1129a90efe66fce532e9ba5f0a513f2823270d24f172"),
    "document": (ROOT / "docs/cycle-162-workflow-migration-v1.md", "58909db336ed246b75479be4eb861a9a8bf3a10eaea8e68fe13468ab6d27819d"),
    "cycle157_document": (ROOT / "docs/sic-stark-cycle157.md", "72149e87781915319f6e82ea9218e92ab748714666ba8d37e67334dd572c977e"),
    "cycle161_document": (ROOT / "docs/sic-stark-cycle161.md", "6b6e1150fd4863970f118b74c470d0cba9bc3a65739d95ee93e6733d3c0ed07d"),
    "cycle157_certificate": (ROOT / "certificates/dimension-six-cycle157-fourier-normalization-audit.json", "f5dd1d19e4fdbcdf74c0744835fe68ed47721f7577b408aba12e910c8b693fdb"),
    "cycle161_certificate": (ROOT / "certificates/dimension-seven-cycle161-discriminant-eight-closure.json", "49fdbeaeecba0802e0b54cbb2e404cfb2c6fac2112d814de700dd6e9a12129cf"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
    "verifier": (ROOT / "proof/verify_cycle_162_workflow_migration.py", "eefb92b9f49d51bb4bde055584fb1d7f1212209f1a8c0236e8d2d0d1a67d307f"),
    "tests": (ROOT / "tests/test_research_workflow_migration.py", "c211ae47f8177d8868299554a20b7a1bccd91827963bde1f37a35c08a56f4dee"),
}


def preflight() -> dict[str, object]:
    require(sha256(PREFLIGHT_VALIDATOR) == PREFLIGHT_VALIDATOR_HASH, "preflight validator hash mismatch")
    checked = validate_preregistration(
        ROOT / "docs/cycle-162-workflow-migration-preregistration-v1.md",
        expected_cycle=162,
        enforce_manifest_head=False,
    )
    return {
        "schema": checked["schema"],
        "cycle": checked["cycle"],
        "manifest_sha256": checked["manifest_sha256"],
        "input_hashes": checked["input_hashes"],
        "parameters": checked["parameters"],
    }


def seal() -> dict[str, Any]:
    from verify_cycle_162_workflow_migration import verify

    verification = verify()
    return {
        "artifact_id": "cycle-162-workflow-migration-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_WORKFLOW_MIGRATION_AND_INTERFACE_GATE",
        "claim_boundary": "This proves only the current record-workflow migration and its frozen dimension-six handoff; it proves no mathematical theorem, dimension-six TCC identity, boundary limit, or nonexistence claim.",
        "runtime": check_runtime("Cycle 162"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "preflight_validator": {"path": "../../tools/preregistration_check.py", "sha256": PREFLIGHT_VALIDATOR_HASH},
        "preregistration_preflight": preflight(),
        "workflow_result": {"epistemic_status": "PROVED", **verification},
        "active_gate": {
            "epistemic_status": "PROVED",
            "statement": "The current dimension-six boundary-packet formulation has no defined coefficient-to-cocycle/ray-logarithm map; no numerical extension or downstream conditional algebra closes that gap."
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct and test a convention-pinned finite-characteristic coefficient-to-cocycle/ray-logarithm interface with explicit selection, operation, branches, finite part, and AFK identification."
        },
        "mentor_checkpoint": {
            "recommendation": "Seal Cycle 162 as a workflow/strategic containment record, not a mathematical advance; retain D6 as blocked and D7 as closed scope.",
            "known_flaw": "PROVED is limited to exact replayed preservation/indexing assertions and does not certify the missing mathematical interface or exhaust all possible obstructions.",
            "falsifier": "A legacy byte/hash mismatch, profile inclusion outside cycle-*.json, or a located exact interface resolving the listed Cycle-157 conventions invalidates this gate statement.",
            "next_action": "Run immutable replay/check plus status/profile rebuild, record the scope/tag boundary, then seal the migration record.",
            "resolution": "ADOPTED: Cycle 162 is sealed only as workflow containment; the mathematical interface remains CONJECTURED and open."
        },
        "replay": {
            "preflight_command": "research prereg check docs/cycle-162-workflow-migration-preregistration-v1.md --expected-cycle 162 --allow-head-drift",
            "write_command": "python proof/build_cycle_162_workflow_migration_v1.py --write",
            "check_command": "python proof/build_cycle_162_workflow_migration_v1.py --check",
            "test_command": "python -m unittest tests.test_research_workflow_migration -v",
            "verification_command": "python proof/verify_cycle_162_workflow_migration.py"
        }
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 162", output=OUTPUT, payload_factory=seal))
