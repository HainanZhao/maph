#!/usr/bin/env python3
"""Seal the corrected analytic-only Cycle 4 CRR-U formalization v2."""
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
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v1.json", "7eadb2a66e957cceaac4031614cddaebfd3d5df12cde45155ae26f6ed43e9b72"),
    "v1_builder": (ROOT / "proof/build_cycle_4_p1r_crr_u_formalization_v1.py", "25022535a7f3d5679dbb687422d5641960df4515651a2a41b2bf3209a13fff84"),
    "v1_conventions": (ROOT / "conventions/crr_formalization_v1.py", "eb0ee6e84bdfa3b87f5fffdc2901192db1b75b700a3d9621b10c670458ffd42b"),
    "v1_document": (ROOT / "docs/cycle-4-p1r-crr-u-formalization-v1.md", "b0aaf464540f9c41eb8414dc38d7be4a7680c0ac1148eadf0a6a61f4836471ed"),
    "v1_tests": (ROOT / "tests/test_cycle_4_p1r_crr_u_formalization_v1.py", "5096615eab239570b766e00a4c5afb8115977145bea4501b3a8519a07f2b6c2a"),
    "v1_fail_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1.json", "9cea180d4a649df219d6e8ee9c6a490a279bda7889972e7c9dc70076d584d02f"),
    "v1_fail_script": (ROOT / "proof/audit_cycle_4_p1r_crr_u_formalization_v1.py", "03b48cddd9255302a0cad28babd7fbfd74d800b60268d765103780c4fcb3e5d4"),
    "v1_fail_document": (ROOT / "docs/cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1.md", "684eb0856775503729038d71ff81945fcb590321c4fd2e348bf5168f8b9665b6"),
    "v1_fail_tests": (ROOT / "tests/test_cycle_4_p1r_crr_u_formalization_v1_hostile_audit_v1.py", "5e12ac419cb15cd2898b7a7a800c0d7dd3d450383649ca80fc67d79316f90e76"),
    "v2_conventions": (ROOT / "conventions/crr_formalization_v2.py", "0d960b76a4ad03cce43727159cf846696dbee732184df44b2ee0503b9ae18ce8"),
    "v2_document": (ROOT / "docs/cycle-4-p1r-crr-u-formalization-v2-correction.md", "00bd9e1a20e79fda774301495ffa032e8e61c67d6e8a0475980e2ceefce3f5e0"),
    "gm_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
}
SOURCE_FRAGMENTS = (
    "Let $W$ be $T^\\epsilon$-separated, and let $|b_n|\\le 1$ be such that $|D_N(t)|>N^\\sigma$ for all $t\\in W$.",
    "\\begin{lmm}[$L^2$ bound] \\label{RL2}",
    "\\begin{lmm}[$L^4$ bound] \\label{RL4}",
    "\\label{propsumaff}",
    "\\label{prp:energybound}",
    "\\label{prpstn:S3}",
    "S_3=\\sum_{m_1,m_2,m_3 \\not= 0} I_m",
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
    path = INPUTS["v2_conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_formalization_v2", path)
    require(spec is not None and spec.loader is not None, "cannot load CRR v2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "CRR-U formalization v2 requires non-optimized CPython 3.12.3")
    return runtime


def render_affine(value: tuple[Fraction, Fraction]) -> str:
    constant, coefficient = value
    left = str(constant.numerator) if constant.denominator == 1 else f"{constant.numerator}/{constant.denominator}"
    if coefficient == 0:
        return left
    sign = "+" if coefficient > 0 else "-"
    magnitude = abs(coefficient)
    right = str(magnitude.numerator) if magnitude.denominator == 1 else f"{magnitude.numerator}/{magnitude.denominator}"
    return f"{left}{sign}{right}*delta"


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    v1 = load_json(INPUTS["v1_artifact"][0])
    failure = load_json(INPUTS["v1_fail_artifact"][0])
    require(v1.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v1", "v1 identity mismatch")
    require(failure.get("decision") == "FAIL", "v1 failure decision mismatch")
    require([row.get("id") for row in failure.get("findings", [])] == ["F1_SLACKED_POINTWISE_SOURCE_HYPOTHESIS", "F2_OMITTED_SLACK_IN_RATIONAL_AND_AFFINE_TIES", "F3_PHASE_LABEL_DERIVATION_INCOMPLETE"], "v1 failure ledger mismatch")

    source = INPUTS["gm_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source, f"GM source fragment missing: {fragment}")

    c = load_conventions()
    rows = {key: [render_affine(value) for value in values] for key, values in c.exact_slack_checks().items()}
    expected_rows = {
        "large_values_upper": ["6+2*delta", "8+4*delta", "8+4*delta"],
        "energy_upper_at_cardinality_upper": ["20+5*delta", "20+37/8*delta", "20+5*delta"],
        "s3_upper_at_cardinality_upper": ["36+3/2*delta", "36+3*delta", "36+3*delta", "36+45/16*delta"],
        "rational_lower_moments": ["8-3*delta", "20-5*delta"],
        "rational_induced_affine_lower": ["28-6*delta", "28-5*delta"],
        "source_affine_upper_from_base": ["28+2*delta", "28+1*delta"],
    }
    require(rows == expected_rows, "corrected slack row rendering mismatch")

    witness_schema = json.loads(json.dumps(v1["witness_schema"]))
    witness_schema["positive_cubic"]["reality"] = c.S3_REALITY_INVOLUTION + "; the all-nonzero-coordinate lattice is invariant"
    witness_schema["rational_mass"]["upper_moment_bridge"] = "For A=integral psi1 and F=Rtilde^2, Fubini/Cauchy give integral F=A integral psi2|R|^2 and integral F^2<=A^2 integral psi2^2|R|^4; apply the raw-R RL2/RL4 arguments, not the source's existential smoothed pair."

    return {
        "artifact_id": "cycle-4-p1r-crr-u-formalization-v2",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_ANALYTIC_FORMALIZATION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "Corrected CRR-U definition and exact slack bookkeeping only. CRR-U remains CONJECTURED; no witness, incompatibility theorem, density result, short-interval theorem, or method saturation is proved, and no discovery search is authorized.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "historical_replay": {"current_plan_read": False, "current_plan_eligibility": "EXCLUDED_FROM_HISTORICAL_ARTIFACT"},
        "correction": {
            "preserves_v1": True,
            "v1_status": "CONTAINED_FAIL",
            "failure_record": "cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1",
            "defects_corrected": ["source-threshold slack", "rational/affine slack", "full Fourier phase involution", "arbitrary-bump RL4 bridge"],
            "witness_class_narrowed": False,
        },
        "research_stage_review_policy": {
            "lightweight_checks": "required now: exact algebra, source anchors, replay, tamper rejection, and explicit claim boundaries",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
            "effect": "research findings may remain CONJECTURED/OBSERVED without a hostile promotion gate; proof-grade manuscript claims still require paper-stage hostile audit",
        },
        "classification": v1["classification"],
        "conventions": {
            "scale_exponents": c.SCALE_EXPONENTS,
            "sigma_for_admitted_base": render_affine(c.SIGMA_V),
            "separation_exponent_in_H": str(c.SEPARATION_EXPONENT_IN_H),
            "slack": c.SLACK,
            "fourier": c.FOURIER_CONVENTION,
            "exponential": c.EXPONENTIAL_CONVENTION,
            "smooth_functions": c.SMOOTH_FUNCTIONS,
            "support_and_plateau": c.SUPPORT_AND_PLATEAU,
            "s3_reality_involution": c.S3_REALITY_INVOLUTION,
        },
        "witness_schema": witness_schema,
        "exact_slack_bookkeeping": {
            "epistemic_status": "PROVED",
            "rows": rows,
            "central_delta_zero_limits": {key: [value.split("+")[0].split("-")[0] for value in values] for key, values in rows.items()},
            "range_check": "L=v^10=H^(5/6)>=H^(3/4)",
            "implication": "All displayed source upper and witness lower bands are leading-exponent compatible; no contradiction follows from these rows alone.",
            "non_implication": "The rows do not construct common coefficients/W and do not prove sharpness or incompatibility.",
        },
        "moment_bridge": {
            "epistemic_status": "PROVED",
            "identity": "For A=integral psi1 and F=Rtilde^2: integral F=A integral psi2|R|^2 and integral F^2<=A^2 integral psi2^2|R|^4.",
            "source_use": "Apply the published raw-R RL2/RL4 arguments on the fixed psi2 support; do not identify the explicit bumps with the existential S3Expansion pair.",
            "consequence": "RationalMass plus Base yields only the critical sandwich integral F=v^(8+o(1)), integral F^2=v^(20+o(1)), E(W)=v^(20+o(1)); no incompatibility.",
        },
        "resource_policy": v1["resource_policy"],
        "independent_analytic_obligations": v1["independent_analytic_obligations"],
        "first_analytic_subbranches": v1["first_analytic_subbranches"],
        "gate": {
            "formalization": "RESEARCH_STAGE_SEALED_LIGHTWEIGHT_CHECKED",
            "mathematical_classification": "OPEN",
            "search": "PROHIBITED",
            "paper_stage_hostile_audit": "PENDING",
        },
        "replay": {
            "write_command": "python3 proof/build_cycle_4_p1r_crr_u_formalization_v2.py --write",
            "check_command": "python3 proof/build_cycle_4_p1r_crr_u_formalization_v2.py --check",
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
        require(not OUTPUT.exists(), "refusing to overwrite CRR-U formalization v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR-U formalization v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR-U formalization v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"], "search": payload["gate"]["search"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

