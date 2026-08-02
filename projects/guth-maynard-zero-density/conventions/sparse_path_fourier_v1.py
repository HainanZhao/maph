"""Cycle 143 sparse-path layering and coefficient-moment ledger."""

from __future__ import annotations

from fractions import Fraction


def layered_large_sieve_factor(path_layers: int) -> int:
    if path_layers < 1:
        raise ValueError("positive layer count required")
    return path_layers


def scalar_threshold(rho: Fraction, tau: Fraction) -> dict[str, Fraction]:
    if tau <= rho:
        raise ValueError("tail frequency must be positive")
    frequency = tau - rho
    return {
        "frequency": frequency,
        "kappa_threshold": 2 * rho - frequency,
        "kappa_threshold_simplified": 3 * rho - tau,
        "rational_error_threshold": 2 * rho - 2 * tau,
    }


def signed_moments(weights: tuple[Fraction, ...], labels: tuple[Fraction, ...], order: int) -> tuple[Fraction, ...]:
    if len(weights) != len(labels) or order < 0:
        raise ValueError("invalid moment data")
    return tuple(sum((w * x**m for w, x in zip(weights, labels)), Fraction(0)) for m in range(order + 1))


def theorem_record() -> dict[str, object]:
    return {
        "path_layering": (
            "each fixed-multiplier path has Lambda=O(log N) edges; grouping by "
            "path position produces Lambda layers of distinct height-N rational labels"
        ),
        "layer_bound": (
            "the separated-label large sieve on every layer and Cauchy across "
            "layers give M2<<Lambda(L+N^2/|kappa_d|)sum|w_a|^2"
        ),
        "self_duality": (
            "Lambda=X^{o(1)}, so sparse-path decomposition leaves the power-scale "
            "threshold |kappa_d|>>N^2/L=N^3/S unchanged"
        ),
        "scoped_saturator": (
            "in the arbitrary-weight class, if L|kappa_d| is sufficiently small "
            "and all weights have one sign, every phase is coherent and the second "
            "moment has size L|E_d|^2"
        ),
        "moment_expansion": (
            "for small kappa_d, the paired sum expands through signed moments "
            "M_m(d)=sum_a w_a x_a^m; M_0=sum_a w_a is the first surviving lock"
        ),
        "replacement_invariant": (
            "any improvement beyond the arbitrary-weight sparse-path architecture "
            "must use cancellation in the actual signed moment hierarchy, or an "
            "equivalent coefficient-sensitive cross-component invariant"
        ),
        "boundary": (
            "the actual signed moments are not bounded here; no paired norm, endpoint, "
            "moment theorem, density, or prime intervals is proved"
        ),
    }
