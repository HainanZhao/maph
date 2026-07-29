"""Reference radix-two FFT and an explicit Higham-style error envelope."""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Iterable, Sequence

from flint import acb, arb, ctx


UNIT_ROUNDOFF = Fraction(1, 2**53)
DEFAULT_TWIDDLE_ERROR = 8 * UNIT_ROUNDOFF


def gamma_k(k: int, *, unit_roundoff: Fraction = UNIT_ROUNDOFF) -> Fraction:
    if k < 0 or k * unit_roundoff >= 1:
        raise ValueError("gamma_k requires 0 <= k*u < 1")
    return k * unit_roundoff / (1 - k * unit_roundoff)


def local_butterfly_factor(
    *,
    unit_roundoff: Fraction = UNIT_ROUNDOFF,
    twiddle_error: Fraction = DEFAULT_TWIDDLE_ERROR,
) -> Fraction:
    """Bound one reference butterfly by eta*(|a|+|b|).

    Complex multiplication uses four real multiplications and two real
    additions.  The rational inequality sqrt(2) <= 3/2 removes any
    transcendental constant from the certificate.
    """

    if unit_roundoff <= 0 or twiddle_error < 0:
        raise ValueError("rounding and twiddle bounds must be nonnegative")
    product_error = (
        twiddle_error
        + Fraction(3, 2)
        * gamma_k(2, unit_roundoff=unit_roundoff)
        * (1 + twiddle_error)
    )
    return product_error + unit_roundoff * (1 + product_error)


def transform_error_factor(
    length: int,
    *,
    unit_roundoff: Fraction = UNIT_ROUNDOFF,
    twiddle_error: Fraction = DEFAULT_TWIDDLE_ERROR,
    radix2_equivalent_depth: int | None = None,
) -> Fraction:
    """Return delta where max error <= delta * ||input||_1."""

    if length <= 0 or length & (length - 1):
        raise ValueError("length must be a positive power of two")
    natural_depth = length.bit_length() - 1
    depth = (
        natural_depth
        if radix2_equivalent_depth is None
        else radix2_equivalent_depth
    )
    if depth < natural_depth:
        raise ValueError("depth cannot be below log2(length)")
    eta = local_butterfly_factor(
        unit_roundoff=unit_roundoff, twiddle_error=twiddle_error
    )
    return (1 + eta) ** depth - 1


def _bit_reverse(value: int, width: int) -> int:
    output = 0
    for _ in range(width):
        output = (output << 1) | (value & 1)
        value >>= 1
    return output


def _complex_multiply(left: complex, right: complex) -> complex:
    real = left.real * right.real - left.imag * right.imag
    imag = left.real * right.imag + left.imag * right.real
    return complex(real, imag)


def reference_fft(
    values: Sequence[complex | float | int],
    *,
    inverse: bool = False,
    normalize_inverse: bool = False,
) -> list[complex]:
    """Iterative radix-two binary64 FFT with an explicit operation graph."""

    length = len(values)
    if length <= 0 or length & (length - 1):
        raise ValueError("input length must be a positive power of two")
    width = length.bit_length() - 1
    output = [
        complex(values[_bit_reverse(index, width)]) for index in range(length)
    ]
    sign = 1.0 if inverse else -1.0
    block = 2
    while block <= length:
        half = block // 2
        for start in range(0, length, block):
            for offset in range(half):
                angle = sign * 2.0 * math.pi * offset / block
                twiddle = complex(math.cos(angle), math.sin(angle))
                product = _complex_multiply(
                    twiddle, output[start + offset + half]
                )
                top = output[start + offset]
                output[start + offset] = complex(
                    top.real + product.real, top.imag + product.imag
                )
                output[start + offset + half] = complex(
                    top.real - product.real, top.imag - product.imag
                )
        block *= 2
    if inverse and normalize_inverse:
        output = [
            complex(value.real / length, value.imag / length)
            for value in output
        ]
    return output


def _fraction_arb(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _exact_float_acb(value: complex | float | int) -> acb:
    number = complex(value)
    return acb(
        _fraction_arb(Fraction.from_float(number.real)),
        _fraction_arb(Fraction.from_float(number.imag)),
    )


def exact_dft(
    values: Sequence[complex | float | int],
    *,
    inverse: bool = False,
    normalize_inverse: bool = False,
) -> list[acb]:
    """Arb enclosure of the exact DFT of the binary64 input values."""

    length = len(values)
    sign = 1 if inverse else -1
    exact_values = [_exact_float_acb(value) for value in values]
    output = []
    for frequency in range(length):
        total = acb(0)
        for index, value in enumerate(exact_values):
            angle = acb(
                0, sign * 2 * arb.pi() * frequency * index / length
            )
            total += value * angle.exp()
        if inverse and normalize_inverse:
            total /= length
        output.append(total)
    return output


def _twiddle_errors(length: int, inverse: bool) -> Iterable[arb]:
    sign = 1.0 if inverse else -1.0
    block = 2
    while block <= length:
        for offset in range(block // 2):
            angle_float = sign * 2.0 * math.pi * offset / block
            approximate = complex(math.cos(angle_float), math.sin(angle_float))
            angle_exact = acb(
                0, (1 if inverse else -1) * 2 * arb.pi() * offset / block
            )
            yield abs(_exact_float_acb(approximate) - angle_exact.exp())
        block *= 2


def certify_reference_fft(
    values: Sequence[complex | float | int],
    *,
    inverse: bool = False,
    normalize_inverse: bool = False,
    precision: int = 256,
    twiddle_error: Fraction = DEFAULT_TWIDDLE_ERROR,
    radix2_equivalent_depth: int | None = None,
) -> dict[str, object]:
    """Check the reference transform against its analytic envelope."""

    old_precision = ctx.prec
    ctx.prec = precision
    try:
        approximate = reference_fft(
            values,
            inverse=inverse,
            normalize_inverse=normalize_inverse,
        )
        exact = exact_dft(
            values,
            inverse=inverse,
            normalize_inverse=normalize_inverse,
        )
        input_l1 = sum(
            (abs(_exact_float_acb(value)) for value in values), arb(0)
        )
        factor = transform_error_factor(
            len(values),
            twiddle_error=twiddle_error,
            radix2_equivalent_depth=radix2_equivalent_depth,
        )
        bound = _fraction_arb(factor) * input_l1
        if inverse and normalize_inverse:
            bound /= len(values)
        errors = [
            abs(_exact_float_acb(observed) - target)
            for observed, target in zip(approximate, exact)
        ]
        maximum_error = max((error.abs_upper() for error in errors), default=arb(0))
        twiddle_errors = list(_twiddle_errors(len(values), inverse))
        maximum_twiddle_error = max(
            (error.abs_upper() for error in twiddle_errors), default=arb(0)
        )
        twiddle_bound = _fraction_arb(twiddle_error)
        twiddles_contained = bool(
            maximum_twiddle_error.upper() <= twiddle_bound.lower()
        )
        transform_contained = bool(
            maximum_error.upper() <= bound.lower()
        )
        return {
            "length": len(values),
            "inverse": inverse,
            "normalized_inverse": normalize_inverse,
            "precision_bits": precision,
            "unit_roundoff": str(UNIT_ROUNDOFF),
            "twiddle_error_assumption": str(twiddle_error),
            "local_butterfly_factor": str(
                local_butterfly_factor(twiddle_error=twiddle_error)
            ),
            "transform_error_factor": str(factor),
            "input_l1_enclosure": input_l1.str(40),
            "error_bound": bound.str(40),
            "maximum_observed_error_enclosure": maximum_error.str(40),
            "maximum_twiddle_error_enclosure": maximum_twiddle_error.str(40),
            "twiddles_contained": twiddles_contained,
            "transform_contained": transform_contained,
        }
    finally:
        ctx.prec = old_precision
