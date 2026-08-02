#!/usr/bin/env python3
"""Seal Cycle 181 common-intercept stable packet reduction."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-181-common-intercept-packet-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-181-common-intercept-packet-preregistration-v1.md", "936a5fecb9ac0d62afc26681d6f30186f2336720c047ad3ae69f0c29e2e8cd41"),
    "document": (ROOT / "docs/cycle-181-common-intercept-packet-v1.md", "566a21ff7bc20af6979d9967b42cb993de86e3ab5bf560a1d6f92127238927b9"),
    "conventions": (ROOT / "conventions/common_intercept_packet_v1.py", "0834c169168e345e3307926e31ab0ac0ee5b7bae3d721ef0ccddc389bec65333"),
    "tests": (ROOT / "tests/test_cycle_181_common_intercept_packet_v1.py", "13b7d06a3e11f135039ca187d410bc6adcefae19d3bb16d88725d8f4c4ddbd6f"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "cycle180": (ROOT / "artifacts/cycle-180-cross-label-pair-determinant-v1.json", "cdf34df41021fd1b0eab05f34202b23ea3fec96f010fbf3f0467328084b0d91a"),
}


def exact_json(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [exact_json(item) for item in value]
    return value


def exact_checks() -> dict[str, object]:
    module = __import__("conventions.common_intercept_packet_v1", fromlist=["verify_all"])
    rows = module.verify_all()
    sample = rows["samples"]
    rectangle = sample["rectangle"]
    require(rectangle["intercept_determinant"] == 0, "intercept exactification")
    require(rectangle["common_intercept"]["value"] == Fraction(-1, 2), "common intercept")
    require(rectangle["slope_determinant"] == 2, "retained slope determinant")
    require(rectangle["phase_state"]["beta"] == Fraction(1, 2), "retained beta")
    require(sample["eligible_intercepts"] == 1 and sample["packet_lower_bound"] == 33, "packet replay")
    return exact_json(rows)


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle180"][0], "SEALED_NONZERO_CROSS_LABEL_PAIR_DETERMINANT_AND_STABLE_SHELL_REDUCTION")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="common_intercept_packet_v1")
    return {
        "artifact_id": "cycle-181-common-intercept-packet-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COMMON_INTERCEPT_EXACTIFICATION_AND_STABLE_PACKET_REDUCTION",
        "claim_boundary": "This proves exact common-intercept compatibility and a large stable common-intercept packet under the Cycle-180 critical light branch. It proves no in-packet upper bound, aggregate recurrence, density gain, or interval result.",
        "runtime": check_runtime("Cycle 181"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "common_intercept_exactification": {"epistemic_status": "PROVED", **exact_json(theorem)},
        "stable_packet_reduction": {
            "epistemic_status": "PROVED",
            "statement": "When 10*C*H^2/X<1 and 5*C*H/X<1/2, every Cycle-180 stable rectangle has a shared reduced intercept rho=p/v with v dividing both pair gaps and |p+v*beta|<=5*C*H/X. Thus at most H intercept packets occur and a stable population >=X^(32/25)/64 yields one complete labelled packet >=X^(21/25)/64.",
        },
        "mentor_checkpoint": {
            "recommendation": "APPROVE SEAL",
            "known_flaw": "The first-row height factor changes the exactification constants from the initial 3/6 proposal to 5/10; the corrected cutoff is frozen in the preregistration.",
            "resolution": "The height ledger explicitly uses h1,h2,s1,s2 in [H,2H], giving the safe 10*C*H^2/X cutoff. Exactification is global; only the packet pigeonhole is applied after the Cycle-180 stable split.",
            "next_action": "Analyze the X^(21/25) common-intercept packet through v|d,e, retained slopes, and base-row congruences, or construct its actual saturator.",
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Prove a coefficient-preserving upper bound inside a fixed common-intercept stable packet, or construct a nonrational actual saturator for such a packet. A packet decomposition alone is not recurrence, density, or interval progress.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "exact_replay": exact_checks(),
        "replay": {
            "write_command": "python3 proof/build_cycle_181_common_intercept_packet_v1.py --write",
            "check_command": "python3 proof/build_cycle_181_common_intercept_packet_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_181_common_intercept_packet_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 181", output=OUTPUT, payload_factory=seal))
