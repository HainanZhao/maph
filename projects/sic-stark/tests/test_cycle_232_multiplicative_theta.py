#!/usr/bin/env python3
"""Regression checks for Cycle 232's frozen theta candidate."""
from proof.verify_cycle_232_multiplicative_theta import audit


def test_single_theta_candidate_solves_only_principal_multiplier() -> None:
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["principal_multiplier"]["equation"] == "H(576*mu)/H(mu)=mu^(-4)"
    assert result["principal_multiplier"]["monomial_q_power"] == -4
    assert result["principal_multiplier"]["theta_q_power"] == 4
    assert result["principal_multiplier"]["tier_1"] == "PROVED"


def test_full_residual_hyperplanes_prevent_promotion() -> None:
    result = audit()
    rows = result["full_residual_divisor"]["rows"]
    assert [row["start"] for row in rows] == ["A", "C"]
    assert all(row["uncancelled"] for row in rows)
    assert all(not row["present_in_mu_to_minus_four"] for row in rows)
    assert result["tier_2"]["absorbs_both_full_residuals"] is False
    assert result["reflection_and_normalization"]["status"] == "UNAVAILABLE_AFTER_TIER_2_FAILURE"
