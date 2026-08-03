from proof.verify_cycle_239_rarefied_beta_embedding import audit


def test_rarefied_beta_theorem_has_no_direct_c228_embedding():
    result = audit()
    assert result["status"] == "FALSIFIED_DIRECT_RAREFIED_BETA_KERNEL_EMBEDDING"
    assert len(result["blocks"]) == 2
    for row in result["blocks"]:
        assert row["direct_embedding"] is False
        assert not any(condition["satisfied"] for condition in row["conditions"].values())
