# Cycle 010 — bounded W1 pilot result

Date: 2026-07-29

The preregistered parameter slice \(D\le13\),
\(N\mathfrak f\le12\) contains 66 Galois-deduplicated rows.
All 66 terminated and passed `bnfcertify`.

Exact structural routing:

| result | count |
|---|---:|
| Engine-A route candidate | 59 |
| Engine-B route candidate | 1 |
| Engine-C route candidate | 5 |
| frontier (`INDEX_GT_2`) | 1 |

The transcript is `artifacts/w1-pilot-v1.transcript`; the complete
records are `artifacts/w1-pilot-v1.json`.

This pilot deliberately does not fire the Phase-1 yield checkpoint.
None of its 65 candidates is counted as a new `PROVED` instance until
the engine-specific packet and identification gates close.  Its
research value is that it identifies a concrete next queue: first the
single B candidate, then the five C candidates, while the A queue gets
an exact conductor/regulator sieve.  Status:
`VERIFIED_STRUCTURAL_SCREEN`.
