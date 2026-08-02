"""Cycle 159 ray-multiplier information-loss conventions."""

from __future__ import annotations

from fractions import Fraction


def ray_atoms(*, numerator: int, denominator: int, multiplier: int) -> tuple[int, int]:
    """Return the ordered Cycle-92 collision atoms (n,n')=t(q,p)."""
    if numerator <= 0 or denominator <= 0 or multiplier <= 0:
        raise ValueError("positive primitive ray and multiplier required")
    return multiplier * denominator, multiplier * numerator


def multiplier_loss_witness(
    *,
    numerator: int,
    denominator: int,
    first_multiplier: int,
    second_multiplier: int,
    first_oriented_product: Fraction,
    second_oriented_product: Fraction,
) -> dict[str, object]:
    """Certify that metadata omitting t cannot reconstruct oriented weights."""
    if first_multiplier == second_multiplier or first_oriented_product == second_oriented_product:
        raise ValueError("need distinct multipliers with distinct oriented products")
    first_atoms = ray_atoms(numerator=numerator, denominator=denominator, multiplier=first_multiplier)
    second_atoms = ray_atoms(numerator=numerator, denominator=denominator, multiplier=second_multiplier)
    return {
        "retained_ray_metadata": (numerator, denominator),
        "first_multiplier": first_multiplier,
        "second_multiplier": second_multiplier,
        "first_ordered_atoms": first_atoms,
        "second_ordered_atoms": second_atoms,
        "first_oriented_product": first_oriented_product,
        "second_oriented_product": second_oriented_product,
        "minimal_repair": "retain the ray multiplier t, equivalently the ordered atom pair (n,n')",
    }


def theorem_record() -> dict[str, object]:
    return {
        "cycle124_input": (
            "Cycle 124 has coefficient atoms c_(a,n)(ell) indexed by the original polynomial variables (a,n)"
        ),
        "cycle92_ray_map": (
            "Cycle 92 writes every collision on one primitive ray as (n,n')=t(q,p), but the primitive ray label p/q omits t"
        ),
        "information_loss": (
            "whenever two admissible multipliers t1!=t2 have different oriented products "
            "c_(a',t_i p)(ell)conjugate(c_(a,t_i q)(ell)), no pushforward depending only on the retained primitive-ray metadata "
            "can reconstruct both coefficient products"
        ),
        "minimal_missing_label": (
            "within the original atom labels, the ray multiplier t, equivalently the ordered atom pair (n,n'), is the minimal repair once p/q and the ordered modes are retained"
        ),
        "boundary": (
            "this is an information-loss theorem for any nonconstant coefficient fibre with two admissible ray multipliers; "
            "it does not assert such a pair has target mass in the frozen operator or prove a moment, density, or intervals"
        ),
    }
