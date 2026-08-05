"""Seal Cycle 37's exact degree-two signed product functional."""
from __future__ import annotations

from pathlib import Path

from check_cycle_37_degree_two import EXPECTED_NORMALS, audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle37-degree-two-product"
OUTPUT = ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-37-b037-lrc-degree-two-product-preregistration-v1.md", "0b7a6f019b3f1e0e1a961eb0c013bf93a5c68cc6181d267299dcd05b8e17e91b"),
    "prior_artifact": (ROOT / "artifacts/cycle-36-b036-lrc-degree-one-pseudoexpectation-v1.json", "5b4e48dfefddbffa61ced6319439ad5d5a50fbc5b00dbaf15c88c283ede35dd8"),
    "idea_selection": (ROOT / "discovery/cycle37_degree_two_product_idea_selection.md", "d941629243d7715806ea94a5a2db805cbd92fc3f926993d3fd71ac04b32be8bc"),
    "primary_engine": (ROOT / "discovery/lrc_degree_two_predicate_compressed.py", "916dbf2db7878be8445ed1663c16ef7d5f961cdc23385ad9a64d630e49778e75"),
    "independent_replay": (ROOT / "proof/replay_cycle_37_degree_two_independent.py", "6bf5cff40e6a8340a77b632b4c7b632f461eef64703d03e592d51f1a1600ccc6"),
    "audit": (ROOT / "proof/check_cycle_37_degree_two.py", "12947c430aee608ed853e9a8bf3fb8a0a24412a95b46a58096657ec5e1dc95a4"),
    "soundness": (ROOT / "proof/cycle_37_degree_two_soundness.md", "181a147d92d7d29c6c22da39072ffaef1927544e96d7c4b423c2cd156d9f862d"),
    "test": (ROOT / "tests/test_cycle_37_degree_two.py", "769047be2d23107d7284ad64bea4a6bc9efc499eba45dd7936984cc7650d032c"),
    "primary_result": (OUT / "result.json", "6d4f4ddb592be0f4cb1739b7b2ef0aab992b3b27defb7acf7fd4726f1d10558c"),
    "independent_result": (OUT / "independent-replay.json", "238da2b03bec099b3908d029bc30b4757fa93714fa3e4cc64e22d427b1a1710d"),
    "primary_timing": (ROOT / "discovery/out/cycle37-degree-two-product.time", "0fd958934b12519eed48ac6c455e3a8837bd256018a14237266cf958eda0fce4"),
    "independent_timing": (OUT / "independent-replay.time", "2276eb43cefee5e14abc7e34e13998fa64cc4a09a4878f220996bb621fbeeeb2"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-37-b037-lrc-degree-two-product-v1",
        "budget_ordinal": "B037",
        "cycle": 37,
        "record_type": "PROVED_DEGREE_TWO_PRODUCT_FUNCTIONAL",
        "recorded_at_utc": "2026-08-04T16:00:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A mass-one rank-one integer signed functional annihilates all 1,394 direct predicates, 221,646 degree-one one-hot multiples, and 16,170,400 distinct-coordinate degree-two multiples for p199 base 4 / leaf 78. Hence no degree-at-most-two identity exists in that direct-predicate calculus.",
        "claim_boundary": "This excludes only the frozen degree-at-most-two direct-predicate/one-hot calculus for one leaf. It does not classify nonproduct duals, ownership semantics, higher degree, the leaf, or LRC(13), and does not authorize an automatic higher-degree sequence.",
        "audit": checked,
        "breakthrough": {"epistemic_status": "PROVED", "local_normals_by_allowed_option_offset": EXPECTED_NORMALS, "local_masses": [1] * 13, "global_mass": 1, "degree_zero_generators": 1394, "degree_one_generators": 221646, "degree_two_generators": 16170400, "nonzero_generator_contractions": 0, "predicates_with_strong_kill": 1056, "maximum_absolute_local_coefficient": 5, "independent_full_raw_replay": "PASS"},
        "compression_theorem": {"epistemic_status": "PROVED", "statement": "All one-hot multiples of F_t supported on at most two coordinates vanish under a product functional iff t has at least three ordinary zero contractions or at least one strong pointwise zero coordinate.", "raw_degree_two_constraints": 16170400, "compressed_predicate_conditions": 1394},
        "prior_boundary": {"cycle36_escaping_predicates": 54, "cycle36_nonzero_degree_two_labels": 2010},
        "cycle_decision": {"companion_identity": "/root/darwin_cycle25_short", "outcome": "SEALED_FOR_OWNERSHIP_EXTENSION_QUESTION", "scope_review": "Full independent raw replay verifies the degree-two hierarchy. Continuing degree by degree would accumulate method no-gos without introducing leaf-closing semantics.", "strongest_flaw": "A product functional can exist even when a nonproduct ownership-aware proof or dual behaves differently; this result is not evidence against ownership calculus.", "independent_ideas": ["extend the functional to the exact rank-at-most-three ownership-blocker ideal", "defer CRT transfer because it spreads a method no-go", "use the first failing blocker constraint to select a nonproduct ownership engine"], "falsifier": "Any nonzero independently rebuilt degree-two contraction or one-hot/compression mismatch invalidates the result.", "next_action": "Open Cycle 38 to test exact label-preserving extension of the C37 functional to Cycle 29's ownership-blocker interface; do not open degree three automatically."},
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 484.20, "largest_peak_rss_kib": 180280, "worker_address_space_cap_bytes": 1258291200, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 37 degree-two product functional"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_degree_two_predicate_compressed.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_37_degree_two_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_37_degree_two.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_37_degree_two -v", "check_command": ".venv/bin/python proof/build_cycle_37_lrc_degree_two.py --check"},
        "sealer": {"path": "proof/build_cycle_37_lrc_degree_two.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
