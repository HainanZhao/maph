#!/usr/bin/env python3
"""Seal the analytic-only Cycle 4 P1R-CRR-U formalization."""
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
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "p1r_preregistration_v4": (ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json", "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9"),
    "formalization_document": (ROOT / "docs/cycle-4-p1r-crr-u-formalization-v1.md", "b0aaf464540f9c41eb8414dc38d7be4a7680c0ac1148eadf0a6a61f4836471ed"),
    "conventions": (ROOT / "conventions/crr_formalization_v1.py", "eb0ee6e84bdfa3b87f5fffdc2901192db1b75b700a3d9621b10c670458ffd42b"),
    "gm_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
}
SOURCE_FRAGMENTS = (
    "Throughout the rest of the paper we fix a smooth function $w",
    "\\label{eq:DNDef}",
    "\\label{eq:htDef}",
    "\\label{lmm:TraceExpansion}",
    "\\label{eq:RDef}",
    "\\label{eq:RtDef}",
    "\\label{propsumaff}",
    "There are two key examples which correspond to the two terms",
    "\\label{eq:EnergyDef}",
    "\\label{prp:energybound}",
    "\\label{prpstn:S3}",
    "the set of these values is highly concentrated on rationals",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_formalization_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load CRR conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "CRR-U formalization v1 requires non-optimized CPython 3.12.3")
    return runtime


def render_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    prior = load_json(INPUTS["p1r_preregistration_v4"][0])
    require(prior.get("artifact_id") == "cycle-4-p1r-preregistration-v4", "v4 identity mismatch")
    require(prior.get("discovery_authorization") == "PROHIBITED_PENDING_CRR_FORMALIZATION", "v4 search prohibition mismatch")
    require(prior.get("p1r_crr", {}).get("formalization_gate", {}).get("search_authorized") is False, "v4 CRR gate mismatch")

    tex = INPUTS["gm_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in tex, f"GM source fragment missing: {fragment}")

    c = load_conventions()
    exact = c.exact_scale_checks()
    exact_strings = {key: [render_fraction(x) for x in values] for key, values in exact.items()}
    require(exact_strings == {"large_values": ["6", "8", "8"], "energy": ["20", "20", "20"], "s3": ["36", "36", "36", "36"], "rational_moments": ["8", "20"], "affine": ["28", "28"]}, "exact convention output mismatch")

    return {
        "artifact_id": "cycle-4-p1r-crr-u-formalization-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_ANALYTIC_FORMALIZATION",
        "claim_boundary": "This artifact defines the CONJECTURED CRR-U universal-incompatibility target. It proves only exact source-bound exponent compatibility and formal integrity; it proves no incompatibility, construction, density estimate, short-interval theorem, or method saturation.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "historical_replay": {"current_plan_read": False, "current_plan_eligibility": "EXCLUDED_FROM_HISTORICAL_ARTIFACT"},
        "source_status": {
            "gm_displayed_bounds": "PROVED from pinned source under their stated hypotheses; used only for exact exponent compatibility",
            "gm_rational_remark": "OBSERVED heuristic example, not a predicate and not a consequence of energy",
            "new_rational_predicate": "CONJECTURED diagnostic definition; no source attribution",
            "positive_cubic_lower_bound": "CONJECTURED simultaneous witness condition; source supplies upper bounds only",
        },
        "conventions": {
            "scale_exponents": c.SCALE_EXPONENTS,
            "sigma": render_fraction(c.SIGMA),
            "separation_exponent_in_H": render_fraction(c.SEPARATION_EXPONENT_IN_H),
            "slack": c.SLACK,
            "fourier": c.FOURIER_CONVENTION,
            "exponential": c.EXPONENTIAL_CONVENTION,
            "smooth_functions": c.SMOOTH_FUNCTIONS,
            "support_and_plateau": c.SUPPORT_AND_PLATEAU,
        },
        "exact_source_bound_compatibility": {
            "epistemic_status": "PROVED",
            "exponents_in_v": exact_strings,
            "range_check": "L=v^10=H^(5/6) >= H^(3/4)",
            "implication": "No contradiction is available from these displayed exponent upper bounds alone.",
            "non_implication": "Exponent compatibility does not construct common coefficients or a common W and does not prove sharpness.",
        },
        "classification": {
            "branch": "CRR-U_UNIVERSAL_INCOMPATIBILITY",
            "epistemic_status": "CONJECTURED",
            "statement": "There exists v0 such that no witness exists for any integer v>=v0.",
            "falsifier": "A sequence of integers v_j tending to infinity with one common-pair witness (b^(j),W_j) at every v_j.",
            "finite_witness_policy": "A finite witness neither proves nor refutes the asymptotic statement.",
        },
        "witness_schema": {
            "common_object_rule": "One common pair (b,W) must satisfy Base(v), RationalMass(v), and PositiveCubic(v); no separately optimized W is admissible.",
            "base": {
                "coefficients": "b_n for n>=1 complex with |b_n|<=1",
                "polynomial": "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)",
                "set": "finite W subset [0,H], H^(1/100)-separated",
                "cardinality": "v^(8-delta(v)) <= |W| <= v^(8+delta(v))",
                "pointwise": "|D_v(t)| >= v^(7-delta(v)) for every t in W",
                "energy_definition": "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1",
                "energy_band": "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))",
            },
            "rational_mass": {
                "R": "R_W(u)=sum_(t in W)|u|^(it)",
                "smoothing": "Rtilde_W(u)^2=integral_R H psi1(H(u-u')) psi2(u') |R_W(u')|^2 du'",
                "rational_net": "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, intervals of radius 1/(100H)",
                "threshold": "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))",
                "circularity_audit": "Predicate uses only frozen constants, explicit bumps, the rational net, and W; it does not inspect S3 or computed candidates.",
            },
            "positive_cubic": {
                "h": "h_t(u)=w(u)^2u^(it)",
                "I_m": "L^3 times the W^3 sum of the three cyclic Fourier factors at m_i L",
                "S3_signed": "sum over integer triples with m1*m2*m3 nonzero",
                "convergence": "absolute for each finite W by rapid Fourier decay of fixed compactly supported smooth h_t",
                "reality": "conjugation plus simultaneous t-order reversal and m -> -m",
                "threshold": "S3_signed >= v^(36-delta(v))",
            },
        },
        "resource_policy": {
            "mode": "ANALYTIC_ONLY",
            "discovery_search_authorized": False,
            "row_cap": 0,
            "coefficient_families": [],
            "set_families": [],
            "rng_seed": None,
            "failed_row_rule": "No rows may be generated under v1. Any computation represented as CRR evidence is an unauthorized exploratory result and cannot be promoted.",
            "certification_margin": None,
            "future_search_rule": "A new versioned preregistration must freeze all families, ranges, seed, cap, failed-row handling, and rigorous margin before any finite probe.",
        },
        "independent_analytic_obligations": [
            "uniform Base(v) pointwise and separation hypotheses",
            "both energy-band inequalities",
            "explicit rational-mass measure inequality",
            "signed cubic convergence, reality, positivity, and size",
            "uniform handling of delta(v) and every source subpower loss",
            "two independent proof routes or a documented mechanism-specific reason independence is impossible",
        ],
        "first_analytic_subbranches": [
            "energy-versus-rational-mass incompatibility",
            "rational-mass-versus-positive-signed-cubic incompatibility",
        ],
        "gate": {
            "formalization": "PASS_PENDING_HOSTILE_AUDIT",
            "mathematical_classification": "OPEN",
            "search": "PROHIBITED",
            "promotion_rule": "PASS-INCOMPATIBLE requires a universal theorem; PASS-COMPATIBLE requires an explicit asymptotic family and all simultaneous estimates.",
        },
        "replay": {
            "write_command": "python3 proof/build_cycle_4_p1r_crr_u_formalization_v1.py --write",
            "check_command": "python3 proof/build_cycle_4_p1r_crr_u_formalization_v1.py --check",
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
        require(not OUTPUT.exists(), "refusing to overwrite CRR-U formalization v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR-U formalization v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR-U formalization v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"], "search": payload["gate"]["search"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

