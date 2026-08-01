# Cycle 6 actual-log spectral probe preregistration v2 correction

## Scope

`OBSERVED`: v1 froze every mathematical and computational choice in prose and
in its conventions module, but was sealed before the executable runner file
was itself hash-pinned.  No row was run under v1.  V1 remains immutable as
`CONTAINED_PRE_RUNNER_HASH`; it is not a discovery outcome and supplies no
evidence about CRR compatibility.

V2 changes no scientific choice.  It pins the exact runner path and SHA-256,
its resource-cap control flow, and the conventions hash before the first
execution.  It retains v1's scales, labels, three rows/order, no-RNG rule,
all iteration counts, selectors, theta nodes, thresholds, retention rule,
and 600-second/1-GiB caps byte-for-byte.  No result was inspected in making
this correction.

`CONJECTURED`: V2 remains a bounded discovery protocol only.  A hit is
`OBSERVED`; floating complex data are `RECOGNIZED`; a miss is not a universal
negative and proves nothing about AFARI, FARI, CRR-U, density, or intervals.

## Added executable pin

The only new frozen implementation input is

```text
discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py
SHA-256 9591e287e7ff879449bf7091615520f406d56fc01bdbcd1884a57019ef26661f.
```

The runner validates the V2 artifact before computation, rechecks its own
hash and the conventions hash, uses literal actual-log/Farey labels, and
retains a resource cap without retry.  Its `--check` recomputes semantic
fields while excluding only the non-deterministic wall/RSS observations.

The exact correction is deliberately separate from the phase-lift theorem:
it neither changes nor supplies evidence for the analytic `rho`/`phi` gate.

## Replay

```sh
python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py --write
python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py --check
python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --write
python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --check
```
