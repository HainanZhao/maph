# Cycle 68 preregistration: folded-frequency baseline

## Question

Fold the Cycle-66 primitive Poisson form by the composite frequency
`m=rq'`. Bound the resulting coefficients without Möbius cancellation and
measure the exact gap between a generic separated-point large sieve and the
raw `31/25` target.

## Frozen setup

- `theta+kappa<=11/25` and `M=KXQ=X^(1+theta+kappa+o(1))`.
- The curve has `Delta=X^(3/5)` points and fixed total range, with spacing
  `asymp Delta^(-1)` before a constant number of modulo-one colour classes.
- The raw primitive-Poisson target is exponent strictly below `31/25`.
- No cancellation in `mu(b)` may be assumed in the baseline.

## Outcomes

- `FOLDED_BASELINE`: prove a divisor bound for the folded coefficient,
  derive its square norm, and compute the exact generic large-sieve exponent
  and deficit to target.
- `COEFFICIENT_EXPLOSION`: folding creates coefficients larger than a
  divisor bound by a fixed power.

No improved exponential-sum estimate, packet theorem, recurrence theorem,
powered saving, density gain, or interval gain is asserted by
`FOLDED_BASELINE`.
