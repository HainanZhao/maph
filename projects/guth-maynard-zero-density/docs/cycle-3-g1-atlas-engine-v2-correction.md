# Cycle 3 G1 finite-probe engine v2 correction

Date: 2026-08-01 UTC.

## Claim boundary

`OBSERVED`: the first v1 full-screen launch ended with no observation or
performance artifact. This is an operational containment event, not a failed
mathematical row and not evidence for or against any G1 route.

The exact evidence is frozen in
`artifacts/cycle-3-g1-atlas-first-launch-failure-v1.json`. The child PID was
live at approximately one CPU core and 27 MiB RSS, disappeared after the
launching agent finalized, and left no recoverable stderr or journal entry.
Rows `G1-S000` through `G1-S015` were subsequently invoked individually
without reproducing a nonzero row exit; that diagnostic was stopped before it
could become an unauthorized full retry.

`CONJECTURED`: lifecycle coupling to the agent execution session caused the
child termination. The unavailable stderr prevents promoting this causal
assessment. `OBSERVED`: v1 wrote only at final assembly, so any premature
termination necessarily discarded all completed-row progress.

## Contained v1 defects

Engine v1 is preserved at SHA-256
`78f5088cbe615237d565854428511cda03e22fc04838d192c64d3215748c28ee`.
It is not a release engine because:

1. it records but does not enforce the frozen CPython, Python, mpmath, and
   optimization-mode requirements;
2. it does not adjudicate the preregistered larger-scale score-loss falsifier;
3. an unexpected `Exception` aborts the entire run rather than becoming one
   retained failed row; and
4. it has no crash-safe phase checkpoint.

No v1 row semantics, source artifact, or failed launch is overwritten.

## v2 correction boundary

The successor `discovery/run_g1_atlas_v2.py` may reuse v1's pinned finite
constructors only after hashing v1 exactly. It must add explicit, optimization-
safe runtime checks; deterministic high-precision validation comparisons;
sanitized distinct unexpected-exception rows while allowing
`KeyboardInterrupt` and `SystemExit` to propagate; atomic per-row
checkpointing and atomic final assembly; and a deterministic replay/check
path. A full retry remains prohibited until hostile audit signs off.

Before any v2 complex screen is run, freeze the literal validation comparison:
`SCORE_LOSS_FALSIFIER` means that the 112-digit Decimal validation score is
strictly smaller than the corresponding recorded screen score. Equality is
`NO_SCORE_LOSS`; an invalid validation row is
`VALIDATION_EXECUTION_FAILURE`, not a numerical comparison. This operational
classification is `OBSERVED` finite evidence only.

The final timing-independent summary must expose scheduled, completed, failed,
and retained counts, every failure-code count, and feasible-row counts by the
declared low/intermediate/high regime. In particular, the already observed
finite construction outcome that all registered W0 rows fail must appear as
`NO_FEASIBLE_LOW_REGIME_ROWS` if reproduced. No construction is retuned, and
all 588 complex-screen schedules are still executed or retained as their
predeclared construction failure; the exact energy obstruction does not
authorize a short circuit.

These corrections alter operational robustness and falsifier reporting only.
They do not authorize a changed grid, family, set, seed, precision, threshold,
resource cap, or parameter-changing retry.
