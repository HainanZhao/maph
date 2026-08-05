"""Seal Cycle 32's exact degree-zero GF(2) tensor boundary."""
from __future__ import annotations

from pathlib import Path

from check_cycle_32_gf2_tensor import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle32-gf2-tensor"
OUTPUT = ROOT / "artifacts/cycle-32-b032-lrc-gf2-tensor-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-32-b032-lrc-gf2-tensor-preregistration-v1.md", "f60fbb26b8e02a01514b8ee63bee19f6888a6d34b7693a5251c5716f45d07ed1"),
    "ownership_artifact": (ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v2.json", "faf097ebcc22e9e18055cbf4139aef30e17ee85e86ea2096d43b31873f6e8d09"),
    "prior_artifact": (ROOT / "artifacts/cycle-31-b031-lrc-convolution-quotient-v1.json", "1bb295614b4bb9c0fa186feedc6dc37dffd3d3ba030b891e4ac7d2d17f451467"),
    "idea_selection": (ROOT / "discovery/cycle32_gf2_tensor_idea_selection.md", "b5d883b985f08a8b3c64ae58eff61ae0ecdedc4f20f2bfe76b983a0a14212509"),
    "primary_engine": (ROOT / "discovery/lrc_gf2_tensor.py", "b686c5f0a05d2d24fe5ee70f7c4602caf7870be8ab0dc20b255045e798035e50"),
    "independent_replay": (ROOT / "proof/replay_cycle_32_gf2_tensor_independent.py", "219d9b482331044e515587f2af333ff4f220ae98ed2f6a4c0d7ac6682eab4c8f"),
    "audit": (ROOT / "proof/check_cycle_32_gf2_tensor.py", "8fac9ef513c672f3d210ad28823581ef943c3c02b8d8eeed22a860cb8bdc8fdc"),
    "soundness": (ROOT / "proof/cycle_32_gf2_tensor_soundness.md", "56e5ca59c0c1bbd92bab14ff3a75e074c8e15f6033fdbc1a8f257ce41ea271f2"),
    "test": (ROOT / "tests/test_cycle_32_gf2_tensor.py", "0c66a107e450488b7aac34043b3ae8dc569eb790b65dc16848b1b237a574d2d5"),
    "primary_result": (OUT / "result.json", "7fa9ea71f14096276bf5d708d775316083cbffab817e3937aea28ab5c7817c87"),
    "independent_result": (OUT / "independent-replay.json", "20111fa1aed1766280d6304b7919bafe5a444eca1279fd1f12892930bb8b54e4"),
    "primary_timing": (ROOT / "discovery/out/cycle32-gf2-tensor.time", "11c64b389a2036c52a84b31867b5dee3b0b8a51bf47bea68fa2c80707cecd2f4"),
    "independent_timing": (OUT / "independent-replay.time", "8c72808e455058bb7852b6993a03e145a83d33e98d01f5f42958549317ccba83"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-32-b032-lrc-gf2-tensor-v1",
        "budget_ordinal": "B032",
        "cycle": 32,
        "record_type": "PROVED_DEGREE_ZERO_FIELD_BOUNDARY",
        "recorded_at_utc": "2026-08-04T14:36:10Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A degree-zero GF(2) uncovered-tensor identity exactly refutes the first infeasible H11 base, but no such identity exists for p199 base 4 / leaf 78: a 577-row evaluation subsystem has zero XOR on all 1,394 predicate columns and RHS one.",
        "claim_boundary": "This classifies only degree-zero GF(2) combinations of negation-deduplicated direct uncovered predicates for one H11 base and one p199 leaf. It does not constrain odd characteristics, rational coefficients, positive degree, ownership polynomial calculus, the leaf itself, or LRC(13).",
        "audit": checked,
        "finite_results": {
            "epistemic_status": "PROVED",
            "h11": {"base": [1, 1, 1], "assignments": 64, "identity": "F_12=1", "coefficient_weight": 1},
            "p199": {"base_index": 4, "leaf_ordinal": 78, "predicate_columns": 1394, "evaluation_rows": 4243, "rank_least_pivot_before_contradiction": 1226, "contradiction_rows": 577, "degree_zero_identity": False, "independent_reverse_elimination": "INCONSISTENT"},
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_DISTINCT_ODD_CHARACTERISTIC_QUESTION",
            "scope_review": "The exact left-null XOR witness eliminates the entire degree-zero GF(2) family, but parity is unusually restrictive and cannot stand for other fields.",
            "strongest_flaw": "The positive H11 control is a fixed-uncovered-time identity; p199 may admit signed identities in odd characteristic even though parity fails.",
            "independent_ideas": ["test degree zero over GF(3) and GF(5) before positive degree", "defer degree-one GF(2) until an exact column-count benchmark", "defer rational Gram and ownership auxiliaries because of higher state cost"],
            "falsifier": "For each odd field, an exact left-null witness eliminates degree zero; any candidate identity requires full tensor verification rather than sampled agreement.",
            "next_action": "Open a distinct cycle for degree-zero GF(3) and GF(5) on the same frozen interface before considering positive degree.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 1.91, "largest_peak_rss_kib": 24320, "memory_max_bytes": 4294967296, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 32 GF2 tensor boundary"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_gf2_tensor.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_32_gf2_tensor_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_32_gf2_tensor.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_32_gf2_tensor -v",
            "check_command": ".venv/bin/python proof/build_cycle_32_lrc_gf2_tensor.py --check",
        },
        "sealer": {"path": "proof/build_cycle_32_lrc_gf2_tensor.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
