from proof.verify_cycle_252_reciprocal_negative_alpha import audit


def test_reciprocal_rule_stops_at_source_continuation_gate():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "RECIPROCAL_BASE_RULE_FAILS_SOURCE_CONTINUATION_GATE"
    algebra = result["algebraic_audit"]
    assert algebra["shifts"]["both_expected_negative_alpha_shifts_pass"]
    assert algebra["double_sign"]["returns_source_product_formula"]
    continuation = result["continuation_scope_audit"]
    assert continuation["first_failed_prerequisite"] == 4
    assert not continuation["path_independent_meromorphic_continuation_proved"]
    assert not continuation["jets_compared"]
    assert not continuation["eight_reflected_factors_compared"]
