#!/usr/bin/env python3
"""Seal Cycle 162's accelerated workflow and dimension-six interface gate."""
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
    "preregistration": (ROOT / "docs/cycle-162-workflow-migration-preregistration-v1.md", "ad080d9fbf497904d891ffa885dc4cd395f65e95c287b4ba9da6963b7af78984"),
    "document": (ROOT / "docs/cycle-162-workflow-migration-v1.md", "b3afc59c8bbf415e5454db81604023fd96ae5c0a481fa23118f9ad90f690d420"),
    "effective_stark_context": (ROOT / "docs/effective-stark-sweep-context-v1.md", "1963372c6e82b068844cc9469ddea2e39647d0b7e05e5c9aa4744bed814b7853"),
    "cycle157_document": (ROOT / "docs/sic-stark-cycle157.md", "72149e87781915319f6e82ea9218e92ab748714666ba8d37e67334dd572c977e"),
    "cycle161_document": (ROOT / "docs/sic-stark-cycle161.md", "6b6e1150fd4863970f118b74c470d0cba9bc3a65739d95ee93e6733d3c0ed07d"),
    "cycle157_certificate": (ROOT / "certificates/dimension-six-cycle157-fourier-normalization-audit.json", "f5dd1d19e4fdbcdf74c0744835fe68ed47721f7577b408aba12e910c8b693fdb"),
    "cycle161_certificate": (ROOT / "certificates/dimension-seven-cycle161-discriminant-eight-closure.json", "49fdbeaeecba0802e0b54cbb2e404cfb2c6fac2112d814de700dd6e9a12129cf"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
    "verifier": (ROOT / "proof/verify_cycle_162_workflow_migration.py", "f184c073eb8a0f8dd174356109cb09ef819566ab772be594bfbbe31adf529ddb"),
    "tests": (ROOT / "tests/test_research_workflow_migration.py", "0933d237e6ed41d947b0ad859bf5cb8f2fab4b385187eacb61f94137823510ae"),
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
        "status": "SEALED_ACCELERATED_WORKFLOW_AND_INTERFACE_FIRST_PROGRAM",
        "claim_boundary": "This proves only the replayed workflow attachment, immutable evidence inventory, and scope-accurate strategic handoff; it proves no mathematical theorem, dimension-six TCC identity, fusion-continuity bridge, wild-local extension, boundary limit, or nonexistence claim.",
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
        "effective_stark_dependency": {
            "epistemic_status": "PROVED",
            "results_paper": "Effective Archimedean Stark Theorems over Real Quadratic Fields: Quadratic Support, Shintani Transfer, and CM Descent",
            "version": "1.5",
            "doi": "10.5281/zenodo.21713178",
            "controls": [
                "Order six alone is not the obstruction (RQ-000190 over Q(sqrt(7))).",
                "Order six plus a ramified 3-power conductor is not sufficient to explain the obstruction (RQ-002057 over Q(sqrt(57)))."
            ],
            "shared_object": "RQ-000692 is the same Q(sqrt(21)), modulus-(6), C_6 ray object, with P_SIC(X)=P_census(-X), Shintani index 6, and relative ramification index 6 above 3.",
            "boundary": "The no-wild-prime hypothesis above 3 in the audited Roblot sextic route fails; this is a theorem-hypothesis boundary, not a TCC no-go."
        },
        "accelerated_program": {
            "epistemic_status": "STRATEGIC_DECISION",
            "phase0": "First close and exactly test the coefficient-to-cocycle/ray-log interface; in parallel design an oriented wild-local RQ-000692 engine; only then attempt fusion continuity.",
            "paper_iii": "September 2026 targets a new version of published Paper III v1 (DOI 10.5281/zenodo.21682631); proof-paper scope requires full Phase-0 closure.",
            "q4_campaign_cap": 100,
            "class_a": "A proof-grade replayable reduction of the operational bridge to an explicitly compact or finitely covered parameter theorem with pinned conventions and a strict exact or certified margin.",
            "kill_criterion": "No Class-A reduction after 100 substantive Q4 campaign cycles freezes dimension six and redirects primary effort to cross-dimension pattern mining."
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Construct and test a convention-pinned finite-characteristic coefficient-to-cocycle/ray-logarithm interface with explicit selection, operation, branches, finite part, and AFK identification; determine whether an oriented wild-local extension at RQ-000692 supplies any part of it."
        },
        "mentor_checkpoint": {
            "recommendation": "Authorize replacement and seal, preserving Cycle 157 and tagging all dimension-six bridge claims CONJECTURED.",
            "known_flaw": "Wild-local orientation may still leave the analytic coefficient-to-cocycle/ray-logarithm interface undefined.",
            "falsifier": "Any dependency on old Cycle 162, or any replacement claim that treats order-six control as TCC closure.",
            "next_action": "Seal the workflow-only Cycle 162, rerun preflight, verifier, and reference checks, then expose interface-first Phase 0 in PLAN and STATUS.",
            "resolution": "ADOPTED: no old Cycle-162 dependency was found; the replacement preserves the mathematical claim boundary and records the sweep result only as proved context and an open engine."
        },
        "replay": {
            "preflight_command": "research prereg check docs/cycle-162-workflow-migration-preregistration-v1.md --expected-cycle 162 --allow-head-drift",
            "write_command": "python3 proof/build_cycle_162_workflow_migration_v1.py --write",
            "check_command": "python3 proof/build_cycle_162_workflow_migration_v1.py --check",
            "test_command": "python3 -m unittest tests.test_research_workflow_migration -v",
            "verification_command": "python3 proof/verify_cycle_162_workflow_migration.py"
        }
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 162", output=OUTPUT, payload_factory=seal))
