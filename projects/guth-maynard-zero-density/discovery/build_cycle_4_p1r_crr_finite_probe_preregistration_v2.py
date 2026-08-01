#!/usr/bin/env python3
"""Seal/check the executable corrected CRR finite-probe preregistration v2."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any

import mpmath
import numpy


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v2.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_preregistration": (ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v1.json", "02b9f77c65c027ae13f929985d1e7a7c5fa695ca1dba2ab2c8c190b2c1f867de"),
    "v2_conventions": (ROOT / "conventions/crr_finite_analogue_probe_v2.py", "8cc54eafebe058da091e74b41ae01e80373b5ec0824fa7f5a09f0afc80d9aad7"),
    "correction_document": (ROOT / "docs/cycle-4-p1r-crr-finite-probe-preregistration-v2-correction.md", "60b32334d12fae81d75f7e5cce540af379a53e0d7cf8552ea88149cf020208c0"),
}
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "mpmath": "1.2.1",
    "numpy": "1.26.4",
    "optimization_level": 0,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_conventions():
    path = INPUTS["v2_conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_finite_analogue_probe_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load v2 finite-probe conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "mpmath": mpmath.__version__,
        "numpy": numpy.__version__,
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "finite CRR preregistration v2 requires pinned CPython 3.12.3, mpmath 1.2.1, NumPy 1.26.4, and no -O")
    return result


def seal() -> dict[str, Any]:
    run = runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    v1 = json.loads(INPUTS["v1_preregistration"][0].read_text(encoding="utf-8"))
    require(v1["status"] == "SEALED_DISCOVERY_PREREGISTRATION_UNEXECUTED", "v1 predecessor identity/status mismatch")
    c = load_conventions()
    rows = c.scheduled_rows()
    old_rows = v1["schedule"]["rows"]
    require(len(rows) == len(old_rows) == 160, "v2 must retain all v1 rows")
    for old, new in zip(old_rows, rows, strict=True):
        for key in ("row_number", "id", "N", "family", "replicate", "row_seed"):
            require(old[key] == new[key], f"v2 changed v1 schedule field {key}")
        for key, value in old["variant"].items():
            require(new["variant"].get(key) == value, f"v2 changed v1 variant {key}")
    scales = c.expected_scale_rows()
    require({str(key): value for key, value in scales.items()} == v1["exact_scale_rows"], "v2 changed exact finite scales")
    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-preregistration-v2",
        "epistemic_status": "CONJECTURED",
        "status": "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE",
        "claim_boundary": "Corrected executable 160-row finite discovery protocol only. It proves no CRR compatibility/incompatibility, extremizer, saturation theorem, density estimate, or short-interval result. Any finite hit is OBSERVED and complex final values are RECOGNIZED.",
        "runtime": run,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "predecessor": {
            "artifact_id": v1["artifact_id"],
            "v1_disposition": "CONTAINED_UNEXECUTABLE: immutable v1 lacked fully executable construction, phase, score, and feasible precision rules; no v1 row was run.",
            "preserved": ["160 ids/order/seeds", "N,H,R,Q,V scales", "five families/four variants/two replicates", "thresholds", "128 proposals", "16/32 quadrature", "8/12 cubic", "5% margins", "55-minute cap", "1-GiB cap", "retention semantics"],
        },
        "research_stage_review_policy": {"lightweight_checks": ["hash pins", "schedule preservation", "exact-scale preservation", "byte replay", "tests"], "hostile_audit": "NOT_INITIATED; DEFERRED_TO_PAPER_STAGE"},
        "schedule": {"factorization": "4 N values * 5 families * 4 variants * 2 replicates = 160", "canonical_order": "N, family, variant, replicate", "master_seed": f"0x{c.MASTER_SEED:016X}", "rng": "SplitMix64 unsigned-64 wraparound; exact word consumption fixed in execution_contract", "rows": rows},
        "exact_scale_rows": {str(key): value for key, value in scales.items()},
        "execution_contract": c.CONSTRUCTION_CONTRACT,
        "resources": {"aggregate_wall_seconds": c.WALL_SECONDS, "aggregate_wall_minutes": c.WALL_SECONDS // 60, "max_rss_bytes": c.RSS_BYTES, "max_rss_gib": 1},
        "thresholds": v1["retention"]["thresholds"],
        "failure_codes": v1["retention"]["failure_codes"],
        "precision": {"mutation_proxy": "NumPy binary64/complex128; never final", "outcome": "mpmath 256/384-bit screen-confirmed first failed complex diagnostic, or all diagnostics for provisional hit", "recognition_ball": v1["retention"]["recognition_ball"], "classification": "complex outcome values are RECOGNIZED, not CERTIFIED_NUMERICAL"},
        "execution": {"authorized_after_seal": True, "executed_by_this_builder": False, "future_output_directory": "discovery/", "all_misses_are_not_universal_negative": True, "no_parameter_changing_retry": True},
        "replay": {"check_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v2.py --check", "write_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v2.py --write"},
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
        require(not OUTPUT.exists(), "refusing to overwrite v2 finite-probe preregistration artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "v2 finite-probe preregistration artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "v2 finite-probe preregistration artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "rows": len(payload["schedule"]["rows"]), "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
