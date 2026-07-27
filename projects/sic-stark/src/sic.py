"""Numerical diagnostics for Weyl--Heisenberg covariant SICs.

The module deliberately uses only the Python standard library.  It is a
small, independently testable baseline for later exact arithmetic involving
algebraic fiducials and the Shintani--Faddeev construction.
"""

from __future__ import annotations

import cmath
import math
from collections.abc import Iterable, Sequence


ComplexVector = tuple[complex, ...]
DisplacementCoefficients = dict[tuple[int, int], complex]


def normalize(vector: Iterable[complex]) -> ComplexVector:
    """Return ``vector`` with Euclidean norm one.

    Raises:
        ValueError: if the vector is empty or has zero norm.
    """

    entries = tuple(complex(value) for value in vector)
    if not entries:
        raise ValueError("a fiducial vector must have positive dimension")
    norm_squared = sum(abs(value) ** 2 for value in entries)
    if norm_squared == 0:
        raise ValueError("a fiducial vector must be nonzero")
    scale = math.sqrt(norm_squared)
    return tuple(value / scale for value in entries)


def displacement_overlap(
    fiducial: Sequence[complex], p: int, q: int
) -> complex:
    r"""Compute ``<psi|D_(p,q)|psi>`` in a standard phase convention.

    We use

    .. math::

       D_{p,q}=\tau^{pq}X^pZ^q,\qquad
       \tau=-e^{\pi i/d},\quad
       Z|j\rangle=e^{2\pi i j/d}|j\rangle.

    Changing the overall phase convention for ``D_(p,q)`` does not change
    the squared modulus tested by the SIC equations.
    """

    psi = normalize(fiducial)
    dimension = len(psi)
    p %= dimension
    q %= dimension
    omega = cmath.exp(2j * math.pi / dimension)
    tau = -cmath.exp(1j * math.pi / dimension)
    phase = tau ** (p * q)
    return phase * sum(
        psi[(index + p) % dimension].conjugate()
        * (omega ** (q * index))
        * psi[index]
        for index in range(dimension)
    )


def sic_residuals(fiducial: Sequence[complex]) -> dict[tuple[int, int], float]:
    r"""Return residuals in all nonidentity fiducial SIC equations.

    For a normalized vector in :math:`\mathbb C^d`, the Weyl--Heisenberg
    orbit is a SIC precisely when every returned value is zero:

    .. math::

       |\langle\psi|D_{p,q}|\psi\rangle|^2-\frac1{d+1}=0

    for ``(p, q) != (0, 0)`` modulo ``d``.
    """

    psi = normalize(fiducial)
    dimension = len(psi)
    target = 1.0 / (dimension + 1)
    return {
        (p, q): abs(displacement_overlap(psi, p, q)) ** 2 - target
        for p in range(dimension)
        for q in range(dimension)
        if (p, q) != (0, 0)
    }


def max_sic_residual(fiducial: Sequence[complex]) -> float:
    """Return the largest absolute Weyl--Heisenberg SIC residual."""

    residuals = sic_residuals(fiducial)
    return max((abs(value) for value in residuals.values()), default=0.0)


def projector_displacement_coefficients(
    fiducial: Sequence[complex],
) -> DisplacementCoefficients:
    r"""Return the displacement-basis coefficients of ``|psi><psi|``.

    With the conventions in :func:`displacement_overlap`,

    .. math::

       |\psi\rangle\langle\psi|
       =\frac1d\sum_{p,q}a_{p,q}D_{p,q},\qquad
       a_{p,q}=\operatorname{Tr}(|\psi\rangle\langle\psi|D_{p,q}^\dagger).
    """

    psi = normalize(fiducial)
    dimension = len(psi)
    return {
        (p, q): displacement_overlap(psi, p, q).conjugate()
        for p in range(dimension)
        for q in range(dimension)
    }


def twisted_idempotency_residuals(
    coefficients: DisplacementCoefficients, dimension: int
) -> DisplacementCoefficients:
    r"""Return the finite twisted-convolution residual for ``P^2=P``.

    For

    .. math::

       P=\frac1d\sum_{\boldsymbol p}a_{\boldsymbol p}D_{\boldsymbol p},

    the displacement multiplication law reduces idempotency to

    In odd dimension the equation is simply

    .. math::

       \sum_{\boldsymbol p}
       a_{\boldsymbol p}a_{\boldsymbol t-\boldsymbol p}
       \tau^{p_2t_1-p_1t_2}
       =d\,a_{\boldsymbol t}

    for every :math:`\boldsymbol t\in(\mathbb Z/d\mathbb Z)^2`.  In even
    dimension, reducing a displacement index modulo ``d`` contributes an
    additional sign because ``D_(p+d,q)=(-1)^q D_(p,q)`` and
    ``D_(p,q+d)=(-1)^p D_(p,q)``.  The implementation includes this
    representative-wrap sign explicitly.
    """

    if dimension <= 0:
        raise ValueError("dimension must be positive")
    expected_keys = {
        (p, q) for p in range(dimension) for q in range(dimension)
    }
    if set(coefficients) != expected_keys:
        raise ValueError("coefficients must contain every displacement key")
    tau = -cmath.exp(1j * math.pi / dimension)
    residuals: DisplacementCoefficients = {}
    for target_p in range(dimension):
        for target_q in range(dimension):
            total = 0j
            for p in range(dimension):
                for q in range(dimension):
                    remainder_p = (target_p - p) % dimension
                    remainder_q = (target_q - q) % dimension
                    raw_p = p + remainder_p
                    raw_q = q + remainder_q
                    wrap_p = raw_p // dimension
                    wrap_q = raw_q // dimension
                    wrap_sign = 1
                    if dimension % 2 == 0:
                        wrap_sign = (-1) ** (
                            wrap_p * target_q + wrap_q * target_p
                        )
                    total += (
                        coefficients[(p, q)]
                        * coefficients[(remainder_p, remainder_q)]
                        * tau ** (q * remainder_p - p * remainder_q)
                        * wrap_sign
                    )
            residuals[(target_p, target_q)] = (
                total - dimension * coefficients[(target_p, target_q)]
            )
    return residuals


def max_twisted_idempotency_residual(
    coefficients: DisplacementCoefficients, dimension: int
) -> float:
    """Return the largest absolute twisted-convolution residual."""

    return max(
        abs(value)
        for value in twisted_idempotency_residuals(
            coefficients, dimension
        ).values()
    )


def displacement_vector(
    fiducial: Sequence[complex], p: int, q: int
) -> ComplexVector:
    """Apply ``D_(p,q)`` to a normalized fiducial vector."""

    psi = normalize(fiducial)
    dimension = len(psi)
    p %= dimension
    q %= dimension
    omega = cmath.exp(2j * math.pi / dimension)
    tau = -cmath.exp(1j * math.pi / dimension)
    phase = tau ** (p * q)
    result = [0j] * dimension
    for index, amplitude in enumerate(psi):
        result[(index + p) % dimension] = (
            phase * (omega ** (q * index)) * amplitude
        )
    return tuple(result)


def frame_operator(fiducial: Sequence[complex]) -> tuple[ComplexVector, ...]:
    r"""Return the frame operator of the full displacement orbit.

    A normalized Weyl--Heisenberg orbit always satisfies
    ``sum |D_pq psi><D_pq psi| = d I``.  Checking this independently catches
    implementation and normalization errors even though it does not by
    itself certify the equiangular SIC condition.
    """

    psi = normalize(fiducial)
    dimension = len(psi)
    operator = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for p in range(dimension):
        for q in range(dimension):
            vector = displacement_vector(psi, p, q)
            for row in range(dimension):
                for column in range(dimension):
                    operator[row][column] += (
                        vector[row] * vector[column].conjugate()
                    )
    return tuple(tuple(row) for row in operator)


def max_frame_residual(fiducial: Sequence[complex]) -> float:
    """Return the max-entry residual from ``d`` times the identity."""

    operator = frame_operator(fiducial)
    dimension = len(operator)
    return max(
        abs(
            operator[row][column]
            - (dimension if row == column else 0.0)
        )
        for row in range(dimension)
        for column in range(dimension)
    )


def qubit_tetrahedral_fiducial() -> ComplexVector:
    """Return a dimension-two SIC fiducial with Bloch vector (1,1,1)/sqrt(3)."""

    z_coordinate = 1.0 / math.sqrt(3.0)
    upper = math.sqrt((1.0 + z_coordinate) / 2.0)
    lower = cmath.exp(1j * math.pi / 4.0) * math.sqrt(
        (1.0 - z_coordinate) / 2.0
    )
    return (upper, lower)


def hesse_fiducial() -> ComplexVector:
    """Return the standard dimension-three Hesse SIC fiducial."""

    scale = 1.0 / math.sqrt(2.0)
    return (0j, scale, -scale)


def dimension_four_fiducial() -> ComplexVector:
    r"""Return an exact-radical representative of the dimension-four orbit.

    This is Eq. (10) of Zhu, Teo, and Englert, *Structure of Two-qubit
    Symmetric Informationally Complete POVMs* (2010), arXiv:1008.1138.
    """

    golden_ratio_conjugate = (math.sqrt(5.0) - 1.0) / 2.0
    eighth_root = cmath.exp(1j * math.pi / 4.0)
    inverse_eighth_root = eighth_root.conjugate()
    inverse_power = golden_ratio_conjugate ** (-1.5)
    scale = 1.0 / (
        2.0 * math.sqrt(3.0 + golden_ratio_conjugate)
    )
    return tuple(
        scale * entry
        for entry in (
            1.0 + inverse_eighth_root,
            eighth_root + 1j * inverse_power,
            1.0 - inverse_eighth_root,
            eighth_root - 1j * inverse_power,
        )
    )
