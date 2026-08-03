#!/usr/bin/env python3
"""Ordered residual-word reflection closure audit for Cycle 236/B073."""
from __future__ import annotations
import json

try:
    from .verify_cycle_228_f3_square_residual_block import audit as residual_audit
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import audit as residual_audit


def audit() -> dict[str, object]:
    source = residual_audit()
    rows = source["reflection_audit"]
    assert len(rows) == 8
    per_block = {"A": [], "C": []}
    for row in rows:
        per_block[row["start"]].append(row)
        assert row["reflection_match_available"] is False
    result_rows = []
    for start, word in (("A", "a c"), ("C", "c a")):
        partner_positions = [row["position"] for row in per_block[start] if not row["reflection_match_available"]]
        result_rows.append({"start": start, "ordered_loop_word": word, "dual_word_order": "reversed", "missing_reflection_partner_positions": partner_positions, "dualization_is_endofunctor": False})
    assert all(len(row["missing_reflection_partner_positions"]) == 4 for row in result_rows)
    return {"epistemic_status":"PROVED","ordered_word_category":{"objects":["A","C"],"edge_words":{"A_to_C":"a","C_to_A":"c"},"loop_words":{"A":"a c","C":"c a"},"composition":"concatenation without commutation"},"dualization":{"rule":"reverse order and replace every factor by its S--S (32) reflection partner with Bernoulli factor","rows":result_rows,"source_reflection_endofunctor_exists":False,"status":"FALSIFIED_BY_FACTOR_PARTNER_ABSENCE"},"conclusion":"Neither A nor C ordered F3^2 residual word is closed under source reflection reversal/inversion, because every required factor partner is absent from the frozen word category. This excludes only the frozen ordered-word dualization and proves no Gamma_M interface, target representation, AFK, fusion, Stark, or TCC result."}


if __name__ == "__main__": print(json.dumps(audit(),indent=2,sort_keys=True))
