"""Seal Cycle 15's exact bounded LRAT-slicing no-go."""

from __future__ import annotations

from pathlib import Path

from check_cycle_15_resolution_slicing import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256
from lrc_resolution_slicing import OUT, read_table

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-15-b015-lrc-resolution-slicing-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-15-b015-lrc-resolution-slicing-preregistration-v1.md", "6a79aef6ca45879a94d0378da95813c9b25a16e2460aa2fd36a2648a1891e052"),
    "engine": (ROOT / "discovery/lrc_resolution_slicing.py", "8c8a19962a82a8d2c66b4419d5612007bece0301be97df712e565e6579831037"),
    "soundness": (ROOT / "proof/cycle_15_resolution_slicing_soundness.md", "392d97fc0dce3f52def357addddaa42b2617d66e01ef323d58667c7db5a256fe"),
    "audit": (ROOT / "proof/check_cycle_15_resolution_slicing.py", "368da9b811e79a375f4ee07b33382121a5a281ab3ae0d77012ff3ff767b7f0e7"),
    "test": (ROOT / "tests/test_cycle_15_resolution_slicing.py", "25c20c5129f030ff48c59546fbcdd3791d35644e84aa167e89761b4df37bf49d"),
    "source_lrat": (OUT / "source.lrat", "6c167fa38747a834108855ca5a0222a68e11ff5d6520d95a607a598e6a2ada76"),
    "analysis_result": (OUT / "analysis.result", "8306a40b640e4b3b9ac7bdcccc69c9f41307bc2ca81ddfcca8601aac05630f7e"),
    "candidate_table": (OUT / "candidates.tsv", "d678e149175093dd98be4bfaf6f980278dca3cbec8813c5b9769160cf0e97263"),
    "result_table": (OUT / "results.tsv", "1cef00a522085c9933919c23abef987510f0a11f3268a02cf9311860e55a3cd9"),
    "solve_result": (OUT / "solve.result", "73b7b4f4d0cc17db8f57674f58f54dc1388f6a5cc8b23ac878f78965b6d83984"),
    "lrat_timing": (ROOT / "discovery/out/cycle15-lrat.time", "3f11a6aad0baaa436c25c7e1a67bec0c264411a7e3399f43b3facbe81a8609af"),
    "analysis_timing": (ROOT / "discovery/out/cycle15-analysis.time", "bc67c08c62ab1a3f22d52340b6bfcdb856d8bf1c33c123b7670afb78beaf13bc"),
    "solve_timing": (ROOT / "discovery/out/cycle15-solve.time", "4c5bf97f8031d601d0dde2b5faf0fa900c0bfbaa6f2769913e9dca080b344bbe"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 15 resolution slicing")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit()
    manifest = []
    for row in read_table(OUT / "results.tsv"):
        family, parameter = row["family"], row["parameter"]
        cnf = OUT / f"candidates/{family}-{parameter}.cnf"
        model = OUT / f"models/{family}-{parameter}.model"
        if sha256(cnf) != row["cnf_sha256"] or sha256(model) != row["evidence_sha256"]:
            raise RuntimeError("candidate evidence hash mismatch")
        manifest.append({
            "family": family,
            "parameter": int(parameter),
            "clauses": int(row["clauses"]),
            "discriminating_clauses": int(row["discriminating_clauses"]),
            "status": "CERTIFIED_SAT",
            "cnf_path": str(cnf.relative_to(ROOT)),
            "cnf_sha256": row["cnf_sha256"],
            "model_path": str(model.relative_to(ROOT)),
            "model_sha256": row["evidence_sha256"],
        })
    return {
        "artifact_id": "cycle-15-b015-lrc-resolution-slicing-v1",
        "budget_ordinal": "B015",
        "cycle": 15,
        "record_type": "STRUCTURAL_NO_GO",
        "recorded_at_utc": "2026-08-03T21:01:40Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The checked LRAT proof depends on 2294 of 2329 source clauses. Its final empty clause has 31 immediate branches and no derived node reachable from every branch, so there is no strict derived dominator of the input super-sink. All six frozen protected distance/frequency slices of sizes 128, 256, and 500 are SAT by preserved, directly checked models. Hence none is a small UNSAT source slice.",
        "claim_boundary": "This closes only strict derived dominators and the six frozen graph-centrality prefixes for one proof. It does not establish source-core minimality or exclude other subsets, branch-community unions, proofs, cores, target embeddings, F_1 or J emptiness, or LRC(13).",
        "dependency_result": {
            "epistemic_status": "PROVED",
            "final_empty_id": summary["empty_id"],
            "source_clauses": 2329,
            "reached_input_clauses": summary["reached_inputs"],
            "irrelevant_to_lrat_derivation": 35,
            "immediate_branches": summary["root_children"],
            "strict_derived_dominator_candidates": summary["dominator_candidates"],
        },
        "slice_result": {
            "epistemic_status": "PROVED",
            "candidates": 6,
            "certified_sat": summary["sat_candidates"],
            "certified_unsat": 0,
            "caps": 0,
            "errors": 0,
            "advance_gate": "FAIL: no at-most-500 certified UNSAT slice",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The exact result concerns one strict-dominator test and six prefixes, not all proof-graph unions or core minimality.",
            "recommendation": "Seal Cycle 15; reranking more heuristic prefixes is low-information continuation.",
            "strongest_flaw": "Centrality prefixes can destroy complementary constraints by removing one half of each necessary pair.",
            "falsifier": "Any LRAT/source-ID mismatch, missed all-branch-reachable node, invalid SAT model, or certified UNSAT frozen slice invalidates the affected result.",
            "independent_ideas": ["gcd-conditioned learned-certificate decision tree", "exact CRT equivalence preflight", "certificate-checked resolution-community subset optimization"],
            "next_action": "New Cycle 16: exact gcd-conditioned learned-certificate decision tree, with cover-deficit or DRAT closure at every leaf.",
        },
        "resources": {
            "aggregate_wall_seconds": 40.59,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 221_412,
            "corpus_bytes": 136_118_395,
            "temporary_disk_cap_bytes": 21_474_836_480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "candidate_manifest": manifest,
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "audit_command": "python3 proof/check_cycle_15_resolution_slicing.py",
            "check_command": "python3 proof/build_cycle_15_lrc_resolution_slicing.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_15_resolution_slicing.py -v",
        },
        "sealer": {"path": "proof/build_cycle_15_lrc_resolution_slicing.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
