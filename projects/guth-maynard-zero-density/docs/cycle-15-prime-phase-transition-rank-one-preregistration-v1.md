# Cycle 15 prime phase transition and rank-one semiprime preregistration v1

## Claim boundary

`OBSERVED`: Cycle 14 identified order `24/5` by continuous exponent
optimization. This cycle tests whether that order is an artefact, determines
the extremizers that make it sharp, and removes the noninteger-power language
from the source-facing large-value problem.

The cycle may prove finite moment lower bounds, exact exponent translations,
and an equivalence from prime large values to a restricted rank-one
semiprime coefficient problem. It may not prove the required restricted
large-value estimate, a new density theorem, or that the prime component is
selected on every zero row.

## Frozen scales and source input

Write

```text
X=v^5,          H=v^12=X^(12/5),
V=X^(7/10)=v^(7/2),       p_*=24/5.
```

Let `P_a(t)=sum_(p in [X,2X]) a_p p^(it)` with `|a_p|=1`, and let `m` be
the number of those primes. The exponent translation may use only
`m=X^(1-o(1))`, supplied by the already source-checked prime-number theorem
baseline. All finite identities are stated exactly in `m`.

Freeze the Guth--Maynard Theorem 1.1 source with SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.

## Frozen two-extremizer lower theorem

For every real `p>=4`, register two independent coefficient constructions.

1. Coherent spike. Given an interior point `t_0`, choose
   `a_p=p^(-it_0)`. On a fixed interval about `t_0`, all relative phases lie
   in an arc of length less than `pi/3`; hence

   ```text
   integral |P_a|^p >= c_p m^p.
   ```

2. Random bulk. Average over independent Steinhaus coefficients. For every
   fixed `t`,

   ```text
   E |P_a(t)|^4 = 2m^2-m.
   ```

   Therefore some deterministic coefficient vector has fourth moment at
   least `H(2m^2-m)`. Monotonicity of normalized `L^p` norms gives

   ```text
   integral |P_a|^p >= H^(1-p/4)[H(2m^2-m)]^(p/4)
                      >= H m^(p/2).
   ```

At exponent scale, every uniform `L^p` upper must therefore contain

```text
max(X^p, H X^(p/2)).
```

The branches cross iff `p=24/5`; at that point both equal `X^(24/5)`. Thus
the Cycle-14 target is simultaneously sharp against a coherent spike and a
random-bulk construction. The result is a lower-bound theorem, not an upper.

## Frozen rank-one semiprime reduction

Square the prime polynomial:

```text
P_a(t)^2 = sum_p a_p^2 (p^2)^(it)
         + sum_(p<q) 2a_pa_q (pq)^(it).
```

After division by two, every coefficient has modulus at most one. Split the
support `[X^2,4X^2]` into the two dyadic intervals `[X^2,2X^2]` and
`[2X^2,4X^2]`; at each large-value row one piece has modulus at least
`V^2/2`. A two-colour selection has constant cost.

The off-diagonal coefficient array is the symmetric rank-one tensor
`a tensor a`; the diagonal is separately explicit. Freeze the generic GM
translation for either dyadic piece:

```text
N=X^2,   T=H=X^(12/5),   V_Q=X^(7/5)=N^(7/10).
```

The three terms in GM Theorem 1.1 have `X`-exponents

```text
6/5, 8/5, 8/5.
```

The desired local exponent `v^(36/5)` is `X^(36/25)`. Hence the exact new
source-facing target is:

> Improve the tied `X^(8/5)` terms to `X^(36/25+o(1))` for dyadic
> semiprime polynomials whose coefficient matrix is symmetric rank one,
> at threshold exponent `7/10` and time exponent `6/5` in `N`-scale.

The required fixed saving is `4/25` in `X`-scale, equivalently `4/5` in
`v`-scale. A global `L^(24/5)` bound implies this target by Markov, but is not
declared equivalent; the restricted rank-one theorem is the weaker and
principal target.

## Registered structural tests

- Verify the exact coefficient-square norm
  `sum_n |coeff(P^2)_n|^2=2m^2-m`.
- Verify the phase-transition and all GM exponents with `Fraction` arithmetic.
- Verify that dropping rank one admits arbitrary bounded semiprime
  coefficient matrices and returns the generic architecture; no saving may
  be attributed merely to semiprime support.
- Preserve coherent and Steinhaus constructions as different extremizers.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact integers/Fractions, no
  RNG, third-party libraries, or network.
- Finite coefficient identities are enumerated for `1<=m<=12`; this is an
  identity check, not asymptotic evidence.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
