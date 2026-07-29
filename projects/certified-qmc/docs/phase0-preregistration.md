# Phase-0 preregistration

Date frozen: 2026-07-29

## Objective

Establish one executable exact ground truth before implementing CRT,
NTTs, Arb comparisons, or a production CBC search.

## Frozen mathematical target

- Quantity: squared shift-averaged worst-case error.
- Space/convention: product-weight unanchored Sobolev,
  `DKS2013-eq5.13-beta0-product-B2`.
- Smoothness scope: the `B2` kernel only.
- Inputs: \(N\ge2\), integer generator, nonnegative rational weights.
- Exact output: one reduced rational plus denominator and summand
  certificates.

No generic “Korobov alpha=2” input is accepted during Phase 0 because
that phrase does not uniquely fix the \(2\pi^2\) normalization.

## Frozen external audit target

The first table target is Frances Kuo's fixed rule
`lattice-29102-1024.3600`:

- \(N=1024\);
- product weights \(\gamma_j=1/j^2\);
- 3,600 components upstream;
- downloaded size 57,600 bytes and 3,600 lines;
- SHA-256
  `d42503eda84c7fede8d2513d674a9eca4075041dc4cf8c2e0995b46b035b5ce9`.

The first 16 components are frozen in `data/phase0-targets.json`.
Initial certification dimensions are 2, 4, 8, and 16. The full table is
not claimed vendored or audited.

## Acceptance gates

Phase 0 passes only if:

1. the single-sum result equals an independently enumerated RKHS
   double sum on every small regression case;
2. every reduced denominator divides the derived rational-weight
   master denominator;
3. binary64 agrees with exact conversion within \(2\times10^{-14}\)
   on 100 pseudorandom cases from seed `20260729`;
4. certificate replay reproduces the complete deterministic core
   payload and detects mutation;
5. exact CBC decisions minimize every candidate score in a small
   exhaustive oracle;
6. candidate sign symmetry is explicitly quotiented;
7. the cited reference NTT prime, factorization, 2-adic valuation, and
   primitive root pass an independent exact audit.

## Non-gates and deferred claims

- Existing certified-QMC novelty: `OPEN_LITERATURE_AUDIT`.
- Full upstream table audit: deferred to Workstream B.
- CRT reconstruction and prime count: deferred until a numerator bound
  is proved.
- Fast CBC complexity and wall time: `PROJECTED`, not an acceptance
  fact.
- Arb dependency and nonrational metrics: Phase 1.
- Exact-tie escalation rate: measured only after all known exact
  symmetries are quotiented.
- Finance/UQ pilot: no work before an explicit function-space membership
  argument is selected.

## Halt and escalation rules

- Any mismatch between the single and double sums halts implementation.
- Any upstream checksum change creates a new target version; it does
  not silently update this record.
- Any claimed table discrepancy is independently replayed before
  contact with maintainers.
- No exact-versus-published merit subtraction is performed until the
  timestamped Workstream B discrepancy protocol and a source-specific
  certified production/formatting error bound are frozen.
- Any performance estimate that differs by more than a factor of two
  from measurement is corrected before scale-up.
- If a maintained certified implementation already covers A1/A3, the
  project pivots to audit interoperability, Arb metrics, and
  number-theoretic constructions.
