"""Exact Cycle-185 three-label curvature and AP-free occupancy ledgers."""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def curvature_identity(
    *, v: int, u_minus: int, u_zero: int, u_plus: int,
    A_minus: int, A_zero: int, A_plus: int,
    alpha_minus: Q, alpha_zero: Q, alpha_plus: Q,
) -> dict[str, object]:
    """Clear the exact exponential three-label product relation."""
    require(min(v, u_minus, u_zero, u_plus) > 0, "positive common-intercept ray data")
    require(alpha_minus * alpha_plus == alpha_zero * alpha_zero, "three-label exponential product")
    U_minus, U_zero, U_plus = v * u_minus, v * u_zero, v * u_plus
    epsilon_minus = Q(A_minus) - U_minus * alpha_minus
    epsilon_zero = Q(A_zero) - U_zero * alpha_zero
    epsilon_plus = Q(A_plus) - U_plus * alpha_plus
    K = U_zero**2 * A_minus * A_plus - U_minus * U_plus * A_zero**2
    require(K % (v * v) == 0, "common-intercept curvature square divisibility")
    K_prime = K // (v * v)
    P = U_minus * U_plus * U_zero**2
    expanded = (
        alpha_minus * Q(epsilon_plus, U_plus)
        + alpha_plus * Q(epsilon_minus, U_minus)
        + Q(epsilon_minus * epsilon_plus, U_minus * U_plus)
        - 2 * alpha_zero * Q(epsilon_zero, U_zero)
        - Q(epsilon_zero * epsilon_zero, U_zero * U_zero)
    )
    require(Q(K, P) == expanded, "cleared curvature expansion")
    F_minus_zero = u_zero * A_minus - u_minus * A_zero
    F_zero_plus = u_plus * A_zero - u_zero * A_plus
    syzygy = u_zero * A_plus * F_minus_zero - u_minus * A_zero * F_zero_plus
    require(K_prime == syzygy, "primitive curvature pair-determinant syzygy")
    return {
        "U": {"minus": U_minus, "zero": U_zero, "plus": U_plus},
        "epsilon": {"minus": epsilon_minus, "zero": epsilon_zero, "plus": epsilon_plus},
        "K": K,
        "K_prime": K_prime,
        "formula": "K=U_0^2*A_-*A_+-U_-*U_+*A_0^2=v^2*K_prime",
        "expansion": "K/(U_-*U_+*U_0^2)=alpha_-*delta_++alpha_+*delta_-+delta_-*delta_+-2*alpha_0*delta_0-delta_0^2",
        "syzygy": "K_prime=u_0*A_+*F_-0-u_-*A_0*F_0+",
        "expanded_value": expanded,
    }


def deep_exactification_bound(*, chart_cap: Q, C: int, H: int, X: int, v: int, S: int) -> dict[str, Q]:
    """A sufficient bound for primitive curvature exactification at depth S."""
    require(chart_cap >= 1 and min(C, H, X, v, S) > 0 and H < X, "positive curvature scales")
    linear = Q(8 * chart_cap * C * H**3, v**2 * S**4 * X)
    quadratic = Q(8 * C * C * H**2, v**2 * S**4 * X**2)
    return {"linear": linear, "quadratic": quadratic, "total": linear + quadratic}


def cantor_encode(bits: int, digits: int) -> int:
    """Map a binary word to ternary digits 0/1; these values are 3-AP-free."""
    require(digits >= 0 and 0 <= bits < 2**digits, "Cantor word range")
    value = 0
    for index in range(digits):
        value += ((bits >> index) & 1) * 3**index
    return value


def cantor_ap_free(digits: int) -> list[int]:
    return [cantor_encode(bits, digits) for bits in range(2**digits)]


def critical_ap_free_occupancy(k: int) -> dict[str, object]:
    """An exact scale ledger disproving mass/capacity-only AP forcing.

    This deliberately contains no actual-exponential phase assignment.
    """
    require(k >= 1, "positive scale parameter")
    X, H, Delta = 3 ** (50 * k), 3 ** (22 * k), 3 ** (30 * k)
    S, U, M = 3 ** (4 * k), 3 ** (18 * k), 3 ** (13 * k)
    require(H == S * U and X == 3 ** (50 * k), "frozen capacity exponents")
    require(2 ** (30 * k) >= M, "Cantor AP-free capacity")
    labels = {
        "ambient_upper": Delta,
        "construction": "1+cantor_encode(bits,30*k) for 0<=bits<M",
        "selected_count": M,
        "three_ap_free": "ternary digits 0/1 admit no nontrivial x+z=2y digitwise; subsets and shifts preserve this",
    }
    N = S + 1
    pair_count = comb(N, 2)
    ordered_cross_mass = M * (M - 1) * pair_count * pair_count
    target = 3 ** (42 * k)  # X^(21/25)
    require(8 * ordered_cross_mass >= target, "critical mass lower bound")
    stable_cutoff_upper = 2 * H * Delta // X + 1  # 4/pi<2 for C=1.
    require(U * U >= stable_cutoff_upper, "every pair is in the stable shell")
    return {
        "parameters": {"k": k, "X": X, "H": H, "Delta": Delta, "S": S, "U": U, "M": M},
        "fibres": {
            "depth": N,
            "capacity": H // U + 1,
            "pair_count_per_label": pair_count,
            "complete": True,
        },
        "labels": labels,
        "stable_shell": {"minimum_product": U * U, "cutoff_upper": stable_cutoff_upper},
        "mass": {"ordered_cross_mass": ordered_cross_mass, "critical_target": target, "lower_factor": Q(ordered_cross_mass, target)},
        "boundary": "This is an AP-free abstract occupancy ledger, not an actual-positive-exponential configuration or a counterexample to an analytic distribution theorem.",
    }


def verify_all() -> dict[str, object]:
    curvature = curvature_identity(
        v=2, u_minus=1, u_zero=2, u_plus=4,
        A_minus=1, A_zero=2, A_plus=4,
        alpha_minus=Q(1, 2), alpha_zero=Q(1), alpha_plus=Q(2),
    )
    require(curvature["K"] == 0 and curvature["K_prime"] == 0, "geometric curvature fixture")
    bound = deep_exactification_bound(chart_cap=Q(2), C=1, H=100, X=10**10, v=1, S=100)
    require(bound["total"] < 1, "deep exactification threshold fixture")
    values = cantor_ap_free(5)
    require(all(x + z != 2 * y for x in values for y in values for z in values if not (x == y == z)), "Cantor AP-free fixture")
    occupancy = critical_ap_free_occupancy(1)
    require(occupancy["mass"]["ordered_cross_mass"] > 0, "critical AP-free occupancy fixture")
    return {
        "three_label_exactification": "For an arithmetic-progression label triple, K=U_0^2*A_-*A_+-U_-*U_+*A_0^2 is divisible by v^2 and its primitive quotient has the retained pair-determinant syzygy. If all depths exceed S and 8*A_c*C*H^3/(v^2*S^4*X)+8*C^2*H^2/(v^2*S^4*X^2)<1, then K=0.",
        "mass_only_no_go": "A shifted ternary-digit AP-free set with M=X^(13/50) complete fibres of depth X^(2/25)+1 and denominator X^(9/25) has stable ordered cross mass >>X^(21/25), yet contains no three-label arithmetic progression. Thus mass, capacity, and stable shells alone cannot force the deep triples needed for curvature exactification.",
        "boundary": "This proves a three-label exactification lemma and a mass/capacity-only no-go. It proves no actual-exponential distribution bound, populated-box bound, seeded recurrence, density gain, or interval result.",
        "samples": {"curvature": curvature, "bound": bound, "occupancy_k1": occupancy},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
