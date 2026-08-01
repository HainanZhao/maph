# Cycle 3 G1 engine v4 two-fresh-run promotion boundary

Date: 2026-08-01 UTC, before either v4 production execution.

## Claim boundary and correction

`OBSERVED`: v3 correctly separated read-only cached assembly from true replay,
but a structurally valid tampering of cached row payloads could pass its resume
and assembly checks. The project does not attempt to turn a mutable crash cache
into an adversarially self-authenticating proof object. V3 is preserved at
SHA-256 `921f25ae3f6d535899b439b04f310bc91b4278046976b7ad7947c04b6166f06f`.

V4 instead creates a promotion boundary based on two complete executions from
two distinct nonexistent checkpoint paths. There is no v4 resume interface.
Each timing-independent observation artifact says
`UNVERIFIED_PENDING_SECOND_FRESH_RUN` and `promotion_allowed=false`. Separate
performance records remain host observations and are never compared for byte
identity.

The standard-library-only adjudicator imports no probe engine. It checks the
v1--v4 and preregistration identities, both fresh-origin declarations, distinct
checkpoint and output paths, all 588 screen rows, 7,744 local structural rows,
560 transfer rows, retained/validation coverage, checkpoint-to-observation
payload and hash bindings, resource counts, and byte identity of the two
complete timing-independent observation files. Only then may it create
`cycle-3-g1-atlas-empirical-reconciliation-v1.json` with status
`EMPIRICALLY_RECONCILED`. That status remains `OBSERVED` finite evidence, not
a proof, extremizer, no-go theorem, density improvement, or independent
mathematical route.

## Exact commands after hostile signoff

Fresh production A:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_atlas_v4.py \
  --run-fresh --run-label A \
  --checkpoint projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-a-checkpoint-v4.json \
  --observations projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-a-v4.json \
  --performance projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-performance-a-v4.json
```

Fresh production B, from distinct paths:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_atlas_v4.py \
  --run-fresh --run-label B \
  --checkpoint projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-b-checkpoint-v4.json \
  --observations projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-b-v4.json \
  --performance projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-performance-b-v4.json
```

Immutable empirical reconciliation:

```sh
python3 projects/guth-maynard-zero-density/discovery/adjudicate_g1_atlas_v4.py \
  --checkpoint-a projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-a-checkpoint-v4.json \
  --observations-a projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-a-v4.json \
  --checkpoint-b projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-run-b-checkpoint-v4.json \
  --observations-b projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-observations-b-v4.json \
  --write projects/guth-maynard-zero-density/artifacts/cycle-3-g1-atlas-empirical-reconciliation-v1.json
```

A failed or interrupted production retains its checkpoint as an `OBSERVED`
containment artifact but cannot be resumed or cited for promotion. Start a new
run from a new explicit path after recording the failure.
