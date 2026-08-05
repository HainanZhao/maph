"""Seal Cycle 29's exact ownership/blocker semantic interface."""
from __future__ import annotations

from pathlib import Path

from check_cycle_29_ownership_blocker import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle29-ownership-blocker"
OUTPUT = ROOT / "artifacts/cycle-29-b029-lrc-ownership-blocker-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-29-b029-lrc-ownership-blocker-preregistration-v1.md", "52296c1d5fd3b5fe69d45d7bd57cb243a1d7c3c8eae9478577795d1fe4a88263"),
    "semantic_collapse_boundary": (ROOT / "artifacts/cycle-13-b013-lrc-semantic-collapse-v1.json", "96be5ec65bc9fe433dc02292c333cae08f856ec2ed5b33853c31ce22f1aafb6e"),
    "prior_artifact": (ROOT / "artifacts/cycle-28-b028-lrc-portfolio-cyclic-width-five-v1.json", "60baf18fb77e0edb0ef8e80f7bf32a603296984d0166b6aef0a3f884f4ea90f9"),
    "idea_selection": (ROOT / "discovery/cycle29_semantic_primal_idea_selection.md", "bcf8d3f590bb740ef672a9df20aa1c96cd914270139afb09dcfbf732b4ae51d1"),
    "primary_engine": (ROOT / "discovery/lrc_ownership_blocker.py", "68f41288d000638b74bf2d0cfb0cc020754aa38f46e0328b7c591c2122740cda"),
    "independent_replay": (ROOT / "proof/replay_cycle_29_ownership_blocker_independent.py", "5ea4751be12bea744c96591e107cb8e8e801c1e2d75ec075d8c46e2a3a66bf80"),
    "audit": (ROOT / "proof/check_cycle_29_ownership_blocker.py", "8c2f04eadbd56401898f6012c84d76ce3c3b67d81628eb3b9375dd0ef6a9fc2b"),
    "soundness": (ROOT / "proof/cycle_29_ownership_blocker_soundness.md", "cae55125a4255c1c3e404225cc6b2c68f1ade69c32a8fdd42180d7064656feda"),
    "test": (ROOT / "tests/test_cycle_29_ownership_blocker.py", "79ee6afd7956cc097858518ba23fad505adf5d89930f18d9d946d437957a5b07"),
    "primary_result": (OUT / "result.json", "b213f8b790b2f53e2de30d244ead973143973e236083d24b38fffb5234271f15"),
    "primary_summary": (OUT / "summary.txt", "5ca1eb6a01fffce66b95200b3a74032c4e36564dc8f88833a59b1d2e7fb008af"),
    "primary_timing": (OUT / "run.time", "1a7aaa79ff4969b9f7c48fb5644da74486dd953e918e01981c854200a9ef899b"),
    "independent_result": (OUT / "independent-replay.json", "0c3888ad16b9038067d2df13897a03acbb794cd12f2dd4932a8b4dd611653632"),
    "independent_timing": (OUT / "independent-replay.time", "2908c8d872276110dbd7633f6b9183837d2ae2ee5252e7373a7ea1b73279cf12"),
    "target_cnf": (ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", "ea4356bd1ff5cdf06fb5504411d0ca57ddc8b3056dc8281c8025d1d24ef60648"),
    "targets": (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv", "aa78578f2e54e7045d6dcf63e1278805d04057e48cd2b3981a4853889074e3d3"),
    "bases": (ROOT / "discovery/out/cycle8-p199-strata.txt", "327334cf85b821a77b254420d0617c8771a9f272cf38b2512ab79c937de4299b"),
    "direct": (ROOT / "discovery/lrc_pair_choice.py", "f3faa9c3152467243ec1acfe27310c857cadbbe40b565c7cf51fb6e47318d55a"),
    "coupled": (ROOT / "discovery/lrc_coupled_incidence.py", "b40d9ff5077b40caaeda0e1622d456ce9e9673c9451bc6cd19d2b58286853469"),
    "raw_masks": (ROOT / "discovery/lrc_width_four_stage_a.py", "3faee2712066bb15014b87b47f58a7be914298965dbf32678ee36485e9a0a9b9"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-29-b029-lrc-ownership-blocker-v1",
        "budget_ordinal": "B029",
        "cycle": 29,
        "record_type": "PROVED_SEMANTIC_INTERFACE",
        "recorded_at_utc": "2026-08-04T14:15:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Finite direct-cover feasibility is exactly equivalent to a labeled ownership partition avoiding complete coordinate-local blockers. Exact signature quotienting compresses the named p199 target's 190,867,444 concrete blockers to 12,264 patterns of rank at most three.",
        "claim_boundary": "The theorem holds for every finite frozen direct-cover interface. The exact computations validate two implementations and give a complete census only for p199 base 4 / leaf 78. They do not exclude that leaf, close the other 59 survivors, prove LRC(13), or make generic rank-three coloring a new engine.",
        "audit": checked,
        "theorems": [
            {"epistemic_status": "PROVED", "statement": "A direct full cover exists iff the time set has a labeled disjoint ownership partition whose coordinate cells each lie in one allowed digit mask."},
            {"epistemic_status": "PROVED", "statement": "A local cell is legal iff it contains no inclusion-minimal illegal blocker; digit-support signatures give a complete quotient, and each symbolic blocker lifts with multiplicity equal to the product of its signature-class sizes."},
            {"epistemic_status": "PROVED", "statement": "A minimal empty-intersection signature family has rank at most the number of allowed digits."},
        ],
        "finite_results": {
            "epistemic_status": "PROVED",
            "synthetic_interfaces": 327680,
            "h11_lifted_assignments": 64000,
            "h11_retained_improper_bases": 0,
            "p199_target": {"base_index": 4, "leaf_ordinal": 78, "times": 2786},
            "symbolic_patterns": 12264,
            "concrete_blockers": 190867444,
            "symbolic_rank_counts": {"1": 13, "2": 9311, "3": 2940},
            "max_rank": 3,
            "same_color_witness": {"coordinate": 0, "digits": [0, 4], "divisor_color": [0, 0], "distinguishing_time": 1},
            "independent_replay": "PASS",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_DISTINCT_SYNCHRONIZATION_ENGINE",
            "scope_review": "The exact labeled equivalence is genuinely stronger than Cycle 6's necessary-only uniform triple cut; forgetting labels or using generic hypergraph coloring collapses back toward that old relaxation.",
            "strongest_flaw": "Rank three alone is a re-expression, not a leaf certificate, and the local complexes remain coupled through the shared CRT time labels.",
            "independent_ideas": ["CRT-conjugacy synchronization invariant with exact integer-semigroup certificates", "coordinate-specific polynomial-calculus certificate after synchronization quotient", "small quotient nerve control before any topological campaign"],
            "falsifier": "An exact normalized ownership-summary state satisfying all transport and global-time relations shows that the selected synchronization invariant cannot exclude the target.",
            "next_action": "Open a distinct cycle for a smallest exact CRT-conjugacy synchronization prototype; do not continue with generic rank-three coloring.",
        },
        "resources": {
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
            "primary_wall_seconds": 5.362633,
            "independent_wall_seconds": 2.5,
            "largest_peak_rss_kib": 91108,
            "memory_max_bytes": 4294967296,
            "temporary_disk_cap_bytes": 5368709120,
        },
        "runtime": check_runtime("Cycle 29 ownership/blocker interface"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 taskset -c 0-2 .venv/bin/python discovery/lrc_ownership_blocker.py",
            "independent_command": "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 taskset -c 0-2 .venv/bin/python proof/replay_cycle_29_ownership_blocker_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_29_ownership_blocker.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_29_ownership_blocker -v",
            "check_command": ".venv/bin/python proof/build_cycle_29_lrc_ownership_blocker.py --check",
        },
        "sealer": {"path": "proof/build_cycle_29_lrc_ownership_blocker.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
