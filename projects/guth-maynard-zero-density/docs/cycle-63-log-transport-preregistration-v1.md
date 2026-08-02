# Cycle 63 preregistration: averaged logarithmic transport census

## Question

Convert E13's instruction “average over `h` before maximizing in `beta`”
into an exact two-dimensional lattice census, compute its curvature and
exponent targets, and derive the beta-free differenced pair problem.

## Frozen scales

- `Delta=X^(3/5)` and `H=X^(11/25)`.
- `h` ranges over one dyadic interval `[H,2H]`.
- `1<=ell<=c Delta`, with fixed `0<c<1`.
- `alpha_ell=exp(2pi ell/Delta)-1`.
- The subunit strip is `|j+beta-h alpha_ell|<=C/X`.
- The desired average wrap exponent is strictly below `1/5`, equivalent to
  total census exponent strictly below `16/25`.

## Outcomes

- `TRANSPORT_REDUCTION`: the summed inverse-log count is equivalent to the
  triple strip census; the surface Hessian determinant is a nonzero negative
  square, and differencing in `h` removes `beta` exactly.
- `REDUCTION_FAILS`: the inversion, exponent target, or differencing identity
  does not hold under the frozen scales.

No two-dimensional lattice estimate, powered saving, `LCAM_s`, density gain,
or interval gain is asserted by the first outcome.
