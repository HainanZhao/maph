"""Seal C83's exact local ordered-tip method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-83-b083-lem-local-defect-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-83-b083-lem-tip-fiber-preregistration-v1.md", "a35eaa7ccecc4940d7517204982e496bb1de5d8a8dd03a5d156c2e282290cc8c"),
    "idea_selection": ("discovery/cycle83_triangle_tip_idea_selection.md", "9154395f7e624f269082b674d6da9d60e6729d6cc5da1e11f1e89cae4c40b448"),
    "source_context": ("discovery/cycle83_source_context.md", "30960f1038e8d9a3bc19f11ed37291e85b0228acc6c9f0540deedabaa47a2b51"),
    "reduction": ("proof/cycle83_triangle_tip_reduction.md", "d6f858040809a3f75dd89c412fbc885739a1b1426695cab65e08ec1d69280948"),
    "tip_checker": ("proof/check_cycle83_tip_fibers.py", "aec260b32f09af54ce6d296d2014a8cab4735f028e58506f5ec0f331af1537ea"),
    "conditional_checker": ("proof/check_cycle83_interval_conditioning.py", "0a4c197e46fe5c3b393a2e71957e2e7d2fce7a85daae616c50378272feffaf54"),
    "word_checker": ("proof/check_cycle83_word_pairing.py", "ea328808ce6fc5b478baf081d14585852b8d29924e11cf3aa66693d4c48e1cad"),
    "defect_checker": ("proof/check_cycle83_global_defect.py", "3b9cb09ac23bd78c2087f06c7590589f5c2be00cbd55a0bcccea3e40296282b0"),
    "boundary": ("proof/cycle83_local_defect_boundary.md", "4c51d0ec591303ef737ca74696d652a0b3a1d600d06dd660f888e872aa1be16f"),
    "test": ("tests/test_cycle83_local_defect_boundary.py", "c1b18b16cb56287f69b5ff0a5a1bf16d9cf366dcea12c0da049d549d71350e04"),
    "prior_c81": ("artifacts/cycle-81-b081-lem-method-boundary-v1.json", "817e1643b33c6d4c1f9f943e93507fadb5efe31289e26ceaf5193e39953c53f5"),
    "prior_c82": ("artifacts/cycle-82-b082-lem-inverse-family-boundary-v1.json", "8a89cef3b5536e210528e3de6138aad1dd11a8ddf0b1b319301eaa64a398d7bf"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def run(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def audit() -> dict:
    tips = run(HASHES["tip_checker"][0])
    conditional = run(HASHES["conditional_checker"][0])
    words = run(HASHES["word_checker"][0])
    defect = run(HASHES["defect_checker"][0])
    require(tips["status"] == conditional["status"] == words["status"] == defect["status"] == "PASS", "checker failure")
    require(tips["c81"]["identities"] == 84 and tips["c82"]["identities"] == 78, "tip identity drift")
    require(conditional["reversed_rows"] == 30, "conditional counterexample drift")
    require(words["c81_imbalanced_global_arrow_queries"] == 216, "word-pairing counterexample drift")
    require(defect["c81"]["inequality_failures"] == 18 and defect["c82"]["inequality_failures"] == 768, "defect counterexample drift")
    return {"tip_identities": tips, "conditional_fibers": conditional, "outside_word_pairing": words, "global_defect": defect}


def payload() -> dict:
    return {
        "artifact_id": "cycle-83-b083-lem-local-defect-boundary-v1",
        "budget_ordinal": "B083",
        "cycle": 83,
        "record_type": "METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-06T00:08:35Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Exact C81/C82 controls falsify C83's conditional-majority, outside-word-pairing, and global-defect mechanisms; the last has 18 and 768 marked-tuple violations respectively.",
        "claim_boundary": "This closes only the local-fiber/global-defect method family. It neither proves nor refutes Gupta Question 14 and does not realize or exclude the full ordered two-triangle hypothesis.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c83_pivot (Oracle)",
            "companion_advice": "Retain C83 for one final full-hypothesis global-defect gate; pivot immediately if it is falsified or no precise charge map emerges.",
            "decision": "Seal the exact method boundary and return to portfolio discovery rather than extend the failed local-fiber framing.",
            "falsifier": "A differing exact marked-tuple count or defect scan; specifically, no C81/C82 tuple may violate the proposed three-probability inequality.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c83"),
        "sealer": {"path": "proof/build_cycle_83_lem_local_defect_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle83_tip_fibers.py && python3 proof/check_cycle83_interval_conditioning.py && python3 proof/check_cycle83_word_pairing.py && python3 proof/check_cycle83_global_defect.py",
            "test": "pytest -q tests/test_cycle83_local_defect_boundary.py",
            "check": "python3 proof/build_cycle_83_lem_local_defect_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
