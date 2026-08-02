"""Cycle 153 exact routing of a negative divisor-comb correlation."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


ESCAPE_REASONS = frozenset(
    {
        "boundary_denominator",
        "phase_changing_chart",
        "nonsmooth_payload",
        "unbounded_tau",
        "failed_rational_label",
        "inadmissible_lcm",
        "registered_truncation",
    }
)


def strict_negative_mass(real_correlations: Iterable[Fraction]) -> Fraction:
    return sum((max(-value, Fraction()) for value in real_correlations), Fraction())


def routing_dichotomy(*, post_error_negative_mass: Fraction, strict_real_correlations: Iterable[Fraction]) -> dict[str, object]:
    """Route a normalized negative residual into strict mass or escape mass.

    The input means -Re(H) >= post_error_negative_mass and H=S+E.  The
    returned escape lower bound is -Re(E) >= mu - N_S.
    """
    if post_error_negative_mass <= 0:
        raise ValueError("a positive post-error negative mass is required")
    strict_rows = tuple(strict_real_correlations)
    strict_mass = strict_negative_mass(strict_rows)
    escape_lower_bound = post_error_negative_mass - strict_mass
    half = post_error_negative_mass / 2
    if strict_mass >= half:
        route = "STRICT_LABELLED_MASS"
    else:
        route = "LABELLED_ESCAPE_OBLIGATION"
        if escape_lower_bound < half:
            raise AssertionError("routing inequality failed")
    return {
        "post_error_negative_mass": post_error_negative_mass,
        "strict_negative_mass": strict_mass,
        "escape_correlation_lower_bound": escape_lower_bound,
        "threshold": half,
        "route": route,
    }


def validate_partition(*, strict_ids: Iterable[str], escape_rows: Iterable[tuple[str, str]]) -> None:
    strict_rows = tuple(strict_ids)
    strict = set(strict_rows)
    escape = list(escape_rows)
    escape_ids = {mode_id for mode_id, _ in escape}
    if len(strict) != len(strict_rows):
        raise ValueError("duplicate strict mode")
    if len(escape_ids) != len(escape):
        raise ValueError("duplicate escape mode")
    if strict & escape_ids:
        raise ValueError("partition is not disjoint")
    if any(reason not in ESCAPE_REASONS for _, reason in escape):
        raise ValueError("unregistered escape reason")


def theorem_record() -> dict[str, object]:
    return {
        "routing_identity": (
            "for H=S+E and -Re(H)>=mu_*, N_S=sum_b(-Re gamma_b)_+ gives "
            "-Re(E)>=mu_*-N_S"
        ),
        "dichotomy": (
            "either N_S>=mu_*/2, or the labelled escape class has negative "
            "correlation at least mu_*/2 in the same one-witness normalization"
        ),
        "label_audit": (
            "strict modes retain b,w_b,r_b,h_b,d_b,m_b,L_b,tau_b,gamma_b; every "
            "other mode has one registered escape reason in an exhaustive disjoint partition"
        ),
        "cycle152_interface": (
            "the strict branch activates Cycle 152 only after a separate normalized-weight "
            "and uniform per-mode bound 0<=(-Re gamma_b)_+<=Cw_b/m_b is proved or imported"
        ),
        "boundary": (
            "this exact routing compiler bounds neither branch and proves no full moment, density, or intervals"
        ),
    }
