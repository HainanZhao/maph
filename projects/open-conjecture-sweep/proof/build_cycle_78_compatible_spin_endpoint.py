"""Seal C78's compatible three-qubit endpoint-interpolation theorem."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-78-b078-compatible-spin-endpoint-v1.json"
HASHES = {
    "preregistration": (
        "docs/cycle-78-b078-compatible-spin-endpoint-preregistration-v1.md",
        "53f1d2e83421cf2ac23ca589123450ec70198afa9d82bbd2216313d4b4a13794",
    ),
    "source_audit": (
        "docs/cycle78_endpoint_source_audit.md",
        "919ba97585492cc3990614257704cb7eda1a3ec867fa3425c9c750fb4c1164a6",
    ),
    "idea_selection": (
        "discovery/cycle77_coherent_idea_selection.md",
        "1c816fc324afd47e68eefe64b47ed15a8d43d7951f37b9176f07e29b455f2090",
    ),
    "theorem": (
        "proof/cycle78_endpoint_interpolation.md",
        "8381e4450b7e16425357bb2f253f629537fba5bbbff1b2432e6702c8145cf8a6",
    ),
    "checker": (
        "proof/check_cycle78_endpoint_interpolation.py",
        "b949c480c8e8acc89e22f28d92fcd87216fc1031e18719ddce7d3302de2b2976",
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
        "epistemic_status": "PROVED",
        "ky_fan_indices": 7,
        "source_half_scale": "1/2",
        "status": "PASS",
        "sympy_version": "1.12",
        "target_entries": 8,
    }, "C78 endpoint checker mismatch")
    return output


def payload() -> dict:
    result = audit()
    return {
        "artifact_id": "cycle-78-b078-compatible-spin-endpoint-v1",
        "budget_ordinal": "B078",
        "cycle": 78,
        "record_type": "PROVED_COMPATIBLE_THREE_QUBIT_ENDPOINT_THEOREM",
        "recorded_at_utc": "2026-08-05T18:15:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": (
            "Song--Chen Conjecture 2 holds for every compatible three-qubit "
            "state, arbitrary nonnegative weights supported on AB, AC, BC, "
            "and every qubit state Q."
        ),
        "claim_boundary": (
            "This proves only the n=3, d=2, two-body-support compatible "
            "gate. It does not prove Conjecture 2 for other subset supports, "
            "more parties, or higher local dimension."
        ),
        "proof_mechanism": {
            "published_endpoint": "Song--Chen Proposition 3 at Q=I/2, scaled by 1/2",
            "pure_endpoint": "A density matrix is majorized by the pure aligned target",
            "bridge": "qubit endpoint interpolation plus Ky Fan convexity and the common ordered target spectrum",
        },
        "audit": result,
        "cycle_decision": {
            "companion_identity": "/root/oracle_c78_seal_review (Oracle)",
            "companion_advice": "Seal after C78 naming, tensor-order/unitary clarification, and a seven-Ky-Fan hardened checker.",
            "decision": "All hardening and exact replay checks passed; seal the theorem and begin the non-budgeted paper phase.",
            "falsifier": "A compatible rho_ABC, weights a,b,c, qubit Q, and Ky Fan index k<=7 with K_k(H_Q)>K_k(T_Q), or a failure of the endpoint/source/order audit.",
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("c78"),
        "sealer": {
            "path": "proof/build_cycle_78_compatible_spin_endpoint.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "audit": "python3 proof/check_cycle78_endpoint_interpolation.py",
            "check": "python3 proof/build_cycle_78_compatible_spin_endpoint.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
