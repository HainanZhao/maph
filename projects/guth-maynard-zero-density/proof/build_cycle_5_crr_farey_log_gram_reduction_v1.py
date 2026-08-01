#!/usr/bin/env python3
"""Seal the Cycle 5 actual-Farey/log-Gram CRR reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json"
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
    "montgomery_reduction": (
        ROOT / "artifacts/cycle-4-crr-montgomery-reduction-v1.json",
        "5d0b5b14df5e6aed5fd28dc1094c36a0b6c6de83da2605a75cbd5d9163154190",
    ),
    "generic_alias_barrier": (
        ROOT / "artifacts/cycle-4-crr-alias-model-barrier-v1.json",
        "be9422f9afaa179129f5c46a21ae71220d38545c70ef43c3f293d43e6745b80d",
    ),
    "finite_probe_correction": (
        ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1.json",
        "3aedf729001c3d91810035d3d8c30d41540f9c12d077534edcb8a7d4cbbde686",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
    "document": (
        ROOT / "docs/cycle-5-crr-farey-log-gram-reduction-v1.md",
        "c5d89a3c5e5a7871919fbe8dbdc6aa0f17ba7973883774c14e0039cb3327223e",
    ),
    "conventions": (
        ROOT / "conventions/crr_farey_log_gram_v1.py",
        "d2301a36dd25cd73702a9e5220c2ad5e3c5d820444d6775f0aeea3d9a4783d73",
    ),
}
SOURCE_FRAGMENTS = (
    "(M_W)_{t,n}=w(n/N)n^{it}",
    "R(v):=\\sum_{t\\in W}|v|^{it}",
    "If $U$ is the $1/T$-neighborhood of the set of rational numbers $r/s$",
    "the set of these values is highly concentrated on rationals with numerator and denominator of size $T_1^{1/3}$",
    "\\label{propsumaff}",
    "\\label{eq:RtDef}",
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


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Farey-log conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "Farey-log Gram reduction v1 requires non-optimized CPython 3.12.3")
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
    rational = crr.get("witness_schema", {}).get("rational_mass", {})
    base = crr.get("witness_schema", {}).get("base", {})
    require(
        rational.get("rational_net") == "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, intervals of radius 1/(100H)",
        "actual CRR rational-net convention mismatch",
    )
    require(
        rational.get("threshold") == "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))",
        "CRR RationalMass threshold mismatch",
    )
    require(base.get("polynomial") == "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)", "Base coefficient matrix convention mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "Base pointwise convention mismatch")

    montgomery = load_json(INPUTS["montgomery_reduction"][0])
    require(montgomery.get("fixed_sigma_reduction", {}).get("epistemic_status") == "PROVED", "Montgomery reduction status mismatch")
    alias = load_json(INPUTS["generic_alias_barrier"][0])
    exclusions = alias.get("scope_exclusions", [])
    require(any("Farey nodes" in item for item in exclusions), "alias barrier must exclude actual Farey nodes")
    finite = load_json(INPUTS["finite_probe_correction"][0])
    require(finite.get("artifact_id") == "cycle-4-p1r-crr-finite-probe-v3-replay-metadata-correction-v1", "finite-probe correction identity mismatch")
    return {
        "crr_v2_status": crr.get("status"),
        "montgomery_scope": montgomery.get("claim_boundary"),
        "alias_exclusion": next(item for item in exclusions if "Farey nodes" in item),
        "finite_probe_scope": finite.get("claim_boundary"),
    }


def exact_rows() -> dict[str, Any]:
    c = load_conventions()
    verified = c.verify_all()
    exponent_rows = {key: affine_text(value) for key, value in c.exponent_rows().items()}
    expected_exponents = {
        "activated_actual_farey_cells": "8-1*delta",
        "jittered_raw_amplitude": "6-1*delta",
        "jittered_raw_square": "12-2*delta",
        "plateau_ray_multiplicity": "6",
        "farey_log_gram_bundle_lower": "26-3*delta",
        "base_coefficient_spectral_lambda_lower": "12-3*delta",
    }
    require(exponent_rows == expected_exponents, "Farey-log exponent rows mismatch")
    cells = verified["cells"]
    rays = verified["rays"]
    jitter = verified["jitter"]
    require(cells["central_farey_count_lower"] == Fraction(cells["Q"] * cells["Q"], 200), "central Farey count mismatch")
    require(cells["all_cells_measure_scale"] == Fraction(1, cells["Q"]), "Farey cover measure mismatch")
    require(rays["integer_k_count_lower"] == Fraction(verified["scales"]["v"] ** 6, 20), "ray count mismatch")
    require(jitter["jitter_log_radius"] == 3, "jitter radius mismatch")
    return {
        "scales_at_v8": verified["scales"],
        "actual_farey_cells_at_v8": {
            key: fraction_text(value) if isinstance(value, Fraction) else value for key, value in cells.items()
        },
        "plateau_rays_at_v8": {
            key: fraction_text(value) if isinstance(value, Fraction) else value for key, value in rays.items()
        },
        "jitter_constants": {
            key: fraction_text(value) if isinstance(value, Fraction) else value for key, value in jitter.items()
        },
        "farey_union_bound_certificate": {
            key: fraction_text(value) if isinstance(value, Fraction) else value
            for key, value in verified["certificate"].items()
        },
        "exponent_rows": exponent_rows,
        "affine_factorization": verified["affine"],
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-5-crr-farey-log-gram-reduction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_FAREY_LOG_GRAM_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves an exact actual-Farey cell/jittered-node/multiplicative-ray reduction and a conditional FARI implication. It proves neither FARI nor CRR-U, and gives no witness, cubic lower bound, density estimate, prime-interval theorem, saturation theorem, or L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {
            "lightweight_checks": "source anchors, exact Fraction/integer geometry, labeled matrix algebra, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": context,
        "actual_farey_geometry": {
            "epistemic_status": "PROVED",
            "net": "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, with radius-1/(100H) cells",
            "reduced_center_gap_lower": "1/(4Q^2)",
            "cells_disjoint_at_frozen_scales": True,
            "central_count_lower": "#F_Q >= Q^2/200 for Q>=4096",
            "cover_measure_scale": "Q^2/H=Q^-1=v^-4",
            "scope": "actual reduced fractions only; no logarithmic alias substitution",
        },
        "rationalmass_to_jittered_farey_lift": {
            "epistemic_status": "PROVED",
            "conditional_on": "the CRR-v2 RationalMass(v) predicate for v>=8",
            "activated_fraction_count_lower": "50*v^(8-delta(v))",
            "raw_node_form": "x_(r,s)=(r/s)*exp(theta_(r,s)/H)",
            "theta_range": "|theta_(r,s)|<3",
            "raw_amplitude_lower": "2^(-1/2)*v^(6-delta(v))",
            "selection_note": "The jitter is retained; positive smoothing alone does not center x_(r,s) at r/s.",
        },
        "multiplicative_ray_cross_gram": {
            "epistemic_status": "PROVED",
            "measurement_matrix": "M_W(t,n)=w(n/L)n^(it)",
            "row_modulation": "P_theta(t,t)=exp(i*theta*t/H)",
            "cross_gram": "C_theta=M_W^* P_theta M_W",
            "ray": "K_(r,s)={k>0: 6L/5<=rk,sk<=9L/5}",
            "ray_count_lower": "#K_(r,s)>=L/(20Q)=v^6/20",
            "labeled_entry_identity": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))",
            "entry_injectivity": "(r,s,k)->(sk,rk) is injective for reduced positive r/s",
        },
        "forced_bundle_lower": {
            "epistemic_status": "PROVED",
            "conditional_on": "RationalMass(v)",
            "definition": "B_v(W)=sum_(r,s in F_Q) sup_(|theta|<=3) sum_(k in K_(r,s)) |C_theta(sk,rk)|^2",
            "lower_bound": "B_v(W)>=(5/4)*v^(26-3*delta(v))",
            "exponent_derivation": "(8-delta)+(12-2delta)+6=26-3delta",
            "does_not_use": ["generic spacing", "additive-energy upper bound", "positive cubic sign or size"],
        },
        "base_coefficient_coupling": {
            "epistemic_status": "PROVED",
            "conditional_on": "the CRR-v2 Base(v) predicate for the same W and b",
            "identity": "D_v|_W=M_W b",
            "coefficient_norm": "||b||_2^2<=L on the nonzero support of w",
            "spectral_lower": "lambda_max(M_W M_W^*)>=v^(12-3*delta(v))",
            "derivation": "|W|*v^(14-2delta)/L >= v^(12-3delta)",
            "common_object_rule": "The bundle and spectral lower bound use the same measurement matrix M_W; they are not separately optimized models.",
        },
        "fari_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "For some fixed eta>0 and all sufficiently large v, every H^(1/100)-separated Base-admissible W satisfies B_v(W)<=v^(26-eta).",
            "arithmetic_content": "actual reduced Farey nodes, bounded archimedean jitter, multiplicative rays, and one common Dirichlet measurement matrix",
            "not_claimed": "No proof or disproof of this restricted inverse inequality is supplied.",
        },
        "conditional_incompatibility_reduction": {
            "epistemic_status": "PROVED",
            "conditional_on": "FARI_eta for any fixed eta>0",
            "conclusion": "For sufficiently large v with 3*delta(v)<eta, Base(v) and RationalMass(v) cannot hold together; hence FARI_eta implies CRR-U.",
            "scope": "PositiveCubic(v) is not needed for this conditional contradiction; this does not prove FARI_eta or CRR-U.",
        },
        "source_affine_scale_relation": {
            "epistemic_status": "PROVED",
            "identity": "(d*(r/(d*e))+m2)/m3=(r+e*m2)/(e*m3)",
            "critical_scale": "Q=M^2, so d,e,m2,m3 asymp M and r asymp Q produce numerator and denominator asymp Q",
            "scope_limit": "This is dyadic scale compatibility only; it neither preserves the exact [Q,2Q] shell/coprimality nor proves a CRR configuration.",
        },
        "distinctions_from_prior_work": {
            "generic_alias_barrier": "The pinned alias barrier excludes actual Farey nodes; its generic no-go is not invoked here.",
            "finite_probe": "The equal-weight finite surrogate did not test this continuous cross-Gram/FARI condition and supplies no universal negative.",
            "montgomery": "The pinned Montgomery reduction remains conditional on a separate large-values conjecture; this artifact supplies an unconditional algebraic reduction to a different, explicitly CONJECTURED inequality.",
        },
        "falsifiers": {
            "reduction": "A failure of Farey-cell disjointness, the smoothing selector, the plateau-ray count, or the labeled cross-Gram identity would refute the proved reduction.",
            "fari": "An asymptotic Base-plus-RationalMass family satisfying the forced bundle lower bound refutes every FARI_eta that covers it.",
        },
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py --write",
            "check_command": "python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_5_crr_farey_log_gram_reduction_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Farey-log Gram reduction v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Farey-log Gram reduction v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Farey-log Gram reduction v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
