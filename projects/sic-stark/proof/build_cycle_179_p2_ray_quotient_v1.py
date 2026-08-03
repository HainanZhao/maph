#!/usr/bin/env python3
"""Seal Cycle 179's modulus-defined prime-2 ray-factor result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-179-p2-ray-quotient-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "section": (ROOT / "artifacts/cycle-164-oriented-ray-monoid-section-v1.json", "f1815f8641780570c15c7e9c6b40f9de8390358fb3dec0ac93aa311b78a6a26d"),
    "p3_prior": (ROOT / "artifacts/cycle-177-characteristic-local-ray-v1.json", "cb501f35db6a697d9a761bf5c082a6c6796c39ab38c61bc28de03118ca794978"),
    "prior": (ROOT / "artifacts/cycle-178-crt-local-admissible-set-v1.json", "08da527e3d66a2f78e5bf1f706139e3fd7bb2aeeb6abe9fcb1eea65290711e2b"),
    "prereg": (ROOT / "docs/cycle-179-p2-ray-quotient-preregistration-v1.md", "cb9d0098db17b6986262f0fe46203bde0252b7801ecc13037c1a6789adb9897d"),
    "replay": (ROOT / "proof/verify_cycle_179_p2_ray_quotient.py", "10c4f4e622b5410aaec43b2c934a283658b2e4512ba96d8c016b7b84fda64155"),
    "output": (ROOT / "discovery/cycle-179-p2-ray-quotient-prototype-v1.json", "21de802ee28d1d920ef5cc3069659fa0caf0f18b226a1f7e8d2b13cdf226dae1"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 179 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-179-p2-ray-quotient-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["distinct_crt_records"], summary["nontrivial_fibres"], summary["empty_intersection_fibres"]) == (36, 36, 0, 0), "CRT fibre summary drift")
    require(summary["p2_conductor_exponent_counts"] == {"0": 9, "1": 27}, "p2 conductor count drift")
    require(summary["p2_factor_class_counts"] == {"0:[0, 0]": 9, "1:[0, 1]": 9, "1:[1, 0]": 9, "1:[1, 1]": 9}, "p2 factor class drift")
    require(1 in summary["anchor_admissible_sets"]["3,5"] and 2 in summary["anchor_admissible_sets"]["3,4"], "anchor admissible set drift")
    return {
        "artifact_id": "cycle-179-p2-ray-quotient-v1", "cycle": 179, "budget_ordinal": "B017", "epistemic_status": "PROVED", "status": "SEALED_RAY_EXACT_P2_FACTOR_CRT_INJECTIVE_VACUOUS",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The conductor-lowered prime-2 ray factor and its canonical transition are exact, but together with the frozen prime-3 record they still resolve all 36 rows; the fibre compatibility test remains vacuous."},
        "local_exact_sequence": result["local_exact_sequence"], "exact_prototype": {"source_output": "discovery/cycle-179-p2-ray-quotient-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "LOCAL_RAY_FACTORS_RESOLVE_ROWS_ARTIN_ASSEMBLY_REQUIRED", "remaining_bottleneck": "A valid interface needs a functorial local-global Artin assembly with a structural relation to the characteristic dynamics, rather than a row-resolving local record.", "disallowed_pseudo_progress": ["calling singleton-fibre compatibility an interface", "discarding a modulus-defined local factor merely to create collisions", "using s,d, selected exponents, or target labels"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The next engine, subject to companion review, is an explicit local-global Artin assembly for admissible exponent sets with global-unit ambiguity and a preregistered structural identity test."},
        "preregistration_preflight": {"cycle": 179, "manifest_sha256": sha256(ROOT / "docs/cycle-179-p2-ray-quotient-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-179-p2-ray-quotient-preregistration-v1.md --expected-cycle 179 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_179_p2_ray_quotient.py --output discovery/cycle-179-p2-ray-quotient-prototype-v1.json", "write_command": "python3 proof/build_cycle_179_p2_ray_quotient_v1.py --write", "check_command": "python3 proof/build_cycle_179_p2_ray_quotient_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_179_p2_ray_quotient_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
