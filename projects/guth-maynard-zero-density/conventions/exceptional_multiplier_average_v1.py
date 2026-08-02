"""Cycle 137 exceptional-multiplier volume and edge-weight ledger."""

from __future__ import annotations

from fractions import Fraction


def average_ledger(
    xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction, edge: Fraction
) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if tau <= 3 * rho:
        raise ValueError("outside strict Cycle-136 region")
    if edge < 0:
        raise ValueError("negative edge exponent")
    target = Fraction(2, 3) - 2 * mu - 2 * edge
    discretization = 4 * rho
    volume = Fraction(3, 5) + 6 * rho - 2 * tau
    return {
        "exception_discretization": discretization,
        "exception_volume": volume,
        "exception_bound": max(discretization, volume),
        "edge_weight_target": target,
        "discretization_margin": target - discretization,
        "volume_margin": target - volume,
        "edge_ceiling_discretization": Fraction(1, 3) - mu - 2 * rho,
        "edge_ceiling_volume": Fraction(1, 30) - mu + tau - 3 * rho,
        "edge_ceiling": min(
            Fraction(1, 3) - mu - 2 * rho,
            Fraction(1, 30) - mu + tau - 3 * rho,
        ),
    }


def theorem_record() -> dict[str, object]:
    return {
        "exception_count": (
            "rational multipliers have height <=N^2 and exceptional intervals "
            "have width O(N^2/S^2); the mode-grid union bound is "
            "B_exc<<X^epsilon(N^4+D N^6/S^2)"
        ),
        "weighted_target": (
            "on |E_d|~J, a coherent exceptional contribution costs B_exc J^2; "
            "the diagonal edge budget is (Q/M)^2, so B_exc<<(Q/M)^2/J^2 suffices"
        ),
        "closure_region": (
            "writing J=X^j, volume plus discretization closes exactly when "
            "j<min(1/3-mu-2rho, 1/30-mu+tau-3rho)"
        ),
        "nonempty_cell": (
            "at xi=16/25, mu=0, rho=7/45, and minimal tau=184/225, "
            "the edge ceiling is 1/45, so every fixed j<1/45 closes strictly"
        ),
        "residual_deficit": (
            "outside the closed region, the elementary count is obstructed first "
            "by the N^4 rational-discretization term whenever "
            "1/3-mu-2rho is the smaller ceiling"
        ),
        "inverse_output": (
            "each surviving difference retains E_d, r_d, its convergent "
            "denominator <=N^2, next denominator >>S^2/N^4, next partial "
            "quotient >>S^2/N^6, and the original signed phase anchor"
        ),
        "boundary": (
            "no high-edge or full exceptional average, paired norm, endpoint, "
            "moment, density, or prime-interval theorem is proved"
        ),
    }
