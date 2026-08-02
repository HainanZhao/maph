# Cycle 79 preregistration: sublattice-aware double B-process

## Question

Derive the exact Fourier/Poisson contract for the Cycle-77 anchored saddle
without replacing its anisotropic mesh by a common denominator. Identify the
dual lattice, phase, determinant, amplitude, frequency ceiling, and low-
frequency boundary before attempting an estimate.

## Frozen setup

- `D=Delta=X^(3/5)`, `Q=X^(1/3)`,
  `eta=X^(-83/75)`, and packet target `X^(2/15)`.
- Use smooth compact dyadic weights in `d/D` and `q/Q`, and
  `e(z)=exp(2pi i z)`.
- The phase is `phi_k(d,q)=k c_0 q exp(beta d/D)`, `beta=2pi`, with `c_0`
  in a frozen compact positive interval.
- A band-limited nonnegative tube majorant has Fourier support
  `k<=eta^-1`.

## Exact checks

1. Derive the Fourier `L1` target after the factor `eta`.
2. Write the exact two-dimensional Poisson integral and solve both stationary
   equations with their inverse map.
3. Derive the primal Hessian determinant, stationary amplitude, Legendre
   phase, dual support exponents, and the Hessian of the dual phase.
4. Separate `k<D/Q`, where the positive `h` stationary range is empty, from
   the high-frequency dual branch.
5. Compare the maximum dual `h` scale with the independently frozen
   `X^(21/25)` prime-row skeleton scale.

## Outcomes

- `DOUBLE_B_GEOMETRY`: seal the exact transform geometry and leave uniform
  stationary errors and the dual sum estimate open.
- `DOUBLE_B_CLOSURE`: additionally prove a strict `X^(31/25)` raw Fourier
  bound and close the critical cell.
- `TRANSFORM_CORRECTION`: any map, sign, scale, determinant, or boundary
  assertion fails; record its correction.

No density or interval gain follows unless the critical and remaining atlas
cells close with strict margins.
