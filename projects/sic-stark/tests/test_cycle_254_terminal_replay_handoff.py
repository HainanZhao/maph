from proof.verify_cycle_254_terminal_replay_handoff import audit


def test_terminal_replay_freezes_project_without_universal_nogo():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["status"] == "C_FROZEN"
    assert not result["dimension_six_TCC_proved"]
    assert result["independent_replay"]["implementation_independent_of_C253_verifier"]
    assert result["independent_replay"]["all_eight_reproduced_at_both_embeddings"]
    assert result["transition_inventory"]["record_count"] == 12
    assert result["transition_inventory"]["survivor_count"] == 0
    assert result["terminal_outcome"]["project_stopped"]
    assert not result["terminal_outcome"]["new_cycle_authorized"]
