# Cycle 9 / B009 preregistration: exact weighted-time dual

## Decision question

For a fixed base tuple `v` and first-lift masks `D_{i,d}` at modulus `q=cp`,
can a nonnegative rational time weight certify that no digit choice gives an
improper lift?

\[
y_a\geq0,\qquad \sum_i\max_d\sum_{a\in D_{i,d}}y_a < \sum_a y_a.
\]

Every choice of one lift digit per coordinate that covers all times contradicts
this inequality. The first prototype exhausts raw `(k,p,c)=(3,11,4)` base
tuples; it does not begin p199 work.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 9,
  "parameters": {
    "idea_selection": {"kind":"text","value":"Primary proposal: exact rational weighted-time dual. Independent companion alternatives: saturate P1, CRT-factorized masks, pinned CDCL, and the dual. Rejected now: saturation mistakes a non-discriminating cap for a no-go; CRT needs a separate equivalence prototype; CDCL is unavailable locally and is validation rather than an invariant. Questioning the chosen question: the dual is sufficient only, so its failure is neither a survivor nor a first-lift-fusion failure.","rationale":"Records both agents' ideas, their adversarial comparison, and the central scope hazard."},
    "dual": {"kind":"expression","value":"For each raw l=1-improper base v and coordinate i/digit d, D_{i,d} is its exact denominator-cp bad-time mask. Accept y only when an integer scaling n_a>=0 satisfies sum_i max_d sum_{a in D_{i,d}} n_a < sum_a n_a. This certifies that no one-mask-per-coordinate selection covers all times and hence that v is absent from F_1(k,p,c).","rationale":"The strict integer inequality is independently recheckable and avoids floating-point certificate claims."},
    "prototype": {"kind":"expression","value":"Enumerate every raw base v in (Z_11^times)^3. For every v in I(3,11,1), generate a candidate rational dual by a deterministic exact finite LP/basic-feasible search with numerator/denominator cap 2^20; verify each candidate solely by the integer inequality. Independently compare each certified absence with the complete raw Cycle-8 H11 fiber oracle. On every NO_CERTIFICATE row, exhaust the 4^3 lift choices ignoring the gcd clause: one selected mask cover is an exact falsifier of every nonnegative weighted dual for that base.","rationale":"The 10^3 raw-base instance is exhaustive and the direct mask-cover diagnostic distinguishes a weak optimizer from a structural dual barrier."},
    "advance_condition": {"kind":"expression","value":"Advance only if at least one nonzero accepted exact dual certificate is independently rechecked and no certificate contradicts the raw H11 oracle. A complete certificate family for all raw H11 base covers is proof-grade finite evidence but does not authorize p199; a partial family is an observed design result. No accepted certificate or any mismatch triggers review of a distinct engine.","rationale":"Separates a real dual mechanism from mere solver output."},
    "claim_boundary": {"kind":"expression","value":"This cycle concerns a sufficient weighted-mask inequality on the H11 first-lift prototype. It proves neither that every first-lift UNSAT instance has such a dual nor anything about F_1(13,199,14), J(13,199), or LRC(13).","rationale":"Dual infeasibility is not a mathematical survivor witness."}
  },
  "resource_caps": {
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "h11_raw_bases": {"kind":"integer","value":1000,"rationale":"Exactly (11-1)^3 raw base tuples."},
    "h11_lift_assignments_per_base": {"kind":"integer","value":64,"rationale":"Exactly 4^3 direct raw lift assignments for independent comparison."},
    "dual_numerator_denominator_cap": {"kind":"integer","value":1048576,"rationale":"Bounds exact certificate encoding and prevents post-result coefficient growth."},
    "lp_basis_candidates_per_base": {"kind":"integer","value":100000,"rationale":"A search cap yields NO_CERTIFICATE/CAP, never a negative mathematical claim."},
    "wall_seconds": {"kind":"integer","value":1200,"rationale":"Bounds the complete H11 prototype."},
    "peak_memory_mib": {"kind":"integer","value":2048,"rationale":"The prototype must not materialize broad p199 structures."},
    "temporary_disk_bytes": {"kind":"integer","value":1073741824,"rationale":"Below the measured free-space-minus-5-GiB maximum; only compact certificates and results are permitted."},
    "rng_seed": {"kind":"not_applicable","justification":"Basis ordering and all certificate checks are deterministic.","rationale":"No randomized witness supports a certificate."}
  },
  "formula_families": ["first-lift bad-time masks D_{i,d}", "nonnegative weighted cover dual", "integer-scaled strict certificate inequality", "raw H11 direct first-lift oracle", "raw H11 mask-cover dual falsifier"],
  "selection_rule": ["Write the weighted-dual soundness proof before executable work.", "Run the complete H11 direct fiber oracle and exact certificate verifier before accepting any LP/search output.", "A candidate is promoted only after integer recheck of nonnegativity, strict margin, mask conventions, and the direct raw H11 comparison.", "For every NO_CERTIFICATE row, run the exact 4^3 mask-cover diagnostic before interpreting it as a dual barrier.", "Do not run p47, p199, CRT factorization, or any CDCL backend in this cycle without a separate material decision."],
  "failure_rule": ["A malformed certificate, non-strict margin, sign/mask mismatch, or disagreement with the raw H11 oracle halts the affected dual claim.", "NO_CERTIFICATE, a basis cap, or an LP failure means only that this frozen search did not find the sufficient dual; it does not retain or prove a lifted tuple.", "Do not infer dual completeness, p199 behavior, J-empty, or LRC from the H11 prototype."],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T16:58:29Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent work; Cycle 8 is sealed before this distinct weighted-dual engine.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28233363456,"available":178650140672,"reserved":5368709120,"maximum_temporary_cap":173281431552,"chosen_temporary_cap":1073741824,"mount":"/"}
  },
  "input_paths": ["artifacts/cycle-8-b008-lrc-fused-lift-v1.json", "proof/cycle_8_fused_lift_soundness.md", "proof/cycle_9_weighted_dual_soundness.md", "../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop the prototype at the frozen H11 basis cap or any exactness failure. A
complete H11 dual family or a non-discriminating no-certificate result goes to
a material co-planning review before another engine or larger instance.
