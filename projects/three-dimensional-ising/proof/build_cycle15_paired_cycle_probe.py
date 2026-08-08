#!/usr/bin/env python3
"""Seal the timeboxed width-four paired-cycle extension probe."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_width4_l_attachment import search  # noqa: E402
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/cycle-15-b15-paired-cycle-probe-v1.json"
HASHES = {
    "preregistration": ("discovery/cycle-15-paired-cycle-probe-preregistration.md", "39efe8ee25bc149a1433c075ded56fd4505d8d5a7478452b9b2df0fb6ba48dfd"),
    "outcome": ("discovery/cycle-15-paired-cycle-probe-outcome.md", "2b543b435a77692080182434277b89610f3f81753bcb74b50b94b140e0379bb3"),
    "search": ("discovery/search_g1_width4_l_attachment.py", "079ea422fc2572d56c426cd8c2419d7ee7aa79dd55eb35ade0428e25e5dbdbce"),
    "live_result": ("discovery/cycle-15-paired-cycle-probe-live.json", "7264c37e134dd34c4864afb69af37ab9e8d1c0892f0318d0e54d88ebae1b69ca"),
    "paired_cycle_dependency": ("proof/verify_g1_paired_cycle_w3.py", "5ceee917c21e24670a09b5bfb03176f87b814ecf55b470eb05b838e8bb06156b"),
    "matroid_dependency": ("discovery/search_g1_paired_fundamental_cycles.py", "9d7445cdbe81844b800de8cb0104b77f27db3f597a13946c6dee0fcebc4f9ecb"),
    "induction_dependency": ("discovery/search_g1_width_induction.py", "47ab173108ec450e67f45f07d4e553372ae72a2d95700220bc15cd2fa24d74a3"),
    "frontier_dependency": ("proof/verify_lane_b_arbitrary_width_frontier.py", "f98f80b203eb93bd0c18deb37e80dbf7cdcbb58237129cba60c42cff3fa73615"),
    "conventions": ("src/conventions.py", "b6b328f6b7b1725c39f4e4ba4084c275a141189b7efe32e9727c75488d705bb3"),
    "failure_ledger": ("discovery/failure-ledger-cycle15.md", "4d3a2561538eaa63f28dce913e94220d77708f95734ddeb738a984dfa5d35990"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    frozen = freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()})
    result = search(50000, 20260808)
    live = json.loads((ROOT / "discovery/cycle-15-paired-cycle-probe-live.json").read_text())
    if json.loads(json.dumps(result, sort_keys=True)) != live:
        raise RuntimeError("paired-cycle search is not deterministic")
    if result["best"]["total_common_rank"] != 12 or result["best"]["additional_rank"] != 4:
        raise RuntimeError("timeboxed paired-cycle outcome changed")
    return {
        "artifact_id": "cycle-15-b15-paired-cycle-probe-v1",
        "author": "Hainan Zhao",
        "budget_ordinal": "B15",
        "cycle": 15,
        "status": "SEALED",
        "epistemic_status": "OBSERVED_EXACT_GF2_TIMEBOX",
        "record_type": "PAIRED_CYCLE_GENERALIZATION_PROBE",
        "outcome": "No rank-15 witness was found in the preregistered structured L-boundary family; best rank was 12.",
        "gate_outcome": "T5_TERMINAL_NEGATIVE_DROP_PROBE",
        "claim_boundary": result["claim_boundary"],
        "exact_replay": result,
        "frozen_hashes": frozen,
        "runtime": check_runtime("cycle-15-paired-cycle-probe"),
        "sealer": {"path": "proof/build_cycle15_paired_cycle_probe.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "search": "python3 discovery/search_g1_width4_l_attachment.py --trials 50000 --seed 20260808",
            "artifact_check": "python3 proof/build_cycle15_paired_cycle_probe.py --check"
        }
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
