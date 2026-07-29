"""Exact decimal-formatting cells for Workstream B."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import re


DECIMAL_LEXEME = re.compile(
    r"^[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?$"
)


def _power_of_ten(exponent: int) -> Fraction:
    if exponent >= 0:
        return Fraction(10**exponent)
    return Fraction(1, 10 ** (-exponent))


def exact_decimal(lexeme: str) -> Fraction:
    text = lexeme.strip()
    if DECIMAL_LEXEME.fullmatch(text) is None:
        raise ValueError(f"invalid finite decimal lexeme: {lexeme!r}")
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ValueError(f"invalid finite decimal lexeme: {lexeme!r}") from error
    if not value.is_finite():
        raise ValueError("decimal merit must be finite")
    sign, digits, exponent = value.as_tuple()
    numerator = int("".join(str(digit) for digit in digits) or "0")
    if sign:
        numerator = -numerator
    return Fraction(numerator) * _power_of_ten(exponent)


def observed_significant_digits(lexeme: str) -> int:
    """Count displayed significant digits, retaining trailing zeroes."""

    text = lexeme.strip().lower()
    if DECIMAL_LEXEME.fullmatch(text) is None:
        raise ValueError(f"invalid finite decimal lexeme: {lexeme!r}")
    mantissa = text.split("e", 1)[0].lstrip("+-")
    digits = mantissa.replace(".", "")
    nonzero = next((index for index, digit in enumerate(digits) if digit != "0"), None)
    if nonzero is None:
        return len(digits)
    return len(digits) - nonzero


def lexical_grid_exponent(lexeme: str) -> int:
    """Return the decimal exponent of the last displayed digit."""

    text = lexeme.strip().lower()
    if DECIMAL_LEXEME.fullmatch(text) is None:
        raise ValueError(f"invalid finite decimal lexeme: {lexeme!r}")
    mantissa, marker, exponent_text = text.partition("e")
    explicit_exponent = int(exponent_text) if marker else 0
    mantissa = mantissa.lstrip("+-")
    fractional_digits = len(mantissa.split(".", 1)[1]) if "." in mantissa else 0
    return explicit_exponent - fractional_digits


@dataclass(frozen=True)
class FormattingBound:
    lexeme: str
    exact_value: Fraction
    significant_digits: int
    grid_exponent: int
    grid_spacing: Fraction
    half_cell: Fraction
    convention: str

    def as_dict(self) -> dict[str, object]:
        def encode(value: Fraction) -> dict[str, str]:
            return {
                "numerator": str(value.numerator),
                "denominator": str(value.denominator),
            }

        return {
            "lexeme": self.lexeme,
            "exact_value": encode(self.exact_value),
            "significant_digits": self.significant_digits,
            "grid_exponent": self.grid_exponent,
            "grid_spacing": encode(self.grid_spacing),
            "half_cell": encode(self.half_cell),
            "convention": self.convention,
        }


def formatting_bound(
    lexeme: str,
    *,
    significant_digits: int | None = None,
) -> FormattingBound:
    """Return exact T_format for round-to-nearest decimal formatting.

    If a table-wide significant-digit convention is supplied, it fixes
    the grid even for integer lexemes with ambiguous trailing zeroes.
    Otherwise, the place value of the final displayed lexical digit is
    used.
    """

    value = exact_decimal(lexeme)
    observed = observed_significant_digits(lexeme)
    if significant_digits is not None:
        if significant_digits <= 0:
            raise ValueError("significant_digits must be positive")
        if value == 0:
            exponent = lexical_grid_exponent(lexeme)
        else:
            exponent = Decimal(lexeme.strip()).copy_abs().adjusted()
            exponent = int(exponent) - significant_digits + 1
        convention = "table-wide significant digits; round-to-nearest"
        digits = significant_digits
    else:
        exponent = lexical_grid_exponent(lexeme)
        convention = "final displayed lexical digit; round-to-nearest"
        digits = observed
    spacing = _power_of_ten(exponent)
    return FormattingBound(
        lexeme=lexeme.strip(),
        exact_value=value,
        significant_digits=digits,
        grid_exponent=exponent,
        grid_spacing=spacing,
        half_cell=spacing / 2,
        convention=convention,
    )
