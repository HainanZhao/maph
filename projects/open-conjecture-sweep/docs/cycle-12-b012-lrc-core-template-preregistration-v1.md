# Cycle 12 / B012 preregistration: checked core templates

## Decision question and idea selection

Do the sealed p199 contradictions contain a reusable UNSAT subformula which,
after intrinsic residue normalization and coordinate permutation, certifies
new base fibers outside the Cycle-11 sample?

The primary ideas were verifier-only completion, checked-core invariants, an
exact CRT prototype, and stopping Problem 1.  Darwin independently proposed a
core-template/interpolation engine, verifier-only completion, and CRT as a
fallback.  We questioned whether “recurring cores” would be only a solver
artifact; the selected question therefore requires literal-level containment
of a certified UNSAT core in a new CNF, not statistical similarity.  CRT is
rejected for this cycle because it still lacks an exact cross-factor bridge,
and a raw 4,748,938-orbit SAT census is rejected because it spends computation
without extracting a reusable mechanism.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":12,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: checked-core invariant, CRT prototype, or stop after verifier completion. Companion: core-template/interpolation, verifier completion, and CRT fallback. Choose exact core containment because it can prove new fibers without raw solving. Reject statistical-only clustering, raw full census, and CRT before equivalence.","rationale":"Records independent proposals and challenges solver-artifact framing."},
    "core_extraction":{"kind":"expression","value":"Run pinned drat-trim with -c on each of the 100 sealed p199 CNF/proof pairs. Accept a core only if its clauses form a multiset subset of the source CNF and the core receives a fresh VERIFIED proof/check result.","rationale":"An extracted core must be an independently certified unsatisfiable subformula."},
    "normalization":{"kind":"expression","value":"Rename x(i,d) to x(i,s), s=v_i+199d mod 14; retain y(r,i). A template map is a coordinate permutation pi with x(i,s)->x(pi(i),s) and y(r,i)->y(r,pi(i)), preserving signs and clause multiplicities.","rationale":"The residue label is intrinsic and preserves the exact gcd channels."},
    "split":{"kind":"expression","value":"Within each of the 10 Cycle-8 strata, rows at offsets 0..7 are training (80 total) and offsets 8..9 are validation (20 total). External targets are census indices stratum*4748938//10 + offsets 10..19 (100 total), disjoint from Cycle 11.","rationale":"Freezes discovery, validation, and new-target sets before extraction."},
    "selection":{"kind":"expression","value":"Extract one certified core per training row. For each core, count exact embeddings into the 20 validation CNFs. Select maximum validation coverage; tie by fewer core clauses, then lexicographic core SHA-256. Evaluate only that selected template on the 100 external targets.","rationale":"Prevents post-result template cherry-picking on external bases."},
    "continuation":{"kind":"expression","value":"The whole-core evaluation returned zero validation matches for every training core. Continue in the same cycle with the already selected row-76 core: scan its 302 clauses in original order and greedily delete a clause exactly when the resulting formula receives a fresh CaDiCaL UNSAT result and drat-trim VERIFIED proof. SAT, timeout, or failed proof retains the clause. Freshly certify the final subcore, then rerun the identical 20-validation and 100-external exact embedding tests; do not select another source row.","rationale":"Deletion shrinking tests the same frozen core-reuse question without post-result target selection."},
    "advance_condition":{"kind":"expression","value":"An exact embedding into at least one validation CNF establishes recurrence; an exact embedding into at least one external target proves a new first-lift fiber UNSAT. Literal-level mapped-clause containment plus the certified source core is the proof. No embedding or timeout is a method failure only.","rationale":"Requires a reusable, proof-bearing result outside the training corpus."},
    "falsifier":{"kind":"expression","value":"A core clause absent from its source, a core proof rejection, a mapped clause absent from a claimed target, a non-bijective coordinate map, or a directly checked SAT lift for a claimed target invalidates the affected template claim.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Only named matched base fibers are excluded. Clustering scores, refinement hashes, and failure to match are OBSERVED; no density, universal template, F_1 emptiness, J emptiness, or LRC claim follows.","rationale":"Prevents structural search overclaim."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2; reserve CPU 3."},
    "training_cores":{"kind":"integer","value":80,"rationale":"Frozen 8-per-stratum training split."},
    "validation_targets":{"kind":"integer","value":20,"rationale":"Frozen 2-per-stratum validation split."},
    "external_targets":{"kind":"integer","value":100,"rationale":"Frozen disjoint 10-per-stratum target set."},
    "coordinate_permutations":{"kind":"integer","value":6227020800,"rationale":"Logical maximum 13!; exact backtracking must stop at the aggregate cap and need not enumerate all permutations."},
    "mus_candidate_deletions":{"kind":"integer","value":302,"rationale":"Exactly one original-order pass over the frozen selected core."},
    "mus_wall_seconds":{"kind":"integer","value":240,"rationale":"Leaves time for the frozen continuation embedding search."},
    "continuation_embedding_wall_seconds":{"kind":"integer","value":360,"rationale":"Keeps total Cycle-12 wall below the aggregate cap."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Core extraction, certification, embedding, and exact checks combined."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"At most three checker/search processes."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Splits, ties, extraction, and embedding search are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["DRAT-extracted input cores","lifted-residue variable normalization","coordinate-block permutation","exact mapped-clause multiset containment","held-out fiber exclusion"],
  "selection_rule":["Verify every extracted core before clustering.","Use only the frozen 80 training rows to propose templates.","Select by frozen validation coverage and ties before inspecting external embeddings.","After the frozen whole-core zero-match result, shrink only selected row 76 by one original-order certified deletion pass.","Rerun the identical validation and external sets on the certified final subcore.","Accept an external exclusion only after exact mapped-clause containment and independent direct/CNF consistency checks.","Do not run a full-census SAT sweep."],
  "failure_rule":["Any source-core or proof mismatch halts that core.","A heuristic hash collision without exact embedding is no match.","Timeout or no external embedding closes only this template family, not Problem 1.","No resource continuation creates a new cycle while this exact template question remains live."],
  "pre_execution":{"timestamp_utc":"2026-08-03T18:21:41Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 11 is sealed before this distinct structural engine.","filesystem_observation_bytes":{"size":206900281344,"used":31128240128,"available":175755264000,"reserved":5368709120,"maximum_temporary_cap":170386554880,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-11-b011-lrc-certified-sat-v1.json","discovery/out/cycle11-certified-sat/controls.tsv","discovery/out/cycle11-certified-sat/p199.tsv","discovery/out/cycle8-p199-strata.txt","discovery/out/k13-p199.txt","proof/cycle_12_core_template_soundness.md","discovery/vendor/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f.tar.gz","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a core-certification failure or aggregate cap.  After the frozen
external evaluation, obtain a material companion review before sealing,
changing engines, or declaring Problem 1 saturated.
