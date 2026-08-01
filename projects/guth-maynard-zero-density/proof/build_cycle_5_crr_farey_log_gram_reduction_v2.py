#!/usr/bin/env python3
"""Seal the Cycle 5 averaged-jitter actual-Farey/log-Gram reduction v2."""
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
OUTPUT = ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json"
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
    "farey_log_v1_artifact": (
        ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json",
        "8f204d56a5609fa9c8a93b152a969a038bc13463d3a36ca746e842bfe21e5f40",
    ),
    "farey_log_v1_document": (
        ROOT / "docs/cycle-5-crr-farey-log-gram-reduction-v1.md",
        "c5d89a3c5e5a7871919fbe8dbdc6aa0f17ba7973883774c14e0039cb3327223e",
    ),
    "farey_log_v1_conventions": (
        ROOT / "conventions/crr_farey_log_gram_v1.py",
        "d2301a36dd25cd73702a9e5220c2ad5e3c5d820444d6775f0aeea3d9a4783d73",
    ),
    "farey_log_v1_builder": (
        ROOT / "proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py",
        "9f00151ad1d7d51c6cd68715669c94b8e81978cac98088246a37922644e05539",
    ),
    "farey_log_v1_tests": (
        ROOT / "tests/test_cycle_5_crr_farey_log_gram_reduction_v1.py",
        "93cadfec064e9fd60ca172a9031b4675c61c32e53ece88fa4b0326296c1b3133",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
    "document": (
        ROOT / "docs/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.md",
        "a2cf217d616feab889e48783b477454038c60ca006afb6775126532167f972f2",
    ),
    "conventions": (
        ROOT / "conventions/crr_farey_log_gram_v2.py",
        "25aa0b8642f09a8d9b1752de870105764204470db05a241e9359c0d1a46c7f9a",
    ),
}
SOURCE_FRAGMENTS = (
    "R(v):=\\sum_{t\\in W}|v|^{it}",
    "\\begin{lmm}[$L^2$ bound] \\label{RL2}",
    "\\int_{v \\asymp 1} |R(v)|^2 dv \\ll_\\epsilon |W|",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def affine_text(value: tuple[Fraction, Fraction]) -> str:
    constant, delta_coefficient = value
    constant_text = fraction_text(constant)
    if delta_coefficient == 0:
        return constant_text
    sign = "+" if delta_coefficient > 0 else "-"
    return f"{constant_text}{sign}{fraction_text(abs(delta_coefficient))}*delta"


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
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load averaged-jitter conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "averaged-jitter v2 requires non-optimized CPython 3.12.3")
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
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "CRR Base separation mismatch")
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "CRR Base cardinality mismatch")
    require(base.get("polynomial") == "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)", "CRR Base coefficient convention mismatch")
    require(
        rational.get("rational_net") == "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, intervals of radius 1/(100H)",
        "actual CRR rational-net convention mismatch",
    )
    require(
        rational.get("threshold") == "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))",
        "CRR RationalMass threshold mismatch",
    )

    v1 = load_json(INPUTS["farey_log_v1_artifact"][0])
    require(v1.get("artifact_id") == "cycle-5-crr-farey-log-gram-reduction-v1", "v1 Farey-log identity mismatch")
    require(v1.get("forced_bundle_lower", {}).get("epistemic_status") == "PROVED", "v1 bundle status mismatch")
    require(
        v1.get("multiplicative_ray_cross_gram", {}).get("labeled_entry_identity")
        == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))",
        "v1 labeled cross-Gram identity mismatch",
    )
    require(v1.get("fari_target", {}).get("epistemic_status") == "CONJECTURED", "v1 FARI status mismatch")
    return {
        "gm_rl2_label": "RL2",
        "gm_rl2_source_lines": "1242-1243",
        "base_set": base["set"],
        "base_cardinality": base["cardinality"],
        "rational_net": rational["rational_net"],
        "rationalmass_threshold": rational["threshold"],
        "preserved_v1_identity": v1["multiplicative_ray_cross_gram"]["labeled_entry_identity"],
        "preserved_v1_fari_status": v1["fari_target"]["epistemic_status"],
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_conventions()
    verified = conventions.verify_all()
    exponents = {key: affine_text(value) for key, value in conventions.exponent_rows().items()}
    expected_exponents = {
        "rationalmass_integral_over_cells": "8-3*delta",
        "raw_actual_farey_l2_cell_sum_lower": "8-3*delta",
        "theta_parameter_mass_lower": "20-3*delta",
        "averaged_actual_farey_bundle_lower": "26-3*delta",
        "raw_rl2_global_upper_under_base": "26+1*delta",
    }
    require(exponents == expected_exponents, "averaged-jitter exponent rows mismatch")
    geometry = verified["geometry"]
    rays = verified["rays"]
    constants = verified["constants"]
    require(geometry["expanded_cell_diameter"] < geometry["reduced_fraction_gap_lower"], "expanded-cell gap mismatch")
    require(geometry["theta_neighborhood_diameter"] < geometry["reduced_fraction_gap_lower"], "theta-neighborhood gap mismatch")
    require(constants["averaged_bundle_prefactor"] == Fraction(15, 8), "averaged lower constant mismatch")
    require(rays["integer_k_count_lower"] == Fraction(8**6, 20), "ray lower count mismatch")
    require(rays["integer_k_count_upper"] == 2 * 8**6, "ray upper count mismatch")
    return {
        "scales_at_v8": json_exact(verified["scales"]),
        "averaged_geometry_at_v8": json_exact(geometry),
        "ray_rows_at_v8": json_exact(rays),
        "averaged_lower_constants": json_exact(constants),
        "exponent_rows": exponents,
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter",
        "epistemic_status": "PROVED",
        "status": "SEALED_AVERAGED_JITTER_EXTENSION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves, conditional on frozen RationalMass/Base predicates and the checked published raw-R L2 lemma, an averaged actual-Farey lower bound and the matching uncoupled global-L2 upper scale. It proves neither AFARI nor v1 FARI, CRR-U, a compatible witness, a cubic estimate, a density gain, a short-interval theorem, a full-method saturation theorem, or an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "preserves_v1": {
            "epistemic_status": "PROVED",
            "statement": "v1 is retained as an immutable, hash-pinned supremum-over-jitter reduction; v2 adds a distinct averaged statistic.",
            "v1_artifact_id": "cycle-5-crr-farey-log-gram-reduction-v1",
            "v1_artifact_sha256": INPUTS["farey_log_v1_artifact"][1],
        },
        "research_stage_review_policy": {
            "lightweight_checks": "primary-source anchor, exact Fraction/integer geometry, labeled matrix identities inherited from v1, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "source_context": context,
        "averaged_actual_farey_bundle": {
            "epistemic_status": "PROVED",
            "definition": "A_v(W)=sum_(r,s in F_Q) integral_(-3)^3 sum_(k in K_(r,s)) |C_theta(sk,rk)|^2 dtheta",
            "labeled_identity": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))",
            "actual_nodes": "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4; no generic logarithmic-alias substitution",
            "jitter": "theta is integrated over [-3,3], not optimized cell-by-cell",
            "entry_injectivity": "(r,s,k)->(sk,rk) is injective for reduced positive r/s",
        },
        "averaged_actual_farey_lower": {
            "epistemic_status": "PROVED",
            "conditional_on": "the CRR-v2 RationalMass(v) predicate for v>=8",
            "expanded_cells": "J_(r,s)^+=[r/s-101/(100H),r/s+101/(100H)] are pairwise disjoint",
            "smoothing_incidence_upper": "H*measure({u in union J_(r,s): |u-u'|<=1/H})<=2/100",
            "raw_actual_farey_l2_sum_lower": "sum_(r,s) integral_(J_(r,s)^+) |R_W(u)|^2 du >= 50*v^(8-3*delta(v))",
            "theta_cover": "J_(r,s)^+ subset {(r/s)*exp(theta/H): |theta|<=3}",
            "theta_mass_lower": "sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta >= (75/2)*H*v^(8-3*delta(v))",
            "ray_multiplicity_lower": "#K_(r,s)>=L/(20Q)=v^6/20",
            "lower_bound": "A_v(W)>=(15/8)*v^(26-3*delta(v))",
            "exponent_derivation": "(8-3delta)+12+6=26-3delta",
        },
        "raw_rl2_global_upper": {
            "epistemic_status": "PROVED",
            "conditional_on": "the CRR-v2 Base(v) separation/cardinality conditions and source Lemma RL2",
            "source_anchor": "LargevaluesDirichlet17.tex, Lemma RL2, lines 1242-1243 in the pinned source",
            "hypotheses_checked": "W is H^(1/100)-separated and contained in an interval of length H",
            "theta_neighborhoods": "{(r/s)*exp(theta/H): |theta|<=3} lie in disjoint [r/s-8/H,r/s+8/H] subsets of [1/2,3/2]",
            "raw_parameter_bound": "sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta << H*|W|",
            "ray_multiplicity_upper": "#K_(r,s)<=9L/(5Q)<=2L/Q",
            "global_bound": "A_v(W) << (L/Q)*H*|W| << v^(26+delta(v))=v^(26+o(1))",
            "exponent_derivation": "12+6+(8+delta)=26+delta",
        },
        "uncoupled_global_l2_saturation": {
            "epistemic_status": "PROVED",
            "statement": "The RationalMass lower route gives central exponent 26-3delta, while raw RL2 plus Base cardinality gives 26+delta; their displayed exponent gap is 4delta=o(1).",
            "scope": "This isolates the critical saturation of the uncoupled global-RL2 step after the Base coefficient vector is discarded except for |W|.",
            "required_new_information_for_fixed_power_gain": "A fixed power saving cannot come from the displayed raw global RL2/cardinality estimate alone; a proof must use Base/coefficient coupling or a stronger arithmetic/restricted-L2 input.",
            "not_a_no_go": "This is not a proof that AFARI, v1 FARI, or another method lacks a fixed power gain, and not a full-method saturation theorem.",
        },
        "afari_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "For some fixed eta>0 and all sufficiently large v, every H^(1/100)-separated Base-admissible W satisfies A_v(W)<=v^(26-eta).",
            "not_claimed": "No proof or disproof of AFARI_eta is supplied. The v^(26+o(1)) raw-RL2 bound is not AFARI_eta.",
        },
        "conditional_incompatibility_reduction": {
            "epistemic_status": "PROVED",
            "conditional_on": "AFARI_eta for any fixed eta>0",
            "conclusion": "For sufficiently large v with 3*delta(v)<eta, RationalMass(v) and Base(v) cannot hold together; hence AFARI_eta implies CRR-U.",
            "scope": "PositiveCubic(v) is not needed for this conditional contradiction; this does not prove AFARI_eta, v1 FARI_eta, or CRR-U.",
        },
        "falsifiers": {
            "lower_reduction": "A failure of expanded-cell disjointness, the smoothing-incidence estimate, the theta cover/Jacobian bound, the ray lower count, or the inherited labeled identity refutes the stated lower reduction.",
            "raw_rl2_route": "A failure of the source RL2 hypotheses, theta-neighborhood disjointness, or ray upper count refutes the stated global upper route.",
            "afari": "An asymptotic Base-plus-RationalMass family meeting the lower scale refutes every AFARI_eta that applies to it.",
        },
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v2.py --write",
            "check_command": "python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v2.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_5_crr_farey_log_gram_reduction_v2.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite averaged-jitter v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "averaged-jitter v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "averaged-jitter v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
