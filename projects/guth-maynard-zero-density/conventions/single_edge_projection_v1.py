"""Exact Cycle 62 single-edge projection ledger."""
from __future__ import annotations

from fractions import Fraction as Q


def single_edge_ledger(s: int, ordinary_kernel_square: Q, powered_kernel_square: Q) -> dict[str, object]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive ordinary-coordinate count")
    u = Q(ordinary_kernel_square)
    v = Q(powered_kernel_square)
    if not 0 <= u <= 1 or not 0 <= v <= 1:
        raise RuntimeError("normalized kernel squares")
    retained = (1 - v) * (1 - u) ** s
    lost = 1 - retained
    union_upper = v + s * u
    return {
        "s": s,
        "ordinary_kernel_square": u,
        "powered_kernel_square": v,
        "retained_fraction": retained,
        "lost_fraction": lost,
        "lost_fraction_union_upper": union_upper,
        "union_bound_verified": lost <= union_upper,
        "pointwise_status": "SINGLE_EDGE_SATURATES_AS_KERNELS_VANISH",
        "genuine_edge_vector": "beta_n=sum_(t,u)z_t conj(z_u)n^(-i(t-u))=|sum_t z_t n^(-it)|^2",
        "genuine_edge_nonnegative": True,
    }


def verify_all() -> dict[str, object]:
    s3 = single_edge_ledger(3, Q(1, 25), Q(1, 49))
    s4 = single_edge_ledger(4, Q(1, 25), Q(1, 49))
    if not s3["union_bound_verified"] or not s4["union_bound_verified"]:
        raise RuntimeError("single-edge union bound")
    zero = single_edge_ledger(4, 0, 0)
    if zero["retained_fraction"] != 1 or zero["lost_fraction"] != 0:
        raise RuntimeError("zero-kernel endpoint")
    return {
        "s3": s3,
        "s4": s4,
        "zero_kernel_endpoint": zero,
        "asymptotic_statement": "if |k(h)|<=X^-alpha and |k(mh)|<=X^-beta then loss<=sX^-2alpha+X^-2beta=o(1)",
        "analytic_gate": "use_nonnegative_multi_edge_convolution_and_row_set_structure_not_pointwise_projection",
    }


if __name__ == "__main__":
    print(verify_all())
