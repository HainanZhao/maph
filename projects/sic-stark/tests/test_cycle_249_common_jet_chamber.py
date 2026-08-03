from proof.verify_cycle_249_common_jet_chamber import audit


def test_all_c228_factors_share_the_fixed_upper_q_product_chamber():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "COMMON_FIXED_UPPER_CHAMBER_FOR_C228_JETS"
    assert result["factor_count"] == 8
    assert all(row["period_determinant"] in {"1/24", "24"} for row in result["factors"])
    assert all(row["analytic_jet"]["absolute_convergence"] for row in result["factors"])
