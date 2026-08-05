# Cycle 11 / B011 preregistration: certified first-lift SAT

## Decision question and idea selection

Can a proof-producing CDCL/PB representation classify the exact first-lift
fibers that defeated the custom DFS engines, while preserving independently
checkable SAT witnesses and UNSAT certificates?

The primary ideas were proof-producing CDCL, a CRT decomposition, custom
learned cores, and stopping Problem 1.  Darwin independently proposed both
proof-producing CDCL and certified PB/MaxSAT, with a small exact CRT prototype
as the principal alternative.  We questioned whether changing solvers merely
hides the same combinatorial difficulty; the discriminating feature is learned
clause reuse plus proof output, not a speed claim.  CDCL is selected because a
SAT model is directly falsifiable and a DRAT proof is independently checkable.
CRT is rejected for this cycle because no exact cross-factor equivalence has
yet been proved; custom learned cores have weaker certification; stopping now
would discard a materially different exact engine.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":11,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: proof-producing CDCL, CRT decomposition, custom learned cores, or stop. Companion: proof-producing CDCL, certified PB/MaxSAT, and small exact CRT preflight. Choose CDCL because it adds learned clauses and independently checkable proof output. Reject CRT until exact equivalence, custom cores for weak certification, and stopping before this distinct engine.","rationale":"Records independent proposals and adversarial comparison."},
    "solver":{"kind":"text","value":"CaDiCaL 2.1.3, official source https://github.com/arminbiere/cadical.git tag rel-2.1.3 commit f13d74439a5b5c963ac5b02d05ce93a8098018b8; command cadical DIMACS PROOF with default deterministic configuration.","rationale":"Pinned proof-producing CDCL implementation."},
    "proof_checker":{"kind":"text","value":"drat-trim official source https://github.com/marijnheule/drat-trim.git tag v05.22.2023 commit 2e5e29cb0019d5cfd547d4208dca1b3ec290349f; accept only exit zero plus VERIFIED output.","rationale":"Independent DRAT validation."},
    "encoding":{"kind":"expression","value":"Variables x(i,d) select exactly one digit per coordinate. One cover clause per a in Z/(pc) contains precisely choices bad at a. Auxiliary y(r,i) iff selected speed is divisible by prime r|c. For each r and each (k-1)-coordinate subset, a clause of negated y enforces at most k-2 divisible coordinates.","rationale":"CNF is equivalent to an improper first lift by the written soundness argument."},
    "controls":{"kind":"expression","value":"All 240 raw l=1-improper H11 bases must be certified UNSAT; all 53 canonical p47 base orbits must be certified UNSAT. The independent direct predicate and every CNF clause are checked for any SAT model. Only after both controls pass, classify exactly the frozen 100 Cycle-8 p199 strata.","rationale":"Complete controls precede frontier use."},
    "advance_condition":{"kind":"expression","value":"A directly rechecked p199 SAT model proves that sampled base has an improper first lift. A drat-trim VERIFIED proof certifies that sampled base fiber is UNSAT. At least one certified p199 classification passes the engine gate; all CAP fails performance only.","rationale":"Separates mathematical classification from bounded failure."},
    "falsifier":{"kind":"expression","value":"Any control classification other than certified UNSAT, any model failing direct Definition-2.1 or clause checking, any DRAT rejection, or any independent encoding mismatch halts the affected claim.","rationale":"Defines decisive contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"A p199 classification concerns one frozen first-lift base fiber only. A sample result proves no full F_1 emptiness, J emptiness, LRC(13), CRT decomposition, or universal gcd-forcing theorem.","rationale":"Prevents sample overclaim."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "h11_control_bases":{"kind":"integer","value":240,"rationale":"Complete raw l=1-improper control set."},
    "p47_control_orbits":{"kind":"integer","value":53,"rationale":"Complete sealed canonical control set."},
    "p199_sample_orbits":{"kind":"integer","value":100,"rationale":"Exact frozen Cycle-8 strata."},
    "solver_seconds_per_instance":{"kind":"integer","value":300,"rationale":"Timeout retains the row as CAP."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Includes controls, p199 solve, and proof checking."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three solver/checker processes plus orchestration."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":107374182400,"rationale":"100 GiB, below current free space minus the mandatory 5 GiB reserve; includes DIMACS, proofs, sources, builds, and outputs."},
    "rng_seed":{"kind":"not_applicable","justification":"Encoding and selected solver configuration are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["exactly-one digit CNF","denominator-q bad-time cover clauses","prime-divisibility channel variables","at-most-(k-2) gcd-admissibility clauses","DRAT unsatisfiability certificates"],
  "selection_rule":["Write the encoding soundness argument before executable work.","Download and build only the pinned official solver and checker revisions after preflight.","Validate the encoder against an independent direct predicate and exact CNF evaluator.","Pass all H11 and p47 controls before p199.","Preserve accepted UNSAT proofs; directly preserve and recheck SAT witnesses.","Run at most three independent processes on CPUs 0-2."],
  "failure_rule":["Any control mismatch or checker failure halts frontier execution.","Timeout, proof-size cap, aggregate cap, or unverified output is CAP/ERROR and retains the base.","No all-CAP sample or solver status without its required independent evidence supports a mathematical claim."],
  "pre_execution":{"timestamp_utc":"2026-08-03T17:31:17Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 10 is sealed before this distinct proof-producing method family.","filesystem_observation_bytes":{"size":206900281344,"used":28231036928,"available":178652467200,"reserved":5368709120,"maximum_temporary_cap":173283758080,"chosen_temporary_cap":107374182400,"mount":"/"}},
  "input_paths":["artifacts/cycle-10-b010-lrc-gcd-pattern-v1.json","artifacts/cycle-8-b008-lrc-fused-lift-v1.json","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a control failure or aggregate cap.  After the fixed p199 sample,
classify only rows with the required independent evidence and take a material
companion review before sealing or changing engines.
