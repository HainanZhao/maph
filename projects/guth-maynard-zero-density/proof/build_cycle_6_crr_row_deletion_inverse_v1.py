#!/usr/bin/env python3
"""Seal the CRR actual-log row-deletion inverse reduction, version 1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-row-deletion-inverse-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (
        ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json",
        "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e",
    ),
    "crr_v2_conventions": (
        ROOT / "conventions/crr_formalization_v2.py",
        "0d960b76a4ad03cce43727159cf846696dbee732184df44b2ee0503b9ae18ce8",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
    "farey_log_v2_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json",
        "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8",
    ),
    "phase_flatness_artifact": (
        ROOT / "artifacts/cycle-6-crr-phase-flatness-v1.json",
        "28990f2c703e0f8bfba8e25fb40ecc3d8231392e564653a01fcf5330a52b83ff",
    ),
    "conventions": (ROOT / "conventions/crr_row_deletion_inverse_v1.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-row-deletion-inverse-v1.md", ""),
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


def load_module(label: str, module_name: str):
    path = INPUTS[label][0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "row-deletion inverse v1 requires non-optimized CPython 3.12.3")
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
    crr_conventions = load_module("crr_v2_conventions", "crr_formalization_v2_for_deletion")
    require(crr_conventions.SUPPORT_AND_PLATEAU["w"] == "0<=w<=1; supp(w) subset [1,2]; w=1 on [6/5,9/5]", "plateau convention mismatch")
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    require(r"with $w(t)=1$ for $t\in [6/5,9/5]$" in source, "source plateau anchor mismatch")
    require("(M_W)_{t,n}=w(n/N)n^{it}" in source, "source matrix anchor mismatch")
    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    identity = farey.get("averaged_actual_farey_bundle", {}).get("labeled_identity")
    theta_mass = farey.get("averaged_actual_farey_lower", {}).get("theta_mass_lower")
    require(identity == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "Farey label mismatch")
    require(theta_mass == "sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta >= (75/2)*H*v^(8-3*delta(v))", "Farey theta-mass mismatch")
    phase = load_json(INPUTS["phase_flatness_artifact"][0])
    lower = phase.get("phase_flatness_lemma", {}).get("lower_bound")
    require(lower == "phi>=((1-kappa)/sqrt(1+kappa^2))*sqrt(mu_top) whenever chi_ph<=kappa<1", "phase-flatness lemma mismatch")
    return {
        "base_polynomial": base["polynomial"],
        "coefficient_cap": base["coefficients"],
        "common_set": base["set"],
        "weight_plateau": crr_conventions.SUPPORT_AND_PLATEAU["w"],
        "actual_farey_identity": identity,
        "rationalmass_theta_mass": theta_mass,
        "phase_flatness_lower": lower,
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_row_deletion_inverse_v1")
    verified = conventions.verify_all()
    deletion = conventions.deletion_rows()
    require(deletion["coordinate_lower"] == "|u_t|^2>=d_t^2/(d_t^2+beta_t^2), with 0/0 interpreted as 0", "coordinate lower mismatch")
    rank_one = conventions.rank_one_sharpness()
    require(rank_one["minimum_top_leverage"] == Fraction(3, 14), "rank-one sharpness mismatch")
    cancellation = conventions.cancellation_projection_calibration()
    require(cancellation["chi_ph_square"] == Fraction(1), "projection sharpness mismatch")
    return json_exact(verified)


def seal() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_row_deletion_inverse_v1_for_seal")
    return {
        "artifact_id": "cycle-6-crr-row-deletion-inverse-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_LOG_ROW_DELETION_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves actual-log row-deletion and Gram-projection reductions, plus a scoped diagonal-Cauchy limitation and Farey deletion accounting. It proves neither an RFDI theorem nor an actual witness, AFARI/FARI/CFARI/CRR-U, a cubic estimate, a density gain, a short-interval theorem, a saturation theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "exact finite-dimensional spectral algebra, pinned source/convention anchors, rational scale bookkeeping, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "actual_log_gram": {
            "epistemic_status": "PROVED",
            "matrix": "M_W(t,n)=w(n/L)n^(it)",
            "gram": "G_W(t,s)=sum_(L<n<2L)w(n/L)^2*n^(i(t-s))",
            "constant_diagonal": "G_W(t,t)=S_L=sum_(L<n<2L)w(n/L)^2",
            "plateau_bounds": json_exact(conventions.plateau_l2_bounds()),
            "source_anchor": "LargevaluesDirichlet17.tex lines 425-426 and 484-487 in the pinned source",
        },
        "row_deletion_leverage": {
            "epistemic_status": "PROVED",
            "definitions": {
                "lambda_minus_t": "lambda_max(G_(W minus {t}))",
                "d_t": "lambda-lambda_minus_t",
                "beta_t": "||G_(W minus {t},t)||_2",
                "actual_beta_square": "beta_t^2=sum_(s in W,s!=t)|sum_(L<n<2L)w(n/L)^2*n^(i(t-s))|^2=(G_W^2)_(t,t)-S_L^2",
                "DelCov": "|W|*min_t d_t^2/(d_t^2+beta_t^2), with 0/0 interpreted as 0",
            },
            "coordinate_lower": "|u_t|^2>=d_t^2/(d_t^2+beta_t^2)",
            "consequence": "mu_top(W)>=DelCov(W)",
            "sharpness": json_exact(conventions.rank_one_sharpness()),
        },
        "phase_projection": {
            "epistemic_status": "PROVED",
            "definitions": {
                "q": "b^ph-||x||_1*x",
                "eta_ph": "||q||_2^2/||x||_1^2=(||b^ph||_2^2-||x||_1^2)/||x||_1^2",
                "r": "M_W*q",
            },
            "row_bound": "|r_t|^2<=(S_L-lambda|u_t|^2)||q||_2^2",
            "relative_bound": "chi_ph^2<=eta_ph*max_t(S_L/(lambda|u_t|^2)-1)<=eta_ph*(|W|*S_L/(lambda*mu_top)-1)",
            "combined_actual_test": "DelCov>0 and eta_ph*(|W|*S_L/(lambda*DelCov)-1)<=kappa^2 imply chi_ph<=kappa",
            "rho_relation": "eta_ph=(1-rho)/rho if x has full support; always eta_ph<=(1-rho)/rho",
            "sharpness_calibration": json_exact(conventions.cancellation_projection_calibration()),
        },
        "conditional_actual_gate": {
            "epistemic_status": "PROVED",
            "common_object_rule": "The same actual W supplies M_W, G_W, DelCov, RationalMass, the actual Farey kernel, and b^ph. The coefficient is capped coordinatewise and is not separately optimized.",
            "assumptions": [
                "lambda>=v^(12-ell*delta(v))",
                "rho>=v^(-r*delta(v))",
                "DelCov(W)>=v^(-2*s*delta(v))",
                "eta_ph*(R*S_L/(lambda*DelCov(W))-1)<=kappa^2 for fixed 0<=kappa<1",
                "ell+r+2*s<=2-gamma for fixed gamma>0",
                "the same W obeys the frozen CRR separation/cardinality/energy predicates and RationalMass(v)",
            ],
            "conclusion": "For all sufficiently large v, b^ph has |b_n^ph|<=1 and min_(t in W)|(M_W b^ph)_t|>=v^(7-delta(v)).",
            "farey_preservation": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H)) and all actual reduced labels, rays, and bounded jitter are retained.",
        },
        "diagonal_cauchy_limitation": {
            "epistemic_status": "PROVED",
            "conditional_regime": "If lambda<=v^(12+a*delta(v)) for fixed a>=0, then R*S_L/(lambda*DelCov)-1>=(1/2)*v^(6-a*delta(v))-1.",
            "meaning": "The displayed projection/Cauchy certificate for chi_ph<=kappa then requires eta_ph<=kappa^2/((1/2)*v^(6-a*delta(v))-1). This is a limitation of that certificate, not a no-go for the exact chi_ph.",
        },
        "farey_deletion_accounting": {
            "epistemic_status": "PROVED",
            "identities": json_exact(conventions.farey_deletion_rows()),
            "rationalmass_consequence": "RationalMass implies only the average Farey deletion lower bound 75*v^(12-3*delta(v))-6*v^8, not a minimum row bound or a transfer to DelCov(G_W).",
            "abstract_scope_limit": "J_(R-1) direct_sum [1] has total mass asymptotic to R^2 but minimum deletion influence one. It is not asserted to be the actual Farey kernel.",
        },
        "rfd_inverse_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Every actual W satisfying frozen RationalMass, separation, cardinality, and energy has DelCov(W)>=v^(-2*s*delta(v)) and eta_ph*(R*S_L/(lambda*DelCov(W))-1)<=kappa^2 for fixed s,kappa with kappa<1.",
            "conditional_effect": "Together with the lambda/rho rows and ell+r+2*s<2, this implies the prior capped all-row Base construction on the same W.",
            "what_it_must_control": "Each actual row's spectral deletion deficit relative to its aggregate off-row log correlation, plus phase-rounding projection; total Farey mass alone is insufficient.",
        },
        "falsifiers": {
            "deletion_lemma": "A finite PSD Gram matrix violating the block eigenvector inequality or its rank-one equality case refutes the reduction.",
            "projection_lemma": "A finite matrix violating the orthogonal projection identity or the displayed chi_ph upper bound refutes the reduction.",
            "actual_context": "A mismatch in the pinned w plateau, actual M_W label, common-W rule, Farey identity, or RationalMass theta-mass antecedent invalidates the actual-log specialization.",
        },
        "exact_replay": exact_rows(),
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_row_deletion_inverse_v1.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_row_deletion_inverse_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_row_deletion_inverse_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite row-deletion inverse artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "row-deletion inverse artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "row-deletion inverse artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
