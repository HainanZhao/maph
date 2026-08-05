# Cycle 5 / B005 preregistration: 128 GiB partition tranche

## Decision question

Cycle 4 validated the exact 64-partition engine but stopped at its configured
64 GiB logical-disk cap. At the user's direction, this cycle reruns the same
engine with only that tranche changed to 128 GiB. No mathematical,
serialization, partition, pruning, scheduling, or other resource rule changes.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 5,
  "parameters": {
    "frozen_engine": {"kind":"expression","value":"Use byte-for-byte the Cycle-4 source implementing the Cycle-3 retained-path augmentation, fixed 16-byte states, 64-bit FNV-1a partition & 63, three worker-private shards per target, and partition-local lexicographic sort/unique. Reuse the sealed partition-union proof.","rationale":"Only the user-authorized disk tranche changes."},
    "resource_change": {"kind":"expression","value":"Change temporary_disk_gib from 64 to 128. Keep the Cycle-4 state cap 586985072, edge cap 5869850724, leaf cap 29565371, wall cap 3600 seconds, virtual-memory cap 8192 MiB, 64 partitions, and three workers on CPUs 0,1,2.","rationale":"Isolates whether the prior stop was only the selected logical-storage tranche."},
    "storage_observation": {"kind":"expression","value":"The runner logs df -B1 size, used, available, and mount immediately before execution and immediately after engine cleanup, plus the engine's exact serialized live-byte peak. The logical cap is canonical; filesystem figures are observational because block allocation and concurrent use may differ.","rationale":"Distinguishes the exact internal cap from physical filesystem observations."},
    "cleanup": {"kind":"expression","value":"Reuse only discovery/out/cycle4-work, refuse if it exists, and remove only that explicit root after a complete or classified engine result. A crash leaves it intact. The wrapper never deletes it.","rationale":"Preserves the Cycle-4 safe cleanup boundary."},
    "frontier_target": {"kind":"text","value":"For k=13,p=199, pass requires the complete 4,748,938-row tuple set equal to Cycle 1, at most 586985072 expanded states, 5869850724 edges, 29565371 leaves, 3600 seconds, 8192 MiB virtual memory, and 128 GiB logical temporary storage.","rationale":"All non-disk decision thresholds remain frozen."},
    "claim_boundary": {"kind":"expression","value":"The outcome concerns only the frozen finite initial-sieve engine. It proves no J-empty claim, prime-product closure, LRC(13), general asymptotic improvement, or physical disk exhaustion.","rationale":"A larger resource tranche does not broaden the mathematics."}
  },
  "resource_caps": {
    "frontier_instances": {"kind":"integer","value":1,"rationale":"One rerun of k=13,p=199."},
    "partitions": {"kind":"integer","value":64,"rationale":"Unchanged engine partition count."},
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use three of four CPUs and reserve one."},
    "expanded_state_cap": {"kind":"integer","value":586985072,"rationale":"Unchanged Cycle-4 cap."},
    "generated_edge_cap": {"kind":"integer","value":5869850724,"rationale":"Unchanged Cycle-4 cap."},
    "leaf_state_cap": {"kind":"integer","value":29565371,"rationale":"Unchanged Cycle-4 cap."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"Unchanged one-hour cap."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Unchanged logged virtual-memory cap."},
    "temporary_disk_gib": {"kind":"integer","value":128,"rationale":"Explicit user-authorized increase from Cycle 4."},
    "rng_seed": {"kind":"not_applicable","justification":"The frozen engine is exact and output-deterministic.","rationale":"No randomized selection exists."}
  },
  "formula_families": [
    "sealed Cycle-4 64-partition exact engine",
    "128-GiB logical serialized-live-byte tranche",
    "pre-run and post-cleanup physical-filesystem observations"
  ],
  "selection_rule": [
    "Verify the Cycle-4 source hash and sealed artifact before launch.",
    "Do not rerun baselines because the executable source and every non-disk rule are byte-identical to the sealed engine.",
    "Run once on CPUs 0-2 with logged 8-GiB virtual memory and 128-GiB logical disk caps.",
    "Pass only after complete tuple equality and all unchanged thresholds pass."
  ],
  "failure_rule": [
    "Any source drift, existing work root, or mismatch in configured non-disk arguments blocks launch.",
    "A logical disk, state, edge, leaf, wall, memory, IO, or partition failure is an algorithmic gate failure only.",
    "Physical df observations do not replace the exact internal logical-byte counter.",
    "Do not promote the finite result to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T14:30:00Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes and the active open-conjecture-sweep project. Cycles 1-4 are sealed; Cycle 5 changes only the disk tranche.",
    "filesystem_observation_bytes": {"size":206900281344,"used":28415700992,"available":178467803136,"mount":"/"}
  },
  "input_paths": [
    "artifacts/cycle-4-b004-lrc-partitioned-v1.json",
    "discovery/lrc_coverage_partitioned.cpp",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Run the unchanged exact engine once. At completion or a classified frozen cap,
take the next material decision; do not enlarge another resource or alter the
engine inside this cycle.
