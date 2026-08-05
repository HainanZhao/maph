"""Seal C78's same-cycle certification reinstatement after C79."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v2.json"
HASHES = {
    "reinstatement_note": (
        "docs/cycle78_endpoint_reinstatement.md",
        "675ddfe90486ffea57a4521c8db679f66659819b3f435e06ddf2ceb49f2930df",
    ),
    "original_record": (
        "artifacts/cycle-78-b078-compatible-spin-endpoint-v1.json",
        "7542ffb9b8a49579accc884f62f36870baa1b1715aaa4b3a47bcfa1f2e73ede5",
    ),
    "withdrawal_record": (
        "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v1.json",
        "5091f16f52f2b8d48b5eef2dde55d153617a72f7a1c5e7fdfe0915fe47218d2e",
    ),
    "c79_record": (
        "artifacts/cycle-79-b079-compatible-endpoint-foundation-v1.json",
        "4efb203967b29dc99fe7b669c590fafb5d1d2bb88fadc4682210c1fb7a014166",
    ),
    "c78_theorem": (
        "proof/cycle78_endpoint_interpolation.md",
        "8381e4450b7e16425357bb2f253f629537fba5bbbff1b2432e6702c8145cf8a6",
    ),
    "c78_checker": (
        "proof/check_cycle78_endpoint_interpolation.py",
        "b949c480c8e8acc89e22f28d92fcd87216fc1031e18719ddce7d3302de2b2976",
    ),
    "c79_theorem": (
        "proof/cycle79_compatible_endpoint_foundation.md",
        "b071f5aa80715a6827f52345aee91fbeb5f62d1a0bf75ffcbbc2e8472672ebd4",
    ),
    "c79_checker": (
        "proof/check_cycle79_compatible_endpoint_foundation.py",
        "2532c3ccc9cdb5e671c64895c8e1bddb6fcf9a16064a490e9f0a44376fefc426",
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
    c78 = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / HASHES["c78_checker"][0])], text=True
    ))
    c79 = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / HASHES["c79_checker"][0])], text=True
    ))
    require(c78 == {
        "epistemic_status": "PROVED",
        "ky_fan_indices": 7,
        "source_half_scale": "1/2",
        "status": "PASS",
        "sympy_version": "1.12",
        "target_entries": 8,
    }, "C78 interpolation checker mismatch")
    require(c79 == {
        "D_fan_vertex_rows": 736,
        "epistemic_status": "PROVED",
        "minimum_rows": 40,
        "polygon_vertices": {"s_ge_1": 4, "s_le_1": 4},
        "scope": "exact finite scalar audit only",
        "spin_flip_basis_rows": 64,
        "status": "PASS",
        "sympy_version": "1.12",
        "target_ky_fan_rows": 8,
    }, "C79 endpoint checker mismatch")
    return {"c78_interpolation": c78, "c79_endpoint": c79}


def payload() -> dict:
    result = audit()
    return {
        "artifact_id": "cycle-78-b078-compatible-spin-endpoint-correction-v2",
        "budget_ordinal": "B078",
        "cycle": 78,
        "record_type": "CORRECTION_CERTIFICATION_REINSTATEMENT",
        "recorded_at_utc": "2026-08-05T19:05:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "supersedes": "cycle-78-b078-compatible-spin-endpoint-correction-v1",
        "outcome": (
            "C78's arbitrary-qubit compatible three-qubit pair-support "
            "theorem is reinstated as PROVED. C79 independently supplies "
            "the exact Q=I/2 endpoint, so Song--Chen Proposition 3 is no "
            "longer a preprint-only dependency."
        ),
        "claim_boundary": (
            "The proved result covers compatible three-qubit states, "
            "probability weights on AB, AC, BC, and every qubit Q. It "
            "excludes incompatible triples, other supports, more parties, "
            "and higher local dimensions."
        ),
        "correction": {
            "affected_claims": (
                "C78 v1's certification status and the C78 correction v1 "
                "withdrawal, not either immutable historical payload."
            ),
            "cause": (
                "C79 independently proved the endpoint that was previously "
                "available only in a preprint."
            ),
            "repair": (
                "Replace Song--Chen endpoint authority with the sealed C79 "
                "proof, recheck normalization and interpolation, and restore "
                "the PROVED status through this new record."
            ),
        },
        "proof_mechanism": {
            "endpoint": "C79 unnormalized-I inequality scaled by 1/2",
            "other_endpoint": "trace-one positivity against P_000 at Q=P_0",
            "bridge": "common local-unitary diagonalization and affine Ky Fan interpolation",
        },
        "audit": result,
        "cycle_decision": {
            "companion_identity": "/root/oracle_c78_reinstatement (Oracle)",
            "companion_advice": (
                "Issue a same-cycle B078 reinstatement record; do not mutate "
                "C78 v1 or its withdrawal record; re-enter paper phase only "
                "after a self-contained manuscript rewrite and new audit."
            ),
            "decision": (
                "C79's exact endpoint scope, scaling, pure endpoint, target "
                "ordering, and all interpolation rows were independently "
                "rechecked. Reinstate the theorem in a new immutable record."
            ),
            "falsifier": (
                "A compatible rho_ABC, admissible weights and qubit Q with "
                "a Ky Fan violation, or a defect in C79's endpoint proof, "
                "the 1/2 scaling, or target-affinity audit."
            ),
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("c78-reinstatement"),
        "sealer": {
            "path": "proof/build_cycle_78_endpoint_reinstatement.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "audit": (
                "python3 proof/check_cycle79_compatible_endpoint_foundation.py "
                "&& python3 proof/check_cycle78_endpoint_interpolation.py"
            ),
            "check": "python3 proof/build_cycle_78_endpoint_reinstatement.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
