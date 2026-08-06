"""Seal C88's greedy residual fractional-drop method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-88-b088-ryser-fractional-drop-boundary-v1.json"
PYTHON = ROOT / ".venv/bin/python"
HASHES = {
    "preregistration": ("docs/cycle-88-b088-ryser-fractional-drop-preregistration-v1.md", "5c566279e0c962fe6e2d3460ad3c43e48be21c6927baa7b12eab50fd293001c7"),
    "idea_selection": ("discovery/cycle88_ryser_fractional_drop_selection.md", "ea28e33151755d65ab839a9ece3e7dc257a61858ea50bb4d5826bc2577892ecd"),
    "source_audit": ("discovery/cycle88_ryser_fractional_drop_source_audit.md", "d4ca4921a593c51a4da82751a48fbf77496573fb5a7d44f5f7e994509ef7029c"),
    "published_control": ("discovery/cycle69_r6_extremal_control.py", "c62edddd382483e1b243e385bfe14ba99a40a0b1e137d3145e995b3223bf2276"),
    "checker": ("proof/check_cycle88_fractional_drop.py", "633b00126769cd1b6b6fb9de251f122a9dc090aebb603dc5735195370c75c01e"),
    "boundary": ("proof/cycle88_fractional_drop_boundary.md", "d50a497a01f0346d52dfc398a77f9ca5a9f667fe8937f21c0c069cc40f5f368a"),
    "test": ("tests/test_cycle88_fractional_drop.py", "3031e82e62a3b08415471d2ef991a859e8f4babfb01892c5139d3a8b83873b98"),
    "prior_c87": ("artifacts/cycle-87-b087-ryser-private-absorption-boundary-v1.json", "0a692a7065614ab64b25199e43065c4a4be65c6c907e4264a76c05ddc5a029f3"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def audit() -> dict:
    result = json.loads(subprocess.check_output([str(PYTHON), str(ROOT / HASHES["checker"][0])], text=True))
    require(result["status"] == "FD_REFUTED" and result["epistemic_status"] == "PROVED", "C88 checker did not refute FD")
    require(result["unreconstructed"] == [], "C88 has an unreconstructed LP row")
    require(result["layer_counts"] == [1, 31, 420, 2582, 5403, 6101], "residual traversal drift")
    require(result["certificate_cache_size"] == 6102 and len(result["failures"]) == 263, "certificate packet drift")
    first = result["failures"][0]
    require(first["depth"] == 1 and first["residual_edges"] == list(range(1, 10)), "first residual drift")
    require(first["tau_star"] == "23/8" and first["k"] == 3 and first["drop_vertices"] == [], "FD_3 falsifier drift")
    return {"status": result["status"], "epistemic_status": result["epistemic_status"],
            "layer_counts": result["layer_counts"], "distinct_exact_lps": result["certificate_cache_size"],
            "residual_rows": result["residuals_checked"], "failure_count": len(result["failures"]),
            "unreconstructed_count": len(result["unreconstructed"]), "first_failure": first}


def payload() -> dict:
    return {
        "artifact_id": "cycle-88-b088-ryser-fractional-drop-boundary-v1", "budget_ordinal": "B088", "cycle": 88,
        "record_type": "METHOD_BOUNDARY", "recorded_at_utc": "2026-08-06T01:34:31Z", "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "The published 13-edge r=6 control has a nine-edge residual after deleting (1,6) with exact tau*=23/8, but every one-vertex child has tau*>2; this refutes greedy FD_3. The depth-five packet has 263 exact least-applicable FD failures and no unreconstructed LP.",
        "claim_boundary": "This refutes only greedy one-vertex unit descent for the C88 residual fractional-cover-drop mechanism. It does not refute Ryser at r=6, the control's integral five-cover, non-greedy tuple rounding, or other fractional/dual methods.",
        "cycle_decision": {"companion_identity": "/root/oracle_c88_retry (Oracle)", "companion_advice": "Seal the FD boundary and do not repair it with pair deletions, altered thresholds, or a larger census.", "decision": "Seal the greedy fractional-drop method boundary and return to fresh portfolio discovery.", "falsifier": "The exact nine-edge residual after deleting (1,6), with tau*=23/8 and no vertex child of tau*<=2."},
        "audit": audit(), "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c88"), "sealer": {"path": "proof/build_cycle_88_ryser_fractional_drop_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {"audit": ".venv/bin/python proof/check_cycle88_fractional_drop.py", "test": ".venv/bin/python -c \"import runpy; ns=runpy.run_path('tests/test_cycle88_fractional_drop.py'); ns['test_c88_fractional_drop_falsifier']()\"", "check": ".venv/bin/python proof/build_cycle_88_ryser_fractional_drop_boundary.py --check"},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
