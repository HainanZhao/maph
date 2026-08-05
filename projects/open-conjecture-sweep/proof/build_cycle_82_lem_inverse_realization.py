"""Seal C82's exact one-family LEM inverse-realization boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-82-b082-lem-inverse-family-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-82-b082-lem-inverse-realization-preregistration-v1.md", "22ec952cf5ba777093cdc35f5cd4e10b1dde9e382443b943723992641936dc7f"),
    "source_screen": ("discovery/cycle81_lem_source_screen.md", "e1f424c942c002f3fbd6d7e22d6b9f0ef1c07aa236606f4e6497209bcd2b63d0"),
    "idea_selection": ("discovery/cycle82_inverse_realization_idea_selection.md", "a5c2c0a110c7e137e9161eb4ae3ac5019f2afbd8cbf5937f43d3a00a6dc6d9a5"),
    "prior_artifact": ("artifacts/cycle-81-b081-lem-method-boundary-v1.json", "817e1643b33c6d4c1f9f943e93507fadb5efe31289e26ceaf5193e39953c53f5"),
    "dynamic_checker": ("proof/check_cycle82_chain_substitution.py", "5139f738d05dc82dabdf9db5e11449679af02ce5c5726e32d3707535205b271c"),
    "direct_checker": ("proof/check_cycle82_direct_enumeration.py", "39774c518feb80a7620e8e7647948adfb3098fd6ed3f60dec004d3ec08c57949"),
    "certificate": ("proof/cycle82_chain_substitution.md", "1dede072c2180eba2ec2b955476f341d13f9ec4862d647b256499330495b1318"),
    "test": ("tests/test_cycle82_chain_substitution.py", "fde8c0f83a051a40cd0cd55562c3f80e4c84b67207a350047af3abf19914968e"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def run(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def audit() -> dict:
    dynamic = run(HASHES["dynamic_checker"][0])
    direct = run(HASHES["direct_checker"][0])
    for result in (dynamic, direct):
        require(result["status"] == "PASS", "checker did not pass")
        require(result["vertices"] == 15, "wrong poset order")
        require(result["extensions"] == 571_725, "wrong extension count")
        require(not result["full_has_4_cycle"], "unexpected full 4-cycle")
        require(not result["restricted_has_4_cycle"], "unexpected restricted 4-cycle")
    require(direct["transitive_closure_added_relations"] == 3, "closure convention drift")
    return {"dynamic_program": dynamic, "direct_enumeration": direct}


def payload() -> dict:
    return {
        "artifact_id": "cycle-82-b082-lem-inverse-family-boundary-v1",
        "budget_ordinal": "B082",
        "cycle": 82,
        "record_type": "FAMILY_BOUNDARY",
        "recorded_at_utc": "2026-08-05T20:45:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The frozen 15-element three-chain substitution has 571,725 linear extensions and no full strict pair-majority directed 4-cycle; it is not a LEM mismatch realization.",
        "claim_boundary": "This proves only the named one-member substitution boundary. It neither proves nor refutes Gupta Question 14, nor excludes other order-15-or-larger inverse modular realizations.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c82_gate_review (Oracle)",
            "companion_advice": "Seal C82 as a FAMILY_BOUNDARY; select the triangle-tip interval theorem rather than widen the construction. The strongest flaw is that this non-parametric miss has no implication beyond P_82.",
            "decision": "Seal the exact family no-go and pivot to the distinct triangle-tip interval engine.",
            "falsifier": "A differing exact extension count or an explicit ordered four-tuple forming a full strict pair-majority cycle in P_82.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c82"),
        "sealer": {"path": "proof/build_cycle_82_lem_inverse_realization.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle82_chain_substitution.py && python3 proof/check_cycle82_direct_enumeration.py",
            "test": "pytest -q tests/test_cycle82_chain_substitution.py",
            "check": "python3 proof/build_cycle_82_lem_inverse_realization.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
