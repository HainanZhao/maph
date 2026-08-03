from proof.verify_cycle_250_graded_f3_jet_representation import audit


def test_source_specific_graded_positive_f3_representation():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "GRADED_POSITIVE_F3_JET_REPRESENTATION_CONSTRUCTED"
    assert result["representation"]["positive_A_C_edges_intertwined"]
    assert not result["representation"]["negative_k_or_cross_sign_law_derived"]
    for path in result["paths"]:
        assert path["derived_factor_specs_equal_C228_in_order"]
        assert path["two_edge_normalization"] == "24^(-2)"
        assert path["jet_identity_holds_degree_0_to_3"]
        assert path["matrix_identity_holds"]
