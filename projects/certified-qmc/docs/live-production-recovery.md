# Live production recovery checkpoint

Status: operational recovery record for the active Cycles 016–018 run.
This file is not a certification result and promotes no data.  The
authoritative mutable state is the chunked dataset under
`artifacts/fidelity-v2`; this tracked record explains how to resume it
without recomputing completed chunks.

## Banked snapshot

Snapshot time: `2026-07-29T11:39:39Z`.

- repository commit at snapshot: `d9c855a`;
- production PID: `901613`;
- continuation-watcher PID: `922856`;
- production stage: `WAITING_FOR_FIDELITY_SEAL`;
- telemetry: 6,300 chained records, terminal sequence 6,299;
- telemetry terminal hash:
  `b5dd75ec3d20b81639803aae6e770faacb2ddb47b3b490cb9b4a4f439cc1ea9f`;
- accumulated updates: 4,723,137,331,200 of 53,797,264,588,800
  (`8.77951205753927%`);
- aggregate throughput: `2.8862619151492015 ns/update`;
- pause records: zero;
- manifest terminal sequence: 201,599;
- manifest terminal hash:
  `8205ca3ebb9acd1dc903a8bed1082fd80610ed6d04e7d347f5af40e5f99f01df`;
- last structurally complete chunk: fixed family `29102`,
  \(N=2^{18}\), work-prime index 1,797, dimensions 3,585–3,600;
- fixed-family columns \(N=2^{10},\ldots,2^{17}\) have every scheduled
  work and overflow chunk; all values remain unpromoted until the
  sealed production audit.

Frozen file digests at the snapshot:

| File | SHA-256 |
|---|---|
| `artifacts/fidelity-v2/run-manifest.json` | `cb9e4ac83bd5e8ff7fd739b41d9ac47c0c8452eb96822d38a199a7e4845469f8` |
| `artifacts/fidelity-v2/table-index.json` | `2952fbb6b98d19c6a7a5fd2b7451165ddba0a00d5244dd9eb41b4e321dd0e8a6` |
| `data/cycles-016-017-fidelity-spec-v2.json` | `28789f431c71dd0b29ae65dd6caf6949d02cba89ae3eb6178611e51571fd8bbe` |
| `data/primes-schedule-v1.json` | `22fadf04ddc70749a5c340483d457590dbe445fbf87883f4875f0ccf71331697` |

The run manifest additionally binds the frozen native binary, its C
source, compiler and flags, every input table, every preregistration,
and the independent prime-schedule certificate.  A live read-only
audit at this snapshot passed all 56 such bindings.

## Why a process crash does not restart the computation

`scripts/run_chunked_production.py` is a deterministic resume driver.
At startup it:

1. rebuilds and compares the table index and run manifest;
2. scans the append-only manifest and authenticates every recorded
   chunk;
3. rejects duplicate keys, unsafe paths, missing payloads, hash
   mismatches, and metadata changes;
4. groups only missing `(table, prime)` work; and
5. appends from the prior chain endpoint.

Chunks are written to a temporary sibling and atomically renamed before
their manifest record is appended.  A crash can therefore lose at most
the currently executing four-prime batch.  The Cycle-015 gate already
demonstrated byte-identical recovery after three literal forced kills.

## Recovery after process crash or host reboot

Never run two production drivers against the same output directory.
First inspect the process and terminal records:

```sh
cd /root/projects/maph/projects/certified-qmc
pgrep -af 'run_chunked_production.py|continue_production_cycles.py'
tail -n 1 artifacts/fidelity-v2/telemetry.jsonl
tail -n 1 artifacts/fidelity-v2/manifest.jsonl
```

Apply these rules:

- If a production driver is still live, do not start another.
- If the terminal telemetry event is `PAUSE`, do not resume; preserve
  the transcript and escalate.
- If the terminal manifest event is `SEAL`, do not rerun production;
  start only the continuation watcher if the Cycle-018 data gate has
  not already passed.
- Never resume `artifacts/fidelity-v1`; that failed run is quarantined.

If the v2 dataset is unsealed and no producer is live, resume the exact
frozen command:

```sh
cd /root/projects/maph/projects/certified-qmc
nohup .venv/bin/python scripts/run_chunked_production.py \
  --spec data/cycles-016-017-fidelity-spec-v2.json \
  --output artifacts/fidelity-v2 \
  >> /var/tmp/certified-qmc-fidelity-v2.log 2>&1 &
```

After the producer has begun appending fresh telemetry, start the
continuation watcher if it is absent:

```sh
cd /root/projects/maph/projects/certified-qmc
nohup .venv/bin/python scripts/continue_production_cycles.py \
  >> /var/tmp/certified-qmc-continuation.log 2>&1 &
```

The watcher has a 15-minute stale-telemetry fail-closed threshold, so
start the producer first after a long outage.  It automatically runs,
in order:

1. sealed fidelity audit;
2. usability production;
3. usability audit and `j^-2` reuse check; and
4. the 298-case engine-oracle extraction.

Inspect recovery state with:

```sh
jq . artifacts/cycle-continuation-state.json
.venv/bin/python scripts/audit_production_phase_completion.py
```

Any resume metadata mismatch, oracle mismatch, overflow-prime failure,
manifest break, or new `PAUSE` is an escalation condition.  Do not
delete, rewrite, truncate, or manually “repair” a chunk or chain.

## Persistence boundary

This checkpoint and all frozen source/configuration files are tracked
and pushed to the repository.  Completed production chunks are stored
on the VPS disk and make process-crash or ordinary reboot recovery
incremental.  Git does not contain the live multi-gigabyte dataset, so
total loss of the VPS volume would still lose those completed chunks;
an external volume snapshot or object-store mirror is required to
cover provider-level disk loss.

