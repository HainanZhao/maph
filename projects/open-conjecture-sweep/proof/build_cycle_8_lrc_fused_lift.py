"""Seal Cycle 8's fused first-lift controls and capped p199 CSP sample."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import subprocess

from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-8-b008-lrc-fused-lift-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-8-b008-lrc-fused-lift-preregistration-v1.md", "19eae02e556b981a162b72ab2153356b8ae5da7b3e03c90b362b3cc6f4cf9f54"),
    "fused_soundness": (ROOT / "proof/cycle_8_fused_lift_soundness.md", "e433fa1b8091998093c7c0b8e4d0e4fb9fda47618fc2c16696bceb5e3f762f40"),
    "multichoice_soundness": (ROOT / "proof/cycle_8_p199_multichoice_soundness.md", "29e67a50c34661203d91f09d048dba3353283d1f2c098d03b1283e8b5590dd95"),
    "fused_engine": (ROOT / "discovery/lrc_fused_first_lift.cpp", "4acf461a2716ec3a91a42491c99ccaaa8acc872b06ef703d071d90b0e3a74052"),
    "independent_control": (ROOT / "proof/check_cycle_8_fused_lift.py", "705f706e175a30f13dcf67db0b6b9ce79093c188c1425893b55b5b370a7f75c7"),
    "fused_result": (ROOT / "discovery/out/cycle8-fused.result", "a680d74cfdf174a624f40b2b01104c4ca92dead167253350800d7659e61d732f"),
    "independent_result": (ROOT / "discovery/out/cycle8-independent.result", "593c165c64f4960167ef85b81bc99aac7d13648c31ecee117758dcf6313718c5"),
    "p47_retained": (ROOT / "discovery/out/cycle8-p47-retained.txt", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "strata_builder": (ROOT / "discovery/make_cycle_8_p199_strata.py", "d3d9a34134b277bc8d2d317b3864618fcdacc3bdcdbba413eeb3d7842842956b"),
    "p199_census": (ROOT / "discovery/out/k13-p199.txt", "667c5582ec1719d9d85fdc33a95d812234bfe7480c050a442cb566d1505a935c"),
    "p199_strata": (ROOT / "discovery/out/cycle8-p199-strata.txt", "327334cf85b821a77b254420d0617c8771a9f272cf38b2512ab79c937de4299b"),
    "multichoice_engine": (ROOT / "discovery/lrc_p199_multichoice_lift.cpp", "3478bc9b0723292f4b380dcf887935206219b3100d56eb1e9c6a0a34784facf8"),
    "multichoice_v1": (ROOT / "discovery/out/cycle8-p199-multichoice-v1.txt", "f2bcf4455cfd9c552e8be3ab5a26989f506b0343fe1b837a18b760a9d3ce904d"),
    "multichoice_v2": (ROOT / "discovery/out/cycle8-p199-multichoice.txt", "c606cae296659cb70a1eeba83a61c3edd89223f490372336400fe59613652e35"),
    "multichoice_v1_time": (ROOT / "discovery/out/cycle8-p199-multichoice-v1.time", "0dfdfd91fbc9d3fc34fcb4f5952e9e8599646d9e6515432af41fb76e75627a4d"),
    "multichoice_v2_time": (ROOT / "discovery/out/cycle8-p199-multichoice.time", "064d38aa5dab9b93ea93ebc9d3dd336ec428ec663e701c9d7ab8a06a97323acd"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_8_lrc_fused_lift.py", "58b01551f2af12b97db2bd8ffbfc4c4d74cfe2c3d0a67021d606d7f77ad8db5b"),
}


def metrics(path: str) -> Counter[str]:
    return Counter(line.split()[1] for line in (ROOT / path).read_text().splitlines() if line.strip())


def max_nodes(path: str) -> int:
    return max(int(line.split()[2]) for line in (ROOT / path).read_text().splitlines() if line.strip())


def elapsed_seconds(path: str) -> float:
    match = re.search(r"Elapsed \(wall clock\).*?: (\d+):(\d+\.\d+)", (ROOT / path).read_text())
    if not match:
        raise RuntimeError(f"missing elapsed time in {path}")
    return int(match.group(1)) * 60 + float(match.group(2))


def payload() -> dict:
    runtime = check_runtime("Cycle 8 fused lift")
    frozen = freeze_inputs(ROOT, INPUTS)
    first = metrics("discovery/out/cycle8-p199-multichoice-v1.txt")
    strengthened = metrics("discovery/out/cycle8-p199-multichoice.txt")
    if first != Counter({"CAP": 100}) or strengthened != Counter({"CAP": 100}):
        raise RuntimeError("unexpected p199 sample classifications")
    if max_nodes("discovery/out/cycle8-p199-multichoice-v1.txt") != 1_000_001:
        raise RuntimeError("unexpected v1 cap counter")
    if max_nodes("discovery/out/cycle8-p199-multichoice.txt") != 1_000_001:
        raise RuntimeError("unexpected v2 cap counter")
    return {
        "artifact_id": "cycle-8-b008-lrc-fused-lift-v1",
        "budget_ordinal": "B008",
        "cycle": 8,
        "record_type": "CONTROL_AND_PERFORMANCE_GATE",
        "recorded_at_utc": "2026-08-03T16:55:00Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": "The exact parent-intersected first-lift interface passed complete raw H11 and full p47 controls. On the fixed 100 completed p199 orbits, both capped multi-choice CSP formulations produced only CAP; no p199 orbit was classified SAT or UNSAT.",
        "claim_boundary": "The proved finite control statements are F_1(3,11,4)=empty and F_1(6,47,7)=empty, hence J(6,47)=empty by exactly checked Proposition 3.1. The p199 result is host/method-specific performance evidence only: it gives no survivor count and proves nothing about F_1(13,199,14), J(13,199), or LRC(13).",
        "proved_controls": {
            "epistemic_status": "PROVED",
            "h11_raw_lift_tuples": 64_000,
            "h11_f1_survivors": 0,
            "p47_base_orbits": 53,
            "p47_f1_survivors": 0,
            "p47_consequence": "J(6,47)=empty under Proposition 3.1 with the certified l=1 parent enumeration",
            "independent_direct_recheck": "PASS h11_retained=0 p47_retained=0 p47_eliminated=53",
        },
        "p199_performance": {
            "epistemic_status": "OBSERVED",
            "sample_orbits": 100,
            "strata": "10 lexicographic index strata x 10 completed Cycle-1 representatives",
            "v1": {"status_counts": dict(first), "node_counter_total": 100_000_100, "node_counter_per_row": 1_000_001, "wall_seconds": elapsed_seconds("discovery/out/cycle8-p199-multichoice-v1.time")},
            "v2": {"status_counts": dict(strengthened), "node_counter_total": 100_000_100, "node_counter_per_row": 1_000_001, "wall_seconds": elapsed_seconds("discovery/out/cycle8-p199-multichoice.time")},
            "cap_interpretation": "Each reported 1,000,001 is a 1,000,000 explored-node cap plus its deterministic sentinel check. CAP retained the orbit; it is neither SAT nor UNSAT.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "recommendation": "Seal Cycle 8; open distinct Cycle 9 for an exact weighted-time dual certificate, with CDCL only as independent validation if the dual produces candidates.",
            "independent_ideas": ["saturate P1", "CRT factorization", "pinned CDCL backend", "exact rational weighted-time dual"],
            "flaw": "The all-CAP p199 sample is non-discriminating and cannot distinguish structural difficulty from weak branch ordering/bounds.",
            "falsifier": "Any raw/fused H11 mismatch, p47 fiber missed by independent direct checking, or retained-path/orbit counterexample invalidates the control proof; for p199 a cap is not a falsifier.",
            "next_action": "New Cycle 9: smallest exact prototype of the weighted dual certificate.",
        },
        "runtime": {**runtime, "compiler": subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]},
        "frozen_hashes": frozen,
        "replay": {
            "control_check": "python3 proof/check_cycle_8_fused_lift.py",
            "check_command": "python3 proof/build_cycle_8_lrc_fused_lift.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_8_lrc_fused_lift.py -v",
        },
        "sealer": {"path": "proof/build_cycle_8_lrc_fused_lift.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
