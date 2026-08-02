"""Exact ledgers for Cycle 161's labelled high-cell refinement."""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence


def effective_multiplicity(weights: Sequence[Fraction]) -> Fraction:
    """Return (sum weights)^2 / sum weights^2 for nonnegative edge weights."""
    if any(weight < 0 for weight in weights):
        raise ValueError("edge weights must be nonnegative")
    square_mass = sum((weight * weight for weight in weights), Fraction())
    if not square_mass:
        return Fraction()
    return sum(weights, Fraction()) ** 2 / square_mass


def refined_class_witness(classes: Sequence[Sequence[Fraction]]) -> dict[str, Fraction]:
    """Certify a fixed finite refinement retains global multiplicity / class count."""
    if not classes:
        raise ValueError("at least one refined class is required")
    flat = tuple(weight for cell in classes for weight in cell)
    global_multiplicity = effective_multiplicity(flat)
    best = max((effective_multiplicity(cell) for cell in classes), default=Fraction())
    return {
        "global_effective_multiplicity": global_multiplicity,
        "class_count": Fraction(len(classes)),
        "best_refined_effective_multiplicity": best,
        "retained_lower_bound": global_multiplicity / len(classes),
    }


def disjoint_pair_mass_lower_bound(total_mass: Fraction, maximum_incidence: Fraction) -> Fraction:
    """Lower-bound ordered disjoint-edge mass using sum_x D_x=2 total_mass."""
    if total_mass < 0 or maximum_incidence < 0:
        raise ValueError("masses must be nonnegative")
    return max(Fraction(), total_mass * total_mass - 2 * total_mass * maximum_incidence)


def hub_effective_neighbor_lower_bound(
    *, hub_incidence: Fraction, total_square_mass: Fraction
) -> Fraction:
    """Lower-bound a hub's effective neighbor degree using the whole cell L2 mass."""
    if hub_incidence < 0 or total_square_mass < 0:
        raise ValueError("masses must be nonnegative")
    if not total_square_mass:
        return Fraction()
    return hub_incidence * hub_incidence / total_square_mass


def theorem_record() -> dict[str, object]:
    return {
        "finite_refinement": (
            "after discarding zero-weight edges, a 24-by-12 half-open circular difference/phase refinement has B=288 classes; "
            "some selected class has effective multiplicity at least the original cell multiplicity divided by B"
        ),
        "nondegenerate_case": (
            "for x_r=|b_r|, L=sum_r x_r, and D_x=sum_(r incident to x)x_r, if max_x D_x<tau L then "
            "the weighted ordered mass of pairs of edges with four distinct endpoints is at least (1-2tau)L^2"
        ),
        "phase_alignment": (
            "within one difference subcell and one coefficient-phase sector, |delta_r-delta_s|<=1/(24K) and the coefficient-phase gap is at most pi/6; "
            "for every integer k in the frozen nonnegative cutoff support K<=k<=2K the combined angle is at most pi/3, so "
            "Re(b_r conjugate(b_s)e(k(delta_r-delta_s)))>=|b_r b_s|/2"
        ),
        "star_case": (
            "if D_x>=tau L, one incoming or outgoing labelled common-anchor fan has incidence at least D_x/2 and effective neighbor degree at least "
            "(D_x/2)^2/E_j, hence at least tau^2/4 times the retained-cell effective multiplicity"
        ),
        "boundary": (
            "this conditional combinatorial refinement does not prove that Cycle-89 excess occurs, a rational web, a transport seed, a fourth-moment estimate, density, or intervals"
        ),
    }
