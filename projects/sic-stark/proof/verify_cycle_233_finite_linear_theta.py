#!/usr/bin/env python3
"""Exact finite linear-theta divisor obstruction for Cycle 233/B070."""
from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction

try:  # Support direct replay and package-style regression imports.
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - exercised by direct replay.
    from verify_cycle_228_f3_square_residual_block import blocks


F = Fraction


@dataclass(frozen=True)
class Affine:
    """c+s*N with exact rational c,s and N constrained to N>=0."""

    constant: F
    slope: F

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(self.constant + other.constant, self.slope + other.slope)

    def __sub__(self, other: "Affine") -> "Affine":
        return Affine(self.constant - other.constant, self.slope - other.slope)

    def scale(self, scalar: F) -> "Affine":
        return Affine(scalar * self.constant, scalar * self.slope)

    def text(self) -> str:
        if self.slope == 0:
            return str(self.constant)
        return f"{self.constant}{'+' if self.slope >= 0 else ''}{self.slope}*N"


def _solve_zero_coefficients(item: dict[str, object]) -> tuple[Affine, Affine]:
    """Solve c*p_N=r*alpha+s*beta for the A pole p_N exactly."""
    c = F(item["argument_mu"])
    alpha = tuple(F(x) for x in item["alpha"])
    beta = tuple(F(x) for x in item["beta"])
    determinant = alpha[0] * beta[1] - alpha[1] * beta[0]
    assert determinant != 0
    # p_N=(-1,-5-24*N) in (omega1,omega2) coordinates.
    x = Affine(-c, F(0))
    y = Affine(-5 * c, -24 * c)
    r = (x.scale(beta[1]) - y.scale(beta[0])).scale(F(1, 1) / determinant)
    s = (y.scale(alpha[0]) - x.scale(alpha[1])).scale(F(1, 1) / determinant)
    return r, s


def _positive_for_every_nonnegative_n(value: Affine) -> bool:
    return value.constant >= 1 and value.slope >= 0


def residual_family_audit() -> dict[str, object]:
    block = blocks()["A"]
    rows = []
    for position, item in enumerate(block, 1):
        r, s = _solve_zero_coefficients(item)
        can_cancel = _positive_for_every_nonnegative_n(r) and _positive_for_every_nonnegative_n(s)
        assert not can_cancel
        rows.append({
            "position": position,
            "zero_lattice_r": r.text(),
            "zero_lattice_s": s.text(),
            "cancels_every_family_member": can_cancel,
        })
    expected = [
        ("-1", "0-1*N"),
        ("-24-115*N", "-5-24*N"),
        ("-24-115*N", "-5-24*N"),
        ("-1", "0-1*N"),
    ]
    assert [(row["zero_lattice_r"], row["zero_lattice_s"]) for row in rows] == expected
    return {
        "epistemic_status": "PROVED",
        "pole_family": "mu=-omega1-(5+24*N)*omega2 for every integer N>=0",
        "pole_source": "A first residual factor, (j,n)=(1,N)",
        "zero_checks": rows,
        "uncancelled_for_every_N_ge_0": True,
    }


def audit() -> dict[str, object]:
    residual = residual_family_audit()
    # If [(-1,-5-24N)]=[(-1,-5-24M)], the first coordinate forces the
    # projective scale to be 1, and then N=M.  Thus this is an infinite set
    # of directions.  q^m*ell has the same direction as ell, so a finite
    # theta product supplies only finitely many directions.
    return {
        "epistemic_status": "PROVED",
        "frozen_theta_family": "mu^a*product_{r=1}^Ntheta theta_q(mu/ell_r(omega1,omega2))^(e_r), with arbitrary finite N and linear ell_r",
        "residual_family": residual,
        "direction_invariant": {
            "residual_direction": "[-1:-5-24*N]",
            "residual_directions_pairwise_distinct": True,
            "theta_factor_direction": "[ell_r] for all q^m divisor translates",
            "finite_theta_product_directions": "finite",
            "comparison": "infinite residual direction set versus finite theta direction set",
        },
        "completion": {
            "finite_linear_theta_completion_exists": False,
            "status": "FALSIFIED_FOR_ENTIRE_FROZEN_FAMILY",
            "reason": "The uncancelled A residual pole family has infinitely many projective period directions, so it cannot be contained in the divisor of any finite linear-argument theta product.",
        },
        "reflection_and_normalization": {
            "status": "UNAVAILABLE_AFTER_DIVISOR_OBSTRUCTION",
            "reason": "A theta product that misses an infinite residual divisor family cannot enter reflection or source-normalization tests.",
        },
        "conclusion": "No finite product of q=1/576 theta factors with linear period-dependent arguments can absorb the frozen A residual block. This leaves nonlinear, multivariable, or infinite theta completions and all AFK, fusion, Stark, and TCC claims open.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
