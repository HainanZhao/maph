"""Seal Cycle 14's bounded proof-diversification outcome."""

from __future__ import annotations

from pathlib import Path

from check_cycle_14_proof_diversification import audit, table
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle14-proof-diversification"
OUTPUT = ROOT / "artifacts/cycle-14-b014-lrc-proof-diversification-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-14-b014-lrc-proof-diversification-preregistration-v1.md", "ed63ff64f5efe8e2d623e81527ffa3f46aa24556cf4010becde8b43fcb6cc0d7"),
    "engine": (ROOT / "discovery/lrc_proof_diversification.py", "5f9081a7f23080c2f155b4bc41d55fc723e3a46ba066cd717bcf232818ccb664"),
    "audit": (ROOT / "proof/check_cycle_14_proof_diversification.py", "f275a3b5eb521acccbacfab4e651e1507c2b8a09fe9dddb9524d6c8c1686df8d"),
    "test": (ROOT / "tests/test_cycle_14_proof_diversification.py", "93721e3f5959f5ad97f7f74b6d746ea3522f1e7b96eb0a503b14c47d32269d04"),
    "census": (OUT / "census.tsv", "719b25fb733e475e27516cf375f5be486d2ecb089dd7d59280c3b54c2d01df40"),
    "census_result": (OUT / "census.result", "5655b5e8d0f0693017270cfba5c54b772d0f3447f914010a5f8a53693a633c47"),
    "diversified": (OUT / "diversified.tsv", "3f84bb6831e4dc2ceeeaaca454a15866749508096cf0431624f869711f3d2a7b"),
    "diversified_result": (OUT / "diversified.result", "f2239f23ba739fc27023a82120413cd7fad97b79d613b03afa0feed77d43a0bf"),
    "single_final_cnf": (OUT / "shrunk/007.cnf", "d5396917b2ce04460baea3367c5c69f8d09fd4341b255e356b9762327dac3446"),
    "single_final_proof": (OUT / "shrunk/007.drat", "3d902249cca83dd059faa347bef0c925a333fc888ed7323cbfa95aaace30e5a7"),
    "single_deletions": (OUT / "shrunk/deletions.tsv", "752de3c6d668a8a5e19c38a74f4f0b590aabb93c3e4e8bfaffcda511e21c3a5e"),
    "single_result": (OUT / "shrunk/shrink.result", "ce9bcc849326275568a4e16e8eb587c1362597d69d10c1c5281cebed8d61c5e0"),
    "group_final_cnf": (OUT / "role-groups/007.cnf", "f7b635e24d15054e13cbd302c746eb72f996ad6d5508483da3679756e9917c33"),
    "group_final_proof": (OUT / "role-groups/007.drat", "958a383fc710c9c1f1fb8649fe266987cdb7d23179ba61fb370b1d6fa01faafc"),
    "group_table": (OUT / "role-groups/groups.tsv", "c60836dfbf1ce705e3872802da233c0234afc8a06c3345afad67f2bc724845bb"),
    "group_result": (OUT / "role-groups/groups.result", "aea75db8288b7a5b8c95930e8bda566e65e9bf15373b2224a13074b7362517b7"),
    "diversify_timing": (ROOT / "discovery/out/cycle14-diversify.time", "d932665a762bff2992a136b8aa8ef214f952d8220dd54e76adab49c64005cb00"),
    "shrink_timing": (ROOT / "discovery/out/cycle14-shrink.time", "2240fe123b231ed0d3feb6ae2eec7973d281cdc436d064a638fe06194838e7a7"),
    "group_timing": (ROOT / "discovery/out/cycle14-role-groups.time", "c43c42174405cdb138b0e9ace4b50ae5a72a222531b7442671d568311e9ecab0"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 14 proof diversification")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit(False)
    certified = []
    for row in table(OUT / "diversified.tsv"):
        if row["status"] != "CERTIFIED":
            continue
        index = int(row["index"])
        core = OUT / f"cores/{index:03d}/{row['config']}/{row['mode']}.cnf"
        proof = OUT / f"core-proofs/{index:03d}/{row['config']}/{row['mode']}.drat"
        certified.append({
            "index": index,
            "configuration": row["config"],
            "extraction_mode": row["mode"],
            "clauses": int(row["clauses"]),
            "discriminating_clauses": int(row["discriminating_clauses"]),
            "core_path": str(core.relative_to(ROOT)),
            "core_sha256": row["core_sha256"],
            "proof_path": str(proof.relative_to(ROOT)),
            "proof_sha256": row["proof_sha256"],
        })
    return {
        "artifact_id": "cycle-14-b014-lrc-proof-diversification-v1",
        "budget_ordinal": "B014",
        "cycle": 14,
        "record_type": "BOUNDED_METHOD_FAILURE",
        "recorded_at_utc": "2026-08-03T20:52:21Z",
        "status": "SEALED",
        "epistemic_status": "MIXED",
        "outcome": "PROVED: the exact 80-core census found abundant non-color-invariant coverage structure, and 16 diversified extracted cores received fresh checked UNSAT certificates. OBSERVED: the frozen protected single-clause shrink made zero certified deletions (2328 CAP), and deleting any one of four whole role groups returned solver SAT and was retained. The selected core remains 2329 clauses with 1180 discriminating clauses and fails the preregistered at-most-500 advance gate.",
        "claim_boundary": "No result says a small discriminating core does not exist or that any retained individual clause is necessary. Timeout rows and unpreserved group-deletion SAT models are bounded method outcomes only. No validation/external embedding, full F_1 or J emptiness, or LRC(13) claim follows.",
        "exact_census": {
            "epistemic_status": "PROVED",
            "training_cores": 80,
            "selected_indices": [7, 4, 3],
            "selected_discriminating_counts": [1179, 1174, 1169],
        },
        "diversification": {
            "epistemic_status": "PROVED",
            "attempted_extractions": 27,
            "certified_cores": 16,
            "resource_caps": 11,
            "errors": 0,
            "selected": {"index": 7, "configuration": "noelimprobe", "mode": "default", "clauses": 2329, "discriminating_clauses": 1180},
        },
        "shrink_outcome": {
            "epistemic_status": "OBSERVED",
            "single_clause_attempts": 2328,
            "single_clause_caps": 2328,
            "certified_deletions": 0,
            "role_groups": 4,
            "role_groups_retained_after_solver_sat": 4,
            "role_group_caps": 0,
            "final_clauses": summary["final_clauses"],
            "final_discriminating_clauses": summary["final_discriminating"],
            "advance_gate": "FAIL: final core exceeds 500 clauses; validation instantiation not authorized",
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "event": "The initial table labeled CaDiCaL timeout exit 0 and wrapper timeouts as ERROR. Before selection it was deterministically repaired to 11 CAP and zero ERROR; accepted certificate rows were unchanged.",
            "effect_on_claim": "No mathematical effect: all 11 rows remain unknown and only the 16 proof-verified rows enter selection.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The certificates and census are exact; the timeout-limited shrink does not support nonexistence of a small core.",
            "recommendation": "Continue Cycle 14 for one frozen role-group deletion pass; if no group shrinks, seal and open Cycle 15.",
            "strongest_flaw": "A ten-second proof requirement made the individual deletion pass nearly vacuous.",
            "falsifier": "Any proof/core/hash/classification mismatch invalidates the affected certified claim; a checked UNSAT role-group deletion would falsify the practical group-necessity observation.",
            "independent_ideas": ["role-group deletion", "resolution-graph backward/dominator slicing", "exact CRT equivalence prototype"],
            "next_action": "New Cycle 15: resolution-graph backward/dominator slicing on the selected proof before another solver-driven shrink.",
        },
        "resources": {
            "aggregate_wall_seconds": 3464.65,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 816_132,
            "corpus_bytes": 4_866_609_841,
            "temporary_disk_cap_bytes": 21_474_836_480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "certified_core_manifest": certified,
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "structure_command": "python3 proof/check_cycle_14_proof_diversification.py --structure-only",
            "selected_proof_command": "python3 proof/check_cycle_14_proof_diversification.py",
            "check_command": "python3 proof/build_cycle_14_lrc_proof_diversification.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_14_proof_diversification.py -v",
        },
        "sealer": {"path": "proof/build_cycle_14_lrc_proof_diversification.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
