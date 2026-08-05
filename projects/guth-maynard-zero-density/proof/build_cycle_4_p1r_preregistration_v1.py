#!/usr/bin/env python3
"""Seal the no-search Cycle 4 P1R preregistration."""
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
OUTPUT = ROOT / "artifacts/cycle-4-p1r-preregistration-v1.json"
EXPECTED_PYTHON = "3.12.3"

# The documentation hash is filled only after its versioned text is frozen.
INPUTS: dict[str, tuple[Path, str]] = {
    "program": (ROOT / "PROGRAM.md", "ce8cfb2c4c196b53a0e823667da2ce4e840d7ce18c754a9be1423064d9fce479"),
    "p1r_document": (ROOT / "docs/cycle-4-p1r-preregistration-v1.md", "675708d31772f9483f3d6d53c5975908d40fe6ab76d9a5c189170c7a332899f8"),
    "gm_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "gm_pdf": (ROOT / "artifacts/sources/arxiv-2405.20552v2.pdf", "915392cf7d0ecd108479814a9a1481e23423ef63415776471cec3975ae482cae"),
    "gm_source_tar": (ROOT / "artifacts/sources/arxiv-2405.20552v2.tar", "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"),
    "huxley_pdf": (ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf", "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797"),
    "classical_ledger": (ROOT / "docs/literature-ledger-classical-inputs.md", "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11"),
    "gm_source_metadata": (ROOT / "artifacts/guth-maynard-source-metadata-v1.json", "720da7b4ab8e3290c27df44b466eb74099daadd3eb010ae9ec32ae34914fd963"),
    "g1_route_decision_v2": (ROOT / "artifacts/cycle-3-g1-route-decision-v2.json", "87e697850dea074664227f6be5b187cc12ab4491bad6d2bda0065ee9df1b3872"),
    "g1_route_hostile_audit_v2": (ROOT / "artifacts/g1-route-decision-v2-hostile-audit-v1.json", "a6f0cb5f3ec6deaebe5888c966c8fc573e3d1328a15b027c7c81945d6295e2b4"),
    "g1_exact_atlas_v2": (ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json", "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
    "g1_envelope_sensitivity_v1": (ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json", "850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e"),
    "g1_literature_correction_v2": (ROOT / "artifacts/g1-current-literature-audit-v2-correction.json", "f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076"),
    "g1_conventions": (ROOT / "conventions/g1_atlas_v1.py", "642a61fc03e5de6c7f7df5338e88da552ef1c72a7b7d7897898fb23740106ca5"),
}

PLAN_FRAGMENTS = (
    "P1R ACTIVE",
    "Frozen architecture: retain the checked Ingham/Huxley-restated coefficient",
    "`I(sigma)=3/(2-sigma)` for `1/2 <= sigma < 7/10`",
    "`T=v^13`, `U=H=v^12`, `L=v^10`, `R=v^8`, `M=v^2`, `Q=v^4`, `V=v^7`",
    "Before any search, a versioned preregistration must freeze:",
    "CONTAINED if finite probes find no candidate",
)
SOURCE_FRAGMENTS = (
    "\\begin{thrm}[Large values estimate]\\label{thrm:LargeValues}",
    "|b_n| \\le 1",
    "$1$-separated points in $[0,T]$",
    "\\begin{prpstn}[Equidistribution over affine transformations] \\label{propsumaff}",
    "\\begin{prpstn}[Refined $S_3$ bound] \\label{prpstnS3}",
    "\\begin{prpstn}[Bound for energy] \\label{prp:energybound}",
    "T^{3/4} \\le N \\le T",
    "S_1=O_\\epsilon(T^{-10})",
    "a random set $W$ would have $E(W)\\approx |W|^4/T_1$",
    "essentially tight if the $R$ function",
)
CLASSICAL_FRAGMENT = "N(\\alpha,T)\\ll T^{3(1-\\alpha)/(2-\\alpha)}(\\log T)^5"


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
    require(
        runtime == {"implementation": "CPython", "python": EXPECTED_PYTHON, "optimization_level": 0},
        "P1R preregistration requires non-optimized CPython 3.12.3",
    )
    return runtime


def source_hypothesis_ledger() -> list[dict[str, Any]]:
    return [
        {
            "id": "HUX-ING",
            "epistemic_status": "PROVED",
            "locator": "Huxley (1.8), frozen classical ledger lines 44--48",
            "hypotheses": ["1/2 <= sigma <= 3/4", "two-sided zero-count convention recorded in the ledger"],
            "statement": "N(sigma,T) << T^(3(1-sigma)/(2-sigma)) (log T)^5",
            "permitted_use": "retained left coefficient I(sigma) for P1R-FS only",
        },
        {
            "id": "GM-T1.1",
            "epistemic_status": "PROVED",
            "locator": "GM TeX lines 68--81, Theorem thrm:LargeValues",
            "hypotheses": ["|b_n| <= 1", "1-separated points", "points in [0,T]", "large value at least V"],
            "statement": "R <= T^o(1)(N^2 V^-2 + N^(18/5) V^-4 + T N^(12/5) V^-4)",
            "permitted_use": "source-grounded CRR monomial bookkeeping; no common-family assertion",
        },
        {
            "id": "GM-AFF",
            "epistemic_status": "PROVED",
            "locator": "GM TeX lines 1408--1412, Proposition propsumaff",
            "hypotheses": ["f non-negative", "support u asymp 1", "stated Fourier decay"],
            "statement": "J(f) lessapprox M^6 (integral f)^2 + M^4 integral f^2",
            "permitted_use": "formal rational-affine scale only; arbitrary f is not automatically |R_W|^2",
        },
        {
            "id": "GM-S3",
            "epistemic_status": "PROVED",
            "locator": "GM TeX lines 1684--1692, Proposition prpstnS3",
            "hypotheses": ["W is T^epsilon-separated", "W lies in an interval of length T"],
            "statement": "refined four-term S3 upper bound",
            "permitted_use": "formal exponent balance only; stronger separation remains a future CRR obligation",
        },
        {
            "id": "GM-P11.1",
            "epistemic_status": "PROVED",
            "locator": "GM TeX lines 1803--1810, Proposition prp:energybound",
            "hypotheses": ["|b_n| <= 1", "W is 1-separated", "W lies in interval length T", "|D(t)| >= N^sigma", "T^(3/4) <= N <= T"],
            "statement": "three-term energy upper bound",
            "permitted_use": "formal exponent balance only; no energy lower bound or extremizer classification",
        },
        {
            "id": "GM-S1",
            "epistemic_status": "PROVED",
            "locator": "GM TeX lines 810--837, Proposition prpstn:S1",
            "hypotheses": ["source S1 setup"],
            "statement": "S1 = O_epsilon(T^-10)",
            "permitted_use": "P1R-CRR does not require S1 extremality",
        },
        {
            "id": "GM-CRITICAL-REMARK",
            "epistemic_status": "OBSERVED",
            "locator": "GM TeX lines 2398--2399",
            "hypotheses": [],
            "statement": "random-energy and rational-concentration discussion is likely/essentially tight language",
            "permitted_use": "motivation only; no simultaneous construction, lower bound, or saturation theorem",
        },
    ]


def scale_bookkeeping() -> dict[str, Any]:
    exponents = {"T_global": 13, "U": 12, "H": 12, "L": 10, "R_cardinality": 8, "M": 2, "Q": 4, "V": 7, "E_formal": 20, "R_over_M": 6}
    sigma = Fraction(7, 10)
    lv = [2 * exponents["L"] - 2 * exponents["V"], Fraction(18 * exponents["L"], 5) - 4 * exponents["V"], exponents["H"] + Fraction(12 * exponents["L"], 5) - 4 * exponents["V"]]
    energy = [exponents["R_cardinality"] + exponents["L"] * (4 - 4 * sigma), Fraction(21 * exponents["R_cardinality"], 8) + Fraction(exponents["H"], 4) + exponents["L"] * (1 - 2 * sigma), 3 * exponents["R_cardinality"] + exponents["L"] * (1 - 2 * sigma)]
    s3 = [2 * exponents["H"] + Fraction(3 * exponents["R_cardinality"], 2), exponents["H"] + exponents["R_cardinality"] + exponents["L"] * (3 - 2 * sigma), exponents["H"] + 2 * exponents["R_cardinality"] + exponents["L"] * (Fraction(3, 2) - sigma), Fraction(9 * exponents["H"], 8) + Fraction(29 * exponents["R_cardinality"], 16) + exponents["L"] * (Fraction(3, 2) - sigma)]
    require(lv == [6, 8, 8], "critical large-values exponent balance mismatch")
    require(energy == [20, 20, 20], "critical energy exponent balance mismatch")
    require(s3 == [36, 36, 36, 36], "critical S3 exponent balance mismatch")
    return {
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact monomial substitution into pinned displayed upper-bound formulas only; no lower bound, actual coefficient family, common W, or saturation conclusion.",
        "source_variable_relabeling": {"source_interval_T": "H", "source_polynomial_N": "L", "project_global_height": "T_global", "source_R_function": "mathcal_R_W", "project_cardinality": "R_cardinality"},
        "monomial_scales": exponents,
        "identities": ["L=H^(5/6)", "M=H/L", "V=L^(7/10)", "R_cardinality=H^(2/3)", "Q=H^(1/3)", "E_formal=U^(5/3)=R_cardinality^(5/2)=R_cardinality^4/H", "R_cardinality/M=H^(1/2)"],
        "large_values_term_exponents_in_v": [str(value) for value in lv],
        "energy_term_exponents_in_v": [str(value) for value in energy],
        "refined_s3_term_exponents_in_v": [str(value) for value in s3],
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen_hashes: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(expected != "DOCUMENT_HASH_TO_BE_FILLED", "P1R document hash is not sealed")
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen_hashes[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    plan_text = INPUTS["plan"][0].read_text(encoding="utf-8")
    for fragment in PLAN_FRAGMENTS:
        require(fragment in plan_text, f"PLAN P1R authorization fragment missing: {fragment}")
    source_text = INPUTS["gm_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source_text, f"GM source fragment missing: {fragment}")
    classical_text = INPUTS["classical_ledger"][0].read_text(encoding="utf-8")
    require(CLASSICAL_FRAGMENT in classical_text, "Huxley/Ingham restatement fragment missing")

    return {
        "artifact_id": "cycle-4-p1r-preregistration-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_PREREGISTRATION_NO_SEARCH_AUTHORIZED",
        "claim_boundary": "Source-anchored Cycle 4 P1R preregistration only. It seals neither a large-values, zero-density, short-interval, compatibility, extremizer, nor saturation theorem, and authorizes no discovery computation.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_hashes,
        "program_authorization": {"status": "OBSERVED", "path": "PROGRAM.md", "required_action": "seal preregistration before P1R-FS routes or any P1R-CRR formalization/search"},
        "source_hypothesis_ledger": source_hypothesis_ledger(),
        "p1r_fs": {
            "epistemic_status": "PROVED",
            "claim_boundary": "Exact fixed-splice algebra conditional on the pinned Huxley/Ingham restatement and the explicitly frozen architecture; not a lower bound for the actual zero count or a Guth--Maynard saturation theorem.",
            "architecture": {"left_range": "1/2 <= sigma < 7/10", "left_coefficient": "I(sigma)=3/(2-sigma)", "right_policy": "arbitrary replacement permitted only for sigma >= 7/10"},
            "required_two_route_targets": ["30/13-I(sigma)=30(7/10-sigma)/(13(2-sigma))", "sup_{1/2<=sigma<7/10} I(sigma)=30/13", "right-only change cannot certify a strict uniform coefficient below 30/13 within this architecture"],
            "falsifier": "A pinned-source/range mismatch, failed exact identity, or failed strict-supremum witness fails this branch. A changed left branch or splice is outside the frozen architecture.",
            "gate": "UNEXECUTED_REQUIRES_TWO_INDEPENDENT_EXACT_ROUTES_RECONCILIATION_AND_HOSTILE_AUDIT",
        },
        "p1r_crr": {
            "epistemic_status": "CONJECTURED",
            "claim_boundary": "The compatibility classification is an unproved target. This artifact freezes only source-grounded formal bookkeeping; it does not formalize a rational high-mass predicate or authorize a search.",
            "target": "classify whether actual 1-bounded coefficients and one common separated W can simultaneously meet pointwise threshold, random-scale energy, rational-affine concentration, and positive cubic-trace obligations",
            "scale_bookkeeping": scale_bookkeeping(),
            "s1_policy": "S1 extremality is not required, consistent with the frozen PLAN.",
            "formalization_gate": {
                "status": "FORMALIZATION_REQUIRED_NO_SEARCH",
                "search_authorized": False,
                "unsealed_required_fields": ["smoothed correlation normalization", "energy normalization and radius", "universal-incompatibility versus explicit-construction branch", "asymptotic quantifiers", "rational high-mass predicate and neighborhood width", "smoothing and separation", "cubic-trace sign/size predicate", "coefficient/set families", "ranges and thresholds", "failed-row rule", "finite resource cap", "RNG seed", "certification margin", "independent analytic proof obligations and detector hypotheses"],
                "failure_rule": "No field may be selected after observing a candidate. Any attempted computation before all fields are sealed is a preregistration failure and is not evidence for either CRR outcome.",
            },
            "falsifiers": {"future_universal_incompatibility": "only an infinite source-compliant family satisfying every future sealed clause", "future_explicit_construction": "failure of any future sealed simultaneous obligation", "finite_model_or_probe": "CONTAINED only; neither an asymptotic negative nor a saturation theorem"},
        },
        "resource_policy": {"epistemic_status": "OBSERVED", "status": "UNSEALED_NO_COMPUTATION", "wall_time_cap": None, "memory_cap": None, "sample_cap": None, "rng_seed": None, "reason": "PLAN requires all resource and discovery choices to be frozen before a probe; choosing them here without a source-grounded formal predicate would be post-hoc invention."},
        "falsifier": "Any frozen-byte mismatch, missing PLAN/source clause, runtime mismatch, or failed exact monomial identity invalidates this preregistration. It does not convert heuristic source language into a theorem.",
        "replay": {"write_command": "python3 proof/build_cycle_4_p1r_preregistration_v1.py --write", "check_command": "python3 proof/build_cycle_4_p1r_preregistration_v1.py --check"},
    }


def render(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite P1R preregistration artifact")
        with OUTPUT.open("xb") as stream:
            stream.write(render(payload))
    else:
        require(OUTPUT.is_file(), "P1R preregistration artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "P1R preregistration artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
