"""Exact row-local slack ledger for Cycle 174 forward transport."""
from __future__ import annotations

from fractions import Fraction as Q


ETA = Q(1, 2)


def residual_multiplier(*, h: int, h_plus: int, a: int, q: int, K: int, y: Q) -> Q:
    """Return h*y/(aK)=h_plus*y/(qK) for an integral forward edge."""
    if min(h, h_plus, a, q, K, y) <= 0:
        raise ValueError("positive row data required")
    if a * h_plus != q * h:
        raise ValueError("forward affine edge required")
    left, right = Q(h, a * K) * y, Q(h_plus, q * K) * y
    if left != right:
        raise RuntimeError("row-local residual multiplier")
    return left


def capacity_class(*, q: int, K: int, H: int) -> dict[str, int | str]:
    """Classify every admissible edge as saturated or one retained dyadic deficit."""
    if min(q, K, H) <= 0 or q * K > H:
        raise ValueError("admissible capacity data required")
    if Q(q * K, H) >= ETA:
        return {"kind": "capacity_saturated", "index": 0}
    index = 1
    while Q(q * K, H) <= Q(1, 2**index):
        index += 1
    # Now 2^-index < qK/H <= 2^-(index-1), matching D_(index-1).
    return {"kind": "capacity_deficit", "index": index - 1}


def saturated_transport(*, h: int, h_plus: int, a: int, q: int, K: int, H: int, y: Q, Y: Q) -> dict[str, Q | str]:
    """Certify fixed 4Y slack for a capacity-saturated labelled row."""
    if y <= 0 or Y < y:
        raise ValueError("valid fixed curve bound required")
    if not (H <= h <= 2 * H and H <= h_plus <= 2 * H):
        raise ValueError("frozen row range required")
    classification = capacity_class(q=q, K=K, H=H)
    if classification["kind"] != "capacity_saturated":
        raise ValueError("saturated row required")
    rho = residual_multiplier(h=h, h_plus=h_plus, a=a, q=q, K=K, y=y)
    if rho > 4 * Y:
        raise RuntimeError("fixed saturated slack")
    return {"class": "capacity_saturated", "rho": rho, "slack": 4 * Y, "target_constant": "C0+4Y*C1"}


def deficit_lower_bound(*, h: int, h_plus: int, a: int, q: int, K: int, H: int, y: Q) -> dict[str, Q | int | str]:
    """Retain a dyadic deficit index and its unavoidable row-local slack."""
    classification = capacity_class(q=q, K=K, H=H)
    if classification["kind"] != "capacity_deficit":
        raise ValueError("deficit row required")
    if not (H <= h <= 2 * H and H <= h_plus <= 2 * H):
        raise ValueError("frozen row range required")
    index = int(classification["index"])
    rho = residual_multiplier(h=h, h_plus=h_plus, a=a, q=q, K=K, y=y)
    lower = (2**index) * y
    if rho < lower:
        raise RuntimeError("dyadic deficit multiplier")
    return {"class": "capacity_deficit", "index": index, "rho": rho, "lower": lower}


def propagated_residual(*, source: Q, edge_error: Q, rho: Q) -> Q:
    """Exact C167 target residual after replacing the conservative bound by rho."""
    return source - rho * edge_error


def verify_all() -> dict[str, object]:
    # h=20, h+=10, a/q=2, K=10, H=10 is capacity saturated.
    saturated = saturated_transport(h=20, h_plus=10, a=2, q=1, K=10, H=10, y=Q(6, 5), Y=Q(3, 2))
    if saturated["rho"] != Q(6, 5) or saturated["slack"] != 6:
        raise RuntimeError("saturated transport")
    # qK/H=1/4 lies in D_2 and forces rho at least 4y.
    deficit = deficit_lower_bound(h=40, h_plus=20, a=2, q=1, K=5, H=20, y=Q(6, 5))
    if deficit["index"] != 2 or deficit["lower"] != Q(24, 5):
        raise RuntimeError("deficit ledger")
    if propagated_residual(source=Q(0), edge_error=Q(1, 100), rho=Q(6, 5)) != Q(-3, 250):
        raise RuntimeError("exact residual")
    return {
        "identity": "target residual equals source residual minus rho*(qE-a), with rho=h(1+alpha)/(aK)=h_plus(1+alpha)/(qK)",
        "saturated": "qK>=H/2 implies rho<=4Y, so the fixed strip constant C0+4Y*C1 is valid and Cycle67 keeps its depth exponent",
        "deficit": "2^(-(r+1))H<qK<=2^(-r)H retains labelled deficit index r and forces rho>=2^r(1+alpha)",
        "boundary": "This is a finite adaptive-slack classifier. It proves no actual saturated population, target-local packet, recurrence, skeleton, density, or interval gain.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
