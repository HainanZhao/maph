# Cycle 111 preregistration: exact `k`-stationary normalization correction

Date frozen: 2026-08-02 UTC.

## Trigger

Cycle 108 records `k*=c*c0*Delta/m`, whereas the Cycle-87 differentiated
cross phase records `k*=c*Delta/m`. The sealed Cycle-108 files will not be
edited.

## Gates

1. Derive the `k` phase directly from the Cycle-81 column and its conjugate,
   including the constant `log(c0)` term.
2. Differentiate it symbolically and evaluate its stationary value and
   Hessian.
3. Recombine the three stationary values and compare with the sealed
   Cycle-94 entropy phase.
4. List every affected and unaffected claim. In particular, do not preserve
   a cutoff claim merely because scale invariance survives.
5. Freeze a versioned correction artifact and replay Cycles 94, 107, 109,
   and 110. Cycle 108 itself remains immutable and is cited as corrected.

## Outcomes

- `LOCATION_ONLY_CORRECTION`: the point changes but the entropy, Hessian,
  Jacobian scale law, and later scale/split sums survive.
- `DOWNSTREAM_INVALIDATION`: halt and contain every dependent branch whose
  formula changes.
