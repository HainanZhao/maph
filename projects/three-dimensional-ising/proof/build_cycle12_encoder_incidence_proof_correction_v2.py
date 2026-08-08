#!/usr/bin/env python3
"""Correct Cycle 12 sealing scope without changing its mathematics."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402
from proof.generate_encoder_incidence_tables import build_payload, render_latex  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-12-b12-encoder-incidence-proof-v2.json"
HASHES: dict[str, tuple[str, str]] = {
    "superseded_v1": ("artifacts/cycle-12-b12-encoder-incidence-proof-v1.json", "6c81032760285933d36f090fedc665c1cd13604a20c6023407debe5e326f7bd8"),
    "correction": ("discovery/cycle12-encoder-incidence-seal-correction.md", "3ff81a7ab58e369ece9dbb77f2b222e89893d1cb2eda0360be2520249b2ff0a0"),
    "preregistration": ("discovery/cycle-12-encoder-incidence-preregistration.md", "2c7ebf6137cd756d41083f87fb8c94ce8c65b1d9d69a9a1804a91ec9a280ed30"),
    "failure_ledger": ("discovery/failure-ledger-cycle12.md", "f95c5ea5e0e09b748370d2e9d51de376c97079cf5ec789d717039a049f3b0c71"),
    "proof": ("proof/encoder_incidence_proof.md", "d6e84f3ad53c1fa04fb7eb7cd59508fb73c515b1d4c410e69297bf4a511f0711"),
    "generator": ("proof/generate_encoder_incidence_tables.py", "8a5bf5c765aeadab8ae606fc3ebe6802be876f491241261b51d81305387bfa3d"),
    "tests": ("tests/test_encoder_incidence_tables.py", "7b48de58ab601790121064a29d9244da4727ff5b3aeb5b231c8433832d1cf6d3"),
    "generated_table": ("paper/canonical-spin-structure-compression/encoder-incidence-firewall.tex", "0239b0c12dd90b3ee76885f64898dcad06941ac05488aa2cde9f2e99bde41609"),
    "normal_exceptional_dependency": ("discovery/audit_g1_explicit_common_basis.py", "07d84fe4ab0d6058b95e8e1ac95e047440e2b89c251cf7f6f5a9a39d897f01df"),
    "opposite_dependency": ("discovery/audit_g1_opposite_explicit_all_width.py", "cdfbd0e26ef1d65d0229054556a516d73d41a5317e298e95a0faa653ff9108d4"),
    "component_dependency": ("proof/verify_g1_arbitrary_width_generic_tightness.py", "4d55b1fc8667261d19ca9e89c276d7763c41c629b336471de519565e5e14e63b"),
    "tree_dependency": ("proof/verify_g1_buffered_factorization.py", "8859db6ae70c2189f6bb3276728d05c383f471f6fada2f48b85e549dcfba725f"),
    "rotation_dependency": ("src/lane_b_universal_embedding.py", "62e57075103f4f2f252f30f9bd1e01c63820656455900b6db0b875e5294ab430"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
    "requirements": ("requirements.txt", "8347daed02ebf7b3c3cfa494e97049b7e0ab15b9af00a5addd843ed44381a64a"),
}


def payload() -> dict[str, object]:
    replay = build_payload()
    rows = replay["rows"]
    if [row["width"] for row in rows] != list(range(4, 9)):
        raise RuntimeError("width firewall changed")
    if any(
        item["unclassified_count"] or not item["is_dual_component"]
        for row in rows for item in row["normal"]
    ):
        raise RuntimeError("normal incidence/component invariant regressed")
    if any(row["opposite"].get("unclassified_count", 0) for row in rows):
        raise RuntimeError("opposite incidence gained an unclassified edge")
    generated = ROOT / "paper/canonical-spin-structure-compression/encoder-incidence-firewall.tex"
    if generated.read_text() != render_latex(replay):
        raise RuntimeError("checked-in incidence table differs from generator")
    return {
        "artifact_id": "cycle-12-b12-encoder-incidence-proof-v2",
        "author": "Hainan Zhao",
        "budget_ordinal": "B12",
        "cycle": 12,
        "status": "SEALED",
        "epistemic_status": "PROVED_WITH_EXACT_COMBINATORIAL_FIREWALL",
        "record_type": "CORRECTION_LANE_B_ENCODER_INCIDENCE_PROOF",
        "supersedes": "cycle-12-b12-encoder-incidence-proof-v1",
        "correction": (
            "v1 incorrectly froze the mutable manuscript. v2 narrows the frozen "
            "inputs to the standalone proof package; mathematical content is unchanged."
        ),
        "outcome": (
            "The normal I3/I5/I2r and even-width opposite C_W cellular boundaries "
            "are exact arbitrary-width identities. Widths 4..8 independently agree "
            "with face walks in the fixed normal and translated-opposite rotations."
        ),
        "gate_outcome": "ENCODER_INCIDENCE_GAP_CLOSED",
        "claim_boundary": (
            "Finite face-walk rows audit but do not prove the arbitrary-width encoder "
            "parent recurrences. No homogeneous-weight or thermodynamic claim follows."
        ),
        "theorem": {
            "normal_boundary_classes": ["internal", "T_W^0", "X_W^+"],
            "opposite_boundary_classes": ["T_W^0", "X_W^-", "P_W^-"],
            "opposite_bridge_components": 2,
            "modular_arithmetic": "not applicable; GF(2) cellular incidence only",
        },
        "exact_replay": replay,
        "frozen_hashes": freeze_inputs(
            ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}
        ),
        "runtime": check_runtime("cycle-12-encoder-incidence-proof-correction-v2"),
        "sealer": {
            "path": "proof/build_cycle12_encoder_incidence_proof_correction_v2.py",
            "sha256": sha256(Path(__file__)),
        },
        "replay": {
            "verification": "python3 proof/generate_encoder_incidence_tables.py --check-tex paper/canonical-spin-structure-compression/encoder-incidence-firewall.tex",
            "tests": "python3 -m unittest tests/test_encoder_incidence_tables.py -v",
            "artifact_check": "python3 proof/build_cycle12_encoder_incidence_proof_correction_v2.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
