#!/usr/bin/env python3
"""Seal the CRR capped spectral phase-lift reduction, version 1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-spectral-phase-lift-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (
        ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json",
        "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e",
    ),
    "farey_log_v1_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json",
        "8f204d56a5609fa9c8a93b152a969a038bc13463d3a36ca746e842bfe21e5f40",
    ),
    "farey_log_v2_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json",
        "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8",
    ),
    "conventions": (ROOT / "conventions/crr_spectral_phase_lift_v1.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-spectral-phase-lift-v1.md", ""),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def json_exact(value: Any) -> Any:
    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, tuple):
        return [json_exact(item) for item in value]
    if isinstance(value, list):
        return [json_exact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_exact(item) for key, item in value.items()}
    return value


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_spectral_phase_lift_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load spectral phase-lift conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "spectral phase-lift v1 requires non-optimized CPython 3.12.3")
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
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("polynomial") == "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)", "CRR polynomial label mismatch")
    require(base.get("coefficients") == "b_n for n>=1 complex with |b_n|<=1", "CRR coefficient cap mismatch")
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "CRR common set mismatch")
    v1 = load_json(INPUTS["farey_log_v1_artifact"][0])
    require(v1.get("multiplicative_ray_cross_gram", {}).get("labeled_entry_identity") == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "Farey v1 label mismatch")
    v2 = load_json(INPUTS["farey_log_v2_artifact"][0])
    require(v2.get("afari_target", {}).get("epistemic_status") == "CONJECTURED", "AFARI status mismatch")
    require("Base/coefficient coupling" in v2.get("uncoupled_global_l2_saturation", {}).get("required_new_information_for_fixed_power_gain", ""), "coupling target mismatch")
    return {
        "base_polynomial": base["polynomial"],
        "coefficient_cap": base["coefficients"],
        "common_set": base["set"],
        "actual_farey_identity": v1["multiplicative_ray_cross_gram"]["labeled_entry_identity"],
        "afari_status": v2["afari_target"]["epistemic_status"],
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_conventions()
    verified = conventions.verify_all()
    rows = conventions.exponent_rows()
    require(rows["base_pointwise_square"] == (Fraction(14), Fraction(-2)), "pointwise square row mismatch")
    require(rows["central_top_eigenvalue"] == (Fraction(12), Fraction()), "top eigenvalue row mismatch")
    require(rows["central_support_over_cardinality"] == (Fraction(2), Fraction()), "support/cardinality row mismatch")
    require(rows["strict_closure_condition"] == "ell+r+2s<=2-gamma for fixed gamma>0", "strict margin row mismatch")
    return json_exact(verified)


def seal() -> dict[str, Any]:
    return {
        "artifact_id": "cycle-6-crr-spectral-phase-lift-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CAPPED_SPECTRAL_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves an exact finite-dimensional coefficient-capped phase-lift/minimax reduction and a leading-eigenvector sufficient certificate for the actual CRR matrix. It proves neither an asymptotic CRR witness nor AFARI/FARI/CRR-U, a cubic estimate, a density gain, a short-interval theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "finite-dimensional algebra, explicit separation proof, exact scale arithmetic, antecedent-hash replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "phase_lift": {
            "epistemic_status": "PROVED",
            "matrix": "M_W(t,n)=w(n/L)n^(it) on I_L={n in Z:L<n<2L}",
            "common_object_rule": "One fixed W is used in M_W, in Gamma(W), and in every coefficient vector; no separately optimized set is allowed.",
            "capped_value": "Gamma(W)=max_(|b_n|<=1) min_(t in W)|(M_W b)_t|",
            "exact_identity": "Gamma(W)=max_(z in T^W) min_(p in Delta(W)) sum_(n in I_L)|(M_W^*(p z))_n|",
            "proof_mechanism": "finite compact-convex separation for the row-margin vector, followed by the coordinatewise complex-polydisc support function",
            "minimum_value_warning": "Uniform p is only one lower-level diagnostic; the inner min over p is indispensable for an all-row certificate.",
        },
        "leading_eigenvector_gate": {
            "epistemic_status": "PROVED",
            "definitions": {
                "lambda": "lambda_max(M_W M_W^*)",
                "u": "a unit top left eigenvector",
                "x": "M_W^*u/sqrt(lambda), a unit top right eigenvector",
                "b_phase": "b_n^ph=x_n/|x_n|, with 0 when x_n=0",
                "rho": "||x||_1^2/N",
                "phi": "sqrt(|W|)*min_(t in W)|(M_W b^ph)_t|/||M_W b^ph||_2",
            },
            "range": "0<=rho<=1 and 0<=phi<=1",
            "certificate": "Gamma(W)^2>=lambda*N*rho*phi^2/|W|",
            "interpretation": "rho is the coefficient-cap/delocalization loss and phi is the all-row flatness loss; lambda alone is not enough.",
        },
        "central_asymptotic_gate": {
            "epistemic_status": "PROVED",
            "scope": "central-cardinality W with |W|=R=v^8 only; energy and RationalMass remain independent requirements",
            "assumptions": [
                "lambda>=v^(12-ell*delta(v))",
                "rho>=v^(-r*delta(v))",
                "phi>=v^(-s*delta(v))",
                "ell+r+2s<=2-gamma for fixed gamma>0",
            ],
            "conclusion": "For all sufficiently large v, Gamma(W)>=v^(7-delta(v)).",
            "reason": "N=L-1 and the strict gamma margin absorb the fixed support factor because v^(gamma*delta(v)) tends to infinity.",
            "boundary_limit": "Failure of this sufficient gate is not a no-go for other capped coefficients or for a CRR witness.",
        },
        "actual_farey_relation": {
            "epistemic_status": "PROVED",
            "preserved_identity": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))",
            "scope": "The phase lift does not replace actual reduced Farey labels, multiplicative rays, bounded jitter, energy, or RationalMass. It isolates the remaining coefficient-capped all-row condition on the same W.",
        },
        "next_gate": {
            "status": "OPEN",
            "construction": "Construct an actual-Farey/RationalMass-relevant W with the strict leading gate, or solve the exact phase program directly.",
            "obstruction": "Prove an inverse bound for the exact max_z min_p phase program on the relevant actual-Farey class.",
        },
        "falsifiers": {
            "phase_lift": "An orientation error in the polydisc support function, failure of the finite separation argument, or a finite counterexample to the stated identity.",
            "leading_gate": "A finite matrix for which the displayed b^ph violates Gamma(W)^2>=lambda*N*rho*phi^2/|W|.",
        },
        "exact_replay": exact_rows(),
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_spectral_phase_lift_v1.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_spectral_phase_lift_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_spectral_phase_lift_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite spectral phase-lift artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "spectral phase-lift artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "spectral phase-lift artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
