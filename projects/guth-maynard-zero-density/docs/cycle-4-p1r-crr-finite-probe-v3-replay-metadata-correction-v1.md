# Cycle 4 P1R-CRR finite-probe v3 replay-metadata correction v1

## Scope

`OBSERVED`: the immutable v3 result artifact
`discovery/cycle-4-p1r-crr-finite-probe-v3.json` has SHA-256
`41576b9ad21d44435d251a8fefad1cc64bb038384644ce93c1d1a4314c38a0cb`.
Its runner metadata correctly identifies
`discovery/run_cycle_4_p1r_crr_finite_probe_v3.py`, but its two replay-command
strings incorrectly name the v2 runner.

This narrow correction does not edit the result artifact or runner, does not
run the search, and does not alter a row, seed, candidate, numerical value,
status, cap, or research conclusion.  It creates a separate, hash-pinned
metadata record only.  No hostile audit is initiated.

## Corrected commands

```sh
python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --check
python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --write
```

The `--write` command remains historical-only: the preserved result artifact
already exists, and the runner refuses to overwrite it.  The usable replay
verification command is the `--check` command above.

## Cause and invariants

`OBSERVED`: v3 wraps the v2 implementation and corrected its runner path and
hash, but inherited the base payload's literal replay strings.  The correction
builder pins the immutable v3 result hash and verifies:

- 160 retained rows, in their original order and with unique identifiers;
- exactly `{"NO_RETAINED_HIT": 160}` status counts;
- unchanged resources: 713.8161791041493 seconds, 564809728 peak RSS bytes,
  and the frozen 3300-second/1073741824-byte caps;
- v3 runner path and SHA-256
  `667207f0f690aaf36f33fa498a5b90594e2ac500173c44db64388e2958b4d90f`.

This correction has no mathematical content.  The finite-table claim remains
`OBSERVED`, and its complex diagnostics remain `RECOGNIZED`.

## Replay boundary correction

`OBSERVED`: the original result's `--check` mode is a structural/hash check;
it does **not** recompute the 160 rows.  Accordingly, neither this correction
nor the earlier results note describes it as a byte-for-byte or full semantic
replay.  A separate deterministic semantic-replay harness recomputes all 160
rows from the sealed schedule, compares every deterministic row/status field
exactly while excluding variable wall/RSS observations, records its own
resources, and preserves any mismatch as an artifact.  The harness is a
replay of the frozen discovery calculation, not a new candidate search or a
parameter-changing rerun.

## Retraction of over-localized outcome language

`OBSERVED` / `EXPLORATORY`: the v3 results note incorrectly described the
all-miss outcome as localized to cubic-proxy mode stability.  The runner
dual-precision-checked cubic first, so cubic was the recorded **final**
outcome diagnostic for every row; it did not establish that other screens
passed.  A post-result binary64 census of the immutable row fields gives:

| Screen | Binary64 passes / 160 | Classification |
|---|---:|---|
| large value | 0 | `OBSERVED` / `EXPLORATORY` screen evidence |
| energy lower | 160 | `OBSERVED` / `EXPLORATORY` screen evidence |
| energy upper | 147 | `OBSERVED` / `EXPLORATORY` screen evidence |
| rational measure | 13 | `OBSERVED` / `EXPLORATORY` screen evidence |
| 16/32 quadrature agreement | 10 | `OBSERVED` / `EXPLORATORY` screen evidence |
| cubic positivity and C12 size | 160 | `RECOGNIZED` at 256/384 bits |
| C8/C12 cubic agreement | 0 | `RECOGNIZED` final failure at 256/384 bits |

For the binary64 screens, the ratios to their relevant final cutoffs have
minimum/median/maximum: large value `0.000620/0.15744/0.41159`, rational
measure `0.0167/0.2683/1.705`, and quadrature-disagreement divided by its
allowed bound `0.970/15.106/216.56`.  The correction builder recomputes this
census directly from the hash-pinned result artifact.  Since non-cubic
screens were not dual-precision evaluated, they are not recognized final
failures and must not be promoted as such.

The corrected interpretation is therefore a multi-diagnostic finite miss:
the retained table records a recognized cubic agreement failure in every row,
alongside exploratory binary64 evidence that the large-value screen also
misses every row and other screens often miss.  It remains neither a
continuous CRR no-go theorem nor a universal negative.
