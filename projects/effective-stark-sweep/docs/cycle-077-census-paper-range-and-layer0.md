# Cycle 077 — census-paper range freeze and Layer-0 reconciliation

Date: 2026-07-30 UTC

The One-Place Stark Census paper now has a frozen executable plan.
Its theorem universe is the existing maximal-order backbone:
squarefree radicands \(2\le D\le200\), every nonzero integral ideal of
norm at most 100, and one representative of each conjugate one-place
pair. A clean PARI rerun reproduced 121 fields, 13,939 raw ideals, and
8,200 representatives with a byte-identical mathematical payload
after removing the run timestamp.

The support-first reconciliation found
\[
  8200=3936_{\rm T}+1560_{\rm Q}+2704_{\rm H}.
\]
This supersedes the use of census v5's routing histogram as a
trichotomy theorem. V5 labeled 3,899 rows `PROVED_TRIVIAL` and 1,628
rows `FRONTIER`; 37 of those frontier rows have exact empty Fourier
support and trivial sign class. They entered `EXPONENT_CAP` because
the v5 routing declaration applied the cap before the empty-support
theorem to W1 engine-`NONE` rows. No packet theorem is damaged. The
historical v5 artifact remains unchanged; the census paper uses 3,936
T rows and a 1,591-row higher-order frontier.

The quadratic stratum reconciles exactly: 1,560 rows, 2,232 supported
quadratic character occurrences, and 912 distinct quartic fields.
The exact imprimitive audit has 672 zero Euler products affecting 603
rows; all supported derivatives vanish in 346 rows. Those rows remain
in Q because the trichotomy is by Fourier support, although their
evaluated packet is \(X_A=1\).

The exact-resultant cap is frozen at absolute compositum degree 32.
The independent audit is frozen at 50 deterministically selected
Q-rows, initially 192-bit Arb precision, and a 38-decimal-digit
target. RQ-000013 is preselected as the fully worked imprimitive
\(E_\chi=2\) row before its exact unit extraction.

Evidence:

- `data/census-paper-preregistration-v1.json`;
- `artifacts/census-paper-layer0-reconciliation-v1.json`;
- `data/census-paper-imprimitive-worked-case-selection-v1.json`;
- `scripts/audit_census_paper_layer0.py`;
- `docs/census-paper-execution-plan-v1.md`.

Validation: 132/132 unit tests, full results-paper audit, and complete
results-companion replay all pass.
