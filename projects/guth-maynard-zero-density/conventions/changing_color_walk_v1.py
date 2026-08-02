"""Cycle 142 deterministic valuation walk and recurrence saturation."""

from __future__ import annotations

from math import ceil, gcd, log2


def reduction_step(a: int, b: int, p: int, q: int) -> tuple[int, int, int]:
    if min(a, b, p, q) <= 0 or gcd(a, b) != 1 or gcd(p, q) != 1:
        raise ValueError("positive reduced inputs required")
    z = gcd(a * p, b * q)
    pp, qq = a * p // z, b * q // z
    if gcd(pp, qq) != 1:
        raise RuntimeError("reduction failed")
    return pp, qq, z


def valuation_update(alpha: int, beta: int, pval: int, qval: int) -> tuple[int, int, int]:
    if min(alpha, beta, pval, qval) < 0 or alpha * beta != 0:
        raise ValueError("A and B are coprime primewise")
    zval = min(alpha, qval) + min(beta, pval)
    return pval + alpha - zval, qval + beta - zval, zval


def logarithmic_chain_ceiling(height: int, compact_constant: int = 2) -> int:
    if height < 2 or compact_constant < 1:
        raise ValueError("positive nontrivial height required")
    return ceil(3 * log2(compact_constant * height))


def recurrence_density_ledger(vertices: int, chain_ceiling: int) -> dict[str, int | float]:
    if vertices < 2 or chain_ceiling < 1:
        raise ValueError("invalid recurrence parameters")
    forbidden_depth = chain_ceiling + 1
    required_edges = ceil(forbidden_depth * vertices / (forbidden_depth + 1))
    return {
        "forbidden_depth": forbidden_depth,
        "required_edges": required_edges,
        "allowed_edge_deficit": vertices - required_edges,
        "required_density": required_edges / vertices,
    }


def theorem_record() -> dict[str, object]:
    return {
        "reduction_walk": (
            "for reduced x_t=p_t/q_t and r=A/B, z_t=gcd(Ap_t,Bq_t)="
            "gcd(A,q_t)gcd(B,p_t), and p_{t+1}=Ap_t/z_t, "
            "q_{t+1}=Bq_t/z_t"
        ),
        "valuation_walk": (
            "primewise, with alpha=v_l(A), beta=v_l(B), alpha*beta=0, "
            "z=min(alpha,v_l(q_t))+min(beta,v_l(p_t)); subtract z from both "
            "updated numerator and denominator valuations"
        ),
        "deterministic_colors": (
            "the cross-gcd color z_t is determined by the current reduced label; "
            "changing colors do not create an independent recurrence parameter"
        ),
        "height_ceiling": (
            "for nontrivial A/B, a supported rational geometric chain at height "
            "N has O(log N) edges by the Cycle-78 lower bound "
            "height(x_0(A/B)^t)>=2^t/(C^2N^2)"
        ),
        "density_gate": (
            "if Lambda is the logarithmic chain ceiling, the path-forest bound "
            "forces a contradiction only from L>=ceil((Lambda+1)R/(Lambda+2)); "
            "the required density is 1-O(1/log N)"
        ),
        "scoped_saturation": (
            "the fixed-multiplier divisor/continuation compiler yields at most a "
            "logarithmic contradiction and no fixed-power saving unless an "
            "independent theorem forces near-complete edge density"
        ),
        "remaining_object": (
            "sparse path components must be controlled in the original paired "
            "Fourier norm, retaining component starts, r_d-g^d, and signed tails"
        ),
        "boundary": (
            "this is not a no-go for analytic cancellation across sparse components; "
            "no paired norm, endpoint, moment, density, or prime intervals is proved"
        ),
    }
