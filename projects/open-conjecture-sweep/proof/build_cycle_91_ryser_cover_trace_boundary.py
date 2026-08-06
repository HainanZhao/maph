"""Seal C91's frozen Ryser deletion-cover trace method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

OUT = ROOT / "artifacts/cycle-91-b091-ryser-cover-trace-boundary-v1.json"
PY = ROOT / ".venv/bin/python"
H = {
    "preregistration": ("docs/cycle-91-b091-ryser-cover-trace-preregistration-v1.md", "73bb7b3411c8a10c74028dc02a00fb91a6b3e0d3661297ad1c469edd6ed918ca"),
    "selection": ("discovery/cycle91_ryser_trace_selection.md", "03f137b265cca3afdb7f97e0a1629781804312589b9dbd0662f6e286059db5ae"),
    "source_audit": ("discovery/cycle91_ryser_trace_source_audit.md", "784eed1a8b0b3065ce63ae099a99ccdad982b7e9f347a523f103deff303d564d"),
    "published_control": ("discovery/cycle69_r6_extremal_control.py", "c62edddd382483e1b243e385bfe14ba99a40a0b1e137d3145e995b3223bf2276"),
    "checker": ("proof/check_cycle91_ryser_cover_trace.py", "4d64e5262f434d149ff33e7309681d1a593d11708e5f7db9bb28b820e6753454"),
    "boundary": ("proof/cycle91_ryser_cover_trace_boundary.md", "0349ede128285af734c0b69dc840e1b4be16fa0d1c7bd47c818e02e93c691c52"),
    "test": ("tests/test_cycle91_ryser_cover_trace.py", "d04cd74fb58224a152adf0b8a01b935cb8e3d85b8eddf2935503c13a8e3ec95b"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}
COUNTS = [3, 5, 5, 5, 5, 6, 4, 6, 4, 5, 6, 4, 6]


def audit():
    result = json.loads(subprocess.check_output([str(PY), str(ROOT / H["checker"][0])], text=True))
    require(result["status"] == "PASS", "C91 checker failed")
    require(result["vertices"] == 31 and result["edges"] == 13 and result["tau"] == 5, "C91 source-control mismatch")
    require(result["family_counts"] == COUNTS, "C91 cover-family mismatch")
    require(result["route_a_csp"] == result["route_b_csp"] == "UNSAT", "C91 CSP disagreement or SAT")
    return result


def payload():
    return {
        "artifact_id": "cycle-91-b091-ryser-cover-trace-boundary-v1",
        "budget_ordinal": "B091",
        "cycle": 91,
        "record_type": "METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-06T00:00:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The complete four-vertex deletion-cover families of the published 13-edge tau=5 control have counts [3,5,5,5,5,6,4,6,4,5,6,4,6]. Two exact routes agree that the frozen reciprocal shared-coordinate trace CSP is UNSAT.",
        "claim_boundary": "This refutes only the frozen reciprocal shared-coordinate trace condition on one rank-shifted tau=5 equality control. It says nothing about tau=6 counterexamples, intersecting Ryser, nonreciprocal/global trace systems, or the fractional matching theorem.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c88_retry (Oracle)",
            "companion_advice": "Seal and pivot; do not weaken reciprocity or use another control.",
            "decision": "End C91 after the preregistered finite falsifier and return to portfolio discovery.",
            "falsifier": "Any missing minimum cover, enumeration disagreement, satisfying reciprocal assignment, or source-transcription mismatch.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in H.items()}),
        "runtime": check_runtime("c91"),
        "sealer": {"path": "proof/build_cycle_91_ryser_cover_trace_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": ".venv/bin/python proof/check_cycle91_ryser_cover_trace.py",
            "test": ".venv/bin/python -c \"import runpy; ns=runpy.run_path('tests/test_cycle91_ryser_cover_trace.py'); ns['test_c91_cover_trace_routes_agree']()\"",
            "artifact_check": ".venv/bin/python proof/build_cycle_91_ryser_cover_trace_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUT, payload_factory=payload))
