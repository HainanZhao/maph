# Cycle 32 flat-support modulation preregistration v1

## Claim boundary

This cycle may reduce an arbitrary reconstructed direction in the self-dual
block subspace to one dyadic amplitude level with near-flat coefficients and
quantify its prime-coordinate support. It may not prove the resulting
prime-Vandermonde bound, exclude any support exponent, close the skeleton
target, or promote density/interval consequences.

## Frozen dyadic reduction

Let `y in C^J` be unit, with `J=X^(4/25+o(1))`, and suppose

```text
||Ey-v||<=epsilon,
epsilon=exp(-X^(2/25-o(1))),
```

where `v` lies in the span of the scaled prime-phase rows. Discard indices
with `|y_j|<1/(2sqrt(J))`; their total squared mass is at most `1/4`.

Partition the remaining coordinates into dyadic bins

```text
2^(-ell-1)<|y_j|<=2^(-ell).
```

There are at most

```text
L=ceil(log_2(2sqrt(J)))+1=O(log X)
```

nonempty relevant bins. Freeze a bin `S` with squared mass

```text
mu^2=sum_(j in S)|y_j|^2>=3/(4L).
```

## Frozen flat direction

Project the reconstruction to the union of blocks in `S` and normalize:

```text
z_j=y_j/mu  (j in S),
d_S=sum_(j in S)z_j e_j.
```

If `s=|S|`, verify

```text
1/(2sqrt(s))<=|z_j|<=2/sqrt(s),
||d_S-mu^(-1)P_S v||<=epsilon/mu
 <=sqrt(4L/3)epsilon.
```

Thus the error remains `exp(-X^(2/25-o(1)))`.

## Frozen support ladder

Write `s=X^(lambda+o(1))`, with `0<=lambda<=4/25`. At the self-dual block
scale, one block has `X^(21/25-o(1))` primes. Register

```text
prime-coordinate support exponent =21/25+lambda,
row exponent                       =21/25,
per-prime coefficient magnitude    =X^(-(21/25+lambda)/2+o(1)).
```

At `lambda=0`, rows and prime coordinates have the same exponent `21/25`;
at `lambda>0`, the coordinate excess is exactly `lambda`.

## Checks

- Exact finite vector with `J=16`, including discarded mass, dyadic mass,
  normalization bounds, and projected-error amplification.
- Exact exponent table for `lambda in {0,1/25,2/25,3/25,4/25}`.
- CPython `3.12.3`, `Fraction`, no RNG/network; pin Cycles 29 and 31.
