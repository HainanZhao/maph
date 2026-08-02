# Cycle 177 working ledger: actual-curve primitive rays

## Frozen question

See `docs/cycle-177-actual-curve-census-preregistration-v1.md`.

## Candidate invariant

`PROVED` input from Cycle 64: every fixed-label hit set is a single primitive
ray together with a multiplier interval.  Cycle 177 tests the missing
actual-curve fact: a rational-root label can carry the full multiplier bank.

## Work log

- `PROVED` candidate ledger: for fixed `r` and
  `Delta_L=2pi L/log(1+1/r)`, the label `ell=L` has `alpha=1/r`.  Its
  `d=kr` pair bank has weight at least `H^2/(8r)`, hence exponent `22/25`.
  The proof still needs sealing in the Cycle 177 record.
- `PROVED` candidate ledger: its beta-zero label contributes `H/r+O(1)` exact
  triple rows and has a central seeded `(a,q)=(1,r)` packet of depth
  `floor(H/(4r))`; both have exponent `11/25`.  This is the label's
  contribution, not a bound for the full census.
- `RECOGNIZED`: the frozen 100-digit scan for `r in {1,2,3,5,8}` and
  `L in {10,100,1000}` returned every label admissible for `c=1/4`, every
  multiplier accepted, and residuals at most `3e-100`.  It is a sanity check,
  not evidence for the symbolic identity.
- `PENDING`: state the replacement analytic target: diagonal-aware triple
  census or heavy-packet-to-seeded-recurrence routing.

## Rejected routes

None yet.

## Consequence under test

`CONJECTURED`: no uniform proof of the raw Cycle-63 pair target can be valid
when the continuous `Delta` scale is unrestricted.  The replacement must
separate heavy seeded packets from the diagonal-aware direct triple census;
the present construction supplies the first exact structured exception.
