# Cycle 6 / B006 preregistration: triple non-co-cover hypergraph cut

## Decision question

Cycle 5 proved that every pair of times in (H_{199}) can be co-covered by a
translate of the frozen bad set (B). This cycle tests the next strictly
higher-order invariant: a triple may fail to be co-coverable even when all of
its pairs are. The decision is whether the resulting forbidden-triple
hypergraph can certify that the uncovered times require more remaining
translates than are available before child emission.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 6,
  "parameters": {
    "frozen_base_model": {"kind":"expression","value":"Use the Cycle-4 cyclic cover model on H_p with its pinned bad-time convention. A translate B-x co-covers a triple {u,v,w} exactly when some x has u,v,w in B-x.","rationale":"The new object changes only the co-cover arity, not conventions or the retained-path engine."},
    "forbidden_hypergraph": {"kind":"expression","value":"Let F be the 3-uniform hypergraph on H_p whose edges are triples T with no common covering center. For an uncovered set W, use the induced hypergraph F[W].", "rationale":"Every one-center color class in a genuine completion contains no edge of F."},
    "cut_rule": {"kind":"expression","value":"With r=k-|A| remaining centers and 2<=r<=5, prune only if an exact deterministic weak-r-colorability solver proves F[W] is not r-colorable. A completion by r translates assigns every uncovered time to one covering center, yielding a proper weak r-coloring; thus non-r-colorability is sound. For r=1, use a direct common-center check only.","rationale":"This is the minimal higher-order analogue of the Cycle-5 pairwise packing rule. Solver failure to refute colorability never prunes."},
    "global_saturation_test": {"kind":"expression","value":"First solve exact weak 2-colorability of the global F on H_199. If a coloring is found, verify every forbidden triple is non-monochromatic. Its restriction colors every F[W], so the r>=2 cut is structurally vacuous for all states and no frontier run is authorized.","rationale":"A global 2-coloring is a decisive, stronger falsifier than a finite no-prune sample."},
    "small_oracle": {"kind":"text","value":"For k=3,p=11 exhaust all subsets W of H_11 and r=1..3. Compare the exact weak-colorability solver against brute-force enumeration of all r-colorings, and separately revalidate every declared forbidden triple by exhaustive center search.","rationale":"The small group gives a complete independent oracle for hyperedges and colorability."},
    "sample_if_needed": {"kind":"text","value":"Only if the global H_199 hypergraph is not weakly 2-colorable, enumerate a fixed lexicographic prefix of at most 100000 Cycle-4 canonical depth-8 states and compare the hypergraph cut with an exact r-translate set-cover oracle. Do not execute the full frontier unless the cut prunes at least 25 percent of that fixed sample while every exact-cover-feasible state is retained.","rationale":"The sample distinguishes a mathematically nontrivial relation from an economically useful pre-emission cut without spending a frontier instance prematurely."},
    "claim_boundary": {"kind":"expression","value":"Any result concerns only this forbidden-triple weak-colorability cut under the frozen cyclic model. It proves no J-empty claim, LRC(13), lift, prime-product closure, or statement about higher arities.","rationale":"A finite local completion invariant is not a Lonely Runner proof."}
  },
  "resource_caps": {
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "global_color_nodes": {"kind":"integer","value":10000000,"rationale":"Hard cap for deterministic exact global-color search; a cap hit means no structural conclusion."},
    "h11_colorings": {"kind":"integer","value":4096,"rationale":"At most 32 subsets times 3^5 assignments per fixed r, exhaustively checked."},
    "sample_states": {"kind":"integer","value":100000,"rationale":"Fixed upper bound only if the global saturation falsifier fails."},
    "wall_seconds": {"kind":"integer","value":1200,"rationale":"No full frontier is authorized unless the fixed sample first passes its utility gate."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Repository runtime cap."},
    "temporary_disk_bytes": {"kind":"integer","value":173294731264,"rationale":"Measured free bytes 178663440384 minus the repository-required 5-GiB reserve."},
    "rng_seed": {"kind":"not_applicable","justification":"All triple enumeration, search order, and color assignment order are deterministic.","rationale":"Randomness is unnecessary."}
  },
  "formula_families": [
    "triple common-center relation for B translates",
    "forbidden 3-uniform hypergraph F",
    "exact weak r-colorability as a completion necessary condition",
    "global 2-color saturation certificate"
  ],
  "selection_rule": [
    "Write the hypergraph soundness argument before executable work.",
    "Pass the H_11 exhaustive hyperedge and colorability oracle before any p=199 conclusion.",
    "If the verified global H_199 2-coloring exists, classify the triple cut as structurally vacuous and do not run a redundant frontier.",
    "If not, use only the fixed sample before deciding whether a frontier is justified."
  ],
  "failure_rule": [
    "Any forbidden-triple revalidation failure or H_11 oracle mismatch halts this branch.",
    "A search cap or failure to find a coloring proves neither colorability nor non-colorability and authorizes no prune.",
    "A hypergraph-coloring prune must be independently checked against direct r-translate feasibility on every sampled pruned state before promotion.",
    "Do not promote a no-prune result to a no-go for four-way relations or fused cover/lifting."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T15:36:08Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes and active open-conjecture-sweep work; Cycle 5 is sealed and this is a distinct higher-order invariant.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28220063744,"available":178663440384,"reserved":5368709120,"temporary_cap":173294731264,"mount":"/"}
  },
  "input_paths": [
    "artifacts/cycle-5-b005-lrc-packing-cut-v1.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop this invariant after a verified global 2-color saturation certificate, a
small-oracle failure, or the fixed sample gate. Only a positive fixed-sample
utility result can authorize the substantially more expensive frontier run.
