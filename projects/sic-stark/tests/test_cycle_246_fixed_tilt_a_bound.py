from proof.verify_cycle_246_fixed_tilt_a_bound import audit


def test_fixed_tilt_a_recurrence_has_the_frozen_uniform_bound():
    result = audit()
    assert result["bound"]["epistemic_status"] == "PROVED"
    assert result["bound"]["C"] == "2^40000000"
    assert result["bound"]["d"] == 0
    assert result["bound"]["all_N"]
    assert not result["bound"]["numerical_sampling_used"]
