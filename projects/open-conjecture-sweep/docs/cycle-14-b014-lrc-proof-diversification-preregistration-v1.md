# Cycle 14 / B014 preregistration: proof and core diversification

## Decision question and idea selection

Can independently checked proof traces or MUS deletion orders expose a small
certified UNSAT core whose coverage clauses split a 2/7 divisor-color class,
thereby avoiding Cycle 13's exact collapse?

The primary proposed alternate solver configurations, targeted shrinking that
protects a discriminating coverage clause, and resolution-motif extraction.
Darwin independently proposed alternate DRAT/MUS proof generation, with
resolution motifs and CRT as later alternatives.  We questioned whether blind
proof diversity would merely create larger syntactic variants.  The chosen
engine therefore begins with a cheap structural census of the 80 frozen
training cores, chooses only three bases by a frozen discriminating score, and
accepts a diversified core only after proof verification and exact structural
classification.  Long proof generation without the target feature is a
failure, not progress.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":14,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: alternate CaDiCaL traces, protected-clause MUS shrinking, or resolution motifs. Companion: alternate DRAT/MUS generation, then resolution motifs or CRT. Choose a staged structural census plus targeted proof diversification because it tests the precise Cycle-13 collapse mechanism before spending solver time.","rationale":"Both agents proposed engines; the staged rule rejects undirected proof churn."},
    "training_census":{"kind":"expression","value":"Normalize the 80 Cycle-12 training cores (sample offsets 0..7 in each stratum). A positive x-only clause is discriminating iff its residue set in at least one coordinate intersects but does not contain an entire (2|s,7|s) color class. Count such clauses exactly.","rationale":"A discriminating clause is exactly what the Cycle-13 selected core lacked."},
    "base_selection":{"kind":"expression","value":"Rank the 80 training bases by descending discriminating-clause count, then ascending certified-core clause count, core SHA-256, and index. Select the first three; do not inspect alternate proof results before selection.","rationale":"Targets structural signal while freezing ties."},
    "solver_configurations":{"kind":"expression","value":"For each selected Cycle-11 source CNF run pinned CaDiCaL 2.1.3 in exactly three deterministic configurations: default --seed=0; --plain --seed=1; and --elim=false --probe=false --seed=2. Require exit 20 and a pinned drat-trim VERIFIED proof.","rationale":"Produces genuinely different deterministic proof traces with a fixed checker."},
    "core_extractions":{"kind":"expression","value":"For every verified proof run pinned drat-trim core extraction in exactly three modes: default -c, -u -c, and -f -c. Accept only source-clause multiset subsets which receive a fresh CaDiCaL UNSAT proof and drat-trim VERIFIED check.","rationale":"Diversifies both proof production and dependency extraction without weakening certification."},
    "candidate_selection":{"kind":"expression","value":"Among all certified existing and diversified cores for the three selected bases, retain those with at least one discriminating coverage clause. Select by ascending clause count, descending discriminating count, core SHA-256, base index, solver configuration, and extraction mode.","rationale":"Chooses the smallest proof-bearing non-collapsed source before shrinking."},
    "protected_shrink":{"kind":"expression","value":"Protect the lexicographically smallest discriminating clause of the selected candidate. Scan every other clause once in original order; delete it only after fresh CaDiCaL UNSAT plus drat-trim VERIFIED. SAT, timeout, or failed proof retains it. Freshly certify the final core and recheck that the protected clause remains discriminating.","rationale":"Attempts a small usable core without deleting the feature that makes the engine distinct."},
    "role_group_continuation":{"kind":"expression","value":"The single-clause pass returned 2328 CAP and zero deletions. Continue on the same selected core with four deterministic groups in this order: all discriminating positive-x clauses except the protected clause; all color-invariant positive-x clauses; all negative same-coordinate choice-pair clauses; all remaining clauses. For each group, test deletion from the current core with a 25-second CaDiCaL limit; accept only fresh UNSAT plus drat-trim VERIFIED, otherwise retain. Freshly certify the final core.","rationale":"Companion-reviewed continuation tests large mutual redundancy in the same minimization question without post-result group selection."},
    "instantiation_preflight":{"kind":"expression","value":"If the final core has at most 500 clauses, run the Cycle-13 typed substitution checker on the frozen 20 validation targets. A MATCH must pass full literal clause-multiset containment; no external targets are inspected in this cycle.","rationale":"Tests usefulness before a later blind external gate while limiting search cost."},
    "advance_condition":{"kind":"expression","value":"A certified at-most-500-clause core retaining a discriminating coverage clause is a structural advance. An exact validation embedding additionally proves the named target fiber UNSAT. Larger cores, absent discriminating clauses, CAP, or heuristic motifs do not advance.","rationale":"Separates reusable structure from mere trace diversity."},
    "falsifier":{"kind":"expression","value":"Any proof rejection, core clause absent from its source, incorrect clause classification, protected-clause loss, SAT model for a claimed UNSAT core or target, or false mapped containment invalidates the affected result.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Claims concern only the frozen bases, configurations, extracted cores, and validation CNFs. No proof about other traces, all semantic roles, F_1 emptiness, J emptiness, or LRC(13) follows.","rationale":"A bounded proof-diversity experiment is not universal."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "training_cores":{"kind":"integer","value":80,"rationale":"Frozen Cycle-12 training split."},
    "selected_bases":{"kind":"integer","value":3,"rationale":"Only the top three frozen structural signals receive new solves."},
    "solver_configurations_per_base":{"kind":"integer","value":3,"rationale":"Default, plain, and disabled elimination/probing."},
    "core_extraction_modes_per_proof":{"kind":"integer","value":3,"rationale":"Default, unit-first, and forward modes."},
    "protected_deletion_attempts":{"kind":"integer","value":3000,"rationale":"One pass, capped above every current source-core size."},
    "role_group_deletion_attempts":{"kind":"integer","value":4,"rationale":"Exactly four frozen exhaustive role groups."},
    "role_group_wall_seconds":{"kind":"integer","value":120,"rationale":"Fits inside the original 3600-second aggregate cap."},
    "validation_targets":{"kind":"integer","value":20,"rationale":"No external target inspection in this cycle."},
    "solver_seconds_per_instance":{"kind":"integer","value":600,"rationale":"Timeout retains the configuration."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Census, proof generation/checking, extraction, shrinking, and preflight combined."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"At most three solver/checker processes."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"No stochastic sampling; deterministic CaDiCaL seed values 0, 1, and 2 are frozen in solver_configurations.","rationale":"Selection and replay are deterministic."}
  },
  "formula_families":["p199 first-lift CNF","deterministic DRAT proof variants","checked input cores","2/7 color-class coverage split","protected-clause deletion-minimal core","typed exact instantiation"],
  "selection_rule":["Classify all 80 existing training cores before selecting bases.","Select exactly three bases by the frozen structural order.","Verify every proof and extracted core independently.","Select and shrink one candidate by the frozen rules.","After the zero-deletion single-clause outcome, run exactly the four frozen role-group deletions on the same core.","Run validation instantiation only if the final core has at most 500 clauses.","Use only CPUs 0-2."],
  "failure_rule":["Any source, proof, or classification mismatch halts the affected candidate.","Timeout or cap retains the row and proves nothing.","No discriminating small core closes only this proof-diversification family.","Do not inspect external targets or launch a full-census solve in this cycle."],
  "pre_execution":{"timestamp_utc":"2026-08-03T19:45:02Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycles 12 and 13 are sealed before this distinct proof-diversification family.","filesystem_observation_bytes":{"size":206900281344,"used":34062319616,"available":172821184512,"reserved":5368709120,"maximum_temporary_cap":167452475392,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-13-b013-lrc-semantic-collapse-v1.json","artifacts/cycle-12-b012-lrc-core-template-v1.json","artifacts/cycle-12-b012-lrc-core-template-v2.json","artifacts/cycle-11-b011-lrc-certified-sat-v1.json","discovery/out/cycle12-core-template/cores.tsv","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_13_semantic_instantiation_soundness.md","discovery/vendor/cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8.tar.gz","discovery/vendor/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f.tar.gz","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a systemic proof/classification failure or aggregate cap.  After the
protected shrink and optional validation preflight, obtain a material companion
review before sealing, changing engines, or declaring Problem 1 saturated.
