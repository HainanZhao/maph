# Cycle 66 preregistration: primitive packet Poisson dual

## Question

Dualize the depth-packet census without dropping the coprimality of the
approximating numerator and denominator. Determine the exact diagonal scale,
off-diagonal target, and frequency ceiling.

## Frozen setup

- `Delta=X^(3/5)` and `alpha_ell=exp(2pi ell/Delta)-1`.
- `q=X^(theta+o(1))`, `K=X^(kappa+o(1))`, with
  `theta+kappa<=11/25`.
- A packet satisfies `(a,q)=1` and
  `|q alpha_ell-a|<=C/(KX)`.
- The dyadic packet-count target is exponent strictly below `6/25-kappa`.
- Use a fixed nonnegative band-limited majorant `f_C>=1` on `[-C,C]` and
  apply the divisor identity `1_((a,q)=1)=sum_(b|(a,q)) mu(b)` before
  Poisson summation.

## Outcomes

- `PRIMITIVE_POISSON_CONTRACT`: derive an exact Möbius--Poisson expression,
  verify the diagonal exponent and its margin, and derive the normalized and
  raw off-diagonal targets and the maximum Fourier frequency.
- `PRIMITIVITY_LOST`: the proposed dual necessarily counts nonprimitive
  rational multiples at leading scale.

No estimate for the off-diagonal form, packet discrepancy theorem,
recurrence theorem, powered saving, density gain, or interval gain is
asserted by `PRIMITIVE_POISSON_CONTRACT`.
