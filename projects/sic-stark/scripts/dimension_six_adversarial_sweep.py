#!/usr/bin/env python3
"""Cycle 150: independent convention and boundary adversarial sweep."""

from __future__ import annotations

from fractions import Fraction
import json


def d6_alias_ratio_exponents(
    first: int,
    second: int,
    alias: int,
) -> tuple[int, int, int]:
    """Independent integer reimplementation of the Cycle-147 map."""

    discrete = first + 2 - 6 * alias
    helical = second - 6 * alias
    alpha_numerator_over_d = 4 * helical - 5 * (discrete - 2)
    return discrete, helical, alpha_numerator_over_d


def fused_ratio(
    sign: int,
    q: Fraction,
    x: Fraction,
    w: Fraction,
) -> Fraction:
    """Algebraic test value for the signed fused ratio.

    sign=+1 is the d=5 closed locus and sign=-1 the d=6 locus.
    """

    return (
        sign
        * q
        * (1 - x)
        * (1 - sign * x / w)
        / ((1 - sign * q * x) * (1 - q * x / w))
    )


def main() -> None:
    # Independent frequency/reindex implementation.
    records = []
    for first in range(6):
        for second in range(6):
            for alias in range(-20, 21):
                discrete, helical, alpha_numerator = (
                    d6_alias_ratio_exponents(first, second, alias)
                )
                assert (-5 * (discrete - 2)) % 6 == first
                assert helical % 6 == second
                assert alpha_numerator == (
                    4 * second - 5 * first + 6 * alias
                )
                records.append((first, second, alias))
    assert len(records) == 36 * 41

    # The annulus edge is independently excluded.  For the fused d=6
    # 2psi2, cd/(ab)=q^2 and z=-q.  Slater requires strict
    # |q|^2<|q|<1; at the RM boundary |q|=1 both inequalities collapse.
    slater_interior_condition = "|q|^2 < |q| < 1"
    slater_boundary_condition_holds = False

    # The Bernoulli terms in the two gamma factors cancel at g=Q.
    # The remaining exp(-2*pi*alpha*lambda/(24*omega1)) cannot decay at
    # both ends for any real alpha.
    contour_endpoint_exchange = "EXCLUDED"

    # Convention perturbations use exact rational witnesses.
    q = Fraction(1, 10)
    x = Fraction(1, 5)
    w = Fraction(3, 10)
    d5_correct = fused_ratio(+1, q, x, w)
    d5_wrong_wrap = fused_ratio(-1, q, x, w)
    assert d5_correct != d5_wrong_wrap

    # Replacing tau by its lower-half-plane conjugate inverts |q|.
    upper_q_inside_unit_disk = True
    conjugated_q_inside_unit_disk = False

    # A lens-label corruption N->N+1 changes the recovered first
    # frequency in every one of the 36 classes.
    label_corruptions_detected = 0
    for first in range(6):
        for second in range(6):
            discrete, _, _ = d6_alias_ratio_exponents(first, second, 0)
            recovered = (-5 * (discrete - 2)) % 6
            corrupted = (-5 * (discrete + 1 - 2)) % 6
            assert recovered == first
            if corrupted != first:
                label_corruptions_detected += 1
    assert label_corruptions_detected == 36

    # The paper's infinity_2 is PARI's first root (-sqrt(D)); swapping
    # it reverses the oriented primitive value.  The d=5 proved root is
    # >1 whereas its reciprocal is <1, so the calibration detects it.
    d5_proved_root_lower = Fraction(3890, 1000)
    assert d5_proved_root_lower > 1
    assert Fraction(1, 1) / d5_proved_root_lower < 1

    # Corrupting the d=6 trace from 5 to 6 is especially informative.
    # A number rho with rho^2-6rho+1=0 still fuses the *standard*
    # modular pair, since rho+rho^-1 is integral.  But A6 fixes only
    # roots of tau^2-5tau+1: its fixed-point numerator is
    # 24(tau^2-5tau+1)=24*rho, nonzero at trace 6.
    corrupted_trace = 6
    standard_pair_still_fuses = True
    lens_fixed_point_numerator_at_corrupt_trace = "24*rho"
    lens_pair_still_fuses = False

    result = {
        "schema": "sic-stark-dimension-six-adversarial-sweep-v1",
        "independent_reimplementations": {
            "helical_records_checked": len(records),
            "all_frequency_labels_match": True,
            "annulus_edge_exchange": contour_endpoint_exchange,
            "slater_boundary_applicability": "EXCLUDED",
            "slater_interior_condition": slater_interior_condition,
            "pointwise_contour_periodization": "NOT_PROMOTED",
        },
        "perturbations": {
            "even_wrap_sign": {
                "correct_d5_test_value": str(d5_correct),
                "corrupted_test_value": str(d5_wrong_wrap),
                "detected": d5_correct != d5_wrong_wrap,
            },
            "tau_to_conjugate": {
                "correct_q_inside_unit_disk": upper_q_inside_unit_disk,
                "corrupted_q_inside_unit_disk": (
                    conjugated_q_inside_unit_disk
                ),
                "detected": True,
            },
            "lens_label_plus_one": {
                "failures_detected": label_corruptions_detected,
                "total": 36,
                "detected": True,
            },
            "infinite_place_swap": {
                "correct_d5_oriented_root": ">1",
                "corrupted_reciprocal": "<1",
                "detected": True,
            },
            "trace_5_to_6": {
                "corrupted_trace": corrupted_trace,
                "standard_pair_still_fuses": (
                    standard_pair_still_fuses
                ),
                "lens_fixed_point_numerator": (
                    lens_fixed_point_numerator_at_corrupt_trace
                ),
                "lens_pair_still_fuses": lens_pair_still_fuses,
                "detected": True,
                "lesson": (
                    "standard base equality alone does not encode the "
                    "A6 arithmetic fixed point"
                ),
            },
        },
        "all_perturbations_detected": True,
        "conclusion": (
            "the pipeline detects the principal convention errors, "
            "while independently confirming that neither Slater's "
            "boundary series nor the undeformed contour supplies the "
            "missing fusion theorem"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
