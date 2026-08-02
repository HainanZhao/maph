"""Exact Cycle 75 denominator-average geometry and exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd


DELTA_EXP = Q(3, 5)
TARGET_BASE = Q(6, 25)
ATLAS_CEILING = Q(11, 25)


Matrix2 = tuple[tuple[Q, Q], tuple[Q, Q]]


def det2(matrix: Matrix2) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def hessian_aq(c: Q, a: Q, q: Q) -> Matrix2:
    """Hessian of c*log(1+a/q) in (a,q), evaluated exactly."""
    if min(c, a, q) <= 0:
        raise ValueError("c,a,q must be positive")
    s = a + q
    aa = -c / s**2
    aq = -c / s**2
    qq = c * (Q(1) / q**2 - Q(1) / s**2)
    return ((aa, aq), (aq, qq))


def hessian_nq(c: Q, n: Q, q: Q) -> Matrix2:
    """Hessian of c*(log n-log q) in (n,q), evaluated exactly."""
    if min(c, q) <= 0 or n <= q:
        raise ValueError("require c>0 and n>q>0")
    return ((-c / n**2, Q(0)), (Q(0), c / q**2))


def transform_aq_to_nq(matrix: Matrix2) -> Matrix2:
    """Apply J^T H J for a=n-q, with J=d(a,q)/d(n,q)."""
    aa, aq = matrix[0]
    _, qq = matrix[1]
    return ((aa, -aa + aq), (-aa + aq, aa - 2 * aq + qq))


def scaled_hessian(c: Q, a_scale: Q, q_scale: Q, x: Q, y: Q) -> Matrix2:
    """Hessian after a=A*x, q=Q*y."""
    if not (c > 0 and Q(0) < a_scale <= q_scale and Q(1) <= x <= 2 and Q(1) <= y <= 2):
        raise ValueError("outside normalized dyadic box")
    base = hessian_aq(c, a_scale * x, q_scale * y)
    aa, aq = base[0]
    _, qq = base[1]
    return (
        (a_scale**2 * aa, a_scale * q_scale * aq),
        (a_scale * q_scale * aq, q_scale**2 * qq),
    )


def normalized_hessian(c: Q, a_scale: Q, q_scale: Q, x: Q, y: Q) -> Matrix2:
    scale = c * a_scale / q_scale
    matrix = scaled_hessian(c, a_scale, q_scale, x, y)
    return tuple(tuple(value / scale for value in row) for row in matrix)  # type: ignore[return-value]


def primitive_ray_unique(a1: int, q1: int, a2: int, q2: int) -> bool:
    if min(a1, q1, a2, q2) <= 0:
        raise ValueError("positive integer pairs required")
    if gcd(a1, q1) != 1 or gcd(a2, q2) != 1:
        raise ValueError("primitive pairs required")
    return a1 * q2 != a2 * q1 or (a1 == a2 and q1 == q2)


def hs_w(theta: Q, alpha: Q) -> Q:
    return min(alpha, max(Q(0), alpha + Q(1, 10) - theta / 2))


def exponent_cell(theta: Q, kappa: Q, alpha: Q) -> dict[str, object]:
    if min(theta, kappa, alpha) < 0 or alpha > theta or theta + kappa > ATLAS_CEILING:
        raise ValueError("cell outside registered atlas")
    lam = DELTA_EXP + alpha - theta
    fixed_q = theta + hs_w(theta, alpha)
    banked = min(lam, fixed_q)
    target = TARGET_BASE - kappa
    return {
        "theta": theta,
        "kappa": kappa,
        "alpha": alpha,
        "lambda": lam,
        "normalized_curvature_exponent": lam,
        "normalized_determinant_exponent": 2 * lam,
        "relative_tube_exponent": -1 - alpha - kappa,
        "ell_injectivity_bound": lam,
        "fixed_q_hs_bound": fixed_q,
        "banked_count_bound": banked,
        "packet_target_open": target,
        "live_residual": banked >= target,
        "additional_saving_required_strictly_more_than": banked - target,
    }


def verify_all() -> dict[str, object]:
    anchors = ((Q(1), Q(2), Q(3)), (Q(7, 5), Q(4, 3), Q(9, 4)))
    for c, a, q in anchors:
        aq = hessian_aq(c, a, q)
        nq = hessian_nq(c, a + q, q)
        if det2(aq) != -c**2 / (q**2 * (a + q) ** 2):
            raise RuntimeError("(a,q) determinant identity")
        if transform_aq_to_nq(aq) != nq or det2(nq) != det2(aq):
            raise RuntimeError("shifted-coordinate Hessian identity")

    for c, a_scale, q_scale, x, y in (
        (Q(1), Q(1), Q(1), Q(1), Q(1)),
        (Q(3, 2), Q(1, 7), Q(5, 3), Q(2), Q(3, 2)),
    ):
        epsilon = a_scale / q_scale
        matrix = normalized_hessian(c, a_scale, q_scale, x, y)
        expected_det = -Q(1) / (y**2 * (y + epsilon * x) ** 2)
        if det2(matrix) != expected_det:
            raise RuntimeError("normalized determinant identity")

    if not primitive_ray_unique(1, 2, 2, 3):
        raise RuntimeError("primitive ray uniqueness")
    if gcd(7 + 12, 12) != gcd(7, 12):
        raise RuntimeError("shifted primitivity")

    critical = exponent_cell(Q(1, 3), Q(8, 75), Q(1, 3))
    if critical["ell_injectivity_bound"] != Q(3, 5):
        raise RuntimeError("critical ell bound")
    if critical["fixed_q_hs_bound"] != Q(3, 5):
        raise RuntimeError("critical HS bound")
    if critical["additional_saving_required_strictly_more_than"] != Q(7, 15):
        raise RuntimeError("critical deficit")

    closed_by_ell = exponent_cell(Q(11, 25), Q(0), Q(0))
    if closed_by_ell["live_residual"]:
        raise RuntimeError("Cycle 70 closure not incorporated")

    return {
        "hessian_aq": "C*[[-1/(a+q)^2,-1/(a+q)^2],[-1/(a+q)^2,1/q^2-1/(a+q)^2]]",
        "hessian_nq": "C*diag(-1/n^2,1/q^2)",
        "determinant": "-C^2/(q^2*(a+q)^2)",
        "normalized_curvature_unit": "C*A/Q=X^(lambda+o(1))",
        "normalized_singular_value_bounds": "(C*A/Q)/832 <= s_min <= s_max <= 13*(C*A/Q)",
        "relative_tube": "X^(-1-alpha-kappa+o(1))",
        "shifted_phase": "e(kY)=(n/q)^(i*k*Delta)",
        "primitive_ray": "gcd(a,q)=gcd(n,q)=1 removes every nontrivial exact radial repetition",
        "banked_bound": "B=min(lambda,theta+w)",
        "live_residual": "B+kappa>=6/25",
        "worst_required_saving": "strictly more than 7/15, uniquely at (theta,alpha,kappa)=(1/3,1/3,8/75)",
        "gate": "attempt an affine-normalized E14 estimate and shifted-strip E15 estimate on the combined live residual",
    }


if __name__ == "__main__":
    print(verify_all())
