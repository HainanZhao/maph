# Cycle 14 sealing correction v2

- Error: v1 copied the freshly measured `wall_seconds` into the deterministic
  artifact payload under `benchmark.preseal_wall_seconds`.
- Cause: the code removed volatile row timings but reused the current replay's
  top-level timing instead of the frozen pre-seal measurement.
- Effect: every determinant, pivot transcript, tensor hash, theorem field, and
  claim boundary in v1 is valid, but `--check` cannot reproduce its bytes.
- Correction: v2 freezes the original pre-seal benchmark value `134.689078`
  as descriptive metadata and excludes every newly measured timing from the
  deterministic payload.  v2 supersedes v1.
