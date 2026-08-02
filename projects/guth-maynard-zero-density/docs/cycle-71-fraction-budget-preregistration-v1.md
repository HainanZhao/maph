# Cycle 71 preregistration: primitive-fraction budget

## Question

Before applying oscillatory estimates, use packet injectivity and the number
of available reduced fractions on one denominator scale. Determine exactly
which `(theta,kappa)` cells already satisfy the strict packet and weighted
pair targets.

## Frozen setup

- `q=X^(theta+o(1))`, `K=X^(kappa+o(1))`.
- The curve values lie in a fixed bounded interval, so `a=O(q)`.
- Cycle 64 makes primitive packets injective in their reduced fraction.
- The packet-count target is strictly below `X^(6/25-kappa)`.
- One packet has pair-weight exponent `11/25+kappa`.

## Outcomes

- `FRACTION_WEDGE_CLOSED`: derive the primitive-fraction count and identify
  an open region with a strict pair-census margin.
- `NO_WEDGE`: the fraction budget never improves the registered target.

No assertion is made on the boundary without a separate strict margin. No
powered, density, or interval gain is asserted by `FRACTION_WEDGE_CLOSED`
alone.
