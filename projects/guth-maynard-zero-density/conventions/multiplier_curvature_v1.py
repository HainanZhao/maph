"""Cycle 139 order-three multiplier-curvature ledger."""

from __future__ import annotations

from fractions import Fraction


def curvature_ledger(
    xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction, edge: Fraction
) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if edge < 0 or edge > min(2 * rho, Fraction(1, 3) - mu):
        raise ValueError("edge exponent outside realizable range")
    if tau <= 3 * rho:
        raise ValueError("outside strict exact region")
    target = Fraction(2, 3) - 2 * mu
    derivative = Fraction(1, 10) + 3 * rho + edge / 2
    tube = Fraction(1, 5) + 14 * rho / 3 - 2 * tau / 3
    ratio = 14 * rho / 3 - 2 * tau / 3
    constant = 2 * rho + edge
    return {
        "derivative": derivative,
        "tube": tube,
        "ratio": ratio,
        "constant": constant,
        "target": target,
        "derivative_margin": target - derivative,
        "tube_margin": target - tube,
        "ratio_margin": target - ratio,
        "constant_margin": target - constant,
        "edge_ceiling_derivative": Fraction(17, 15) - 4 * mu - 6 * rho,
        "edge_ceiling_constant": Fraction(2, 3) - 2 * mu - 2 * rho,
    }


def range_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    old = Fraction(1, 6) - mu / 2
    new = Fraction(17, 90) - 2 * mu / 3
    tau = xi + Fraction(1, 3) - new
    row = curvature_ledger(xi, mu, new, tau, Fraction(0))
    return {
        "old_all_edge_ceiling": old,
        "new_low_edge_ceiling": new,
        "extension": new - old,
        "tube_margin_at_new_ceiling": row["tube_margin"],
        "ratio_margin_at_new_ceiling": row["ratio_margin"],
        "constant_margin_at_new_ceiling": row["constant_margin"],
    }


def theorem_record() -> dict[str, object]:
    return {
        "specialization": (
            "with H=N^2/J and delta=D N^2/S^2, the order-three total terms "
            "before edge weight are D^(1/6)H^(3/2), H^2 delta^(1/3), "
            "H^2(delta/D)^(1/3), and H"
        ),
        "weighted_terms": (
            "after multiplying by J^2 the exponents are "
            "1/10+3rho+j/2, 1/5+14rho/3-2tau/3, "
            "14rho/3-2tau/3, and 2rho+j"
        ),
        "edge_ceiling": (
            "the derivative and constant terms require respectively "
            "j<17/15-4mu-6rho and j<2/3-2mu-2rho"
        ),
        "regional_extension": (
            "the derivative ceiling is positive for rho<17/90-2mu/3, "
            "extending beyond 1/6-mu/2 by 1/45-mu/6, which remains positive"
        ),
        "secondary_terms": (
            "at rho=17/90-2mu/3 and tau=xi+1/3-rho, the tube, ratio, and "
            "constant margins are uniformly positive in the registered range"
        ),
        "high_edge_limit": (
            "the derivative term grows as j/2 and the constant term as j; "
            "order three does not extend the Cycle-138 all-edge ceiling"
        ),
        "boundary": (
            "no high-edge or all-multiplicity extension, full paired norm, "
            "endpoint, moment, density, or prime-interval theorem is proved"
        ),
    }
