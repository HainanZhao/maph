"""Exact Cycle 63 averaged logarithmic transport exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
H = Q(11, 25)
STRIP = Q(-1)
HS_POINTWISE = Q(8, 25)
DESIRED_AVERAGE_WRAP = Q(1, 5)


def transport_ledger() -> dict[str, object]:
    summed_hs = H + HS_POINTWISE
    desired_total = H + DESIRED_AVERAGE_WRAP
    random_volume = H + DELTA + STRIP
    averaging_saving_required = summed_hs - desired_total
    desired_pair_census = 2 * desired_total - DELTA
    crude_pair_census = 2 * H + HS_POINTWISE
    random_difference_pair_volume = DELTA + 2 * H + STRIP
    return {
        "delta_exponent": DELTA,
        "h_exponent": H,
        "strip_width_exponent": STRIP,
        "pointwise_hs_count": HS_POINTWISE,
        "summed_pointwise_census": summed_hs,
        "desired_average_wrap_open_endpoint": DESIRED_AVERAGE_WRAP,
        "desired_total_census_open_endpoint": desired_total,
        "saving_beyond_summed_hs_required": averaging_saving_required,
        "random_volume_census": random_volume,
        "surface": "F(h,ell)=h(exp(2pi ell/Delta)-1)",
        "mixed_derivative": "F_(h ell)=(2pi/Delta)exp(2pi ell/Delta)",
        "hessian_determinant": "-(2pi/Delta)^2 exp(4pi ell/Delta)",
        "hessian_determinant_exponent": -2 * DELTA,
        "transport_difference": "F(h+d,ell)-F(h,ell)=d alpha_ell",
        "pair_condition": "||d alpha_ell||<=2C/X",
        "desired_pair_census_open_endpoint": desired_pair_census,
        "crude_hs_pair_census": crude_pair_census,
        "random_difference_pair_volume": random_difference_pair_volume,
    }


def verify_all() -> dict[str, object]:
    data = transport_ledger()
    if data["summed_pointwise_census"] != Q(19, 25):
        raise RuntimeError("summed Huxley--Sargos census")
    if data["desired_total_census_open_endpoint"] != Q(16, 25):
        raise RuntimeError("desired transport census")
    if data["saving_beyond_summed_hs_required"] != Q(3, 25):
        raise RuntimeError("averaging saving")
    if data["random_volume_census"] != Q(1, 25):
        raise RuntimeError("random volume")
    if data["hessian_determinant_exponent"] != -Q(6, 5):
        raise RuntimeError("Monge--Ampere scale")
    if data["desired_pair_census_open_endpoint"] != Q(17, 25):
        raise RuntimeError("pair census target")
    if data["crude_hs_pair_census"] != Q(6, 5):
        raise RuntimeError("crude pair census")
    if data["random_difference_pair_volume"] != Q(12, 25):
        raise RuntimeError("random pair volume")
    return {
        "transport": data,
        "analytic_gate": "prove_weighted_beta_free_pair_census_below_X^17_25_or_direct_triple_census_below_X^16_25",
    }


if __name__ == "__main__":
    print(verify_all())
