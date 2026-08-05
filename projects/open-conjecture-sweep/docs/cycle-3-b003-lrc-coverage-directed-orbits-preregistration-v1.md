# Cycle 3 / B003 preregistration: coverage-directed orbit levels

## Decision question

Cycle 2 proved useful orbit canonicalization on the frozen controls but its
largest-entry parent abandoned the selected-uncovered-time branch that made the
original exact-cover search effective. This cycle tests one distinct engine:
level-wise canonical state deduplication combined with coverage-directed
augmentation.

The decision is whether this engine retains at least one construction path for
every cover orbit, reproduces both frozen tuple sets, and completes
\((k,p)=(13,199)\) within the frozen resource bounds. It remains an initial
sieve and cannot establish \(J(13,199)=\varnothing\) or \(LRC(13)\).

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 3,
  "parameters": {
    "cyclic_cover_model": {
      "kind": "expression",
      "value": "For odd prime p let H_p=F_p^*/{+1,-1}, h=(p-1)/2, in exponent coordinates for the least positive primitive root modulo p. Let B_{k,p} be the signed residue classes r with (k+1)*min(r,p-r)<p. A size-k speed multiset M is l=1 improper exactly when the translates B_{k,p}-x for x in M cover H_p.",
      "rationale": "This is the exact frozen translate-cover model used in Cycles 1 and 2."
    },
    "canonical_state": {
      "kind": "expression",
      "value": "can(M) is the lexicographically least sorted translate among {M+a:a in H_p}. At each cardinality d maintain exactly the set L_d of distinct canonical multisets reached by the declared augmentation rule; duplicates are removed globally within the level before any state is expanded.",
      "rationale": "Level deduplication removes orbit-equivalent partial states without imposing the Cycle-2 largest-entry parent."
    },
    "directed_augmentation": {
      "kind": "expression",
      "value": "For A in L_d compute its covered set U(A). If U(A) is not H_p, select q(A)=min(H_p minus U(A)) in the pinned exponent order and generate can(A multiset-union {x}) exactly for centers x whose translate B_{k,p}-x contains q(A). If U(A)=H_p and d<k, generate all x in H_p so extensions to size k are retained. L_{d+1} is the global set of resulting canonical states.",
      "rationale": "Every added center normally covers a deterministic uncovered time, restoring exact-cover direction while canonicalization handles the unit orbit."
    },
    "completeness_obligation": {
      "kind": "expression",
      "value": "For every size-k cover S, construct a retained path inductively. After translating the current prefix to its canonical representative A, translate the unused elements of S by the same shift. If A is not yet a cover, the full translated S covers q(A), so at least one unused element x covers q(A) and the rule emits can(A union {x}); if A already covers, the all-x clause emits every extension. Thus some path reaches can(S). Level deduplication can merge paths but cannot remove the reached orbit. Prove this argument before frontier execution and verify it against a naive tiny oracle.",
      "rationale": "This supplies cover-orbit existence without requiring a unique canonical parent."
    },
    "pruning": {
      "kind": "expression",
      "value": "The only authorized pruning beyond directed augmentation is: with r=k-|A| remaining slots and uncovered set W, prune if |W| exceeds r times max_x |(B_{k,p}-x) intersect W|. No heuristic ordering, dominance cut, or post-result threshold may remove a state.",
      "rationale": "The bound is orbit-invariant and cannot discard a completable cover."
    },
    "parallel_schedule": {
      "kind": "expression",
      "value": "Use exactly three worker threads on CPUs 0,1,2 and leave CPU 3 available. Partition each frozen level through a shared dynamic work queue; workers accumulate local child sets and the deterministic union forms the next level. All node, edge, time, and memory caps are aggregate across workers.",
      "rationale": "Fine-grained dynamic scheduling follows the repository compute rule and avoids Cycle-2 static-shard imbalance."
    },
    "baselines": {
      "kind": "text",
      "value": "Required exact outputs are 53 canonical tuples for (k,p)=(6,47) and 50 for (7,47), with tuple sets equal to the frozen Cycle-1 files. A count-only match fails.",
      "rationale": "Full tuple equality detects an omitted orbit or convention error."
    },
    "frontier_target": {
      "kind": "text",
      "value": "For (k,p)=(13,199), a pass requires a complete size-13 canonical tuple set equal to the 4,748,938-row Cycle-1 census, at most 586,985,072 expanded unique states, at most 5,869,850,724 generated candidate edges, and at most 29,565,371 examined size-13 canonical states.",
      "rationale": "The state threshold preserves the intended tenfold reduction while the separate edge cap prevents cheap node accounting from hiding excessive work."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A pass establishes only completeness and frozen-instance performance of this finite cyclic-cover engine. It proves no eventual properness, J-empty claim, prime-product contradiction, LRC(13), novelty beyond reviewed sources, or general asymptotic improvement.",
      "rationale": "The target is an improved exact initial-sieve interface, not the conjecture itself."
    }
  },
  "resource_caps": {
    "baseline_instances": {"kind":"integer","value":2,"rationale":"The two frozen exact controls."},
    "frontier_instances": {"kind":"integer","value":1,"rationale":"Only k=13,p=199 is authorized for the frontier decision."},
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use three of four available CPUs and reserve one."},
    "expanded_state_cap": {"kind":"integer","value":586985072,"rationale":"Ten percent of the Cycle-1 DFS-node count, rounded down."},
    "generated_edge_cap": {"kind":"integer","value":5869850724,"rationale":"The full Cycle-1 DFS-node count bounds hidden candidate-generation work."},
    "leaf_state_cap": {"kind":"integer","value":29565371,"rationale":"Ten percent of the Cycle-1 leaf count, rounded down."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"Same wall cap as the prior frontier runs."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Shared aggregate memory limit."},
    "rng_seed": {"kind":"not_applicable","justification":"The level construction, work assignment, and set union are exact and result-deterministic.","rationale":"Random sampling cannot establish completeness."}
  },
  "formula_families": [
    "cyclic signed-unit group in least-primitive-root exponent coordinates",
    "bad-time translate cover B_{k,p}-x",
    "lexicographic translation canonicalization of multisets",
    "minimum-uncovered-time directed augmentation",
    "global per-level canonical-state deduplication",
    "orbit-invariant remaining-coverage upper bound"
  ],
  "selection_rule": [
    "Write the retained-path completeness proof and exhaust a naive tiny oracle before using the engine as an exact enumeration.",
    "Require byte-for-byte canonical tuple equality on both p=47 baselines before frontier execution.",
    "Compile the validated hot path with -O3 -march=native -flto -DNDEBUG -pthread and benchmark an exact control before the long run.",
    "Run the frontier with exactly three dynamically scheduled workers and aggregate caps.",
    "Pass only after complete frontier tuple-set equality and every frozen state, edge, leaf, time, and memory threshold passes."
  ],
  "failure_rule": [
    "Any tiny-oracle or baseline tuple mismatch falsifies the implementation or completeness argument and halts the frontier run.",
    "Any unproved pruning or deduplication rule is exploratory and cannot affect an exact output.",
    "A timeout, memory breach, expanded-state breach, generated-edge breach, or leaf breach is an algorithmic gate failure, not a mathematical no-go.",
    "If early full covers occur, omitting their all-center extension clause is a completeness failure.",
    "Do not promote a finite quotient result to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T13:55:23Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes elsewhere and the active untracked open-conjecture-sweep project. Cycles 1 and 2 are sealed; this freeze names their artifacts, this preregistration, and the shared validator as inputs."
  },
  "input_paths": [
    "artifacts/cycle-1-b001-lrc-frontier-census-v1.json",
    "artifacts/cycle-2-b002-lrc-orbit-quotient-v1.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop before the frontier run if the retained-path proof, tiny oracle, either
baseline tuple comparison, or representative benchmark fails. After a complete
frontier decision or frozen resource failure, take the next material engine
decision without changing this cycle's augmentation or pruning family.
