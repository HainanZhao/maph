# G0 read-only replay harness v2

## Claim boundary

`OBSERVED`: [this v2 runner](../proof/run_g0_replay_v2.py) reports only that
its 16 listed read-only checkers exited zero. It is not a second G0 decision
and proves no new mathematical theorem. The G0 decision is exclusively the
claim of the separately sealed
[`PROVED` authoritative reconstruction](../artifacts/g0-full-reconstruction-v1.json),
under that artifact's stated conditional boundary.

V2 supersedes the operational inventory in v1, without modifying or
invalidating [v1](g0-read-only-replay-harness-v1.md). It adds, after their
separate seals, the bounded literature/source audit v1, hostile final-gate
audit v1, and full reconstruction v1.

## One-command replay

From the project directory:

```sh
python3 proof/run_g0_replay_v2.py
```

The fixed inventory first repeats all v1 checks: source manifest; Stream A;
Cycle 1; both Stream B routes and reconciliation; official Stream C source
chain, routes, and reconciliation; immutable resource configuration; and the
historical matrix correction. Its final three `--check` calls replay the
literature audit, hostile audit, and authoritative reconstruction in that
order. Any failure stops the runner and reports the failed command's captured
output; it never regenerates an artifact.

The regression replay is:

```sh
python3 -m unittest tests/test_g0_replay_harness_v2.py -v
```

## Timing and legacy boundary

No directory scan or writer appears in the harness. It excludes legacy
route-writer outputs and all raw host-timing/performance records, including
the four current Cycle-2 per-route measurements. The immutable resource
configuration is checked directly; the full reconstruction's separately
pinned `OBSERVED` resource evidence retains its own stated scope. The test
hashes every excluded timing record before and after the one-command replay,
so a future accidental mutation fails the regression.
