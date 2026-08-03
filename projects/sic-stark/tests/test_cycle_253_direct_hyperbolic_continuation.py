from proof.verify_cycle_253_direct_hyperbolic_continuation import audit


def test_direct_continuation_exists_but_misses_every_target():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "DIRECT_CONTINUATION_EXISTS_BUT_UNCORRECTED_TARGET_MAP_FALSIFIED"
    assert result["theorem_audit"]["path"]["path_independent"]
    assert result["theorem_audit"]["negative_alpha_endpoint"]["now_source_authorized_by_theorem"]
    target = result["target_test"]
    assert target["all_eight_continuations_exist_at_both_embeddings"]
    assert target["all_eight_target_maps_fail_by_nonconstant_shift_quotient"]
    assert not target["degree_0_to_3_jets_compared"]
    assert len(target["rows"]) == 8
