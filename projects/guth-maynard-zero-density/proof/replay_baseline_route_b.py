#!/usr/bin/env python3
"""Exact route-B audit of the published zero-density baseline.

This is deliberately a small, source-free rational-arithmetic certificate.
It does not reconstruct the large-values or explicit-formula arguments.  Its
inputs are the three published zero-density estimates and the two sufficient
criteria stated in the source proof; its output checks every comparison and
threshold conversion needed for the frozen baseline.

Run from the repository root:
  python3 projects/guth-maynard-zero-density/proof/replay_baseline_route_b.py \
      --write projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-baseline.json
  python3 projects/guth-maynard-zero-density/proof/replay_baseline_route_b.py \
      --check projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-baseline.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "artifacts" / "cycle-1-route-b-baseline.json"
SOURCE_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE_TARBALL_SHA256 = "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"


def q(value: Fraction) -> str:
    """Serialize a rational exactly, with integers kept as integers."""
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def in_ingham(sigma: Fraction) -> Fraction:
    return Fraction(3, 1) / (Fraction(2, 1) - sigma)


def guth_maynard(sigma: Fraction) -> Fraction:
    return Fraction(15, 1) / (Fraction(3, 1) + 5 * sigma)


def huxley(sigma: Fraction) -> Fraction:
    return Fraction(3, 1) / (3 * sigma - 1)


def critical_large_values_cell() -> dict[str, Any]:
    """Certify the exact T-exponents at N=T^(4/5), V=N^(3/4)."""
    n_exponent = Fraction(4, 5)
    v_as_power_of_n = Fraction(3, 4)
    v_exponent = n_exponent * v_as_power_of_n

    # The three Theorem 1.1 terms are N^2 V^-2,
    # N^(18/5) V^-4, and T N^(12/5) V^-4.
    gm_terms = {
        "N^2*V^-2": 2 * n_exponent - 2 * v_exponent,
        "N^(18/5)*V^-4": Fraction(18, 5) * n_exponent - 4 * v_exponent,
        "T*N^(12/5)*V^-4": Fraction(1, 1) + Fraction(12, 5) * n_exponent - 4 * v_exponent,
    }
    # The classical bound is N^2 V^-2 plus T times the minimum of
    # N V^-2 and N^4 V^-6.  At this cell the two min-branches tie exactly.
    classical_terms = {
        "N^2*V^-2": 2 * n_exponent - 2 * v_exponent,
        "T*N*V^-2": Fraction(1, 1) + n_exponent - 2 * v_exponent,
        "T*N^4*V^-6": Fraction(1, 1) + 4 * n_exponent - 6 * v_exponent,
    }
    gm_max = max(gm_terms.values())
    classical_max = max(classical_terms.values())
    assert n_exponent == Fraction(4, 5)
    assert v_exponent == Fraction(3, 5)
    assert gm_terms == {
        "N^2*V^-2": Fraction(10, 25),
        "N^(18/5)*V^-4": Fraction(12, 25),
        "T*N^(12/5)*V^-4": Fraction(13, 25),
    }
    assert classical_terms == {
        "N^2*V^-2": Fraction(10, 25),
        "T*N*V^-2": Fraction(15, 25),
        "T*N^4*V^-6": Fraction(15, 25),
    }
    assert gm_max == Fraction(13, 25)
    assert classical_max == Fraction(3, 5)
    assert classical_max - gm_max == Fraction(2, 25)
    return {
        "parameterization": {
            "N": "T^(4/5)",
            "V": "N^(3/4) = T^(3/5)",
        },
        "published_hypotheses_used": [
            "|b_n| <= 1",
            "the t_r are 1-separated points in [0,T]",
            "|sum_(n=N)^(2N) b_n n^(i*t_r)| >= V for every r",
        ],
        "guth_maynard_theorem_1_1": {
            "terms": {name: q(value) for name, value in gm_terms.items()},
            "term_order_certificate": [
                "13/25 - 12/25 = 1/25 > 0",
                "12/25 - 10/25 = 2/25 > 0",
            ],
            "max_T_exponent": q(gm_max),
        },
        "classical_equation_1_1": {
            "terms_before_minimum": {name: q(value) for name, value in classical_terms.items()},
            "min_branch_equality": "15/25 = 15/25",
            "max_T_exponent": q(classical_max),
        },
        "strict_gain": {
            "classical_minus_guth_maynard": q(classical_max - gm_max),
            "conclusion": "T^(13/25+o(1)) versus T^(3/5+o(1)); gain 2/25 in the T exponent.",
        },
    }


def certificate() -> dict[str, Any]:
    """Return a deterministic, exact certificate or raise AssertionError."""
    sigma_star = Fraction(7, 10)
    b = Fraction(30, 13)
    uniform_theta = Fraction(1, 1) - Fraction(1, 1) / b
    almost_all_theta = Fraction(1, 1) - Fraction(2, 1) / b

    # Cross-multiplication is legitimate in each stated interval: every
    # denominator listed below is strictly positive there.
    assert in_ingham(sigma_star) == guth_maynard(sigma_star) == b
    assert huxley(Fraction(4, 5)) < b
    assert in_ingham(Fraction(1, 2)) < b
    assert guth_maynard(Fraction(4, 5)) < b
    assert huxley(Fraction(1, 1)) < b
    assert uniform_theta == Fraction(17, 30)
    assert almost_all_theta == Fraction(2, 15)
    assert Fraction(1, 1) / b == Fraction(13, 30)
    assert Fraction(2, 1) / b == Fraction(13, 15)

    # These are the cleared numerator polynomials for the comparisons.
    # Their listed interval signs establish the complete case split, not a
    # floating-point sampling of it.
    return {
        "artifact_type": "exact-rational-baseline-certificate",
        "certificate_version": 1,
        "route": "B",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Exact algebraic audit conditional on the cited published "
            "zero-density estimates and the stated sufficient criteria in "
            "their short-interval proof. It is not an independent proof of "
            "those analytic estimates or of either short-interval theorem."
        ),
        "source_inputs": {
            "citation": (
                "Larry Guth and James Maynard, New large value estimates for "
                "Dirichlet polynomials, arXiv:2405.20552v2; published Annals "
                "of Mathematics 203 (2026), 623--675, DOI "
                "10.4007/annals.2026.203.2.6."
            ),
            "source_archive_url": "https://export.arxiv.org/e-print/2405.20552v2",
            "source_tarball_sha256": SOURCE_TARBALL_SHA256,
            "tex_member": "LargevaluesDirichlet17.tex",
            "tex_member_sha256": SOURCE_TEX_SHA256,
            "checked_locations": [
                "introduction, source lines 96--160 (Ingham, Huxley, Theorem 1.2, Corollaries 1.3--1.4)",
                "introduction, source lines 64--91 (Theorem 1.1 and classical equation (1.1))",
                "source lines 2307--2402 (case ranges in proof of Theorem 1.2)",
                "source lines 2407--2471 (explicit-formula deductions)",
            ],
        },
        "frozen_hypotheses": {
            "counting_convention": (
                "N(sigma,T) counts zeros rho of zeta with Re(rho)>=sigma and "
                "|Im(rho)|<=T, with multiplicity."
            ),
            "sigma_domain_for_case_split": "1/2 <= sigma <= 1",
            "published_zero_density_inputs": [
                {
                    "label": "Ingham",
                    "coefficient_A_sigma": "3/(2-sigma)",
                    "used_on": "1/2 <= sigma <= 7/10",
                },
                {
                    "label": "Guth--Maynard Theorem 1.2",
                    "coefficient_A_sigma": "15/(3+5*sigma)",
                    "used_on": "7/10 <= sigma <= 4/5",
                },
                {
                    "label": "Huxley",
                    "coefficient_A_sigma": "3/(3*sigma-1)",
                    "used_on": "4/5 <= sigma <= 1",
                },
            ],
            "exponent_format": "N(sigma,T) <= T^(A(sigma)*(1-sigma)+o(1))",
            "uniform_short_interval_sufficient_criterion": (
                "As used in the cited proof: with b the uniform density "
                "coefficient and T=x/y times a subpower factor, it is enough "
                "that T < x^(1/b-epsilon)."
            ),
            "almost_all_sufficient_criterion": (
                "As used in the cited proof: T=delta^(-1) times a subpower "
                "factor must satisfy T < X^(2/b-epsilon), and the reduction "
                "requires y >= delta*X."
            ),
        },
        "exact_case_analysis": {
            "crossover": {
                "equation": "3/(2-sigma) = 15/(3+5*sigma)",
                "cleared_numerator_for_ingham_minus_guth_maynard": "30*sigma-21",
                "unique_root_in_domain": q(sigma_star),
                "value_at_root": q(b),
                "sign_conclusion": (
                    "Ingham <= Guth--Maynard for sigma <= 7/10; "
                    "Guth--Maynard <= Ingham for sigma >= 7/10."
                ),
            },
            "comparison_to_global_coefficient": [
                {
                    "case": "Ingham on [1/2,7/10]",
                    "cleared_numerator_for_b-Ingham": "21-30*sigma",
                    "denominator": "13*(2-sigma) > 0",
                    "conclusion": "3/(2-sigma) <= 30/13",
                },
                {
                    "case": "Guth--Maynard on [7/10,4/5]",
                    "cleared_numerator_for_b-Guth--Maynard": "150*sigma-105",
                    "denominator": "13*(3+5*sigma) > 0",
                    "conclusion": "15/(3+5*sigma) <= 30/13",
                },
                {
                    "case": "Huxley on [4/5,1]",
                    "cleared_numerator_for_b-Huxley": "90*sigma-69",
                    "denominator": "13*(3*sigma-1) > 0",
                    "conclusion": "3/(3*sigma-1) <= 30/13",
                },
            ],
            "global_envelope": {
                "b": q(b),
                "attained_at": q(sigma_star),
                "conclusion": "A(sigma) <= 30/13 in every stated case.",
            },
        },
        "critical_large_values_cell": critical_large_values_cell(),
        "short_interval_thresholds": {
            "uniform": {
                "density_input_b": q(b),
                "source_criterion_exponent": "1/b",
                "exact_value": q(Fraction(1, 1) / b),
                "theta_formula": "1-1/b",
                "theta": q(uniform_theta),
                "classification": (
                    "PROVED exact consequence of the stated sufficient "
                    "criterion; the underlying explicit-formula criterion is "
                    "a cited analytic input."
                ),
            },
            "almost_all": {
                "density_input_b": q(b),
                "source_criterion_exponent": "2/b",
                "exact_value": q(Fraction(2, 1) / b),
                "delta_exponent": "-2/b",
                "theta_formula_from_y>=delta*X": "1-2/b",
                "theta": q(almost_all_theta),
                "classification": (
                    "REPLAYED from the source's stated almost-all reduction; "
                    "only its rational exponent conversion is independently "
                    "checked here. This certificate does not independently "
                    "derive the mean-square/explicit-formula argument."
                ),
            },
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": script_sha256(),
            "write_command": (
                "python3 projects/guth-maynard-zero-density/proof/"
                "replay_baseline_route_b.py --write "
                "projects/guth-maynard-zero-density/artifacts/"
                "cycle-1-route-b-baseline.json"
            ),
        },
    }


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH", help="write the deterministic certificate")
    action.add_argument("--check", type=Path, metavar="PATH", help="verify a certificate byte-for-byte")
    args = parser.parse_args()
    data = certificate()
    rendered = canonical_json(data)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(rendered, encoding="utf-8")
    elif args.check:
        observed = args.check.read_text(encoding="utf-8")
        if observed != rendered:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
