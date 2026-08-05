# Cycle 7 / B007 preregistration: exact residual translate feasibility

## Decision question

Cycle 6 found that direct exact feasibility of covering the residual uncovered
times by the remaining (r) translates rejects 85.594% of a frozen depth-8
sample. This cycle tests whether that stronger predicate can be engineered as
a pre-emission frontier cut rather than merely a sample oracle.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 7,
  "parameters": {
    "predicate": {"kind":"expression","value":"For uncovered W and r remaining centers, FEAS(W,r) is true exactly when there exist at most r frozen translates B-x whose union contains W. Prune exactly when FEAS(W,r) is false; for r>5 retain without this cut.","rationale":"This is the stronger direct completion predicate discovered in Cycle 6."},
    "search": {"kind":"expression","value":"Use deterministic minimum-branch uncovered-time selection, deterministic center order, exact mask memoization keyed by (W,r), and a separately implemented verifier of every reported no-feasibility outcome on controls and the fixed stratified sample. A cache miss or resource cap retains the state.","rationale":"The predicate is sound only if negative answers are exact; performance shortcuts cannot prune."},
    "stratified_comparison": {"kind":"text","value":"On the frozen Cycle-6 100000-state depth-8 prefix, use exactly 100 lexicographic rows from each decile (1000 total) to compare direct FEAS with the Cycle-6 triple weak-5-color predicate. Record agreement/disagreement, but do not claim equivalence from agreement.","rationale":"The strata prevent the first-prefix-only comparison from disguising a distribution shift."},
    "performance_gate": {"kind":"expression","value":"Benchmark direct FEAS on the fixed 1000 stratified rows after warm-up. To authorize a full 33,193,860-state depth-8 frontier, the measured 99th-percentile per-state direct-search wall time must be at most 100 microseconds and no result may depend on an unverified cache answer. Otherwise classify the engine as a sample-only reduction and do not run the full frontier.","rationale":"At three workers this leaves material budget below the 1200-second frontier cap; slower exact work would only create a predictable resource failure."},
    "frontier_if_authorized": {"kind":"text","value":"Only after the performance gate passes, reuse the Cycle-4 partitioned retained-path engine with FEAS after existing sound pruning. Require baseline tuple equality and then either a complete Cycle-1 tuple set or at least 25% reduction in emitted depth-9 edges while preserving the depth-9 state set.","rationale":"The gate prohibits an uninformative long run."},
    "claim_boundary": {"kind":"expression","value":"This concerns exact finite residual-translate feasibility and its implementation cost. It proves no J-empty claim, LRC(13), lifting theorem, or equivalence to triple weak colorability.","rationale":"A local completion oracle is not a solution of the conjecture."}
  },
  "resource_caps": {
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "baseline_instances": {"kind":"integer","value":2,"rationale":"p47 k6/k7 tuple controls."},
    "stratified_rows": {"kind":"integer","value":1000,"rationale":"Exactly 100 rows from each of 10 fixed deciles."},
    "direct_nodes_per_state": {"kind":"integer","value":1000000,"rationale":"A node cap retains rather than prunes and prevents pathological sample rows."},
    "wall_seconds": {"kind":"integer","value":1200,"rationale":"The full frontier is forbidden unless the performance gate passes."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Repository runtime cap."},
    "temporary_disk_bytes": {"kind":"integer","value":173283487744,"rationale":"Measured free bytes 178652196864 minus the repository-required 5-GiB reserve."},
    "rng_seed": {"kind":"not_applicable","justification":"State selection, branching, and memoization are deterministic.","rationale":"No randomized search is used."}
  },
  "formula_families": [
    "residual B-translate set cover FEAS(W,r)",
    "deterministic exact memoized branch-and-cover",
    "triple weak-colorability comparison",
    "pre-emission retained-path cut"
  ],
  "selection_rule": [
    "Write the direct-feasibility soundness argument before executable work.",
    "Pass exhaustive H11 direct oracle and both p47 tuple controls before timing the stratified p199 rows.",
    "Require the frozen performance gate before any full frontier run.",
    "On a failed performance gate, preserve the sample reduction and switch at the reviewed boundary to fused cover/lifting rather than consuming a frontier instance."
  ],
  "failure_rule": [
    "Any false negative, cache inconsistency, direct-witness verification failure, or baseline tuple mismatch halts the frontier branch.",
    "A triple/direct disagreement is an observation requiring diagnosis; it does not by itself invalidate direct FEAS because triple colorability is only necessary.",
    "A failed performance gate is an algorithmic result, not a mathematical no-go.",
    "Do not promote finite feasibility rejection to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T16:19:01Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent work; Cycle 6 is sealed and Cycle 7 freezes the distinct direct-feasibility engine.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28231307264,"available":178652196864,"reserved":5368709120,"temporary_cap":173283487744,"mount":"/"}
  },
  "input_paths": [
    "artifacts/cycle-6-b006-lrc-triple-hypergraph-v1.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop before a frontier run on any exactness/control failure or a failed
100-microsecond 99th-percentile performance gate. Preserve the reduction and
move to fused initial-cover/lifting at the next material decision boundary.
