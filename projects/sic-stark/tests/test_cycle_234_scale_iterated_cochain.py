#!/usr/bin/env python3
"""Regression checks for Cycle 234 source-scale product obstruction."""
from proof.verify_cycle_234_scale_iterated_cochain import audit


def test_source_scaling_preserves_all_four_residual_factors() -> None:
    result = audit()
    rows = result["source_scale"]["factor_rows"]
    assert len(rows) == 4
    assert all(row["ordinary_gamma_scale_invariant"] for row in rows)
    assert result["normalized_residual"]["laurent_coefficient_homogeneity"] == "c_A(lambda*omega)=lambda^4*c_A(omega)"


def test_repeated_factor_fails_nonzero_infinite_product_condition() -> None:
    result = audit()
    product = result["scale_iterated_product"]
    assert product["exact_partial_product"] == "P_N(x)=Rhat_A(x)^N"
    assert product["nonzero_meromorphic_product_converges_generically"] is False
    assert result["full_divisor_reflection_normalization"]["status"] == "UNAVAILABLE_AFTER_CONVERGENCE_FAILURE"
