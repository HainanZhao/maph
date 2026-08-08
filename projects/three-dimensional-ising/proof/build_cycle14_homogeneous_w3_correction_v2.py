#!/usr/bin/env python3
"""Correct Cycle 14 by removing volatile timing from deterministic replay."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.build_cycle14_homogeneous_w3 import EXPECTED, HASHES, _prior_control  # noqa: E402
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_homogeneous_w3 import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-14-b14-homogeneous-w3-v2.json"
EXTRA = {
    "correction": ("discovery/cycle14-homogeneous-seal-correction.md", "f05646b90cf3b01044dac8600e1d78411395e6882bd837127199d977ddd00574"),
    "v1_artifact": ("artifacts/cycle-14-b14-homogeneous-w3-v1.json", "62cf5108cb41ed46f8f4125723dc091729e03795f379387ee31ba43a5a393098"),
    "v1_builder": ("proof/build_cycle14_homogeneous_w3.py", "d0cfbc3d5519a2168f0b9e41d2a2be64bf7f7891b5cb84f314c271e9de554eea"),
}


def payload():
    inputs = {**HASHES, **EXTRA}
    frozen = freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in inputs.items()})
    replay = verify()
    replay.pop("runtime")
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
        "artifact_id": "cycle-14-b14-homogeneous-w3-v2",
        "author": "Hainan Zhao",
        "budget_ordinal": "B14",
        "cycle": 14,
        "status": "SEALED",
        "supersedes": "cycle-14-b14-homogeneous-w3-v1",
        "correction": {
            "error": "v1 included a newly measured wall time in deterministic payload construction",
            "affected_claims": "none",
            "mathematical_fields_changed": False,
        },
        "epistemic_status": "PROVED_BY_EXACT_TWO_PRIME_SPECIALIZATION",
        "record_type": "HOMOGENEOUS_WIDTH_THREE_NONVANISHING_CORRECTION",
        "outcome": "The frozen Cycle 8 paired-cycle determinant is nonzero on both the homogeneous anisotropic width-three locus and its isotropic line.",
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
            "canonical_preseal_wall_seconds": 134.689078,
            "python": "3.12.3",
            "note": "fixed descriptive v1 measurement; current replay timings are excluded"
        },
        "frozen_hashes": frozen,
        "runtime": check_runtime("cycle-14-homogeneous-w3-v2"),
        "sealer": {"path": "proof/build_cycle14_homogeneous_w3_correction_v2.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "verification": "python3 proof/verify_lane_b_homogeneous_w3.py",
            "tests": "python3 -m unittest tests/test_lane_b_homogeneous_w3.py -v",
            "artifact_check": "python3 proof/build_cycle14_homogeneous_w3_correction_v2.py --check"
        }
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
