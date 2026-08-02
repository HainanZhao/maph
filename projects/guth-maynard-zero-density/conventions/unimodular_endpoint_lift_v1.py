"""Cycle 132 unimodular endpoint exponent and inverse ledger."""

from __future__ import annotations

from fractions import Fraction


def endpoint_ledger(
    xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction
) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    hs_floor = Fraction(7, 45) - 2 * mu / 3
    full_ceiling = Fraction(1, 3) - mu
    if not hs_floor <= rho <= full_ceiling:
        raise ValueError("rho outside registered endpoint range")
    next_denominator_floor = xi + Fraction(1, 3) - rho
    if tau < next_denominator_floor:
        raise ValueError("tau below continued-fraction jump floor")
    bandwidth = rho + tau - Fraction(3, 5)
    restored_volume = mu + rho - tau + Fraction(3, 5)
    target = Fraction(1, 3)
    cluster_allowance = 2 * (Fraction(1, 3) - mu - rho)
    return {
        "hs_floor": hs_floor,
        "full_ceiling": full_ceiling,
        "next_denominator_floor": next_denominator_floor,
        "mode_interval_width": -bandwidth,
        "fourier_bandwidth": bandwidth,
        "restored_volume": restored_volume,
        "volume_margin": target - restored_volume,
        "cluster_allowance": cluster_allowance,
        "ray_tolerance": -(rho + tau),
        "target": target,
    }


def extremal_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    rho = Fraction(1, 3) - mu
    tau = xi + mu
    row = endpoint_ledger(xi, mu, rho, tau)
    return {
        "rho": rho,
        "tau": tau,
        "fourier_bandwidth": row["fourier_bandwidth"],
        "restored_volume": row["restored_volume"],
        "volume_margin": row["volume_margin"],
        "cluster_allowance": row["cluster_allowance"],
        "ray_tolerance": row["ray_tolerance"],
    }


def theorem_record() -> dict[str, object]:
    return {
        "unimodular_lift": (
            "if p/q and P/R are consecutive convergents, then "
            "s=Pq-pR is +1 or -1, R=-s*p^{-1} (mod q), and "
            "1/[q(q+R)]<|alpha-p/q|<1/(qR)"
        ),
        "shell_telescope": (
            "for fixed p/q and s, denominators R in one dyadic block occupy "
            "one residue class modulo q; their consecutive error shells tile, "
            "so all hits lie in a logarithmic-mode interval of length O(D/(qS))"
        ),
        "block_ledger": (
            "for q~N=X^rho and R~S=X^tau the natural bandwidth is "
            "H=NS/D, the candidate-label count is O(N^2), and the restored "
            "volume M*N^2/H has exponent mu+rho-tau+3/5"
        ),
        "volume_closure": (
            "R>>KQ/N implies tau>=xi+1/3-rho; throughout the Cycle-131 "
            "endpoint the restored volume is at most X^(14/15-xi-mu), "
            "below X^(1/3) by xi+mu-3/5>=1/25"
        ),
        "fourier_norm": (
            "after the volume term, a sufficient endpoint estimate is "
            "H^{-1} sum_{1<=|h|<=H}|sum_{p/q in V} "
            "e(hD log(p/q)/(2pi))| << Q/M, with smooth dyadic weights allowed"
        ),
        "inverse_graph": (
            "if a block contains more than Q/M hits, those hit vertices form "
            "a cluster graph whose edge (v,v') carries d=a-a' and satisfies "
            "|p q'/(p' q)-g^d|<<1/(NS)<=1/(KQ); every vertex also carries "
            "the matrix [[P,p],[R,q]] of determinant s"
        ),
        "cluster_threshold": (
            "a clustered-large-sieve proof may allow local multiplicity "
            "X^(2(1/3-mu-rho)+epsilon); at the full endpoint rho=1/3-mu "
            "this becomes only X^epsilon"
        ),
        "boundary": (
            "the volume term is closed but the Fourier norm is not proved; "
            "no endpoint, low-multiplicity, simple-root, complete-moment, "
            "density, or prime-interval closure follows"
        ),
    }
