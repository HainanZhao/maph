#!/usr/bin/env python3
"""Seal the CRR actual-log/Farey RFDI outlier-surgery obstruction, v1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v1.json"
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
    "row_deletion_artifact": (
        ROOT / "artifacts/cycle-6-crr-row-deletion-inverse-v1.json",
        "9b0d74235c587d8624879626703efc9577020ebb8770defe022108914c35e832",
    ),
    "conventions": (ROOT / "conventions/crr_rfdi_outlier_surgery_v1.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-rfdi-outlier-surgery-v1.md", ""),
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
    require(result == EXPECTED_RUNTIME, "RFDI outlier surgery v1 requires non-optimized CPython 3.12.3")
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
    rational = crr.get("witness_schema", {}).get("rational_mass", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "CRR set anchor mismatch")
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "CRR cardinality anchor mismatch")
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "CRR energy anchor mismatch")
    require(base.get("energy_definition") == "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1", "CRR energy definition mismatch")
    require(rational.get("threshold") == "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))", "CRR RationalMass threshold mismatch")
    require(crr.get("witness_schema", {}).get("common_object_rule") == "One common pair (b,W) must satisfy Base(v), RationalMass(v), and PositiveCubic(v); no separately optimized W is admissible.", "common-object rule mismatch")
    conventions = load_module("crr_v2_conventions", "crr_formalization_v2_for_outlier_surgery")
    require(conventions.SUPPORT_AND_PLATEAU["psi1"] == "psi1>=0; supp(psi1) subset [-1,1]; psi1(0)=1", "psi1 anchor mismatch")
    require(conventions.SUPPORT_AND_PLATEAU["psi2"] == "psi2>=0; supp(psi2) subset [1/2,3/2]; psi2(1)=1", "psi2 anchor mismatch")
    require(conventions.SMOOTH_FUNCTIONS["psi1"] == "psi1(x)=eta(1-x^2)/eta(1)", "psi1 normalization mismatch")
    require(conventions.SMOOTH_FUNCTIONS["psi2"] == "psi2(u)=eta(1-4*(u-1)^2)/eta(1)", "psi2 normalization mismatch")
    require(conventions.SUPPORT_AND_PLATEAU["w"] == "0<=w<=1; supp(w) subset [1,2]; w=1 on [6/5,9/5]", "weight anchor mismatch")
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    require(r"with $w(t)=1$ for $t\in [6/5,9/5]$" in source, "source plateau anchor mismatch")
    require("(M_W)_{t,n}=w(n/N)n^{it}" in source, "source matrix anchor mismatch")
    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    identity = farey.get("averaged_actual_farey_bundle", {}).get("labeled_identity")
    theta_mass = farey.get("averaged_actual_farey_lower", {}).get("theta_mass_lower")
    require(identity == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "actual Farey label mismatch")
    require(theta_mass == "sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta >= (75/2)*H*v^(8-3*delta(v))", "Farey theta-mass anchor mismatch")
    phase = load_json(INPUTS["phase_flatness_artifact"][0])
    require(phase.get("actual_log_conditional_gate", {}).get("matrix") == "M_W(t,n)=w(n/L)n^(it) on the exact support L<n<2L", "phase matrix anchor mismatch")
    deletion = load_json(INPUTS["row_deletion_artifact"][0])
    require(deletion.get("row_deletion_leverage", {}).get("consequence") == "mu_top(W)>=DelCov(W)", "row-deletion consequence mismatch")
    return {
        "base_set": base["set"],
        "base_cardinality": base["cardinality"],
        "base_energy": base["energy_band"],
        "base_energy_definition": base["energy_definition"],
        "rationalmass_threshold": rational["threshold"],
        "common_object_rule": crr["witness_schema"]["common_object_rule"],
        "weight": conventions.SUPPORT_AND_PLATEAU["w"],
        "smoothing": f"{conventions.SUPPORT_AND_PLATEAU['psi1']}; {conventions.SUPPORT_AND_PLATEAU['psi2']}; normalized formulas give 0<=psi1,psi2<=1",
        "actual_farey_identity": identity,
        "rationalmass_theta_mass": theta_mass,
        "row_deletion_consequence": deletion["row_deletion_leverage"]["consequence"],
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_rfdi_outlier_surgery_v1")
    verified = conventions.verify_all()
    require(verified["large_v_mean_value_coarse_tail_at_v64"] == Fraction(81, 128), "mean-value tail mismatch")
    require(verified["outlier_windows"]["energy_increment"] == 4 * 64**8 - 3, "energy increment mismatch")
    require("C_v:=1+32" in verified["mean_value_rows"]["average_bound"], "mean-value formula mismatch")
    require("8*g^(-2)" in verified["spectral_surgery_rows"]["central_failure"], "central failure formula mismatch")
    return json_exact(verified)


def seal() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_rfdi_outlier_surgery_v1_for_seal")
    return {
        "artifact_id": "cycle-6-crr-rfdi-outlier-surgery-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDITIONAL_ACTUAL_LOG_FAREY_RFDI_OUTLIER_OBSTRUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves a conditional actual-log/Farey one-row surgery theorem. It does not construct its surplus/spectral core, refute RFDI, establish the full Base pointwise coefficient condition after surgery, prove an actual CRR witness, AFARI/FARI/CFARI/CRR-U, a cubic estimate, a density gain, a short-interval theorem, a saturation theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "exact row/Gram algebra, elementary integral and harmonic estimates, frozen source/convention anchors, rational scale bookkeeping, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "conditional_core": {
            "epistemic_status": "CONJECTURED",
            "geometry": "A has R-1 rows in [0,H/4], is H^(1/100)-separated, and has E(A) in [v^(20-delta(v)),v^(20+delta(v))-(4R-3)].",
            "spectral": "lambda_1(G_A)=Lambda, lambda_2(G_A)<=(1-g)Lambda, Lambda>=v^(12-ell*delta(v)), and S_L+sqrt(Lambda*S_L)<=g*Lambda/2 for fixed 0<g<=1.",
            "rationalmass_surplus": "On a rational set E of measure at least v^(-4-delta(v)), F_A>=(1+epsilon)*v^(12-2*delta(v)) for fixed epsilon>0.",
            "boundary": "No existence theorem for this core is supplied; it is an explicit conditional antecedent, not an actual counterexample to RFDI.",
        },
        "scalar_and_farey_preservation": {
            "epistemic_status": "PROVED_CONDITIONAL_ON_THE_CORE",
            "outlier_window": "tau is selected in [3H/4,H], so W=A union {tau} is one common actual row set.",
            "separation_cardinality_energy": "E(W)=E(A)+4R-3; the displayed core interior energy band gives the frozen Base separation/cardinality/energy predicates for W.",
            "rationalmass": "F_W(u)>=F_A(u)-2sqrt(2F_A(u)); if v^(12-2delta(v))>=max(2,8(1+epsilon)/epsilon^2), the same rational set E proves RationalMass(v) for W.",
            "farey": "The actual K_F feature identity and C_theta(sk,rk)=R_W((r/s)*exp(theta/H)) remain attached to this same W; no alias or row-set replacement is made.",
            "farey_rows": json_exact(conventions.farey_kernel_rows()),
        },
        "actual_log_outlier_selection": {
            "epistemic_status": "PROVED_CONDITIONAL_ON_THE_CORE",
            "coupling": "f(tau)=u_A^*G_(A,tau)=sqrt(Lambda)D_c(tau), where D_c(tau)=sum_(L<n<2L) conjugate(x_n)w(n/L)n^(-i*tau) and sum|c_n|^2<=1.",
            "elementary_average": "(1/|I|)integral_I|D_c(tau)|^2dtau<=C_v:=1+32L(1+log L)/H, so a tau in I has |f(tau)|^2<=Lambda*C_v.",
            "large_v_constant": "For v>=64, C_v<=2 by log(v)<=sqrt(v) and L/H=v^(-2).",
            "circularity_audit": "The time tau is selected from the fixed core eigenvector and actual M_A before inspecting G_W's top eigenvector, deletion statistic, phase rounding, or Farey outcome.",
        },
        "row_deletion_failure": {
            "epistemic_status": "PROVED_CONDITIONAL_ON_THE_CORE",
            "block_gap": "||B||<=Lambda-gLambda/2 in the [u_A] direct-sum complement decomposition of G_W.",
            "top_coordinate": "For every unit top eigenvector u_W, |(u_W)_tau|^2<=4C_v/(g^2Lambda).",
            "actual_deletion_bound": "DelCov(W)<=mu_top(W)<=4RC_v/(g^2Lambda).",
            "central_bound": "For v>=64 and Lambda>=v^(12-ell*delta(v)), DelCov(W)<=8g^(-2)v^(-4+ell*delta(v)).",
            "rfd_failure": "For any fixed g,ell,r,s with ell+r+2s<2, this is <v^(-2s*delta(v)) for all sufficiently large v, so the deletion half of RFDI_(s,kappa) fails independently of kappa and r.",
        },
        "structural_consequence": {
            "epistemic_status": "PROVED_CONDITIONAL_ON_THE_CORE",
            "statement": "A set-only RFDI proof cannot use only scalar/hereditary properties preserved by this surgery. It must exploit an all-row log/Farey mechanism, exclude the isolated-core configuration, or use the non-hereditary coefficient/pointwise portion of Base.",
            "not_a_no_go": "This does not say the full Base/RationalMass/PositiveCubic witness class admits the core, nor that RFDI is false.",
        },
        "falsifiers": {
            "energy": "A failure of the pair-sum class separation or of E(A union {tau})=E(A)+4R-3 refutes the scalar-preservation lemma.",
            "rationalmass": "A failure of the pinned smoothing positivity/support bound J<=2 or of the Cauchy estimate refutes the RationalMass-preservation lemma.",
            "actual_log": "A sign/orientation error in the expansion of f(tau), the integral/log-spacing bound, or the harmonic estimate refutes the actual-row selection lemma.",
            "spectral": "A block matrix satisfying the stated core gap and scale condition but violating the top-coordinate or DelCov bound refutes the spectral surgery lemma.",
            "scope": "An actual proof that no core meets the listed antecedents changes the research route but does not refute this conditional theorem.",
        },
        "exact_replay": exact_rows(),
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_rfdi_outlier_surgery_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite RFDI outlier surgery artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "RFDI outlier surgery artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "RFDI outlier surgery artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
