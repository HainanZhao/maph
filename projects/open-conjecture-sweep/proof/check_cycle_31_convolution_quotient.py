#!/usr/bin/env python3
"""Audit Cycle 31's exact additive-convolution splitting witness."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle31-convolution-quotient"


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == "CONTAINED" and independent["status"] == "PASS"
    assert primary["atom_count"] == 1390
    assert primary["atom_size_counts"] == {"1": 2, "2": 1386, "6": 2}
    assert primary["singleton_profiles_checked"] == independent["singleton_profiles_checked"] == 2780
    assert primary["pair_profiles_checked"] == independent["pair_profiles_to_first_split"] == 198
    assert primary["pair_target_evaluations"] == independent["target_evaluations_to_first_split"] == 395
    witness = primary["first_splitting_witness"]
    replay = independent["first_splitting_witness"]
    expected = {
        "left_atom_index": 1,
        "left_atom": [1, 2785],
        "right_atom_index": 198,
        "right_atom": [198, 2588],
        "target_atom_index": 199,
        "target_atom": [199, 597, 995, 1791, 2189, 2587],
        "sum_multiplicities": [[197, 1], [199, 1], [2587, 1], [2589, 1]],
    }
    for key, value in expected.items():
        assert witness[key] == replay[key] == value
    assert (witness["left_point"], witness["left_value"], witness["right_point"], witness["right_value"]) == (199, 1, 597, 0)
    assert replay["values_on_target"] == [[199, 1], [597, 0], [995, 0], [1791, 0], [2189, 0], [2587, 1]]
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "the sealed 1390-atom p199 partition only",
        "singleton_profiles": 2780,
        "first_splitting_pair_profile": 198,
        "first_splitting_target_evaluation": 395,
        "convolution_quotient": False,
        "independent_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
