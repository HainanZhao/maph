# Cycle 23 / B023 preregistration: adaptive width-four partition oracle

## Decision question and idea selection

Can exact pair-overlap savings select width-four partitions that yield strict
integer deficits on the 60 Cycle-22 survivors, including contradictions missed
by the three-most-restricted-coordinate policy?

The primary proposed an exact pair-savings partition oracle, width-five
restricted blocks, and a Fourier-character obstruction. Darwin independently
recommended adaptive width-four column generation before Fourier analysis. We
questioned whether pairwise savings can see a genuinely four-way obstruction;
it need not, and its score is never evidence. It is selected because all 78
pair maxima are cheap, the global partition optimization is exact, and one
reselection tests whether the score responds to a leaf-specific LP weight.
Width five is rejected until width-four selection—not merely width—has been
tested, and Fourier remains the next structurally distinct fallback.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":23,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: exact pair-savings partition oracle, restricted width five, or Fourier obstruction. Companion: adaptive width-four column generation next, Fourier later. Choose pair-savings width four with one reselection; reject width five until selection bias is tested and treat the score as discovery only.","rationale":"Low-cost adaptive test of the identified Cycle-22 flaw."},
    "targets":{"kind":"expression","value":"Exactly the 60 Cycle-22 Stage-B rows with status UNRESOLVED, in frozen table order. Require exactly one CERTIFIED_DEFICIT row (base 4 leaf 952) and exact agreement with the Cycle-22 artifact before execution.","rationale":"No target reselection."},
    "initial_weight":{"kind":"expression","value":"Use exactly the base-4 leaf-952 integer weight from the frozen Cycle-22 Stage-B result, interpreting clause 1197+t as raw time t. Require support 176, W=65528, U=65440, margin 88 before use.","rationale":"Only new proved width-four weight, frozen before Cycle 23."},
    "pair_savings":{"kind":"expression","value":"On the target's original direct CNF and canonical allowed digits, compute M_i=max covered weight for every singleton and M_ij=max union-covered weight for every pair. Set s_ij=M_i+M_j-M_ij exactly. No floating value enters this score.","rationale":"Exact overlap signal under the current weight."},
    "partition_oracle":{"kind":"expression","value":"Enumerate every set partition of coordinates 0..12 into exactly one block of size 4 and three unordered blocks of size 3. Score a partition by the sum of s_ij over every coordinate pair within a common block. Choose maximum score; break ties by lexicographic canonical block tuple. There are 715 choices of the four-block and 280 triple partitions of its complement, 200200 candidates per leaf.","rationale":"Removes the prior forced-locality policy with an exact global selector."},
    "wave_zero":{"kind":"expression","value":"Apply the frozen initial weight to the oracle-selected partition and enumerate all target block options exactly. Promote immediately only if integer U<W; otherwise solve the nonnegative time-weight LP for that partition using all 2786 raw times.","rationale":"Tests a cheap exact transfer before optimization."},
    "wave_one":{"kind":"expression","value":"For a target not certified in wave zero, parse the 17-significant-digit binary64 LP vector; require every entry at least -1e-12 and the sum within 1e-12 of one, clip only entries in [-1e-12,0), and renormalize. Then exhaustively recompute singleton and pair maxima in deterministic IEEE-754 binary64 arithmetic, set the floating pair score from those maxima, select the oracle partition again, and solve one final LP only if the partition differs. The floating weight and score select only; exact integer arithmetic remains required for promotion. No target receives more than two LPs total.","rationale":"One bounded adaptive column-generation step; the deterministic parsing rule contains observed sub-4e-14 solver roundoff before its first successful wave-one execution."},
    "lp_and_integerization":{"kind":"expression","value":"Normalize nonnegative weights to sum one. Solve the identical all-option LP by deterministic cutting planes: begin with the lexicographically first option of each block, solve, then exactly enumerate every option in each block under the floating weight and add the lexicographically first maximizer for every violation above 1e-9. At most 512 separation rounds are allowed; a nonconvergent round is CAP, not a result. For each solved LP with objective below 1-1e-9, test denominators 4096,65536,1048576,16777216 in order, retain positive support at most 256, and promote only after full exact target-option enumeration gives U<W.","rationale":"The original explicit sparse matrix made one target use 8.65 GiB and was OOM-killed at three workers. Exact separation implements the same LP while enforcing the aggregate memory cap."},
    "selection":{"kind":"expression","value":"Use CPUs 0-2 and reserve CPU 3. Process all targets through initial selection/transfer and LP wave zero before adaptive wave one. Preserve target order, oracle score, selected partition, LP status/objective, integerization outcome, and all caps.","rationale":"Breadth before adaptive depth."},
    "advance_condition":{"kind":"expression","value":"At least one of the 60 survivors receives an independently replayed exact integer deficit. A direct full-cover assignment is a headline falsifier. Selection changes or lower floating objectives alone do not advance.","rationale":"Requires new proved leaf discrimination."},
    "falsifier":{"kind":"expression","value":"Any target, initial-weight, allowed-digit, direct-mask, singleton/pair maximum, candidate census, score, tie, partition, LP, integerization, W/U, or independent-replay mismatch invalidates the affected result. U>=W never certifies.","rationale":"Exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Every certificate concerns one named canonical leaf. Failure or caps do not rule out other width-four selectors, more adaptive waves, width five, Fourier methods, either base, F_1, J, or LRC(13).","rationale":"Strict finite scope."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "target_rows":{"kind":"integer","value":60,"rationale":"Exact Cycle-22 unresolved boundary."},
    "partition_candidates_per_oracle":{"kind":"integer","value":200200,"rationale":"715 four-blocks times 280 complementary triple partitions."},
    "pair_maxima_per_oracle":{"kind":"integer","value":78,"rationale":"13 singletons and 78 pairs are computed; pair score uses the 78 pairs."},
    "adaptive_reselections":{"kind":"integer","value":1,"rationale":"One bounded response to the target-specific LP weight."},
    "lp_solves_per_leaf":{"kind":"integer","value":2,"rationale":"Initial selected partition plus at most one distinct reselection."},
    "integer_certificate_support":{"kind":"integer","value":256,"rationale":"Exact replay support cap."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Both breadth-first waves, direct audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three sparse arbitrary width-four LP workers."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB below free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Targets, weights, maxima, candidate partitions, scores, ties, LP method, denominators, and order are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical gcd-witness leaves","direct Cycle-11 raw-time masks","exact pair-overlap savings","global one-four-plus-three-triples partition oracle","two-wave adaptive width-four deficit LP"],
  "selection_rule":["Verify the 60-row boundary and initial weight.","Compute exact pair savings.","Select the unique frozen-tie oracle optimum.","Test exact transfer before LP.","Run wave zero across all targets.","Permit one distinct adaptive reselection in wave one.","Promote only independent direct-CNF integer deficits."],
  "failure_rule":["Any boundary or oracle mismatch halts the branch.","A failed transfer, LP, or integerization remains unresolved.","A resource cap preserves affected targets as CAP.","No score or floating result is proof."],
  "pre_execution":{"timestamp_utc":"2026-08-04T01:41:54Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 22 is sealed before this distinct adaptive selector.","filesystem_observation_bytes":{"size":206900281344,"used":41251762176,"available":165631741952,"reserved":5368709120,"maximum_temporary_cap":160263032832,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-22-b022-lrc-width-four-v1.json","discovery/out/cycle22-width-four/stage-b-results.tsv","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle8-p199-strata.txt","discovery/lrc_adaptive_width_four_oracle.py","discovery/lrc_adaptive_width_four_wave0.py","discovery/lrc_adaptive_width_four_wave1.py","discovery/out/cycle23-adaptive-width-four/oracle.tsv","discovery/out/cycle23-adaptive-width-four/wave0.tsv","proof/cycle_22_width_four_soundness.md","proof/cycle_23_adaptive_width_four_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on an oracle/construction failure or aggregate cap. After the complete
run, ask Darwin to review the evidence, propose independent next engines, and
advise whether Cycle 23 continues, seals, or yields to a distinct question.

## Live implementation amendment

The original all-constraint sparse LP launch was killed by the kernel OOM
manager: one representative simplex solve used 8.65 GiB RSS, so three workers
cannot fit in this 15 GiB, swapless host. An interior-point control used 8.58
GiB and was slower. This is a resource containment result, not a mathematical
observation. The embedded manifest now fixes an equivalent, bounded
cutting-plane implementation before its first execution. It keeps the same
targets, partition selector, LP, integerization, and aggregate caps; only the
solver representation changes. The two controls consumed 258.83 seconds of
the aggregate wall allowance and produced no promoted claim.
