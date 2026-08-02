# Cycle 29: polynomial block-subspace amplification

## Claim boundary

`PROVED`: the common detector direction may be enlarged to a
`J=X^(1/25+o(1))` block-constant prime subspace without losing projection
strength. A half-sized near-subspace packet is excluded by blockwise
two-logarithm rigidity. Every target-sized skeleton therefore forces a
rank-`J` negative shift, stretched-exponentially accurate block-modulated
detector reconstruction, or exact scaled-row dependence. No skeleton,
zero-density, or interval improvement is proved.

## Polynomial detector subspace with no threshold loss

Partition `[X,2X]` into

```text
J=2^floor(log_2 X^(1/25))=X^(1/25+o(1))
```

consecutive intervals. Let `a_j` be the restriction of the unimodular prime
coefficient vector `a` to block `j`, and let `e_j=a_j/||a_j||`. The checked
baseline uniform prime-number theorem applies on intervals of length
`X^(24/25+o(1))`, so every block and each fixed positive-proportion
subinterval contains the expected asymptotic number of primes.

The vectors `e_j` have disjoint support and are orthonormal. More importantly,

```text
b=a/||a||=sum_j (||a_j||/||a||)e_j
```

belongs to their span. Hence for every normalized prime phase row `x_t`,

```text
||E*x_t||^2>=|<x_t,b>|^2>=rho=X^(-3/5-o(1)).           (1)
```

Unlike coloring or the single signed-detector threshold, passing to the full
block subspace costs no power of `J`.

## Excluding a near-block-constant packet

Let `P_E=EE*` and freeze

```text
delta=exp(-k rho/8).
```

Suppose at least half the separated skeleton rows satisfy
`||(I-P_E)x_t||^2<=delta`. Choose two, at difference `h`. On each block the
phase vector `p^(-it)` is within mean squared error `O(J delta)` of a scalar
multiple of `a_p`. Markov's inequality shows that all but an
`O((J delta)^(1/2))` proportion of primes have pointwise error at most
`(J delta)^(1/4)`. The same holds for the second row.

Choose good primes `q,p,r` in three separated positive-proportion
subintervals of one block. The coefficient phases `a_p` cancel between the
two rows. With

```text
alpha=log(p/q), beta=log(r/q),
```

one has `alpha,beta asymp J^(-1)`. Angular lifting gives positive integers
`m,n asymp |h|/J` and

```text
|n alpha-m beta|
 <=exp(-k rho/32+O(log X)).                            (2)
```

Here `|h|/J>=X^(14/25+o(1))`, so the integer coefficients are nonzero and
polynomially bounded. Unique factorization shows that the form is nonzero.
The rational Matveev theorem pinned in Cycle 25 instead gives

```text
|n alpha-m beta|>=exp(-O((log X)^3)),                  (3)
```

contradicting (2) for sufficiently large `X`. Thus a half-sized
near-block-constant packet cannot occur.

## Regular rank-J alternatives

Retain `n>=k/2` rows with block-subspace deficit greater than `delta`. From
(1), their total block projection satisfies

```text
K=sum_t rho_t>=k rho/2.
```

Cycle 28 now gives one of:

1. normalized residual shift at most `-K/2<=-k rho/4`;
2. an adaptive direction in the block detector subspace reconstructed from
   the scaled phase rows with error at most
   `sqrt(2)exp(-k rho/(8J))`;
3. exact reconstruction of a block-modulated detector direction from a
   residual null vector;
4. exact scaled-row dependence.

At the critical scales,

```text
k rho=X^(6/25-o(1)),  J=X^(1/25+o(1)),
```

so the approximate reconstruction error is

```text
exp(-X^(1/5-o(1))).
```

## Gate effect

`PROVED`: the detector-surgery obstruction has polynomial internal
dimension, not merely a subpower collection of colors. The live structural
object is a blockwise scalar modulation of the original prime coefficients
that is reconstructed to stretched-exponential accuracy by the large-value
rows. The next inverse theorem should exploit the entropy/support profile of
that modulation; exact row dependence and negative-shift detection remain
parallel alternatives.
