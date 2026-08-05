# Cycle 4 / B004 preregistration: disk-partitioned coverage levels

## Decision question

Cycle 3 retained every cover orbit and reproduced all exact controls, but an
in-memory next-level union exceeded the frozen memory budget before depth 8.
This cycle changes only the storage engine: deterministic radix partitions
replace the monolithic in-memory union.

The decision is whether partition-local exact deduplication preserves the
Cycle-3 level set and completes ((k,p)=(13,199)) within explicit aggregate
RAM, disk, wall, state, edge, and leaf caps. This remains an initial sieve and
cannot establish (J(13,199)=arnothing) or (LRC(13)).

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 4,
  "parameters": {
    "mathematical_engine": {
      "kind": "expression",
      "value": "Use exactly the Cycle-3 cyclic cover model, least-primitive-root coordinates, lexicographic translation canonicalization, minimum-uncovered-time augmentation, early-cover all-center clause, and remaining-coverage pruning. The sealed Cycle-3 retained-path lemma is the completeness argument.",
      "rationale": "Cycle 4 tests storage, not a post-result mathematical rule change."
    },
    "state_serialization": {
      "kind": "expression",
      "value": "A canonical partial multiset is one fixed 16-byte record: its sorted exponent entries as unsigned bytes followed by zero bytes. At a fixed depth the depth supplies the active length. Records compare lexicographically as unsigned bytes; no padding, header, native integer, or endianness-dependent field is serialized.",
      "rationale": "A fixed portable record makes sorting, hashing, replay, and byte accounting exact."
    },
    "partition_rule": {
      "kind": "expression",
      "value": "Use P=64 partitions. Compute 64-bit FNV-1a over all 16 serialized bytes, starting at 1469598103934665603 and multiplying by 1099511628211 after each xor, with unsigned 64-bit wraparound. The partition is hash & 63. Each worker writes one private shard per target partition, so concurrent writes never share a file.",
      "rationale": "Every equal state has one deterministic target partition and worker-private shards avoid synchronization-dependent bytes."
    },
    "partition_dedup": {
      "kind": "expression",
      "value": "For each target partition, concatenate its three worker shards in worker-index order, sort all fixed records lexicographically, remove adjacent equal records, and write one sorted unique partition file. Partitions are disjoint by the frozen hash; therefore the union of independently deduplicated partition files is exactly the global canonical child set, with no cross-part duplicate possible.",
      "rationale": "This is the exact replacement for Cycle 3's monolithic global sort/unique."
    },
    "parallel_schedule": {
      "kind": "expression",
      "value": "Use exactly three worker threads with process affinity CPUs 0,1,2, leaving CPU 3 free. Expansion dynamically assigns current partitions; deduplication dynamically assigns target partitions. Counters and resource caps are aggregate. Output content is independent of assignment order because shard concatenation order and final sorting are fixed.",
      "rationale": "Partition work is fine-grained enough to avoid the prior static-shard imbalance."
    },
    "workspace_and_cleanup": {
      "kind": "expression",
      "value": "Use only discovery/out/cycle4-work as the temporary root and refuse to start if it already exists. Record per-level unique counts, raw record counts, and byte totals. On complete or classified failure, remove only that explicit temporary root after the durable result/timing files have been written; a crash may leave it for recovery and must not trigger broad recursive deletion.",
      "rationale": "The run is recoverable and cleanup cannot target unrelated data."
    },
    "baselines": {
      "kind": "text",
      "value": "Required exact outputs are the naive k=3,p=11 oracle and byte-for-byte tuple equality for (6,47)=53 and (7,47)=50. Also require per-level state counts equal to Cycle 3 on both p=47 controls.",
      "rationale": "Tuple and level equality jointly test mathematical coverage and the partition storage interface."
    },
    "frontier_target": {
      "kind": "text",
      "value": "For (13,199), pass requires a complete size-13 tuple file equal to the 4,748,938-row Cycle-1 census, at most 586,985,072 expanded unique states, 5,869,850,724 generated edges, and 29,565,371 examined leaf states, plus all resource caps below.",
      "rationale": "Storage changes cannot weaken the Cycle-3 exactness or performance target."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A pass establishes only completeness and frozen-instance performance of the partitioned finite cyclic-cover engine. It proves no eventual properness, J-empty claim, prime-product contradiction, LRC(13), novelty beyond reviewed sources, or asymptotic result.",
      "rationale": "This remains initial-sieve infrastructure."
    }
  },
  "resource_caps": {
    "baseline_instances": {"kind":"integer","value":2,"rationale":"The two frozen published controls; the tiny oracle is a correctness preflight."},
    "frontier_instances": {"kind":"integer","value":1,"rationale":"Only k=13,p=199 is authorized for the frontier gate."},
    "partitions": {"kind":"integer","value":64,"rationale":"Bounds each exact sort while limiting open worker shards."},
    "worker_threads": {"kind":"integer","value":3,"rationale":"Use three of four CPUs and reserve one."},
    "expanded_state_cap": {"kind":"integer","value":586985072,"rationale":"Cycle-3 frozen state threshold."},
    "generated_edge_cap": {"kind":"integer","value":5869850724,"rationale":"Cycle-3 frozen edge threshold."},
    "leaf_state_cap": {"kind":"integer","value":29565371,"rationale":"Cycle-3 frozen leaf threshold."},
    "wall_seconds_frontier": {"kind":"integer","value":3600,"rationale":"One-hour frontier cap."},
    "peak_memory_mib": {"kind":"integer","value":8192,"rationale":"Aggregate virtual-memory cap enforced and logged by the runner."},
    "temporary_disk_gib": {"kind":"integer","value":64,"rationale":"Well below the observed 167 GiB free space while allowing partition shards and adjacent levels."},
    "rng_seed": {"kind":"not_applicable","justification":"Partitioning, scheduling, sorting, and deduplication are exact and output-deterministic.","rationale":"Randomization is unnecessary and cannot certify completeness."}
  },
  "formula_families": [
    "Cycle-3 minimum-uncovered-time canonical level construction",
    "fixed 16-byte canonical-state serialization",
    "64-way FNV-1a radix partition",
    "worker-private raw shards",
    "partition-local lexicographic sort and unique",
    "aggregate state, edge, leaf, disk, memory, and wall counters"
  ],
  "selection_rule": [
    "Write the partition-union exactness argument before executable work relies on partition output.",
    "Pass the tiny oracle, both tuple-set comparisons, and both p=47 per-level count comparisons before frontier execution.",
    "Compile the hot path with -O3 -march=native -flto -DNDEBUG -pthread and benchmark the exact controls.",
    "Run the frontier on CPUs 0-2 with one CPU reserved, a logged 8 GiB virtual-memory limit, and aggregate disk accounting.",
    "Pass only after complete frontier tuple equality and every frozen counter/resource threshold passes."
  ],
  "failure_rule": [
    "Any serialization round-trip failure, wrong-partition record, duplicate within a unique partition, or baseline level/tuple mismatch falsifies the storage engine and halts the frontier run.",
    "Any unproved pruning or mathematical augmentation change is exploratory and cannot affect exact output.",
    "A timeout, allocation failure, disk-cap breach, state-cap breach, edge-cap breach, or leaf-cap breach is an algorithmic gate failure, not a mathematical no-go.",
    "A crash leaves the explicit temporary root intact for diagnosis; cleanup may remove only that resolved path after classification.",
    "Do not promote a finite partitioned result to J(13,199)=empty or LRC(13)."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T14:08:23Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY with unrelated concurrent changes elsewhere and the active untracked open-conjecture-sweep project. Cycles 1-3 are sealed; this freeze names their artifacts, this preregistration, and the shared validator as inputs."
  },
  "input_paths": [
    "artifacts/cycle-1-b001-lrc-frontier-census-v1.json",
    "artifacts/cycle-2-b002-lrc-orbit-quotient-v1.json",
    "artifacts/cycle-3-b003-lrc-coverage-levels-v1.json",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Stop rule

Stop before the frontier run if the partition proof, serialization check, tiny
oracle, either baseline tuple set, or either baseline level sequence fails.
After a complete frontier decision or frozen resource failure, take the next
material engine decision without changing the mathematical augmentation or
partition family inside this cycle.
