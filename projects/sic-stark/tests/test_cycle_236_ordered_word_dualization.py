#!/usr/bin/env python3
from proof.verify_cycle_236_ordered_word_dualization import audit

def test_all_ordered_loop_words_fail_factor_level_reflection_closure() -> None:
    result=audit(); rows=result["dualization"]["rows"]
    assert [row["ordered_loop_word"] for row in rows]==["a c","c a"]
    assert all(not row["dualization_is_endofunctor"] for row in rows)
    assert all(len(row["missing_reflection_partner_positions"])==4 for row in rows)
    assert result["dualization"]["source_reflection_endofunctor_exists"] is False
