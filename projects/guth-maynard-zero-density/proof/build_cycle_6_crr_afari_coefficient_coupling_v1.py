#!/usr/bin/env python3
"""Seal the Cycle 6 CRR coefficient--Farey coupling reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json"
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
    "farey_log_v2_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json",
        "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8",
    ),
    "farey_log_v2_conventions": (
        ROOT / "conventions/crr_farey_log_gram_v2.py",
        "25aa0b8642f09a8d9b1752de870105764204470db05a241e9359c0d1a46c7f9a",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
    "document": (
        ROOT / "docs/cycle-6-crr-afari-coefficient-coupling-v1.md",
        "5ed3d0d2c17e0e0766704e59c58d5a013f80a26243d13b8ff96fe6c63d54f9fe",
    ),
    "conventions": (
        ROOT / "conventions/crr_afari_coupling_v1.py",
        "8d74815084b859a985de90cd1429bab734269f7373794dd81c5515fad49b6bbf",
    ),
    "tests": (
        ROOT / "tests/test_cycle_6_crr_afari_coefficient_coupling_v1.py",
        "8e29c1a50b69c9e9574578e24f8a5cefa4c1862801efd35d1b0debdffe74bdb7",
    ),
}
SOURCE_FRAGMENTS = (
    "R(v):=\\sum_{t\\in W}|v|^{it}",
    "\\label{RL4}",
    "|R(v)|^4 dv \\lessapprox E(W).",
    "(M_W)_{t,n}=w(n/N)n^{it}",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def affine_text(value: tuple[Fraction, Fraction]) -> str:
    constant, slack = value
    constant_text = fraction_text(constant)
    if slack == 0:
        return constant_text
    sign = "+" if slack > 0 else "-"
    return f"{constant_text}{sign}{fraction_text(abs(slack))}*delta"


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
    spec = importlib.util.spec_from_file_location("crr_afari_coupling_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load CRR AFARI coupling conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "CRR AFARI coupling v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}
    return frozen


def validate_context() -> dict[str, Any]:
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source, f"GM source fragment missing: {fragment}")

    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    rational = crr.get("witness_schema", {}).get("rational_mass", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base set convention mismatch")
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "Base cardinality convention mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "Base pointwise convention mismatch")
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "Base energy convention mismatch")
    require(base.get("polynomial") == "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)", "Base polynomial convention mismatch")
    require(
        rational.get("rational_net") == "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, intervals of radius 1/(100H)",
        "actual CRR rational-net convention mismatch",
    )

    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    require(
        farey.get("artifact_id") == "cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter",
        "averaged Farey artifact identity mismatch",
    )
    lower = farey.get("averaged_actual_farey_lower", {})
    upper = farey.get("raw_rl2_global_upper", {})
    require(lower.get("lower_bound") == "A_v(W)>=(15/8)*v^(26-3*delta(v))", "averaged lower convention mismatch")
    require(lower.get("ray_multiplicity_lower") == "#K_(r,s)>=L/(20Q)=v^6/20", "Farey ray lower convention mismatch")
    require(upper.get("ray_multiplicity_upper") == "#K_(r,s)<=9L/(5Q)<=2L/Q", "Farey ray upper convention mismatch")
    return {
        "base_set": base["set"],
        "base_cardinality": base["cardinality"],
        "base_pointwise": base["pointwise"],
        "base_energy_band": base["energy_band"],
        "base_polynomial": base["polynomial"],
        "actual_rational_net": rational["rational_net"],
        "gm_rl4_anchor": "LargevaluesDirichlet17.tex, Lemma RL4, lines 1267-1305 in the pinned source",
        "v2_averaged_lower": lower["lower_bound"],
        "v2_ray_comparison": "L/(20Q)<=#K_(r,s)<=2L/Q",
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_conventions()
    verified = conventions.verify_all()
    exponents = {key: affine_text(value) for key, value in conventions.exponent_rows().items()}
    expected_exponents = {
        "base_energy_upper": "20+1*delta",
        "energy_cauchy_theta_mass_upper_base_slack_only": "20+1/2*delta",
        "energy_cauchy_ray_bundle_upper_base_slack_only": "26+1/2*delta",
        "rationalmass_theta_mass_lower": "20-3*delta",
        "rationalmass_local_l2_lower": "8-3*delta",
        "rationalmass_local_l4_lower": "20-6*delta",
        "base_phase_rayleigh_lower": "20-4*delta",
        "base_rationalmass_phase_farey_product_lower": "40-7*delta",
        "scalar_envelope_local_l4": "20",
        "scalar_envelope_theta_mass": "20",
        "scalar_envelope_ray_bundle": "26",
    }
    require(exponents == expected_exponents, "CRR AFARI coupling exponent rows mismatch")
    windows = verified["farey_windows"]
    rays = verified["rays"]
    localization = verified["rationalmass_localization"]
    scalar = verified["scalar_envelope"]
    phase = verified["coefficient_phase"]
    require(windows["union_measure_lower"] == Fraction(1, 50 * 8**4), "Farey union lower measure mismatch")
    require(windows["union_measure_upper"] == Fraction(16, 8**4), "Farey union upper measure mismatch")
    require(rays["ray_weight_lower"] == Fraction(8**6, 20), "Farey ray lower mismatch")
    require(rays["ray_weight_upper"] == 2 * 8**6, "Farey ray upper mismatch")
    require(localization["local_l4_lower_from_cauchy"] == Fraction(225, 16384), "local fourth-moment constant mismatch")
    require(scalar["integral_f_star_squared"] == 8**20, "scalar envelope L4 calibration mismatch")
    require(phase["rayleigh_lower"] == "a^*(M_W M_W^*)a>=v^(20-4*delta(v))", "Base phase bridge mismatch")
    return {
        "scales_at_v8": json_exact(verified["scales"]),
        "farey_windows_at_v8": json_exact(windows),
        "ray_comparison_at_v8": json_exact(rays),
        "rationalmass_localization_constants": json_exact(localization),
        "scalar_envelope_at_v8": json_exact(scalar),
        "coefficient_phase_at_v8": json_exact(phase),
        "exponent_rows": exponents,
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-6-crr-afari-coefficient-coupling-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_COEFFICIENT_FAREY_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves an actual-Farey energy/fourth-moment saturation reduction, a scalar-envelope calibration, and the exact common-coefficient phase bridge. It proves neither F4F_eta, AFARI_eta, CFARI_eta, CRR-U, a compatible witness, a cubic estimate, a density gain, a short-interval theorem, a full-method saturation theorem, or an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {
            "lightweight_checks": "primary-source anchors, exact Fraction/integer scale bookkeeping, labeled PSD kernel algebra, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "source_context": context,
        "actual_farey_kernel": {
            "epistemic_status": "PROVED",
            "actual_labels": "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4; each retains its reduced (r,s) label",
            "theta_windows": "I_(r,s)={(r/s)*exp(theta/H): |theta|<=3}",
            "unweighted_kernel": "(K_F)_(t,t')=sum_(r,s in F_Q) integral_(-3)^3 ((r/s)*exp(theta/H))^(i(t-t')) dtheta",
            "positive_semidefinite_reason": "K_F is an integral/sum of rank-one exponential kernels",
            "theta_mass_identity": "1^*K_F*1=Mcal_v(W)=sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta",
            "ray_kernel_comparison": "(L/(20Q))*K_F <= K_F^ray <= (2L/Q)*K_F",
            "bundle_comparison": "(L/(20Q))*Mcal_v(W)<=A_v(W)<=(2L/Q)*Mcal_v(W)",
            "farey_union_measure": "(1/50)v^-4<=|U_v|<=16v^-4",
        },
        "energy_restricted_upper": {
            "epistemic_status": "PROVED",
            "conditional_on": "Base(v) separation/energy hypotheses and the checked GM raw-R Lemma RL4",
            "jacobian_identity": "Mcal_v(W)=H*integral_(U_v)|R_W(u)|^2 du/u",
            "cauchy_bound": "Mcal_v(W)<=8Q*H^(1/2)*(integral_(1/2)^(3/2)|R_W(u)|^4du)^(1/2)",
            "source_bound": "integral_(1/2)^(3/2)|R_W(u)|^4du<=H^(o(1))*E(W)",
            "bundle_bound": "A_v(W)<<H^(o(1))*L*H^(1/2)*E(W)^(1/2)<=v^(26+o(1))",
            "explicit_base_slack_only": "26+(1/2)*delta(v); the published RL4 subpower factor remains",
            "scope": "This uses actual Farey windows and Base energy, but it is not AFARI_eta.",
        },
        "rationalmass_localization": {
            "epistemic_status": "PROVED",
            "conditional_on": "the v2 RationalMass(v) predicate and its sealed averaged bundle lower bound",
            "theta_mass_lower": "Mcal_v(W)>=(15/16)*v^(20-3*delta(v))",
            "local_l2_lower": "integral_(U_v)|R_W(u)|^2du>=(15/32)*v^(8-3*delta(v))",
            "local_l4_lower": "integral_(U_v)|R_W(u)|^4du>=(225/16384)*v^(20-6*delta(v))",
            "conclusion": "The global RL4/Base-energy upper scale and RationalMass-forced local L4 lower scale both have central exponent 20.",
            "no_go_scope": "No fixed power can arise from the displayed scalar global-fourth-moment, Farey-window-measure, and Cauchy route alone.",
        },
        "scalar_envelope_calibration": {
            "epistemic_status": "PROVED",
            "function": "f_star(u)=v^10*|U_v|^(-1/2)*1_(U_v)(u)",
            "exact_moment": "integral_(U_v)f_star(u)^2du=v^20",
            "critical_scales": "integral_(U_v)f_star(u)du asymp v^8; H*integral_(U_v)f_star(u)du/u asymp v^20; ray-weighted scale asymp v^26",
            "scope_limit": "f_star is not claimed to be |R_W|^2 for any W and has no Base coefficient vector. It proves sharpness only for scalar support/measure/fourth-moment bookkeeping.",
        },
        "coefficient_phase_bridge": {
            "epistemic_status": "PROVED",
            "conditional_on": "one common Base(v) pair (b,W)",
            "phase": "a_t=D_v(t)/|D_v(t)| with D_v|_W=M_Wb",
            "phase_identity": "sum_t conjugate(a_t)D_v(t)=sum_t|D_v(t)|>=v^(15-2*delta(v))",
            "rayleigh_lower": "a^*(M_W*M_W^*)a=||M_W^*a||_2^2>=v^(20-4*delta(v))",
            "derivation": "Cauchy against b and ||b||_2^2<=L; no separately chosen coefficient vector or row set occurs.",
        },
        "f4f_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "For some fixed eta>0 and all sufficiently large v, every Base(v)-admissible W has integral_(U_v)|R_W(u)|^4du<=v^(20-eta).",
            "conditional_effect": "F4F_eta implies a fixed-power AFARI after Cauchy/ray comparison and contradicts RationalMass at large v.",
            "not_claimed": "No proof or disproof of F4F_eta is supplied.",
        },
        "cfari_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "For some fixed eta>0 and all sufficiently large v, every common Base(v) pair (b,W), with a_t=D_v(t)/|D_v(t)|, satisfies (a^*(M_W*M_W^*)a)*(1^*K_F*1)<=v^(40-eta).",
            "meaning": "A phase-sensitive mixed-kernel anti-alignment inequality on the same W, coefficient vector, and actual reduced Farey labels.",
            "not_claimed": "No proof or disproof of CFARI_eta is supplied.",
        },
        "conditional_implication": {
            "epistemic_status": "PROVED",
            "conditional_on": "CFARI_eta for any fixed eta>0",
            "derivation": "phase Rayleigh lower v^(20-4delta) gives Mcal_v(W)<=v^(20-eta+4delta), then A_v(W)<=2v^(26-eta+4delta)",
            "conclusion": "For all sufficiently large v, CFARI_eta implies AFARI_(eta/2), hence CRR-U through the sealed v2 averaged-jitter reduction.",
            "rationalmass_falsifier": "Base(v)+RationalMass(v) forces (a^*(M_W*M_W^*)a)*(1^*K_F*1)>=(15/16)*v^(40-7delta(v)); an asymptotic common witness refutes every covering CFARI_eta.",
        },
        "falsifiers": {
            "kernel_reduction": "Failure of actual theta-window disjointness, the exact change of variables, labeled ray comparison, or PSD kernel identity refutes the proved reduction.",
            "energy_route": "Failure of the checked RL4 hypotheses/source conclusion or of the Base energy bound refutes the stated energy-restricted upper route.",
            "cfari": "An asymptotic common Base-plus-RationalMass family refutes every CFARI_eta that covers it.",
            "scope": "The scalar f_star calibration is not an AFARI counterexample; it can be refuted as a scalar calibration only by an error in its exact measure/moment arithmetic.",
        },
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_afari_coefficient_coupling_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite coefficient-Farey v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "coefficient-Farey v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "coefficient-Farey v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
