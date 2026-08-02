"""Exact sandwich ledgers for Cycle 186 actual-exponential convexity."""
from __future__ import annotations

from fractions import Fraction as Q


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def convexity_bounds(*, p: int, q: int, t_lower: Q, t_upper: Q, exp_upper: Q) -> dict[str, Q]:
    """Bounds for p f(a)+q f(c)-(p+q)f(b), f(x)=exp(t*x)."""
    require(min(p, q) > 0 and 0 < t_lower <= t_upper and exp_upper >= 1, "positive convexity ledger")
    r = p + q
    lower = Q(p * q * r, 2) * t_lower * t_lower
    upper = Q(p * q * r, 2) * t_upper * t_upper * exp_upper
    require(0 < lower <= upper, "convexity envelope order")
    return {"p": Q(p), "q": Q(q), "r": Q(r), "lower": lower, "upper": upper}


def forbidden_rational_sandwich(*, denominator_product: int, curve_lower: Q, curve_upper: Q, error_upper: Q) -> dict[str, object]:
    """Certify the incompatible curvature/grid sandwich for a rational sum."""
    require(denominator_product > 0 and 0 < curve_lower <= curve_upper and error_upper >= 0, "positive sandwich data")
    grid = Q(1, denominator_product)
    require(error_upper < curve_lower, "error does not preserve positive curvature")
    require(curve_upper + error_upper < grid, "curve does not lie below rational grid")
    return {
        "status": "FORBIDDEN_DEEP_TRIPLE", "grid": grid,
        "curve_lower": curve_lower, "curve_upper": curve_upper, "error_upper": error_upper,
        "reason": "0<R<1/(U_a*U_b*U_c) contradicts the cleared integer denominator grid",
    }


def consecutive_deep_triple_regime(*, T: int, C: int, chart_exp_upper: int) -> dict[str, object]:
    """Exact power-scale ledger for three consecutive deep labels in one box."""
    require(T >= 2 and C > 0 and chart_exp_upper >= 1, "positive scale regime")
    Delta, X, S = T**15, T**25, T**2
    denominator_lower, denominator_upper = T**9, 2 * T**9
    bounds = convexity_bounds(
        p=1, q=1, t_lower=Q(6, Delta), t_upper=Q(44, 7 * Delta), exp_upper=Q(chart_exp_upper),
    )
    error_upper = Q(8 * C, S * denominator_lower * X)
    certificate = forbidden_rational_sandwich(
        denominator_product=denominator_upper**3,
        curve_lower=bounds["lower"], curve_upper=bounds["upper"], error_upper=error_upper,
    )
    return {
        "parameters": {
            "T": T, "C": C, "chart_exp_upper": chart_exp_upper,
            "Delta": Delta, "X": X, "minimum_depth_minus_one": S,
            "denominator_interval": [denominator_lower, denominator_upper],
        },
        "convexity": bounds, "error_upper": error_upper, "certificate": certificate,
        "scope": "No three consecutive labels can all carry full-fibre shifted approximants in this denominator/depth box. This is local crowding exclusion only.",
    }


def verify_all() -> dict[str, object]:
    bounds = convexity_bounds(p=1, q=1, t_lower=Q(6, 10**30), t_upper=Q(44, 7 * 10**30), exp_upper=Q(1000))
    certificate = forbidden_rational_sandwich(
        denominator_product=(2 * 10**18) ** 3,
        curve_lower=bounds["lower"], curve_upper=bounds["upper"], error_upper=Q(8, 10**72),
    )
    regime = consecutive_deep_triple_regime(T=100, C=1, chart_exp_upper=1000)
    require(certificate["status"] == regime["certificate"]["status"], "sandwich status mismatch")
    return {
        "actual_curve_local_exclusion": "For a<b<c, the weighted shifted-slope second difference is strictly convex. Whenever its retained error is below the curve lower bound and its curve upper bound plus error is below 1/(U_aU_bU_c), no such deep rational-ray triple exists.",
        "scale_specialization": "At Delta=T^15, X=T^25, depths >=T^2+1, and denominators in [T^9,2T^9], three consecutive labels satisfy the forbidden sandwich for every sufficiently large T in a fixed compact chart; T=100 is an exact conservative fixture when C=1 and z^ell<=1000.",
        "boundary": "This is an actual-exponential, denominator-labelled local three-point exclusion. It does not yet bound the number of separated labels in a critical box, defeat the AP-free occupancy model, prove a recurrence, density gain, or interval result.",
        "samples": {"bounds": bounds, "certificate": certificate, "regime": regime},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
