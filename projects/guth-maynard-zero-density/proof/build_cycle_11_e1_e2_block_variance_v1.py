#!/usr/bin/env python3
"""Seal the Cycle 11 E1+E2 block-variance reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-11-e1-e2-block-variance-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-11-e1-e2-block-variance-preregistration-v1.md", "c4046cdafbcd545135632c8c897b4f11a1c4081f4dd67cb90da781d80eafb8b8"),
    "document": (ROOT / "docs/cycle-11-e1-e2-block-variance-v1.md", "80cb85be068597596e3e36050c14a081fdd654b461a86b6be5259443b648f0fe"),
    "conventions": (ROOT / "conventions/e1_e2_block_variance_v1.py", "d96837822581d785249571838810ea7254d1b932bcfb035e4f68a09b3dbce6d4"),
    "tests": (ROOT / "tests/test_cycle_11_e1_e2_block_variance_v1.py", "4869425aa79bbc3165ec7469149855c6395712360c577eedb1900b8096a9e60b"),
    "cycle10_artifact": (ROOT / "artifacts/cycle-10-e1-frame-e2-two-step-v1.json", "ca1e179cb2b39c2fe8c243aba0d6557b61f4d1dee3a02927bdac528030cb2246"),
    "crr_v2": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 11 block-variance v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return frozen


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("e1_e2_block_variance_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load block-variance conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, Any]:
    cycle10 = load_json(INPUTS["cycle10_artifact"][0])
    require(cycle10.get("artifact_id") == "cycle-10-e1-frame-e2-two-step-v1", "Cycle 10 identity mismatch")
    require("K^r" in cycle10.get("e1_frame_trace", {}).get("colour_cost", ""), "Cycle 10 colour-cost context mismatch")
    require("C_2" in cycle10.get("e2_two_step", {}).get("identity", ""), "Cycle 10 two-step context mismatch")
    crr = load_json(INPUTS["crr_v2"][0])
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "CRR cardinality mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "CRR pointwise mismatch")
    return {
        "cycle10": "weighted-frame K^r cost and two-step-return identity",
        "critical_rows": {"R_lower": "v^(8-delta)", "V_lower": "v^(7-delta)", "registered_K_upper": "v^delta"},
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    zero = checked["zero_variance"]["variance"]
    require(all(entry == 0 for row in zero for entry in row), "zero-variance model mismatch")
    constant = checked["constant_rank_one"]
    require(constant["lambda_p"] == Fraction(35, 3), "rank-one eigenvalue row mismatch")
    require(constant["lambda_c2_top"] == Fraction(196, 3), "C2 top eigenvalue row mismatch")
    require(constant["lambda_c2_other"] == Fraction(-49, 3), "C2 secondary eigenvalue row mismatch")
    random_rows = checked["random_colouring"]
    require(len(random_rows) == 8, "random-colouring row-count mismatch")
    require(random_rows["n5_k3"]["colourings"] == 243, "largest colouring enumeration mismatch")
    return exact_json(checked)


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-11-e1-e2-block-variance-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_BLOCK_VARIANCE_DECOMPOSITION_RANK_ONE_COHERENT_SATURATION_RANDOM_COLOUR_EXPECTATION",
        "claim_boundary": "This artifact proves the exact block-frame decomposition into the original detector rank-one kernel and a PSD variance kernel, raw Schatten saturation by the rank-one term, its coherent two-step scale, and the exact random-colouring expectation. It proves no arithmetic lower bound for variance, analytic saving, density improvement, shorter interval, Base/CRR incompatibility, or L-function theorem.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "exact algebra, exhaustive registered finite colouring checks, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "source_context": context,
        "block_variance": {
            "epistemic_status": "PROVED",
            "identity": "F=P+Z with F=sum_j d_jd_j^*, P=dd^*/K, d=sum_j d_j, Z=sum_j(d_j-d/K)(d_j-d/K)^*>=0",
            "diagonal": "Z_tt=sum_j|d_j(t)-d(t)/K|^2",
            "zero_variance_model": "d_j=d/K for every j gives Z=0 despite arbitrary largeness of d",
        },
        "raw_trace_boundary": {
            "epistemic_status": "PROVED",
            "statement": "For every integer r>=1, tr(F^r)>=tr(P^r)=(||d||_2^2/K)^r>=(RV^2/K)^r when |d_t|>=V.",
            "excess_factor": "The forced rank-one lower is R^(r-1) times the Cycle-10 row-diagonal threshold R(V^2/K)^r.",
            "implication": "An uncentred mixed Schatten trace retains the original common-detector obstruction; it cannot measure diversity without removing P.",
        },
        "rank_one_two_step": {
            "epistemic_status": "PROVED",
            "general_lower": "If |d_t|^2/K>=a on R>=3 rows, then ||C_2(P)||_op>=(R-1)(R-2)a^2.",
            "constant_spectrum": "For constant a: spec(C_2)={(R-1)(R-2)a^2,(2-R)a^2 with multiplicity R-1}.",
            "critical_eigenvalue": "lambda_max(P)>=v^(22-4delta) for R>=v^(8-delta), V>=v^(7-delta), K<=v^delta.",
            "critical_lower": "For sufficiently large v, ||C_2(P)||_op>=(1/4)v^(44-8delta).",
        },
        "random_colouring": {
            "epistemic_status": "PROVED",
            "identity": "E_chi sum_j D_j(t)conj(D_j(s))=D(t)conj(D(s))/K+(1-1/K)G_c(t,s)",
            "finite_exact_coverage": "All colourings for coefficient-set sizes 2 through 5 and K in {2,3}; 8 rows, no RNG.",
            "implication": "Random colouring preserves the forced rank-one detector kernel in expectation.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_ANALYTIC_GAIN", "statement": "The arithmetic size/dispersion of Z is open, so no density or interval propagation is authorized."},
        "next_gate": {"epistemic_status": "CONJECTURED", "statement": "Use actual multiplicative/prime blocks to force quantitative variance or build a detector ensemble without the old rank-one forced component."},
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_11_e1_e2_block_variance_v1.py --write",
            "check_command": "python3 proof/build_cycle_11_e1_e2_block_variance_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_11_e1_e2_block_variance_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 11 block-variance v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 11 block-variance v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 11 block-variance v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
