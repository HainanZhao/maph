# Cycle 1 / B001 preregistration: Lonely Runner frontier and exact ansatz baseline

## Claim boundary and decision question

`OBSERVED`: a bounded source audit through 2026-08-03 identifies
\(LRC(13)\), the case of 14 total runners, as the first unresolved finite
Lonely Runner case. Sungkawichai--Trakulthongchai, arXiv:2604.23906v1,
Theorem 1.3 proves \(LRC(k)\) for \(k\leq 12\), and Section 7 names efficient
computation of \(I(k,p,1)\) as the bottleneck for \(k=13\). Searches for
"fourteen lonely runners" and \(LRC(13)\), plus an official OpenAI-source
search, found no later solution. This is bounded evidence, not proof of
universal openness or absence of unpublished work.

The cycle asks whether we can reproduce the exact \(I(k,p,1)\) ansatz
interface independently and expose the true computational boundary at the
first frozen \(k=13\) prime. It does not claim that an \(I(13,p,1)\) result,
even for several primes, proves \(LRC(13)\).

The published implementation is frozen for comparison at main commit
`755b116b2e6090cd4a83187a696f863388b7d746`. Its recorded baseline outputs
are \(|I(6,47,1)/\!\sim|=53\) and \(|I(7,47,1)/\!\sim|=50\), under the
paper's canonical representative convention. The frontier probes are
\(k=13\) and primes \(199,211,223\), in that order; only \(p=199\) is
required in this cycle.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 1,
  "parameters": {
    "target_statement": {
      "kind": "expression",
      "value": "LRC(13): every tuple (u_1,...,u_13) of positive integers has a real witness t with ||t u_i|| >= 1/14 for all i; this is the 14-total-runner case.",
      "rationale": "Fixes the one-fewer-runner convention and prevents an off-by-one frontier claim."
    },
    "ansatz_definition": {
      "kind": "expression",
      "value": "For prime p and l=1, I(k,p,1) consists of tuples v in (Z_p\\{0})^k for which no a/p, a in Z, satisfies min((a v_i mod p), p-(a v_i mod p))*(k+1) >= p for every i. The gcd alternative in properness is impossible at l=1.",
      "rationale": "This is the exact integer verifier interface from Definition 2.1 of arXiv:2604.23906v1 specialized to l=1."
    },
    "canonicalization": {
      "kind": "expression",
      "value": "Identify tuples under coordinate permutation, independent coordinate sign flips modulo p, and common multiplication by a unit modulo p. Emit sorted representatives 1=v_1<=...<=v_k<=(p-1)/2, deduplicated by the full orbit canonical form.",
      "rationale": "Matches Section 5.1 and makes published counts comparable without treating raw DFS paths as distinct tuples."
    },
    "published_baselines": {
      "kind": "text",
      "value": "At upstream commit 755b116b2e6090cd4a83187a696f863388b7d746: k=6,p=47 has 53 canonical l=1 improper tuples; k=7,p=47 has 50.",
      "rationale": "Two frozen exact outputs test the verifier across different dimensions before any frontier computation."
    },
    "frontier_order": {
      "kind": "text",
      "value": "Probe (k,p) in the fixed order (13,199), (13,211), (13,223); stop after p=199 unless it completes within cap and the same frozen algorithm can continue without modification.",
      "rationale": "The upstream k=13 configuration begins with these primes; fixed ordering prevents selecting an easy post-result instance."
    },
    "source_boundary": {
      "kind": "text",
      "value": "Primary boundary: Sungkawichai and Trakulthongchai, arXiv:2604.23906v1, Theorem 1.3, Proposition 3.1, Section 5, Section 7; comparison code main commit 755b116b2e6090cd4a83187a696f863388b7d746 and for-k-12 commit bd4fb465b874db1fe29b73ee3e7b3811674c00a5.",
      "rationale": "Pins the theorem, algorithmic interface, stated bottleneck, and comparison implementation inspected before execution."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "Baseline agreement is OBSERVED reproduction. Exact enumeration under independently checked exhaustive logic may be promoted only for the stated finite ansatz. No finite I(k,p,1) count alone proves J(k,p)=empty or LRC(k), and no bounded search proves novelty or universal openness.",
      "rationale": "Separates exact finite evidence from the lifting and prime-product bridge required for LRC."
    }
  },
  "resource_caps": {
    "baseline_instances": {"kind":"integer","value":2,"rationale":"The frozen k=6 and k=7 instances at p=47."},
    "frontier_primes": {"kind":"integer","value":3,"rationale":"The fixed ordered list 199,211,223, with only the first required."},
    "required_frontier_primes": {"kind":"integer","value":1,"rationale":"One exact boundary measurement is enough for the Cycle-1 decision."},
    "wall_seconds_per_baseline": {"kind":"integer","value":300,"rationale":"Small exact reproductions should fail fast if conventions disagree."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"Timeboxes the known I(13,p,1) bottleneck without turning the cycle into an unbounded compute run."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Prevents an accidental exhaustive materialization beyond the available research envelope."},
    "rng_seed": {"kind":"not_applicable","justification":"All enumeration and checks are deterministic and exact.","rationale":"No randomized search may support the cycle decision."}
  },
  "formula_families": [
    "exact modular distance test (k+1)*min(r,p-r) >= p",
    "bad-time set cover dual: an l=1 tuple is improper exactly when its coordinate bad-time sets cover all nonzero times modulo sign",
    "permutation, coordinate-sign, and global-unit orbit canonicalization",
    "published lift/project interface J(k,p) subset pi_p(S), used only to state what the l=1 verifier does not prove"
  ],
  "selection_rule": [
    "Implement a transparent brute-force oracle for tiny instances and a separate exact bitset/set-cover enumerator for the frozen baselines.",
    "Require both frozen baseline counts and direct tuple-by-tuple modular rechecks before running k=13.",
    "Run k=13,p=199 with the unchanged exact enumerator and record completion, timeout, node count, canonical solution count if complete, wall time, and peak memory.",
    "Advance to p=211 and then p=223 only if the preceding instance completes within its cap without code or rule changes.",
    "A Cycle-1 advance is baseline reproduction plus a reproducible exact frontier measurement that identifies the next design bottleneck; a full LRC result is not required."
  ],
  "failure_rule": [
    "Any mismatch with either frozen published count halts the frontier run until the convention or implementation defect is resolved.",
    "Any pruning rule lacking a proof that it preserves every cover is exploratory and may not affect an exact count.",
    "A timeout or memory cap is a measured boundary, not evidence that no efficient algorithm exists and not a mathematical no-go.",
    "A later vetted proof of LRC(13) makes this problem ineligible and stops Problem 1.",
    "Do not infer J(k,p)=empty, LRC(13), novelty, or OpenAI noninvolvement from a finite ansatz count or bounded source search."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T12:13:02Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes in other projects and tools, plus the untracked open-conjecture-sweep project. This cycle freezes only its embedded mathematical and source parameters and the shared validator."
  },
  "input_paths": [
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop and interpretation rules

If the two baseline counts agree, the exact modular predicate and orbit
conventions are reproduced for this scope. If \((13,199)\) finishes, its
count is an exact finite result only after an independent direct recheck of
every emitted tuple and exhaustive-search coverage. If it does not finish,
the retained node/time/memory profile defines the next pruning design
question. New pruning or a changed method family requires the next cycle.
