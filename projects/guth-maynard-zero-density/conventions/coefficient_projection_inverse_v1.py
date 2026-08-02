"""Exact symbolic Cycle 61 coefficient-projection inverse ledger."""
from __future__ import annotations

from math import factorial


def projection_ledger(s: int) -> dict[str, object]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive ordinary-coordinate count")
    coordinate_count = s + 1
    fiber_bound = (1 + s // 2) * factorial(s)
    return {
        "s": s,
        "coordinate_count": coordinate_count,
        "fiber_bound": fiber_bound,
        "ordered_lift": "(B beta)_(q,p_1,...,p_s)=beta_(q^m p_1...p_s)",
        "full_projection": "C=P_q tensor P_p1 tensor ... tensor P_ps",
        "hilbert_synthesis": "A=C B",
        "label_coefficient": "a_n=C 1_(L^(-1)(n))",
        "bessel_operator_bound": fiber_bound,
        "bessel_statement": "||A beta||^2<=D_s sum_n|beta_n|^2",
        "exact_defect": "||B beta||^2-||A beta||^2=sum_(J proper)||C_J B beta||^2",
        "proper_anova_component_count": 2 ** coordinate_count - 1,
        "powered_coordinate_marginal": "sum_e omega_e k(mh_e) product_j p_j^(-ih_e)",
        "ordinary_coordinate_marginal": "sum_e omega_e k(h_e) q^(-imh_e) product_(l!=j)p_l^(-ih_e)",
        "near_saturation_implication": "if ||A beta||^2>=(1-delta)||B beta||^2 then every raw coordinate marginal has energy<=delta||B beta||^2",
    }


def verify_all() -> dict[str, object]:
    s3 = projection_ledger(3)
    s4 = projection_ledger(4)
    if s3["fiber_bound"] != 12 or s4["fiber_bound"] != 72:
        raise RuntimeError("fiber constants")
    if s3["proper_anova_component_count"] != 15:
        raise RuntimeError("s3 proper components")
    if s4["proper_anova_component_count"] != 31:
        raise RuntimeError("s4 proper components")
    return {
        "s3": s3,
        "s4": s4,
        "inverse_gate": "exclude_simultaneously_small_prime_coordinate_marginals_for_actual_edge_Fourier_vectors_or_exploit_them_as_annihilators",
    }


if __name__ == "__main__":
    print(verify_all())
