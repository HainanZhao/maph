#!/usr/bin/env python3
"""Seal homogeneous anisotropic/isotropic nonvanishing at width three."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_homogeneous_w3 import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-14-b14-homogeneous-w3-v1.json"
HASHES: dict[str, tuple[str, str]] = {
    "preregistration": (
        "discovery/cycle-14-homogeneous-locus-preregistration.md",
        "6f11be9face086fe179d2da8b040ecf767a5c83e10b295caaaa5602c3b35773e",
    ),
    "machine_preregistration": (
        "discovery/cycle-14-homogeneous-locus-preregistration.json",
        "7471bdd54de3b2671390c9f5a4ff71bc3dc36655207dc73c5eb7356574651d60",
    ),
    "failure_ledger": (
        "discovery/failure-ledger-cycle14.md",
        "3a896a46f1733894920fbc7a4b7cec084d66262832ea44ff0be4e126c4830c35",
    ),
    "proof": (
        "proof/lane_b_homogeneous_w3_proof.md",
        "2a048eb2c420ea97a3ce332e2bc92901a799741836114386d48d7ddb8f025659",
    ),
    "verifier": (
        "proof/verify_lane_b_homogeneous_w3.py",
        "461e07d0032f08c629002358d7d869b088054e8628bb2b2af7e88d23be66bf75",
    ),
    "tests": (
        "tests/test_lane_b_homogeneous_w3.py",
        "42e18b2c6810828655d1df016293c6644f277b8f53e8372ebee00e8cb956f5ea",
    ),
    "transfer_source": (
        "proof/lane_b_width4_character_transfer.cpp",
        "dd7f5f3e381ae3759eaa8d86a930d968ab3ac75773646ba69c52d59f77e1d940",
    ),
    "paired_cycle_dependency": (
        "proof/verify_g1_paired_cycle_w3.py",
        "5ceee917c21e24670a09b5bfb03176f87b814ecf55b470eb05b838e8bb06156b",
    ),
    "canonical_dependency": (
        "proof/verify_lane_b_universal_canonical_ranks.py",
        "d631149c9429d921359a6a67042b0e476cb681b9bc8aa63de42bcac6503662b0",
    ),
    "width_dependency": (
        "proof/verify_lane_b_width_scaling.py",
        "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4",
    ),
    "frontier_dependency": (
        "proof/verify_lane_b_arbitrary_width_frontier.py",
        "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615",
    ),
    "conventions": (
        "src/conventions.py",
        "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3",
    ),
    "embedding": (
        "src/lane_b_universal_embedding.py",
        "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430",
    ),
    "independent_rank_control": (
        "artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json",
        "3caa6e9e2a170b6de7660a158719c762d733dcc9f022707143d6ff2aaa80320c",
    ),
    "requirements": (
        "requirements.txt",
        "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a",
    ),
    "scaffold": (
        "proof/cycle_seal_v1.py",
        "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163",
    ),
}


EXPECTED = {
    ("anisotropic", (2, 3, 5), 1_000_000_007): 907493871,
    ("anisotropic", (7, 11, 13), 1_000_000_007): 448249861,
    ("anisotropic", (17, 19, 23), 1_000_000_007): 641093518,
    ("isotropic", (2, 2, 2), 1_000_000_007): 125206307,
    ("isotropic", (3, 3, 3), 1_000_000_007): 811017752,
    ("isotropic", (5, 5, 5), 1_000_000_007): 798579921,
    ("anisotropic", (2, 3, 5), 1_000_000_009): 154871535,
    ("anisotropic", (7, 11, 13), 1_000_000_009): 721745845,
    ("anisotropic", (17, 19, 23), 1_000_000_009): 194264410,
    ("isotropic", (2, 2, 2), 1_000_000_009): 463248719,
    ("isotropic", (3, 3, 3), 1_000_000_009): 761169288,
    ("isotropic", (5, 5, 5), 1_000_000_009): 115825239,
}


def _prior_control() -> dict[str, object]:
    data = json.loads(
        (ROOT / "artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json").read_text()
    )
    cases = data["exact_replay"]["rank_certificates"]["cases"]
    selected = [
        case for case in cases
        if case["shape"] == [10, 3, 3]
        and case["regime"] in (
            "homogeneous_anisotropic_(2,3,5)", "homogeneous_isotropic_t=2"
        )
    ]
    if len(selected) != 4 or any(max(case["canonical_binary_rank_profile"]) != 256 for case in selected):
        raise RuntimeError("independent homogeneous rank control changed")
    return {
        "artifact": "cycle-7-b7-lane-b-arbitrary-width-closure-v1.json",
        "cases": [
            {
                "prime": case["prime"],
                "regime": case["regime"],
                "maximum_rank": max(case["canonical_binary_rank_profile"]),
            }
            for case in selected
        ],
        "role": "independent rank-revealing full-tensor control; it did not select the Cycle 14 frozen minor",
    }


def payload() -> dict[str, object]:
    frozen = freeze_inputs(
        ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
    )
    replay = verify()
    benchmark = replay.pop("runtime")
    for row in replay["rows"]:
        row.pop("wall_seconds")
    observed = {
        (row["locus"], tuple(row["point"]), row["prime"]): row["determinant"]
        for row in replay["rows"]
    }
    if observed != EXPECTED:
        raise RuntimeError("homogeneous determinant residues changed")
    if not replay["anisotropic_nonzero_polynomial"] or not replay["isotropic_nonzero_polynomial"]:
        raise RuntimeError("Branch A nonvanishing regressed")
    return {
        "artifact_id": "cycle-14-b14-homogeneous-w3-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B14",
        "cycle": 14,
        "status": "SEALED",
        "epistemic_status": "PROVED_BY_EXACT_TWO_PRIME_SPECIALIZATION",
        "record_type": "HOMOGENEOUS_WIDTH_THREE_NONVANISHING",
        "outcome": (
            "The frozen Cycle 8 paired-cycle determinant is nonzero on both "
            "the homogeneous anisotropic width-three locus and its isotropic line."
        ),
        "gate_outcome": "T4_BRANCH_A_COMPLETE",
        "claim_boundary": replay["claim_boundary"],
        "theorem": {
            "anisotropic": "rank 256 on a nonempty Zariski-open subset",
            "isotropic": "rank 256 outside a finite algebraic exceptional set",
            "isotropic_exception_cardinality_upper_bound": 51456,
            "particular_temperature_claim": False,
            "arbitrary_width_homogeneous_claim": False,
        },
        "exact_replay": replay,
        "independent_control": _prior_control(),
        "benchmark": {
            "preseal_wall_seconds": benchmark["wall_seconds"],
            "python": benchmark["python"],
            "note": "volatile timing is excluded from deterministic replay",
        },
        "frozen_hashes": frozen,
        "runtime": check_runtime("cycle-14-homogeneous-w3"),
        "sealer": {
            "path": "proof/build_cycle14_homogeneous_w3.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/verify_lane_b_homogeneous_w3.py",
            "tests": "python3 -m unittest tests/test_lane_b_homogeneous_w3.py -v",
            "artifact_check": "python3 proof/build_cycle14_homogeneous_w3.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
