"""Seal C103's exact one-reflection book-Ramsey method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-103-b103-book-ramsey-reflection-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-103-b103-book-ramsey-reflection-preregistration-v1.md", "2b083d678c08069ec8b2b1dd1472a9936f642fcea370e857c0f24708cf053655"),
    "selection": ("discovery/_005_f001_book_ramsey_reflection_selection.md", "c0f3c1b343157fa2d6d1f0aa1e78d2c206dae75bfbce04b073b2a882f0d73380"),
    "engine": ("proof/cycle103_book_ramsey_reflection.py", "76935c823b096e454d0b42e06c8bb9a9b349f64eb3a86d9393392a5edb99e9d7"),
    "checker": ("proof/check_cycle103_book_ramsey_reflection.py", "db7321ac87e5c75269e6383c95c992684b579686da684fdf257879add7ab0323"),
    "test": ("tests/test_cycle103_book_ramsey_reflection.py", "17f56f58c376d6ba53ce1006ce825266a4589825fb01494ad8d3abd4eb85b711"),
    "result": ("discovery/out/cycle103-book-reflection/result.json", "a1447bd79a9a856738348a18043833be39668d870e8cb45846de9de616f9c54d"),
    "check": ("discovery/out/cycle103-book-reflection/check.json", "f46a8cbfd849634b7f73f549fbcf652687c9883917ce04c494176da738ebd68e"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def audit() -> dict[str, object]:
    result = json.loads((ROOT / HASHES["result"][0]).read_text())
    checked = json.loads((ROOT / HASHES["check"][0]).read_text())
    require(result["logical_assignments"] == 1 << 25, "logical cap drift")
    require(len(result["row_sum_masks"]) == 222, "row-sum filter drift")
    require(result["seidel_checked_assignments"] == 14_208, "Seidel count drift")
    require(result["q7_hits"] == [], "q=7 hit")
    require(checked == {"logical_assignments": 1 << 25, "q7_hits": [], "row_sum_masks": 222, "seidel_checked_assignments": 14_208}, "checker drift")
    return {"enumerator": result, "independent_checker": checked}


def payload() -> dict[str, object]:
    return {
        "artifact_id": "cycle-103-b103-book-ramsey-reflection-boundary-v1",
        "cycle": 103,
        "budget_ordinal": "B103",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "FINITE_METHOD_FAMILY_BOUNDARY",
        "outcome": "No one of the complete 2^25 signed six-block templates with independently chosen inversion on each of its six inter-block entries satisfies the frozen q=7 Seidel conditions.",
        "claim_boundary": "This exact obstruction concerns only the D001 block placement with its 19 signs and one inversion bit per listed inter-block entry. It does not rule out other block types, further dihedral layers, free blocks, individual graph constructions, or the all-n book-Ramsey conjecture.",
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {label: (ROOT / path, digest) for label, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c103"),
        "sealer": {"path": "proof/build_cycle103_book_ramsey_reflection_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "preflight": "source ../../tools/dev-env.sh && research prereg check docs/cycle-103-b103-book-ramsey-reflection-preregistration-v1.md --expected-cycle 103",
            "engine": "python3 proof/cycle103_book_ramsey_reflection.py --output discovery/out/cycle103-book-reflection/result.json",
            "checker": "python3 proof/check_cycle103_book_ramsey_reflection.py discovery/out/cycle103-book-reflection/result.json > discovery/out/cycle103-book-reflection/check.json",
            "test": "pytest -q tests/test_cycle103_book_ramsey_reflection.py",
            "check": "python3 proof/build_cycle103_book_ramsey_reflection_boundary.py --check",
        },
        "cycle_decision": {
            "decision": "Seal and close F001's one-reflection family.",
            "stop": "Do not enlarge the reflection family, add diagonal twists or free blocks, or run a graph census. A continuation needs a distinct bounded block type with its own state and verifier.",
            "falsifier": "A replayed sign/reflection assignment satisfying the q=7 Seidel conditions invalidates this boundary.",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
