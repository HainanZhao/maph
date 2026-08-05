# Cycle 10 / B010 preregistration: gcd-admissible lift patterns

## Decision question

For `(13,199,14)`, can exact lifted-mask cover search that conditions on the
actual gcd properness counts find an improper lift or certify a pattern-class
exclusion more effectively than Cycle 8's unstructured CSP?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":10,
  "parameters":{
    "idea_selection":{"kind":"text","value":"The primary agent proposed gcd-pattern cover search; the companion independently ranked it above CRT, CDCL, and stopping. Question the framing: Cycle 8 already counted divisibility, so a mere relabel is insufficient. The new engine must use pattern-conditioned feasible-mask bounds or find an explicit admissible cover. A p199 admissible cover falsifies this branch; CAP does not.","rationale":"Records joint idea selection and rejects a cosmetic successor."},
    "pattern_interface":{"kind":"expression","value":"Each v_i+199d is classified modulo 14 as divisible by 2 only, 7 only, 14, or coprime. A lift is gcd-admissible exactly when N_2<12 and N_7<12. Branch by uncovered lifted time while maintaining this pattern state; prune only with a bound proved for every remaining pattern choice.","rationale":"This targets the Definition-2.1 condition exposed by Cycle 9."},
    "controls":{"kind":"expression","value":"Reproduce H11: all raw l=1-improper bases have mask-cover lifts but no gcd-admissible improper lift. Reproduce p47: all 53 canonical base orbits have no gcd-admissible c=7 lift. Then use exactly the frozen 100 completed p199 Cycle-8 strata.","rationale":"Controls distinguish the new gcd-aware state from the mask-only dual."},
    "advance_condition":{"kind":"expression","value":"A directly rechecked p199 gcd-admissible cover is an improper-lift witness. A complete UNSAT is a finite F_1 exclusion. CAP retains. No frontier follows without material review.","rationale":"Separates witnessed, certified, and bounded outcomes."},
    "claim_boundary":{"kind":"expression","value":"This is a first-lift fixed-sample engine only; it proves no J-empty, LRC(13), prime-product, CRT-equivalence, or universal gcd-forcing statement.","rationale":"A sample cannot close the conjecture."}
  },
  "resource_caps":{
    "worker_threads":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2."},
    "h11_raw_bases":{"kind":"integer","value":1000,"rationale":"Complete raw control."},
    "p47_base_orbits":{"kind":"integer","value":53,"rationale":"Sealed canonical control."},
    "p199_sample_orbits":{"kind":"integer","value":100,"rationale":"Frozen Cycle-8 strata exactly."},
    "nodes_per_p199_orbit":{"kind":"integer","value":2000000,"rationale":"A deterministic cap returns CAP/retain; this is a distinct frozen engine resource."},
    "wall_seconds":{"kind":"integer","value":1200,"rationale":"Aggregate bounded run."},
    "peak_memory_mib":{"kind":"integer","value":2048,"rationale":"No broad frontier materialization."},
    "temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"Below free-space minus the 5-GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"All branching is deterministic.","rationale":"No randomized support."}
  },
  "formula_families":["Definition-2.1 gcd properness","four mod-14 digit patterns","gcd-admissible multiple-choice cover","conditional pattern-capacity bounds"],
  "selection_rule":["Write the pattern-state soundness argument before executable work.","Pass H11 and p47 controls before p199.","SAT is directly recomputed; CAP retains; UNSAT is replayed before promotion.","Do not use CDCL or CRT in this cycle."],
  "failure_rule":["Any control mismatch halts the pattern claim.","A capacity bound may prune only when proved for every remaining pattern choice.","No CAP, failed bound, or lack of SAT authorizes saturation."],
  "pre_execution":{"timestamp_utc":"2026-08-03T17:07:12Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 9 is sealed before this distinct gcd-aware engine.","filesystem_observation_bytes":{"size":206900281344,"used":28233895936,"available":178649608192,"reserved":5368709120,"maximum_temporary_cap":173280899072,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-9-b009-lrc-weighted-dual-v1.json","artifacts/cycle-8-b008-lrc-fused-lift-v1.json","discovery/out/cycle8-p199-strata.txt","proof/cycle_10_gcd_pattern_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a control mismatch or after the fixed sample gate; a material review,
not an all-CAP sample, chooses any later engine change.
