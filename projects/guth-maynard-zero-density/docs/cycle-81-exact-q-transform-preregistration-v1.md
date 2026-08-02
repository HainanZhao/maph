# Cycle 81 preregistration: exact q-transform

## Claim boundary

This cycle will test only the smooth weighted Cycle-79 transform and its
uniform remainder.  It will not claim cancellation in the dual sum, closure
of the remaining Fourier range, packet closure, a density gain, or an
interval gain.

## Frozen conventions

- `e(x)=exp(2 pi i x)` and `beta=2 pi`.
- Fourier transform:
  `hat V(y)=int_R V(t)e(-yt)dt`, hence
  `V(a)=int_R hat V(y)e(ay)dy`.
- `W,V` are fixed `C_c^infinity` functions supported inside a fixed compact
  subinterval of `(0,infinity)` and extended by zero.
- Central indices satisfy `r~k`, `a=hD/(beta Qr)` in a fixed compact subset
  of `(0,infinity)`, and `Qr>=2`.
- The frequency range is `1<=k<=X^(83/75+o(1))`, with
  `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`.

## Frozen gates

The cycle passes only if all of the following are derived under the frozen
conventions:

1. exact change-of-variables identity before approximation;
2. leading term
   `D/(beta r) W(beta^-1 log(r/(kc0)))
    V(hD/(beta Qr)) e((hD/beta)log(kc0/r))`;
3. central error `O_(W,V)(D/(Qr^2))`, uniformly in the stated support;
4. summed central error `O_(W,V)(1)` per `k`;
5. nonstationary Poisson tails `O_A(X^-A)` after fixed support enlargement;
6. accumulated error exponent `83/75`, strictly below `31/25` by `2/15`.

Any failed item contains the transform claim.  A sign mismatch is corrected
from the frozen Fourier convention, not by changing the convention.

## Verification plan

- Pin the algebra and exponent ledger in `conventions/exact_q_transform_v1.py`.
- Test the forward transform sign, Fourier-inversion sign, support map,
  pointwise error scale, summed error, and strict margin independently.
- Seal a deterministic JSON artifact whose inputs include this
  preregistration, the discovery candidate, Cycle 79, and Cycle 80.
- Research-stage checks remain lightweight; hostile audit is deferred until
  a manuscript theorem is frozen.

