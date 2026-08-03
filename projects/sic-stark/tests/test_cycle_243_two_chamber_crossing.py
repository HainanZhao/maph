from proof.verify_cycle_243_two_chamber_crossing import audit


def test_two_chamber_connection_has_an_infinite_uncancelled_crossing_family():
    result = audit()
    assert result["epistemic_status"] == "PROVED"
    assert result["chambers"]["every_continuous_path_crosses_wall"]
    assert result["crossing_family"]["side_changes_at_wall"]
    assert result["uncancelled_crossings"]["cardinality"] == "infinite"
    assert not result["finite_residue_ledger_available"]
