"""Exact Cycle 64 primitive Farey-packet exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
H = Q(11, 25)
WINDOW = Q(-1)
PAIR_TARGET = Q(17, 25)


def packet_ledger() -> dict[str, object]:
    farey_separation = -2 * H
    curve_spacing = -DELTA
    packet_weight_prefactor = 2 * H
    packet_mass_target = PAIR_TARGET - packet_weight_prefactor
    random_packet_mass = DELTA + WINDOW
    return {
        "delta_exponent": DELTA,
        "h_exponent": H,
        "ratio_window_exponent_worst": WINDOW,
        "farey_separation_exponent": farey_separation,
        "curve_spacing_exponent": curve_spacing,
        "window_smaller_than_farey_gap_margin": farey_separation - WINDOW,
        "window_smaller_than_curve_gap_margin": curve_spacing - WINDOW,
        "unique_reduced_approximant_per_ell": WINDOW < farey_separation,
        "unique_ell_per_reduced_approximant": WINDOW < curve_spacing,
        "packet_definition": "(ell,a/q) reduced with |alpha_ell-a/q|<=C/(qX)",
        "multiple_definition": "d=kq, j=ka",
        "weighted_multiples_upper": "sum_(k<=H/q)(H-kq)<=H^2/(2q)",
        "packet_weight_prefactor_exponent": packet_weight_prefactor,
        "pair_target_exponent_open": PAIR_TARGET,
        "harmonic_packet_mass_target_open": packet_mass_target,
        "random_harmonic_packet_mass_exponent": random_packet_mass,
        "random_margin_to_target": packet_mass_target - random_packet_mass,
    }


def verify_all() -> dict[str, object]:
    data = packet_ledger()
    if data["farey_separation_exponent"] != -Q(22, 25):
        raise RuntimeError("Farey separation")
    if data["window_smaller_than_farey_gap_margin"] != Q(3, 25):
        raise RuntimeError("Farey uniqueness margin")
    if data["window_smaller_than_curve_gap_margin"] != Q(2, 5):
        raise RuntimeError("curve uniqueness margin")
    if not data["unique_reduced_approximant_per_ell"] or not data["unique_ell_per_reduced_approximant"]:
        raise RuntimeError("packet uniqueness")
    if data["harmonic_packet_mass_target_open"] != -Q(1, 5):
        raise RuntimeError("packet mass target")
    if data["random_harmonic_packet_mass_exponent"] != -Q(2, 5):
        raise RuntimeError("random packet mass")
    if data["random_margin_to_target"] != Q(1, 5):
        raise RuntimeError("random packet margin")
    return {
        "packet": data,
        "analytic_gate": "prove_harmonic_packet_mass_below_X^-1_5_with_strict_margin_or_extract_low_denominator_recurrence",
    }


if __name__ == "__main__":
    print(verify_all())
