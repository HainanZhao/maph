# Cycle 2 — G0 per-route resource gate v1

`OBSERVED` claim boundary: this is a host-specific operational measurement of
four already sealed route checks. It does not prove any theorem and does not
promote G0.

The deterministic configuration fixes four checks, each including its sealed
source verification path:

- Stream B Route A v3;
- Stream B Route B v1;
- Stream C Route A v5;
- Stream C Route B v5.

Each command is measured separately with `/usr/bin/time -v`. A route fails
closed unless its command exits zero, GNU-time fields parse, wall time is
strictly below 60 seconds, and peak resident memory is strictly below 256 MiB
(`262144` KiB). The performance artifact records exact commands, interpreter,
GNU time, and `mutool` versions, plus observed wall time and RSS. The
deterministic config and harness contain no runtime measurements.

Run the whole gate with:

```sh
python3 projects/guth-maynard-zero-density/proof/run_cycle2_g0_resource_gate_v1.py --write-performance projects/guth-maynard-zero-density/artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json
```

Verify the fixed configuration with:

```sh
python3 projects/guth-maynard-zero-density/proof/run_cycle2_g0_resource_gate_v1.py --check-config projects/guth-maynard-zero-density/artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json
```

Even a `PASS` resource gate is not a G0 PASS; theorem-hypothesis and
independent-route reconciliation requirements remain separate.
