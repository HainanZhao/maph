# Cycle 2 / B002 preregistration: cyclic-cover canonical augmentation

## Decision question

Cycle 1 exposed \(I(k,p,1)\) as a cyclic translate-cover problem but
enumerated billions of normalization-equivalent partial branches before
canonicalizing only at the leaves. This cycle tests one new engine: canonical
augmentation of partial multisets under the global-unit action.

The decision is whether that quotient is proved complete, reproduces the two
frozen baselines exactly, and reduces both DFS nodes and leaves by at least a
factor of ten on \((k,p)=(13,199)\). This remains an initial-sieve result and
cannot establish \(J(13,199)=\varnothing\) or \(LRC(13)\).

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 2,
  "parameters": {
    "cyclic_cover_model": {
      "kind": "expression",
      "value": "For odd prime p let H_p=F_p^*/{+1,-1}, a cyclic group of order h=(p-1)/2. Let B_{k,p}={[t] in H_p : (k+1)*min(t mod p,p-(t mod p))<p}. A speed multiset M is l=1 improper exactly when the translates B_{k,p}-x, x in M, cover H_p, with multiplicity allowed in M.",
      "rationale": "The identity C_s={t: ts is bad}=B-s in discrete-log coordinates turns the ansatz into an exact cyclic translate cover."
    },
    "group_action": {
      "kind": "expression",
      "value": "H_p acts on a partial speed multiset M by translation M+a and on its covered-time set U by U-a. Permutations are removed by treating M as a multiset; coordinate sign flips are already quotiented in H_p. Coverage and extendability to a k-cover are invariant under this action.",
      "rationale": "This is precisely the permutation/sign/global-unit equivalence used in Cycle 1, expressed on partial states rather than only leaves."
    },
    "cyclic_coordinate": {
      "kind": "expression",
      "value": "For each frozen prime p, choose the least positive primitive root g modulo p. Represent the signed residue class of g^e by e modulo h=(p-1)/2, and order H_p by the integer exponents 0,1,...,h-1 for every lexicographic canonical-form comparison.",
      "rationale": "Pins the generator and ordering on which the canonical parent depends."
    },
    "canonical_form": {
      "kind": "expression",
      "value": "can(M) is the lexicographically least sorted multiset among {M+a:a in H_p}. For nonempty M, write C=can(M), delete one copy of the largest entry of C, and define parent(M)=can(C without that entry). A child orbit represented by can(A union {x}) is accepted from canonical parent A exactly when parent(A union {x})=A; duplicate canonical children are emitted once.",
      "rationale": "This is an orbit-invariant canonical-parent map and supplies an orderly construction path without assuming arbitrary prefixes of a canonical leaf are canonical."
    },
    "completeness_obligation": {
      "kind": "expression",
      "value": "Prove by induction on multiset size that every H_p orbit has exactly one emitted canonical representative: existence follows by applying the invariant parent map and adding back the deleted element after aligning the parent; uniqueness follows from canonical child deduplication and the unique canonical parent orbit. Coverage pruning may depend only on orbit-invariant covered-set data and a proved upper bound on what the remaining slots can cover.",
      "rationale": "The Cycle-1 weakness was omitted-branch completeness; the quotient cannot count unless this proof is explicit and executable invariants match it."
    },
    "baselines": {
      "kind": "text",
      "value": "Required exact outputs: |I(6,47,1)/~|=53 and |I(7,47,1)/~|=50, with tuple-orbit sets equal to the frozen Cycle-1 outputs, not merely equal counts.",
      "rationale": "Tuple equality detects an incorrect parent rule hidden by an accidental count match."
    },
    "frontier_target": {
      "kind": "text",
      "value": "For k=13,p=199 compare against Cycle 1: 4,748,938 representatives, 5,869,850,724 nodes, and 295,653,716 leaves. Pass requires the same representative set and at most 586,985,072 nodes and 29,565,371 leaves.",
      "rationale": "A preregistered tenfold reduction is large enough to justify carrying the quotient into lifting work."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A pass proves only completeness and performance of the declared finite cyclic-cover quotient on the frozen instances. It proves no eventual properness, J-empty claim, prime-product contradiction, LRC(13), novelty beyond reviewed sources, or general asymptotic speedup.",
      "rationale": "The new engine addresses initial-cover duplication only."
    }
  },
  "resource_caps": {
    "baseline_instances": {"kind":"integer","value":2,"rationale":"The two independently frozen Cycle-1 controls."},
    "frontier_instances": {"kind":"integer","value":1,"rationale":"Only k=13,p=199 is authorized for the performance decision."},
    "node_cap": {"kind":"integer","value":586985072,"rationale":"Ten percent of the Cycle-1 frontier node count, rounded down."},
    "leaf_cap": {"kind":"integer","value":29565371,"rationale":"Ten percent of the Cycle-1 frontier leaf count, rounded down."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"Same wall cap as Cycle 1."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Same memory cap as Cycle 1."},
    "rng_seed": {"kind":"not_applicable","justification":"Canonical augmentation and all comparisons are deterministic exact computations.","rationale":"Randomized orbit sampling cannot satisfy completeness. "}
  },
  "formula_families": [
    "cyclic group H_p=F_p^*/{+1,-1} in discrete-log coordinates",
    "bad-time translate cover B_{k,p}-x",
    "lexicographic translation canonical form for multisets",
    "invariant largest-entry deletion canonical-parent map",
    "orbit-invariant exact coverage and proved remaining-slot upper bounds"
  ],
  "selection_rule": [
    "Write the canonical-parent completeness argument before using the quotient output as an exact count.",
    "Exhaust tiny cyclic groups by a naive orbit oracle, then require tuple-orbit equality on both p=47 baselines.",
    "Run k=13,p=199 only after the proof obligations and baselines pass, using the unchanged accepted-child and pruning rules.",
    "Pass only if the complete frontier representative set equals Cycle 1 and both frozen tenfold node and leaf thresholds hold.",
    "If representative equality passes but either performance threshold fails, classify the engine as exact but strategically insufficient."
  ],
  "failure_rule": [
    "Any orbit missing from or duplicated by canonical augmentation falsifies the engine and halts the frontier run.",
    "Any pruning rule not proved orbit-invariant and cover-preserving is exploratory and cannot affect an exact output.",
    "A count-only baseline match without equality of canonical tuple sets is a failure.",
    "A timeout, memory breach, node-cap breach, or leaf-cap breach is a failed performance gate, not a mathematical no-go.",
    "Do not promote a finite quotient result to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T12:52:33Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes elsewhere and the active untracked open-conjecture-sweep project. Cycle 1 is sealed; this freeze names only its artifact, this preregistration, and the shared validator as inputs."
  },
  "input_paths": [
    "artifacts/cycle-1-b001-lrc-frontier-census-v1.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop before the frontier run if the canonical-parent proof, tiny oracle, or
either baseline tuple-set comparison fails. After a complete frontier pass or
a frozen resource/performance failure, take a material engine decision; do
not alter the parent rule or pruning family inside this cycle.
