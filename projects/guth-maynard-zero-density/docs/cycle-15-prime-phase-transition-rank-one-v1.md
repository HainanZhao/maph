# Cycle 15: phase transition and the rank-one semiprime target

## Claim boundary

`PROVED`: order `24/5` is the unique meeting point of two unavoidable prime
moment mechanisms, and prime large values reduce to a Guth--Maynard problem
with a symmetric rank-one semiprime coefficient matrix. `CONJECTURED`: that
rank-one restriction supplies a `4/25` saving in the prime-length scale.

No restricted large-value estimate, density gain, or zero-detector selection
theorem is proved here.

## 1. Why `24/5` is intrinsic

Let `m` be the number of primes in `[X,2X]` and
`P_a(t)=sum_p a_p p^(it)`, with `|a_p|=1`, on an interval of length
`H=X^(12/5)`.

`PROVED`: two different coefficient families force the lower scales

```text
coherent spike:       integral |P_a|^p >= c_p m^p,
random bulk:          integral |P_a|^p >= H m^(p/2)
                      for some deterministic a.
```

For the first, choose `a_p=p^(-it_0)`. In a fixed neighborhood of `t_0`, all
relative phases stay in a fixed short arc, so the sum has size comparable to
`m`. For the second, independent Steinhaus averaging gives the exact identity

```text
E_a |P_a(t)|^4 = 2m^2-m.
```

After integrating, select one coefficient vector with at least this fourth
moment and use monotonicity of normalized `L^p` norms.

Since `m=X^(1-o(1))`, any uniform moment theorem must accommodate

```text
max(X^p, X^(12/5+p/2)).
```

The branches meet only at `p=24/5`, where both have exponent `24/5`. Thus
the Cycle-14 moment target lies exactly at the transition between a planted
coherent spike and Gaussian-scale bulk. It cannot be improved by a fixed
power, even if true.

## 2. Eliminate the fractional power at the source interface

Squaring gives

```text
P_a(t)^2 = sum_p a_p^2(p^2)^(it)
         + sum_(p<q) 2a_pa_q(pq)^(it).
```

`PROVED`: the coefficient-square norm is exactly `2m^2-m`. More
importantly, away from the explicit diagonal the coefficients form the
symmetric rank-one matrix `2aa^T`. Splitting `[X^2,4X^2]` into two dyadic
pieces costs only two colours, and a large value of `P_a` selects a piece
with size at least a constant multiple of `X^(7/5)`.

For either piece, put

```text
N=X^2,       T=X^(12/5)=N^(6/5),
V_Q=X^(7/5)=N^(7/10).
```

The three terms of the checked Guth--Maynard large-values theorem become

```text
X^(6/5),     X^(8/5),     X^(8/5).
```

The desired local count `v^(36/5)` equals `X^(36/25)`. Therefore the exact
source-facing conjecture is:

> At the critical `N^(7/10)` threshold and `N^(6/5)` time scale, symmetric
> rank-one semiprime coefficients improve both tied generic terms from
> `X^(8/5)` to `X^(36/25+o(1))`.

The required saving is `4/25` in `X`, or `4/5` in `v`. This formulation uses
only an ordinary squared Dirichlet polynomial. The global fractional moment
estimate is a sufficient route, not the theorem that must be proved.

## 3. Consequence for engine design

`OBSERVED`: “prime support” alone is not the structural input. An arbitrary
bounded matrix on semiprimes has no rank-one relation and remains within the
generic GM theorem. The exploitable datum is that the coefficient at `pq`
factors as `a_pa_q` and that the same vector occurs on both prime coordinates.

The next engine should therefore operate on the coefficient tensor before
the GM trace expansion discards it. Candidate forms are:

- a bilinear Gram matrix indexed separately by the two prime coordinates;
- a symmetric-square/exterior-square decomposition that quarantines repeated
  primes;
- a rank-one inverse theorem for simultaneous saturation of the two tied GM
  terms;
- a direct restricted weak-type argument at count `X^(36/25)`.

Any counterexample must preserve the common prime vector `a`, not merely the
semiprime support.
