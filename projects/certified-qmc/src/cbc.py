"""Small exact CBC oracle used to validate future fast implementations."""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Sequence

from .exact_error import exact_squared_error


def _fraction_record(value: Fraction) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
    }


def unit_candidates(modulus: int, quotient_sign: bool = True) -> list[int]:
    """Return unit candidates, optionally quotienting z ~ -z.

    The B2 product merit is invariant under replacing a candidate z by
    N-z.  Counting those mirror pairs as numerical ties would make a
    tie-rate benchmark meaningless.
    """

    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    units = [z for z in range(1, modulus) if gcd(z, modulus) == 1]
    if not quotient_sign:
        return units
    return sorted({min(z, modulus - z) for z in units})


def exact_cbc(
    modulus: int,
    weights: Sequence[Fraction | int | str],
    *,
    quotient_sign: bool = True,
) -> dict[str, object]:
    """Construct a small rule by exhaustive exact CBC.

    This is O(d*N^2) and deliberately serves as a ground-truth oracle,
    not as the planned production fast-CBC implementation.
    """

    if not weights:
        raise ValueError("weights must contain at least one component")
    rational_weights = [Fraction(weight) for weight in weights]
    if any(weight < 0 for weight in rational_weights):
        raise ValueError("weights must be nonnegative")

    candidates = unit_candidates(modulus, quotient_sign=quotient_sign)
    generator = [1]
    first_error = exact_squared_error(
        modulus,
        generator,
        rational_weights[:1],
    )
    decisions: list[dict[str, object]] = [
        {
            "dimension": 1,
            "winner": 1,
            "winner_error": _fraction_record(first_error),
            "selection": "fixed_by_rank1_normalization",
        }
    ]

    for dimension in range(2, len(rational_weights) + 1):
        scored = [
            (
                exact_squared_error(
                    modulus,
                    generator + [candidate],
                    rational_weights[:dimension],
                ),
                candidate,
            )
            for candidate in candidates
        ]
        scored.sort()
        winner_error, winner = scored[0]
        generator.append(winner)
        runner_error, runner = scored[1] if len(scored) > 1 else scored[0]
        gap = runner_error - winner_error
        exact_ties = [
            candidate for error, candidate in scored if error == winner_error
        ]
        decisions.append(
            {
                "dimension": dimension,
                "candidate_count_after_symmetry_quotient": len(candidates),
                "winner": winner,
                "winner_error": _fraction_record(winner_error),
                "runner_up": runner,
                "runner_up_error": _fraction_record(runner_error),
                "runner_up_gap": _fraction_record(gap),
                "minimizer_count": len(exact_ties),
                "minimizers": exact_ties,
                "selection": "exact_argmin_smallest_representative_on_tie",
            }
        )

    final_error = exact_squared_error(
        modulus,
        generator,
        rational_weights,
    )
    return {
        "tag": "VERIFIED",
        "algorithm": "exhaustive-exact-CBC-oracle",
        "production_scale_claimed": False,
        "modulus": modulus,
        "weights": [
            _fraction_record(weight) for weight in rational_weights
        ],
        "sign_symmetry_quotiented": quotient_sign,
        "generator": generator,
        "final_squared_error": _fraction_record(final_error),
        "decisions": decisions,
    }
