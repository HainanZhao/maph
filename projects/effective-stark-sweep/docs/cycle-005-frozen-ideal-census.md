# Cycle 005 — exact ideal census backbone

Date: 2026-07-29

PARI enumerated every integral ideal of norm at most 100 in all 121
real quadratic fields with squarefree \(2\le D\le200\).  Every field
passed `bnfcertify`.

Raw ideal count: 13,939.  After exact conjugation and normalized-HNF
canonicalization: 8,200 one-place Galois-orbit representatives.

The result is `artifacts/frozen-ideal-census-v1.json`.  This is the
maximal-order ideal backbone.  Conductor-lowered nonmaximal-order
moduli remain a separate census layer; they have not been silently
identified with these 8,200 rows.  Status: `VERIFIED`.
