#!/usr/bin/env python3
"""Seal the corrected width-three cochain closure and saturation certificates."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_cochain_gauge import verify as verify_upper  # noqa: E402
from proof.verify_lane_b_longitudinal_saturation import verify as verify_lower  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-6-b6-lane-b-longitudinal-saturation-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "correction": ("artifacts/cycle-4-b4-lane-b-canonical-handle-correction-v2.json", "03c795cb7452488c99ecc77f41f40e6e92499e34c65452cfeafa08df22361ec1"),
    "prior": ("artifacts/cycle-5-b5-lane-b-width-rank-audit-v1.json", "89307d257a0e8263c62e3e5948707ac656657c015fb69d31a96d32917718a150"),
    "selection": ("discovery/cycle-6-b6-longitudinal-saturation-selection.md", "f319a9cb1a0a53a3e32c58003daef01db13b1381610b909e595a74b6bc72b9b9"),
    "failure_ledger": ("discovery/failure-ledger-cycle6.md", "9a79a84eba22ac83ff973a2d315907b24a5ffbb236f98cde24aa557711562639"),
    "report": ("docs/cycle6-lane-b-longitudinal-saturation.md", "817774b02e11e65d0a35ed6b09b51413f035e7a222e05a208bf54113f0cbe646"),
    "proof": ("proof/lane_b_cochain_gauge_proof.md", "da33907099dfc2a345ede511430fcf8b3da106480f42feb6a0d6c98c2674477b"),
    "cochain_module": ("src/lane_b_cochain_gauge.py", "9f54aa39773cc6e675e21a9ba3ba8b26fd9d2d851c385e658bef06f644bc76fc"),
    "upper_verifier": ("proof/verify_lane_b_cochain_gauge.py", "bb6db11ac8e9a800c883d30c5368917acfd9fbb600fb42e55800aa6d9bc49a08"),
    "lower_verifier": ("proof/verify_lane_b_longitudinal_saturation.py", "6ac976394a4bae5dbd5b7869b3affc675499dd5128f118c90ea5f6ae3f911fef"),
    "gauge_engine": ("proof/lane_b_gauge_reduced_character_transfer.cpp", "504d8d60e2982b48be5d8cc3af5495615877c5ea5c8492e64e9c0023720ccd91"),
    "projected_minor_engine": ("proof/lane_b_modular_determinant.cpp", "6103696e14c9b36ccd434670ec772711323152bf4fd61699f36bc1c511f2a804"),
    "legacy_engine": ("proof/lane_b_width4_character_transfer.cpp", "dd7f5f3e381ae3759eaa8d86a930d968ab3ac75773646ba69c52d59f77e1d940"),
    "tests": ("tests/test_lane_b_cochain_gauge.py", "7fafedc1794792c9abaaf8eb9bb656bbb21a7d941498ed29aaa987af85d4e545"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    upper = verify_upper()
    lower = verify_lower()
    theorem = upper["rank_theorem"]
    saturation = lower["saturation"]
    if theorem["F_pair_upper"] != 256 or theorem["F_internal_upper"] != 256:
        raise RuntimeError("cochain upper-bound regression")
    if saturation["R_infinity_pair_w3"] != 256 or saturation["R_infinity_internal_w3"] != 256:
        raise RuntimeError("saturation regression")
    return {
        "artifact_id": "cycle-6-b6-lane-b-longitudinal-saturation-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B6",
        "cycle": 6,
        "status": "SEALED",
        "epistemic_status": "MIXED_PROVED_AND_CERTIFIED_NUMERICAL",
        "record_type": "LANE_B_CANONICAL_COHCHAIN_CLOSURE_AND_SATURATION",
        "outcome": (
            "In corrected canonical handles, every pair and internal cut of the complete "
            "width-three spin-structure tensor factors through the ordinary 256-state even "
            "frontier. Exact projected minors prove both saturation suprema equal 256."
        ),
        "gate_outcome": "B1_FIXED_TOPOLOGICAL_OVERHEAD_ZERO_BEYOND_PHYSICAL_CARRIER_AT_W3",
        "claim_boundary": (
            "This is an all-length theorem only for the fixed 3x3 tube family. It does not "
            "prove arbitrary-width closure, a sub-area cubic carrier, a thermodynamic limit, "
            "a critical temperature, or a solution of the three-dimensional Ising model."
        ),
        "correction_dependency": "cycle-4-b4-lane-b-canonical-handle-correction-v2",
        "exact_replay": {"upper_factorization": upper, "rank_certificates": lower},
        "principal_replay_benchmark": {
            "command": "python3 proof/verify_lane_b_longitudinal_saturation.py",
            "wall_seconds": 775.45,
            "peak_rss_kib": 401188,
            "threads": 3,
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-6-lane-b-longitudinal-saturation"),
        "sealer": {"path": "proof/build_cycle6_lane_b_longitudinal_saturation.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "upper": "python3 proof/verify_lane_b_cochain_gauge.py",
            "lower": "python3 proof/verify_lane_b_longitudinal_saturation.py",
            "tests": "python3 -m unittest tests/test_lane_b_cochain_gauge.py -v",
            "artifact_check": "python3 proof/build_cycle6_lane_b_longitudinal_saturation.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
