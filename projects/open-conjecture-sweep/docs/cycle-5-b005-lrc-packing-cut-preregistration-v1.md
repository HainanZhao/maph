# Cycle 5 / B005 preregistration: uncovered-time packing cut

## Decision question

Cycle 4's exact partition engine reached the edge cap because nearly every
depth-9 state emitted all centers covering its selected uncovered time. This
cycle tests a distinct mathematical invariant before emission: uncovered times
that cannot be pairwise covered by one translate require distinct remaining
centers.

The decision is whether a certified packing-witness cut preserves every cover
orbit, reproduces all frozen controls, and completes or materially reduces the
((13,199)) frontier within the existing state/edge/leaf/time/RAM gates.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 5,
  "parameters": {
    "frozen_base_engine": {"kind":"expression","value":"Reuse the corrected Cycle-4 64-partition engine: cyclic cover model, canonicalization, minimum-uncovered-time augmentation, early-cover extension, fixed 16-byte serialization, FNV-1a partitioning, partition-local exact deduplication, three workers, and all existing sound pruning.","rationale":"The only new mathematical rule is the declared packing cut."},
    "co_cover_relation": {"kind":"expression","value":"Let B be the frozen bad-time set in H_p and Delta=B-B. Two times u,v can lie in one translate B-x only if u-v is in Delta. For a current uncovered set W, define the incompatibility graph G_W on W by joining distinct u,v exactly when u-v is not in Delta.","rationale":"An edge certifies that no one remaining center can cover both endpoints."},
    "packing_witness": {"kind":"expression","value":"With r=k-|A| remaining centers, apply the new cut only when r<=5. Search deterministically for a clique P of size r+1 in G_W using ascending vertices and exact bitset backtracking with the cardinality bound |chosen|+|candidates|<r+1. Prune only after explicitly rechecking that every vertex of P is uncovered and every pair difference is outside Delta.","rationale":"Each pair in P requires distinct covering centers, so r centers cannot cover r+1 packed times. Explicit witness validation prevents a search bug from becoming an unsound prune."},
    "packing_soundness": {"kind":"expression","value":"If a completion by r translates existed, assign each time of P to one translate covering it. By pigeonhole, one translate would cover two members of P, contradicting their incompatibility. Therefore a validated size-(r+1) clique is a sound non-completability certificate. Failure to find a clique causes no prune and cannot omit a cover.","rationale":"This is the new invariant's complete logical interface."},
    "controls": {"kind":"text","value":"Require the naive k=3,p=11 oracle and byte-for-byte 53/50 p47 final-tuple equality. Every pruned state must expose a revalidated packing witness. Additionally exhaust all subsets W of H_11 and r=1..3, comparing the bitset witness search with brute-force clique enumeration. Intermediate level counts may decrease and are reported, not required to equal Cycle 4.","rationale":"Sound pruning is expected to remove non-completable intermediate states; final tuples and explicit witnesses test no omission."},
    "frontier_target": {"kind":"text","value":"For k=13,p=199, a complete pass requires the Cycle-1 4,748,938-row tuple set, at most 586985072 expanded states, 5869850724 generated edges, and 29565371 leaves. A strategically useful incomplete result must reduce emitted edges through the completed depth-9 level by at least 25 percent relative to Cycle 4 while preserving the exact level-9 state set.","rationale":"A 25-percent pre-emission reduction is large enough to justify further completion-cut development even if a later cap still fires."},
    "claim_boundary": {"kind":"expression","value":"The outcome concerns only the finite initial-sieve engine and packing invariant. It proves no J-empty claim, LRC(13), prime-product closure, novelty beyond reviewed sources, or general asymptotic theorem.","rationale":"A finite pruning certificate does not close the conjecture."}
  },
  "resource_caps": {
    "baseline_instances": {"kind":"integer","value":2,"rationale":"The two frozen p47 controls; H_11 subsets are an exhaustive code preflight."},
    "frontier_instances": {"kind":"integer","value":1,"rationale":"One k13,p199 decision run."},
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "expanded_state_cap": {"kind":"integer","value":586985072,"rationale":"Unchanged corrected Cycle-4 cap."},
    "generated_edge_cap": {"kind":"integer","value":5869850724,"rationale":"Unchanged corrected Cycle-4 cap."},
    "leaf_state_cap": {"kind":"integer","value":29565371,"rationale":"Unchanged corrected Cycle-4 cap."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"Unchanged one-hour cap."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Unchanged virtual-memory cap."},
    "temporary_disk_bytes": {"kind":"integer","value":173296054272,"rationale":"Measured free bytes 178664763392 minus the repository-required 5-GiB reserve."},
    "rng_seed": {"kind":"not_applicable","justification":"Clique search, partitioning, and enumeration are deterministic exact computations.","rationale":"Randomized packing witnesses are unnecessary."}
  },
  "formula_families": [
    "bad-set difference co-cover relation Delta=B-B",
    "uncovered-time incompatibility graph",
    "validated size-(r+1) clique certificate for r<=5",
    "corrected Cycle-4 partitioned canonical-level engine"
  ],
  "selection_rule": [
    "Write the packing soundness argument before using the cut.",
    "Pass the exhaustive H_11 subset oracle, explicit witness validation, and both end-to-end baseline final-tuple comparisons before frontier execution.",
    "Benchmark the optimized exact controls and run on CPUs 0-2 with one CPU reserved.",
    "Classify a complete equal frontier as a pass; classify an exact 25-percent depth-9 edge reduction as useful even if a later frozen cap fires."
  ],
  "failure_rule": [
    "Any invalid packing witness, subset-oracle mismatch, or baseline final-tuple mismatch falsifies the cut and halts frontier execution.",
    "A packing-search miss never authorizes pruning; only a revalidated witness does.",
    "Any cap breach is an algorithmic outcome, not a mathematical no-go.",
    "Do not promote a finite packing result to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T14:59:17Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes and the active open-conjecture-sweep project. Corrected Cycle 4 is sealed; Cycle 5 freezes a genuinely new packing invariant.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28218740736,"available":178664763392,"reserved":5368709120,"temporary_cap":173296054272,"mount":"/"}
  },
  "input_paths": [
    "artifacts/cycle-4-b004-lrc-partitioned-v2.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop before the frontier run on any packing-oracle or baseline failure. After
the exact frontier decision, choose whether the packing invariant continues or
the program switches to fused cover/lifting; resource-only adjustments remain
inside this cycle.
