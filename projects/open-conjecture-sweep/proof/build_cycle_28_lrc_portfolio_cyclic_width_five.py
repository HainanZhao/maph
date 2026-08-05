"""Seal Cycle 28's incomplete-audit portfolio containment boundary."""
from __future__ import annotations

from pathlib import Path

from check_cycle_28_portfolio_cyclic_width_five import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"
OUTPUT = ROOT / "artifacts/cycle-28-b028-lrc-portfolio-cyclic-width-five-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-28-b028-lrc-portfolio-cyclic-width-five-preregistration-v1.md", "e537412eddfebf7115d59bafda8ff00e6e45d42eed7a9e4af58dfb8afd5f9610"),
    "source_artifact_c21": (ROOT / "artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json", "360daaf46d9f4442a65cce29d8011d05ea529ad0e59a7f16dc6c12b6b66a0200"),
    "source_artifact_c22": (ROOT / "artifacts/cycle-22-b022-lrc-width-four-v1.json", "512ecc6f854e2400b6ee733fd2d91f8860de50a522820703d44290ad53aab58d"),
    "target_artifact": (ROOT / "artifacts/cycle-25-b025-lrc-quadratic-crt-v1.json", "61fa41306155dbc55e6853434f2c0d567a6a6a2409c6847934dda902ebf80c68"),
    "prior_artifact": (ROOT / "artifacts/cycle-27-b027-lrc-width-five-lp-v2.json", "aa93f44575a8c26d3f20e35d660f9e7f5b71173cf1a0a4f5a91a425132d6ce08"),
    "idea_selection": (ROOT / "discovery/cycle28_width_five_partition_idea_selection.md", "59e83b53af2c6eb430112d6d55fb549a8310a1ccc59c98f447cafc48d4b5c431"),
    "source_results_c21": (ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv", "122c1977f4c3314f311ada8d36e7f3816ae6d1e80b9320d1b322a7cac4809832"),
    "source_results_c22": (ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv", "a89a0532292f188cedc0f5b41a04cb68e2ebcae09ed9514ffba6f0f0941b0c07"),
    "targets": (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv", "aa78578f2e54e7045d6dcf63e1278805d04057e48cd2b3981a4853889074e3d3"),
    "coupled": (ROOT / "discovery/lrc_coupled_incidence.py", "b40d9ff5077b40caaeda0e1622d456ce9e9673c9451bc6cd19d2b58286853469"),
    "direct": (ROOT / "discovery/lrc_pair_choice.py", "f3faa9c3152467243ec1acfe27310c857cadbbe40b565c7cf51fb6e47318d55a"),
    "width_four": (ROOT / "discovery/lrc_width_four_stage_a.py", "3faee2712066bb15014b87b47f58a7be914298965dbf32678ee36485e9a0a9b9"),
    "search": (ROOT / "discovery/lrc_portfolio_cyclic_width_five.py", "9323e6a583d6118c8c8bd861223393d7a81dcb5ebd43ca720011b123ca5d0e43"),
    "independent_replay": (ROOT / "proof/replay_cycle_28_portfolio_independent.py", "247007be3bac9a0069c1f451b2acd5d57753aa0d19282a9052c7c10a688a10de"),
    "mismatch_diagnostic": (ROOT / "proof/diagnose_cycle_28_lp_mismatch.py", "3780fa0ccc8a0e01445980830ecc40186fbfa0b0aaa56525d5002a3035e7161b"),
    "thread_classifier": (ROOT / "proof/classify_cycle_28_thread_trace.py", "2382fbee2dd5d63de45cb7f07288254d4850591f514a70c5e5ba2e9532b3ebfd"),
    "audit": (ROOT / "proof/check_cycle_28_portfolio_cyclic_width_five.py", "c9c60df717d43e4997006c2350bd792eb61a14268013eaecde83eff0d23e6b0d"),
    "test": (ROOT / "tests/test_cycle_28_portfolio_cyclic_width_five.py", "78a76d21da40247e3142e2b10950b14c209376920314590476f441324ae6797b"),
    "soundness": (ROOT / "proof/cycle_28_portfolio_cyclic_width_five_soundness.md", "1e49b9a68c8905b519bbf08c7681ce016050b2695dc3fdb41b6f2c8ae80762c2"),
    "control": (OUT / "control.json", "ae18a5b5dba4982e10781b152896cda64bbc84fc98a436791eddb969d922752b"),
    "selection_tranche1": (OUT / "selection-tranche1.tsv", "9e40cdf9e97e34a99762353e8b835fdadb93a1711070aba52bbc1b4ab252817e"),
    "results_tranche1": (OUT / "results-tranche1.tsv", "b3e7271e5f152543c636bf32ff4d60752e808368f2344ca3a9f26ea8fbb97725"),
    "summary_tranche1": (OUT / "result-tranche1.txt", "4ecbe8487cb1327627cd03b9f26e503dfe64a947b6dc6ee1078d39a5e005b5d5"),
    "timing_tranche1": (OUT / "run-tranche1.time", "7d37dcbde29cae721c3ba3058d4e0bbb05541398d013452a4ff1a01b8f72eb69"),
    "selection": (OUT / "selection.tsv", "9e40cdf9e97e34a99762353e8b835fdadb93a1711070aba52bbc1b4ab252817e"),
    "results": (OUT / "results.tsv", "a21f61a0e962a4822a3ba46ea6dc773ff92692ed3873350667bd2b2bfebf8d48"),
    "summary": (OUT / "result.txt", "e81c5ccdeb7f163f75588593bfeb0c709b5ef53680b763a28959d5da87631e3c"),
    "timing_tranche2": (OUT / "run-tranche2.time", "7192f7576693376a6b8fd624383d59c7a0758f45a3b31ebfec2d0fc460e39469"),
    "inconclusive_audit_timing": (OUT / "independent-replay.time", "3a499e9aa79c598285ed4aeafa59dcf05248a61d4712104606fa79c75c88f783"),
    "failed_audit": (OUT / "independent-replay-error-tranche2.json", "4ee313bfce9225556ed75ffaa6c3e3184d000d1de27b8bcd873a2d1154478dee"),
    "failed_audit_timing": (OUT / "independent-replay-tranche2.time", "9a43830c4b540aacf5a2d70cd3daa42e1e2cd088c4be10ffc8c1517b5ca93ca0"),
    "diagnostic_rows": (OUT / "independent-lp-diagnostic.tsv", "8a841e3d4eb5e781741589de5604b0024712d6e2cda2bae88587c671236c63e1"),
    "diagnostic_result": (OUT / "independent-lp-diagnostic.json", "f8dc77b8d5e96effddfd5abb513c80cd5f9d0c1c94a705ae0de83e247b1434d0"),
    "diagnostic_timing": (OUT / "independent-lp-diagnostic.time", "bb7aa5e9479e9c30bda28c0818cf440f1707f27b2e83d4af56a8fe9645eee3c4"),
    "thread_control": (OUT / "thread-trace-control.json", "3d7a8ed907e1f4a283bfed1e61e317c82fdabfe79393619a72d108d57409dcce"),
    "thread_control_timing": (OUT / "thread-trace-control.time", "732f8a143cf5e21565e62e9eaad56afdf32d95628529eba55bd5ee24ae274951"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-28-b028-lrc-portfolio-cyclic-width-five-v1",
        "budget_ordinal": "B028",
        "cycle": 28,
        "record_type": "OBSERVED_INCOMPLETE_AUDIT_CONTAINMENT",
        "recorded_at_utc": "2026-08-04T13:30:16Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": "The four-witness selector chose nonbaseline cyclic width-five geometries for all 60 frozen survivors and the primary floating LP promoted none; independent closure failed on a thread-sensitive separator trace, leaving 24 LP traces unconfirmed.",
        "claim_boundary": "This record preserves a primary 60-row OBSERVED all-unresolved census, four exact source controls, 35 exact independent LP-trace matches, one classified trace mismatch, and 24 unconfirmed traces. It is not a 60/60 independent audit, an exact LP lower bound, a closure of the cyclic family, a width-five no-go, or an LRC result.",
        "audit": checked,
        "proved_interface": {
            "epistemic_status": "PROVED",
            "statement": "Complete integer direct-option replays recover the four frozen source identities: (65528,65440), (4091,4090), (65539,65448), and (4107,4080).",
        },
        "primary_outcome": {
            "epistemic_status": "OBSERVED",
            "targets": 60,
            "nonbaseline_selections": 60,
            "rotation_counts": {"2": 6, "3": 20, "4": 17, "5": 17},
            "unresolved": 60,
            "certified_leaves": [],
            "rounds_range": [20, 117],
            "cuts_range": [58, 236],
            "objective_statement": "Floating values range from 0.9999999999999979 to 1.0000000000000018; none is promoted as an exact lower bound.",
        },
        "audit_containment": {
            "epistemic_status": "OBSERVED",
            "coarse_full_audit": "FAIL: LP mismatch after source and selector phases",
            "exact_trace_matches": 35,
            "first_mismatch": {"base_index": 3, "leaf_ordinal": 91, "primary": {"objective": 1.0, "rounds": 28, "cuts": 80}, "unpinned_independent": {"objective": 1.0, "rounds": 26, "cuts": 74}},
            "thread_control": "With OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1, the independent implementation reproduces the primary (1,28,80) trace.",
            "unconfirmed_lp_traces": 24,
            "implication": "The numerical path is thread-environment-sensitive; the failed audit remains and strong finite-family closure is withheld.",
        },
        "companion_decision": {
            "identity": "/root/darwin_cycle25_short",
            "scope_review": "Seal only an OBSERVED incomplete-audit containment record; do not claim a validated finite-method closure.",
            "recommendation": "Open a distinct semantic primal lift with an exact bidirectional equivalence control before any survivor search.",
            "strongest_flaw": "The semantic lift may merely re-encode the earlier typed mapping family.",
            "falsifier": "Any frozen small control where either direction fails to preserve coordinate labels, feasibility, and exclusion status halts the semantic branch.",
            "independent_ideas": ["semantic primal lift with exact bidirectional equivalence", "rational reconstruction of one representative primal lower-bound certificate", "non-class-constant individual/cyclotomic characters after an exact direct-CNF interpretation"],
            "final_action": "Contain C28 with its audit defect and change engines in C29.",
        },
        "resources": {
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
            "aggregate_wall_seconds": 19506,
            "aggregate_wall_cap_seconds": 20000,
            "largest_observed_process_peak_rss_kib": 1168436,
            "isolated_diagnostic_memory_max_bytes": 6442450944,
            "temporary_disk_cap_bytes": 21474836480,
        },
        "runtime": check_runtime("Cycle 28 portfolio cyclic width-five containment"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_portfolio_cyclic_width_five.py",
            "failed_independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_28_portfolio_independent.py",
            "diagnostic_command": "taskset -c 0-2 .venv/bin/python proof/diagnose_cycle_28_lp_mismatch.py",
            "thread_control_command": "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 taskset -c 0 .venv/bin/python proof/classify_cycle_28_thread_trace.py",
            "audit_command": "taskset -c 0 .venv/bin/python proof/check_cycle_28_portfolio_cyclic_width_five.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_28_portfolio_cyclic_width_five -v",
            "check_command": ".venv/bin/python proof/build_cycle_28_lrc_portfolio_cyclic_width_five.py --check",
        },
        "sealer": {"path": "proof/build_cycle_28_lrc_portfolio_cyclic_width_five.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
