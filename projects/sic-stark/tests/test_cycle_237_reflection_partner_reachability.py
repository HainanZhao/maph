#!/usr/bin/env python3
from proof.verify_cycle_237_reflection_partner_reachability import audit
def test_no_positive_source_edge_reaches_a_reflection_partner():
 r=audit();assert len(r["positive_edges"])==4;assert len(r["rows"])==32;assert r["source_reachable_partner_count"]==0;assert all(not x["argument_match"] for x in r["rows"]);assert r["formula_level_orientation_invariant"]["arbitrary_finite_positive_k_path_reaches_partner"] is False
