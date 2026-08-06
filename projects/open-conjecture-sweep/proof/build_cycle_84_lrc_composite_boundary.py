"""Seal C84's direct composite-modulus LRC polynomial boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-84-b084-lrc-composite-polynomial-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-84-b084-lrc-composite-eventual-properness-preregistration-v1.md", "6ad97975a51887e7b3097d6beb0624740c0cc5acdea08fbf68d83d568dcbd13a"),
    "idea_selection": ("discovery/cycle84_portfolio_idea_selection.md", "01fb3a89b2ba32b81068f928812e691402dc61c1d71703eed5482db71c549549"),
    "source_audit": ("discovery/cycle84_lrc_source_audit.md", "94051d81a7c342e98a1ba23545941b154b8e2102aae67beb3a0921a91aff2da5"),
    "exhaustive_checker": ("proof/check_cycle84_composite_prop41.py", "d9b82942894455aab304177d237a72b0ae7e661fecceec50f794e4060e3053c8"),
    "witness_checker": ("proof/check_cycle84_composite_witness.py", "f676986f4d347c1e3ebc5349473e786503f9d1c2049ef24e5765018bc3153348"),
    "certificate": ("proof/cycle84_composite_prop41_boundary.md", "0a48911b5088de0f17c0045697cb8d31e7447dd12689d67aac3e76d6d259c78e"),
    "test": ("tests/test_cycle84_composite_prop41.py", "6c56845b4d1daca46081597ea83c221108dff4ee9df3aa80123bdeca6054dc7e"),
    "prior_lrc_boundary": ("artifacts/cycle-50-b050-lrc-deletion-aware-packet-v1.json", "c29fb94c0e7eea145157ea3e71deb71c5352da6ebc53c96e908a93576047f3e9"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def run(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def audit() -> dict:
    exhaustive = run(HASHES["exhaustive_checker"][0])
    witness = run(HASHES["witness_checker"][0])
    require(exhaustive["status"] == witness["status"] == "PASS", "checker failure")
    require(exhaustive["fiber_vectors"] == 8191, "binary fiber drift")
    require(exhaustive["failing_vectors"] == 4824, "failure count drift")
    require(exhaustive["first_failure"]["vector"] == witness["vector"], "named witness drift")
    require(len(witness["r_rows"]) == 6, "unit table drift")
    return {"exhaustive_binary_fiber": exhaustive, "independent_witness_table": witness}


def payload() -> dict:
    return {
        "artifact_id": "cycle-84-b084-lrc-composite-polynomial-boundary-v1",
        "budget_ordinal": "B084",
        "cycle": 84,
        "record_type": "METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-06T00:20:22Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The direct Z_14 analogue of the source's prime-field target-box lemma fails: 4,824 of 8,191 declared binary zero-divisor vectors fail, including (0,7,0,...,0).",
        "claim_boundary": "This refutes only the verbatim composite extension of the cited target-box lemma. It neither refutes LRC(13), nor eventual properness, nor every possible CRT/composite-modulus theorem.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c84_portfolio (Oracle)",
            "companion_advice": "Audit the k=13 CRT obstruction in the prime-field Proposition 4.1 and pivot if a structural zero-divisor case survives.",
            "decision": "Seal the exact direct-extension boundary and return to portfolio discovery rather than reopen the paused p=199 local LRC engine.",
            "falsifier": "A successful unit pair for the named vector, or a differing exhaustive binary-fiber count.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c84"),
        "sealer": {"path": "proof/build_cycle_84_lrc_composite_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle84_composite_prop41.py && python3 proof/check_cycle84_composite_witness.py",
            "test": "pytest -q tests/test_cycle84_composite_prop41.py",
            "check": "python3 proof/build_cycle_84_lrc_composite_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
