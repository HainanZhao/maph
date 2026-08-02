"""Cycle 160 coefficient-weighted off-diagonal condenser ledger."""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence


def effective_codegree(weights: Sequence[Fraction]) -> Fraction:
    """The weighted effective occupancy (sum |b|)^2 / sum |b|^2 of one cell."""
    if any(weight < 0 for weight in weights):
        raise ValueError("cell magnitudes must be nonnegative")
    l2_squared = sum((weight * weight for weight in weights), Fraction())
    if not l2_squared:
        return Fraction()
    return sum(weights, Fraction()) ** 2 / l2_squared


def condenser_ledger(
    *,
    atom_l2_mass: Fraction,
    off_pair_l2_mass: Fraction,
    maximum_effective_codegree: Fraction,
    cutoff_mass_over_k: Fraction,
    kernel_schur_constant: Fraction,
) -> dict[str, Fraction]:
    """Normalize the diagonal-plus-off-diagonal fourth-moment bound by K."""
    if min(atom_l2_mass, off_pair_l2_mass, maximum_effective_codegree, cutoff_mass_over_k, kernel_schur_constant) < 0:
        raise ValueError("nonnegative condenser inputs required")
    diagonal_baseline = cutoff_mass_over_k * atom_l2_mass * atom_l2_mass
    off_diagonal_bound = kernel_schur_constant * maximum_effective_codegree * off_pair_l2_mass
    return {
        "diagonal_baseline_over_k": diagonal_baseline,
        "off_diagonal_bound_over_k": off_diagonal_bound,
        "fourth_moment_bound_over_k": 2 * (diagonal_baseline + off_diagonal_bound),
    }


def theorem_record() -> dict[str, object]:
    return {
        "exact_pair_difference": (
            "|S_k|^2=A_2+P_off(k), where A_2=sum_u|a_u|^2 and P_off is the sum over ordered u!=v of "
            "a_u conjugate(a_v)e(k(z_u-z_v))"
        ),
        "weighted_codegree": (
            "for a K^(-1)-scale pair-difference cell I, rho_I=sum_(r in I)|b_r|^2 and "
            "C_I=(sum_(r in I)|b_r|)^2/rho_I, with C_I=0 when rho_I=0"
        ),
        "schur_condenser": (
            "a frozen smooth nonnegative cutoff has kernel |L_K(t)|<=C_U K(1+K||t||)^(-A); the finite-overlap cell Schur bound gives "
            "sum_k U(k/K)|P_off(k)|^2<=C K(max_I C_I)sum_(u!=v)|a_u a_v|^2<=C K(max_I C_I)A_2^2"
        ),
        "excess_inverse": (
            "therefore M4<=C K A_2^2(1+max_I C_I); an M4 excess X^(1/75-o(1)) over K A_2^2 forces a labelled off-diagonal cell "
            "with effective codegree X^(1/75-o(1)), hence in particular X^(1/150-o(1))"
        ),
        "colored_configuration": (
            "two ordered pairs in one retained cell obey ||(z_u-z_v)-(z_u'-z_v')||=O(1/K), equivalently the candidate phase relation "
            "z_u+z_v'=z_u'+z_v+O(1/K); coincident vertices are retained as labelled degenerate rows, so this is not yet a phase-aligned colored four-cycle"
        ),
        "boundary": (
            "this condenser does not prove the Cycle-89 fourth-moment excess, a low-codegree hypothesis, a phase-aligned nondegenerate colored four-cycle, a moment, density, or intervals"
        ),
    }
