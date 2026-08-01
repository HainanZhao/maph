#!/usr/bin/env python3
"""Seal/check v3, the dimensional correction to the CRR finite probe."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v3.json"
INPUTS = {
    "v2_preregistration": (ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v2.json", "e98941eb26368b3f77d9fc9fd012f33a4e997355ae986a39c5e4c5541d616cf0"),
    "v3_conventions": (ROOT / "conventions/crr_finite_analogue_probe_v3.py", "f8d85addbb1d6fd4033a1b61bb89ef8aad43af2e17108736286db706d38ac4fa"),
    "correction_document": (ROOT / "docs/cycle-4-p1r-crr-finite-probe-preregistration-v3-correction.md", "a22ac5fc4f34c86716ba9ebf77939ce9d21c0e3cb4e843b3aa24c3cf189dabee"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_v3():
    spec = importlib.util.spec_from_file_location("crr_finite_analogue_probe_v3", INPUTS["v3_conventions"][0])
    require(spec is not None and spec.loader is not None, "cannot load v3 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def seal() -> dict[str, Any]:
    pins: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        pins[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    v2 = json.loads(INPUTS["v2_preregistration"][0].read_text(encoding="utf-8"))
    require(v2["status"] == "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE", "v2 status mismatch")
    c = load_v3()
    require(c.scheduled_rows() == v2["schedule"]["rows"], "v3 changed schedule or variants")
    require({str(n): row for n, row in c.expected_scale_rows().items()} == v2["exact_scale_rows"], "v3 changed scale rows")
    require("Never use tr((diag(w)G-M I_(2M))^3)." in c.CUBIC_DIMENSIONAL_IDENTITY, "v3 cubic prohibition missing")
    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-preregistration-v3",
        "epistemic_status": "CONJECTURED",
        "status": "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE",
        "claim_boundary": "Executable 160-row finite discovery protocol only. No CRR compatibility/incompatibility, extremizer, saturation, density, or short-interval theorem follows. Finite hits are OBSERVED; complex diagnostics are RECOGNIZED.",
        "runtime": v2["runtime"],
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": pins,
        "predecessor": {"v1": "CONTAINED_UNEXECUTABLE: family/phase/proxy/precision omissions", "v2": "CONTAINED_UNEXECUTED: cubic low-rank dimensional identity not explicit", "preserved_v2_schedule_and_scientific_thresholds": True},
        "schedule": v2["schedule"],
        "exact_scale_rows": v2["exact_scale_rows"],
        "execution_contract": c.CONSTRUCTION_CONTRACT,
        "resources": v2["resources"],
        "thresholds": v2["thresholds"],
        "failure_codes": v2["failure_codes"],
        "precision": v2["precision"],
        "execution": v2["execution"],
        "research_stage_review_policy": {"lightweight_checks": ["hash pins", "schedule/threshold invariance", "ambient trace identity", "byte replay", "tests"], "hostile_audit": "NOT_INITIATED; DEFERRED_TO_PAPER_STAGE"},
        "replay": {"check_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v3.py --check", "write_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v3.py --write"},
    }


def render(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite v3 preregistration")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file() and OUTPUT.read_bytes() == render(payload), "v3 preregistration byte mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "rows": len(payload["schedule"]["rows"]), "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
