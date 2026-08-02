#!/usr/bin/env python3
"""Seal Cycle 176's all-row local-pairing transport consistency check."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-176-local-pairing-transport-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "torsor": (ROOT / "artifacts/cycle-166-fibre-torsor-v1.json", "cd0cf07f8ded432a7f53c18126d26b5054b3fddadb530375483c7adbc753991e"),
    "pairing": (ROOT / "artifacts/cycle-175-leading-residue-pairing-v1.json", "9ec7b4bf1a8a8ca87e586988e6e6d14e85aa597e163be032c9e668d128c593bb"),
    "prereg": (ROOT / "docs/cycle-176-local-pairing-transport-preregistration-v1.md", "679974a0c567cc9af47bdfd508dd4a8652e04bedefa6a0af4e0c8858916e562e"),
    "replay": (ROOT / "proof/verify_cycle_176_local_pairing_transport.py", "0aa9ba169db1bfa7435fa97525bff484bafefdb73a6ae17926abe44679e49c74"),
    "output": (ROOT / "discovery/cycle-176-local-pairing-transport-prototype-v1.json", "4cdd00dfec2a558e7de70fc4907bd89e1f9b66463a056ae66d7a738d14596feb"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 176 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-176-local-pairing-transport-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["base_rows_checked"], summary["local_states_checked"]) == (36, 108), "coverage drift")
    require(summary["all_row_covariances"] and summary["local_third_return"], "transport consistency drift")
    require(summary["orientation_anchors"] == {"3,5": 2, "3,4": 1}, "anchor drift")
    return {
        "artifact_id": "cycle-176-local-pairing-transport-v1", "cycle": 176, "budget_ordinal": "B014", "epistemic_status": "PROVED", "status": "SEALED_LOCAL_PAIRING_TRANSPORT_CONSISTENCY_ONLY", "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The direct local-pairing projection is total on 36 rows, preserves both anchors, and has order-three transport on all 108 local states; its covariance is inherited from the sealed torsor section."},
        "exact_prototype": {"source_output": "discovery/cycle-176-local-pairing-transport-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "LOCAL_PAIRING_CONSISTENT_BUT_NO_INDEPENDENT_CHARACTERISTIC_TO_RAY_MAP", "remaining_bottleneck": "Define an arithmetic local-to-ray reciprocity map directly from the 36 characteristics, without s or d inputs, and test recovery of local-pairing values, ray labels, and anchors.", "disallowed_pseudo_progress": ["calling inherited torsor covariance an interface advance", "using s or d as inputs to the proposed map", "fitting a local-to-ray map from target labels"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 177/B015: preregister an arithmetic characteristic-to-local-to-ray reciprocity map independent of s,d, then test all 36 labels and both anchors."},
        "preregistration_preflight": {"cycle": 176, "manifest_sha256": sha256(ROOT / "docs/cycle-176-local-pairing-transport-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-176-local-pairing-transport-preregistration-v1.md --expected-cycle 176 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_176_local_pairing_transport.py --output discovery/cycle-176-local-pairing-transport-prototype-v1.json", "write_command": "python3 proof/build_cycle_176_local_pairing_transport_v1.py --write", "check_command": "python3 proof/build_cycle_176_local_pairing_transport_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_176_local_pairing_transport_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
