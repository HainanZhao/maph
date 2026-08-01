# Cycle 3 G1 engine v3 replay-boundary correction

Date: 2026-08-01 UTC, before any corrected full-screen rerun.

## Claim boundary

`OBSERVED`: v2 draft SHA-256
`62d3b565f4b80f7a7d17d19e779eec5107a1b2df11990cb30db1dc1d07830941`
closed the runtime, exception, validation, and checkpoint defects, but its
`--check-observations` interface could assemble from an existing completed
checkpoint, call that operation replay, and then mutate the supplied
checkpoint. The v2 draft and its manifest remain preserved; no v2 full run was
launched.

V3 pins and reuses that exact v2 row engine but separates the operations:

1. `--verify-sealed-assembly` reads a complete checkpoint, reconstructs final
   JSON, compares it byte-for-byte, and verifies that the checkpoint hash did
   not change. It is explicitly cached assembly verification, not replay.
2. `--full-replay-fresh` refuses any existing checkpoint path, creates a new
   empty checkpoint bound to the exact v3 driver, then enters the row core's
   explicit resume path with zero cached rows. It therefore recomputes every
   one of the 588 scheduled rows and any retained validations, and compares the
   resulting timing-independent observations. Its fresh checkpoint is explicit
   replay evidence.
3. `--run-full` remains the production/resume path and writes performance
   before observations, using observations as the final commit marker.

No grid, family, set, seed, precision, score, resource cap, failure policy, or
row semantics changed.

## One-command interfaces

Production from a fresh checkpoint:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_atlas_v3.py \
  --run-full \
  --checkpoint projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-checkpoint-v3.json \
  --observations projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-v3.json \
  --performance projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-performance-v3.json
```

Read-only cached assembly verification:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_atlas_v3.py \
  --verify-sealed-assembly \
  --checkpoint projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-checkpoint-v3.json \
  --observations projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-v3.json \
  --performance projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-performance-v3.json
```

True full replay into a new explicit checkpoint:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_atlas_v3.py \
  --full-replay-fresh \
  --checkpoint projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-replay-1-checkpoint-v3.json \
  --observations projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-v3.json
```

The final command is a full deterministic replay of the same implementation,
not an independent mathematical verification route.
