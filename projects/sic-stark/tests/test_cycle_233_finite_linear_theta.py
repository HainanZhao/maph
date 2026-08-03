#!/usr/bin/env python3
"""Regression checks for Cycle 233's finite linear-theta obstruction."""
from proof.verify_cycle_233_finite_linear_theta import audit


def test_all_four_zero_lattices_miss_the_full_a_pole_family() -> None:
    result = audit()
    rows = result["residual_family"]["zero_checks"]
    assert len(rows) == 4
    assert all(not row["cancels_every_family_member"] for row in rows)
    assert rows[1]["zero_lattice_r"] == "-24-115*N"
    assert rows[2]["zero_lattice_s"] == "-5-24*N"


def test_infinite_direction_family_excludes_every_finite_product() -> None:
    result = audit()
    invariant = result["direction_invariant"]
    assert invariant["residual_directions_pairwise_distinct"] is True
    assert invariant["finite_theta_product_directions"] == "finite"
    assert result["completion"]["finite_linear_theta_completion_exists"] is False
    assert result["reflection_and_normalization"]["status"] == "UNAVAILABLE_AFTER_DIVISOR_OBSTRUCTION"
