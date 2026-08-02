# Cycle 87 preregistration: second-moment Mellin alias atlas

## Claim boundary

This cycle will derive the exact signed pair kernel, atom diagonal, and dual
Mellin alias trichotomy.  It will not prove the diagonal-strength second
moment, close a new Fourier band, prove a large-value theorem, packet
closure, density gain, or interval gain.

## Frozen conventions and ranges

- Use the Cycle-81 transform convention `e(x)=exp(2pi i x)`.
- `U in C_c^infinity((0,infinity))` is a fixed dyadic `k/K` weight, so
  `U(0)=0`.
- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`,
  `16/25<=xi<58/75`, and `K=X^(xi+o(1))`.
- Dual support: `r~K`, `h~KQ/D`.
- Pair variables use `Delta h=h-h'`; the stationary Poisson integer is `m`.

## Frozen gates

The cycle passes only if:

1. the primal second moment and Poisson pair kernel are derived with the
   frozen sign;
2. identical atoms contribute exponent `xi+14/15`;
3. the continuous pair kernel has zero mode `U(0)=0`;
4. the dual cross phase in `k` is
   `(D Delta h/(2pi))log k-mk` up to `k`-independent terms;
5. the stationary map is
   `k=D Delta h/(2pi m)` and its leading amplitude is
   `sqrt(D|Delta h|/(2pi))/|m|`;
6. nonzero stationary aliases require `|Delta h|>>K/D`;
7. the full support gives `1<=|m|<<Q`;
8. the unresolved moment is explicitly partitioned into same-`h`,
   nonstationary small-difference, and stationary-`m` branches.

## Verification plan

- Pin all signs, inverse maps, supports, and exponents in
  `conventions/mellin_alias_atlas_v1.py`.
- Independently test the stationary derivative, Hessian, amplitude, support
  ceiling, and diagonal target.
- Seal against Cycles 81 and 86.
- Defer hostile audit to paper stage.

