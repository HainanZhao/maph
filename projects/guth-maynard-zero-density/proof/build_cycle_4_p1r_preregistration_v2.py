#!/usr/bin/env python3
"""Seal the corrected no-search Cycle 4 P1R preregistration."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-preregistration-v2.json"
EXPECTED_PYTHON = "3.12.3"
INPUTS: dict[str, tuple[Path, str]] = {
    "authorization_snapshot": (ROOT / "artifacts/cycle-4-p1r-authorization-snapshot-v1.json", "cd42352b145f67af0289aa21b142f40fbc2aac891944bb49d054631384c176d0"),
    "p1r_v2_document": (ROOT / "docs/cycle-4-p1r-preregistration-v2-correction.md", "31865f458d751c8a39258fb12e92b55e31b4fa0591a866c230efdef9220c11de"),
    "v1_artifact": (ROOT / "artifacts/cycle-4-p1r-preregistration-v1.json", "c6491407fb3cc5096610ddda8a8db952ffe0e002441d105024368f6486e39a5b"),
    "v1_builder": (ROOT / "proof/build_cycle_4_p1r_preregistration_v1.py", "9010102782404cf63eb669714dadfb1a0f4b67005f895c3175ec669c60c94059"),
    "v1_document": (ROOT / "docs/cycle-4-p1r-preregistration-v1.md", "675708d31772f9483f3d6d53c5975908d40fe6ab76d9a5c189170c7a332899f8"),
    "v1_tests": (ROOT / "tests/test_cycle_4_p1r_preregistration_v1.py", "779f504a333dcbfda1ed7f06d380a20b369919a3a494004e974621e6fc97e8b4"),
    "v1_hostile_artifact": (ROOT / "artifacts/cycle-4-p1r-preregistration-v1-hostile-audit-v1.json", "245ab832fe695c90307df2409378d74414921777b805f3905d375f9f25ea1b64"),
    "v1_hostile_script": (ROOT / "proof/audit_cycle_4_p1r_preregistration_v1_hostile.py", "8852bb954e77a20679033ea841f084ee2991643fe152c8b5856d3913baf9b5dc"),
    "gm_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "huxley_pdf": (ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf", "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797"),
    "classical_ledger": (ROOT / "docs/literature-ledger-classical-inputs.md", "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11"),
    "g1_route_decision_v2": (ROOT / "artifacts/cycle-3-g1-route-decision-v2.json", "87e697850dea074664227f6be5b187cc12ab4491bad6d2bda0065ee9df1b3872"),
    "g1_envelope_sensitivity_v1": (ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json", "850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e"),
    "g1_exact_atlas_v2": (ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json", "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
}
SOURCE_FRAGMENTS = (
    "\\begin{thrm}[Large values estimate]\\label{thrm:LargeValues}",
    "\\begin{prpstn}[Equidistribution over affine transformations] \\label{propsumaff}",
    "\\begin{prpstn}[Refined $S_3$ bound] \\label{prpstnS3}",
    "\\begin{prpstn}[$S_3$ Bound]\\label{prpstn:S3}",
    "Let $N\\ge T^{3/4}$",
    "\\begin{prpstn}[Bound for energy] \\label{prp:energybound}",
    "a random set $W$ would have $E(W)\\approx |W|^4/T_1$",
    "essentially tight if the $R$ function",
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


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == {"implementation": "CPython", "python": EXPECTED_PYTHON, "optimization_level": 0}, "P1R preregistration v2 requires non-optimized CPython 3.12.3")
    return runtime


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def check_current_program_text(text: str) -> dict[str, str]:
    value = normalized(text)
    clauses = {
        "p1r_active": "| p1r | active |",
        "fs_branch": "p1r-fs: fixed-splice obstruction",
        "crr_branch": "p1r-crr: critical rational/random compatibility",
        "crr_pre_search": "before any search, a versioned preregistration must freeze:",
        "no_p2_selection": "no p2a/p2b/p2c route is presently selected.",
    }
    for label, clause in clauses.items():
        require(clause in value, f"current PROGRAM semantic clause missing: {label}")
    return {label: "PRESENT" for label in clauses}


def scale_bookkeeping() -> dict[str, Any]:
    e = {"T_global": 13, "U": 12, "H": 12, "L": 10, "R_cardinality": 8, "M": 2, "Q": 4, "V": 7, "E_formal": 20, "R_over_M": 6}
    sigma = Fraction(7, 10)
    lv = [2 * e["L"] - 2 * e["V"], Fraction(18 * e["L"], 5) - 4 * e["V"], e["H"] + Fraction(12 * e["L"], 5) - 4 * e["V"]]
    energy = [e["R_cardinality"] + e["L"] * (4 - 4 * sigma), Fraction(21 * e["R_cardinality"], 8) + Fraction(e["H"], 4) + e["L"] * (1 - 2 * sigma), 3 * e["R_cardinality"] + e["L"] * (1 - 2 * sigma)]
    four_s3 = [2 * e["H"] + Fraction(3 * e["R_cardinality"], 2), e["H"] + e["R_cardinality"] + e["L"] * (3 - 2 * sigma), e["H"] + 2 * e["R_cardinality"] + e["L"] * (Fraction(3, 2) - sigma), Fraction(9 * e["H"], 8) + Fraction(29 * e["R_cardinality"], 16) + e["L"] * (Fraction(3, 2) - sigma)]
    require(lv == [6, 8, 8], "large-values scale mismatch")
    require(energy == [20, 20, 20], "energy scale mismatch")
    require(four_s3 == [36, 36, 36, 36], "four-term S3 scale mismatch")
    require(e["L"] >= Fraction(3 * e["H"], 4), "four-term S3 N>=T^(3/4) range mismatch")
    return {"epistemic_status": "PROVED", "claim_boundary": "Exact substitution into pinned upper-bound formulas only; no lower bound, common coefficient/set family, or saturation conclusion.", "source_variable_relabeling": {"source_interval_T": "H", "source_polynomial_N": "L", "source_R_function": "mathcal_R_W", "project_cardinality": "R_cardinality"}, "monomial_scales": e, "four_term_source": "GM Proposition prpstn:S3", "four_term_range_check": "L=H^(5/6)>=H^(3/4)", "large_values_term_exponents_in_v": [str(x) for x in lv], "energy_term_exponents_in_v": [str(x) for x in energy], "four_term_s3_exponents_in_v": [str(x) for x in four_s3]}


def source_ledger() -> list[dict[str, Any]]:
    return [
        {"id": "HUX-ING", "epistemic_status": "PROVED", "locator": "Huxley (1.8), classical ledger", "hypotheses": ["1/2 <= sigma <= 3/4"], "permitted_use": "retained P1R-FS left coefficient only"},
        {"id": "GM-T1.1", "epistemic_status": "PROVED", "locator": "GM TeX lines 68--81, thrm:LargeValues", "hypotheses": ["|b_n| <= 1", "1-separated points in [0,T]", "values at least V"], "permitted_use": "formal CRR large-value bookkeeping"},
        {"id": "GM-AFF", "epistemic_status": "PROVED", "locator": "GM TeX lines 1408--1412, propsumaff", "hypotheses": ["f non-negative", "support u asymp 1", "Fourier decay"], "permitted_use": "formal affine scale only; arbitrary f is not automatically |mathcal_R_W|^2"},
        {"id": "GM-S3-REFINED-TWO-TERM", "epistemic_status": "PROVED", "locator": "GM TeX lines 1684--1692, prpstnS3", "hypotheses": ["W is T^epsilon-separated", "interval length T"], "statement": "two-term refined S3 upper bound", "permitted_use": "separate two-term source record"},
        {"id": "GM-S3-FOUR-TERM", "epistemic_status": "PROVED", "locator": "GM TeX lines 1828--1835, prpstn:S3", "hypotheses": ["N >= T^(3/4)"], "statement": "four-term S3 upper bound", "permitted_use": "critical four-term monomial bookkeeping after L=H^(5/6) range check"},
        {"id": "GM-P11.1", "epistemic_status": "PROVED", "locator": "GM TeX lines 1803--1810, prp:energybound", "hypotheses": ["|b_n| <= 1", "W 1-separated in interval length T", "|D(t)| >= N^sigma", "T^(3/4) <= N <= T"], "permitted_use": "formal energy balance only"},
        {"id": "GM-CRITICAL-REMARK", "epistemic_status": "OBSERVED", "locator": "GM TeX lines 2398--2399", "hypotheses": [], "statement": "likely/essentially-tight random/rational discussion", "permitted_use": "motivation only"},
    ]


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require("TO_BE_FILLED" not in expected, f"unsealed expected hash: {label}")
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    snapshot = load_json(INPUTS["authorization_snapshot"][0])
    require(snapshot.get("artifact_id") == "cycle-4-p1r-authorization-snapshot-v1", "authorization snapshot identity mismatch")
    require(snapshot.get("observed_plan", {}).get("historical_sha256") == "ce8cfb2c4c196b53a0e823667da2ce4e840d7ce18c754a9be1423064d9fce479", "historical authorization hash mismatch")
    hostile = load_json(INPUTS["v1_hostile_artifact"][0])
    require(hostile.get("status") == "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS", "v1 hostile FAIL record mismatch")
    tex = INPUTS["gm_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in tex, f"GM source fragment missing: {fragment}")
    live_program = check_current_program_text((ROOT / "PROGRAM.md").read_text(encoding="utf-8"))
    return {"artifact_id": "cycle-4-p1r-preregistration-v2", "epistemic_status": "OBSERVED", "status": "SEALED_PREREGISTRATION", "discovery_authorization": "PROHIBITED_PENDING_CRR_FORMALIZATION", "claim_boundary": "Corrected Cycle 4 P1R preregistration only. It preserves v1, records the hostile defects, seals no P1R-FS obstruction theorem, and authorizes no CRR discovery/search.", "runtime": runtime, "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)}, "frozen_hashes": frozen, "current_program_semantic_check": {"path": "PROGRAM.md", "byte_hash_pinned": False, "clauses": live_program}, "correction": {"supersedes_for_continuing_replay": "cycle-4-p1r-preregistration-v1", "preserves_v1": True, "hostile_status": hostile["status"], "defects_corrected": ["valid documented replay CLI", "immutable authorization snapshot plus semantic live PROGRAM check", "four-term S3 attribution to prpstn:S3 with N>=T^(3/4)", "unexecuted FS gate status"]}, "source_hypothesis_ledger": source_ledger(), "p1r_fs": {"identity_algebra": {"epistemic_status": "PROVED", "identity": "30/13-3/(2-sigma)=30(7/10-sigma)/(13(2-sigma))", "scope": "exact pinned algebra only"}, "gate_status": "PREREGISTERED_UNEXECUTED", "completed_theorem": False, "required_completion": "two independent exact routes, reconciliation, and hostile audit", "claim_boundary": "No scoped obstruction theorem is recorded."}, "p1r_crr": {"epistemic_status": "CONJECTURED", "formalization_gate": {"status": "FORMALIZATION_REQUIRED_NO_SEARCH", "search_authorized": False, "unsealed_required_fields": ["normalizations", "classification branch and quantifiers", "rational predicate/smoothing/separation", "families/ranges/thresholds", "failed-row rule/resource cap/RNG seed/certification margin", "independent analytic obligations"]}, "scale_bookkeeping": scale_bookkeeping()}, "resource_policy": {"status": "UNSEALED_NO_COMPUTATION", "rng_seed": None, "finite_resource_cap": None, "certification_margin": None}, "falsifier": "Any frozen-byte mismatch, hostile-record mismatch, source/range mismatch, or missing live PROGRAM semantic clause invalidates v2. No formal exponent balance establishes a Guth--Maynard saturation theorem.", "replay": {"write_command": "python3 proof/build_cycle_4_p1r_preregistration_v2.py --write", "check_command": "python3 proof/build_cycle_4_p1r_preregistration_v2.py --check"}}


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
        require(not OUTPUT.exists(), "refusing to overwrite P1R preregistration v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "P1R preregistration v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "P1R preregistration v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"], "discovery_authorization": payload["discovery_authorization"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
