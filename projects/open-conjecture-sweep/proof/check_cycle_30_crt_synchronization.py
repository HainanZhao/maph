#!/usr/bin/env python3
"""Exact output audit for Cycle 30's CRT synchronization algebra."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle30-crt-synchronization"


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == independent["status"] == "PASS"
    h11 = primary["h11"]
    assert (h11["algebra"]["generated_mask_count"], h11["algebra"]["atom_count"], h11["algebra"]["atom_size_counts"]) == (20, 23, {"1": 2, "2": 21})
    assert (h11["lifted_assignments"], h11["raw_full_covers"], h11["quotient_full_covers"], h11["gcd_admissible_assignments"], h11["retained_improper_bases"]) == (64000, 720, 720, 32000, 0)
    assert set(h11["parity_signature_counts"].values()) == {8000}
    assert independent["h11"]["atom_count"] == 23
    assert independent["h11"]["atom_size_counts"] == {"1": 2, "2": 21}

    p199 = primary["p199"]
    algebra = p199["algebra"]
    assert (p199["base_index"], p199["leaf_ordinal"], p199["times"]) == (4, 78, 2786)
    assert p199["allowed_digit_counts"] == [6, 6, 7] + [14] * 10
    assert (p199["allowed_speed_count"], p199["control_tuple_count"], p199["control_full_cover_count"]) == (159, 147, 0)
    assert (algebra["generated_mask_count"], algebra["atom_count"], algebra["atom_size_counts"]) == (1386, 1390, {"1": 2, "2": 1386, "6": 2})
    assert algebra["strategic_threshold"] == 1393 and algebra["strategic_outcome"] == "ADVANCE"
    assert {row["gcd"] for row in algebra["gcd_strata"]} == {1, 2, 7, 14}
    assert {row["generated_subgroup_size"] for row in algebra["gcd_strata"]} == {1188}
    replay = independent["p199"]
    assert replay["atom_count"] == 1390
    assert replay["negation_orbit_count"] == 1394
    assert replay["beyond_negation_atom_reduction"] == 4
    assert replay["merged_negation_orbit_atoms"] == [
        [199, 597, 995, 1791, 2189, 2587],
        [398, 796, 1194, 1592, 1990, 2388],
    ]
    convolution = json.loads((OUT / "convolution-result.json").read_text(encoding="utf-8"))
    convolution_independent = json.loads((OUT / "convolution-independent.json").read_text(encoding="utf-8"))
    assert convolution["status"] == convolution_independent["status"] == "PASS"
    assert convolution["first_splitting_witness"] is None
    assert (convolution["generator_count"], convolution["exceptional_atom_count"], convolution["planned_profiles"], convolution["checked_profiles"]) == (1386, 2, 2772, 2772)
    assert convolution["incidence_checks"] == 46336752
    assert (convolution_independent["profiles_checked"], convolution_independent["distinct_compressed_profiles"], convolution_independent["incidence_additions"]) == (2772, 2079, 6623100)
    assert convolution_independent["failures"] == []
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "transport theorem plus complete H11 and one p199 target only",
        "h11_atoms": 23,
        "p199_atoms": 1390,
        "p199_negation_orbits": 1394,
        "p199_beyond_negation_reduction": 4,
        "exceptional_convolution_profiles": 2772,
        "exceptional_convolution_distinct_profiles": 2079,
        "exceptional_convolution_action": "PASS",
        "independent_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
