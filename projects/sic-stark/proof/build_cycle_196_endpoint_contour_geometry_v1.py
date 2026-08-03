#!/usr/bin/env python3
"""Seal Cycle 196/B033's exact finite-pole endpoint-contour geometry."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-196-b033-endpoint-contour-geometry-v1.json"
INPUTS = {
    "prior_finite_residues": (ROOT / "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json", "7e4d7615414dbf49627c9ea9cfa2b5e0191502cd6a6915fa93d13085cd50ae8d"),
    "preregistration": (ROOT / "docs/cycle-196-b033-endpoint-contour-geometry-preregistration-v1.md", "9887325d21f58c612149fdd0576a3f3f1fd93978b6d32cf3e89b9ab505cde213"),
    "prior_replay": (ROOT / "proof/verify_cycle_195_finite_anti_residue_sum.py", "df7ccb34c408ce29d453373ed8811c7fcca435e101827d660db534030ef36d2b"),
    "replay": (ROOT / "proof/verify_cycle_196_endpoint_contour_geometry.py", "aa8a98e94b19738040ae7ead70615b53c9e16a760fd67383b9d61de3a3107577"),
    "regression_test": (ROOT / "tests/test_cycle_196_endpoint_contour_geometry.py", "4f850c2da8e40dd5f3757859a4b106792ccffba1ee0a4f4678f05e25e8ca55ab"),
    "prototype": (ROOT / "discovery/cycle-196-b033-endpoint-contour-geometry-prototype-v1.json", "168126057d18838a724aff048f05a1f620ab42596ca51cd8979e6ab4bbc1af7b"),
    "beta_kernel_match": (ROOT / "scripts/dimension_six_beta_kernel_match.py", "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27"),
    "beta_fourier": (ROOT / "scripts/dimension_six_beta_fourier.py", "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 196 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-196-b033-endpoint-contour-geometry-prototype-v1.json").read_text())
    geometry = result["attracting_path_geometry"]
    cones = result["kernel_pole_cones"]
    jumps = result["anti_residue_jumps"]
    regular = result["regular_part_boundary"]
    require(geometry["Re_omega_1_lower_bound"] == 55, "path cone bound drift")
    require(geometry["Re_Q_lower_bound"] == 56, "Q bound drift")
    require(len(cones["records"]) == 24 and cones["total_finite_kernel_crossings"] == 0, "kernel crossing drift")
    require(jumps["finite_anti_residue_jump_vector"] == [0] * 6, "anti jump drift")
    require(regular["T_to_infinity_limit"] == "OPEN", "infinity boundary drift")
    require(not regular["endpoint_continuation_claimed"], "endpoint scope drift")
    return {
        "artifact_id": "cycle-196-b033-endpoint-contour-geometry-v1",
        "cycle": 196,
        "budget_ordinal": "B033",
        "epistemic_status": "PROVED",
        "status": "SEALED_ENDPOINT_CONTOUR_FINITE_POLE_FREE_INFINITY_OPEN",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "On the frozen attracting A_6 segment, Re(omega_1)>=55 and the source central contour Re(y)=Re(Q)/2 separates the left and right true-pole cones for every m mod24. It has zero finite kernel crossings, and the six finite anti-residue jumps are all zero. The remaining obstruction is solely the unproved regular-part limit at imaginary infinity."},
        "attracting_path_geometry": geometry,
        "kernel_pole_cones": cones,
        "anti_residue_jumps": jumps,
        "regular_part_boundary": regular,
        "gate_outcome": {
            "d6_interface": "FINITE_POLE_FREE_ENDPOINT_CONTOUR_PROVED_INFINITY_FINITE_PART_OR_DISTRIBUTIONAL_CONTROL_REQUIRED",
            "resolved_class": "fixed source central-contour finite-pole geometry and finite anti-residue jump bookkeeping",
            "remaining_bottleneck": "Choose and prove a source-derived Abel/Fresnel/distributional rule controlling the central-contour regular part at imaginary infinity, then compare its RM endpoint value before any AFK identification.",
            "disallowed_pseudo_progress": ["calling zero finite jumps endpoint continuation", "calling a symmetric truncation its T-to-infinity limit", "fitting a regulator or counterterm", "claiming AFK, boundary, fusion, Stark, or TCC"],
        },
        "next_target": result["next_unresolved_boundary"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal B033/C196 as PROVED only for the frozen contour geometry, pole separation, and zero finite residue-jump vector.",
            "known_flaw": "Absence of finite pole crossings supplies no control of contour tails at imaginary infinity and therefore no Abel, distributional, or endpoint continuation.",
            "falsifier": "Any path-bound, divisor-orientation, central-line, reflected-pole, anti-pole, crossing-count, or replay discrepancy.",
            "next_action": "Open a new cycle freezing an Abel regulator and test-function space, then prove uniform vertical-tail bounds for the Gamma_M kernel along gamma(s) sufficient to pass first T-to-infinity and then the endpoint limit.",
            "adopted": True,
            "reason": "The all-label source-divisor ledger proves the preregistered finite-pole criterion while the artifact explicitly leaves the analytic-infinity limit open.",
        },
        "preregistration_preflight": {"cycle": 196, "manifest_sha256": sha256(ROOT / "docs/cycle-196-b033-endpoint-contour-geometry-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-196-b033-endpoint-contour-geometry-preregistration-v1.md --expected-cycle 196 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_196_endpoint_contour_geometry.py --output discovery/cycle-196-b033-endpoint-contour-geometry-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_196_endpoint_contour_geometry.py tests/test_cycle_195_finite_anti_residue_sum.py", "write_command": "python3 proof/build_cycle_196_endpoint_contour_geometry_v1.py --write", "check_command": "python3 proof/build_cycle_196_endpoint_contour_geometry_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_196_endpoint_contour_geometry_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
