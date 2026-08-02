# Cycle 25: excluding near-Cauchy prime recurrence

## Claim boundary

`PROVED`: the near-Cauchy alternative in Cycle 24 cannot occur for the full
dyadic prime phase vector at the frozen polynomial height, once `X` is
sufficiently large. The residual-singular and stretched-exponentially
ill-conditioned alternatives remain open. This cycle proves no skeleton,
zero-density, or prime-interval improvement.

## Phase concentration

Let `P_X` be the primes in `[X,2X]`, let `M=|P_X|`, and put
`z_p=p^(-ih)`. Suppose

```text
|M^(-1) sum_(p in P_X) z_p| >= 1-2 delta.
```

If `omega` is the phase of the mean, then the exact identity

```text
sum_p |z_p-omega|^2 = 2M(1-|M^(-1)sum_p z_p|)
```

gives a bound of `4M delta`. Hence each point is within
`2 sqrt(M delta)` of `omega`, and every pair obeys

```text
|exp(-ih log(p/q))-1| <= 4 sqrt(M delta) =: eta.
```

For a real `x`, choose its representative `theta=x-2pi ell` in
`[-pi,pi]`. Since
`|exp(ix)-1|=2 sin(|theta|/2)>=2|theta|/pi`, one has

```text
|x-2pi ell| <= (pi/2)|exp(ix)-1|.
```

Thus every prime ratio has angular error at most `(pi/2)eta`.

## Three-prime rigidity

The prime number theorem supplies, for all sufficiently large `X`, distinct
primes

```text
q in [X,11X/10],  p in [7X/5,3X/2],  r in [9X/5,19X/10].
```

After replacing `h` by `|h|`, which conjugates the phase sum but preserves
its modulus, set

```text
alpha=log(p/q),   beta=log(r/q).
```

Both lie in fixed compact subintervals of `(0,infinity)`. There are positive
integers `m,n`, each comparable with `h`, and errors `e_1,e_2` such that

```text
h alpha=2pi m+e_1,   h beta=2pi n+e_2,
|e_1|,|e_2| <= (pi/2)eta.
```

Eliminating `h` gives

```text
|n alpha-m beta| = |n e_1-m e_2|/h << eta.
```

This form is nonzero. Indeed, equality would imply

```text
(p/q)^n (r/q)^(-m)=1,
```

which is impossible for the three distinct primes `p,q,r` by unique
factorization.

## Explicit logarithmic-form contradiction

Apply Theorem 5.4 in Evertse's Chapter 5 notes, which states the explicit
rational case of Matveev (2000), with

```text
a_1=p/q, a_2=r/q, b_1=n, b_2=-m.
```

The rational heights are at most `2X`, while
`B=max(m,n)<<h<=X^(12/5+o(1))`. The theorem therefore yields

```text
|(p/q)^n(r/q)^(-m)-1| >= exp(-O((log X)^3)).
```

Writing `Lambda=n alpha-m beta`, the elementary inequality
`|exp(Lambda)-1|<=2|Lambda|` for `|Lambda|<=1` converts this into

```text
|Lambda| >= (1/2)exp(-O((log X)^3)).
```

(If `|Lambda|>1`, the desired lower bound is automatic.) On the other hand,
Cycle 24 freezes

```text
delta=exp(-k rho/8),   k rho=X^(6/25-o(1)).
```

Since `M<=2X`, the phase-concentration upper bound is

```text
|Lambda| << sqrt(M delta)
          = exp(-k rho/16+O(log X))
          = exp(-X^(6/25-o(1))/16).
```

This is smaller than `exp(-O((log X)^3))` for sufficiently large `X`, a
contradiction.

## Gate effect

`PROVED`: Cycle 24's near-Cauchy arm is closed for actual dyadic prime rows.
The surviving E8 alternatives are a negative normalized residual spectral
shift, a singular residual, or

```text
lambda_min(B) <= 2k exp(-k rho/8).
```

The next theorem must make the negative shift detectable against a
prime-specific reference, or prove a generalized-prime-Vandermonde lower
bound excluding the last two residual-dependence alternatives.
