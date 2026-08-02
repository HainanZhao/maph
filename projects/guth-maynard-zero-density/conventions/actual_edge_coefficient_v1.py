"""Cycle 144 coefficient-faithful edge-measure conventions."""

from __future__ import annotations

from collections.abc import Sequence


def correlation_weights(
    left: Sequence[complex], right: Sequence[complex]
) -> tuple[complex, ...]:
    """Return the oriented coefficients right*conjugate(left)."""
    if len(left) != len(right):
        raise ValueError("edge coefficient arrays must have equal length")
    return tuple(r * l.conjugate() for l, r in zip(left, right))


def frequency_dependent_moments(
    edge_weights: Sequence[Sequence[complex]],
    labels: Sequence[complex],
    order: int,
) -> tuple[tuple[complex, ...], ...]:
    """Return one moment vector for every frequency slice."""
    if order < 0:
        raise ValueError("moment order must be nonnegative")
    result = []
    for weights in edge_weights:
        if len(weights) != len(labels):
            raise ValueError("weight and label arrays must have equal length")
        result.append(
            tuple(sum((w * x**m for w, x in zip(weights, labels)), 0j) for m in range(order + 1))
        )
    return tuple(result)


def theorem_record() -> dict[str, object]:
    return {
        "correlation_identity": (
            "if T(ell)=sum_j c_j(ell)e(-ell z_j), then |T(ell)|^2 is the "
            "sum over oriented pairs (j,j') with coefficient "
            "c_(j')(ell) conjugate(c_j(ell)) and phase e(-ell(z_(j')-z_j))"
        ),
        "typed_boundary": (
            "Cycle 124 records coefficient functions w_alpha(a,n;ell), while "
            "Cycles 132--134 extract support, multiplicity, rational labels, and "
            "continued-fraction decorations from an excess-energy witness; no "
            "sealed coefficient-preserving pushforward to the scalar w_a of "
            "Cycle 135 is defined"
        ),
        "cycle143_correction": (
            "the Cycle-143 moments are the correct hierarchy for a scalar "
            "frequency-independent edge vector, but they are not yet identified "
            "with the actual alias coefficients; the actual formal moments are "
            "M_m(d;ell)=sum_e c_(e,+)(ell)conjugate(c_(e,-)(ell))x_e^m"
        ),
        "minimal_measure": (
            "the next inverse must transport the complex ell-dependent measure "
            "nu_(d,ell)=sum_e c_(e,+)(ell)conjugate(c_(e,-)(ell)) delta_"
            "(x_e,theta_e^-,theta_e^+,s_e^-,s_e^+) together with its tensor and "
            "anchor labels"
        ),
        "leading_chart": (
            "before tensor separation, every algebraic and Jacobian factor in "
            "the Cycle-123 leading coefficient is positive and its only explicit "
            "stationary phase is the common e(1/8); any real smooth symbol nonzero "
            "at an interior point therefore has a smaller fixed-sign chart"
        ),
        "no_forced_vanishing": (
            "the global vanishing moments of the Cycle-122 radial kernel eliminate "
            "the zero Poisson mode; they do not imply M_0(d;ell)=0 for the surviving "
            "nonzero aliases, and the sealed formulas contain no other identity "
            "forcing that vanishing"
        ),
        "next_gate": (
            "prove a coefficient-preserving weighted collision inverse for "
            "nu_(d,ell), or prove tensor-frequency factorization reducing it to "
            "one scalar edge vector; only then test zeroth and higher moments"
        ),
        "boundary": (
            "this is an interface and correction theorem, not a signed-moment "
            "estimate or a one-sign saturator for the full operator; no paired "
            "norm, endpoint, complete moment, density, or interval theorem follows"
        ),
    }
