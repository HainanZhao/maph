#!/usr/bin/env python3
"""Exact constructed-current audit for Cycle 244/B081."""
from __future__ import annotations

import json
from fractions import Fraction as F


def audit() -> dict[str, object]:
    # t+t^(-1)=110 and t*t^(-1)=1.  The C243 support primitive is
    # a=115*t-1, with positive conjugate a'=115/t-1.
    trace = F(115 * 110 - 2)
    norm = F(115 * 115 - 115 * 110 + 1)
    assert trace == 12648
    assert norm == 576
    # Positive trace and norm make the two real roots positive.  Hence
    # v_N=N*(a,a') leaves every compact subset of R^2.
    assert trace > 0 and norm > 0

    residue_classes = list(range(1, 12))
    assert len(residue_classes) == 11
    current = {
        "state": "J_{rho,r}=sum_{M>=0} rho^(12*M+r) kappa_{12*M+r} delta_{v_{12*M+r}}",
        "support": "v_N=N*(115*t_+-1,115*t_--1), N>=1, 12 does not divide N",
        "coefficient_line": "(kappa_N^+,kappa_N^-), the A-word double-pole principal-coefficient line",
        "test_space": "C_c^infinity(R^2; C^2)",
        "galois_action": "swap the two coordinates and coefficient components",
    }
    # Local finiteness makes the sum finite on every compactly supported test
    # function, so rho->1 is coefficientwise and distributionally defined.
    boundary = {
        "support_proper": True,
        "locally_finite": True,
        "rho_to_one_distributional_boundary_exists": True,
        "reason": "both coordinates of the primitive support vector are positive, so each compact test support meets only finitely many v_N",
        "all_nonzero_mod_12_classes_retained": residue_classes,
    }
    # No source normalization freezes the exponential coefficient gauge.
    # For lambda>0, lambda^N preserves all declared support, Galois, and
    # dissection axioms.  A bump around v_1 distinguishes lambda!=1 because
    # kappa_1 is a nonzero C243 double-pole coefficient.
    ambiguity = {
        "deformation": "kappa_N -> lambda^N*kappa_N for lambda>0",
        "preserves_support": True,
        "preserves_galois_swap": True,
        "preserves_12_dissection": True,
        "preserves_local_finiteness_and_boundary": True,
        "changes_boundary_for_lambda_not_1": True,
        "compact_test_witness": "a smooth bump supported near v_1 and equal to one there",
        "intrinsic_regulator_normalization_available": False,
    }
    return {
        "epistemic_status": "PROVED",
        "support_invariant": {"trace": str(trace), "norm": str(norm), "both_embedding_coordinates_positive": True},
        "current": current,
        "boundary": boundary,
        "normalization_ambiguity": ambiguity,
        "source_authorization": False,
        "status": "CONSTRUCTED_LOCAL_FINITE_ABEL_CURRENT_NONCANONICAL",
        "conclusion": "The explicitly constructed A-residual 12-dissected current has a rho-to-one locally finite distributional boundary and exact Galois swap symmetry. Its lambda^N deformation preserves every frozen construction axiom while changing that boundary, so the construction has no intrinsic regulator normalization. It is not source-authorized and supplies no contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC consequence.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
