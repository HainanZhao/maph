#!/usr/bin/env python3
"""Regression checks for the Cycle 231 frozen cover-cochain algebra."""
from proof.verify_cycle_231_cover_cochain import audit


def test_forced_quadratic_coefficient_and_failure_of_descent() -> None:
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["solution_family"]["A"] == "-2/log(576)"
    assert result["coefficient_comparison"]["a_times_log_576"] == "-2"
    assert result["coefficient_comparison"]["exact_scaling_w_coefficient"] == "-4"
    assert result["coefficient_comparison"]["exact_deck_w_coefficient_in_units_pi_i_over_log_576"] == "-8"
    assert result["coefficient_comparison"]["deck_w_coefficient"] == "4*pi*i*A = -8*pi*i/log(576)"
    assert result["descent"]["deck_multiplier_is_constant"] is False
    assert result["descent"]["descends_single_valuedly"] is False


def test_reflection_is_not_replaced_by_an_unfrozen_lift() -> None:
    result = audit()
    assert result["reflection"]["source_reflection_test"] == "UNAVAILABLE_AFTER_DESCENT_FAILURE"
