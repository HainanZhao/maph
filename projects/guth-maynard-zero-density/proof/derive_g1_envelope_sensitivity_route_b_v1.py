#!/usr/bin/env python3
"""Route B: cleared-identity audit for G1 envelope sensitivity.

Unlike Route A, this route works from sign factorizations and cleared
residuals.  Its counterfactual parameter is explicitly formal only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json"
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
TAR = ROOT / "artifacts/sources/arxiv-2405.20552v2.tar"
OUTPUT = ROOT / "artifacts/g1-envelope-sensitivity-route-b-v1.json"

PINS = {
    "atlas_v2": (ATLAS, "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
    "preregistration_v1": (PREREG, "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "guth_maynard_tex": (TEX, "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "guth_maynard_source_tar": (TAR, "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def f(value: str) -> Fraction:
    numerator, denominator = value.split("/")
    return Fraction(int(numerator), int(denominator))


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maxima_from_residuals(s: Fraction, n: Fraction, v: Fraction, w: Fraction) -> tuple[list[str], list[str], list[str], list[str]]:
    # Use a different representation from Route A: pairwise differences give
    # all order relations.  Values are reconstructed only after the signs are
    # determined, as a transcription guard.
    a = {
        "A1": 2*n*(1-v), "A2": n*(Fraction(18, 5)-4*v),
        "A3": 1+n*(Fraction(12, 5)-4*v),
    }
    c = {
        "C1": 2*n*(1-v), "C2": 1+n*(1-2*v), "C3": 1+n*(4-6*v),
    }
    e = {
        "E1": w+n*(4-4*s), "E2": Fraction(21, 8)*w+Fraction(1, 4)+n*(1-2*s),
        "E3": 3*w+n*(1-2*s),
    }
    require(a["A1"]-a["A2"] == 2*n*(v-Fraction(4, 5)), "A12 factorization fails")
    require(a["A1"]-a["A3"] == n*(2*v-Fraction(2, 5))-1, "A13 factorization fails")
    require(a["A2"]-a["A3"] == Fraction(6, 5)*n-1, "A23 factorization fails")
    require(c["C1"]-c["C2"] == n-1, "C12 factorization fails")
    require(c["C1"]-c["C3"] == 2*n*(2*v-1)-1, "C13 factorization fails")
    require(c["C2"]-c["C3"] == n*(4*v-3), "C23 factorization fails")
    require(e["E1"]-e["E2"] == n*(3-2*s)-Fraction(13, 8)*w-Fraction(1, 4), "E12 factorization fails")
    require(e["E1"]-e["E3"] == n*(3-2*s)-2*w, "E13 factorization fails")
    require(e["E2"]-e["E3"] == Fraction(1, 4)-Fraction(3, 8)*w, "E23 factorization fails")
    a_max = [name for name, value in a.items() if value == max(a.values())]
    c_inner_value = min(c["C2"], c["C3"])
    c_inner = [name for name in ("C2", "C3") if c[name] == c_inner_value]
    c_outer = [name for name, value in {"C1": c["C1"], "min(C2,C3)": c_inner_value}.items() if value == max(c["C1"], c_inner_value)]
    e_max = [name for name, value in e.items() if value == max(e.values())]
    return a_max, c_outer, c_inner, e_max


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "Route B forbids -O/-OO")
    require(platform.python_implementation() == "CPython" and platform.python_version() == "3.12.3", "Route B requires CPython 3.12.3")
    hashes = {}
    for label, (path, expected) in PINS.items():
        observed = digest(path)
        require(observed == expected, "frozen input hash mismatch: " + str(path))
        hashes[label] = observed
    atlas = json.loads(ATLAS.read_text())
    require(atlas["artifact_id"] == "cycle-3-g1-exact-structural-atlas-v2" and atlas["epistemic_status"] == "PROVED", "wrong exact atlas")
    ac, cc, ec = Counter(), Counter(), Counter()
    zeroes = []
    for row in atlas["local_rows"]:
        s, n, v, w = (f(row[key]) for key in ("s", "n", "v", "w"))
        a_max, c_outer, c_inner, e_max = maxima_from_residuals(s, n, v, w)
        require(a_max == row["large_values"]["max_tie_set"], "Route B A labels mismatch: " + row["id"])
        require(c_outer == row["classical"]["outer_max_tie_set"] and c_inner == row["classical"]["inner_min_tie_set"], "Route B C labels mismatch: " + row["id"])
        ac[tuple(a_max)] += 1
        cc[(tuple(c_outer), tuple(c_inner))] += 1
        if row["energy_eligible"]:
            require(e_max == row["energy"]["max_tie_set"], "Route B E labels mismatch: " + row["id"])
            ec[tuple(e_max)] += 1
    for row in atlas["transfer_rows"]:
        s, q_value = f(row["s"]), f(row["q"])
        ell = Fraction(10, 1)/(6+10*s)
        upper = Fraction(15, 1)/(6+10*s)
        b = Fraction(15, 1)*(1-s)/(3+5*s)
        alpha = b/(Fraction(18, 5)-4*s)
        residuals = row["B_minus_source_term"]
        if row["branch"] == "q<=alpha":
            expected = {
                "LV1": 2*(1-s)*(upper-q_value),
                "LV2": (Fraction(18, 5)-4*s)*(alpha-q_value),
                "LV3": (4*s-Fraction(12, 5))*(q_value-ell),
            }
        else:
            expected = {
                "MVT1": 2*(1-s)*(upper-q_value),
                "MVT2": b-(1+(1-2*s)*q_value),
            }
        require({name: q(value) for name, value in expected.items()} == residuals, "Route B transfer residual mismatch: " + row["id"])
        for name, value in expected.items():
            if value == 0:
                require(name == "LV3" and q_value == ell and row["k"] == 2 and f(row["n0"]) == ell/2, "bad zero residual structure: " + row["id"])
                zeroes.append({"id": row["id"], "s": row["s"], "term": name, "q": row["q"], "ell": q(ell)})
    require(len(zeroes) == 11 and len({item["s"] for item in zeroes}) == 11, "Route B zero-residual coverage fails")
    critical = next(row for row in atlas["transfer_rows"] if row["id"] == "T:s=7/10;n0=5/13;k=2;q=10/13")
    require(critical["B_minus_source_term"] == {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"}, "critical residual barrier fails")
    # Ingham/Guth--Maynard junction, independently from the atlas formulas.
    h = Fraction(1, 1000)
    s0 = Fraction(7, 10)
    in_gham_gap = Fraction(30, 13) - Fraction(3, 1)/(2-(s0-h))
    require(in_gham_gap == 300*h/(169+130*h), "endpoint gap identity fails")
    return {
        "artifact_id": "g1-envelope-sensitivity-route-b-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED cleared-rational-identity audit conditional on the hash-pinned source and atlas. The formal mu parameter below assumes, but does not establish, a strengthened third Theorem 1.1 term; it gives no density or short-interval theorem.",
        "frozen_inputs": {"hashes": hashes, "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization": sys.flags.optimize}},
        "cleared_identity_map": {"A": ["A1-A2=2n(v-4/5)", "A1-A3=n(2v-2/5)-1", "A2-A3=6n/5-1"], "C": ["C1-C2=n-1", "C1-C3=2n(2v-1)-1", "C2-C3=n(4v-3)"], "E": ["E1-E2=n(3-2s)-13w/8-1/4", "E1-E3=n(3-2s)-2w", "E2-E3=1/4-3w/8"], "transfer": ["B-LV1=2(1-s)(u-q)", "B-LV2=(18/5-4s)(alpha-q)", "B-LV3=(4s-12/5)(q-ell)"]},
        "activity_count_replay": {"A_max_tie_counts": {"|".join(key): value for key, value in sorted(ac.items())}, "C_outer_inner_tie_counts": {"outer="+"|".join(key[0])+";inner="+"|".join(key[1]): value for key, value in sorted(cc.items())}, "E_max_tie_counts_on_diagonal": {"|".join(key): value for key, value in sorted(ec.items())}},
        "zero_B_residuals": {"count": len(zeroes), "all_term_labels": ["LV3"], "all_characterization": "For each frozen s, exactly n0=ell(s)/2 and k=2 give q=ell(s), hence B-LV3=0.", "rows": zeroes},
        "critical_barrier": {"critical_transfer_id": critical["id"], "B_minus_LV1": "3/13", "B_minus_LV2": "1/13", "B_minus_LV3": "0/1", "required_term": "Theorem 1.1 third term T*N^(12/5)*V^(-4) (LV3).", "formal_mu_cap_before_LV2": "mu<=1/10, since LV3 falls by (10/13)mu and LV2 slack is 1/13."},
        "endpoint_and_conditional_propagation": {"published_endpoint_no_effect": {"status": "PROVED", "identity": "30/13-3/(2-(7/10-h))=300h/(169+130h)", "conclusion": "The unchanged Ingham side has left supremum 30/13, so endpoint-only or right-only improvement cannot lower the uniform global coefficient."}, "formal_mu_model": {"premise_tag": "CONJECTURED", "term_change": "12/5 -> 12/5-mu in LV3, with a valid left-neighborhood zero-detection propagation assumed separately", "junction_polynomial": "300h^2+(90-50mu)h-65mu=0", "first_order": {"h": "13mu/18+O(mu^2)", "global_density_coefficient": "30/13-50mu/39+O(mu^2)", "formal_theta": "17/30-13mu/54+O(mu^2)"}, "necessary_left_extent": "at least h(mu)>0, the positive root of the stated polynomial; currently this is not supplied by the published s>=7/10 branch."}},
        "falsifier": "A different zero-residual label, failure of a cleared residual identity, an atlas-label disagreement, or a proposed third-term gain without the separately necessary left extension refutes the respective conclusion.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_b_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_b_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "Route B envelope-sensitivity artifact mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
