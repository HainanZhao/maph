# C82 / B082 preregistration: LEM inverse modular realization

<!-- research-freeze-v1
{"schema":"research-preregistration-freeze-v1","cycle":82,"parameters":{"question":{"kind":"expression","value":"Can the specified 15-element chain substitution of the recovered 9-element LEM witness realize a full LEM 4-cycle absent from the incomparable-only digraph?","rationale":"Tests one fixed realization family rather than a further abstract inequality."},"family_rule":{"kind":"expression","value":"Base predecessor masks (0,0,2,0,1,8,25,7,42); replace base vertices 0,3,1 by ordered three-chains, retain the other six singleton blocks, and impose every blockwise base relation. Use the 15-bit ideal-prefix/suffix recurrence for pair counts.","rationale":"Fixes all modules, relations, and recurrence before execution."},"independent_replay_rule":{"kind":"expression","value":"Enumerate every linear extension by recursive minimal-element deletion, form exact pair counts, and compute incomparability from the transitive closure of the predecessor relation.","rationale":"Separates the certificate replay from the ideal dynamic-programming route and pins the clone-chain comparability convention."},"claim_boundary":{"kind":"expression","value":"A family hit is only a counterexample candidate until independently replayed. Family infeasibility is not a theorem about all posets.","rationale":"Bounds the inverse construction."}},"resource_caps":{"minimum_vertices":{"kind":"integer","value":15,"rationale":"Avoids the published exhaustive agreement through order 14."},"worker_processes":{"kind":"integer","value":3,"rationale":"Reserve one of four CPUs."},"aggregate_wall_seconds":{"kind":"integer","value":900,"rationale":"First exact family gate."},"aggregate_peak_memory_mib":{"kind":"integer","value":512,"rationale":"Exact ideal-state calculations only."},"aggregate_temporary_disk_bytes":{"kind":"integer","value":10485760,"rationale":"Small certificates only."},"rng_seed":{"kind":"not_applicable","justification":"The first gate is deterministic exact algebra.","rationale":"No random search is authorized."}},"formula_families":["uniform linear-extension generating functions","15-element chain substitution","exact pair-margin signs","direct linear-extension enumeration"],"selection_rule":["Construct exactly the frozen chain substitution.","Accept only exact integer margin comparisons.","A valid mismatch requires a full 4-cycle and no restricted 4-cycle."],"failure_rule":["Do not widen the family after a hit or no-hit.","An infeasibility certificate ends this family only.","No census or sampling is authorized in this cycle."],"pre_execution":{"timestamp_utc":"2026-08-05T20:25:00Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY repository; C82 follows sealed C81 method boundary.","filesystem_observation_bytes":{"available":159808917504,"reserved":5368709120,"chosen_temporary_cap":10485760,"mount":"/"}},"input_paths":["discovery/cycle81_lem_source_screen.md","discovery/cycle82_inverse_realization_idea_selection.md","artifacts/cycle-81-b081-lem-method-boundary-v1.json","proof/check_cycle82_direct_enumeration.py","../../tools/preregistration_check.py"]}
-->

No executable discovery begins until the marked modular family is fixed here.
The executable to be frozen for this family is
`proof/check_cycle82_chain_substitution.py`.
Its independent replay is `proof/check_cycle82_direct_enumeration.py`; it
enumerates extensions rather than using the ideal dynamic program, and applies
transitive closure before calling two vertices incomparable.

## Frozen first family

Use the recovered 9-element witness with predecessor masks
`(0,0,2,0,1,8,25,7,42)`. Replace each member of its directed triangle
`0 -> 3 -> 1 -> 0` by a three-element chain, leave the other six vertices
singletons, and order whole blocks whenever their base vertices are ordered.
This is a 15-element lexicographic chain substitution.  The exact recurrence
is the ordinary order-ideal prefix recurrence on its 15-bit predecessor masks;
the pair count for \(a\prec b\) is the sum of prefix-count times suffix-count
over transitions that add \(b\) after \(a\).  Test the full and restricted
4-cycle spectra without selecting marked clone levels after seeing margins.
