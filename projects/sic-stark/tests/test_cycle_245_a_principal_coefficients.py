from proof.verify_cycle_245_a_principal_coefficients import audit


def test_a_coefficient_recurrence_is_nonzero_and_embedding_covariant():
    result = audit()
    assert result["recurrence"]["exact_recurrence_family_derived"]
    assert result["recurrence"]["all_multiplier_factors_nonzero"]
    assert result["galois"]["epistemic_status"] == "PROVED"
    assert not result["growth"]["tempered_bound_proved"]
