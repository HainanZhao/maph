"""Correct C103 v1's omitted imported replay dependency without mutating it."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-103-b103-book-ramsey-reflection-boundary-correction-v2.json"
HASHES = {
    "superseded_record": ("artifacts/cycle-103-b103-book-ramsey-reflection-boundary-v1.json", "6732eb78aa18fcf634b4d3eab49c4a915e48cfd2c3f07a8f9efaa46bc2d69003"),
    "correction": ("docs/cycle-103-b103-book-ramsey-reflection-correction-v2.md", "d1a5a0e8efa4515d3aecbbb7d097f11fb963362967c10bb40cb8787b2b08d5c4"),
    "preregistration": ("docs/cycle-103-b103-book-ramsey-reflection-preregistration-v1.md", "2b083d678c08069ec8b2b1dd1472a9936f642fcea370e857c0f24708cf053655"),
    "selection": ("discovery/_005_f001_book_ramsey_reflection_selection.md", "c0f3c1b343157fa2d6d1f0aa1e78d2c206dae75bfbce04b073b2a882f0d73380"),
    "imported_c101_constructor": ("proof/cycle101_book_ramsey_completion.py", "1c4cb27a6ff4f4a93469146aef78610c26164a0e6b7205eb18433dec80c753b1"),
    "engine": ("proof/cycle103_book_ramsey_reflection.py", "76935c823b096e454d0b42e06c8bb9a9b349f64eb3a86d9393392a5edb99e9d7"),
    "checker": ("proof/check_cycle103_book_ramsey_reflection.py", "db7321ac87e5c75269e6383c95c992684b579686da684fdf257879add7ab0323"),
    "replay": ("proof/replay_cycle103_book_ramsey_reflection.py", "2f46d9bf6138af5f3c3713d0c514d4896b77303f67f0e352e5a0e6e41a8ddbad"),
    "result": ("discovery/out/cycle103-book-reflection/result.json", "a1447bd79a9a856738348a18043833be39668d870e8cb45846de9de616f9c54d"),
    "check": ("discovery/out/cycle103-book-reflection/check.json", "f46a8cbfd849634b7f73f549fbcf652687c9883917ce04c494176da738ebd68e"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload() -> dict[str, object]:
    return {
        "artifact_id": "cycle-103-b103-book-ramsey-reflection-boundary-correction-v2",
        "cycle": 103,
        "budget_ordinal": "B103",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "CORRECTION_REPLAY_DEPENDENCY_FREEZE",
        "supersedes": "cycle-103-b103-book-ramsey-reflection-boundary-v1",
        "outcome": "C103's q=7 no-hit and one-reflection method boundary are unchanged; this correction freezes the imported C101 constructor and supplies a standard-library one-command replay.",
        "correction": {
            "error": "C103 v1 did not freeze or cite proof/cycle101_book_ramsey_completion.py, which its engine imports.",
            "cause": "The new engine reused C101's character-block constructor, but the v1 frozen-input inventory recorded only the direct engine file.",
            "affected_claims": "Only v1 proof-grade replay self-sufficiency; no mathematical result, scope boundary, or q=7 enumeration count changes.",
            "repair": "Freeze the imported constructor and replay script, retain the prior engine/checker outputs, and require the standard-library replay to reproduce the exact counts.",
        },
        "claim_boundary": "The corrected PROVED result remains limited to the 19-sign, six-one-reflection-bit D001 block family at q=7. It does not address other character blocks, arbitrary graphs, or the all-n book-Ramsey conjecture.",
        "cycle_decision": {
            "decision": "Rely on this v2 correction, not v1 alone, for the C103 one-reflection boundary.",
            "stop": "Do not widen the reflection family, add diagonal twists or free blocks, or run a graph census. A continuation needs a distinct bounded block type with its own state and verifier.",
            "falsifier": "A replayed sign/reflection assignment satisfying q=7 Seidel conditions invalidates the corrected boundary.",
        },
        "frozen_hashes": freeze_inputs(ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c103-correction"),
        "sealer": {"path": "proof/build_cycle103_book_ramsey_reflection_correction_v2.py", "sha256": sha256(Path(__file__))},
        "replay": {"full": "python3 proof/replay_cycle103_book_ramsey_reflection.py", "check": "python3 proof/build_cycle103_book_ramsey_reflection_correction_v2.py --check"},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
