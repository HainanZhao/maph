#!/usr/bin/env python3
"""Exact algebra controls for the C75 KKT/boundary reduction."""

from fractions import Fraction


def power(value: Fraction, exponent: int) -> Fraction:
    return value**exponent


def check_template(values: list[Fraction], denominator_squared: Fraction) -> None:
    assert sum(values) == 0
    assert sum(value * value for value in values) == denominator_squared


def objective(
    values: list[Fraction], denominator_squared: Fraction, alpha: int
) -> Fraction:
    return sum(power(abs(value), 2 * alpha) for value in values) / power(
        denominator_squared, alpha
    )


def main() -> None:
    for r in (Fraction(1, 3), Fraction(1), Fraction(2), Fraction(7, 3)):
        e3 = [1 + r, -1, -r, 0]
        q3 = 2 * (r * r + r + 1)
        check_template(e3, q3)

        e13 = [2 + r, -1, -1, -r]
        q13 = 2 * (r * r + 2 * r + 3)
        check_template(e13, q13)
        assert objective(e13, q13, 2) == Fraction(1, 2) - 4 * (
            e13[0] * e13[1] * e13[2] * e13[3]
        ) / q13**2

        e22 = [(1 + r) / 2, (1 + r) / 2, -1, -r]
        q22 = (3 + 2 * r + 3 * r * r) / 2
        check_template(e22, q22)

        for alpha in (1, 2, 3):
            assert objective(e3, q3, alpha) == (
                (1 + r) ** (2 * alpha) + 1 + r ** (2 * alpha)
            ) / q3**alpha
            assert objective(e13, q13, alpha) == (
                (2 + r) ** (2 * alpha) + 2 + r ** (2 * alpha)
            ) / q13**alpha
            assert objective(e22, q22, alpha) == (
                2 * ((1 + r) / 2) ** (2 * alpha) + 1 + r ** (2 * alpha)
            ) / q22**alpha

    # Endpoint and equality-family controls.
    assert objective(
        [Fraction(1), Fraction(-1), Fraction(0), Fraction(0)], Fraction(2), 2
    ) == Fraction(1, 2)
    assert objective(
        [Fraction(3), Fraction(-1), Fraction(-1), Fraction(-1)], Fraction(12), 2
    ) == Fraction(7, 12)
    print("OK: C75 template normalizations and objective identities")


if __name__ == "__main__":
    main()
