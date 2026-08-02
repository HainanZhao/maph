"""Cycle 146 zero-mode-free Gram kernel and signed-cell conventions."""

from __future__ import annotations

from collections.abc import Sequence


def circle_mean(fourier_coefficients: dict[int, complex]) -> complex:
    return fourier_coefficients.get(0, 0j)


def gram_quadratic_form(
    frequencies: Sequence[int],
    weights: Sequence[float],
    atom_coefficients: Sequence[complex],
    phases: Sequence[complex],
) -> float:
    """Return sum_k weight_k |sum_j c_j phase_j^k|^2."""
    if not (len(frequencies) == len(weights)) or len(atom_coefficients) != len(phases):
        raise ValueError("incompatible Gram data")
    if any(weight < 0 for weight in weights):
        raise ValueError("Gram weights must be nonnegative")
    return sum(
        weight * abs(sum((coefficient * phase**frequency for coefficient, phase in zip(atom_coefficients, phases)), 0j)) ** 2
        for frequency, weight in zip(frequencies, weights)
    )


def signed_cell_witness(real_contributions: Sequence[float]) -> tuple[int, float]:
    if not real_contributions:
        raise ValueError("at least one arithmetic cell is required")
    index = max(range(len(real_contributions)), key=real_contributions.__getitem__)
    return index, real_contributions[index]


def positive_majorant_mass(width: float, height: float = 1.0) -> float:
    if width < 0 or height < 0:
        raise ValueError("nonnegative core data required")
    return width * height


def theorem_record() -> dict[str, object]:
    return {
        "highpass_kernel": (
            "Psi_K(t)=sum_k U(k/K)e(kt)=K sum_m hat U(K(m-t)); because the "
            "frequency block is supported away from zero, its circle mean is U(0)=0"
        ),
        "gram_feature": (
            "when U(k/K)>=0, the pair kernel is the Gram kernel of features "
            "sqrt(U(k/K))e(kz); the missing k=0 coordinate is exactly the removed volume mode"
        ),
        "balanced_real_part": (
            "Re Psi_K has integral zero, so its positive and negative L1 masses "
            "are equal; any nonnegative replacement discards the compensating halo"
        ),
        "majorant_cost": (
            "a nonnegative replacement of height at least one on a collision core "
            "of circle width w has mean at least w; after the natural K scaling, "
            "a width 1/K core contributes a constant zero-mode cost per atom pair"
        ),
        "signed_partition": (
            "if a deterministic partition has P cells with real signed contributions "
            "q_C and sum_C q_C=E, then one cell has q_C>=E/P; the exact factor P "
            "must be charged in the exponent ledger"
        ),
        "coefficient_preservation": (
            "define each q_C before absolute values using the original Fourier "
            "frequency, oriented product c_j' conjugate(c_j), and phase difference; "
            "continued-fraction, orientation, anchor, and tail labels may then be "
            "attached without changing the signed equality"
        ),
        "next_gate": (
            "construct an arithmetic partition whose charged entropy still leaves "
            "a target-sized signed cell, then estimate or invert that cell while "
            "retaining its high-pass Fourier feature"
        ),
        "boundary": (
            "the signed partition is an exact interface only; no arithmetic cell "
            "bound, paired norm, endpoint, complete moment, density, or intervals is proved"
        ),
    }
