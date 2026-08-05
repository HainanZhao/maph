"""Seal the C78 certification-status correction without altering C78 v1."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v1.json"
HASHES = {
    "superseded_record": (
        "artifacts/cycle-78-b078-compatible-spin-endpoint-v1.json",
        "7542ffb9b8a49579accc884f62f36870baa1b1715aaa4b3a47bcfa1f2e73ede5",
    ),
    "correction": (
        "docs/cycle78_endpoint_certification_correction.md",
        "59e5c050cfa3246027d8c3c407311bd2ad3f177528d68285ca0c65c562b6b1ca",
    ),
    "preregistration": (
        "docs/cycle-78-b078-compatible-spin-endpoint-preregistration-v1.md",
        "53f1d2e83421cf2ac23ca589123450ec70198afa9d82bbd2216313d4b4a13794",
    ),
    "theorem_note": (
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


def payload() -> dict:
    return {
        "artifact_id": "cycle-78-b078-compatible-spin-endpoint-correction-v1",
        "budget_ordinal": "B078",
        "cycle": 78,
        "record_type": "CORRECTION_CERTIFICATION_STATUS_WITHDRAWAL",
        "recorded_at_utc": "2026-08-05T18:20:00Z",
        "status": "SEALED",
        "epistemic_status": "CONJECTURED",
        "supersedes": "cycle-78-b078-compatible-spin-endpoint-v1",
        "outcome": (
            "C78's endpoint interpolation remains a conditional reduction, "
            "but its unconditional PROVED status and paper readiness are withdrawn "
            "because Song--Chen Proposition 3 is currently a preprint."
        ),
        "correction": {
            "error": "A preprint proposition was treated as a published theorem in the PROVED promotion path.",
            "cause": "The paper-stage hostile audit checked mathematical applicability but surfaced the repository rule requiring a published theorem or an independent proof.",
            "affected_claims": "C78 v1 epistemic status, unconditional theorem claim, and paper/publication readiness.",
            "repair": "Downgrade to a CONJECTURED conditional reduction; require an independent replayable proof of the Q=I/2 endpoint or a peer-reviewed source before promotion.",
        },
        "claim_boundary": (
            "The exact endpoint interpolation algebra is retained only conditional "
            "on Song--Chen Proposition 3. This correction makes no claim about "
            "the truth or falsehood of the compatible-marginal conjecture."
        ),
        "cycle_decision": {
            "companion_identity": "/root/oracle_c78_paper_audit (Oracle)",
            "companion_advice": "Do not publish: internalize the preprint endpoint proof or locate a peer-reviewed version, then rerun hostile audit.",
            "decision": "Seal the certification correction immediately; retain the mathematical route as conditional rather than silently weakening the record.",
            "falsifier": "A peer-reviewed theorem or independent proof of the Q=I/2 endpoint removes this certification defect; a counterexample to it refutes the conditional route.",
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("c78-correction"),
        "sealer": {
            "path": "proof/build_cycle_78_endpoint_correction.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "check": "python3 proof/build_cycle_78_endpoint_correction.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
