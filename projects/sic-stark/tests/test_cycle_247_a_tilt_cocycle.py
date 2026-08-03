from proof.verify_cycle_247_a_tilt_cocycle import audit


def test_proposed_one_q_tilt_cocycle_is_falsified_before_q_series_test():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "FROZEN_ONE_Q_TILT_COCHAIN_FALSIFIED"
    assert result["q_bases"]["not_equal_for_any_positive_tilt"]
    assert not result["q_series_degree_two_inspected"]
