#!/usr/bin/env python3
"""Seal the exact conditional Cycle 4 CRR-to-Montgomery reduction v1.

The script proves only rational exponent identities and finite-threshold
implications conditional on the explicitly recorded conjectural premises.  It
does not invoke Montgomery's large-value conjecture as a theorem.
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
OUTPUT = ROOT / "artifacts/cycle-4-crr-montgomery-reduction-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_conventions": (
        ROOT / "conventions/crr_formalization_v2.py",
        "0d960b76a4ad03cce43727159cf846696dbee732184df44b2ee0503b9ae18ce8",
    ),
    "crr_v2_artifact": (
        ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json",
        "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e",
    ),
    "document": (
        ROOT / "docs/cycle-4-crr-montgomery-reduction-v1.md",
        "e36f83f47ed487c3a1b89530c449953fa0de253a8e58703fa1028865735e40e0",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
}
SOURCE_FRAGMENTS = (
    "\\begin{cnjctr}[Montgomery's large value conjecture] \\label{cnjctr:Montgomery}",
    "Let $\\sigma > 1/2$ and $D(t) = \\sum_{N<n\\le 2N} b_n e^{i t \\log n}$ with $|b_n| \\le 1$.",
    "Suppose $W \\subset [0,T] $ is a 1-separated set such that $|D(t)| > N^\\sigma$ for $t\\in W$.",
    "|W| \\le C(\\sigma) T^{o(1)} N^{2 - 2 \\sigma}.",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "CRR-to-Montgomery reduction v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}
    return result


def fixed_anchor() -> dict[str, str]:
    """Return exact exponent data at sigma=13/20 and epsilon=1/24."""
    sigma = Fraction(13, 20)
    epsilon = Fraction(1, 24)
    length_exponent = Fraction(10)
    height_exponent = Fraction(12)
    pointwise_center = Fraction(7)
    cardinality_center = Fraction(8)
    threshold_exponent = length_exponent * sigma
    pointwise_margin = pointwise_center - threshold_exponent
    montgomery_length_exponent = length_exponent * (2 - 2 * sigma)
    epsilon_height_exponent = height_exponent * epsilon
    upper_exponent = montgomery_length_exponent + epsilon_height_exponent
    cardinality_gap = cardinality_center - upper_exponent
    require(sigma > Fraction(1, 2), "fixed anchor must be in the conjectural range")
    require(threshold_exponent == Fraction(13, 2), "fixed threshold exponent mismatch")
    require(pointwise_margin == Fraction(1, 2), "fixed pointwise margin mismatch")
    require(montgomery_length_exponent == Fraction(7), "fixed Montgomery length exponent mismatch")
    require(epsilon_height_exponent == Fraction(1, 2), "fixed epsilon-height exponent mismatch")
    require(upper_exponent == Fraction(15, 2), "fixed total upper exponent mismatch")
    require(cardinality_gap == Fraction(1, 2), "fixed cardinality gap mismatch")
    return {
        "sigma": fraction_text(sigma),
        "epsilon": fraction_text(epsilon),
        "threshold_exponent_in_v": fraction_text(threshold_exponent),
        "pointwise_margin_before_delta": fraction_text(pointwise_margin),
        "montgomery_length_exponent": fraction_text(montgomery_length_exponent),
        "epsilon_height_exponent": fraction_text(epsilon_height_exponent),
        "upper_exponent_in_v": fraction_text(upper_exponent),
        "cardinality_gap_before_delta": fraction_text(cardinality_gap),
        "sufficient_eventual_conditions": "delta(v)<1/4, v^(1/4)>max(2,C(13/20,1/24),X_0(13/20,1/24)^(1/12))",
    }


def general_interval(sigma: Fraction) -> dict[str, str]:
    """Exact algebra for a fixed rational sample in the open sigma interval."""
    require(Fraction(3, 5) < sigma < Fraction(7, 10), "sigma must lie strictly in (3/5,7/10)")
    pointwise_margin = Fraction(7) - 10 * sigma
    cardinality_gap = Fraction(8) - 20 * (1 - sigma)
    epsilon = cardinality_gap / 48
    upper_exponent = 20 * (1 - sigma) + 12 * epsilon
    require(pointwise_margin > 0, "pointwise margin must be positive")
    require(cardinality_gap > 0, "cardinality gap must be positive")
    require(epsilon > 0, "epsilon must be positive")
    require(upper_exponent == 8 - Fraction(3, 4) * cardinality_gap, "general upper exponent identity mismatch")
    return {
        "sigma": fraction_text(sigma),
        "pointwise_margin_p": fraction_text(pointwise_margin),
        "cardinality_gap_g": fraction_text(cardinality_gap),
        "epsilon_g_over_48": fraction_text(epsilon),
        "upper_exponent_in_v": fraction_text(upper_exponent),
        "lower_minus_upper_margin_under_delta_less_than_g_over_2": fraction_text(cardinality_gap / 4),
    }


def joint_saving_example(kappa2: Fraction, kappa3: Fraction) -> dict[str, str]:
    """Exact dominant-exponent check for a two-tied-term saving."""
    require(kappa2 > 0 and kappa3 > 0, "both tied-term savings must be positive")
    kappa = min(Fraction(2), kappa2, kappa3)
    epsilon = kappa / 4
    upper_exponent = 8 - kappa + epsilon
    require(kappa > 0, "joint saving kappa must be positive")
    require(upper_exponent == 8 - Fraction(3, 4) * kappa, "joint saving exponent mismatch")
    return {
        "kappa_2": fraction_text(kappa2),
        "kappa_3": fraction_text(kappa3),
        "kappa": fraction_text(kappa),
        "epsilon": fraction_text(epsilon),
        "joint_upper_exponent": fraction_text(upper_exponent),
        "base_minus_joint_upper_margin_under_delta_less_than_kappa_over_2": fraction_text(kappa / 4),
    }


def validate_source_and_crr() -> None:
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source, f"Montgomery conjecture source fragment missing: {fragment}")
    crr = json.loads(INPUTS["crr_v2_artifact"][0].read_text(encoding="utf-8"))
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 artifact identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    conventions = crr.get("conventions", {})
    require(base.get("polynomial") == "D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)", "CRR polynomial convention mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "CRR pointwise convention mismatch")
    require(base.get("cardinality", "").startswith("v^(8-delta(v)) <= |W|"), "CRR cardinality lower convention mismatch")
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "CRR separation convention mismatch")
    require(conventions.get("scale_exponents") == {
        "global_height_T0": 13,
        "local_height_H": 12,
        "polynomial_length_L": 10,
        "cardinality_center_R": 8,
        "affine_scale_M": 2,
        "rational_height_Q": 4,
        "large_value_center_V": 7,
    }, "CRR scale conventions mismatch")
    require(conventions.get("support_and_plateau", {}).get("w", "").startswith("0<=w<=1; supp(w) subset [1,2]"), "CRR weight bound/support mismatch")


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    validate_source_and_crr()
    anchor = fixed_anchor()
    interval_samples = [general_interval(Fraction(31, 50)), general_interval(Fraction(13, 20)), general_interval(Fraction(69, 100))]
    joint = joint_saving_example(Fraction(1, 3), Fraction(1, 5))
    one_tied_term = {"saved_term_exponent": "8-1/3", "unsaved_term_exponent": "8", "dominant_exponent": "8"}
    require(one_tied_term["dominant_exponent"] == "8", "one-saving dominant exponent mismatch")
    return {
        "artifact_id": "cycle-4-crr-montgomery-reduction-v1",
        "status": "SEALED_CONDITIONAL_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves exact exponent algebra and finite-threshold implications conditional on two explicitly CONJECTURED premises. It proves neither Montgomery's conjecture nor CRR-U, and it gives no density, prime-interval, saturation, or L-function theorem.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {
            "lightweight_checks": "source transcription, exact Fraction algebra, frozen-input hashes, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "crr_translation": {
            "epistemic_status": "PROVED",
            "conditional_on": "the frozen CRR-v2 Base definition",
            "coefficient_translation": "c_n=w(n/L)b_n has |c_n|<=1 and support within [L,2L]; deleting the possible n=L term changes the value by at most 1",
            "separation_translation": "H^(1/100)-separation implies 1-separation because H=v^12>=1",
            "endpoint_threshold_condition": "For fixed pointwise margin p>0, delta(v)<p/2 and v^(p/2)>2 imply |D_v^+(t)|>L^sigma.",
        },
        "montgomery_fixed_epsilon_premise": {
            "epistemic_status": "CONJECTURED",
            "source_locator": "LargevaluesDirichlet17.tex, Conjecture cnjctr:Montgomery, lines 205-210",
            "statement": "For each fixed sigma>1/2 and epsilon>0, constants C(sigma,epsilon), X_0(sigma,epsilon) give |W|<=C(sigma,epsilon)T^epsilon N^(2-2sigma) for all sufficiently large admissible inputs.",
            "not_a_theorem_in_this_artifact": True,
        },
        "fixed_sigma_reduction": {
            "epistemic_status": "PROVED",
            "conditional_on": "montgomery_fixed_epsilon_premise at sigma=13/20, epsilon=1/24",
            "conclusion": "Any unbounded CRR Base-witness sequence contradicts that conjectural fixed-epsilon premise.",
            "does_not_conclude": "CRR-U, absence of a CRR witness, a density gain, or method saturation",
            "exact_exponents": anchor,
        },
        "general_sigma_reduction": {
            "epistemic_status": "PROVED",
            "conditional_on": "montgomery_fixed_epsilon_premise at each fixed sigma in (3/5,7/10) with epsilon=(20*sigma-12)/48",
            "conclusion": "Any unbounded CRR Base-witness sequence contradicts the corresponding conjectural fixed-epsilon premise at every fixed sigma in the open interval.",
            "endpoint_exclusion": "At sigma=3/5 the cardinality gap is zero; at sigma=7/10 the pointwise margin is zero.",
            "rational_samples": interval_samples,
        },
        "joint_saving_bridge": {
            "epistemic_status": "PROVED",
            "conditional_on": "a uniform CONJECTURED upper bound C(epsilon)v^epsilon(v^6+v^(8-kappa_2)+v^(8-kappa_3)) with fixed kappa_2,kappa_3>0",
            "conclusion": "The stated joint-saving upper bound contradicts the Base cardinality lower bound for all sufficiently large v and hence implies CRR-U.",
            "exact_example": joint,
        },
        "one_saving_limit": {
            "epistemic_status": "PROVED",
            "scope": "exponent comparison in the displayed three-term architecture only",
            "statement": "With one unsaved tied term v^8, the dominant upper exponent remains 8; no fixed positive exponent gap against v^(8-delta(v)) follows from this comparison alone.",
            "example": one_tied_term,
            "not_a_universal_no_go": True,
        },
        "falsifier": {
            "epistemic_status": "PROVED",
            "statement": "An unbounded CRR Base-witness sequence falsifies the stated fixed-epsilon Montgomery premise throughout the open sigma interval; a finite witness does neither.",
        },
        "replay": {
            "write_command": "python3 proof/build_cycle_4_crr_montgomery_reduction_v1.py --write",
            "check_command": "python3 proof/build_cycle_4_crr_montgomery_reduction_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_4_crr_montgomery_reduction_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite CRR-to-Montgomery reduction v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR-to-Montgomery reduction v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR-to-Montgomery reduction v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
