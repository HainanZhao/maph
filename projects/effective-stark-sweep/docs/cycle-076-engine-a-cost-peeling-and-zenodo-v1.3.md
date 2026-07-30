# Cycle 076 — Engine-A cost anatomy, peeling, and Zenodo v1.3

Recorded: 2026-07-30T17:38:30Z

## Editorial result

Three bounded additions were made without changing the abstract,
Theorem 1, or the paper's higher-order headline.

1. The engine overview now distinguishes Engine A as the
   algorithmically closed exact-arithmetic stratum and Engines B/C as
   per-case certified-analysis mechanisms.
2. Remark 7 states the exact cost anatomy:
   - dominant per-character work is one quartic-field
     `bnfinit(P,1)` plus `bnfcertify`;
   - the remaining finite step is the \(2\times2\) regulator-index
     determinant;
   - a quadratic imprimitive Euler product is zero or a power of two;
   - the packet polynomial is obtained by an exact resultant in the
     compositum, with no floating-point recognition.
3. The census bridge now says why the quadratic queue is exhaustively
   verifiable and records the mixed-support peeling principle:
   evaluate and remove the quadratic Fourier slice exactly, then spend
   certified-analysis effort only on the higher-order residual.

No wall-time or unquantified speed claim was introduced.

## Verification and publication

- main manuscript: 18 pages, deterministic, zero warnings;
- supplement: 3 pages, deterministic, zero warnings;
- full referee audit: PASS;
- Engine A/B/C and structural-lemma replay: VERIFIED;
- tests: 127 expected after the v10 freeze update;
- main PDF remains the public default preview.

Public record:

- version: 1.3;
- DOI: `10.5281/zenodo.21708121`;
- concept DOI: `10.5281/zenodo.21703305`;
- companion: `effective-stark-results-companion-v13.tar.gz`;
- companion SHA-256:
  `1ecca96bd388ab2cafa27c091380121db4749e41ae794c2326439adbbe87b608`;
- full freeze: `artifacts/results-paper-full-freeze-v10.json`.
