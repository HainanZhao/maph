# Cycle 8 / B008 preregistration: fused initial-cover and first necessary lift

## Decision question

For fixed `(k,p,c)`, define the published lift-aware upper bound

\[
F(k,p,c):=\pi_{cp\to p} I(k,p,c).
\]

The published lifting proposition applies to the intersection with its parent
set.  Accordingly the fused survivor set is
\[
 F_1(k,p,c):=\pi_{cp\to p}\left(\pi_{cp\to p}^{-1}I(k,p,1)\cap I(k,p,c)\right),
\]
and satisfies `J(k,p) subseteq F_1(k,p,c)`. This cycle asks whether a fused
exact enumerator can emit only representatives in `F_1(k,p,c)`, rather than
materializing all of `I(k,p,1)`, while preserving that inclusion. It tests the
first necessary multiplier `c=k+1`: `(k,p,c)=(3,11,4)`
as a complete raw oracle and `(6,47,7)` as the smallest frozen nontrivial
control. After the material checkpoint passed, the same live question may run
only the frozen 100-orbit `(13,199,14)` solver sample below; this remains not a
frontier run.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 8,
  "parameters": {
    "lift_aware_set": {"kind":"expression","value":"F(k,p,c)=pi_{cp->p} I(k,p,c) is the broad projected lift set. The executable survivor set is F_1(k,p,c)=pi_{cp->p}(pi_{cp->p}^{-1}I(k,p,1) intersect I(k,p,c)). Here I(k,p,c) is Definition 2.1 improperness: no witness a/(cp) and no gcd(c,w_1,...,w_{i-1},w_{i+1},...,w_k)>1. Proposition 3.1 of Sungkawichai--Trakulthongchai gives J(k,p) subseteq F_1(k,p,c).","rationale":"This is the exact published retained-path interface; it retains the parent intersection required by Proposition 3.1."},
    "fused_algorithm": {"kind":"expression","value":"Enumerate a base tuple only through the l=1 bad-time-cover construction. At a completed base cover v, enumerate its c^k fiber w=v+p*d (0<=d_i<c), retain v exactly when at least one w is (k,p,c)-improper, and otherwise emit nothing. The output is exactly F_1 and is canonicalized only after its exact fiber decision.","rationale":"The algorithm fuses emission with the first necessary lift and never serializes rejected l=1 representatives."},
    "orbit_invariant": {"kind":"expression","value":"F_1(k,p,c) is invariant under coordinate permutations, coordinate signs modulo p, and common multiplication by a unit modulo p. For common multiplication choose its CRT lift b congruent to a (mod p), b congruent to 1 (mod c); b is a unit modulo cp and carries witness/gcd properness bijectively. Thus an orbit representative is retained iff its orbit meets F_1.","rationale":"This permits the p47 control to use the already verified canonical l=1 representatives without losing a projected survivor orbit."},
    "oracle": {"kind":"expression","value":"For k=3,p=11,c=4, independently enumerate every raw w in (Z_{44} minus 11Z_4)^3, test improperness directly over all 44 rational times and the gcd clause, retain its base projection only if that base lies in I(3,11,1), and compare the resulting raw F_1 set to the fused cover-plus-fiber output. For k=6,p=47,c=7, independently recheck every retained fiber witness/certificate and compare the fused input representatives byte-for-byte with the sealed 53-row Cycle-4 p47 baseline.","rationale":"The first control proves the fused retained-path identity on a complete finite instance; the second tests the full first-necessary-lift shape on the existing exact baseline."},
    "idea_selection": {"kind":"text","value":"Considered: (A) direct 14^13 fiber enumeration, exact but infeasible; (B) a depth-8 partial-state relaxation, cheaper but not a real completed base orbit; (C) exact multiple-choice mask-cover search on completed stored p199 l=1 orbits. Chosen C. Questioning the question: p47 can be vacuous because LRC(6) is known, so only actual p199 base orbits probe viability; a capped solver must classify CAP/retain, never absence of an improper lift.","rationale":"Records the required brainstorm, adversarial framing check, rejected alternative, and why the next action stays in this live cycle."},
    "p199_sample": {"kind":"expression","value":"Select exactly ten lexicographically indexed completed representatives from each of ten equal-size index strata of the frozen 4,748,938-row Cycle-1 p199 census: index floor(j*N/10)+r for j=0,...,9 and r=0,...,9. For each base v, solve exactly whether some d in {0,...,13}^13 makes w=v+199d (13,199,14)-improper. Encode each coordinate digit as an exactly-one 14-choice variable and every lifted time as a cover clause. First test deterministic greedy digit assignments solely for directly checked SAT witnesses; then use exact branch-and-bound with a minimum-option choice among the first 128 currently uncovered times and the sound sum-of-per-unassigned-coordinate maximum-new-coverage upper bound. It may certify UNSAT, emit a directly rechecked SAT digit witness, or return CAP. CAP retains v and is not an UNSAT result.","rationale":"This uses completed actual I(13,199,1) orbits and transforms the 14^13 Cartesian product into a falsifiable exact multi-choice-cover problem without treating a heuristic as a prune."},
    "advance_condition": {"kind":"expression","value":"Advance only if the raw H11 oracle agrees exactly, the p47 input remains byte-identical, all retained p47 outputs independently recheck, and the fused p47 output is strictly smaller than 53 orbit representatives. Otherwise the result is a bounded no-go for this direct first-lift fusion, not a statement about other representations or LRC(13).","rationale":"A strict finite reduction is necessary before this engine can justify a larger construction."},
    "claim_boundary": {"kind":"expression","value":"Any result proves only exact finite equality/projection facts for the frozen controls and observed reduction counts. It does not prove F(13,199,14) empty, J(13,199) empty, LRC(13), or that a different fusion/lifting representation cannot work.","rationale":"The first lift is merely a retained-path upper bound on J."}
  },
  "resource_caps": {
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use CPUs 0-2; CPU 3 remains reserved for the system and the user-directed existing process."},
    "h11_raw_lifts": {"kind":"integer","value":64000,"rationale":"Exactly (11-1)^3*4^3 raw tuples in the complete H11 oracle."},
    "p47_base_orbits": {"kind":"integer","value":53,"rationale":"The sealed Cycle-4 canonical k6,p47 input count."},
    "p47_lifts_per_orbit": {"kind":"integer","value":117649,"rationale":"Exactly 7^6 fibers per canonical representative."},
    "p199_sample_orbits": {"kind":"integer","value":100,"rationale":"Ten deterministic representatives in each of ten equal index strata."},
    "p199_nodes_per_orbit": {"kind":"integer","value":1000000,"rationale":"A cap returns CAP/retain, preventing unbounded search from being reclassified as UNSAT."},
    "p199_wall_seconds_per_orbit": {"kind":"integer","value":30,"rationale":"Bounds a single exact CSP attempt while preserving safe CAP semantics."},
    "wall_seconds": {"kind":"integer","value":1200,"rationale":"Aggregate bound for controls plus only the frozen p199 sample; no frontier run is authorized."},
    "peak_memory_mib": {"kind":"integer","value":2048,"rationale":"The direct product masks need constant working memory; this prevents accidental fiber materialization."},
    "temporary_disk_bytes": {"kind":"integer","value":1073741824,"rationale":"The cap is below the measured free-space-minus-5-GiB maximum and only permits compact deterministic output/check files."},
    "rng_seed": {"kind":"not_applicable","justification":"All covers, fibers, and raw oracle loops are deterministic.","rationale":"No randomized selection may affect the retained set."}
  },
  "formula_families": [
    "Definition-2.1 improperness in the (k,p,c)-ansatz",
    "exact l=1 bad-time cyclic cover enumeration",
    "parent-intersected fiber projection F_1(k,p,c)",
    "CRT-lifted orbit invariance",
    "complete raw H11 projection oracle",
    "exact multiple-choice lifted-mask cover CSP with CAP/retain semantics"
  ],
  "selection_rule": [
    "Write the retained-path and orbit-invariance argument before executable work.",
    "Pass exact raw H11 equality before the p47 control.",
    "Use the sealed 53-row Cycle-4 p47 tuple file as input and independently recheck every claimed retained p47 orbit by an explicit improper fiber.",
    "If all controls pass and the p47 retained count is strictly below 53, request the mandatory material companion review before deciding whether the live cycle expands to a small p199 sample or opens another cycle.",
    "The received companion recommendation continues this live cycle with the stated 100-orbit p199 sample only; no p199 frontier or extra sample is authorized.",
    "After every SAT result, recompute its lifted tuple directly; after every UNSAT result, replay the deterministic complete search. CAP rows remain in the output as unresolved retained orbits.",
    "At the sample checkpoint, a material companion review decides whether this same engine has evidence for a further live continuation, seals as a bounded result, or requires a distinct cycle."
  ],
  "failure_rule": [
    "Any mismatch between fused and raw H11 projections, any invalid fiber certificate, or any Cycle-4 input mismatch halts the branch and withholds all projection claims.",
    "A resource cap or code error retains rather than rejects any base tuple and is not evidence of properness.",
    "The only p199/c=14 computation authorized is the stated 100-orbit capped sample; any frontier, changed sample, or uncapped method requires a further live-preregistration amendment and material review.",
    "Do not infer that F equals J, that all l=1 covers have been eliminated, or that LRC(13) follows from a control reduction."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T16:29:57Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent work; Cycle 7 is sealed and its companion explicitly recommended the distinct fused cover/lifting question.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28232527872,"available":178650976256,"reserved":5368709120,"maximum_temporary_cap":173282267136,"chosen_temporary_cap":1073741824,"mount":"/"}
  },
  "input_paths": [
    "artifacts/cycle-7-b007-lrc-direct-feasibility-v1.json",
    "artifacts/cycle-4-b004-lrc-partitioned-v2.json",
    "discovery/out/partitioned-k6.txt",
    "discovery/out/k13-p199.txt",
    "proof/cycle_8_fused_lift_soundness.md",
    "proof/cycle_8_p199_multichoice_soundness.md",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

This cycle stops on any exactness failure, or after the p47 control if it does
not yield a strict orbit-level reduction.  A successful reduction requires a
material companion review before any larger test or cycle boundary decision.
