"""Seal C79's independent compatible \(Q=I/2\) endpoint theorem."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-79-b079-compatible-endpoint-foundation-v1.json"
HASHES = {
    "preregistration": (
        "docs/cycle-79-b079-compatible-endpoint-foundation-preregistration-v1.md",
        "f03ffc5d6168f3f3cdb99ca12e65dfd5e5aea7ab15ce020e0574c665b4aeb822",
    ),
    "source_audit": (
        "docs/cycle79_endpoint_foundation_source_audit.md",
        "bfe60ba98a58503a2e32bfe4552ef934d937dad556919678a838a5df3446a31f",
    ),
    "idea_selection": (
        "discovery/cycle79_endpoint_foundation_idea_selection.md",
        "80dd42109f4a43de6febe11b6fb582d5233747ab60236ebb57b8a822cb83557e",
    ),
    "theorem": (
        "proof/cycle79_compatible_endpoint_foundation.md",
        "b071f5aa80715a6827f52345aee91fbeb5f62d1a0bf75ffcbbc2e8472672ebd4",
    ),
    "checker": (
        "proof/check_cycle79_compatible_endpoint_foundation.py",
        "2532c3ccc9cdb5e671c64895c8e1bddb6fcf9a16064a490e9f0a44376fefc426",
    ),
    "c78_correction": (
        "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v1.json",
        "5091f16f52f2b8d48b5eef2dde55d153617a72f7a1c5e7fdfe0915fe47218d2e",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7",
    ),
    "validator": (
        "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
}


def audit() -> dict:
    output = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / HASHES["checker"][0])], text=True
    ))
    require(output == {
        "D_fan_vertex_rows": 736,
        "epistemic_status": "PROVED",
        "minimum_rows": 40,
        "polygon_vertices": {"s_ge_1": 4, "s_le_1": 4},
        "scope": "exact finite scalar audit only",
        "spin_flip_basis_rows": 64,
        "status": "PASS",
        "sympy_version": "1.12",
        "target_ky_fan_rows": 8,
    }, "C79 endpoint-foundation checker mismatch")
    return output


def payload() -> dict:
    result = audit()
    return {
        "artifact_id": "cycle-79-b079-compatible-endpoint-foundation-v1",
        "budget_ordinal": "B079",
        "cycle": 79,
        "record_type": "PROVED_INDEPENDENT_COMPATIBLE_Q_HALF_ENDPOINT",
        "recorded_at_utc": "2026-08-05T18:45:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "For every compatible three-qubit state and arbitrary probability "
            "weights on AB, AC, BC, the pair-support compatible spin-alignment "
            "inequality holds at Q=I/2. This independent proof removes the "
            "preprint-only endpoint dependency identified in C78."
        ),
        "claim_boundary": (
            "This establishes only the normalized Q=I/2 endpoint (equivalently "
            "the unnormalized-I statement). It does not by itself reinstate "
            "C78's arbitrary-Q interpolation, cover incompatible triples, "
            "other supports, more parties, or higher local dimension."
        ),
        "proof_mechanism": {
            "one_prefix": "density-matrix Ky Fan bound",
            "two_prefix": "direct two-rank-two-projection principal-angle spectrum",
            "three_prefix": (
                "published Higuchi--Sudbery--Szulc polygon inequality, "
                "qubit spin-flip identity, and a lower-tail Ky Fan bound"
            ),
            "assembly": "ordered-prefix decomposition, Ky Fan subadditivity, and common nested target order",
        },
        "published_source": {
            "citation": (
                "A. Higuchi, A. Sudbery, J. Szulc, One-qubit reduced states "
                "of a pure many-qubit state: polygon inequalities, Phys. Rev. "
                "Lett. 90, 107902 (2003)"
            ),
            "doi": "10.1103/PhysRevLett.90.107902",
            "checked_hypothesis": (
                "After Ky Fan convexity reduction, the global state is pure "
                "and r_A,r_B,r_C are the smaller eigenvalues of its one-qubit marginals."
            ),
        },
        "audit": result,
        "cycle_decision": {
            "companion_identity": "/root/oracle_c79_seal_review (Oracle)",
            "companion_advice": (
                "After repairing the literal carriage-return defects and "
                "making Q=I/2 scaling and tail notation explicit, seal C79 "
                "in the same cycle; separately re-audit C78 before promotion."
            ),
            "decision": (
                "Documentation repair, preflight, exact replay, and diff "
                "check passed. Seal the independent endpoint theorem; retain "
                "C78 conditional pending its separately scoped re-audit."
            ),
            "falsifier": (
                "An exact compatible rho_ABC, nonnegative normalized weights, "
                "and Ky Fan index r with K_r(H)>K_r(T), or a failed polygon "
                "row, spin-flip row, or target-additivity row."
            ),
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("c79"),
        "sealer": {
            "path": "proof/build_cycle_79_compatible_endpoint_foundation.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "audit": "python3 proof/check_cycle79_compatible_endpoint_foundation.py",
            "check": "python3 proof/build_cycle_79_compatible_endpoint_foundation.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
