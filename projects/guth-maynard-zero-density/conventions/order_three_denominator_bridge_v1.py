"""Cycle 131 order-three denominator-block bridge ledger."""

from __future__ import annotations

from fractions import Fraction


def block_ledger(xi: Fraction, mu: Fraction, rho: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    return {
        "derivative": mu + Fraction(1, 10) + 3 * rho / 2,
        "tube": mu + 2 * rho + Fraction(4, 45) - xi / 3,
        "ratio": mu + 2 * rho - xi / 3 - Fraction(1, 9),
        "constant": mu + rho,
        "target": Fraction(1, 3),
    }


def range_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    ceiling = Fraction(7, 45) - 2 * mu / 3
    broad = Fraction(7, 15) - xi / 2 - mu
    full = Fraction(1, 3) - mu
    at_ceiling = block_ledger(xi, mu, ceiling)
    return {
        "hs_ceiling": ceiling,
        "broad_ceiling": broad,
        "extension_beyond_broad": ceiling - broad,
        "full_ceiling": full,
        "remaining_endpoint_width": full - ceiling,
        "tube_margin": Fraction(1, 3) - at_ceiling["tube"],
        "ratio_margin": Fraction(1, 3) - at_ceiling["ratio"],
        "constant_margin": Fraction(1, 3) - at_ceiling["constant"],
    }


def theorem_record() -> dict[str, object]:
    return {
        "block_terms": (
            "after summing q~X^rho and restoring M, the order-three exponents "
            "are mu+1/10+3rho/2, mu+2rho+4/45-xi/3, "
            "mu+2rho-xi/3-1/9, and mu+rho"
        ),
        "closure_ceiling": (
            "the derivative term reaches target 1/3 at "
            "rho_HS=7/45-2mu/3; all four terms are <=1/3 for rho<=rho_HS"
        ),
        "secondary_margins": (
            "at rho_HS, tube margin=(xi+mu)/3-1/15, ratio margin="
            "2/15+(xi+mu)/3, and constant margin=8/45-mu/3, all positive"
        ),
        "broad_extension": (
            "rho_HS exceeds the Cycle-130 broad cutoff by "
            "xi/2+mu/3-14/45>=2/225"
        ),
        "remaining_width": (
            "the unresolved endpoint rho_HS<rho<=1/3-mu has width "
            "8/45-mu/3>=133/900"
        ),
        "boundary": (
            "no endpoint-denominator, full low-multiplicity or simple-root "
            "closure, complete moment, density, or prime intervals is proved"
        ),
    }
