from proof.verify_cycle_251_residue_dual_cross_sign import audit


def test_canonical_residue_dual_exits_the_fixed_source_chamber():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "CANONICAL_RESIDUE_DUAL_CROSS_SIGN_FALSIFIED"
    orientation = result["orientation_test"]
    assert orientation["canonical_orientation_maps_outside_source_product_domain"]
    assert not orientation["degree_0_to_3_contragredient_coefficients_compared"]
    assert len(orientation["rows"]) == 8
    assert all(row["R_alpha_equals_minus_target_alpha"] and row["R_beta_equals_target_beta"] for row in orientation["rows"])
