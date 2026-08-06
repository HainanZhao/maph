from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/cycle-98-b098-diophantine-fixed-ansatz-boundary-v1.json"
REPLAY = ROOT / "discovery/out/cycle98-diophantine/replay.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    assert replay["cycle"] == 98
    assert replay["status"] == "EXHAUSTED"
    assert replay["hits"] == []
    assert replay["control_pass"] is True
    return {
        "artifact_id": "cycle-98-b098-diophantine-fixed-ansatz-boundary-v1",
        "cycle": 98,
        "budget_ordinal": "B098",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "FINITE_METHOD_FAMILY_BOUNDARY",
        "outcome": "The normalized degree-(4,3,6) polynomial ansatz in the complete integer coefficient box [-648,648] has no identity family for z^2+y^2 z+x^3-2.",
        "claim_boundary": "This is a complete exact boundary for one parity-balanced degree/height family only. It does not prove finiteness or infinitude of the size-22 equation, exclude other degrees, elliptic or norm-form maps, or constrain the five neighboring equations.",
        "audit": replay,
        "frozen_hashes": {
            "prereg": sha(ROOT / "docs/cycle-98-b098-diophantine-fixed-ansatz-preregistration-v1.md"),
            "candidate": sha(ROOT / "discovery/cycle97_diophantine_candidate_screen.md"),
            "selection": sha(ROOT / "discovery/cycle97_fixed_ansatz_selection.md"),
            "engine": sha(ROOT / "proof/cycle98_diophantine_ansatz.py"),
            "checker": sha(ROOT / "proof/check_cycle98_diophantine_ansatz.py"),
            "replay": sha(REPLAY),
        },
        "replay": {
            "engine": "python3 proof/cycle98_diophantine_ansatz.py --out discovery/out/cycle98-diophantine/replay.json",
            "check": "python3 proof/check_cycle98_diophantine_ansatz.py discovery/out/cycle98-diophantine/replay.json",
        },
        "cycle_decision": {
            "decision": "Seal the complete bounded-family no-hit and pivot.",
            "stop": "Do not enlarge the coefficient box or degree pattern; screen an elliptic-surface or norm-form engine before any successor attack.",
            "falsifier": "A deterministic replay candidate in the frozen box whose two independent coefficient routes both vanish identically.",
        },
        "runtime": {
            "engine_wall_seconds": replay["wall_seconds"],
            "engine_peak_rss_kib": 13440,
            "nodes": replay["nodes"],
            "implementation": "Python 3 exact integers; hard-coded and generic polynomial routes",
        },
    }


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit(2)
    p = payload()
    if sys.argv[1] == "--write":
        ART.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        assert json.loads(ART.read_text(encoding="utf-8")) == p
    print(json.dumps({"status": "PASS", "artifact": str(ART), "nodes": p["audit"]["nodes"]}, sort_keys=True))


if __name__ == "__main__":
    main()
