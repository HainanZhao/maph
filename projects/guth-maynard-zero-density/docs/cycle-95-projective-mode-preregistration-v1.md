# Cycle 95 preregistration: exact projective entropy modes

## Claim boundary

This cycle may prove the exact stationary equations for Poisson modes
`(u,v)`, the transcendence of `g=exp(2pi/D)` from the checked
Gelfond--Schneider theorem, and classification of exact stationary modes. It
may not infer a quantitative gradient lower bound, discard near-stationary
noncentral modes, close the alias branch, prove the moment, or promote a
density/interval gain.

## Frozen conventions

- Use the Cycle-94 phase `F` and `c=D/(2pi)`.
- Poisson modes enter as `cF-u h-v Delta` with `u,v in Z`.
- `g=exp(2pi/D)` and `c0=p0/q0>0` is a reduced rational anchor.
- `m,n,n'` are positive integers on the registered stationary supports.

## Frozen gates

1. Derive `F_h=2pi u/D` and `F_Delta=2pi v/D`.
2. Exponentiate and eliminate `h,Delta` to obtain
   `c0 n-c0 n' g^u-m g^(u+v)=0`.
3. Check Gelfond--Schneider with `alpha=-1`, `beta=-2i/D`, and the logarithm
   value `i*pi`, proving `g` transcendental.
4. Multiply the Laurent equation by a power of `g`; since `g` is
   transcendental, group equal exponents and classify every coincidence
   among `0,u,u+v`.
5. Using positivity, prove the only exact stationary mode is
   `u=v=0`, with `p0(n-n')=q0m`.
6. State the remaining target as a quantitative lower bound or inverse
   theorem for near-zero Laurent trinomials. Do not infer it from qualitative
   transcendence.

## Failure rule

Any branch of the exponent-coincidence split permitting a noncentral exact
mode, any unchecked complex-power branch, or any use of qualitative
transcendence as an effective lower bound halts the cycle.

