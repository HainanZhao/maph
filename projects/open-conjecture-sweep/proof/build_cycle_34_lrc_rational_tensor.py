"""Seal Cycle 34's exact rational degree-zero tensor obstruction."""
from __future__ import annotations

from pathlib import Path

from check_cycle_34_rational_tensor import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle34-rational-tensor"
OUTPUT = ROOT / "artifacts/cycle-34-b034-lrc-rational-tensor-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-34-b034-lrc-rational-tensor-preregistration-v1.md", "5937a7f50f0047d4de78fe25f10520200d47ccb562237aa9c7089a74cb66a9f4"),
    "prior_artifact": (ROOT / "artifacts/cycle-33-b033-lrc-odd-tensor-v1.json", "b8c99a100232ca5eab96b3cac11852c247b1ee53527f38566b0dab53158dcb98"),
    "idea_selection": (ROOT / "discovery/cycle34_rational_tensor_idea_selection.md", "f77dfacc22de14b8cde6cee089649d39691f7f3b38f4700a9f2063452792e6d2"),
    "primary_engine": (ROOT / "discovery/lrc_rational_tensor.py", "2c326d991941911c56f2acbf7dd3631e5c74111f0e5cc707c708ac89b0ea869d"),
    "independent_replay": (ROOT / "proof/replay_cycle_34_rational_tensor_independent.py", "e7c526831e3407a8494ea5d2e20138aeaa75cd580c9691dacb63ceacfd087b4a"),
    "audit": (ROOT / "proof/check_cycle_34_rational_tensor.py", "5213eaf5573987ef68165fbc9946ed2e8125493974f9956f63b39902241441d6"),
    "soundness": (ROOT / "proof/cycle_34_rational_tensor_soundness.md", "7dd6e208e19b044529eda63f68c99a933c2518c067199abcd743fe6a4d55f2ca"),
    "test": (ROOT / "tests/test_cycle_34_rational_tensor.py", "821d06a762c6149d1411013f6d6926c5bb3e160c358bc2966a4cf36ec4af5e1f"),
    "primary_result": (OUT / "result.json", "478a3b0a083d84b684cd377707e4ebbc07e4f36d8cad5be9d213a4fef697a0cd"),
    "independent_result": (OUT / "independent-replay.json", "3b980e40d020202115cdb4382c9ec1cbcbb72dd53a6105225b3e87b2bd047c12"),
    "primary_timing": (ROOT / "discovery/out/cycle34-rational-tensor.time", "001be3552576dfbb2c4ab06be32471f03d6afa390d31853a681052b6471db727"),
    "independent_timing": (OUT / "independent-replay.time", "dc373d85a7df6a16864ab0ecd5c40b68a737d5753ac0aaf61349b34dbccc2022"),
    "pari_script": (OUT / "solve-01.gp", "655f3e28da679afe2071cfc4c7d651eb632e0827c954c3981c9883d6d2d6d369"),
    "pari_solution": (OUT / "solve-01.txt", "51c1a178aee0f253019d6ed1fe43e58ef6655c7595b9c2be27bd16c671d61596"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-34-b034-lrc-rational-tensor-v1",
        "budget_ordinal": "B034",
        "cycle": 34,
        "record_type": "PROVED_RATIONAL_DEGREE_ZERO_OBSTRUCTION",
        "recorded_at_utc": "2026-08-04T15:00:15Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The constant tensor is not in the degree-zero rational span of the 1,394 direct uncovered predicates for p199 base 4 / leaf 78. A primitive 1,229-term integer left-null vector annihilates all 1,394 predicate columns and has nonzero coefficient sum.",
        "claim_boundary": "This proves rational inconsistency only for degree-zero direct uncovered predicates on the frozen 4,243-row restriction of one p199 leaf. It does not exclude the leaf, positive degree, ownership auxiliaries, other leaves, or LRC(13).",
        "audit": checked,
        "finite_results": {
            "epistemic_status": "PROVED",
            "matrix": {"assignment_rows": 4243, "predicate_columns": 1394, "assignment_hash": checked["assignment_hash"]},
            "modular_selection_only": {"field": 5, "basis_rank": 1228, "contradiction_rows": 985},
            "integer_certificate": {"terms": 1229, "maximum_height_bits": 2807, "predicate_sum": "ZERO", "rhs_nonzero": True, "primitive": True},
            "rational_degree_zero_identity": False,
            "independent_direct_set_replay": "PASS",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_CERTIFICATE_STRUCTURE_QUESTION",
            "scope_review": "A separately reconstructed direct-set matrix verifies the integer witness, so the conclusion is proof-grade and field-independent over Q. The witness says nothing about positive-degree or enlarged semantic families.",
            "strongest_flaw_resolved": "The primary selector, predicate construction, and solve shared a representation; the independent route rebuilt every predicate membership and assignment before big-integer accumulation.",
            "independent_ideas": ["factor the exact witness into a low-rank coordinate-tensor or Mobius decomposition", "perform a degree-one column census only after structural analysis", "use ownership auxiliaries only if the certificate exposes a missing coordinate-local semantic factor"],
            "falsifier": "Any independently regenerated nonzero predicate dot product or zero RHS invalidates the certificate. For the next mechanism, a flattening rank above its frozen cap falsifies the proposed low-rank decomposition family.",
            "next_action": "Open Cycle 35 to ask whether the exact integer witness admits a certified low-rank coordinate-tensor or Mobius-factor decomposition exposing a smaller local invariant.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 28.86, "largest_peak_rss_kib": 1728296, "memory_max_bytes": 8589934592, "temporary_disk_cap_bytes": 5368709120, "exact_solver": "GP/PARI 2.15.4, GMP 6.3.0"},
        "runtime": check_runtime("Cycle 34 rational tensor obstruction"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_rational_tensor.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_34_rational_tensor_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_34_rational_tensor.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_34_rational_tensor -v",
            "check_command": ".venv/bin/python proof/build_cycle_34_lrc_rational_tensor.py --check",
        },
        "sealer": {"path": "proof/build_cycle_34_lrc_rational_tensor.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
