#!/usr/bin/env python3
"""Seal the correction to the Cycle 4 canonical-handle construction."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.verify_lane_b_cochain_gauge import verify  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-4-b4-lane-b-canonical-handle-correction-v2.json"
HASHES: dict[str, tuple[str, str]] = {
    "superseded_artifact": ("artifacts/cycle-4-b4-lane-b-bounded-theta-transfer-v1.json", "3bbc61164f68eaaed3b1babcdd9e782da06aa0ccfc90637f81de27501c7dcb8d"),
    "correction_report": ("docs/cycle4-canonical-handle-correction.md", "3e161e7dd3ac2fb861026e44a377f12436ddda505eb7de310bb3360829fdf9ed"),
    "proof": ("proof/lane_b_cochain_gauge_proof.md", "da33907099dfc2a345ede511430fcf8b3da106480f42feb6a0d6c98c2674477b"),
    "cochain_module": ("src/lane_b_cochain_gauge.py", "9f54aa39773cc6e675e21a9ba3ba8b26fd9d2d851c385e658bef06f644bc76fc"),
    "recursive_family": ("src/lane_b_recursive_family.py", "2c945132811228cb33acc8a98d1602d3e7133c474b219ceaab73a4e8e72b171e"),
    "verifier": ("proof/verify_lane_b_cochain_gauge.py", "bb6db11ac8e9a800c883d30c5368917acfd9fbb600fb42e55800aa6d9bc49a08"),
    "intersection_verifier": ("proof/verify_lane_b_intersection.py", "1b6b59d188dfdc033b1c37c0059ee3e068181c458a9da028d0a8e0f1a273abd9"),
    "label_verifier": ("proof/verify_lane_b_width_scaling.py", "2cb86284481e69b26bea8d9f7a52e91664a7b2b7869cdf1915795bef18926ae4"),
    "tests": ("tests/test_lane_b_cochain_gauge.py", "7fafedc1794792c9abaaf8eb9bb656bbb21a7d941498ed29aaa987af85d4e545"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload() -> dict[str, object]:
    correction = verify()
    if not correction["semantic_coordinate_checks"]["canonical_symplectic_intersection"]:
        raise RuntimeError("corrected transport is not symplectic")
    return {
        "artifact_id": "cycle-4-b4-lane-b-canonical-handle-correction-v2",
        "author": "Hainan Zhao",
        "budget_ordinal": "B4",
        "cycle": 4,
        "version": 2,
        "status": "SEALED_CORRECTION",
        "epistemic_status": "PROVED",
        "record_type": "POST_SEAL_CANONICAL_COORDINATE_CORRECTION",
        "supersedes_affected_claims_in": "cycle-4-b4-lane-b-bounded-theta-transfer-v1",
        "error": (
            "The old verifier proved d=old_last+raw_new_a was orthogonal, but did not "
            "check that c=raw_new_b was orthogonal to the old homology space. It is not."
        ),
        "correction": "c=old_second_last+raw_new_b",
        "affected_claims": (
            "Withdraw the Cycle 4 canonical-F 1024/2048 rank theorem and the literal "
            "c=raw_new_b statement. Genus, face surgery, carrier dimension, relative defect, "
            "and character-transfer identities are unaffected."
        ),
        "replacement_boundary": (
            "Cycle 6 separately proves and certifies the corrected canonical rank closure. "
            "This record does not modify the immutable Cycle 4 artifact."
        ),
        "exact_replay": correction,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-4-lane-b-canonical-handle-correction-v2"),
        "sealer": {"path": "proof/build_cycle4_lane_b_canonical_correction_v2.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "correction": "python3 proof/verify_lane_b_cochain_gauge.py",
            "tests": "python3 -m unittest tests/test_lane_b_cochain_gauge.py -v",
            "artifact_check": "python3 proof/build_cycle4_lane_b_canonical_correction_v2.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
