# Cycle 4 P1R preregistration v3 lifecycle correction

## Claim boundary

`OBSERVED`: v3 preserves the v1 and v2 artifacts and both hostile `FAIL`
audits.  It corrects only replay lifecycle: historical preregistration replay
validates the immutable authorization snapshot and frozen source records, and
does not inspect the mutable current Plan.  V3 proves no P1R-FS obstruction,
large-values, density, short-interval, compatibility, extremizer, or
saturation theorem.  CRR discovery/search remains prohibited.

The v2 hostile audit established that v2 replay improperly depended on live
P1R being `ACTIVE` and no P2 route being selected.  Both conditions are
expected to change during legitimate program progress.  V3 treats that audit
as a preserved historical `OBSERVED` failure record, rather than rewriting it.

## Historical replay

From the project root, the documented command is exactly:

```sh
python3 proof/build_cycle_4_p1r_preregistration_v3.py --check
python3 -m unittest tests/test_cycle_4_p1r_preregistration_v3.py -v
```

The builder has no current-Plan input or predicate.  Its byte identity is
therefore independent of future transitions such as `P1R ACTIVE` to
`COMPLETE`, or a later affirmative P2 selection.  It validates the immutable
authorization snapshot's recorded historical Plan hash and the frozen source
files only.  `--write` refuses to overwrite the versioned artifact; `-O` and
`-OO` fail closed because the pinned runtime requires non-optimized CPython
3.12.3.

## Separate operational preflight

`proof/preflight_cycle_4_p1r_current_plan_v1.py` is an `OBSERVED`, replaceable
operational eligibility check.  It intentionally reads a supplied current
Plan path and reports whether P1R remains operationally eligible.  Its result
is not a proof, is not a frozen v3 input, and is not required to reproduce
the v3 historical bytes.  For example:

```sh
python3 proof/preflight_cycle_4_p1r_current_plan_v1.py --plan PLAN.md
```

The preflight is expected to change result when P1R completes or a P2 route is
selected; those changes must not affect historical replay.

## Preserved source and status corrections

`PROVED` as exact algebra only:

\[
\frac{30}{13}-\frac3{2-\sigma}
=\frac{30(7/10-\sigma)}{13(2-\sigma)}.
\]

`OBSERVED`: P1R-FS is still `PREREGISTERED_UNEXECUTED`; no scoped obstruction
theorem is recorded.  `PROVED` as source-statement inspection: the separate
refined two-term source is GM `prpstnS3`, while the four-term critical scale
source is GM `prpstn:S3`, with its checked condition
\(N\geq T^{3/4}\).  `CONJECTURED`: CRR remains only a proposed direction;
its formalization gate authorizes no search.
