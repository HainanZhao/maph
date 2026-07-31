# Census-paper preregistration amendment v5: corpus synthesis cap

Frozen: 2026-07-31 UTC, after the preregistered height-only calibration
and before the first corpus packet-polynomial run.

The calibration artifact
`artifacts/census-packet-height-calibration-v1.json`, SHA-256
`cf62dc8df82b500a9483b83b2216c65bcd81ea870e6d8d80418995777afb9e5b`,
contains all 1,560 Q rows.  It opened no analytic packet target and
constructed no packet polynomial.

Its largest coefficient-digit predictor is 89, at RQ-005284.  Applying
the frozen amendment-v4 rule gives a corpus cap of **256 decimal
digits**.  This cap is now immutable for the v1 corpus run.

## Exact runtime gate

For every coefficient in the selected polynomial over the fixed
quadratic power basis, reduce each rational coordinate and count the
decimal digits of the absolute numerator and denominator, with zero
counted as one digit.  The maximum must be at most 256.

The per-row gates are:

1. exact Engine-A conductor, Euler factor, certified quartic field,
   norm-one unit, determinant index, exponent, and orientation;
2. exact effective character relation and Artin sign image;
3. trace-resultant synthesis of the denominator-cleared formal orbit;
4. exact identity-class product in the full ray field and unique factor
   selection from \(P(X^q)\);
5. orbit degree, reciprocity, positivity at the frozen split place,
   squarefreeness, and irreducibility over \(K\);
6. the 256-digit exact coefficient gate;
7. 2 GiB peak resident memory and 300 seconds wall time per row.

All-zero rows emit \(X-1\) directly, with their zero-Euler evidence.
No failing row is dropped.  A resource or mathematical failure is
recorded under the stable RQ id and the affected corpus theorem remains
open; it does not authorize a different method.
