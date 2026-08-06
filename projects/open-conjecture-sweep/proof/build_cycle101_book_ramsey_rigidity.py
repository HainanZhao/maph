from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cycle-101-b101-book-ramsey-character-sign-rigidity-v1.json"
RESULT = ROOT / "discovery/out/cycle101-book-ramsey/result.json"
CHECK = ROOT / "discovery/out/cycle101-book-ramsey/check.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict[str, object]:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    check = json.loads(CHECK.read_text(encoding="utf-8"))
    assert result["assignments"] == 1 << 19
    assert result["q7_masks"] == []
    assert result["q7_q23_masks"] == []
    assert check == {"checked": 1 << 19, "q7_masks": [], "q7_q23_masks": []}
    return {
        "artifact_id": "cycle-101-b101-book-ramsey-character-sign-rigidity-v1",
        "cycle": 101,
        "budget_ordinal": "B101",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "FINITE_METHOD_FAMILY_BOUNDARY",
        "outcome": "No one of the complete 2^19 fixed signed six-block templates satisfies the frozen Seidel conditions at q=7; therefore none can supply the proposed uniform q=7 (mod 8) character family.",
        "claim_boundary": "This exact obstruction concerns only the public block-type placement with the listed 19 signs. It does not refute other block types, sign families, particular graph constructions, or the all-n book-Ramsey conjecture.",
        "audit": {"enumerator": result, "independent_checker": check},
        "frozen_hashes": {
            "preregistration": digest(ROOT / "docs/cycle-101-b101-book-ramsey-character-completion-preregistration-v1.md"),
            "selection": digest(ROOT / "discovery/_003_d001_book_ramsey_selection.md"),
            "source_screen": digest(ROOT / "discovery/cycle96_book_ramsey_candidate_screen.md"),
            "enumerator": digest(ROOT / "proof/cycle101_book_ramsey_completion.py"),
            "checker": digest(ROOT / "proof/check_cycle101_book_ramsey_completion.py"),
            "builder": digest(ROOT / "proof/build_cycle101_book_ramsey_rigidity.py"),
            "result": digest(RESULT),
            "check": digest(CHECK),
        },
        "replay": {
            "engine": "python3 proof/cycle101_book_ramsey_completion.py --output discovery/out/cycle101-book-ramsey/result.json",
            "checker": "python3 proof/check_cycle101_book_ramsey_completion.py discovery/out/cycle101-book-ramsey/result.json > discovery/out/cycle101-book-ramsey/check.json",
            "artifact": "python3 proof/build_cycle101_book_ramsey_rigidity.py --check",
        },
        "cycle_decision": {
            "decision": "Seal the q=7 falsifier for the fixed 19-sign completion and keep D001 on its selected target.",
            "stop": "Do not enlarge the sign family, introduce a free block, or perform a graph census. A continuation needs one explicitly bounded new block type derived from the residual row or two-walk algebra.",
            "falsifier": "A replayed sign vector satisfying the frozen q=7 Seidel conditions invalidates this boundary.",
        },
        "runtime": {"enumerator_wall_seconds": 2.77, "checker_wall_seconds": 13.06, "peak_rss_kib": 13568, "implementation": "Two separate Python exact-integer evaluators; q=7 is a finite necessary control for any uniform q=7 mod 8 identity."},
    }


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit(2)
    record = payload()
    if sys.argv[1] == "--write":
        if ARTIFACT.exists():
            raise SystemExit("refusing to overwrite sealed artifact")
        ARTIFACT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    elif json.loads(ARTIFACT.read_text(encoding="utf-8")) != record:
        raise SystemExit("artifact differs from deterministic payload")
    print(json.dumps({"artifact": str(ARTIFACT), "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
