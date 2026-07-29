"""Exact Bernoulli-kernel figures of merit for rank-1 lattice rules.

The frozen Phase-0 convention is the product-weight, beta=0 case of
Dick--Kuo--Sloan (2013), equation (5.13):

    e^2(z, N) = -1 + (1/N) sum_{k=0}^{N-1}
                       product_j (1 + gamma_j B_2({k z_j/N})).

Here B_2(x)=x^2-x+1/6 and every gamma_j is a nonnegative rational.
This is the shift-averaged squared worst-case error in the weighted
unanchored Sobolev convention used by that source.  It is also a
rationally normalized smoothness-two periodic kernel.  Other common
Korobov conventions multiply B_2 by 2*pi^2; that convention is not
silently mixed into this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from math import gcd, prod
from typing import Iterable, Sequence


CONVENTION = "DKS2013-eq5.13-beta0-product-B2"


def _as_fraction(value: Fraction | int | str) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value)


@dataclass(frozen=True)
class RuleSpec:
    """Validated input for one exact rank-1 lattice merit."""

    modulus: int
    generator: tuple[int, ...]
    weights: tuple[Fraction, ...]

    @classmethod
    def create(
        cls,
        modulus: int,
        generator: Sequence[int],
        weights: Sequence[Fraction | int | str],
    ) -> "RuleSpec":
        if isinstance(modulus, bool) or not isinstance(modulus, int):
            raise TypeError("modulus must be an integer")
        if modulus < 2:
            raise ValueError("modulus must be at least 2")
        if not generator:
            raise ValueError("generator must contain at least one component")
        if len(generator) != len(weights):
            raise ValueError("generator and weights must have equal length")
        if any(isinstance(z, bool) or not isinstance(z, int) for z in generator):
            raise TypeError("generator components must be integers")

        rational_weights = tuple(_as_fraction(weight) for weight in weights)
        if any(weight < 0 for weight in rational_weights):
            raise ValueError("weights must be nonnegative")
        normalized_generator = tuple(z % modulus for z in generator)
        return cls(modulus, normalized_generator, rational_weights)

    @property
    def dimension(self) -> int:
        return len(self.generator)

    @property
    def all_components_are_units(self) -> bool:
        return all(gcd(z, self.modulus) == 1 for z in self.generator)


def bernoulli_b2(residue: int, modulus: int) -> Fraction:
    """Return B_2(residue/modulus) exactly, after reducing the residue."""

    if modulus < 1:
        raise ValueError("modulus must be positive")
    r = residue % modulus
    numerator = 6 * r * r - 6 * r * modulus + modulus * modulus
    return Fraction(numerator, 6 * modulus * modulus)


def kernel_product(spec: RuleSpec, k: int) -> Fraction:
    """Return the k-th product-kernel summand exactly."""

    return prod(
        (
            Fraction(1)
            + weight * bernoulli_b2(k * component, spec.modulus)
        )
        for component, weight in zip(spec.generator, spec.weights)
    )


def exact_squared_error(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> Fraction:
    """Compute the frozen squared worst-case error as a reduced Fraction."""

    spec = RuleSpec.create(modulus, generator, weights)
    total = sum(
        (kernel_product(spec, k) for k in range(spec.modulus)),
        Fraction(0),
    )
    result = total / spec.modulus - 1
    if result < 0:
        raise ArithmeticError(
            "a nonnegative-kernel squared error evaluated as negative"
        )
    return result


def exact_squared_error_double_sum(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> Fraction:
    """Independent O(N^2 d) RKHS double-sum oracle for small tests."""

    spec = RuleSpec.create(modulus, generator, weights)
    total = Fraction(0)
    for i in range(spec.modulus):
        for k in range(spec.modulus):
            difference = i - k
            total += prod(
                (
                    Fraction(1)
                    + weight
                    * bernoulli_b2(
                        difference * component,
                        spec.modulus,
                    )
                )
                for component, weight in zip(
                    spec.generator,
                    spec.weights,
                )
            )
    result = total / (spec.modulus * spec.modulus) - 1
    if result < 0:
        raise ArithmeticError("double-sum squared error is negative")
    return result


def float_squared_error(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> float:
    """Uncertified binary64 reference implementation."""

    spec = RuleSpec.create(modulus, generator, weights)
    float_weights = [float(weight) for weight in spec.weights]
    total = 0.0
    for k in range(spec.modulus):
        term = 1.0
        for component, weight in zip(
            spec.generator,
            float_weights,
        ):
            x = ((k * component) % spec.modulus) / spec.modulus
            term *= 1.0 + weight * (x * x - x + 1.0 / 6.0)
        total += term
    return total / spec.modulus - 1.0


def master_denominator(spec: RuleSpec) -> int:
    """A proved common-denominator multiple for the exact result.

    For gamma_j=a_j/b_j in lowest terms, the j-th factor has
    denominator dividing 6*b_j*N^2.  Averaging contributes one further
    factor N.  Reduction may make the actual denominator much smaller.
    """

    return spec.modulus * prod(
        6 * weight.denominator * spec.modulus * spec.modulus
        for weight in spec.weights
    )


def term_digest(spec: RuleSpec) -> str:
    """Hash the exact sequence of reduced kernel summands."""

    digest = sha256()
    for k in range(spec.modulus):
        term = kernel_product(spec, k)
        digest.update(
            f"{k}:{term.numerator}/{term.denominator}\n".encode("ascii")
        )
    return digest.hexdigest()


def fraction_records(values: Iterable[Fraction]) -> list[dict[str, str]]:
    return [
        {
            "numerator": str(value.numerator),
            "denominator": str(value.denominator),
        }
        for value in values
    ]
