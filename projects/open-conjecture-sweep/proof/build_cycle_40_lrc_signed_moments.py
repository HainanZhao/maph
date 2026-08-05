"""Seal Cycle 40's exact signed ownership moments through degree three."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_40_signed_moments import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle40-signed-moments"
OUTPUT = ROOT / "artifacts/cycle-40-b040-lrc-signed-moments-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-40-b040-lrc-signed-moment-preregistration-v1.md", "d354ea209bb49a43aaa847d5c9ae5ddd9dc3c0a3365f6af2ba50e93c5bb0930b"),
    "cycle29_artifact": (ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v2.json", "faf097ebcc22e9e18055cbf4139aef30e17ee85e86ea2096d43b31873f6e8d09"),
    "cycle39_artifact": (ROOT / "artifacts/cycle-39-b039-lrc-priority-routing-v1.json", "5dfcf363b54fe238021ae84d968a9e10e6a1000fd032b9e81c6839352bc88ec4"),
    "idea_selection": (ROOT / "discovery/cycle40_signed_moment_idea_selection.md", "f689cf65c6614c06d8269636d7798ba92f8e4ff27b7048a7dd42ebabdf411634"),
    "primary_engine": (ROOT / "discovery/lrc_signed_ownership_moments.py", "cb76981ee928abd7b25bf665a83a55e883587c2c89b26b35282226a0afbae5f3"),
    "primary_result": (OUT / "result.json", "fcdcdf203ae7f4c213694039f26b7b3b80a296a79193449c0dddc8f6bd707ecb"),
    "initial_timing": (OUT / "run-initial.time", "42c9cfc2283a9661eb819dfd4aa45878f2bd10837d898e46a94dd7abefc5e1b6"),
    "induced_timing": (OUT / "run-induced.time", "7b99e8dc73308dc90122391d966bbb04f73c3148cd79b040a66d92c03fe1d072"),
    "final_timing": (OUT / "run.time", "08c0fde7d13ae550a3c85de49bf17551735a0ec497aba4f95a49ae039d709e54"),
    "independent_replay": (ROOT / "proof/replay_cycle_40_signed_moments_independent.py", "c85fb0019a542a7f5963e2cb11c2118d2be6f4fb0e3897a8a8574ea5b8e26322"),
    "independent_result": (OUT / "independent-replay.json", "cfdd84543d08e21f6f0ca4ec490059ab89df4ed20241ff297e619146e52a4b0f"),
    "independent_timing": (OUT / "independent-replay.time", "222c5809b8a7a34ec3c125f3849ef6b80cca6c624341c34e5f194c7aa262f69e"),
    "audit": (ROOT / "proof/check_cycle_40_signed_moments.py", "c5724678db1250b4a56fb87e30339a23107a48ff948af8a5e6655726be68a7f0"),
    "soundness": (ROOT / "proof/cycle_40_signed_moments_soundness.md", "b301c11384f25fee19ed4a2debffc894c075205837070a970904b1069f45227b"),
    "test": (ROOT / "tests/test_cycle_40_signed_moments.py", "3f5bea8a7be97b43aad6325ee5eddfa2d2c74f7dde65c950bcdec8a752509d7b"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload() -> dict[str, object]:
    checked = audit()
    result = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    return {
        "artifact_id": "cycle-40-b040-lrc-signed-moments-v1",
        "budget_ordinal": "B040",
        "cycle": 40,
        "record_type": "PROVED_SIGNED_DEGREE_THREE_MOMENT_CONSTRUCTION",
        "recorded_at_utc": "2026-08-04T20:04:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A mass-one rational signed ownership-moment family exists through degree three on p199 base 4 / leaf 78. It satisfies one-hot totality, lifted rank-one support, every unmultiplied rank-two blocker, every unmultiplied rank-three blocker, and exact lower-marginal compatibility.",
        "claim_boundary": "This is a signed local moment construction for one leaf. It is not positive, not a global ownership distribution, not a functional on the full ownership ideal, not a leaf certificate, and not LRC(13). It does not impose arbitrary ownership-literal multiples of rank-two or rank-three blockers.",
        "audit": checked,
        "construction": {
            "epistemic_status": "PROVED",
            "complete_types": result["complete_types"],
            "singleton_variables": result["singleton_variables"],
            "singleton_solution": result["singleton_system"],
            "rank_two_type_tuples": result["rank_two_type_tuples"],
            "pair_classes": result["rank_two_pair_classes"],
            "component_equations": result["deduplicated_component_equations"],
            "rank_three_type_tuples": result["rank_three_type_tuples"],
            "triple_mask_classes": result["triple_completion"]["classes"],
            "initial_nonsurjective_triple_classes": result["triple_completion"]["initial_failing_classes"],
            "induced_pair_deletion_classes": result["triple_completion"]["induced_pair_deletion_classes"],
            "binary_exceptional_triples": result["triple_completion"]["binary_triple_type_classes"],
            "unresolved_triple_classes": result["triple_completion"]["unresolved_kernel_mask_classes_after_induced_pair_zeros"],
            "independent_replay": replay["status"],
        },
        "structural_implication": {
            "epistemic_status": "PROVED",
            "statement": "Unmultiplied ownership blockers and lifted rank-one support alone cannot yield a mass contradiction through degree three on this frozen quotient, because the explicit signed countermodel satisfies all of them.",
            "planning_inference": "CONJECTURED: the first high-information next test is the omitted family consisting of one ownership-literal multiple of every rank-two blocker, not a larger search over local deterministic routing rules.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_AND_OPEN_DISTINCT_MULTIPLIED_IDEAL_TEST",
            "scope_review": "Independent replay supports the exact local degree-three construction, while explicitly withholding probability, global gluing, leaf, and LRC interpretations.",
            "strongest_flaw": "Signed local consistency survives by cancellation because Cycle 40 omits ownership-literal multiples of rank-two blockers.",
            "independent_ideas": ["degree-three ownership-literal multiplied rank-two ideal test", "deferred Cech/cohomological gluing class after a proved bridge", "recursive extension theorem only if the next cycle exposes a canonical extension rule"],
            "recommended_action": "Open Cycle 41 for a sharply bounded exact test of all Boolean-reduced products y_(u,k) times every rank-two blocker, with complete raw replay or an exact augmented left-null certificate.",
            "falsifier": "Any missing multiplier class, Boolean-reduction error, quotient/raw incidence mismatch, or nonzero raw contracted generator invalidates the affected conclusion.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "primary_wall_seconds": 150.80, "independent_wall_seconds": replay["wall_seconds"], "cumulative_wall_seconds": 229.29, "peak_rss_kib": 1238708, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 40 signed degree-three ownership moments"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_signed_ownership_moments.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_40_signed_moments_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_40_signed_moments.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_40_signed_moments -v", "check_command": ".venv/bin/python proof/build_cycle_40_lrc_signed_moments.py --check"},
        "sealer": {"path": "proof/build_cycle_40_lrc_signed_moments.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
