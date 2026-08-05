# Cycle 19 / B019 preregistration: first-seven-coordinate symbolic antichains

## Decision question and idea selection

Can an exact meet-in-the-middle antichain of time-coverage masks close all 76
Cycle-18 survivor leaves while merging the first-seven-coordinate branches by
a proved dominance rule?

The primary proposed maximal coverage antichains, a fractional-solution-guided
case grammar, and a direct CRT equivalence test.  Darwin independently proposed
a first-seven-coordinate symbolic split guided by fractional integrality-gap
witnesses, with exact Hall/DRAT leaves and CRT only after an interface test.
We questioned whether LP guidance was needed: it could leak numerical choices
without strengthening soundness.  The selected engine instead branches over
every allowed digit and merges only by exact set inclusion.  We also questioned
whether this is merely full residual SAT solving; it is a distinct proof state
whose invariant is the maximal union antichain and whose certificate is checked
without a SAT solver.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":19,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: exact maximal coverage antichains, fractional-guided symbolic cases, or CRT. Companion: first-seven symbolic cases with exact Hall/DRAT closure, then CRT after an interface test. Choose the antichain meet-in-the-middle because it exhausts every symbolic branch while using only a proved dominance merge and retains the full bad-time interface.","rationale":"Both agents proposed symbolic branching; floating LP structure is rejected as unnecessary for branch selection."},
    "target_rows":{"kind":"expression","value":"Exactly the 76 Cycle-18 rows with status UNRESOLVED, ordered by base 4 then base 3 and leaf ordinal. Verify exact equality with the frozen Cycle-18 table and membership in the Cycle-17 NO_LP_DEFICIT boundary before execution.","rationale":"No target reselection."},
    "coverage_masks":{"kind":"expression","value":"For each target base/leaf, reconstruct allowed digits from the canonical mod-2/mod-7 conditions. From the exact target Cycle-11 CNF, use the 2786 source coverage clauses indexed 1197 through 3982: B(i,d) contains time offset t exactly when x(i,d) occurs in clause 1197+t. Represent all 2786 times; duplicate clauses remain distinct time bits.","rationale":"Preserves the exact denominator-time interface."},
    "split":{"kind":"expression","value":"Left coordinates are exactly 0..6 in increasing order; right coordinates are exactly 7..12 in increasing order. Begin each side with the empty mask. At each coordinate union every current mask with every allowed digit mask, deduplicate equal masks, then retain exactly the inclusion-maximal masks.","rationale":"First-seven split is frozen and every branch is represented or exactly dominated."},
    "dominance":{"kind":"expression","value":"A generated mask A may be discarded only if a retained mask A' satisfies A subseteq A'. Sort each retained frontier by decreasing popcount then lexicographic unsigned 64-bit word tuple. Store every layer count and SHA-256 plus both final frontier files. The independent checker reconstructs every layer and requires byte equality.","rationale":"Makes the semantic merge exact and replayable."},
    "closure":{"kind":"expression","value":"After both final antichains are complete, for each left mask A test whether any right mask D contains the complement of A. Use an exact subset query and independently replay it. CERTIFIED_NO_COVER requires zero matching pairs. A matching pair is a surviving full-cover candidate and is stored with its digit witnesses if recoverable; any incomplete query is CAP.","rationale":"Meet-in-the-middle equivalence is exact."},
    "selection":{"kind":"expression","value":"Process all 76 rows on CPUs 0-2. Within a leaf build left then right layers and query masks in frozen frontier order. Retain every result. A base closes under the combined Cycle-17/18/19 family only when every one of its remaining target rows is CERTIFIED_NO_COVER.","rationale":"No post-result leaf, split, or frontier choice."},
    "advance_condition":{"kind":"expression","value":"Complete checked no-cover certificates for all remaining rows of base 4 or base 3 complete that base's 6084-leaf canonical tree under a reusable symbolic coverage proof. Partial closure is a named finite result only. A full-cover candidate surviving direct CNF and gcd checks is a headline falsifier.","rationale":"Requires a complete new symbolic closure or a genuine contrary witness."},
    "falsifier":{"kind":"expression","value":"A target mismatch, allowed-digit or coverage-bit error, discarded mask without a retained superset, frontier byte mismatch, missed complement containment, or directly checked full cover in a claimed no-cover leaf invalidates the affected result.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Certificates concern only the 76 named leaves and the two frozen bases. Even complete closure of either base does not prove all sample bases, F_1 emptiness, J emptiness, or LRC(13). A cap is an implementation outcome, not evidence against antichain closure or CRT.","rationale":"Finite symbolic scope only."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "target_rows":{"kind":"integer","value":76,"rationale":"Exactly the Cycle-18 unresolved boundary."},
    "left_coordinates":{"kind":"integer","value":7,"rationale":"Coordinates 0 through 6."},
    "right_coordinates":{"kind":"integer","value":6,"rationale":"Coordinates 7 through 12."},
    "time_bits":{"kind":"integer","value":2786,"rationale":"Every denominator time for q=199*14."},
    "frontier_states_per_side":{"kind":"integer","value":2000000,"rationale":"Hard cap after each exact maximalization."},
    "generated_children_per_leaf":{"kind":"integer","value":50000000,"rationale":"Hard cap across both side constructions."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"All target frontiers, exact queries, independent audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three compact bitset workers plus checker."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Targets, coordinates, digits, dominance, sorting, queries, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical gcd-witness leaves","exact denominator-time coverage masks","layerwise maximal union antichains","first-seven meet-in-the-middle split","exact complement-containment queries"],
  "selection_rule":["Verify the exact 76-row boundary.","Enumerate every allowed digit on both frozen coordinate sides.","Merge only equal or inclusion-dominated coverage masks.","Preserve and hash every layer frontier.","Promote only complete independently replayed no-cover queries.","Claim a base tree complete only when every residual target closes."],
  "failure_rule":["Any target or encoding mismatch halts execution.","A state/child/wall/memory/disk cap retains the leaf as CAP.","A full-cover pair is preserved and directly checked before classification.","Partial frontiers and capped rows support no no-cover claim."],
  "pre_execution":{"timestamp_utc":"2026-08-03T21:58:35Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 18 is sealed before this distinct symbolic-antichain engine.","filesystem_observation_bytes":{"size":206900281344,"used":41185554432,"available":165697949696,"reserved":5368709120,"maximum_temporary_cap":160329240576,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-18-b018-lrc-pair-choice-v1.json","discovery/out/cycle18-pair-choice/results.tsv","discovery/out/cycle17-time-deficit/lp-results.tsv","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_19_symbolic_antichain_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a target/encoding failure or aggregate cap.  After the complete frozen
run, ask Darwin to review the evidence, co-propose next ideas, and advise
whether Cycle 19 continues, seals, or yields to an exact CRT interface test.
