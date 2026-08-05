"""Correct C65's top-level epistemic tag; supersede the immutable v1 record."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.build_cycle_65_step_graphon_packet import payload as v1_payload
from proof.cycle_seal_v1 import run_cli, sha256


def payload():
    result = v1_payload()
    result.update({
        "artifact_id": "cycle-65-b065-step-graphon-v2",
        "record_type": "CORRECTED_BOUNDED_2X2_FALSIFIER_SEARCH_AND_STRATEGIC_PAUSE",
        "epistemic_status": "OBSERVED",
        "correction": {
            "supersedes": "cycle-65-b065-step-graphon-v1",
            "error": "The top-level epistemic_status used the unsupported descriptive value MIXED.",
            "cause": "The exact finite census and bounded search were combined at the record level instead of assigning the conservative top-level tag.",
            "effect": "Metadata only. All mathematical payloads, hashes, counts, decisions, and claim boundaries are unchanged.",
            "resolution": "Use OBSERVED for the bounded-search record; retain PROVED on its exact finite subclaims.",
        },
        "sealer": {"path": "proof/build_cycle_65_step_graphon_packet_v2.py", "sha256": sha256(Path(__file__))},
    })
    result["replay"]["check"] = "python3 proof/build_cycle_65_step_graphon_packet_v2.py --check"
    return result


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-65-b065-step-graphon-v2.json",
        payload_factory=payload,
    ))
