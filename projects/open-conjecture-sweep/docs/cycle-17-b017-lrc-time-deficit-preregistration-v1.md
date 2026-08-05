# Cycle 17 / B017 preregistration: analytic typed time-deficit signatures

## Decision question and idea selection

Can a finite family of exact nonnegative weighted time-deficit inequalities
cover every canonical gcd-witness leaf of a further frozen p199 base without
invoking a SAT solver?

The primary proposed weighted time deficits, exact small-support Hall/set-cover
dual certificates, and a CRT composition fallback.  Darwin independently
proposed typed time-deficit signatures with exact Hall/set-cover certificates,
then CRT.  We questioned whether this merely repackages the Cycle-16 singleton
core: bounded combinations can detect incompatibility among several time
clauses even when each clause has allowed literals.  We also questioned
whether failure of the bounded grammar is a no-go; it is not.  The selected
engine is exact certificate search, while coverage rates remain `OBSERVED`.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":17,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: weighted time deficits, exact Hall/set-cover duals, then CRT. Companion: typed time-deficit signatures and certificate-checked union coverage, then CRT. Choose weighted time deficits because they strictly include Cycle 16's singleton direct deficit while every accepted leaf has a short independently checkable inequality.","rationale":"Both agents proposed analytic deficit certificates; bounded failure is explicitly not saturation."},
    "leaf_state":{"kind":"expression","value":"Use the exact Cycle-16 canonical first-two-nondivisibility partition. For each base and leaf, A_i is the set of digits not forbidden by the canonical mod-2/mod-7 units. Empty A_i is an immediate exact leaf contradiction.","rationale":"Reuses a proved disjoint exhaustive state space."},
    "time_data":{"kind":"expression","value":"Parse every positive x-only coverage clause from the exact Cycle-11 CNF in source order. Deduplicate identical literal sets, retaining the first source clause index. For allowed digit d at coordinate i and retained clause t, b(i,d,t)=1 exactly when x(i,d) occurs in t.","rationale":"The analytic signatures are derived from frozen exact clauses, not floating geometry."},
    "certificate":{"kind":"expression","value":"For nonnegative integer weights w_t define W=sum_t w_t and U=sum_i max_{d in A_i} sum_t w_t*b(i,d,t). Accept a leaf certificate iff U<W, storing the retained source clause indices, positive weights, W, every coordinate maximum, and U. The checker independently reconstructs A_i and b from the frozen CNF and recomputes the strict integer inequality.","rationale":"Any full bad-time cover implies W<=U, so strict deficit is a proof."},
    "grammar":{"kind":"expression","value":"First test every retained time signature as the singleton weight-1 family. If none certifies, rank retained signatures by singleton capacity sum_i max_{d in A_i} b(i,d,t), then retained source clause index, then literal-set SHA-256. Keep the first 24 signatures with singleton capacity at most 5. Exhaustively enumerate supports of one, two, or three distinct kept signatures and positive integer weights of total W at most 6. Candidate order is W, support size, increasing signature-rank tuple, then lexicographic weight tuple; accept the first strict deficit.","rationale":"A finite deterministic grammar extends direct deficits to multi-time choice incompatibilities while remaining cheap to verify."},
    "bases":{"kind":"expression","value":"Run all 6084 leaves of frozen sample base 4 as training and all 6084 leaves of frozen sample base 3 as validation, regardless of the training outcome. Use frozen base 7 leaf ordinal 74 as a positive singleton control. Do not inspect the remaining 97 p199 sample bases or the 4,748,938-base census.","rationale":"Two previously SAT-certified bases measure whether the analytic family closes an entire new tree."},
    "selection":{"kind":"expression","value":"For each leaf retain only the first certificate in the frozen order. Report exact covered-leaf counts for both bases. A base is analytically closed only if all 6084 leaf certificates independently verify; ties and partial rates select no broader claim.","rationale":"Prevents post-result signature or base selection."},
    "continuation":{"kind":"expression","value":"After independently auditing every bounded-grammar certificate, run scipy 1.14.1 optimize.linprog(method='highs-ds', presolve=True) only on the 477 still-uncovered frozen rows. For every leaf use every deduplicated time signature as a nonnegative weight variable, impose sum(w)=1, introduce z_i >= sum_t b(i,d,t)w_t for every allowed digit, and minimize sum_i z_i. Process leaf order by base 4 then base 3 and ordinal. For an optimum below 1-1e-9, round w_t*D to nearest integer with ties to even for D in 2^12,2^16,2^20,2^24 order, discard zero entries, and accept the first integer vector of support at most 192 whose independently recomputed exact U<W. LP status, objective, support, integer weights, source clause indices, coordinate maxima, W, and U are retained for every row.","rationale":"Companion-reviewed same-theorem continuation uses floating optimization only to propose short rational certificates; exact integer verification alone proves a leaf."},
    "advance_condition":{"kind":"expression","value":"A checked 6084-of-6084 certificate union for base 4 or base 3 is a structural advance and an independent exact first-lift exclusion for that named base. Otherwise retain exact certificate counts and close only this bounded grammar.","rationale":"Requires complete symbolic coverage rather than classifier accuracy."},
    "falsifier":{"kind":"expression","value":"A leaf partition mismatch, allowed-digit mismatch, misidentified coverage clause, nonpositive or out-of-grammar weight, incorrect coordinate maximum, U>=W, or uncovered leaf in a claimed complete base invalidates the affected result.","rationale":"Defines direct exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"A certificate proves only its named base/leaf residual. Complete coverage proves only the named base's first-lift exclusion. Failure is not evidence against larger supports, rational weights, other analytic duals, CRT, F_1 emptiness, J emptiness, or LRC(13).","rationale":"The grammar is bounded and incomplete by design."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "training_bases":{"kind":"integer","value":1,"rationale":"Frozen sample index 4."},
    "validation_bases":{"kind":"integer","value":1,"rationale":"Frozen sample index 3."},
    "canonical_leaves_per_base":{"kind":"integer","value":6084,"rationale":"Complete canonical partition."},
    "signature_pool":{"kind":"integer","value":24,"rationale":"Frozen low-singleton-capacity pool per leaf."},
    "singleton_capacity_cap":{"kind":"integer","value":5,"rationale":"Only low-capacity signatures enter combinations; every singleton is still tested."},
    "support_size":{"kind":"integer","value":3,"rationale":"At most three distinct time signatures."},
    "total_integer_weight":{"kind":"integer","value":6,"rationale":"Finite exact weight grammar."},
    "lp_continuation_rows":{"kind":"integer","value":477,"rationale":"Exactly the 176 base-4 and 301 base-3 rows left uncovered by the audited bounded grammar."},
    "lp_integer_support_cap":{"kind":"integer","value":192,"rationale":"Keeps every promoted certificate short and independently checkable."},
    "lp_objective_acceptance_margin":{"kind":"expression","value":"1e-9 below 1","rationale":"Floating solutions only propose candidates; exact U<W is still mandatory."},
    "integerization_denominators":{"kind":"expression","value":"4096,65536,1048576,16777216","rationale":"Deterministic bounded rational reconstruction ladder."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Engine, full two-base run, independent audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three workers plus exact clause tables."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Leaves, signatures, candidates, bases, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical gcd-witness leaves","exact time-coverage clauses","nonnegative integer weighted time deficits","bounded-support Hall/set-cover dual certificates","certificate-checked leaf unions"],
  "selection_rule":["Check base-7 leaf 74 as a singleton positive control.","Process every leaf of bases 4 and 3.","Test all singleton clauses before the frozen bounded combination grammar.","Retain only the first exact certificate per leaf.","Independently audit all stored bounded-grammar certificates before LP continuation.","Run pinned LP separation only on the 477 frozen uncovered rows and promote only exact integerized deficits.","Claim a named base closed only at 6084 independently verified leaves."],
  "failure_rule":["Any control or encoding mismatch halts execution.","An uncovered leaf remains explicit and blocks full-base closure.","A cap retains completed certificates but makes rates OBSERVED only.","No SAT calls, other bases, or census-wide execution are authorized."],
  "pre_execution":{"timestamp_utc":"2026-08-03T21:32:00Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 16 is sealed before this distinct analytic certificate family.","filesystem_observation_bytes":{"size":206900281344,"used":40880799744,"available":166002704384,"reserved":5368709120,"maximum_temporary_cap":160633995264,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-16-b016-lrc-gcd-witness-tree-v1.json","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle11-certified-sat/p199/007.cnf","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_16_gcd_witness_tree_soundness.md","proof/cycle_17_time_deficit_soundness.md","requirements-cycle17.txt","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a control/encoding/audit failure or aggregate cap.  Darwin reviewed the
bounded run and advised same-cycle exact LP separation after independent audit.
After the frozen continuation, ask Darwin to review the completed evidence,
co-propose next ideas, and advise whether Cycle 17 seals, continues, or gives
way to CRT.
