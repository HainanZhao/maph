#!/usr/bin/env python3
"""Seal the CRR all-row phase-flatness reduction, version 1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-phase-flatness-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (
        ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json",
        "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e",
    ),
    "farey_log_v2_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json",
        "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8",
    ),
    "spectral_phase_lift_artifact": (
        ROOT / "artifacts/cycle-6-crr-spectral-phase-lift-v1.json",
        "165aff6e15a9c2177b1a69d7a2ce32ff9ba3b2d651aba6683d9f5ecca21403e4",
    ),
    "conventions": (ROOT / "conventions/crr_phase_flatness_v1.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-phase-flatness-v1.md", ""),
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
    spec = importlib.util.spec_from_file_location("crr_phase_flatness_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load phase-flatness conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "phase-flatness v1 requires non-optimized CPython 3.12.3")
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
    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    identity = farey.get("averaged_actual_farey_bundle", {}).get("labeled_identity")
    require(identity == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "actual Farey label mismatch")
    phase = load_json(INPUTS["spectral_phase_lift_artifact"][0])
    certificate = phase.get("leading_eigenvector_gate", {}).get("certificate")
    require(certificate == "Gamma(W)^2>=lambda*N*rho*phi^2/|W|", "leading certificate mismatch")
    return {
        "base_polynomial": base["polynomial"],
        "coefficient_cap": base["coefficients"],
        "common_set": base["set"],
        "actual_farey_identity": identity,
        "leading_certificate": certificate,
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_conventions()
    verified = conventions.verify_all()
    rows = conventions.phase_flatness_rows()
    require(rows["strict_closure"] == "ell+r+2*s<=2-gamma for fixed gamma>0", "strict phase-flatness closure mismatch")
    block = conventions.block_countermodel_bounds()
    require(block["right_rho"] == Fraction(1), "block rho mismatch")
    require(block["relative_phase_leakage"] == Fraction(0), "block leakage mismatch")
    cancellation = conventions.cancellation_countermodel()
    require(cancellation["minimum_top_leverage"] == Fraction(1), "cancellation leverage mismatch")
    require(cancellation["phi_square"] == Fraction(0), "cancellation flatness mismatch")
    return json_exact(verified)


def seal() -> dict[str, Any]:
    conventions = load_conventions()
    return {
        "artifact_id": "cycle-6-crr-phase-flatness-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALL_ROW_PHASE_FLATNESS_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves a finite-dimensional rowwise phase-flatness lemma for the actual CRR matrix conditional on explicit row statistics, and scoped abstract countermodels. It proves neither AFARI/FARI/CFARI nor CRR-U, a compatible witness, a cubic estimate, a density gain, a short-interval theorem, a saturation theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "finite-dimensional algebra, exact rational countermodel bounds, antecedent-hash replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "phase_flatness_lemma": {
            "epistemic_status": "PROVED",
            "decomposition": "M b^ph=||x||_1*sqrt(lambda)*u+r with r=M(b^ph-||x||_1*x) and ||M b^ph||_2^2=lambda||x||_1^2+||r||_2^2",
            "minimum_top_leverage": "mu_top(M,u)=m*min_t|u_t|^2",
            "relative_phase_leakage": "chi_ph(M,u)=max_t |r_t|/(||x||_1*sqrt(lambda)*|u_t|), with +infinity if some u_t=0",
            "lower_bound": "phi>=((1-kappa)/sqrt(1+kappa^2))*sqrt(mu_top) whenever chi_ph<=kappa<1",
            "scope": "valid for every finite complex matrix; its CRR use below retains the actual M_W and one common W",
        },
        "actual_log_conditional_gate": {
            "epistemic_status": "PROVED",
            "matrix": "M_W(t,n)=w(n/L)n^(it) on the exact support L<n<2L",
            "common_object_rule": "The same W supplies M_W, RationalMass, the actual Farey kernel, and the capped coefficient b^ph; no separately optimized coefficient or row set is used.",
            "assumptions": [
                "lambda>=v^(12-ell*delta(v))",
                "rho>=v^(-r*delta(v))",
                "mu_top>=v^(-2*s*delta(v))",
                "chi_ph<=kappa<1",
                "ell+r+2*s<=2-gamma for fixed gamma>0",
                "the same W satisfies the frozen CRR separation/cardinality/energy conditions and RationalMass(v)",
            ],
            "conclusion": "For all sufficiently large v, b^ph has |b_n^ph|<=1 and min_(t in W)|(M_W b^ph)_t|>=v^(7-delta(v)).",
            "farey_preservation": "The actual reduced labels, bounded jitter, rays, and C_theta(sk,rk)=R_W((r/s)*exp(theta/H)) identity remain untouched; no generic alias model is substituted.",
            "missing_statement": "It is CONJECTURED, not proved here, that the RationalMass-relevant actual-Farey class forces the displayed mu_top and chi_ph bounds.",
        },
        "countermodel_minimum_top_leverage": {
            "epistemic_status": "PROVED",
            "family": "K_(tau,epsilon)=(J_(m-1) direct_sum [1] with tau cross block + epsilon I)/(1+epsilon), factored after a right unitary makes the top right vector flat",
            "properties": "full rank, every Gram diagonal equals one, every cross-block entry is positive, rho=1, chi_ph=0, but phi^2=mu_top can tend to zero",
            "exact_sample": json_exact(conventions.block_countermodel_bounds()),
            "scope": "abstract matrix countermodel only; it is not a Dirichlet/Farey/RationalMass configuration",
        },
        "countermodel_phase_cancellation": {
            "epistemic_status": "PROVED",
            "family": "two-row, four-column SVD factor with x=(10,1,1,1)/sqrt(103), flat u=(1,1)/sqrt(2), and second singular-square 169/243",
            "properties": "lambda=1, fixed spectral gap 74/243, equal row diagonal 206/243, rho=169/412, mu_top=1, chi_ph=1, but phi=0 by exact row cancellation",
            "exact_data": json_exact(conventions.cancellation_countermodel()),
            "scope": "abstract matrix countermodel only; it is not a Dirichlet/Farey/RationalMass configuration",
        },
        "necessity_boundary": {
            "epistemic_status": "PROVED",
            "minimum_leverage": "When r=0, phi^2=mu_top exactly, so global participation cannot replace minimum top leverage.",
            "coordinatewise_leakage": "The cancellation family has mu_top=1 but chi_ph=1 and phi=0, so a global spectral-gap or averaged-residual bound cannot by itself give an all-row lower bound.",
            "next_target": "An actual-Farey inverse theorem must exploit the actual logarithmic matrix/Farey interaction to establish mu_top and chi_ph, or solve the exact phase program directly.",
        },
        "falsifiers": {
            "lemma": "A finite matrix violating the displayed decomposition, orthogonality identity, or phase-flatness lower bound refutes the lemma.",
            "block_countermodel": "An algebraic failure of positive definiteness, equal diagonal, top singular-vector construction, or the stated rational phi/participation bounds refutes that scoped countermodel.",
            "actual_gate": "An orientation error in M_W(t,n), a changed coefficient cap, a changed W, or a generic-alias replacement would invalidate the CRR conditional gate.",
        },
        "exact_replay": exact_rows(),
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_phase_flatness_v1.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_phase_flatness_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_phase_flatness_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite phase-flatness artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "phase-flatness artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "phase-flatness artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
