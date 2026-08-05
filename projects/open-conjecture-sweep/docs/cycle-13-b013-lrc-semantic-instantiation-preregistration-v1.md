# Cycle 13 / B013 preregistration: typed semantic core instantiation

## Decision question and idea selection

Can the certified Cycle-12 subcore recur after choices are identified by their
divisibility and bad-time coverage roles, rather than by equal residue labels,
while every accepted instance still expands to exact clause containment?

The primary independently proposed colored clause-incidence anti-unification,
resolution-proof motifs, and a gcd-conditioned certificate decision tree.
Darwin independently proposed typed time-mask/coverage roles, followed by a
gcd-conditioned tree or CRT bridge.  We questioned whether an abstract motif
could prove anything without a sound inverse map.  We therefore select the
smallest strict generalization of Cycle 12: coordinate permutations plus
within-coordinate choice bijections preserving the exact 2/7 divisor type,
with bad-time roles checked by literal-level target clauses.  Proof-trace
motifs are deferred because their semantic inverse is not yet defined; the
decision tree and CRT remain fallbacks.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":13,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: colored clause-incidence anti-unification, resolution motifs, or gcd-conditioned certificate tree. Companion: typed time-mask/coverage roles, then gcd-conditioned tree or CRT. Choose a typed substitution with an exact inverse because it strictly enlarges Cycle 12 while keeping proof transport literal and falsifiable.","rationale":"Both agents proposed ideas independently and challenged the abstraction-to-proof bridge."},
    "source_template":{"kind":"expression","value":"Use only the sealed Cycle-12 row-76 293-clause deletion-minimal certified UNSAT subcore; do not reselect a source after target results.","rationale":"Avoids post-result core selection and starts from the smallest certified available core."},
    "semantic_substitution":{"kind":"expression","value":"Map coordinates by a permutation pi. For each coordinate independently map its 14 x(i,s) choices by a bijection sigma_i preserving the two-bit color (2|s,7|s). Map y(r,i) to y(r,pi(i)) with r fixed; preserve signs and clause multiplicities. Coverage roles are induced by exact target time clauses, not assumed from colors.","rationale":"This is a precise strict generalization of residue-preserving Cycle-12 maps."},
    "exact_checker":{"kind":"expression","value":"A MATCH must output pi and all sigma_i, prove every map is bijective and type preserving, map every source literal, and verify full mapped-clause multiset containment in the independently rebuilt target CNF. Search signatures and refinement never certify a match.","rationale":"An exact image transports certified UNSAT without trusting heuristics."},
    "controls":{"kind":"expression","value":"First accept identity self-instantiation. Then accept 14 deterministically constructed positive images using one fixed nonidentity permutation within each divisor-color class and independently verify containment. Compare the optimized search with an exhaustive typed-substitution oracle on frozen k=2 synthetic instances. Any control failure halts targets.","rationale":"Exercises identity, generalized positive, and search-completeness paths before frontier use."},
    "targets":{"kind":"expression","value":"Use the same frozen Cycle-12 held-out rows: sample offsets 8..9 within each of 10 strata as 20 validation targets; external census indices stratum*4748938//10 + offsets 10..19 as 100 targets. Evaluate validation first and external only after controls.","rationale":"Tests whether the enlarged family changes the prior exact no-match boundary without selecting targets."},
    "advance_condition":{"kind":"expression","value":"At least one target receives an exact instantiation certificate passing independent literal-level containment. Such a match proves that named target CNF UNSAT. A complete audited NO_MATCH may close only this substitution family; timeout, cap, heuristic similarity, or incomplete search makes no mathematical claim.","rationale":"Requires proof-bearing transfer, not recurrence statistics."},
    "falsifier":{"kind":"expression","value":"A non-bijection, divisor-color violation, absent mapped clause, source proof failure, independent CNF mismatch, SAT model for a claimed target, or optimized/exhaustive control disagreement invalidates the affected claim and halts promotion.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Only exactly certified target first-lift fibers or an audited no-go for this frozen typed-substitution family may be claimed. No other MUS, proof trace, general semantic interpolant, F_1 emptiness, J emptiness, or LRC statement follows.","rationale":"Prevents extrapolation beyond the selected core and map family."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "source_templates":{"kind":"integer","value":1,"rationale":"Frozen row-76 certified subcore only."},
    "validation_targets":{"kind":"integer","value":20,"rationale":"Frozen Cycle-12 validation set."},
    "external_targets":{"kind":"integer","value":100,"rationale":"Frozen Cycle-12 disjoint external set."},
    "synthetic_positive_controls":{"kind":"integer","value":14,"rationale":"Deterministic typed substitutions exercise nonidentity maps."},
    "aggregate_search_nodes":{"kind":"integer","value":100000000,"rationale":"Deterministic global node cap; capped targets remain unknown."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Includes implementation controls, validation, external checks, and audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three optimized search workers and exact checker."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below observed free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"All substitutions, targets, traversal, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["certified UNSAT subcore","typed coordinate-block substitution","2/7 divisor-color choice roles","bad-time clause incidence","exact mapped-clause multiset containment"],
  "selection_rule":["Pass identity, 14 generalized-positive, and exhaustive toy controls before target search.","Use only the frozen row-76 source subcore.","Evaluate all 20 validation targets before the 100 external targets.","Accept only full literal-level containment certificates.","Use at most CPUs 0-2 and stop at the aggregate caps."],
  "failure_rule":["Any control disagreement or false containment halts the branch.","CAP and timeout retain the target and prove nothing.","No match cannot be promoted to a family no-go unless the search-completeness audit establishes uncapped exhaustion.","Failure of this family triggers material review of the gcd-conditioned decision tree and exact CRT bridge, not automatic saturation."],
  "pre_execution":{"timestamp_utc":"2026-08-03T19:35:06Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 12 is sealed before this distinct semantic substitution family.","filesystem_observation_bytes":{"size":206900281344,"used":34061713408,"available":172821790720,"reserved":5368709120,"maximum_temporary_cap":167453081600,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-12-b012-lrc-core-template-v1.json","discovery/out/cycle12-core-template/mus/076.cnf","discovery/out/cycle12-core-template/mus/076.drat","discovery/out/cycle8-p199-strata.txt","discovery/out/k13-p199.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_13_semantic_instantiation_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a control failure or aggregate cap.  After the frozen target search,
obtain a material companion review before sealing, changing engines, or
declaring Problem 1 saturated.
