"""Direct modular evaluator and CRT-certified CBC prototype."""

from __future__ import annotations

from fractions import Fraction
from math import prod
from typing import Sequence

from .cbc import unit_candidates
from .crt import balanced_reconstruct, choose_moduli, modulus_product
from .exact_error import RuleSpec
from .scaled_integer import (
    candidate_difference_bound,
    error_numerator_bound,
    factor_denominator,
    factor_numerator,
)


def _prime_values(schedule: Sequence[int | dict[str, object]]) -> list[int]:
    return [
        int(item["prime"]) if isinstance(item, dict) else int(item)
        for item in schedule
    ]


def error_numerator_residue(spec: RuleSpec, prime: int) -> int:
    c_product = prod(
        factor_denominator(spec.modulus, weight) % prime
        for weight in spec.weights
    ) % prime
    total = 0
    for k in range(spec.modulus):
        term = prod(
            factor_numerator(k * z, spec.modulus, weight) % prime
            for z, weight in zip(spec.generator, spec.weights)
        ) % prime
        total = (total + term) % prime
    return (total - spec.modulus * c_product) % prime


def reconstruct_error_numerator(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
    schedule: Sequence[int | dict[str, object]],
) -> dict[str, object]:
    spec = RuleSpec.create(modulus, generator, weights)
    bound = error_numerator_bound(modulus, spec.weights)
    moduli = choose_moduli(_prime_values(schedule), bound)
    residues = [error_numerator_residue(spec, prime) for prime in moduli]
    numerator = balanced_reconstruct(residues, moduli, bound=bound)
    denominator = modulus * prod(
        factor_denominator(modulus, weight) for weight in spec.weights
    )
    value = Fraction(numerator, denominator)
    return {
        "numerator": numerator,
        "denominator": denominator,
        "reduced_numerator": value.numerator,
        "reduced_denominator": value.denominator,
        "bound": bound,
        "moduli": moduli,
        "residues": residues,
        "modulus_product": modulus_product(moduli),
    }


def candidate_difference_residue(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction],
    candidate_u: int,
    candidate_v: int,
    prime: int,
) -> int:
    previous_weights = weights[:-1]
    new_weight = weights[-1]
    total = 0
    for k in range(modulus):
        previous = prod(
            factor_numerator(k * z, modulus, weight) % prime
            for z, weight in zip(prefix, previous_weights)
        ) % prime
        difference = (
            factor_numerator(k * candidate_u, modulus, new_weight)
            - factor_numerator(k * candidate_v, modulus, new_weight)
        ) % prime
        total = (total + previous * difference) % prime
    return total


def reconstruct_candidate_difference(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    candidate_u: int,
    candidate_v: int,
    schedule: Sequence[int | dict[str, object]],
) -> dict[str, object]:
    normalized = [Fraction(weight) for weight in weights]
    if len(normalized) != len(prefix) + 1:
        raise ValueError("weights must contain prefix weights plus one")
    bound = candidate_difference_bound(
        modulus, normalized[:-1], normalized[-1]
    )
    moduli = choose_moduli(_prime_values(schedule), bound)
    residues = [
        candidate_difference_residue(
            modulus,
            prefix,
            normalized,
            candidate_u,
            candidate_v,
            prime,
        )
        for prime in moduli
    ]
    value = balanced_reconstruct(residues, moduli, bound=bound)
    return {
        "difference": value,
        "bound": bound,
        "moduli": moduli,
        "residues": residues,
        "modulus_product": modulus_product(moduli),
    }


def certified_crt_cbc(
    modulus: int,
    weights: Sequence[Fraction | int | str],
    schedule: Sequence[int | dict[str, object]],
) -> dict[str, object]:
    """Small CBC whose merits and branch comparisons are CRT-certified."""

    normalized = [Fraction(weight) for weight in weights]
    if not normalized or any(weight < 0 for weight in normalized):
        raise ValueError("nonempty nonnegative weights are required")
    candidates = unit_candidates(modulus, quotient_sign=True)
    generator = [1]
    decisions: list[dict[str, object]] = []
    for dimension in range(2, len(normalized) + 1):
        stage_weights = normalized[:dimension]
        scores = []
        for candidate in candidates:
            reconstruction = reconstruct_error_numerator(
                modulus,
                [*generator, candidate],
                stage_weights,
                schedule,
            )
            scores.append((int(reconstruction["numerator"]), candidate))
        scores.sort()
        winner_score, winner = scores[0]
        comparisons = []
        for _, candidate in scores:
            proof = reconstruct_candidate_difference(
                modulus,
                generator,
                stage_weights,
                candidate,
                winner,
                schedule,
            )
            if int(proof["difference"]) < 0:
                raise ArithmeticError("winner failed exact branch comparison")
            comparisons.append(
                {
                    "candidate": candidate,
                    "candidate_minus_winner": str(proof["difference"]),
                    "bound": str(proof["bound"]),
                    "moduli": [str(p) for p in proof["moduli"]],
                    "residues": [str(r) for r in proof["residues"]],
                }
            )
        generator.append(winner)
        decisions.append(
            {
                "dimension": dimension,
                "winner": winner,
                "winner_scaled_numerator": str(winner_score),
                "comparisons": comparisons,
            }
        )
    final = reconstruct_error_numerator(
        modulus, generator, normalized, schedule
    )
    return {
        "schema": "certified-qmc-crt-cbc-v1",
        "tag": "VERIFIED",
        "algorithm": "direct-modular-sum-with-balanced-CRT",
        "production_scale_claimed": False,
        "modulus": modulus,
        "weights": [
            {"numerator": str(w.numerator), "denominator": str(w.denominator)}
            for w in normalized
        ],
        "generator": generator,
        "final_squared_error": {
            "numerator": str(final["reduced_numerator"]),
            "denominator": str(final["reduced_denominator"]),
        },
        "final_reconstruction": {
            key: (
                [str(value) for value in item]
                if isinstance(item, list)
                else str(item)
            )
            for key, item in final.items()
            if key not in {"reduced_numerator", "reduced_denominator"}
        },
        "decisions": decisions,
    }
