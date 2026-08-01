#!/usr/bin/env python3
"""Seal the Cycle 12 balanced five-factor fractional-tensor theorem."""
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
OUTPUT = ROOT / "artifacts/cycle-12-balanced-five-factor-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-12-balanced-five-factor-preregistration-v1.md", "ce00ef8b230ac6806606a01756d8c27aae4115392301b1c3ee81c23e2ec2a88c"),
    "document": (ROOT / "docs/cycle-12-balanced-five-factor-v1.md", "9211c61003a2dcda7a483efa76a6cabed49db3000faa5c4b2883e4411111780a"),
    "conventions": (ROOT / "conventions/balanced_five_factor_v1.py", "da04098ce2fa91457941fa97206ef07fe362b4e3e20f8a9fc4b15d7c9857d2b9"),
    "tests": (ROOT / "tests/test_cycle_12_balanced_five_factor_v1.py", "108e3962c56812fea093102b064c763e9f232b1d8e933b35a2be7003fe5a4748"),
    "source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "cycle11_artifact": (ROOT / "artifacts/cycle-11-e1-e2-block-variance-v1.json", "fa6264fc8d040f0e0164b1256ec97f07a6637c7688b94f794096cb6bdef04a8a"),
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
    require(runtime == EXPECTED_RUNTIME, "Cycle 12 balanced-five-factor v1 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("balanced_five_factor_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load balanced-five-factor conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_sources() -> dict[str, Any]:
    source = INPUTS["source"][0].read_text(encoding="utf-8")
    for text, label in (
        ("$N=T^{5/13}$", "critical original length"),
        ("a Dirichlet polynomial of length $N^2=T^{10/13}$", "critical squared length"),
        ("$T_1=T^{12/13}$", "critical local interval"),
        ("Using a simple orthogonality argument", "mean-value source anchor"),
        ("apply Theorem \\ref{thrm:LargeValues} to the Dirichlet polynomial $\\tilde{D}^k$", "integer-power detector anchor"),
    ):
        require(text in source, f"source anchor missing: {label}")
    cycle11 = load_json(INPUTS["cycle11_artifact"][0])
    require(cycle11.get("artifact_id") == "cycle-11-e1-e2-block-variance-v1", "Cycle 11 identity mismatch")
    require(cycle11.get("next_gate", {}).get("epistemic_status") == "CONJECTURED", "Cycle 11 next-gate mismatch")
    return {
        "zero_detector": "TeX lines 2309--2330",
        "integer_power": "TeX lines 2332--2351",
        "critical_configuration": "TeX line 2398",
        "mean_value": "TeX lines 219--227",
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    rows = checked["critical_exponents"]
    require(rows["local_rows"] == Fraction(36, 5), "local exponent mismatch")
    require(rows["local_gain"] == Fraction(4, 5), "local gain mismatch")
    require(rows["density_coefficient"] == Fraction(82, 39), "conditional density anchor mismatch")
    require(rows["conditional_interval"] == Fraction(43, 82), "conditional interval target mismatch")
    require(checked["balance_grid"]["checked"] == 306, "balance-grid count mismatch")
    require(checked["balance_grid"]["uniformly_admissible"] == [[Fraction(1)] * 5], "balance-grid survivor mismatch")
    return exact_json(checked)


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    sources = validate_sources()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-12-balanced-five-factor-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDITIONAL_BALANCED_FIVE_FACTOR_LOCAL_GAIN_SOURCE_FACTORIZATION_OPEN",
        "claim_boundary": "Conditional on a sum of subpower-many balanced fivefold products with the frozen coefficient-square norms, this artifact proves the local critical row exponent 36/5 and gain 4/5. It does not construct the source factorization, prove a new zeta density estimate, improve a uniform density coefficient or prime interval, close a left neighborhood, prove Base/CRR incompatibility, or extend an L-function family.",
        "conditional_on": [
            "The relevant critical detector is a sum of v^o(1) products of five length-v^(1+o(1)) Dirichlet polynomials.",
            "Each of the ten cube-two/square-three moment polynomials has coefficient square norm at most v^(12+o(1)).",
            "The rows are one-separated in an interval of length v^12 and the component selection loses only v^o(1).",
        ],
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "source inspection, exact combinatorics and exponent algebra, registered rational balance enumeration, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "source_context": {"epistemic_status": "PROVED", **sources},
        "fractional_tensor": {
            "epistemic_status": "PROVED",
            "identity": "For ten two-subsets S, geometric_mean_S |prod_(j in S)A_j^3 prod_(j notin S)A_j^2|=|prod_j A_j|^(12/5).",
            "selection": "At every row, one of ten integer-power moments is at least |A|^(12/5).",
            "length": "Five balanced length-v factors give moment length v^12, exactly the local time scale H.",
        },
        "conditional_local_theorem": {
            "epistemic_status": "PROVED",
            "row_bound": "|W|<=v^(36/5+(24/5)delta+o(1)) under the frozen balanced-factor hypotheses.",
            "main_exponent": "36/5",
            "gain_over_baseline": "4/5",
            "route": "ten-colour geometric-mean selection followed by the discrete mean-value theorem at length H=v^12",
        },
        "balance_boundary": {
            "epistemic_status": "PROVED",
            "statement": "For five nonnegative factor exponents summing to 5, every cube-two/square-three moment has length exponent at most 12 iff all five exponents equal 1.",
            "scope": "This is a sharp boundary for the uniform ten-moment design only; weighted/adaptive variants remain open.",
            "unbalanced_countermodel": "(1/2,1/2,1,3/2,3/2) has moment lengths ranging from 11 to 13.",
        },
        "source_factorization": {
            "epistemic_status": "CONJECTURED",
            "status": "OPEN",
            "target": "Decompose the critical normalized Type-I detector into v^o(1) balanced fivefold products with divisor-bounded convolution coefficients.",
            "adverse_cases": "rough/prime-dominated integers, power-many product components, coefficient multiplicity, or an unavoidable moment length v^(12+kappa)",
        },
        "conditional_anchor_map": {
            "epistemic_status": "PROVED",
            "global_exponent_at_7_10": "41/5",
            "density_coefficient_at_7_10": "82/39",
            "anchor_gain": "8/39",
            "formal_interval_target": "43/82",
            "boundary": "Pointwise conditional anchor only; not a uniform density or interval theorem.",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION", "statement": "The source factorization and left-neighborhood/global-envelope gates are open."},
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_12_balanced_five_factor_v1.py --write",
            "check_command": "python3 proof/build_cycle_12_balanced_five_factor_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_12_balanced_five_factor_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 12 balanced-five-factor v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 12 balanced-five-factor v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 12 balanced-five-factor v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
