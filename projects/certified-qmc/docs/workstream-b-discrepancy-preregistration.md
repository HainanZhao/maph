# Workstream B discrepancy preregistration

Frozen at: **2026-07-29T04:24:47Z**

Status at freeze: no published lattice-merit value had been acquired or
compared. The existing UNSW artifact contains generating-vector
components only. Cycles 005 and 008 compared independent internal
evaluators; neither performed an exact-versus-published merit
comparison.

## Frozen classification rule

Let \(q\) be the exact rational merit after an explicit, audited
conversion into the source's published normalization. Let \(y\) be the
published lexical value interpreted exactly as a decimal rational. Let
\(B_{\rm alg}\) be a certified absolute error bound for the complete
floating-point production path that generated \(y\), including input
rounding, operation order, arithmetic rounding, library operations, and
the final published formatting/rounding step.

> A published value is a discrepancy finding only if
> \(\lvert y-q\rvert>B_{\rm alg}\). Everything inside that bound is
> expected rounding.

Equality with the bound is classified as expected rounding. Binary64
closeness, a decimal-digit heuristic, or agreement after an unstated
rounding convention is not a substitute for \(B_{\rm alg}\).

## Admission gate for an external comparison

Before reading or computing against a published merit value, the audit
checkpoint must freeze:

1. source URL, version, retrieval timestamp, file hash, and the exact
   published lexical value;
2. kernel, weight, and error-versus-squared-error normalization;
3. source algorithm and operation order, including software revision,
   compiler/library versions, and rounding mode;
4. output formatting convention and number of published digits; and
5. a replayable outward-rounded derivation of \(B_{\rm alg}\).

If any item is unavailable, the result is `UNCLASSIFIED_EXTERNAL`, not a
discrepancy and not a clean audit. A source value may be recorded for
provenance, but no subtraction from the exact result is performed until
the gate is complete.

## Prospective amendment

For future unseen targets after **2026-07-29T06:08:09Z**, the
source-specific historical-pipeline requirement above is superseded by
`workstream-b-classification-v2`.  The new rule envelopes an explicit
class of plausible evaluators and deletes CBC selection from
\(B_{\rm alg}\).  This note does not retroactively alter the original
freeze or rehabilitate the quarantined example.

## Standing stop

No further Workstream B merit computation is authorized until this
preregistration and its machine-readable checkpoint replay. Any future
change creates a new version with a later timestamp and cannot be
applied retroactively to data already inspected.
