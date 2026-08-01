#!/usr/bin/env python3
"""Seal the actual-log leading-eigenvector CRR probe preregistration."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v1.json"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "numpy": "1.26.4",
    "optimization_level": 0,
}
INPUTS: dict[str, tuple[Path, str]] = {
    "spectral_phase_lift": (
        ROOT / "artifacts/cycle-6-crr-spectral-phase-lift-v1.json",
        "",
    ),
    "farey_log_v1": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json",
        "8f204d56a5609fa9c8a93b152a969a038bc13463d3a36ca746e842bfe21e5f40",
    ),
    "conventions": (ROOT / "conventions/crr_actual_log_spectral_probe_v1.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-actual-log-spectral-probe-preregistration-v1.md", ""),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, label: str):
    spec = importlib.util.spec_from_file_location(label, path)
    require(spec is not None and spec.loader is not None, f"cannot load module: {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    import numpy as np

    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "actual-log spectral preregistration requires non-optimized CPython 3.12.3 and NumPy 1.26.4")
    return result


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing input: {label}")
        actual = sha256(path)
        if expected:
            require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def validate_context() -> dict[str, str]:
    spectral = json.loads(INPUTS["spectral_phase_lift"][0].read_text(encoding="utf-8"))
    require(spectral.get("phase_lift", {}).get("exact_identity", "").startswith("Gamma(W)=max_"), "phase-lift identity missing")
    farey = json.loads(INPUTS["farey_log_v1"][0].read_text(encoding="utf-8"))
    identity = farey.get("multiplicative_ray_cross_gram", {}).get("labeled_entry_identity")
    require(identity == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "actual Farey label mismatch")
    return {
        "phase_lift_status": spectral["phase_lift"]["epistemic_status"],
        "actual_farey_identity": identity,
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_module(INPUTS["conventions"][0], "crr_actual_log_spectral_probe_v1")
    rows = conventions.exact_rows()
    require(rows["v"] == 2 and rows["H"] == 4096 and rows["L"] == 1024 and rows["R"] == 256 and rows["Q"] == 16, "frozen small-scale row mismatch")
    require(rows["central_value"] == 128 and rows["raw_farey_amplitude"] == 64, "central threshold mismatch")
    require(rows["minimum_separation"] == 2 and rows["macrocells"] == 16 and rows["points_per_macrocell"] == 16, "stratified design mismatch")
    return rows


def seal() -> dict[str, Any]:
    return {
        "artifact_id": "cycle-6-crr-actual-log-spectral-probe-preregistration-v1",
        "epistemic_status": "CONJECTURED",
        "status": "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE",
        "claim_boundary": "A three-row bounded actual-log discovery protocol only. It proves no continuous CRR compatibility/incompatibility statement, AFARI/FARI result, extremizer, saturation theorem, density theorem, or short-interval consequence. A hit is OBSERVED and a miss is not a universal negative.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "literal label construction, exact integer ray/energy checks, fixed deterministic iteration, preregistration replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "frozen_rows": exact_rows(),
        "row_schedule": [
            {"id": "F0-farey-leading-phase", "initial_W": "literal-Farey power-vector stratified selector", "coefficient_design": "top-left-eigenvector capped phase", "joint_reselections": 0},
            {"id": "F1-farey-leading-minimum", "initial_W": "literal-Farey power-vector stratified selector", "coefficient_design": "top-left-eigenvector phase followed by 16 inverse-row-weighted updates", "joint_reselections": 0},
            {"id": "F2-joint-reselection-minimum", "initial_W": "literal-Farey power-vector stratified selector", "coefficient_design": "two fixed joint reselections, each after 16 inverse-row-weighted updates, then final 16 updates", "joint_reselections": 2},
        ],
        "common_object_rule": "Within every row, each reported b and W are the same final pair; no coefficient, W, energy, or Farey diagnostic may be optimized on a separately chosen row object.",
        "actual_labels": {
            "dirichlet": "D_b(t)=sum_(L<n<2L)w(n/L)b_n n^(it)",
            "farey": "gcd(r,s)=1, Q<=r,s<2Q, 3/4<=r/s<=5/4, theta in {-3,0,3}",
            "ray_score": "A_disc(W)=sum_(r,s,theta)#K_(r,s)|R_W((r/s)exp(theta/H))|^2",
            "inherited_cross_gram": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))",
        },
        "iteration": {
            "farey_power_iterations": 32,
            "minimum_value_iterations": 16,
            "joint_outer_iterations": 2,
            "minimum_update": "z=phase(M_W b); p_t proportional to 1/max(|(M_W b)_t|,2^-40); b<-phase(M_W^*(p z))",
            "fixed_p_property": "For the fixed p,z used in one update, the coordinatewise phase replacement cannot decrease the weighted linear phase functional; no global monotonicity is claimed after p changes.",
            "joint_selector": "equal-weight sum of normalized literal-Farey power score and normalized |D_b(t)| score, followed by the frozen stratified selector",
        },
        "retention": {
            "all_rows_rule": "Every scheduled row is retained exactly once as OBSERVED_JOINT_PROXY_HIT, NO_RETAINED_HIT, RESOURCE_CAP, or GLOBAL_CAP_UNREACHED.",
            "hit_gates": {
                "coefficient_cap": "max_n|b_n|<=1+2^-40",
                "central_minimum_value": "min_t|D_b(t)|>=128",
                "central_energy_band": "R^4/(4H)<=E_1(W)<=4R^4/H",
                "discrete_farey_activity": "at least 1/8 of frozen (r,s,theta) labels have |R_W|>=64",
                "leading_certificate": "the numerical leading-phase lower root sqrt(lambda*N*rho*phi^2/R) is at least 128",
            },
            "miss_interpretation": "A NO_RETAINED_HIT is a bounded diagnostic outcome only and is not evidence for AFARI, FARI, CRR-U, or any universal incompatibility.",
        },
        "resources": {
            "rng": "NONE",
            "wall_seconds_cap": 600,
            "rss_bytes_cap": 1073741824,
            "failure_rule": "On a cap, retain the active row as RESOURCE_CAP and all later rows once as GLOBAL_CAP_UNREACHED; do not resume or alter a parameter.",
        },
        "numerics": {
            "status": "RECOGNIZED",
            "algorithm": "NumPy binary64/complex128; exact Python-integer energy and ray labels",
            "not_certified": "No floating result is an interval enclosure or a proof-grade continuous claim.",
        },
        "replay": {
            "write_command": "python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py --write",
            "check_command": "python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py --check",
            "runner_write_command": "python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --write",
            "runner_check_command": "python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --check",
        },
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite actual-log spectral preregistration")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "actual-log spectral preregistration is absent")
        require(OUTPUT.read_bytes() == render(payload), "actual-log spectral preregistration mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
