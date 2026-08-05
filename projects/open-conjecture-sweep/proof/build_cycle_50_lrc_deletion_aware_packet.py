#!/usr/bin/env python3
"""Seal Cycle 50's deletion-aware triple-packet theorem falsifier."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_50_deletion_aware_packet import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle50-deletion-aware-packet"
OUTPUT = ROOT / "artifacts/cycle-50-b050-lrc-deletion-aware-packet-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-50-b050-lrc-deletion-aware-packet-preregistration-v1.md", "55339ee28fc9ff70cd8017612460fdda20d27a8d9d13509ddd10aca90baaafbb"),
    "cycle49_artifact": (ROOT / "artifacts/cycle-49-b049-lrc-relative-diagonal-contraction-v1.json", "c71f6cafaf9724be1458e9fc14af6d4ec69cc2d24b5c355b98006788dd76c76a"),
    "idea_selection": (ROOT / "discovery/cycle50_deletion_aware_packet_idea_selection.md", "72c0cb9ef4400ce9900cbc66bd07bd834699d84e2b6c06ed4ef11ad0917b51cb"),
    "packet_module": (ROOT / "discovery/lrc_deletion_aware_packet.py", "faeb7a9151cab607e044f854851729b980cb2b627ee136df1111574a9d34f20c"),
    "controls_engine": (ROOT / "discovery/lrc_deletion_aware_packet_controls.py", "d1707f3a1a1d30477b65ccf080d54060ebdbd2795006fae0c868d8a3d5c11e7b"),
    "principal_engine": (ROOT / "discovery/lrc_deletion_aware_packet_full.py", "ac08d6ab85fdcd73f5c84a1417e45e5d664163447cc39bf4cdd569c1987a0c34"),
    "controls": (OUT / "controls.json", "8edee0e531e6876c586eb13e1851548d4dbd35c4e626a57ab277eccc289df339"),
    "principal_result": (OUT / "full-pattern-census.json", "98cab0bc9e292d3af3de81221664818256a13aeb9b7b76855da2949941cc4f76"),
    "independent_engine": (ROOT / "proof/replay_cycle_50_deletion_aware_independent.py", "866ec4123662b0ec902d144e316eea9de0996f551a75c79c9335a50f4216d849"),
    "independent_result": (OUT / "independent-replay.json", "075a1ecd890a4279f5bca43990b4cc727a908c59ef906fa5aa94d3479a3e80b2"),
    "audit": (ROOT / "proof/check_cycle_50_deletion_aware_packet.py", "8d70bc79b9c6e042b474e5db21f1297e8274bcbedb985c9f0a4b6fd36a945d2b"),
    "soundness": (ROOT / "proof/cycle_50_deletion_aware_packet_soundness.md", "0dc761be15df261357c900f6be057cfa58e539a389e7e0910366e41803d0100d"),
    "test": (ROOT / "tests/test_cycle_50_deletion_aware_packet.py", "88ffb9cd3631b99414823b7c7d413701b23da3c5ab43a2bd451bf181fc153a05"),
    "principal_timing": (OUT / "run-full-pattern-census.time", "d839fc6140f8afc7b864e773bf5cef2465536b44bedf5518187ba975072a0d36"),
    "independent_timing": (OUT / "run-independent.time", "17505bc0beb17698b4b51192f22f8662cb1e4e100ff0e9651bb970f9ff309323"),
    "c49_relative_module": (ROOT / "discovery/lrc_relative_diagonal.py", "3d73fad7547a0a1448fc67898607b8588c0aa06babf2cfa6ffb7f0079d43175f"),
    "c49_full_audit": (ROOT / "discovery/lrc_relative_diagonal_full_audit.py", "341cef8a1397f2371d6ad2a5d300a230ac93d820b84682affa3104e6901a77f9"),
    "c49_inventory": (ROOT / "discovery/lrc_relative_diagonal_inventory.py", "74bf5a5c73e4919bd08b8b97d7c195a02887fca4a91444449a9399b88b607568"),
    "cube_rewrite": (ROOT / "discovery/lrc_cube_rewrite.py", "106a237501b9bf115e8df265c2075f0605c6a7776c1bd8fdd870adc1b01e4de9"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    controls = json.loads((OUT / "controls.json").read_text())
    return {
        "artifact_id": "cycle-50-b050-lrc-deletion-aware-packet-v1", "budget_ordinal": "B050", "cycle": 50,
        "record_type": "PROVED_DELETION_AWARE_TRIPLE_PACKET_THEOREM_FAIL", "recorded_at_utc": "2026-08-05T08:00:00Z",
        "status": "SEALED", "epistemic_status": "PROVED",
        "outcome": "The sole preregistered deletion-aware triple-packet theorem is false. Its uniform actual-mask rule contracts 29,048 of 29,050 complete selected p199 interfaces, including three of the five C49 residuals, but leaves exactly (4,5,35) and (4,6,35) BUFFER_INCOMPLETE at the unchanged 01 pair-fiber stage. Principal and independent reverse-order reconstructions agree exactly.",
        "claim_boundary": "This is a scoped falsifier of the triple-only actual-mask relaxation plus the inherited C49 pair stage. It is not a terminal relative-homology obstruction, does not exclude a new pair-fiber theorem, and does not prove LRC(13). C50's stop rule prohibits adding that new local family here.",
        "controls": controls,
        "audit": checked,
        "cycle_decision": {
            "outcome": "PAUSE_PROBLEM_1_AND_HANDOFF",
            "reason": "C50 reached its preregistered theorem falsifier. The remaining two rows require a distinct pair-fiber method family, which the C50 stop rule expressly forbids adding.",
            "handoff_point": "C49/C50 establish a sharp local boundary: triple deletion-aware packets cure all (2,2,2) residuals but do not cure the two (2,2,4) pair-fiber failures.",
            "not_authorized": ["another local exception rule", "per-face Gaussian elimination", "an enlarged local fill census", "Cycle 51 on pair packets without a new project decision"],
        },
        "resources": {**checked["resources"], "worker_cpus": [0, 1, 2], "reserved_cpu": 3},
        "runtime": check_runtime("Cycle 50 deletion-aware packet"), "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "controls_command": ".venv/bin/python discovery/lrc_deletion_aware_packet_controls.py",
            "principal_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_deletion_aware_packet_full.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_50_deletion_aware_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_50_deletion_aware_packet.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_50_deletion_aware_packet -v",
            "check_command": ".venv/bin/python proof/build_cycle_50_lrc_deletion_aware_packet.py --check",
        },
        "sealer": {"path": "proof/build_cycle_50_lrc_deletion_aware_packet.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
