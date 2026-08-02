# Cycle 29 polynomial block-subspace preregistration v1

## Claim boundary

This cycle may take a polynomial-dimensional block-constant detector
subspace, exclude a half-sized near-subspace packet by blockwise logarithmic
forms, and retain a rank-J shift/reconstruction trichotomy. It may not exploit
the reconstructed block modulation, exclude exact row dependence, prove the
skeleton target, or promote density/interval consequences.

## Frozen block scale and source input

Set

```text
kappa=1/25,
J=2^floor(log_2 X^kappa)=X^(1/25+o(1)).
```

Partition `[X,2X]` into `J` consecutive equal-length intervals. On each
nonempty block, let `e_j` be the normalized restriction of the unimodular
prime coefficient vector `a`; let `E` have columns `e_j`. Then `E*E=I_J` and
the normalized original detector `b=a/sqrt(M)` belongs to `range(E)`.

Use the already checked baseline uniform PNT (`17/30`) only to guarantee
asymptotic prime counts in each block and in three fixed separated
subintervals of a block. Since block length is `X^(24/25+o(1))`, this lies
well inside the checked range. Pin

```text
artifacts/g0-theorem-dependency-graph-v1.json
SHA-256 14f80b35774a3994c93e1a08de34afb2aefff7023e1797932e6fb4d78af1281b
```

## Frozen no-loss projection

For every normalized prime phase row `x_t`, original detector largeness gives

```text
||E*x_t||^2 >= |<x_t,b>|^2 >= rho=X^(-3/5-o(1)).
```

Thus enlarging the common direction to the block subspace costs no factor of
`J` in projection strength.

## Frozen near-subspace exclusion

Freeze

```text
delta=exp(-k rho/8).
```

If at least half the skeleton rows satisfy
`dist(x_t,range(E))^2<=delta`, choose two such rows with difference
`X^(3/5)<=|h|<=X^(12/5)`. On every block, each row is within mean squared
error `O(J delta)` of a blockwise scalar multiple of `a_p`.

Mark as bad any prime whose pointwise error exceeds `(J delta)^(1/4)`.
The bad proportion is `O((J delta)^(1/2))`. The checked PNT therefore permits
three good primes `q,p,r` in fixed separated subintervals of one block, with

```text
alpha=log(p/q), beta=log(r/q) asymp 1/J.
```

After cancelling `a_p` between the two rows, phase concentration gives
integers `m,n asymp |h|/J` and a nonzero form

```text
n alpha-m beta
```

of size at most

```text
exp(-k rho/32+O(log X)).
```

Unique factorization makes the form nonzero; the pinned rational Matveev
bound from Cycle 25 is `exp(-O((log X)^3))`. Register contradiction for all
sufficiently large `X`.

## Frozen regular rank-J branch

Otherwise retain `n>=k/2` rows with projection deficit at least `delta`.
Apply Cycle 28 with

```text
K=sum_t rho_t >= k rho/2.
```

Register exactly these alternatives:

1. normalized residual shift at most `-k rho/4`;
2. a block-modulated detector direction in `range(E)` reconstructed with
   error at most `sqrt(2)exp(-k rho/(8J))`;
3. exact block-modulated detector reconstruction from a residual null vector;
4. exact scaled-row dependence.

Since `k rho=X^(6/25-o(1))` and `J=X^(1/25+o(1))`, the approximate
reconstruction error has scale

```text
exp(-X^(1/5-o(1))).
```

## Checks

- Exact fractions: block length exponent `24/25`, base shift `6/25`, and
  reconstruction exponent `1/5`.
- Finite block projection and bad-set Markov constant flow.
- CPython `3.12.3`, `Fraction`, no RNG/network, 30 seconds/256 MiB.
- Pin G0, Cycle 25, Cycle 28, and the Evertse source.
