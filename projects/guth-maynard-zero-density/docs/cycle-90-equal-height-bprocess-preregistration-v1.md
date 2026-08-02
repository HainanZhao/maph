# Cycle 90 preregistration: equal-height B-process contract

## Claim boundary

This cycle may prove the exact equal-height quadratic form, its smooth
one-dimensional B-process, the resulting exponent ledger, and the affine
saddle-collision target.  It may not promote the required collision bound,
the full diagonal second moment, a new Fourier band, a density gain, or an
interval gain.

## Frozen ranges and notation

- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`, `K=X^(xi+o(1))`.
- `16/25<=xi<58/75` and `H=KQ/D`.
- Fourier convention `e(x)=exp(2pi i x)`, `beta=2pi`.
- The Cycle-81 leading amplitude and supports are used without changing
  signs: `r~K`, `h~H`, amplitude `D/(beta r)`.
- All weights are fixed smooth functions supported on fixed positive dyadic
  intervals; transition charts use smooth zero extension.

## Frozen gates

1. Expand the exact same-`h` quadratic form as
   `sum_k U(k/K) sum_h |sum_r A_(k,h,r)|^2`.
2. Verify that its same-`r` diagonal has exponent `xi+14/15`.
3. For `t=hD/beta`, Poisson/stationary phase in `r` must have stationary
   index `n=t/r~Q`, stationary point `r=t/n`, phase
   `t(1-log(t/n))`, Hessian `n^2/t`, and amplitude `sqrt(t)/n`.
4. Verify the dual length exponent `1/3`, sample exponent
   `xi-4/15`, and surplus `H/Q=K/D=X^(xi-3/5)`.
5. After expanding the dual square and Poisson localizing the `h` sum, derive
   the collision
   `|n'-n exp(beta*a/D)|<<1/K`, with `a~D`.
6. Verify collision volume exponent `14/15-xi`, target exponent `1/3`, and
   strict target-over-volume margin `xi-3/5>=1/25`.
7. Compute the Hessian of `F(a,n)=n exp(beta*a/D)` and verify
   `det Hess F=-(beta^2/D^2)exp(2beta*a/D)`.
8. State the sufficient analytic target: a Schwartz-weighted collision
   bound `X^(1/3+o(1))` on every fixed annulus.

## Failure rule

Any sign mismatch, nonpositive surplus at `xi=16/25`, failure of the B-
process remainder to lie below the diagonal target, or Hessian degeneracy
halts the cycle.  No range or endpoint may be changed after calculation.

