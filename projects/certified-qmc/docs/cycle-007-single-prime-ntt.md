# Cycle 007 — single-prime radix-two NTT

Date: 2026-07-29

The first audited 62-bit prime and its primitive root now drive a
transparent iterative radix-two NTT. The implementation validates:

- normalized forward/inverse round trips;
- cyclic convolution against a quadratic definition; and
- the plus-shift correlation
  \(C(a)=\sum_t A(t)B(t+a)\) required by CBC scoring.

Frozen deterministic convolutions at lengths 1 through 256 replay by
digest in `certificates/cycle-007-ntt-validation.json`. This gate proves
the transform semantics over one prime. It does not claim an optimized
or constant-time implementation.

Decision: **PASS to group mapping**.
