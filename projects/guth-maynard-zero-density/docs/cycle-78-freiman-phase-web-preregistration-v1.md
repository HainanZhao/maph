# Cycle 78 preregistration: exact Freiman phase web

## Question

At the critical cell, determine whether the packet accuracy is strong enough
to turn additive relations among curve indices into exact multiplicative
relations among primitive rational labels. Classify the image of a complete
arithmetic progression and bound its possible length from rational height.

## Frozen setup

- Retain Cycle 77 scales `Q=X^(1/3+o(1))` and
  `eta=X^(-83/75+o(1))` in `|n-qE_ell|<=eta`.
- Use reduced labels `r_ell=n/q`, with numerator and denominator both
  `X^(1/3+o(1))` on the compact critical cell.
- For four hits with `ell_1+ell_2=ell_3+ell_4`, compare
  `r_1r_2-r_3r_4` with the exact exponential identity.
- Promotion requires the cross-multiplied error to be `X^-delta` for an
  explicit `delta>0`; a floating-point near equality is insufficient.

## Outcomes

- `EXACT_FREIMAN_WEB`: every additive quadruple gives exact multiplicative
  equality, and a complete arithmetic progression of hits has logarithmic
  length.
- `APPROXIMATE_ONLY`: the cross-multiplied error does not beat one, so retain
  only an approximate relation with its exact margin.

The result does not assert that a packet set of size `X^(2/15)` contains an
arithmetic progression or has large additive energy. No ACSI, packet closure,
powered saving, density gain, or interval gain follows automatically.
