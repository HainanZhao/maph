# Cycle 28 / B028 preregistration: portfolio-selected cyclic width-five LP

## Decision question and idea selection

For the frozen 60 Cycle-25 survivors, does an exact four-witness portfolio
select a genuinely different cyclic (5+4+4) coordinate geometry and then
yield a fresh direct-CNF integer deficit under the frozen time-weight LP and
integerization rule?  The adversarial comparison and rejected alternatives are
in `discovery/cycle28_width_five_partition_idea_selection.md`.  The selected
engine changes the geometry before optimization; rational fixed-geometry
diagnostics, semantic lifts without equivalence, and further class refinements
are not this cycle's question.

## Live-cycle amendment: optimized continuation

The first 3,602.374346-second tranche completed the source controls and all
60 exact selections (all nonbaseline), then fully separated 25 target LPs and
left 35 `CAP` rows. Its output is retained as `*-tranche1.*`. The decision
question and formula family are unchanged. Before this continuation, the LP
separator is changed only to return its maximum, lexicographic option, and
mask in one streamed pass instead of enumerating the same option set twice.
The aggregate budget rises to 7,200 seconds; the continuation executable is
limited to 3,500 seconds, leaving room for validation. This is a same-cycle
optimization/resource continuation, not a new method or cycle.

## Live-cycle amendment: independent closure audit

The optimized continuation completed all 60 rows in 1,818.948502 seconds and
left every row `UNRESOLVED`.  No further selector or LP search is authorized.
One separately written closure audit will recompute the four source controls,
all thirteen exact portfolio scores/ties per target, and every final LP's full
separator. Its initial 5,679.31-second attempt did not persist a result or
error marker, so it is retained as an inconclusive audit tranche. The
resumable replay must persist either a `PASS` payload or precise failure
diagnostic. It receives a 6,500-second executable allowance under a 20,000-
second cumulative cycle cap. This is verification of the completed finite
family, not a new engine.

## Live-cycle amendment: row-local mismatch diagnosis

The resumable full audit completed in 5,721.16 seconds and persisted `FAIL: LP
mismatch`. Because the selector comparison passed before the LP phase, the
failure is confined to one or more independently replayed floating LP rows,
but the audit retained no row-local values. The failed payload and timing are
preserved as `independent-replay-error-tranche2.json` and
`independent-replay-tranche2.time`. Before further execution, a diagnostic
continuation will use the same independent LP implementation, compare rows as
workers finish, atomically persist every row's observed objective/round/cut
triple and comparison classification, and stop at the first mismatch or its
2,700-second allowance. Previously persisted exact matches may be reused on
continuation. The cumulative cycle cap remains 20,000 seconds; this is
diagnosis of the failed closure audit, not a fresh selector or LP engine.

## Live-cycle amendment: thread-environment classification control

The row-local diagnostic stopped after 2,625.731264 seconds at base 3 / leaf
91: both implementations returned objective `1`, but the primary trace had
28 rounds and 80 cuts while the independent trace had 26 rounds and 74 cuts.
The solver and separator formulas are semantically identical; the primary
sets `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` before importing NumPy,
while the independent audit did not. One targeted replay of this named row is
authorized under those two one-thread environment settings, with a 300-second
wall allowance. It is a classification control only. Agreement with 28/80
attributes the trace mismatch to an unpinned numerical execution path;
continued 26/74 leaves the precise cause open. Either way, the failed audit is
preserved and no exact LP lower-bound claim may be promoted.

<!-- research-freeze-v1
{"schema":"research-preregistration-freeze-v1","cycle":28,
"parameters":{"portfolio":{"kind":"expression","value":"Exactly four raw-time integer witnesses: Cycle-22 (base 4, leaf 952, W=65528, U=65440) and Cycle-21 (base 4, leaf 83, W=4091, U=4090), (base 4, leaf 104, W=65539, U=65448), (base 3, leaf 94, W=4107, U=4080). Extract their frozen source clauses and positive weights, and exactly replay each stated source capacity on its stated source partition before target work.","rationale":"A small certified portfolio reduces the known single-witness selection bias without adaptive source choice."},"targets":{"kind":"expression","value":"Exactly the 60 Cycle-25 results in frozen order, all UNRESOLVED.","rationale":"No target reselection."},"candidate_partitions":{"kind":"expression","value":"For r=0,...,12, apply i -> (i+r) mod 13 to baseline blocks (0,1,2,3,4), (5,6,7,8), (9,10,11,12); sort coordinates within blocks and sort blocks lexicographically. Require exactly 13 distinct disjoint 5+4+4 partitions.","rationale":"A small, exhaustive, partition-changing family."},"selector":{"kind":"expression","value":"For each target and candidate partition P, compute exact direct capacities U_j(P) for all four frozen weights and minimize the exact rational score S(P)=sum_j U_j(P)/W_j. Select the lexicographically first minimum. If every selected P is the Cycle-27 partition, emit CONTAINED and do not run target LPs.","rationale":"The inherited portfolio determines geometry before any fresh floating optimization."},"lp":{"kind":"expression","value":"For each selected distinct target geometry, minimize sum_B q_B over raw-time w_t>=0 and q_B>=0, normalized by sum_t w_t=1, with every block-option inequality sum_(t covered by option)w_t<=q_B. Start with lexicographically first options; at each round exhaustively enumerate every option and add the lexicographically first maximum violation exceeding 1e-9. Stop after 512 rounds. Stream the complete maximum search: at most a three-coordinate prefix of 2744 Boolean rows, streamed penultimate suffixes, and a final 14-way vectorized batch of at most 38416 rows.","rationale":"Fresh optimizer, complete finite separator, bounded memory."},"integerization":{"kind":"expression","value":"Only after a fully separated LP objective below 1-1e-9, round at denominators 4096,65536,1048576,16777216 in order; require positive support <=256; recompute every option exactly and promote only U<W.","rationale":"Floating LP output never closes a leaf."},"advance_condition":{"kind":"expression","value":"One independently replayed fresh direct-CNF integer U<W deficit on a named survivor selected by a nonbaseline cyclic geometry.","rationale":"Exact advancement only."},"falsifier":{"kind":"expression","value":"Any portfolio extraction/source replay, candidate census, rational score/tie, target boundary, partition, LP separation, integerization, or direct U/W mismatch invalidates the affected claim.","rationale":"Specific contrary evidence."},"claim_boundary":{"kind":"expression","value":"A contained, cap, or all-unresolved outcome concerns this four-witness portfolio, 13 cyclic partitions, one selected geometry per target, and one direct time-weight LP. It is not a width-five, primal-lift, character-dual, or LRC no-go.","rationale":"Finite scope."}},
"resource_caps":{"worker_processes":{"kind":"integer","value":3,"rationale":"CPUs 0-2; reserve CPU 3."},"target_rows":{"kind":"integer","value":60,"rationale":"Frozen survivor boundary."},"portfolio_witnesses":{"kind":"integer","value":4,"rationale":"Frozen source diversity."},"candidate_partitions_per_target":{"kind":"integer","value":13,"rationale":"All cyclic shifts."},"target_lp_rounds":{"kind":"integer","value":512,"rationale":"Bounded full separation."},"maximum_options_per_block":{"kind":"integer","value":537824,"rationale":"At most 14^5 direct choices."},"separation_batch_options":{"kind":"integer","value":38416,"rationale":"At most 14^4 temporary Boolean states."},"integer_certificate_support":{"kind":"integer","value":256,"rationale":"Frozen direct replay bound."},"integerization_denominators":{"kind":"expression","value":"4096,65536,1048576,16777216","rationale":"Finite conversion rule."},"aggregate_wall_seconds":{"kind":"integer","value":20000,"rationale":"All measured execution, failed-audit, row-diagnostic, classification-control, and test tranches."},"continuation_execution_wall_seconds":{"kind":"integer","value":3500,"rationale":"Optimized continuation allowance after the measured first tranche."},"independent_audit_wall_seconds":{"kind":"integer","value":6500,"rationale":"Resumable full independent source, selector, and LP-separation replay allowance."},"mismatch_diagnostic_wall_seconds":{"kind":"integer","value":2700,"rationale":"Row-local continuation of the failed full audit within the unchanged cumulative cycle cap."},"thread_classification_wall_seconds":{"kind":"integer","value":300,"rationale":"One named-row replay under the primary one-thread environment."},"aggregate_peak_memory_mib":{"kind":"integer","value":6144,"rationale":"Three streamed workers must remain safely below the host limit."},"aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB below measured available space minus the required 5 GiB reserve."},"rng_seed":{"kind":"not_applicable","justification":"Rows, sources, partitions, scores, options, cuts, and ties are deterministic.","rationale":"No randomness."}},
"formula_families":["Cycle-11 direct denominator-time masks","exact integer direct capacity","exact rational portfolio selector","deterministic cutting-plane separation","cyclic 5+4+4 partitions"],"selection_rule":["Replay the four source witnesses exactly.","Enumerate all 13 cyclic partitions per frozen target.","Select only by the frozen exact rational portfolio score and lexicographic tie.","For continuation, validate and reuse the complete frozen first-tranche selection census and rerun only its CAP LP rows.","For closure, independently recompute every source, selector score/tie, and final LP separator.","After the coarse LP mismatch, persist and compare each independent row as it completes; stop on the first row-local mismatch and reuse only persisted exact matches on continuation.","Replay only base 3 / leaf 91 under OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1 to classify the trace mismatch.","Require at least one nonbaseline selection before any fresh target LP.","Promote only fresh integer direct U<W replays."],"failure_rule":["A source or candidate-census mismatch halts the branch.","All-baseline selection is CONTAINED, not a new engine result; do not run LPs.","A target round cap or shared aggregate deadline is CAP, not a conclusion.","A row-local objective, round, or cut mismatch is a failed independent audit and blocks strong closure; the named thread control may classify but never erase it.","A non-strict or floating result is UNRESOLVED.","No failed row is dropped."],"pre_execution":{"timestamp_utc":"2026-08-04T07:35:33Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated root work; Cycle 27 fixed-geometry boundary and its metadata correction are sealed before this distinct selector.","filesystem_observation_bytes":{"size":206900281344,"used":45277691904,"available":161605812224,"reserved":5368709120,"maximum_temporary_cap":156237103104,"chosen_temporary_cap":21474836480,"mount":"/"}},"input_paths":["artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json","artifacts/cycle-22-b022-lrc-width-four-v1.json","artifacts/cycle-25-b025-lrc-quadratic-crt-v1.json","artifacts/cycle-27-b027-lrc-width-five-lp-v2.json","discovery/cycle28_width_five_partition_idea_selection.md","discovery/out/cycle21-coupled-incidence/results.tsv","discovery/out/cycle22-width-four/stage-b-results.tsv","discovery/out/cycle25-quadratic-crt/results.tsv","discovery/lrc_coupled_incidence.py","discovery/lrc_pair_choice.py","discovery/lrc_width_four_stage_a.py","discovery/out/cycle28-portfolio-cyclic-width-five/selection-tranche1.tsv","discovery/out/cycle28-portfolio-cyclic-width-five/results-tranche1.tsv","discovery/out/cycle28-portfolio-cyclic-width-five/result-tranche1.txt","discovery/out/cycle28-portfolio-cyclic-width-five/run-tranche1.time","discovery/out/cycle28-portfolio-cyclic-width-five/selection.tsv","discovery/out/cycle28-portfolio-cyclic-width-five/results.tsv","discovery/out/cycle28-portfolio-cyclic-width-five/result.txt","discovery/out/cycle28-portfolio-cyclic-width-five/run-tranche2.time","../../tools/preregistration_check.py"]}
-->

## Stop rule

Stop after four source controls, the complete selector census, an all-baseline
containment, the complete selected-geometry family, a control failure, or the
aggregate cap.  Any candidate deficit requires an independent direct replay
before promotion.
