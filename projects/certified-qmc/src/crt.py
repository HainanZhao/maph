"""Balanced Chinese-remainder reconstruction with explicit bounds."""

from __future__ import annotations

from math import gcd
from typing import Iterable, Sequence


def modulus_product(moduli: Iterable[int]) -> int:
    product = 1
    for modulus in moduli:
        product *= modulus
    return product


def choose_moduli(schedule: Sequence[int], bound: int) -> list[int]:
    """Take the shortest prefix whose product is greater than 2*bound."""

    if bound < 0:
        raise ValueError("bound must be nonnegative")
    chosen: list[int] = []
    product = 1
    for modulus in schedule:
        if modulus < 2:
            raise ValueError("invalid CRT modulus")
        if any(gcd(modulus, previous) != 1 for previous in chosen):
            raise ValueError("CRT moduli must be pairwise coprime")
        chosen.append(modulus)
        product *= modulus
        if product > 2 * bound:
            return chosen
    raise ValueError("schedule is too short for the reconstruction bound")


def balanced_reconstruct(
    residues: Sequence[int],
    moduli: Sequence[int],
    *,
    bound: int,
) -> int:
    """Reconstruct the unique integer in [-bound,bound]."""

    if len(residues) != len(moduli) or not moduli:
        raise ValueError("residues and nonempty moduli must have equal length")
    if modulus_product(moduli) <= 2 * bound:
        raise ValueError("modulus product does not prove uniqueness")
    value = 0
    product = 1
    for residue, modulus in zip(residues, moduli):
        if not 0 <= residue < modulus:
            raise ValueError("residue is not reduced")
        if gcd(product, modulus) != 1:
            raise ValueError("CRT moduli must be pairwise coprime")
        correction = (
            (residue - value) * pow(product, -1, modulus)
        ) % modulus
        value += product * correction
        product *= modulus
    if value > product // 2:
        value -= product
    if abs(value) > bound:
        raise ArithmeticError("residues reconstruct outside the proved bound")
    return value
