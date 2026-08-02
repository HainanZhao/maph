"""Exact slope-shift correction for Cycle 184's nonrational family."""
from __future__ import annotations

from fractions import Fraction as Q

from conventions.ray_box_determinant_orbit_v1 import nonrational_two_ray_family, require


def corrected_two_ray_family(t: int) -> dict[str, object]:
    original = nonrational_two_ray_family(t)
    V, U = t**11, t**22
    B = (3 * V + 1) // 2
    A_left, A_right = B - V, B * B - V * V
    F = U * A_left - V * A_right
    require(F == V * B * (V - B) and F != 0, "shifted primitive determinant")
    require(Q(A_left, V) == Q(B, V) - 1, "left shifted slope")
    require(Q(A_right, U) == Q(B * B, V * V) - 1, "right shifted slope")
    return {
        "phase": "z=r^(1/n), alpha_n=r-1, alpha_2n=r^2-1",
        "shifted_slopes": {"left": Q(A_left, V), "right": Q(A_right, U)},
        "residual_transfer": "h*((q-1)-(r-1))=h*(q-r), and similarly at 2n; original residual bounds are unchanged",
        "determinant": {"F": F, "formula": "V^2*(B-V)-V*(B^2-V^2)=V*B*(V-B)"},
        "surviving_original_ledger": {"fibres": original["fibres"], "populated_box": original["populated_box"]},
    }


def verify_all() -> dict[str, object]:
    sample = corrected_two_ray_family(3)
    return {
        "original_deformation_disposition": "WITHHELD only as written: alpha_j=z^j conflicts with the pinned alpha_j=z^j-1 convention.",
        "corrected_deformation": "The same nonrational two-label family has shifted rational slopes q-1 and q^2-1, unchanged residual bounds, the same nonzero stable determinant, and the same sub-seed box scale.",
        "boundary": "The LCM-resonance redundancy remains valid. This corrected two-label subcritical deformation proves no critical-box saturation or density consequence.",
        "samples": {"T3": sample},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
