"""Seal Cycle 38's exact rooted ownership-functional obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_38_ownership_functional import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle38-ownership-functional"
OUTPUT = ROOT / "artifacts/cycle-38-b038-lrc-ownership-functional-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-38-b038-lrc-ownership-functional-preregistration-v1.md", "9965756e56282a6ebd983a3f850169f6acaea456235384b82a810134cf68c2d8"),
    "cycle29_artifact": (ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v2.json", "faf097ebcc22e9e18055cbf4139aef30e17ee85e86ea2096d43b31873f6e8d09"),
    "cycle37_artifact": (ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json", "0e606c64704f08158fa4a04b98737450b83ada03cb67b601f1680bff75b3265a"),
    "idea_selection": (ROOT / "discovery/cycle38_ownership_functional_idea_selection.md", "35a0fd8328f5459779c00f72de9927e7271df075fa182ba535590e87b9ce8282"),
    "cycle29_result": (ROOT / "discovery/out/cycle29-ownership-blocker/result.json", "b213f8b790b2f53e2de30d244ead973143973e236083d24b38fffb5234271f15"),
    "cycle37_result": (ROOT / "discovery/out/cycle37-degree-two-product/result.json", "6d4f4ddb592be0f4cb1739b7b2ef0aab992b3b27defb7acf7fd4726f1d10558c"),
    "primary_engine": (ROOT / "discovery/lrc_ownership_functional.py", "2e4d63706aff0f0c71f13c06bd0dc63374f28c82a1e9ae4fd2b241141d843589"),
    "primary_result": (OUT / "result.json", "270dcd272c020c5af64e70af6eb57dbf63034d86964ab8a1472763923625fa54"),
    "primary_timing": (OUT / "run.time", "4c5b941f6e89915f0755fbc9736c1186ef4078924014f716b3ebdd808b826c97"),
    "independent_replay": (ROOT / "proof/replay_cycle_38_ownership_functional_independent.py", "e94bdc0b6462c633992dc448b3b4a24506a36934a8ecc838c9fed599820a559a"),
    "independent_result": (OUT / "independent-replay.json", "62777b173d44d615149fecc52c85fc63cfb0f53f7427ec0c73e6ae1efb1bcc54"),
    "independent_timing": (OUT / "independent-replay.time", "11a2393842ed1d5ef708ef14a616207065e22fd5d13a7602fa7e1550842b877c"),
    "audit": (ROOT / "proof/check_cycle_38_ownership_functional.py", "a6b7b4a254c57b829cd517d94f10a1ef0b9de29c2dde38d049e8628c99a9c574"),
    "soundness": (ROOT / "proof/cycle_38_ownership_functional_soundness.md", "46f5c662a99d3ea8321110bbd5438bddd267a0f38be2604fbc4354b33fc1c241"),
    "test": (ROOT / "tests/test_cycle_38_ownership_functional.py", "ef02dcc6f7b3591bab1a2ecc875f65794c554c585fa92ba2c06f4b8cf4d96970"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload() -> dict[str, object]:
    checked = audit()
    result = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    return {
        "artifact_id": "cycle-38-b038-lrc-ownership-functional-v1",
        "budget_ordinal": "B038",
        "cycle": 38,
        "record_type": "PROVED_ROOTED_OWNERSHIP_FUNCTIONAL_NO_GO",
        "recorded_at_utc": "2026-08-04T16:36:43Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Every one of the thirteen cyclic rooted ownership pushforwards of the Cycle 37 signed product measure has a nonzero exact rank-two blocker moment on p199 base 4 / leaf 78. An independently checked integer augmented left-null certificate proves that their linear span contains no mass-one functional annihilating all unmultiplied Cycle 29 ownership generators.",
        "claim_boundary": "This closes only the thirteen deterministic rooted pushforwards and their linear span at the unmultiplied ownership-generator layer for one leaf. It does not constrain arbitrary local or nonlocal routing kernels, generator multiples, the full ownership ideal, the leaf, or LRC(13).",
        "audit": checked,
        "proved_reduction": {
            "epistemic_status": "PROVED",
            "statement": "Rooted total ownership makes totality and exclusivity pointwise, makes every off-root blocker pointwise zero, and factorizes each own-root blocker moment into at most eight products of local signed contractions.",
            "complete_global_types": result["interface"]["distinct_complete_global_types"],
            "symbolic_blocker_patterns": 12264,
            "concrete_blockers": result["concrete_blockers"],
            "complete_type_tuples": result["complete_type_tuples"],
            "maximum_blocker_rank": 3,
        },
        "obstruction": {
            "epistemic_status": "PROVED",
            "all_roots_obstructed": True,
            "first_nonzero_moments_by_root": [row["first_nonzero"]["moment"] for row in result["roots"]],
            "first_nonzero_rank_by_root": [row["first_nonzero"]["rank"] for row in result["roots"]],
            "independent_signed_support_assignments": replay["signed_support_assignments"],
            "augmented_system_left_null_certificate": replay["augmented_system_left_null_certificate"],
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_ROOT_FREE_ROUTING_QUESTION",
            "scope_review": "The exact diagonal augmented-system certificate closes the rooted span, but deterministic first-cover/fallback ownership is highly special.",
            "strongest_flaw": "Even an infeasible local routing system may fail because ownership correlations must be nonlocal; this result is not an ownership-ideal obstruction or leaf certificate.",
            "independent_ideas": ["root-free signed local ownership-routing kernel", "fully symmetric incidence-matrix basis of all covering coordinates", "exact transportation/cohomology system with a left-null witness on failure"],
            "falsifier": "Any raw ownership/type instance whose moment or totality equation disagrees with the complete-type quotient, or any nonzero augmented coefficient product, invalidates the affected claim.",
            "next_action": "Open Cycle 39 for a root-free exact signed local routing kernel over all legally covering owner choices; use the symmetric incidence basis as the principal alternative and preserve an exact left-null witness if rank-two feasibility fails.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "primary_wall_seconds": result["wall_seconds"], "shell_elapsed_seconds": 1395.04, "peak_rss_kib": 129956, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 38 rooted ownership functional"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_ownership_functional.py", "independent_command": "taskset -c 0 .venv/bin/python proof/replay_cycle_38_ownership_functional_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_38_ownership_functional.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_38_ownership_functional -v", "check_command": ".venv/bin/python proof/build_cycle_38_lrc_ownership_functional.py --check"},
        "sealer": {"path": "proof/build_cycle_38_lrc_ownership_functional.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
