"""Cycle 147 strict collision-core phase-wedge conventions."""

from __future__ import annotations

from math import cos, pi


def phase_wedge_floor(
    *, support_ceiling: float, core_radius_scaled: float, atom_phase_wedge: float
) -> float:
    """Cosine floor for |k|<=bK, ||t||<=r/K and atom phases in a wedge."""
    if support_ceiling <= 0 or core_radius_scaled < 0 or atom_phase_wedge < 0:
        raise ValueError("invalid strict-core phase data")
    angle = 2.0 * pi * support_ceiling * core_radius_scaled + 2.0 * atom_phase_wedge
    return cos(angle)


def signed_core_lower_bound(
    *, frequency_weight: float, pair_mass: float, cosine_floor: float
) -> float:
    if frequency_weight < 0 or pair_mass < 0 or cosine_floor < 0:
        raise ValueError("nonnegative strict-core data required")
    return frequency_weight * pair_mass * cosine_floor


def negative_halo_floor_scaled(*, support_ceiling: float) -> float:
    """Below this scaled radius every cos(2 pi k t) is nonnegative."""
    if support_ceiling <= 0:
        raise ValueError("positive support ceiling required")
    return 1.0 / (4.0 * support_ceiling)


def theorem_record() -> dict[str, object]:
    return {
        "strict_core": (
            "for a nonnegative dyadic cutoff supported on 0<k<=bK and circle "
            "residual ||t_e||<=1/(12bK), every Fourier phase has absolute "
            "argument at most pi/6"
        ),
        "phase_wedge": (
            "if atom coefficients lie within phase phi of one common ray, each "
            "oriented correlation product has phase at most 2phi; for phi<=pi/12 "
            "the real signed core is at least one half of frequency weight times "
            "the total pair-magnitude mass"
        ),
        "actual_chart_scope": (
            "Cycle 123's leading smooth coefficient has one explicit common phase "
            "and positive algebraic/Jacobian factors; a real nonzero interior "
            "symbol admits such a fixed-phase subchart, but its share of the full "
            "operator is not bounded below here"
        ),
        "negative_halo_gap": (
            "for exact common-phase coefficients, Re e(kt)>=0 throughout "
            "||t||<=1/(4bK); any negative contribution capable of cancelling the "
            "strict core must therefore use a residual outside that wider collar"
        ),
        "single_cell_obstruction": (
            "an isolated strict endpoint core cannot obtain cancellation from the "
            "high-pass frequency sum; Cycle 146's signed cells must be grouped with "
            "coefficient-faithful halo cells before an upper estimate is attempted"
        ),
        "mass_boundary": (
            "no theorem here says that a fixed-phase strict core carries a "
            "target-sized fraction of the original excessive quadratic form"
        ),
        "next_gate": (
            "construct balanced core--halo bundles using the exact periodic kernel "
            "and prove either a bundle estimate or a target-mass inverse"
        ),
        "boundary": (
            "this is a scoped adverse signed-cell estimate; no paired norm, "
            "endpoint, complete moment, density, or intervals is proved"
        ),
    }
