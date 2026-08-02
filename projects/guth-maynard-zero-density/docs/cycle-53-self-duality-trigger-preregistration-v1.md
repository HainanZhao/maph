# Cycle 53 preregistration: when does self-duality trigger?

## Question

Compare the Cycle 52 one-shot Halász--Montgomery diagonal with the weakest
dyadic row/value class forced by failure of `AMPR_s`.

## Frozen rules

- `AMPR_s` target exponent is `s+31/10`.
- Selecting one of `X^(3/10)` harmonic orders yields
  `r+2v>=s+14/5`, where `R=X^r` and `V=X^v`.
- Coefficient square norm and distinct support both have exponent `s+1`.
- A one-shot off-diagonal is forced only if
  `r+2v>2s+2`.
- Evaluate `s=3,4`; state the exact missing trigger exponent.

## Outcomes

- `TRIGGERS`: `AMPR_s` failure itself forces a large factored difference
  kernel.
- `NEEDS_MULTILINEARIZATION`: the one-shot diagonal is too large; preserve
  Cycle 52 but redesign the inequality coordinate-by-coordinate or by a
  centered higher trace.

No route is terminated by the second outcome, and no analytic gain is
promoted without the redesigned inequality.
