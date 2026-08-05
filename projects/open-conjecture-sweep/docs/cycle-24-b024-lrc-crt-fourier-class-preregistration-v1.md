# Cycle 24 / B024 preregistration: CRT Fourier-class capacity dual

## Decision question and idea selection

Can a nonnegative dual weight in the exact low-degree CRT/Ramanujan class
space, together with its class-aggregated overlap selector, yield a fresh
integer capacity deficit on any of the 60 Cycle-23 survivors?

The primary and Cycle-23 companion independently proposed a Fourier/CRT
higher-order dual, width-five heterogeneous capacity LP, and a semantic
primal route.  The scratch comparison is in
`discovery/cycle24_fourier_idea_selection.md`.  We choose the CRT class dual:
it preserves the two-diagonal coupling exactly while testing alpha--beta
correlations outside the prior single-weight pair score.  Width five is the
main rejected alternative until a compact control justifies its option growth.
The primal route is rejected because no exact improper-lift equivalence has
yet been supplied.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":24,
  "parameters":{
    "targets":{"kind":"expression","value":"Exactly the 60 Cycle-23 oracle rows, in frozen order, all with initial status NEED_LP and final status UNRESOLVED. No target may be added, removed, or reordered.","rationale":"No target reselection."},
    "crt_class_space":{"kind":"expression","value":"For p=199,c=14, label a time by alpha=a mod 199 and beta=a mod 14. Its class is (epsilon,g), where epsilon=0 iff alpha=0 and epsilon=1 otherwise, and g=gcd(beta,14) in {1,2,7,14}. Use exactly eight nonnegative integer class weights z_(epsilon,g), constant on each class. This is the tensor product of the two Ramanujan class algebras: R_199(alpha)=198 for alpha=0 and -1 otherwise, and the four divisor-Ramanujan functions on Z/14Z.","rationale":"An exact integer-valued low-degree Fourier/CRT space."},
    "class_control":{"kind":"expression","value":"Before target execution, exhaustively check every one of 2786 CRT points: its direct time mask equals the Cycle-21 coupled predicate; its class label is unique; the eight class cardinalities equal the CRT product cardinalities; and the eight Ramanujan basis evaluations have full rank over Q on the eight classes.","rationale":"Pins transform, CRT, and class conventions."},
    "partition_oracle":{"kind":"expression","value":"For each class indicator separately, compute exact singleton and pair coverage maxima on the target direct CNF and allowed digits. Sum its pair savings over all eight indicators. Enumerate every coordinate partition into one four-block and three unordered three-blocks, score it by the summed within-block savings, and choose the maximum with lexicographic canonical tie break. Require 200200 candidates per target.","rationale":"A higher-order CRT-class selector, not reuse of the Cycle-23 single witness score."},
    "class_lp":{"kind":"expression","value":"For the selected partition, minimize sum_B q_B over z_(epsilon,g)>=0 with sum_class cardinality(class)*z_class=1 and every exact block option inequality coverage_class(option) dot z <= q_B. Solve this finite LP by deterministic cutting planes: start with the lexicographically first option per block, exhaustively find the lexicographically first maximum violating option in every block, use tolerance 1e-9, and stop after at most 512 rounds. A cap or nonconvergence is CAP, never a conclusion.","rationale":"Eight-variable Fourier-class dual with all options separated exactly."},
    "integerization":{"kind":"expression","value":"If the floating class-LP objective is below 1-1e-9, test denominators 4096,65536,1048576,16777216 in order by rounding class weights, discard an all-zero weight, then build the resulting integer weight on all 2786 direct times. Promote only if a fresh full direct-CNF target-option enumeration gives U<W.","rationale":"Exact closure remains the established block-deficit criterion."},
    "selection":{"kind":"expression","value":"Use CPUs 0-2 with CPU 3 reserved. Complete the class control, then breadth-first process all 60 targets with exactly one selected partition and at most one class LP each. Preserve oracle score, partition, LP status/objective, class vector, integerization, W/U, and all caps.","rationale":"One coherent finite family."},
    "advance_condition":{"kind":"expression","value":"At least one named target receives an independently replayed direct integer U<W deficit. A direct full-cover assignment satisfying the actual improper-lift semantics is a headline falsifier; a class score, floating LP, or partition change is not advance.","rationale":"No discovery-only promotion."},
    "falsifier":{"kind":"expression","value":"Any CRT/direct-mask, class-cardinality, Ramanujan-rank, allowed-digit, oracle count/tie, LP separation, class vector, integerization, direct capacity, or replay mismatch invalidates the affected result. U>=W never certifies.","rationale":"Exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Every certificate concerns one named canonical leaf. Failure, cap, or nonnegative class-LP optimum does not rule out individual Fourier characters beyond this eight-class space, width five, a semantic primal model, either base, F_1, J, or LRC(13).","rationale":"Strict finite scope."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "target_rows":{"kind":"integer","value":60,"rationale":"Exact Cycle-23 boundary."},
    "classes":{"kind":"integer","value":8,"rationale":"Two alpha and four beta Ramanujan classes."},
    "partition_candidates_per_target":{"kind":"integer","value":200200,"rationale":"One four-block times complementary triples."},
    "lp_solves_per_leaf":{"kind":"integer","value":1,"rationale":"No adaptive reselection."},
    "separation_rounds":{"kind":"integer","value":512,"rationale":"Bounded exact all-option solver."},
    "integer_certificate_support":{"kind":"integer","value":2786,"rationale":"Class weights may occupy every time."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Control, target family, and independent audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":8192,"rationale":"Three eight-variable on-demand separation workers."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB below free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Class labels, target order, maxima, partition enumeration, ties, LP method, and integerization are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["direct Cycle-11 time masks","proved coupled CRT two-diagonal predicate","eight-class Ramanujan tensor space","class-aggregated exact pair savings","one-four-plus-three-triples capacity dual"],
  "selection_rule":["Verify CRT/Ramanujan control.","Compute eight-class exact pair savings.","Select the canonical global partition.","Solve one exact-separated class LP.","Promote only direct-CNF integer U<W."],
  "failure_rule":["Any control or oracle mismatch halts the branch.","A failed integerization remains unresolved.","A resource or separation cap preserves the affected target as CAP.","No floating or class result is proof."],
  "pre_execution":{"timestamp_utc":"2026-08-04T04:18:07Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 23 is sealed before this distinct Fourier-class dual.","filesystem_observation_bytes":{"size":206900281344,"used":45233115136,"available":161650388992,"reserved":5368709120,"maximum_temporary_cap":156281679872,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json","artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json","artifacts/cycle-23-b023-lrc-adaptive-width-four-v1.json","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle23-adaptive-width-four/oracle.tsv","discovery/out/cycle23-adaptive-width-four/wave1.tsv","discovery/lrc_coupled_incidence.py","discovery/lrc_crt_fourier_class.py","proof/check_cycle_24_crt_fourier_class.py","proof/cycle_20_crt_diagonal_soundness.md","proof/cycle_21_coupled_incidence_soundness.md","proof/cycle_24_crt_fourier_class_soundness.md","tests/test_cycle_24_crt_fourier_class.py","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop this cycle after the complete frozen class family, a construction/control
failure, or the aggregate cap.  At the resulting material decision point,
obtain one companion review before sealing or selecting a distinct engine.
