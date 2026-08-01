#!/usr/bin/env python3
"""Route A: direct exact sensitivity map for the frozen G1 atlas.

This is a conditional rational-exponent audit.  It identifies the active
published terms and derives implications of an explicitly counterfactual
improvement parameter; it does not claim that such an improvement exists.
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
OUTPUT = ROOT / "artifacts/g1-envelope-sensitivity-route-a-v1.json"

PINS = {
    "atlas_v2": (ATLAS, "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
    "preregistration_v1": (PREREG, "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "guth_maynard_tex": (TEX, "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "guth_maynard_source_tar": (TAR, "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def frac(value: str) -> Fraction:
    numerator, denominator = value.split("/")
    return Fraction(int(numerator), int(denominator))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_local(s: Fraction, n: Fraction, v: Fraction, w: Fraction) -> dict[str, dict[str, Fraction]]:
    a = {
        "A1": 2 * n * (1 - v),
        "A2": n * (Fraction(18, 5) - 4 * v),
        "A3": 1 + n * (Fraction(12, 5) - 4 * v),
    }
    c = {
        "C1": 2 * n * (1 - v),
        "C2": 1 + n * (1 - 2 * v),
        "C3": 1 + n * (4 - 6 * v),
    }
    e = {
        "E1": w + n * (4 - 4 * s),
        "E2": Fraction(21, 8) * w + Fraction(1, 4) + n * (1 - 2 * s),
        "E3": 3 * w + n * (1 - 2 * s),
    }
    return {"A": a, "C": c, "E": e}


def tie(values: dict[str, Fraction], extreme: Fraction) -> list[str]:
    return [name for name, value in values.items() if value == extreme]


def local_summary(atlas: dict[str, Any]) -> dict[str, Any]:
    a_count: Counter[tuple[str, ...]] = Counter()
    c_count: Counter[tuple[tuple[str, ...], tuple[str, ...]]] = Counter()
    e_count: Counter[tuple[str, ...]] = Counter()
    for row in atlas["local_rows"]:
        s, n, v, w = (frac(row[key]) for key in ("s", "n", "v", "w"))
        terms = direct_local(s, n, v, w)
        a_active = tie(terms["A"], max(terms["A"].values()))
        inner = min(terms["C"]["C2"], terms["C"]["C3"])
        outer = max(terms["C"]["C1"], inner)
        outer_active = [name for name, value in {"C1": terms["C"]["C1"], "min(C2,C3)": inner}.items() if value == outer]
        inner_active = tie({"C2": terms["C"]["C2"], "C3": terms["C"]["C3"]}, inner)
        require(a_active == row["large_values"]["max_tie_set"], "Route A A-active mismatch: " + row["id"])
        require(outer_active == row["classical"]["outer_max_tie_set"], "Route A C-outer mismatch: " + row["id"])
        require(inner_active == row["classical"]["inner_min_tie_set"], "Route A C-inner mismatch: " + row["id"])
        a_count[tuple(a_active)] += 1
        c_count[(tuple(outer_active), tuple(inner_active))] += 1
        if row["energy_eligible"]:
            e_active = tie(terms["E"], max(terms["E"].values()))
            require(e_active == row["energy"]["max_tie_set"], "Route A E-active mismatch: " + row["id"])
            e_count[tuple(e_active)] += 1
        else:
            require("energy" not in row, "off-diagonal row carries forbidden energy label")
    return {
        "A_max_tie_counts": {"|".join(key): value for key, value in sorted(a_count.items())},
        "C_outer_inner_tie_counts": {"outer=" + "|".join(key[0]) + ";inner=" + "|".join(key[1]): value for key, value in sorted(c_count.items())},
        "E_max_tie_counts_on_diagonal": {"|".join(key): value for key, value in sorted(e_count.items())},
        "off_diagonal_energy_forbidden_rows": sum(not row["energy_eligible"] for row in atlas["local_rows"]),
    }


def transfer_zeroes(atlas: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for row in atlas["transfer_rows"]:
        s, q_value = frac(row["s"]), frac(row["q"])
        ell = Fraction(10, 1) / (6 + 10 * s)
        zeros = [name for name, residual in row["B_minus_source_term"].items() if frac(residual) == 0]
        if zeros:
            require(zeros == ["LV3"], "a non-third source term has zero B residual: " + row["id"])
            require(q_value == ell, "a zero residual does not occur at q=ell: " + row["id"])
            require(row["branch"] == "q<=alpha" and row["k"] == 2, "zero residual has wrong transfer branch: " + row["id"])
            require(frac(row["n0"]) == ell / 2, "zero residual does not have n0=ell/2: " + row["id"])
            output.append({"id": row["id"], "s": row["s"], "n0": row["n0"], "k": row["k"], "q": row["q"], "zero_terms": zeros, "identity": "B(s)-LV3=(4s-12/5)(q-ell(s))=0"})
    require(len(output) == 11, "frozen 11-point s grid does not yield exactly 11 zero residual rows")
    return output


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "Route A forbids -O/-OO")
    require(platform.python_implementation() == "CPython" and platform.python_version() == "3.12.3", "Route A requires CPython 3.12.3")
    hashes = {}
    for label, (path, expected) in PINS.items():
        actual = digest(path)
        require(actual == expected, "frozen input hash mismatch: " + str(path))
        hashes[label] = actual
    atlas = json.loads(ATLAS.read_text())
    require(atlas["artifact_id"] == "cycle-3-g1-exact-structural-atlas-v2" and atlas["epistemic_status"] == "PROVED", "wrong G1 exact atlas authority")
    require(atlas["counts"] == {"local_total": 7744, "local_energy_eligible": 704, "local_energy_ineligible": 7040, "transfer_total": 560, "transfer_exact_power_scale": 549, "transfer_asymptotic_endpoint_only": 11, "transfer_by_branch": {"q<=alpha": 429, "q>alpha": 131}}, "unexpected G1 atlas scope")
    s, n, v, w = Fraction(7, 10), Fraction(5, 6), Fraction(7, 10), Fraction(2, 3)
    critical = direct_local(s, n, v, w)
    require(critical["A"] == {"A1": Fraction(1, 2), "A2": Fraction(2, 3), "A3": Fraction(2, 3)}, "critical A terms fail")
    require(critical["C"] == {"C1": Fraction(1, 2), "C2": Fraction(2, 3), "C3": Fraction(5, 6)}, "critical C terms fail")
    require(critical["E"] == {"E1": Fraction(5, 3), "E2": Fraction(5, 3), "E3": Fraction(5, 3)}, "critical E terms fail")
    anchor = next(row for row in atlas["transfer_rows"] if row["id"] == "T:s=7/10;n0=5/13;k=2;q=10/13")
    require(anchor["B"] == "9/13" and anchor["source_term_exponents"] == {"LV1": "6/13", "LV2": "8/13", "LV3": "9/13"}, "critical transfer terms fail")
    require(anchor["B_minus_source_term"] == {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"}, "critical transfer residuals fail")
    zero_rows = transfer_zeroes(atlas)
    # Counterfactual notation only: decrease the N-exponent of the source's
    # third term TN^(12/5-4s)V^-4 by mu.  At q=ell(7/10)=10/13 this is a
    # T-exponent decrease delta=10*mu/13.  No such inequality is asserted.
    mu_cap = Fraction(1, 10)
    point_slope = Fraction(100, 39)
    h_slope = Fraction(13, 18)
    theta_slope = Fraction(13, 54)
    return {
        "artifact_id": "g1-envelope-sensitivity-route-a-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED exact rational activity, residual, and conditional-exponent algebra, conditional on the directly hash-pinned Guth--Maynard formulas and G1 atlas v2. No improved Theorem 1.1 term, density theorem, short-interval theorem, extremizer, or saturation theorem is claimed.",
        "frozen_inputs": {"hashes": hashes, "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization": sys.flags.optimize}},
        "named_source_term": {"label": "LV3", "Theorem_1_1_term": "T*N^(12/5)*V^(-4)", "applied_at_zero_detection": "T^(1+q*(12/5-4s))", "reason": "At every frozen zero-residual transfer row, and in particular at the critical transfer anchor, LV3 alone equals B(s)."},
        "symbolic_loci": {
            "A1_minus_A2": "2*n*(v-4/5)",
            "A1_minus_A3": "n*(2*v-2/5)-1",
            "A2_minus_A3": "6*n/5-1",
            "C1_minus_C2": "n-1",
            "C1_minus_C3": "2*n*(2*v-1)-1",
            "C2_minus_C3": "n*(4*v-3)",
            "E1_minus_E2": "n*(3-2*s)-13*w/8-1/4",
            "E1_minus_E3": "n*(3-2*s)-2*w",
            "E2_minus_E3": "1/4-3*w/8",
        },
        "activity_counts": local_summary(atlas),
        "critical_local_cell": {"coordinates": {"s": q(s), "n": q(n), "v": q(v), "w": q(w)}, "A_terms": {key: q(value) for key, value in critical["A"].items()}, "A_active": ["A2", "A3"], "C_terms": {key: q(value) for key, value in critical["C"].items()}, "C_active": {"outer": ["min(C2,C3)"], "inner": ["C2"]}, "E_terms": {key: q(value) for key, value in critical["E"].items()}, "E_active": ["E1", "E2", "E3"]},
        "zero_B_residual_transfer_rows": zero_rows,
        "critical_transfer": {"coordinates": {key: anchor[key] for key in ("s", "n0", "k", "q", "ell", "u", "alpha", "branch", "provenance")}, "B": anchor["B"], "term_exponents": anchor["source_term_exponents"], "B_minus_term": anchor["B_minus_source_term"], "bottleneck": "LV3"},
        "counterfactual_sensitivity": {
            "premise_tag": "CONJECTURED",
            "premise": "For a parameter mu>0, replace only the N-exponent 12/5 in the third Theorem 1.1 term by 12/5-mu in a range sufficient for the stated transfer. This is a formal parameterization, not an asserted bound.",
            "critical_anchor": {"absolute_T_exponent_gain": "delta=10*mu/13", "post_improvement_max_exponent": "max(6/13,8/13,9/13-10*mu/13)", "LV3_active_range": "0<=mu<=1/10", "next_barrier_after_mu_1_10": "LV2 at 8/13", "conditional_pointwise_density_coefficient": "30/13-100*mu/39 for 0<=mu<=1/10", "first_order_pointwise_coefficient_gain": "100*mu/39"},
            "published_range_no_effect": {"status": "PROVED", "statement": "A gain confined to s=7/10 or to the published Guth--Maynard side s>=7/10 cannot by itself yield a uniform coefficient 30/13-eta: the retained Ingham side s<7/10 has supremum 30/13.", "identity": "30/13-3/(2-s)=30*(7/10-s)/(13*(2-s))", "falsifier_for_any_eta": "for 0<eta<30/13 choose 0<h<169*eta/(300-130*eta); then s=7/10-h and 3/(2-s)>30/13-eta"},
            "conditional_left_extension": {"extra_premise_tag": "CONJECTURED", "extra_premise": "The same third-term gain is propagated through a valid zero-detection proof on [7/10-h(mu),7/10], with all non-exponent hypotheses and the complete short-interval argument separately checked.", "crossing_equation": "300*h^2+(90-50*mu)*h-65*mu=0", "positive_root": "h(mu)=(50*mu-90+sqrt((90-50*mu)^2+78000*mu))/600", "conditional_envelope_coefficient": "3/(13/10+h(mu))", "first_order_envelope_coefficient": "30/13-50*mu/39+O(mu^2)", "formal_theta_map_only": "17/30-h(mu)/3 = 17/30-13*mu/54+O(mu^2)", "warning": "The theta display is only the formal density-to-threshold algebra. It is not a short-interval theorem; the full explicit-formula proof is required by PLAN.md."},
        },
        "falsifier": "Any non-LV3 zero residual, mismatch in the 11 q=ell rows, failure of a stated cleared identity, or a claimed gain that does not extend left of s=7/10 as required by the conditional crossing invalidates the corresponding sensitivity conclusion.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_a_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_a_v1.py --check"},
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
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "Route A envelope-sensitivity artifact mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
