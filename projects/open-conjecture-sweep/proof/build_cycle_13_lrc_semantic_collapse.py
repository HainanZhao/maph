"""Seal Cycle 13's exact collapse of the frozen typed semantic map family."""

from __future__ import annotations

from pathlib import Path

from check_cycle_13_semantic_collapse import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-13-b013-lrc-semantic-collapse-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-13-b013-lrc-semantic-instantiation-preregistration-v1.md", "51d469863b7485917f906010dcbe428331d795cd8ca9c499846a6c73557be7cb"),
    "soundness_and_collapse": (ROOT / "proof/cycle_13_semantic_instantiation_soundness.md", "5f06b6279eda04b7efae74cae3a592ac8bd3019f6e141db6fc01b30f5d555743"),
    "independent_audit": (ROOT / "proof/check_cycle_13_semantic_collapse.py", "5ce4c89c33fd9300fda424adeb7fe1496bb0eb0654afe9ac429cea1062da7c6e"),
    "audit_result": (ROOT / "discovery/out/cycle13-collapse.result", "e387ce72bfb4e71ecbe7860c5dbd09f99a1367f148949c90022f65b02eace3bb"),
    "audit_timing": (ROOT / "discovery/out/cycle13-collapse.time", "402ae2bb17fb0267d0442ef5704024251267d847b93e9da62bdadfcc40e63eae"),
    "source_core": (ROOT / "discovery/out/cycle12-core-template/mus/076.cnf", "6179017eaa361064bcd36c9dc71a14e4d0d818b5e8cdb3d7e433c6e96f8d31bc"),
    "source_proof": (ROOT / "discovery/out/cycle12-core-template/mus/076.drat", "d7fcabaae24d3f320ca3d46bf557a72a2792b94a023092d0ceb0ce9d140153ac"),
    "cycle12_artifact": (ROOT / "artifacts/cycle-12-b012-lrc-core-template-v1.json", "45a160c8a0f843820daabe6a2305c9c9563f25786a3fd4cc556ce2d90b0515c7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_13_semantic_collapse.py", "5fe9fc581781df383dbeca38c8a1186184a2c8820b2ed2d87b3d04b23e696b24"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 13 semantic collapse")
    frozen = freeze_inputs(ROOT, INPUTS)
    partition = audit()
    expected = {
        "choice_at_most_one": 196,
        "color_invariant_coverage": 12,
        "x_implies_y2": 84,
        "y2_cardinality": 1,
    }
    if partition != expected:
        raise RuntimeError("frozen clause partition mismatch")
    return {
        "artifact_id": "cycle-13-b013-lrc-semantic-collapse-v1",
        "budget_ordinal": "B013",
        "cycle": 13,
        "record_type": "STRUCTURAL_NO_GO",
        "recorded_at_utc": "2026-08-03T19:41:26Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "For the frozen 293-clause row-76 certified subcore, every divisor-color-preserving within-coordinate choice bijection either fixes a coverage clause setwise or maps a universal exactly-one/gcd-channel clause to another universally present clause. Therefore a Cycle-13 typed embedding exists exactly when a Cycle-12 residue-identity coordinate embedding exists. Cycle 12 proved none exists in the frozen 20 validation and 100 external targets.",
        "claim_boundary": "This closes only the selected core and the frozen coordinate-permutation plus 2/7-divisor-color-preserving within-coordinate substitution family. It does not constrain alternate proofs or cores, finer semantic roles, resolution motifs, exact CRT, full F_1 or J emptiness, or LRC(13).",
        "collapse_theorem": {
            "epistemic_status": "PROVED",
            "source_clauses": 293,
            "clause_partition": partition,
            "validation_nonmatches_inherited": 20,
            "external_nonmatches_inherited": 100,
            "reason": "The only target-dependent source clauses are unions of complete divisor-color classes, hence invariant under every permitted within-coordinate bijection; all other images are guaranteed target schemas.",
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "event": "The first audit invocation incorrectly normalized an already-normalized target formula and failed its y2-channel control. The audit was corrected before the successful replay and sealed result.",
            "effect_on_claim": "None: the failing implementation produced no mathematical conclusion; the final checker, separate regression invocation, and measured replay all passed.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The result closes this specific typed-substitution family only after clause-by-clause multiplicity audit.",
            "recommendation": "Continue Cycle 13 only for the scripted audit; if it passes, seal immediately and do not run the redundant long search.",
            "strongest_flaw": "A partial color class, channel mismatch, or multiplicity error would defeat the collapse.",
            "falsifier": "Any permitted within-color bijection changing a target-dependent clause, or any target match available only under a nonidentity residue map, invalidates the collapse.",
            "independent_ideas": ["alternate DRAT/MUS proof diversification", "resolution-proof motifs", "exact CRT equivalence prototype"],
            "next_action": "Open Cycle 14 for proof diversification and seek certified cores with non-color-invariant coverage structure.",
        },
        "resources": {
            "principal_replay_wall_seconds": 29.03,
            "aggregate_wall_seconds_observed": 89.0,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 643_184,
            "temporary_disk_cap_bytes": 21_474_836_480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "audit_command": "python3 proof/check_cycle_13_semantic_collapse.py",
            "check_command": "python3 proof/build_cycle_13_lrc_semantic_collapse.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_13_semantic_collapse.py -v",
        },
        "sealer": {"path": "proof/build_cycle_13_lrc_semantic_collapse.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
