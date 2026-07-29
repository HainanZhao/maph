# Cycle 004 — modular merit and CBC branch certificates

Date: 2026-07-29

The direct modular evaluator now computes the scaled merit numerator
independently modulo each scheduled prime.  It takes the shortest prime
prefix whose product exceeds twice the proved signed bound and performs
a balanced CRT reconstruction.  Reduction of the resulting integer
fraction agrees with the independent `Fraction` oracle.

The CBC prototype applies the sharper candidate-difference bound to
every branch.  Its frozen \(N=31,d=5,\gamma_j=j^{-2}\) run:

- quotients the forced sign symmetry;
- reconstructs every winning merit exactly;
- records a modular proof that each candidate-minus-winner difference
  is nonnegative; and
- produces the same generator and final fraction as exhaustive rational
  CBC.

The certificate is
`certificates/cycle-004-crt-cbc-n31-d5.json`.
This is intentionally a direct \(O(dN^2)\) modular oracle.  It validates
the representation, bounds, prime selection, signed reconstruction, and
branch semantics; it does not claim fast-CBC production performance.

Decision: **CONTINUE to measured implementation work**.

Tag: `VERIFIED`.
