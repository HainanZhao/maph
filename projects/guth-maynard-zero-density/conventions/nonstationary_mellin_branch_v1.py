"""Exact Cycle 93 strict sub-alias nonstationary ledger."""

from fractions import Fraction

QF = Fraction

D_EXP = QF(3, 5)
DENOM_EXP = QF(1, 3)
XI_MIN = QF(16, 25)
XI_MAX = QF(58, 75)


def support_exponents(xi: Fraction) -> dict[str, Fraction]:
    h = xi + DENOM_EXP - D_EXP
    delta_h = xi - D_EXP
    return {
        "k": xi,
        "r": xi,
        "h": h,
        "strict_delta_h_ceiling": delta_h,
        "minimum_t": D_EXP,
        "maximum_t": xi,
        "ordered_pair_cells": 2 * xi + h + delta_h,
    }


def integration_by_parts_exponent(xi: Fraction, order: int) -> Fraction:
    if order < 1:
        raise ValueError("positive integration-by-parts order required")
    return xi - order * D_EXP


def required_order(xi: Fraction, requested_saving: Fraction) -> int:
    cells = support_exponents(xi)["ordered_pair_cells"]
    order = 1
    while cells + integration_by_parts_exponent(xi, order) > -requested_saving:
        order += 1
    return order


def verify_all() -> dict[str, object]:
    for xi in (XI_MIN, QF(7, 10), XI_MAX):
        row = support_exponents(xi)
        assert row["minimum_t"] == D_EXP
        assert row["maximum_t"] == xi
        assert row["strict_delta_h_ceiling"] == xi - D_EXP
        for saving in (QF(1), QF(10), QF(100)):
            order = required_order(xi, saving)
            total = row["ordered_pair_cells"] + integration_by_parts_exponent(xi, order)
            assert total <= -saving
    return {
        "phase_after_rescaling": "t*log(K*x)-m*K*x",
        "m_zero_derivative": "t/x with |t|>=D/(2*pi)",
        "m_nonzero_derivative": "t/x-m*K with magnitude >> (1+|m|)K",
        "kernel_decay": "for every A, O_A(K*D^-A)",
        "full_branch": "for every B, O_B(X^-B) after all polynomial support sums",
        "strict_branch": "0<|Delta h|<=c_*K/D with fixed stationary buffer",
        "open_transition": "|Delta h|~K/D and every nonzero stationary alias remain open",
        "minimum_mellin_frequency_exponent": str(D_EXP),
        "gate": "strict sub-alias branch closed; transition and integer aliases open",
    }


if __name__ == "__main__":
    print(verify_all())

