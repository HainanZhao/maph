"""Seal Cycle 12's certified syntactic core-template no-go."""

from __future__ import annotations

from pathlib import Path

from check_cycle_12_core_templates import structural, table
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-12-b012-lrc-core-template-v1.json"
OUT = ROOT / "discovery/out/cycle12-core-template"
MUS = OUT / "mus"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-12-b012-lrc-core-template-preregistration-v1.md", "c4eaa7beb2458fe93b840a28d33ba80902776cdeee1028a78cd1dcbb06224513"),
    "core_soundness": (ROOT / "proof/cycle_12_core_template_soundness.md", "e54fb67f096550912e454d49fa87149fbfb30346d69057bdbc53e0f7e855617c"),
    "embedding_completeness": (ROOT / "proof/cycle_12_embedding_completeness.md", "2c45f35118f6da8070d3bc67c6f216227f7033f5203397dd692094650ffdfe81"),
    "engine": (ROOT / "discovery/lrc_core_templates.py", "d5e1ae6e3cf80442dfc6e7fc520d7b9f946f2c1624c0f06dec7d04585b9a050d"),
    "independent_audit": (ROOT / "proof/check_cycle_12_core_templates.py", "5239ee0c6e70fb53d4aa26fe430c8062e15166179f3db9a1491299c239137fbb"),
    "core_table": (OUT / "cores.tsv", "854ab5266b1de712bd44d19ea0caa1983fb5372c429b5ec1b5f7cb6bd3fc5476"),
    "extraction_result": (OUT / "extract.result", "ca1693675d03784950488ac9f555458755845e6a257e67e19e2c9f72141e285b"),
    "whole_validation": (OUT / "validation-scores.tsv", "62746ad9af3a71d074dbf9f85d7c67a3fee4eb58c1756eb35241cad808b11ac1"),
    "whole_external": (OUT / "external-results.tsv", "8b62f9e1b3e43627bca64589a4ffe005619823944cdbe4105cef4aa4d88b8f8b"),
    "whole_result": (OUT / "search.result", "56ab8fadcbbf40e3b11c1b799620db297ccc25722b74fdbfa738e806cd1b2d9d"),
    "deletion_table": (MUS / "deletions.tsv", "3eb9c83c1e91aed6b145c19c837e7289757a18cb7e45668db745b22840160898"),
    "shrunk_cnf": (MUS / "076.cnf", "6179017eaa361064bcd36c9dc71a14e4d0d818b5e8cdb3d7e433c6e96f8d31bc"),
    "shrunk_proof": (MUS / "076.drat", "d7fcabaae24d3f320ca3d46bf557a72a2792b94a023092d0ceb0ce9d140153ac"),
    "shrunk_validation": (MUS / "validation.tsv", "855b24551a962a0b2be49da048a9196a0092d633f0e09ffce32b99678dab28cd"),
    "shrunk_external": (MUS / "external.tsv", "8b62f9e1b3e43627bca64589a4ffe005619823944cdbe4105cef4aa4d88b8f8b"),
    "shrink_result": (MUS / "shrink.result", "876f7898ebd5a83bd22f60bb8f452c5f6f3f547ef4e1eacf0c43d36de2b4a43d"),
    "shrunk_result": (MUS / "search.result", "bed989a46495b7b4a8ab0ee8e2b5092e4789fcad3f2edcd0a5fef7199458def3"),
    "self_embedding_result": (ROOT / "discovery/out/cycle12-self-embedding.result", "a57fea5c4f4cc213b16eb813f9f7e0ee0da267938609a01c6c8bd40c47d60739"),
    "audit_result": (ROOT / "discovery/out/cycle12-audit.result", "dff5506ee03e5950b7f9a7c576915d2147123593ed3004c04481c4ae7c8253ab"),
    "extraction_timing": (ROOT / "discovery/out/cycle12-extract.time", "cd49ff4545fbf58adcd7f5e5e3ac369945fe103b2ff7544da7a8a277df35144b"),
    "stopped_search_timing": (ROOT / "discovery/out/cycle12-search-v1.time", "7a7d90dd1d2d34288c066a4c301ec6940877c8f84e4d2abe22e7bb0d30c0b0ad"),
    "optimized_search_timing": (ROOT / "discovery/out/cycle12-search-v2.time", "d22fd89e49a28f0113565dddf397ce8bdf2c34f3f14ee137b94c3ba727f52e55"),
    "self_embedding_timing": (ROOT / "discovery/out/cycle12-self-embedding.time", "232977d7db9a04f90ae8e83dd7d3a76a6eea692cb772aa8865ce558db701be41"),
    "shrink_timing": (ROOT / "discovery/out/cycle12-shrink.time", "62557fc348ccffeb78d6929c15fa0fded70be2dd73010bb9029442d93492583a"),
    "shrunk_search_timing": (ROOT / "discovery/out/cycle12-search-shrunk.time", "ae7a1a32efd7344da42f5e88cfa2fd52499f12401b8e22d262707d631fe10a6f"),
    "audit_timing": (ROOT / "discovery/out/cycle12-audit.time", "32192930753cf6fdaabbc1a647e64cf070f5aeb086c4d7a4777037dd6b58e656"),
    "benchmark_timing": (ROOT / "discovery/out/cycle12-embedding-benchmark.time", "0e2a3db484a5e0665fea544ee77daaeb990f6cc96963a28c1cd68e4a57ea7b6c"),
    "optimized_benchmark_timing": (ROOT / "discovery/out/cycle12-embedding-benchmark-v2.time", "fafa167b5e0cebea642ff0635918c905af46b28703677480d3f73c2ba4060f21"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_12_lrc_core_templates.py", "10128db7598b314b497fc0ba6074604484a92812fd6f134154988b81e456b302"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 12 core templates")
    frozen = freeze_inputs(ROOT, INPUTS)
    structural()
    rows = table(OUT / "cores.tsv")
    manifest = []
    for row in rows:
        index = int(row["index"])
        core = OUT / f"cores/{index:03d}.cnf"
        proof = OUT / f"core-proofs/{index:03d}.drat"
        if sha256(core) != row["core_sha256"] or sha256(proof) != row["proof_sha256"]:
            raise RuntimeError(f"core certificate hash mismatch: {index}")
        manifest.append({
            "index": index,
            "core_path": str(core.relative_to(ROOT)),
            "core_sha256": row["core_sha256"],
            "proof_path": str(proof.relative_to(ROOT)),
            "proof_sha256": row["proof_sha256"],
            "clauses": int(row["clauses"]),
            "status": "CERTIFIED_UNSAT",
        })
    return {
        "artifact_id": "cycle-12-b012-lrc-core-template-v1",
        "budget_ordinal": "B012",
        "cycle": 12,
        "record_type": "STRUCTURAL_NO_GO",
        "recorded_at_utc": "2026-08-03T22:13:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The frozen lifted-residue/coordinate-permutation template family has no embedding in its held-out targets: all 80 certified training cores have zero matches across 20 validation CNFs, and the selected 302-clause core has zero matches across 100 external CNFs. Its certified 293-clause deletion-minimal subcore likewise has zero matches in all 20 validation and 100 external targets.",
        "claim_boundary": "This closes only literal clause-multiset containment under residue- and prime-preserving coordinate permutations for the frozen cores, split, and targets. It says nothing about other minimal cores, alternate proofs, semantic roles, generalized substitutions, interpolation, full F_1 or J emptiness, or LRC(13).",
        "certified_cores": {
            "epistemic_status": "PROVED",
            "count": 100,
            "checks": ["source clause-multiset subset", "fresh CaDiCaL UNSAT proof", "drat-trim VERIFIED", "positive source self-embedding"],
        },
        "whole_core_no_go": {
            "epistemic_status": "PROVED",
            "training_templates": 80,
            "validation_targets": 20,
            "validation_nonmatches": 1600,
            "selected_template": 76,
            "selected_clauses": 302,
            "external_targets": 100,
            "external_nonmatches": 100,
            "caps": 0,
        },
        "shrunk_template_no_go": {
            "epistemic_status": "PROVED",
            "source_template": 76,
            "original_clauses": 302,
            "certified_deletions": 9,
            "final_clauses": 293,
            "deletion_minimal_under_single_clauses": True,
            "minimality_check": "Each of 293 single-clause deletions received a CaDiCaL SAT model which the independent audit directly evaluated against every remaining clause.",
            "validation_nonmatches": 20,
            "external_nonmatches": 100,
            "caps": 0,
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "event": "The first whole-core search was intentionally stopped after 817.21 seconds because universal clauses were redundantly tested in the hot path. The optimized run omitted those clauses only from pruning and retained the complete final containment test.",
            "effect_on_claim": "None: the completeness argument permits removing a necessary pruning test, and the optimized run exhausted the same frozen mapping family without a cap.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal Cycle 12, then use semantic anti-unification with typed time-mask and coverage roles plus an exact instantiation checker in Cycle 13.",
            "scope_review": "The proof closes the frozen syntactic mapping family, not semantic templates or other MUSes.",
            "strongest_flaw": "The deletion-minimal subcore is not canonical; different proofs or deletion orders may expose different reusable structure.",
            "falsifier": "An omitted permitted embedding, failed source/proof replay, false mapped containment, or SAT target claimed UNSAT invalidates the affected result.",
            "alternatives": ["gcd-conditioned certificate decision tree", "exact CRT equivalence bridge"],
            "next_action": "Open a new Cycle 13 for semantic anti-unification; do not stop Problem 1 yet.",
        },
        "resources": {
            "aggregate_wall_seconds": 3033.19,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 1_126_144,
            "corpus_bytes": 2_930_387_362,
            "temporary_disk_cap_bytes": 21_474_836_480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "core_certificate_manifest": manifest,
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "structure_command": "python3 proof/check_cycle_12_core_templates.py",
            "full_embedding_command": "taskset -c 0-2 python3 proof/check_cycle_12_core_templates.py --embeddings",
            "full_proof_command": "taskset -c 0-2 python3 proof/check_cycle_12_core_templates.py --proofs",
            "check_command": "python3 proof/build_cycle_12_lrc_core_templates.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_12_lrc_core_templates.py -v",
        },
        "sealer": {"path": "proof/build_cycle_12_lrc_core_templates.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
