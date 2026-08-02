"""Cycle 130 broad continued-fraction cylinder ledger."""

from __future__ import annotations

from fractions import Fraction


def cylinder_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside registered low-multiplicity range")
    jump = xi + 2 * mu - Fraction(1, 3)
    q0 = (Fraction(3, 5) - jump) / 2
    L = Fraction(1, 3) - mu
    weighted = Fraction(14, 15) - xi - mu
    return {
        "partial_quotient_floor": jump,
        "broad_denominator_ceiling": q0,
        "full_denominator_ceiling": L,
        "broad_range_width": q0,
        "narrow_range_width": L - q0,
        "weighted_broad_count": weighted,
        "target": Fraction(1, 3),
        "target_margin": xi + mu - Fraction(3, 5),
    }


def theorem_record() -> dict[str, object]:
    return {
        "parameters": "A0=KM^2/Q, q0=sqrt(D/A0), L=Q/M",
        "cylinder_cover": (
            "a convergent p/q with next partial quotient >=cA0 lies in an "
            "interval of length O(1/(A0q^2)) about p/q"
        ),
        "grid_spacing": (
            "on the fixed compact mode chart, consecutive g^a are separated "
            "by asymp 1/D, so an interval J contains O(1+D|J|) modes"
        ),
        "broad_count": (
            "summing p~q and q<=q0 gives O(q0^2+(D/A0)log q0)="
            "O((D/A0)X^epsilon) occupied modes"
        ),
        "weighted_count": (
            "multiplication by M gives DQ/(KM) X^epsilon with exponent "
            "14/15-xi-mu, below Q by xi+mu-3/5>=1/25"
        ),
        "range_margins": (
            "q0 has exponent 7/15-xi/2-mu; it is positive by at least 7/300, "
            "while L/q0 has exponent xi/2-2/15>=14/75"
        ),
        "remaining_range": (
            "only narrow cylinders sqrt(DQ/(KM^2))<q<<Q/M remain in the "
            "low-multiplicity denominator branch"
        ),
        "boundary": (
            "no narrow-cylinder bound, full low-multiplicity or simple-root "
            "closure, complete moment, density, or prime intervals is proved"
        ),
    }
