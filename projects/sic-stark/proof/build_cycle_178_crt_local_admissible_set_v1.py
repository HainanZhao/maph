#!/usr/bin/env python3
"""Seal Cycle 178's CRT-record injectivity containment result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-178-crt-local-admissible-set-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "prior": (ROOT / "artifacts/cycle-177-characteristic-local-ray-v1.json", "cb501f35db6a697d9a761bf5c082a6c6796c39ab38c61bc28de03118ca794978"),
    "prereg": (ROOT / "docs/cycle-178-crt-local-admissible-set-preregistration-v1.md", "dcf0f85c41b32118550642b32be46087135c2642de34364ac9a244963aea5ed5"),
    "replay": (ROOT / "proof/verify_cycle_178_crt_local_admissible_set.py", "90a5f148d4e2e35b00824d5a37ccf332c8c718e4163b49ec09c7c8c8439704dc"),
    "output": (ROOT / "discovery/cycle-178-crt-local-admissible-set-prototype-v1.json", "a80a6cc54727d7b9432197c351d12164ffb2bc67494029ab777d8b43c6b1829f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 178 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-178-crt-local-admissible-set-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["distinct_crt_records"], summary["nontrivial_fibres"], summary["empty_intersection_fibres"]) == (36, 36, 0, 0), "CRT record summary drift")
    require(1 in summary["anchor_admissible_sets"]["3,5"] and 2 in summary["anchor_admissible_sets"]["3,4"], "anchor admissible set drift")
    return {
        "artifact_id": "cycle-178-crt-local-admissible-set-v1", "cycle": 178, "budget_ordinal": "B016", "epistemic_status": "PROVED", "status": "SEALED_CRT_RECORD_INJECTIVE_COMPATIBILITY_VACUOUS", "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The frozen exact-valuation CRT record is injective on 36 rows, so its admissible-set compatibility test has no nontrivial fibres and yields no interface evidence."},
        "exact_prototype": {"source_output": "discovery/cycle-178-crt-local-admissible-set-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "EXACT_V2_CRT_RECORD_TOO_FINE_THEOREM_DEFINED_P2_QUOTIENT_REQUIRED", "remaining_bottleneck": "Derive the finite local quotient of K_p2^times dictated by the modulus-6 ray exact sequence, then rerun the admissible-set fibre test without unrestricted valuation data.", "disallowed_pseudo_progress": ["calling singleton-fibre compatibility an interface", "retaining unrestricted v2 as a finite local quotient", "using s,d or target labels in the source record"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 179/B017: derive the theorem-defined p2 local ray quotient and test its finite classes against admissible ray-exponent sets on all 36 characteristics."},
        "preregistration_preflight": {"cycle": 178, "manifest_sha256": sha256(ROOT / "docs/cycle-178-crt-local-admissible-set-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-178-crt-local-admissible-set-preregistration-v1.md --expected-cycle 178 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_178_crt_local_admissible_set.py --output discovery/cycle-178-crt-local-admissible-set-prototype-v1.json", "write_command": "python3 proof/build_cycle_178_crt_local_admissible_set_v1.py --write", "check_command": "python3 proof/build_cycle_178_crt_local_admissible_set_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_178_crt_local_admissible_set_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
