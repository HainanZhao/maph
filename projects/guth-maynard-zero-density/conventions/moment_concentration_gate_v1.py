"""Exact Cycle 89 moment-concentration exponent contracts."""

from fractions import Fraction

Q = Fraction

ATOM_EXP = Q(14, 15)
RAW_L1_TARGET = Q(31, 25)
MOMENT_SPLIT = Q(58, 75)
FOURIER_CEILING = Q(83, 75)


def required_fourth_moment(xi: Fraction, l1_saving: Fraction = Q(0)) -> Fraction:
    """Exponent forced by M2 diagonal size and an L1 target with saving."""
    return 3 * (xi + ATOM_EXP) - 2 * (RAW_L1_TARGET - l1_saving)


def random_fourth_moment(xi: Fraction) -> Fraction:
    """Exponent of K(DQ)^2."""
    return xi + 2 * ATOM_EXP


def required_excess(xi: Fraction, l1_saving: Fraction = Q(0)) -> Fraction:
    return required_fourth_moment(xi, l1_saving) - random_fourth_moment(xi)


def verify_all() -> dict[str, object]:
    assert required_fourth_moment(Q(0)) == Q(8, 25)
    assert required_excess(MOMENT_SPLIT) == 0
    assert required_excess(FOURIER_CEILING) == Q(2, 3)
    assert required_excess(Q(7, 10)) == Q(-11, 75)
    assert required_excess(Q(9, 10)) == Q(19, 75)
    assert required_excess(Q(1), Q(1, 100)) == Q(34, 75) + Q(1, 50)
    return {
        "holder": "M2<=L1^(2/3)M4^(1/3); equivalently M4>=M2^3/L1^2",
        "conditional_m2": "M2>=X^(xi+14/15-o(1))",
        "conditional_l1": "L1<=X^(31/25-delta+o(1))",
        "forced_m4_exponent": "3xi+8/25+2delta",
        "random_m4_exponent": "xi+28/15",
        "forced_excess": "2xi-116/75+2delta",
        "zero_excess_boundary": str(MOMENT_SPLIT),
        "ceiling_excess": str(required_excess(FOURIER_CEILING)),
        "interpretation": (
            "conditional on diagonal-size M2, upper-range L1 success requires "
            "fourth-moment concentration; concentration is necessary, not sufficient"
        ),
    }


if __name__ == "__main__":
    print(verify_all())
