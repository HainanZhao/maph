# G0 read-only replay harness v1

## Claim boundary

`OBSERVED`: [the replay harness](../proof/run_g0_replay_v1.py) reports only
that its explicitly listed read-only source, exact-arithmetic, and
reconciliation checkers exited zero. It proves no mathematical theorem and
does not decide G0. A G0 decision belongs only in a separately versioned
global analytic reconciliation.

## One-command replay

From the project directory, run:

```sh
python3 proof/run_g0_replay_v1.py
```

The command has a fixed 13-check inventory. It captures individual checker
output, stops fail-closed at the first nonzero exit, and emits one compact JSON
record only on success. It never writes a certificate, source manifest, or
performance measurement.

| Check group | Fixed checker(s) |
|---|---|
| Source inventory and Stream A | source manifest v3; Stream-A frozen-source ledger |
| Published density reconstruction | Cycle-1 two-route reconciliation v3; both Stream-B routes; Stream-B reconciliation v2 |
| Short intervals | official source closure v4; independent SWORD audit; both Stream-C routes; Stream-C reconciliation v2 |
| Operational configuration | deterministic per-route 60-second/256-MiB configuration only |
| Historical correction | fixed-scope G0 evidence-matrix v3 correction |

The resource check is deliberately the immutable configuration check, not a
new runtime measurement. The host-specific performance record is `OBSERVED`
evidence for its own resource gate and is not a deterministic mathematical or
reconciliation input.

## Exclusions and fail-closed policy

The harness has no directory scan and no `--write` command. It excludes all
superseded writers and these timing-mutable raw artifacts:

- `cycle-2-stream-c-route-a-v3-performance.json`
- `cycle-2-stream-c-route-a-v4-performance.json`
- `cycle-2-stream-c-route-a-v5-performance.json`
- `cycle-2-stream-c-route-b-v5-performance.json`
- `cycle-2-g0-per-route-resource-gate-performance-v1.json`

Consequently, a new file cannot silently become evidence, and a change to any
listed source, script, certificate, or checked configuration makes the relevant
checker fail rather than regenerating it. The regression test is:

```sh
python3 -m unittest tests/test_g0_replay_harness_v1.py -v
```
