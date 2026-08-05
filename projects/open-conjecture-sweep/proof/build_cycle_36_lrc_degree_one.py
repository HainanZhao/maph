"""Seal Cycle 36's exact degree-one signed product functional."""
from __future__ import annotations

from pathlib import Path

from check_cycle_36_degree_one import EXPECTED_NORMALS, audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation"
OUTPUT = ROOT / "artifacts/cycle-36-b036-lrc-degree-one-pseudoexpectation-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-36-b036-lrc-degree-one-pseudoexpectation-preregistration-v1.md", "5eef8c5819edc74df07349c91e8afacccedbbd34e8b555a25b04bdf6796ff03e"),
    "prior_artifact": (ROOT / "artifacts/cycle-35-b035-lrc-local-product-measure-v1.json", "5713db8b78597ab36f547836fbf06e5cb24b7aca5677a871beb1068510b17fbd"),
    "idea_selection": (ROOT / "discovery/cycle36_degree_one_pseudoexpectation_idea_selection.md", "42acb42aaea2d690d8e0c7698e368e300898c9bc74dd3f97179d6c3bcaf9670e"),
    "first_engine": (ROOT / "discovery/lrc_degree_one_pseudoexpectation.py", "eeaa8fb737233cb87791261e17797721fe9f2859426db14b0b8d0de0cc332a6f"),
    "compressed_engine": (ROOT / "discovery/lrc_degree_one_predicate_compressed.py", "cf8fb138db806421047884951546a7653630bb9265593bbc9b22739a075e6cf2"),
    "independent_replay": (ROOT / "proof/replay_cycle_36_degree_one_independent.py", "b002dc1815f14924b8e1b269c16f5bb5d3123d53c16d93753c90450c2d56f7d1"),
    "audit": (ROOT / "proof/check_cycle_36_degree_one.py", "2e731805adc02064c16cffe58123d8538c9954602d0d59ec2c0dd299ed4cdccd"),
    "soundness": (ROOT / "proof/cycle_36_degree_one_soundness.md", "b346869af5db21f9b04bb0fdfbeb5d0d5e1304fdcf567344e93d2d17f060ae17"),
    "test": (ROOT / "tests/test_cycle_36_degree_one.py", "67e9838a491cc067f3b226e9a54daeedbac3f570b3d1c6fb8469ee4a0167bb74"),
    "first_result": (OUT / "first-tranche.json", "80aba8d91a6612a2cacf14a3292d34aac3f37ced77c8caae8182a16c20dd96be"),
    "primary_result": (OUT / "result.json", "1a780396b8354c6814647bfc79853522590ba265ee67c4a5c78365e172058999"),
    "independent_result": (OUT / "independent-replay.json", "cdb2b133576e1c31dc8c642b428b6bd51fe176df13770863ac89c92d7116a423"),
    "first_timing": (ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation.time", "fc2ef2744bdc9723dfa4a0873bb0c370a5bc84a5011c7a095eb562844f1ab412"),
    "second_timing": (ROOT / "discovery/out/cycle36-degree-one-pseudoexpectation-second-tranche.time", "c74b98f7613a8eb3aa6ad4a6606ce34802a22e362d21affced12c0edeeba1ba3"),
    "independent_timing": (OUT / "independent-replay.time", "6aecdec96cea9e05ca18015fb55b1a74ca8eabfbc4694182fd1c68cb9d63910e"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-36-b036-lrc-degree-one-pseudoexpectation-v1",
        "budget_ordinal": "B036",
        "cycle": 36,
        "record_type": "PROVED_DEGREE_ONE_PRODUCT_FUNCTIONAL",
        "recorded_at_utc": "2026-08-04T15:45:14Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "A mass-one rank-one integer signed functional annihilates all 1,394 direct uncovered predicates and all 221,646 one-hot coordinate-indicator multiples for p199 base 4 / leaf 78. Therefore no degree-at-most-one rational identity exists in that frozen direct-predicate calculus.",
        "claim_boundary": "This excludes degree-at-most-one identities only in the direct-predicate/one-hot calculus for one p199 leaf. The functional is signed, not positive, and the result does not classify nonproduct duals, degree two, ownership auxiliaries, the leaf itself, or LRC(13).",
        "audit": checked,
        "breakthrough": {
            "epistemic_status": "PROVED",
            "local_normals_by_allowed_option_offset": EXPECTED_NORMALS,
            "local_masses": [1] * 13,
            "global_mass": 1,
            "degree_zero_generators": 1394,
            "raw_degree_one_generators": 221646,
            "automatic_degree_one_generators": 31768,
            "nonzero_generator_contractions": 0,
            "predicates_with_strong_kill": 1112,
            "maximum_absolute_local_coefficient": 6,
            "independent_direct_set_replay": "PASS",
        },
        "compression_theorem": {
            "epistemic_status": "PROVED",
            "statement": "For a product functional, all degree-zero and one-hot degree-one multiples of F_t vanish iff F_t has at least two ordinary zero local contractions or has a strong zero coordinate satisfying u_i(a)b_ti(a)=0 for every option.",
            "raw_constraints": 221646,
            "compressed_predicate_conditions": 1394,
        },
        "contained_path": {
            "epistemic_status": "OBSERVED",
            "engine": "raw deduplicated local-disjunction signatures",
            "outcome": "interrupted at memory cap after 397.43 seconds, peak RSS 4,378,756 KiB, no terminal result",
            "optimized_engine": "ordinary-or-strong predicate compression",
            "optimized_states": 224,
            "optimized_wall_seconds": 83.76,
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_SINGLE_DEGREE_TWO_PRODUCT_TEST",
            "scope_review": "Independent raw-label replay confirms the compression and all contractions. The product functional is a degree-one calculus no-go, not a leaf certificate or a positive pseudoexpectation.",
            "strongest_flaw_resolved": "The first representation exceeded memory; the later predicate theorem is exactly equivalent and independently checked against every raw multiplier.",
            "independent_ideas": ["test one bounded degree-two product-functional lift", "defer cross-leaf transfer without a CRT transport theorem", "use any degree-two escape-pair profile to select ownership semantics"],
            "falsifier": "Any raw multiplier disagreeing with the ordinary-or-strong rule, or any nonzero independently rebuilt contraction, invalidates the degree-one claim.",
            "next_action": "Open Cycle 37 for one bounded exact degree-two product-functional test using coordinate-pair multipliers; do not automatically continue a degree ladder afterward.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 481.40, "largest_peak_rss_kib": 4378756, "memory_boundary_mib": 4096, "compressed_worker_address_space_cap_bytes": 1258291200, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 36 degree-one product functional"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "contained_first_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_degree_one_pseudoexpectation.py",
            "compressed_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_degree_one_predicate_compressed.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_36_degree_one_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_36_degree_one.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_36_degree_one -v",
            "check_command": ".venv/bin/python proof/build_cycle_36_lrc_degree_one.py --check",
        },
        "sealer": {"path": "proof/build_cycle_36_lrc_degree_one.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
