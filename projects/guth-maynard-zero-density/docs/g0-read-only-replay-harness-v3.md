# G0 read-only replay harness v3

## Outcome

`OBSERVED`: [v3](../proof/run_g0_replay_v3.py) completed its fixed 22-check
inventory under explicitly checked CPython 3.12.3 with
`sys.flags.optimize == 0`. It appends the two Cycle-1 read-only route
wrappers, the published-source v5 checker, the six-route resource
configuration, the bounded v2 hostile audit, and
`g0-full-reconstruction-v2` to the preserved v2 operational coverage.

The harness uses explicit `RuntimeError` failures for its own preflight, so
an optimized invocation is rejected before it can delegate to legacy v2:

```sh
python3 -O proof/run_g0_replay_v3.py
```

`OBSERVED CONTAINMENT`: v3 retains rather than hides the audit finding that
the standalone v2 runtime pin is bypassable with `-O`. `OBSERVED`: this
runner does not make a theorem claim or a separate G0 decision; its final
v2 certificate retains its stated conditional reconstruction boundary.

## Replay and regression

```sh
python3 proof/run_g0_replay_v3.py
python3 -m unittest tests/test_g0_replay_harness_v3.py -v
```

No writer, directory scan, discovery script, or direct host-timing artifact
is in the v3 command inventory. The final authoritative checker validates
its own sealed resource record; this runner never regenerates that record.
