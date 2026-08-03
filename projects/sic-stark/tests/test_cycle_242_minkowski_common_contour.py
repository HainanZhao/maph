from proof.verify_cycle_242_minkowski_common_contour import audit


def test_common_affine_cone_separator_is_exactly_obstructed():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert not result["common_affine_linear_cone_separator_exists"]
    assert result["combined_interval"] == {"strict_lower": "5", "strict_upper": "1/115"}
    assert all(not row["common_affine_linear_cone_separator"] for row in result["embeddings"])
