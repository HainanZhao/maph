#!/usr/bin/env python3
"""Regression checks for Cycle 235 loop-holonomy extension."""
from proof.verify_cycle_235_meromorphic_loop_holonomy import audit


def test_two_object_central_extension_is_associative() -> None:
    result = audit()
    rows = result["central_extension"]["rows"]
    assert len(rows) == 2
    assert all(row["associative"] for row in rows)
    assert result["central_extension"]["A_C_intertwining"] is True


def test_extension_does_not_invent_reflection() -> None:
    result = audit()
    assert result["reflection"]["source_reflection_compatible"] is False
    assert result["reflection"]["status"] == "CONTAINED_BY_C228_PARTNER_FAILURE"
