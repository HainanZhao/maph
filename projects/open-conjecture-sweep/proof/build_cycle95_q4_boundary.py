from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/cycle-95-b095-bollobas-meir-q4-boundary-v1.json"
ROWS = ROOT / "discovery/out/cycle95-q4/rows.tsv"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def payload() -> dict:
    summary = json.loads((ROWS.parent / (ROWS.name + ".summary.json")).read_text())
    return {
        "artifact_id": "cycle-95-b095-bollobas-meir-q4-boundary-v1",
        "cycle": 95, "budget_ordinal": "B095", "status": "SEALED",
        "epistemic_status": "PROVED",
        "record_type": "FINITE_SUBCLASS_BOUNDARY",
        "outcome": "All 65,519 labelled nontrivial subsets of Q4 have an exact Hamiltonian cycle of fourth-power Euclidean cost at most 32; the maximum emitted optimum is 32.",
        "claim_boundary": "This proves only the Boolean-vertex Q4 subclass of the adjusted Bollobas--Meir conjecture. It does not prove the conjecture for arbitrary points, any other dimension, or an orbit/metric explanation.",
        "audit": summary,
        "frozen_hashes": {"prereg": sha(ROOT / "docs/cycle-95-b095-bollobas-meir-q4-preregistration-v1.md"), "selection": sha(ROOT / "discovery/cycle95_bollobas_meir_selection.md"), "engine": sha(ROOT / "proof/cycle95_q4_hypercube_dp.cpp"), "checker": sha(ROOT / "proof/check_cycle95_q4.py"), "rows": sha(ROWS)},
        "replay": {"engine": "g++ -std=c++20 -O3 -DNDEBUG proof/cycle95_q4_hypercube_dp.cpp -o /tmp/c95-q4 && /tmp/c95-q4 discovery/out/cycle95-q4/rows.tsv", "check": "python3 proof/check_cycle95_q4.py discovery/out/cycle95-q4/rows.tsv"},
        "cycle_decision": {"decision": "Seal finite Q4 subclass and stop.", "stop": "No Q5, rational grids, random points, or arbitrary-cube continuation without a new source-defined orbit/metric mechanism.", "falsifier": "A replayed labelled subset with exact optimum above 32."},
        "runtime": {"engine_wall_seconds": 0.06, "engine_peak_rss_kib": 7296, "implementation": "C++20 -O3; Python 3 checker"}
    }

def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}: raise SystemExit(2)
    p = payload()
    if sys.argv[1] == "--write":
        ART.parent.mkdir(exist_ok=True)
        ART.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n")
    else:
        assert json.loads(ART.read_text()) == p
    print(json.dumps({"status": "PASS", "artifact": str(ART), "subsets": p["audit"]["subsets"]}, sort_keys=True))

if __name__ == "__main__": main()
