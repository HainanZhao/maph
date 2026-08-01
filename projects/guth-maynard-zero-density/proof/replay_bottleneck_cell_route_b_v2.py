#!/usr/bin/env python3
"""Exact Route-B v2 certificate for Guth--Maynard's final bottleneck cell.

The audit evaluates only the displayed terms in Theorem 1.1 and Proposition
11.1 after the parameter substitution stated in the final Remark of section
13.1.  It does not reproduce their proofs, nor the S_1/S_2/S_3 argument.

Run from the repository root:
  python3 projects/guth-maynard-zero-density/proof/replay_bottleneck_cell_route_b_v2.py \
      --write projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-v2-bottleneck-cell.json
  python3 projects/guth-maynard-zero-density/proof/replay_bottleneck_cell_route_b_v2.py \
      --check projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-v2-bottleneck-cell.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE_TARBALL_SHA256 = "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def own_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def linear_table(rows: list[tuple[str, Fraction]]) -> list[dict[str, str]]:
    """Make an exact table; no decimal or sampled comparison is used."""
    return [{"term": label, "U_exponent": q(value), "cleared_twelfths": str(12 * value)} for label, value in rows]


def certificate() -> dict[str, Any]:
    """Evaluate the frozen cell and raise if any exact equality fails."""
    # All lower-case variables are exponents relative to the local interval U.
    sigma = Fraction(7, 10)
    original_n_in_T = Fraction(5, 13)
    local_u_in_T = Fraction(12, 13)
    length = Fraction(5, 6)  # L = U^(5/6)
    value = Fraction(7, 12)  # V = U^(7/12)
    size_w = Fraction(2, 3)  # |W| = U^(2/3)

    # Theorem 1.1: L^2V^-2, L^(18/5)V^-4, U L^(12/5)V^-4.
    theorem_rows = [
        ("L^2*V^-2", 2 * length - 2 * value),
        ("L^(18/5)*V^-4", Fraction(18, 5) * length - 4 * value),
        ("U*L^(12/5)*V^-4", 1 + Fraction(12, 5) * length - 4 * value),
    ]
    theorem_max = max(exponent for _, exponent in theorem_rows)

    # Proposition 11.1: |W|L^(4-4sigma),
    # |W|^(21/8)U^(1/4)L^(1-2sigma), |W|^3L^(1-2sigma).
    energy_rows = [
        ("|W|*L^(4-4*sigma)", size_w + (4 - 4 * sigma) * length),
        (
            "|W|^(21/8)*U^(1/4)*L^(1-2*sigma)",
            Fraction(21, 8) * size_w + Fraction(1, 4) + (1 - 2 * sigma) * length,
        ),
        ("|W|^3*L^(1-2*sigma)", 3 * size_w + (1 - 2 * sigma) * length),
    ]
    energy_max = max(exponent for _, exponent in energy_rows)

    # All assertions are exact identities or exact interval checks.
    assert original_n_in_T * 2 == Fraction(10, 13)
    assert length * local_u_in_T == Fraction(10, 13)
    assert value * local_u_in_T == Fraction(7, 13)
    assert length * sigma == value
    assert Fraction(3, 4) <= length <= 1  # Proposition 11.1 range.
    assert theorem_rows == [
        ("L^2*V^-2", Fraction(1, 2)),
        ("L^(18/5)*V^-4", Fraction(2, 3)),
        ("U*L^(12/5)*V^-4", Fraction(2, 3)),
    ]
    assert theorem_max == size_w
    assert energy_rows == [
        ("|W|*L^(4-4*sigma)", Fraction(5, 3)),
        ("|W|^(21/8)*U^(1/4)*L^(1-2*sigma)", Fraction(5, 3)),
        ("|W|^3*L^(1-2*sigma)", Fraction(5, 3)),
    ]
    assert energy_max == Fraction(5, 3)
    assert Fraction(5, 2) * size_w == 4 * size_w - 1 == energy_max
    local_w_in_T = size_w * local_u_in_T
    subinterval_count_in_T = 1 - local_u_in_T
    total_count_in_T = local_w_in_T + subinterval_count_in_T
    density_target = Fraction(15, 1) * (1 - sigma) / (3 + 5 * sigma)
    assert local_w_in_T == Fraction(8, 13)
    assert subinterval_count_in_T == Fraction(1, 13)
    assert total_count_in_T == density_target == Fraction(9, 13)

    return {
        "artifact_type": "exact-rational-bottleneck-cell-certificate",
        "certificate_version": 2,
        "route": "B",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Exact substitution and cleared-linear-form audit conditional on "
            "the cited Theorem 1.1, Proposition 11.1, and final section-13.1 "
            "Remark. It neither reproves those results nor proves that no "
            "improvement to S_3 or the full method exists."
        ),
        "source_inputs": {
            "arxiv_version": "2405.20552v2",
            "source_tarball_sha256": SOURCE_TARBALL_SHA256,
            "tex_member": "LargevaluesDirichlet17.tex",
            "tex_member_sha256": SOURCE_TEX_SHA256,
            "checked_locations": [
                "Theorem 1.1, TeX lines 64--79",
                "Proposition 11.1 / equation (11.1), TeX lines 1785--1804",
                "final Remark in section 13.1, TeX line 2398",
            ],
        },
        "frozen_cell": {
            "sigma": q(sigma),
            "original_N_in_T": q(original_n_in_T),
            "squared_length_L_in_T": "10/13",
            "local_interval_U_in_T": q(local_u_in_T),
            "L_in_U": q(length),
            "V_in_U": q(value),
            "V_equals_L_to_sigma": True,
            "W_in_U": q(size_w),
            "energy_in_U": q(energy_max),
            "energy_equivalences": ["|W|^(5/2) = U^(5/3)", "|W|^4/U = U^(5/3)"],
        },
        "theorem_1_1_term_table": {
            "hypotheses_used": [
                "|b_n| <= 1",
                "large-value points are 1-separated in an interval of length U",
                "the polynomial has length L and values at least V",
            ],
            "rows": linear_table(theorem_rows),
            "cleared_comparisons": [
                "12*(2/3) - 12*(1/2) = 2 > 0",
                "12*(2/3) - 12*(2/3) = 0 (tie of the second and third terms)",
            ],
            "max_U_exponent": q(theorem_max),
            "conclusion": "Theorem 1.1 returns the local scale |W| <= U^(2/3+o(1)).",
        },
        "proposition_11_1_energy_table": {
            "hypotheses_checked": {
                "sigma_greater_than_one_half": True,
                "L_in_required_range_U_to_3_4_through_U": True,
                "one_separation_and_coefficient_bound": "inherited stated hypotheses",
            },
            "rows": linear_table(energy_rows),
            "cleared_comparisons": [
                "12*(5/3) = 20 for each of all three Proposition 11.1 terms",
                "all three terms tie exactly at U^(5/3)",
            ],
            "max_U_exponent": q(energy_max),
            "matches_final_remark_energy": True,
        },
        "local_to_global_count": {
            "local_W_in_T_exponent": q(local_w_in_T),
            "number_of_U_subintervals_in_T_exponent": q(subinterval_count_in_T),
            "combined_T_exponent": q(total_count_in_T),
            "theorem_1_2_density_exponent_at_sigma": q(density_target),
            "exact_match": True,
            "interpretation": (
                "Up to the source's T^o(1) factors and endpoint bookkeeping, "
                "U^(2/3) local points across T/U subintervals give T^(9/13), "
                "the Theorem 1.2 target at sigma=7/10."
            ),
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": own_sha256(),
            "write_command": (
                "python3 projects/guth-maynard-zero-density/proof/"
                "replay_bottleneck_cell_route_b_v2.py --write "
                "projects/guth-maynard-zero-density/artifacts/"
                "cycle-1-route-b-v2-bottleneck-cell.json"
            ),
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
