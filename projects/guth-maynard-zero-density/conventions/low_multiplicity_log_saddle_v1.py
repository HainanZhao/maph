"""Cycle 127 low-multiplicity logarithmic-saddle exponent ledger."""

from __future__ import annotations

from fractions import Fraction


D_EXP = Fraction(3, 5)
Q_EXP = Fraction(1, 3)
TARGET = Q_EXP


def exponent_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= Fraction(1, 3):
        raise ValueError("mu outside multiplicity range")
    lam = Q_EXP - mu
    tube = D_EXP - xi - Q_EXP
    return {
        "denominator_length": lam,
        "vertical_tube": tube,
        "hs_derivative_weighted": Fraction(3, 5) - mu / 2,
        "hs_tube_weighted": Fraction(34, 45) - mu - xi / 3,
        "hs_ratio_weighted": Fraction(5, 9) - mu - xi / 3,
        "hs_constant_weighted": TARGET,
        "two_dimensional_volume_weighted": Fraction(14, 15) - xi - mu,
        "target": TARGET,
        "volume_margin": xi + mu - Fraction(3, 5),
        "derivative_gap": Fraction(4, 15) - mu / 2,
        "mellin_sample_count": xi - Fraction(4, 15),
    }


def theorem_record() -> dict[str, object]:
    return {
        "lattice_problem": (
            "with L=Q/M and delta=D/(KQ), count primitive p,q~L satisfying "
            "||(D/(2pi))log(p/q)||<=delta"
        ),
        "hs_sum": (
            "order-three Huxley--Sargos in p, summed over q and multiplied by M, "
            "has exponents derivative=3/5-mu/2, tube=34/45-mu-xi/3, "
            "ratio=5/9-mu-xi/3, constant=1/3"
        ),
        "hs_barrier": (
            "the derivative term exceeds the target 1/3 by 4/15-mu/2; it "
            "never closes the registered low-multiplicity range"
        ),
        "volume": (
            "the joint two-dimensional volume after multiplicity has exponent "
            "14/15-xi-mu, below 1/3 by xi+mu-3/5>=1/25"
        ),
        "mellin_identity": (
            "a Fejer majorant reduces the joint count to delta L^2 plus "
            "delta sum_(1<=h<=H)|sum_(n~L)w(n)n^(ihD)|^2, with "
            "H=1/delta=KQ/D"
        ),
        "mellin_target": (
            "the diagonal sampled-Mellin estimate sum_h|P(hD)|^2<<HL X^epsilon "
            "implies the optimal label count O(L X^epsilon), hence weighted "
            "collision count O(Q X^epsilon)"
        ),
        "generic_loss": (
            "a generic time large sieve at sample span HD supplies a term of "
            "size HD*L and loses the factor D relative to the desired H*L; "
            "removing or inverting these logarithmic aliases is the live lock"
        ),
        "boundary": (
            "no sampled-Mellin diagonal bound, low-multiplicity closure, "
            "simple-root closure, complete moment, density, or prime intervals is proved"
        ),
    }
