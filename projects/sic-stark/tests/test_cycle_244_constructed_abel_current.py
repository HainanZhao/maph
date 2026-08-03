from proof.verify_cycle_244_constructed_abel_current import audit


def test_constructed_current_is_locally_finite_but_not_intrinsically_normalized():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["boundary"]["rho_to_one_distributional_boundary_exists"]
    assert not result["normalization_ambiguity"]["intrinsic_regulator_normalization_available"]
    assert not result["source_authorization"]
