# Cycle 48 preregistration: Huxley--Sargos inside the joint large sieve

## Question

Insert the Cycle 47 local wrap count into the Cycle 45 colouring argument and
compute the exact joint-sum saving for every Fourier exponent
`0<=nu<=11/25`.

## Frozen inputs and rules

- `Delta=X^(3/5)`, prime support and coefficient-square norm exponents one.
- Cycle 47 order-three count:
  `A(h)<=min(h, X^(1/10)h^(1/2)) X^o(1)` for `h=X^nu`.
- With local multiplicity `A=X^a`, use all terms of
  `A(X+Delta/h)X^(1+o(1))`; do not discard the second term before comparing
  exponents.
- Apply Cauchy--Schwarz over `X^(3/5)` resonance indices and compare the
  saving with `2/25`, `7/50`, `4/25`, and `17/50`.

## Outcomes

- `CLOSES_AUXILIARY`: the saving reaches a registered Cycle 39 margin.
- `PARTIAL`: it improves `2/25` but reaches neither margin.
- `NO_GAIN`: it does not improve Cycle 45.

Even `CLOSES_AUXILIARY` does not promote `LCAM_s`, a zero-density estimate,
or a prime-interval theorem without an exact bridge through the full
localized-comb off-diagonal expansion.
