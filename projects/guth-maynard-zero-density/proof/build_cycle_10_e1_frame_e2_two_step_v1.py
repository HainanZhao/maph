#!/usr/bin/env python3
"""Seal the Cycle 10 E1 frame and E2 two-step theorem artifact."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-10-e1-frame-e2-two-step-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-10-e1-e2-engine-preregistration-v1.md", "7c815ed40267bc6320e3783a0d1f4a1b611158b1620583cdad99040509d863d6"),
    "document": (ROOT / "docs/cycle-10-e1-frame-e2-two-step-v1.md", "256a7b8d1d588f318d6d1cc6cd79f304acb2f717a64a792c22c36ea30dc3abb9"),
    "conventions": (ROOT / "conventions/e1_e2_engine_v1.py", "dd2033cdd7eed37c49bc0f90783b7e597465e860dbe4968559bd308055022384"),
    "tests": (ROOT / "tests/test_cycle_10_e1_frame_e2_two_step_v1.py", "dbd740ebc6829730e5b48f490f2e344ff962b3da2e7a2ed375b719547179a9eb"),
    "source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "crr_v2": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "phase_base": (ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json", "3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534"),
    "signed_extremizer": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json", "9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [exact_json(item) for item in value]
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 10 E1/E2 v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return frozen


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("e1_e2_engine_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load E1/E2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def validate_sources() -> dict[str, Any]:
    source = INPUTS["source"][0].read_text(encoding="utf-8")
    require("There are $O(\\log{T})$ choices of $N$" in source, "dyadic detector source anchor missing")
    require("\\tr((M_WM_W^*)^3)-\\frac{\\tr(M_WM_W^*)^3}{k^{2}}" in source, "centred cubic source anchor missing")
    crr = load_json(INPUTS["crr_v2"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    phase = load_json(INPUTS["phase_base"][0])
    require(phase.get("base_necessary_saturation", {}).get("lower_product") == "Base cardinality plus pointwise values force lambda_(P,A)*Xi_(P,A)>=v^(12-3delta(v)).", "phase Base lower-product mismatch")
    extremizer = load_json(INPUTS["signed_extremizer"][0])
    require(extremizer.get("phase_lattice_extremizer", {}).get("epistemic_status") == "PROVED", "signed extremizer context mismatch")
    return {
        "gm_detector": "TeX lines 2309--2330: O(log T) dyadic lengths, largest Type-I family, Fourier translation, one fixed coefficient vector",
        "gm_spectral": "TeX lines 497--587: Gram singular-value bound, trace powers, and scalar-centred cubic statistic",
        "crr_base": "lambda>=v^(12-3delta(v)) is necessary after lambda*Xi>=v^(12-3delta(v)) and Xi<=1",
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    result = checked["nb4_search"]
    require(result["status"] == "NB4_SIGN_COUNTERMODEL", "NB4 search outcome mismatch")
    require(result["order"] == 4 and result["nb4"] == Fraction(-128), "NB4 countermodel mismatch")
    require(result["counts"] == {"3": 125, "4": 5}, "NB4 search counts mismatch")
    for exponent in range(1, 5):
        require(checked["e1_rows"][str(exponent)]["margin"] >= 0, "E1 exact check margin is negative")
    return exact_json(checked)


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    sources = validate_sources()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-10-e1-frame-e2-two-step-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_E1_FRAME_IDENTITY_E2_TWO_STEP_IDENTITY_NB4_COUNTERMODEL_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves the E1 weighted-frame trace inequality with explicit K^r colour cost, the pure-colouring no-gain boundary, the E2 two-step-return identity and spectral alternative, a raw-NB4 sign countermodel, and the resulting necessary Base dichotomy. It proves no saving for either dichotomy branch, no large-value or zero-density improvement, no shorter prime interval, no Base/CRR incompatibility, and no L-function theorem.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "source inspection, exact algebra, deterministic countermodel search, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "source_overlap": {"epistemic_status": "PROVED", **sources},
        "e1_frame_trace": {
            "epistemic_status": "PROVED",
            "kernel": "B=sum_j omega_j b_j b_j^*, K_B=M B M^*, q_t=(K_B)_(t,t)",
            "theorem": "If q_t>=V^2 on S, then |S|V^(2r)<=sum_t q_t^r<=tr(K_B^r) for every integer r>=1.",
            "colour_cost": "If one of K uniformly weighted detectors is V-large on each row, then |S|V^(2r)<=K^r tr(K_B^r).",
            "pure_colouring_boundary": "With no cross-detector structure, partitioning and largest-colour pigeonholing both give |S|<=K F; K=T^o(1) changes no fixed power exponent.",
            "missing_input": "A source-derived dictionary must give a mixed-trace saving larger than the explicit colour loss.",
        },
        "e2_two_step": {
            "epistemic_status": "PROVED",
            "definitions": "A=G-dI, r_i=sum_(j!=i)|A_ij|^2, R=diag(r_i), C_2=A^2-R",
            "identity": "||C_2||_F^2=tr(A^4)-sum_i r_i^2",
            "spectral_bound": "lambda_max(G)<=d+sqrt(max_i r_i+||C_2||_op)<=d+sqrt(max_i r_i+||C_2||_F)",
            "base_dichotomy": "For all sufficiently large v, Base forces max_i r_i>=(1/8)v^(24-6delta(v)) or ||C_2||_op>=(1/8)v^(24-6delta(v)).",
        },
        "nb4_sign": {
            "epistemic_status": "PROVED",
            "identity": "NB4=tr(A^4)-2sum_i r_i^2+sum_(i!=j)|A_ij|^4",
            "countermodel": rows["nb4_search"],
            "implication": "Raw NB4 is not a universal nonnegative spectral surrogate; positive two-step squares and refined centring remain live.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_ANALYTIC_GAIN", "statement": "Neither branch in the Base dichotomy is bounded below the necessary scale, so no density or interval propagation is authorized."},
        "next_hybrid_gate": {"epistemic_status": "CONJECTURED", "statement": "Apply return deletion to a source-derived frame kernel and prove that frame diversity lowers both row returns and coherent two-step excess by more than the K^r colour cost."},
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_10_e1_frame_e2_two_step_v1.py --write",
            "check_command": "python3 proof/build_cycle_10_e1_frame_e2_two_step_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_10_e1_frame_e2_two_step_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 10 E1/E2 v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 10 E1/E2 v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 10 E1/E2 v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
