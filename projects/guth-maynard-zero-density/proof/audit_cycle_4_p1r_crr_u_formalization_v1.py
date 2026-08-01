#!/usr/bin/env python3
"""Hostile audit of the sealed Cycle 4 CRR-U formalization v1.

This audit deliberately records a failure.  It does not repair or rewrite the
sealed v1 formalization.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v1.json", "7eadb2a66e957cceaac4031614cddaebfd3d5df12cde45155ae26f6ed43e9b72"),
    "v1_builder": (ROOT / "proof/build_cycle_4_p1r_crr_u_formalization_v1.py", "25022535a7f3d5679dbb687422d5641960df4515651a2a41b2bf3209a13fff84"),
    "v1_conventions": (ROOT / "conventions/crr_formalization_v1.py", "eb0ee6e84bdfa3b87f5fffdc2901192db1b75b700a3d9621b10c670458ffd42b"),
    "v1_document": (ROOT / "docs/cycle-4-p1r-crr-u-formalization-v1.md", "b0aaf464540f9c41eb8414dc38d7be4a7680c0ac1148eadf0a6a61f4836471ed"),
    "v1_tests": (ROOT / "tests/test_cycle_4_p1r_crr_u_formalization_v1.py", "5096615eab239570b766e00a4c5afb8115977145bea4501b3a8519a07f2b6c2a"),
    "gm_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
}
AUDIT_FILES = (
    ROOT / "docs/cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1.md",
    ROOT / "tests/test_cycle_4_p1r_crr_u_formalization_v1_hostile_audit_v1.py",
)
SOURCE_ANCHORS = (
    "Let $W$ be $T^\\epsilon$-separated, and let $|b_n|\\le 1$ be such that $|D_N(t)|>N^\\sigma$ for all $t\\in W$.",
    "E(W)\\lessapprox |W| N^{4-4\\sigma}+|W|^{21/8}T^{1/4}N^{1-2\\sigma}+|W|^3N^{1-2\\sigma}",
    "S_{3}\\lessapprox T^2|W|^{3/2}+T|W|N^{3-2\\sigma}+T|W|^2N^{3/2-\\sigma}+T^{9/8}|W|^{29/16}N^{3/2-\\sigma}",
    "S_3=\\sum_{m_1,m_2,m_3 \\not= 0} I_m",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "CRR-U hostile audit v1 requires non-optimized CPython 3.12.3")
    return runtime


def render_affine(constant: Fraction, delta_coefficient: Fraction) -> str:
    left = str(constant.numerator) if constant.denominator == 1 else f"{constant.numerator}/{constant.denominator}"
    if delta_coefficient == 0:
        return left
    sign = "+" if delta_coefficient > 0 else "-"
    magnitude = abs(delta_coefficient)
    right = str(magnitude.numerator) if magnitude.denominator == 1 else f"{magnitude.numerator}/{magnitude.denominator}"
    return f"{left}{sign}{right}*delta"


def audit() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing audited input: {label}")
        actual = sha256(path)
        require(actual == expected, f"audited input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    source = INPUTS["gm_tex"][0].read_text(encoding="utf-8")
    for anchor in SOURCE_ANCHORS:
        require(anchor in source, f"required GM source anchor missing: {anchor}")

    artifact = json.loads(INPUTS["v1_artifact"][0].read_text(encoding="utf-8"))
    require(artifact["gate"]["formalization"] == "PASS_PENDING_HOSTILE_AUDIT", "unexpected v1 gate state")
    require(artifact["resource_policy"]["discovery_search_authorized"] is False, "v1 must prohibit search")
    require(artifact["witness_schema"]["base"]["pointwise"] == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "v1 pointwise slack changed")
    require(artifact["witness_schema"]["rational_mass"]["threshold"] == "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))", "v1 rational slack changed")

    # The source hypothesis |D| >= L^sigma, with L=v^10, matches the
    # admitted Base(v) threshold only at sigma_v=7/10-delta/10.  All rows
    # below are exact affine expressions in delta, not asymptotic shorthand.
    sigma_constant, sigma_delta = Fraction(7, 10), Fraction(-1, 10)
    require(10 * sigma_constant == 7 and 10 * sigma_delta == -1, "source-to-witness threshold map failed")
    lv = [(Fraction(6), Fraction(2)), (Fraction(8), Fraction(4)), (Fraction(8), Fraction(4))]
    energy = [(Fraction(20), Fraction(5)), (Fraction(20), Fraction(37, 8)), (Fraction(20), Fraction(5))]
    s3 = [(Fraction(36), Fraction(3, 2)), (Fraction(36), Fraction(3)), (Fraction(36), Fraction(3)), (Fraction(36), Fraction(45, 16))]
    rational = [(Fraction(8), Fraction(-3)), (Fraction(20), Fraction(-5))]
    affine = [(Fraction(28), Fraction(-6)), (Fraction(28), Fraction(-5))]
    require([render_affine(*row) for row in lv] == ["6+2*delta", "8+4*delta", "8+4*delta"], "large-value slack algebra failed")
    require([render_affine(*row) for row in energy] == ["20+5*delta", "20+37/8*delta", "20+5*delta"], "energy slack algebra failed")
    require([render_affine(*row) for row in s3] == ["36+3/2*delta", "36+3*delta", "36+3*delta", "36+45/16*delta"], "S3 slack algebra failed")
    require([render_affine(*row) for row in rational] == ["8-3*delta", "20-5*delta"], "rational-mass slack algebra failed")
    require([render_affine(*row) for row in affine] == ["28-6*delta", "28-5*delta"], "affine slack algebra failed")

    audit_files = {}
    for path in AUDIT_FILES:
        require(path.is_file(), f"missing audit package file: {path.name}")
        audit_files[path.name] = sha256(path)

    return {
        "artifact_id": "cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "decision": "FAIL",
        "claim_boundary": "This is a hostile audit of formalization v1. It preserves v1 and identifies a source-application/slack defect and an incomplete phase-label derivation. It proves neither CRR-U nor its negation.",
        "runtime": runtime,
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audit_package_hashes": audit_files,
        "frozen_v1_and_source_hashes": frozen,
        "checked_passes": {
            "source_object_mapping": "The v1 definitions of D_N, h_t, R, the smoothed correlation form, and the all-nonzero-coordinate S3 sum have identifiable GM source anchors; v1 correctly labels its particular bumps and rational predicate as new.",
            "common_W_and_no_search": "The artifact requires one common (b,W), does not separately optimize W by block, and keeps row_cap=0 with discovery prohibited.",
            "replay_integrity": "The v1 builder rejects optimized mode, pins its frozen inputs, and check replay matches the sealed v1 artifact.",
        },
        "findings": [
            {
                "id": "F1_SLACKED_POINTWISE_SOURCE_HYPOTHESIS",
                "severity": "FAIL",
                "tag": "PROVED",
                "source_anchor": "GM lines 732--740 require |D_N(t)|>N^sigma; v1 Base(v) only requires v^(7-delta(v)).",
                "exact_map": "N=L=v^10 and v^(7-delta)=L^(7/10-delta/10)",
                "consequence": "The v1 claim that exact substitution gives [6,8,8], [20,20,20], and [36,36,36,36] for its actual witness does not follow. Those central rows use sigma=7/10, whereas the admitted witness requires sigma_v=7/10-delta/10.",
            },
            {
                "id": "F2_OMITTED_SLACK_IN_RATIONAL_AND_AFFINE_TIES",
                "severity": "FAIL",
                "tag": "PROVED",
                "source_anchor": "v1 RationalMass(v) requires measure >=v^(-4-delta) at Rtilde>=v^(6-delta); GM affine bound is lines 1408--1422.",
                "exact_map": "The induced lower moment exponents are 8-3delta and 20-5delta, so the corresponding affine exponents are 28-6delta and 28-5delta, not the claimed exact [28,28].",
                "consequence": "The asserted exact rational/affine tie is not established with the formal witness quantifiers. A repaired version must carry explicit slack constants through every comparison or remove the slack from the witness thresholds.",
            },
            {
                "id": "F3_PHASE_LABEL_DERIVATION_INCOMPLETE",
                "severity": "FAIL",
                "tag": "PROVED",
                "source_anchor": "GM lines 683--707 define I_m using the fixed Fourier sign convention.",
                "exact_map": "For real w, conjugation gives overline(I_(m1,m2,m3))=I_(-m3,-m2,-m1), after reversing t2,t3; the all-nonzero-coordinate index set is invariant under this full involution.",
                "consequence": "Reality of the aggregate S3 sum is recoverable, but v1 states only 'm -> -m' and no labeled coordinate permutation. Under the repository convention rule, the displayed phase/reality justification is incomplete and cannot support a sealed formalization gate.",
            },
        ],
        "exact_slack_recomputation": {
            "sigma_for_admitted_base": render_affine(sigma_constant, sigma_delta),
            "large_value_upper_rows": [render_affine(*row) for row in lv],
            "energy_upper_rows_at_cardinality_upper": [render_affine(*row) for row in energy],
            "s3_upper_rows_at_cardinality_upper": [render_affine(*row) for row in s3],
            "rational_mass_lower_moments": [render_affine(*row) for row in rational],
            "affine_lower_rows": [render_affine(*row) for row in affine],
        },
        "gate_consequence": {
            "v1_formalization": "CONTAINED_FAIL",
            "mathematical_classification": "OPEN",
            "discovery_search": "REMAINS_PROHIBITED",
            "promotion": "No CRR-U classification, density result, short-interval result, or saturation theorem may cite v1 as a passed formalization.",
        },
        "required_correction_scope": [
            "Create a new version rather than modify v1.",
            "Either use exact threshold v^7 or carry all explicit delta coefficients through source, moment, affine, and S3 comparisons.",
            "State and prove the full Fourier-conjugation involution with its coordinate permutation.",
            "Re-run a fresh hostile audit before any search authorization.",
        ],
        "replay": {
            "write_command": "python3 proof/audit_cycle_4_p1r_crr_u_formalization_v1.py --write",
            "check_command": "python3 proof/audit_cycle_4_p1r_crr_u_formalization_v1.py --check",
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
    payload = audit()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite CRR-U hostile audit v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR-U hostile audit v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR-U hostile audit v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "decision": payload["decision"], "search": payload["gate_consequence"]["discovery_search"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
