# Cycle 22 / B022 preregistration: targeted width-four deficits

## Decision question and idea selection

Can a width-four block containing the three most gcd-restricted coordinates
convert the 61 Cycle-21 survivors into exact block-deficit certificates?

The primary proposed restricted-coordinate width-four blocks, exhaustive
four-subset search, and a Fourier obstruction. Darwin independently advised
targeted width-four blocks after the exact transfer pass failed, with Fourier
later if incidence signatures become stable. We questioned whether selecting
the most restricted coordinates merely repeats the gcd leaf encoding: that
framing could miss contradictions among unrestricted coordinates. The
countervailing reason is computational and falsifiable—the selected block has
at most 3,528 options in the observed restriction patterns instead of 38,416,
and it is the smallest exact strengthening of the successful width-three
family. Exhaustive 715-subset search is rejected at this stage because it
would spend the cap deeply on a few leaves. The frozen breadth-first family
tests every survivor before deepening.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":22,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: restricted-coordinate width-four blocks, exhaustive four-subsets, or Fourier obstruction. Companion: targeted width four next, Fourier only after stable incidence structure. Choose the ten restricted-coordinate partitions breadth-first; reject all 715 four-subsets because their 14^4 option blocks would consume the cap on a few leaves.","rationale":"Cheapest exact strengthening with full survivor breadth."},
    "targets":{"kind":"expression","value":"Exactly the 61 Cycle-21 results rows with status UNRESOLVED, in frozen table order. Require the other 15 rows to be CERTIFIED_DEFICIT and exact equality with the Cycle-21 artifact counts before execution.","rationale":"No target reselection."},
    "restricted_order":{"kind":"expression","value":"For each target leaf, order coordinates by (number of leaf-allowed digits, coordinate index). Let R be the first three coordinates. Verify allowed digits from the canonical Cycle-16/Cycle-21 mod-2/mod-7 convention. Ties are never broken by coverage or LP output.","rationale":"Frozen gcd-restriction selector only."},
    "partition_family":{"kind":"expression","value":"For each fourth coordinate r outside R, in increasing coordinate order, form the width-four block R union {r}. Split the remaining nine coordinates in increasing order into three consecutive triples. Canonicalize coordinates within blocks and blocks lexicographically. This gives exactly ten partitions per leaf, each with one size-four and three size-three blocks.","rationale":"Small deterministic family with bounded width-four option count."},
    "direct_masks":{"kind":"expression","value":"Use all 2786 original denominator-time clauses 1197..3982 from the target base's frozen Cycle-11 CNF, without deduplicating times. A block option is the exact union of its selected positive choice literals over those clauses.","rationale":"Direct proof interface and unambiguous transferred time weights."},
    "stage_a_transfer":{"kind":"expression","value":"Apply the 15 Cycle-21 certified integer time-weight vectors, in results-table order, to every target partition in frozen order. Interpret clause 1197+t as raw time t. Enumerate every target block option and retain the first exact U<W; resemblance alone proves nothing.","rationale":"Tests the cheapest exact consequence of coarsening blocks."},
    "stage_b_lp":{"kind":"expression","value":"For targets not closed by Stage A, solve the nonnegative time-weight block LP for every frozen partition in breadth-first partition-rank waves across all live leaves. Normalize sum weights=1. Test integerization denominators 4096,65536,1048576,16777216 in order, positive support at most 256, and promote only exact U<W after full target-option enumeration.","rationale":"New weights only after proved weights fail; breadth-first scheduling maximizes leaf coverage."},
    "exhaustive_transfer_continuation":{"kind":"expression","value":"After Stage B produced exactly one proved weight (base 4 leaf 952, support 176, W=65528, U=65440), apply that fixed raw-time weight to all 60 remaining leaves. Enumerate all 715 four-coordinate subsets in lexicographic order; the complement's nine coordinates are split in increasing order into three triples. Cache every block maximum. Compute a block maximum exactly by intersecting option-complement masks over the 176 active times, deduplicating equal masks after each coordinate, and retaining only inclusion-minimal uncovered masks; maximum covered weight is W minus the minimum weighted uncovered mask. Test targets in Stage-B result order and stop each at its first strict U<W.","rationale":"Exhausts the width-four partition choice for the new proved weight without 42,900 repeated LPs or guessed symmetry."},
    "selection":{"kind":"expression","value":"Use CPUs 0-2 and reserve CPU 3. Stage A targets follow frozen row order. Stage B completes rank h for every still-live target before rank h+1. Stop a target at its first exact deficit and retain all statuses. A deadline leaves incomplete rows CAP.","rationale":"Prevents depth-first microcoverage and favorable reselection."},
    "advance_condition":{"kind":"expression","value":"At least one previously unresolved leaf must receive an independently replayed exact width-four deficit. A direct full-cover assignment is a headline falsifier. Zero certificates or caps are implementation outcomes only.","rationale":"Requires new mathematical discrimination."},
    "falsifier":{"kind":"expression","value":"Any target-count, allowed-digit, direct-mask, partition, option-enumeration, weight, W/U, or independent-replay mismatch invalidates the affected result. Any claimed target with U>=W or a surviving direct CNF model is not certified.","rationale":"Exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Certificates concern named canonical leaves only. No partial result closes either base, F_1, J, or LRC(13). Failure does not rule out other width-four blocks, wider blocks, Fourier bounds, or other engines.","rationale":"Strict finite scope."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "target_rows":{"kind":"integer","value":61,"rationale":"Exact Cycle-21 unresolved boundary."},
    "partitions_per_leaf":{"kind":"integer","value":10,"rationale":"One for every fourth coordinate outside the frozen restricted triple."},
    "maximum_block_size":{"kind":"integer","value":4,"rationale":"First strict extension beyond Cycle 21."},
    "transfer_trials":{"kind":"integer","value":9150,"rationale":"At most 61 targets times 10 partitions times 15 proved source weights."},
    "exhaustive_transfer_partitions":{"kind":"integer","value":42900,"rationale":"Exactly 60 targets times all binomial(13,4)=715 partitions."},
    "minimal_uncovered_states_per_block":{"kind":"integer","value":1000000,"rationale":"Hard exact-antichain cap; a capped block yields no target claim."},
    "integer_certificate_support":{"kind":"integer","value":256,"rationale":"Replayable support cap inherited from prior block deficits."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Stage A, breadth-first Stage B, direct audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three sparse LP workers under the observed option bound."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB below available space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Targets, restrictions, partitions, source weights, waves, LP method, denominators, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical gcd-witness leaves","direct Cycle-11 time masks","restricted-coordinate width-four partitions","transferred exact weights","width-four nonnegative deficit LP","all-four-subset exact minimal-uncovered antichains"],
  "selection_rule":["Verify the exact 61-row boundary.","Build exactly ten restricted-coordinate partitions per leaf.","Test all proved source weights before optimization.","Run LPs in breadth-first partition waves.","Apply the one new proved weight to all 715 four-subsets on every remaining leaf.","Promote only fresh direct-clause integer U<W replays."],
  "failure_rule":["Any boundary or construction mismatch halts the branch.","A failed transfer or integerization leaves the target unresolved.","A resource cap retains affected targets as CAP.","No floating result or similarity claim is proof."],
  "pre_execution":{"timestamp_utc":"2026-08-04T00:33:14Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 21 is sealed before this distinct width-four family.","filesystem_observation_bytes":{"size":206900281344,"used":41250848768,"available":165632655360,"reserved":5368709120,"maximum_temporary_cap":160263946240,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "continuation_pre_execution":{"timestamp_utc":"2026-08-04T01:05:26Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","prior_stage":"Stages A/B and the independent direct-CNF audit completed before this same-cycle exhaustive transfer; Stage-B results are now a frozen executable input.","remaining_aggregate_wall_seconds":1975},
  "input_paths":["artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json","discovery/out/cycle21-coupled-incidence/results.tsv","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle8-p199-strata.txt","discovery/out/cycle22-width-four/stage-b-results.tsv","proof/cycle_21_coupled_incidence_soundness.md","proof/cycle_22_width_four_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on an exact construction failure or aggregate cap. After the complete
run, ask Darwin to review the evidence, independently propose next engines,
and advise whether Cycle 22 continues, seals, or yields to a distinct question.
