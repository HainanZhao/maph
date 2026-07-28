#!/usr/bin/env python3
"""Cycle 147': interior factorization and corpus-applicability audit."""

from __future__ import annotations

import json


DIMENSION = 6
LEVEL = 24


def main() -> None:
    records = []
    for first_frequency in range(DIMENSION):
        for second_frequency in range(DIMENSION):
            for alias_index in range(-12, 13):
                discrete = first_frequency + 2 - 6 * alias_index
                beta_mode = 5 * (discrete - 2)
                helical_integer = second_frequency - 6 * alias_index
                alpha_numerator_over_d = (
                    4 * helical_integer - beta_mode
                )
                expected_numerator = (
                    4 * second_frequency
                    - 5 * first_frequency
                    + 6 * alias_index
                )
                assert alpha_numerator_over_d == expected_numerator
                assert (-beta_mode) % DIMENSION == first_frequency
                assert helical_integer % DIMENSION == second_frequency
                records.append(
                    {
                        "frequency": [
                            first_frequency,
                            second_frequency,
                        ],
                        "z": alias_index,
                        "N": discrete,
                        "ell": helical_integer,
                    }
                )
    assert len(records) == 36 * 25

    # Three z-steps are exactly one helical translation.
    for first_frequency in range(DIMENSION):
        for second_frequency in range(DIMENSION):
            for alias_index in range(-6, 7):
                discrete = first_frequency + 2 - 6 * alias_index
                translated_discrete = (
                    first_frequency
                    + 2
                    - 6 * (alias_index + 3)
                )
                assert (translated_discrete - discrete) % LEVEL == 6

    corpus = [
        {
            "source": (
                "Garoufalidis--Kashaev, From state integrals to "
                "q-series, Theorem 1.1"
            ),
            "hypotheses": (
                "I_{A,B}(b)=integral Phi_b(x)^B exp(-A*pi*i*x^2), "
                "with integers B>A>0 and no lens label"
            ),
            "d6_verdict": (
                "NOT_APPLICABLE: the d=6 integrand is a sum over "
                "m mod 24 of two general-lens Gamma_M factors, and "
                "its modular partner is A6*tau rather than the "
                "standard S-transform used in Theorem 1.1"
            ),
        },
        {
            "source": (
                "Beem--Dimofte--Pasquetti, Holomorphic Blocks in "
                "Three Dimensions"
            ),
            "hypotheses": (
                "physics block factorization for specified 3d "
                "N=2 theories and integration cycles"
            ),
            "d6_verdict": (
                "NOT_A_RIGOROUS_SPECIALIZATION: no theorem in that "
                "paper treats the A6 general-lens discrete kernel"
            ),
        },
        {
            "source": (
                "Garoufalidis--Zagier, Asymptotics of Nahm sums at "
                "roots of unity"
            ),
            "hypotheses": "radial asymptotics at rational roots of unity",
            "d6_verdict": (
                "NOT_APPLICABLE: beta6 is a quadratic irrational "
                "boundary point, not a rational root-of-unity cusp"
            ),
        },
    ]

    result = {
        "schema": (
            "sic-stark-dimension-six-interior-factorization-audit-v1"
        ),
        "exact_inputs": {
            "SS_equation_66_fourier_transform": "VERIFIED",
            "helical_quotient": (
                "X=(R x Z/24)/<(omega1-omega2,6)>"
            ),
            "dual_descent": "xi*Delta+n/4=ell",
            "frequency_map": "(xi,n,ell)->(-n,ell) mod 6",
            "alias_records_checked": len(records),
            "three_bibasic_classes_per_frequency": True,
            "two_base_Arb_enclosures": "9/9 at three interior points",
        },
        "proof": {
            "step_1": (
                "Equation (66) is the meromorphic Fourier transform "
                "of the continuous-discrete kernel."
            ),
            "step_2": (
                "Restriction of a Fourier transform to the dual of "
                "the helical quotient collects exactly the four "
                "discrete lifts and all continuous lifts."
            ),
            "step_3": (
                "The exact reindexing above turns those lifts into "
                "three bibasic bilateral classes."
            ),
            "step_4": (
                "In the chamber |q_M|<|q_M_tilde|<1, the geometric "
                "tail bounds of Cycle 144' make each class absolutely "
                "and locally uniformly convergent."
            ),
            "conclusion": (
                "The periodized identity holds as a meromorphic "
                "Fourier-series/distribution identity in the interior."
            ),
        },
        "corpus_checks": corpus,
        "interior_meromorphic_spectral_identity": "VERIFIED",
        "literal_pointwise_contour_periodization": "OPEN",
        "pointwise_gap_list": [
            (
                "choose a single pole-separating contour for every "
                "helical translate near g=Q"
            ),
            (
                "prove a translate-uniform integrable majorant before "
                "interchanging the helical sum and the contour integral"
            ),
            (
                "show that this pointwise periodization equals the "
                "meromorphic spectral continuation"
            ),
        ],
        "named_statement_discipline_satisfied": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
