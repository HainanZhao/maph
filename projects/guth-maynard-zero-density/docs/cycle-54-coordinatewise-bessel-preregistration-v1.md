# Cycle 54 preregistration: coordinatewise-Bessel design ledger

## Question

Assuming a coordinatewise Bessel contraction can remove one full support
power for each exposed ordinary prime coordinate, determine exactly how many
coordinates are required before failure of `AMPR_s` forces an off-diagonal.
Treat the powered `q^m` coordinate separately and insert the proved Cycle 48
joint-sieve saving `7/50` only there.

## Frozen rules

- After harmonic selection, `AMPR_s` failure gives
  `r+2v >= s+14/5`.
- The one-shot support trigger is `2s+2`.
- Exposing `j` ordinary prime coordinates changes the candidate trigger to
  `2s+2-j`.
- A source-valid treatment of `q^m` may additionally subtract `7/50`, but it
  does not count as an ordinary-coordinate contraction.
- Evaluate every `j=0,...,s` for `s=3,4`.
- A trigger is crossed only under a strict inequality.

The rule `2s+2-j` is a design contract for an analytic inequality still to be
proved. This cycle proves only the exact consequences of that contract.

## Outcomes

- `FULL_ORDINARY_EXPOSURE_NECESSARY`: even with `7/50`, `j=s-1` remains
  below the trigger, while `j=s` crosses it.
- `EARLY_TRIGGER`: fewer than all ordinary coordinates suffice.
- `CONTRACT_INSUFFICIENT`: even all ordinary coordinates do not suffice.

No outcome proves the coordinatewise Bessel inequality, `AMPR_s`, a density
gain, or a primes-in-short-interval result.
