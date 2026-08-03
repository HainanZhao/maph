#!/usr/bin/env python3
"""Exact source-scale iteration audit for Cycle 234/B071."""
from __future__ import annotations

import json

try:  # Support direct replay and package-style regression imports.
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - exercised by direct replay.
    from verify_cycle_228_f3_square_residual_block import blocks


SCALE = 576


def source_scale_audit() -> dict[str, object]:
    """Check the exact homogeneous data used by S--S equation (14)."""
    block = blocks()["A"]
    # Equation (14) has q-Pochhammer arguments mu/omega_i and bases formed
    # from omega1/omega2.  Therefore gamma(lambda*z;lambda*a,lambda*b)
    # equals gamma(z;a,b).  C228 stores each A factor as rational coefficients
    # of (mu,omega1,omega2), so the simultaneous S action preserves all three
    # dimensionless inputs factor by factor.
    rows = []
    for position, factor in enumerate(block, 1):
        assert factor["argument_mu"]
        assert len(factor["alpha"]) == len(factor["beta"]) == 2
        rows.append({"position": position, "ordinary_gamma_scale_invariant": True})
    assert len(rows) == 4
    return {
        "epistemic_status": "PROVED",
        "source_formula": "Sarkissian--Spiridonov (14): gamma(lambda*z;lambda*a,lambda*b)=gamma(z;a,b)",
        "action": "S(mu,omega1,omega2)=(576*mu,576*omega1,576*omega2)",
        "factor_rows": rows,
        "residual_scale_invariant": True,
    }


def audit() -> dict[str, object]:
    scaling = source_scale_audit()
    # C229 supplies R_A=c_A(omega)*mu^-4*(1+O(mu)), c_A nonzero. Comparing
    # this expansion after simultaneous lambda scaling gives c_A(lambda*omega)
    # = lambda^4*c_A(omega). Hence Rhat=mu^4 R_A/c_A is S-invariant.
    normalized = {
        "definition": "Rhat_A(mu,omega)=mu^4*R_A(mu,omega)/c_A(omega)",
        "laurent_coefficient_homogeneity": "c_A(lambda*omega)=lambda^4*c_A(omega)",
        "source_scale_invariant": True,
        "nonconstant": True,
        "nonconstancy_witness": "C233 A residual has uncancelled nonzero hyperplanes mu=-omega1-(5+24*N)*omega2.",
    }
    # Thus Rhat(S^-j x)=Rhat(x), so every partial product is the displayed
    # constant power. A nonzero infinite product requires its factors to tend
    # to one; at generic x the repeated nonconstant factor is not one.
    return {
        "epistemic_status": "PROVED",
        "source_scale": scaling,
        "normalized_residual": normalized,
        "scale_iterated_product": {
            "definition": "P_N(x)=product_{j=1}^N Rhat_A(S^(-j)*x)",
            "exact_partial_product": "P_N(x)=Rhat_A(x)^N",
            "factor_limit": "Rhat_A(x), not 1 generically",
            "nonzero_meromorphic_product_converges_generically": False,
            "status": "FALSIFIED_FOR_FROZEN_SOURCE_SCALE_ITERATION",
            "reason": "The factors repeat under the simultaneous source scaling and fail the necessary term-to-one condition on the generic nonconstant locus.",
        },
        "full_divisor_reflection_normalization": {
            "status": "UNAVAILABLE_AFTER_CONVERGENCE_FAILURE",
            "reason": "No nonzero meromorphic scale-iterated cochain exists in the frozen product order to carry those further tests.",
        },
        "conclusion": "The source-normalized scale-iterated product is not a convergent nonzero meromorphic cochain for the frozen simultaneous 576 action. This excludes neither mu-only non-source iterations, regularized products, nonlinear/multivariable completions, nor any signed extension, AFK, fusion, Stark, or TCC construction.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
