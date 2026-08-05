# Cycle 18 / B018 preregistration: conditional pair-choice Hall lift

## Decision question and idea selection

Can exact weighted deficits over disjoint two-coordinate option groups certify
all 40 Cycle-17 survivor leaves of at least one frozen base?

The primary proposed pair-block union capacities, an exact first-seven-
coordinate case split, and CRT.  Darwin independently proposed conditional
pair-choice Hall certificates followed by a symbolic early-coordinate split,
with CRT as fallback.  We questioned whether grouping is cosmetic: it is not,
because duplicate coverage inside a pair is counted once rather than twice.
We also questioned whether the 38 shared ordinals justify training leakage;
they do not.  Both complete frozen 40-row sets, including the two exceptions,
are processed under one deterministic partition family.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":18,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: disjoint pair-block union capacities, symbolic first-seven-coordinate split, then CRT. Companion: conditional pair-choice Hall certificates, then the symbolic split and CRT. Choose pair blocks because they are the smallest exact lift that removes within-pair double counting and directly targets the Cycle-17 boundary.","rationale":"Both agents proposed coupled pair states; canonical overlap alone is not treated as a theorem."},
    "target_rows":{"kind":"expression","value":"Exactly the 80 Cycle-17 LP rows with status NO_LP_DEFICIT: 40 from base 4 and 40 from base 3, in base-4 then base-3 and leaf-ordinal order. Require exact equality with the frozen Cycle-17 bounded and LP tables before execution. Include the two nonshared ordinals from each base without special exclusion.","rationale":"No post-result leaf or exception selection."},
    "block_certificate":{"kind":"expression","value":"For a partition P into disjoint singleton/pair blocks and nonnegative integer time weights, an option selects one allowed digit per coordinate in a block. Let b(B,o,t)=1 iff at least one selected digit in option o covers time t. Define W=sum_t w_t and U_P=sum_B max_o sum_t w_t*b(B,o,t). Accept only if independently recomputed U_P<W.","rationale":"Any full cover has W<=U_P; pair overlap is counted once."},
    "partition_family":{"kind":"expression","value":"For each leaf enumerate and deduplicate partitions in this order: force the canonical mod-2 witness pair then pair remaining coordinates increasingly and leave the largest singleton; force the canonical mod-7 pair by the same rule; if the two witness pairs are disjoint force both then pair remaining increasingly and leave the largest singleton; the 13 cyclic near-perfect matchings obtained by choosing each singleton s and pairing the remaining cyclic order consecutively; then for every coordinate pair in lexicographic order force that pair and pair the remainder increasingly with the largest singleton. Canonicalize each partition by sorting coordinates within blocks and blocks lexicographically; retain first occurrence.","rationale":"Finite family tests leaf-aware, local, and broad pairings while explicitly retaining all rows."},
    "lp_proposal":{"kind":"expression","value":"For each target row and partition use every deduplicated time signature as w_t>=0, sum(w)=1, z_B>=sum_t w_t*b(B,o,t) for every allowed block option, and minimize sum_B z_B using scipy 1.14.1 linprog(method='highs-ds', presolve=True). Test partitions in frozen order and accept the first objective below 1-1e-9 that integerizes exactly.","rationale":"Floating optimization selects candidates only."},
    "integerization":{"kind":"expression","value":"For denominators D=2^12,2^16,2^20,2^24 in order, round w_t*D to nearest integer with ties to even, discard zero entries, require support at most 256, and independently reconstruct every block option maximum from the frozen base, leaf, CNF, partition, clauses, and weights. Accept the first exact U_P<W.","rationale":"Only exact finite arithmetic promotes a certificate."},
    "selection":{"kind":"expression","value":"Retain one first exact certificate or one explicit unresolved row per target. A base closes under the combined Cycle-17/18 family only if all its 40 target rows certify. Report per-partition and exception outcomes but select no semantic pattern from them.","rationale":"Complete leaf union, not LP accuracy, is the gate."},
    "advance_condition":{"kind":"expression","value":"Forty of forty exact pair-choice certificates for base 4 or base 3 completes that base's 6084-leaf canonical tree when combined with Cycle 17 and gives an independent exact first-lift exclusion for the named base. Partial coverage is a finite named result only.","rationale":"Requires complete coverage of at least one frozen base."},
    "falsifier":{"kind":"expression","value":"A target-row mismatch, nonpartition or overlapping blocks, omitted allowed block option, wrong union indicator, invalid weight/support, incorrect maximum, U_P>=W, or uncovered row in a claimed complete base invalidates the affected result.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Certificates concern only named leaves and bases. Even a completed base does not imply all frozen bases, F_1 emptiness, J emptiness, or LRC(13). Failure does not exclude larger blocks, other partitions, symbolic branches, or CRT.","rationale":"This is a finite level-2 lift."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "target_rows":{"kind":"integer","value":80,"rationale":"Exactly the Cycle-17 numerical boundary."},
    "bases":{"kind":"integer","value":2,"rationale":"Frozen base indices 4 and 3."},
    "maximum_block_size":{"kind":"integer","value":2,"rationale":"Level-2 pair-choice lift only."},
    "maximum_distinct_partitions_per_leaf":{"kind":"integer","value":94,"rationale":"Three conditional candidates, 13 cyclic candidates, and 78 forced-pair candidates before deduplication."},
    "integer_support_cap":{"kind":"integer","value":256,"rationale":"Short exact certificates."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"LP proposals, exact reconstruction, independent audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three sparse LP workers."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Rows, partitions, LP method, denominators, checks, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical survivor leaves","disjoint singleton/pair partitions","block-option union masks","nonnegative weighted pair-choice Hall deficits","exact integerized certificates"],
  "selection_rule":["Verify the exact 80-row target set.","Enumerate only the frozen partition family.","Use floating LP only for candidate weights.","Promote only independently reconstructed exact U_P<W inequalities.","Claim a base closed only at 40/40 target certificates combined with its 6044 Cycle-17 certificates."],
  "failure_rule":["Any target or encoding control mismatch halts execution.","A noncertifying partition continues to the next frozen partition.","An unresolved row remains explicit and blocks that base's closure.","Caps and numerical optima alone support no mathematical claim."],
  "pre_execution":{"timestamp_utc":"2026-08-03T21:46:11Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 17 is sealed before this distinct pair-choice state space.","filesystem_observation_bytes":{"size":206900281344,"used":41188610048,"available":165694894080,"reserved":5368709120,"maximum_temporary_cap":160326184960,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-17-b017-lrc-time-deficit-v1.json","discovery/out/cycle17-time-deficit/results.tsv","discovery/out/cycle17-time-deficit/lp-results.tsv","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle8-p199-strata.txt","proof/cycle_17_time_deficit_soundness.md","proof/cycle_18_pair_choice_soundness.md","requirements-cycle17.txt","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a target/encoding/audit failure or aggregate cap.  After the complete
80-row run, ask Darwin to review the evidence, co-propose next ideas, and
advise whether Cycle 18 seals, continues with a symbolic branch, or yields to
CRT.
