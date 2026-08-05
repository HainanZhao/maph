#!/usr/bin/env python3
"""Seal Cycle 46's owner-star Cech classification and coordinate no-go."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_46_cech import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle46-global-cech-quotient"
OUTPUT = ROOT / "artifacts/cycle-46-b046-lrc-global-cech-quotient-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-46-b046-lrc-global-cech-quotient-preregistration-v1.md", "0d832cb4da242f18d6c53a905b3f4a6acf330430fc7f82c0344ee441152842f6"),
    "cycle45_artifact": (ROOT / "artifacts/cycle-45-b045-lrc-critical-projection-v1.json", "bd9759df06e5f32a46f5f0d199bfcc68ce190921ff780cb79672203a29d087a5"),
    "idea_selection": (ROOT / "discovery/cycle46_global_quotient_idea_selection.md", "8bc3a095139f46fa164a2127895e0172407f5ae09c2d5376f4f596e68c330448"),
    "generic_complex": (ROOT / "discovery/lrc_cech_total.py", "91e267ee6f661f632bc417a3cbdf76453c4a4f934d12717c9ecbb2363ce19272"),
    "actual_engine": (ROOT / "discovery/lrc_cech_actual.py", "ffa6b7f6d7623505b1de8dc301b7d7b0b814e878a833bffcb1fd22f76a90a166"),
    "actual_result": (OUT / "actual-quotient-localized.json", "c00a78d4767cf7acc3970363cbf9ced9cb571086cd5bb3c83da00af9cfc919ce"),
    "actual_timing": (OUT / "run-actual-quotient-localized.time", "08de2c42e2b56d4ab32b41c2d90b62de6e84af8784cf3d8aa658f6604a43cd25"),
    "target_cache": (OUT / "target-structure-cache.json", "75a59628e0ebfae6d646a5f51108a066b6f43ccf9de659a93dd2ccadce08dbdf"),
    "control_engine": (ROOT / "discovery/lrc_cech_controls.py", "5a3c759ae112d5a9d11edc7465c4438888a98859aecbc7c538b893bfa13ab03f"),
    "control_result": (OUT / "generic-controls.json", "db5c95a58a579528d234dde3961d4bb40bf66ac388522bf8b3cc29a37b0461e3"),
    "control_timing": (OUT / "run-injected-controls.time", "0d7bf8dc0ab90c15b9f4d1c73de34b40f692ec12c433afd293bf0ef889478623"),
    "independent_replay": (ROOT / "proof/replay_cycle_46_cech_independent.py", "9c118b9be1b5662bb6b8898b8a099fd4439245dacadc49ed74981ba19ef4f761"),
    "independent_result": (OUT / "independent-replay.json", "8bfb5ee6cd5039f0e8272f374ad6e63b6658c15762bc944bd0856f7440223890"),
    "independent_timing": (OUT / "run-independent.time", "6485caa9e2c7f5ef3c251527d51ff38d62fbec97d1eb4a5514d7df1f455ab021"),
    "soundness": (ROOT / "proof/cycle_46_cech_soundness.md", "3b530bc665f4a651d2dc99165c4e601d5fa7274025bb5a75987c1c58e83043ce"),
    "audit": (ROOT / "proof/check_cycle_46_cech.py", "a30e9e3def1d875e965f793a00defd7b386b4cfbaa5d4090d7d97c6e796fac11"),
    "test": (ROOT / "tests/test_cycle_46_cech.py", "b4d084f88604c3167c7c2da10cc8acdaef4ddc1b5faaf9c38a4d60899771f8fa"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    actual = json.loads((OUT / "actual-quotient-localized.json").read_text())
    independent = json.loads((OUT / "independent-replay.json").read_text())
    return {
        "artifact_id": "cycle-46-b046-lrc-global-cech-quotient-v1",
        "budget_ordinal": "B046",
        "cycle": 46,
        "record_type": "PROVED_CECH_CLASSIFICATION_AND_COORDINATE_NO_GO",
        "recorded_at_utc": "2026-08-05T06:30:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The owner-star Cech total complex gives a canonical exact lift and correctly classifies all 457 frozen Cycle 45 residuals as rational boundaries. Its augmentation is a chain resolution and homology isomorphism, so this quotient is exactly a coordinate reformulation of ordinary boundary membership, not the missing global degree-four closure mechanism.",
        "claim_boundary": "The generic equivalence, finite 457-row classification, and coordinate-reformulation no-go are proved. This does not give a globally compatible shared-face section, classify all p199 type quadruples, certify a leaf, or prove LRC(13).",
        "generic_theorem": {
            "statement": "The least-owner horizontal cone produces a linear total-cycle lift L, and augmentation induces a homology isomorphism from the owner-star Cech total complex to the cover union.",
            "consequence": "For a covered cycle z, L(z) is a total boundary exactly when z is an ordinary boundary in the owner-star union.",
            "coefficient_ring": "Q",
        },
        "actual_corpus": {
            "residuals": actual["selected_residuals"],
            "outcomes": checked["outcomes"],
            "pivot_counts": checked["pivot_counts"],
            "target_types": actual["target_types"],
            "target_pair_classes": actual["target_pair_classes"],
            "target_triple_classes": actual["target_triple_classes"],
            "reconstructed_deleted_pairs": actual["reconstructed_deleted_pairs"],
            "reconstructed_deleted_triples": actual["reconstructed_deleted_triples"],
            "witness_nonzero_range": [checked["minimum_witness_nonzero"], checked["maximum_witness_nonzero"]],
            "witness_size_classes": checked["witness_size_classes"],
            "maximum_coefficient_bits": checked["maximum_coefficient_bits"],
            "solver_routes": {"LOCAL_INCIDENCE": 425, "FULL_EXACT": 32, "LOCAL_RADIUS_1": 401, "LOCAL_RADIUS_2": 24},
        },
        "controls": {
            "filled_tetrahedron": "BOUNDARY",
            "unfilled_tetrahedron_sphere": "UNCOVERED",
            "covered_suspension_sphere": "NONBOUNDARY_WITH_EXACT_DUAL",
        },
        "independent_replay": {
            "status": independent["status"],
            "records": independent["selected_records"],
            "solver_classes": independent["selection_classes"],
            "route": "outcome-blind row selection, raw type/signature reconstruction, reversed orientation, and highest-pivot exact elimination",
        },
        "structural_no_go": {
            "closed_family": "owner-star Cech localization as a stronger global quotient",
            "reason": "The total complex is chain-resolved by augmentation; it changes coordinates but adds no relations.",
            "category_guard": "Cycle 41 lower marginal relations cannot be inserted as degree-four boundary columns without a proved graded descent map.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEAL_COORDINATE_NO_GO_AND_OPEN_GLOBAL_AFFINE_DESCENT",
            "strongest_flaw": "The next quotient could invent or erase overlap if repeated faces are identified without a raw-label descent theorem.",
            "primary_decision": "Require a genuinely new shared-face state space and exact descent equivalence; do not rerun local boundary membership under another cover.",
            "next_question": "Do locally fillable constraints on a frozen connected p199 type-class component admit one globally compatible rational section after repeated labeled faces are identified?",
            "falsifier": "An exact global cocycle annihilating every local fill relation but pairing nontrivially with the required shared-face data.",
        },
        "audit": checked,
        "resources": {
            "worker_cpus": [1, 2], "reserved_cpu": 3,
            "actual_wall_seconds": actual["wall_seconds"], "actual_peak_rss_kib": 381252,
            "independent_wall_seconds": independent["wall_seconds"], "independent_peak_rss_kib": 373600,
        },
        "runtime": check_runtime("Cycle 46 Cech classification"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "controls_command": "taskset -c 1-2 .venv/bin/python discovery/lrc_cech_controls.py",
            "actual_command": "taskset -c 1-2 .venv/bin/python discovery/lrc_cech_actual.py --workers 2",
            "independent_command": "taskset -c 1-2 .venv/bin/python proof/replay_cycle_46_cech_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_46_cech.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_46_cech -v",
            "check_command": ".venv/bin/python proof/build_cycle_46_lrc_cech.py --check",
        },
        "sealer": {"path": "proof/build_cycle_46_lrc_cech.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
