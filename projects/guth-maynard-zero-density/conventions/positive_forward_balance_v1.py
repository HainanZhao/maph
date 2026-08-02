"""Exact Cycle-173 positive-forward conservative balance obstruction."""
from __future__ import annotations

from fractions import Fraction as Q


def forward_bounds(*, H: Q, h: Q, h_plus: Q, a: int, q: int, K: Q, y_bound: Q, slack: Q) -> dict[str, Q]:
    """Verify the two exact bounds in the frozen forward direct-map ledger."""
    if min(H, h, h_plus, a, q, K, y_bound, slack) <= 0:
        raise ValueError("positive forward data required")
    if not (H <= h <= 2 * H and H <= h_plus <= 2 * H):
        raise ValueError("row range required")
    if h_plus != Q(q, a) * h:
        raise ValueError("forward affine map required")
    if q * K > H:
        raise ValueError("admissibility required")
    if Q(2) * H * y_bound * slack > a * K:
        raise ValueError("conservative balance required")
    ratio = Q(a, q)
    upper = h / h_plus
    lower = Q(2) * y_bound * slack
    if ratio != upper or ratio > 2 or ratio < lower:
        raise RuntimeError("forward endpoint squeeze")
    return {"a_over_q": ratio, "range_upper": Q(2), "balance_lower": lower}


def positive_forward_infeasible(*, y_bound: Q, slack: Q) -> dict[str, Q | str]:
    """State the contradiction before attempting to construct a forbidden row."""
    if y_bound <= 1 or slack < 1:
        raise ValueError("strict positive branch and registered slack required")
    lower = Q(2) * y_bound * slack
    if lower <= 2:
        raise RuntimeError("strict positive endpoint lost")
    return {
        "range": "a/q=h/h_plus<=2",
        "balance": "a/q=(aK)/(qK)>=2Y C_*",
        "strict_lower": lower,
        "conclusion": "2Y C_*>2 contradicts the simultaneous forward dyadic row ranges",
    }


def verify_all() -> dict[str, object]:
    contradiction = positive_forward_infeasible(y_bound=Q(101, 100), slack=Q(1))
    if contradiction["strict_lower"] != Q(101, 50):
        raise RuntimeError("positive endpoint")
    # The endpoint Y=1, C_*=1 is the only non-strict formal boundary and is
    # realized by h=2H, h_plus=H, a/q=2; it is excluded by alpha_ell>0.
    endpoint = forward_bounds(H=Q(10), h=Q(20), h_plus=Q(10), a=2, q=1, K=Q(10), y_bound=Q(1), slack=Q(1))
    if endpoint["a_over_q"] != 2:
        raise RuntimeError("endpoint model")
    return {
        "obstruction": "on alpha_ell>0 with Y>=1+alpha_ell>1 and C_*>=1, the forward conservative balance/admissibility/range ledger is inconsistent",
        "endpoint": "Y=C_*=1 gives only the formal h=2H,h_plus=H,a/q=2 endpoint, excluded by the positive branch",
        "scope": "forward orientation and the frozen conservative balance gate only; reverse orientation, extra strip slack, and different maps remain open",
        "boundary": "This proves a positive-forward conservative-gate obstruction. It does not prove that every actual beta-preserving transport or global coupling is impossible.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
