# Cycle 072 — results-paper referee must-fixes

Recorded: 2026-07-30 UTC

## Outcome

The current results manuscript is `ACTIVE`, not submitted.  The
referee must-fixes in this round are closed in
`artifacts/results-paper-full-freeze-v4.json`.  The deterministic PDF
has 17 pages.  The local companion is v7 and is not public.

## Mathematical and expository repairs

1. The abstract now reports the proved CM routes \(e=2,6,8\), not
   \(e=2,4,6,8\), and describes all five order-six rows without an
   ambiguous partial count.
2. Every manual `\tag` was removed.  Equations use labels and
   `\eqref`, eliminating the duplicate (32) and the former sequence
   defects.
3. The Fourier transform, inverse transform, Artin action, and
   compatible quartic generator conventions are explicit and are
   referenced from Engines A and C.
4. The zero-radius branch of the height lemma now states that the
   exact ray-field isomorphism pairs candidate and analytic values at
   the same nonsplit place.
5. The Voutier lower bound is mapped to the main theorem on p. 82 and
   its \(d\ge2\) range is stated.
6. The Engine-B proof now has an explicit completion marker linking
   the seven Section 4 cases and RQ-000458 to the selected-results
   theorem.
7. All bibliography entries in the current paper are cited.
8. Historical language now says only: the authors are not aware of
   previous unconditional one-place Stark packet identifications with
   support orders six or ten; the observation plays no role in the
   proofs.  The main paper no longer singles out Kopp.

## New exact Engine-A finding

The exact imprimitive-Euler audit covers all 1,560 Engine-A routing
rows:

- 2,232 supported quadratic-character occurrences;
- 672 zero Euler products;
- 603 affected rows;
- 346 rows in which all supported derivatives vanish, giving the
  empty product \(X_A=1\).

Evidence:

- `artifacts/engine-a-euler-degeneracy-v1.json`
- `scripts/audit_engine_a_euler_degeneracy.py`
- `scripts/screen_engine_a_euler_degeneracy.gp`

This does not alter the genuine v5 routing counts.  It creates a W4
obligation for the census paper: report routing support and effective
derivative support separately.

## Replays and frozen local artifact

- manuscript audit: `RESULTS_PAPER_FULL_AUDIT=PASS`;
- companion verifier: Engines A/B/C and structural lemmas all pass;
- deterministic PDF rebuild: byte-identical under
  `SOURCE_DATE_EPOCH=1785420000`;
- local archive:
  `dist/effective-stark-results-companion-v7.tar.gz`;
- archive SHA-256:
  `5856e4765f8006753a1fc5ff0ef3616f57f026a8e01b70f21d55c3c644547ba1`;
- public DOI: none;
- publication action: none.

## Remaining gate

One fresh human referee pass remains before public deposit.  No
Zenodo or arXiv action was taken in this cycle.
