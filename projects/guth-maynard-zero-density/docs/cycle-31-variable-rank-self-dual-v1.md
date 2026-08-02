# Cycle 31: variable-rank amplification and the self-dual block scale

## Claim boundary

`PROVED`: Cycle 29's polynomial block-subspace theorem holds throughout every
fixed range `0<kappa<6/25`, with an exact rank-versus-reconstruction tradeoff.
The choice `kappa=4/25` makes one prime block and the target skeleton have the
same exponent. This is a structural reduction, not yet a prime determinant,
density, or interval theorem.

## Variable-rank theorem

Fix `0<kappa<6/25` and divide `[X,2X]` into

```text
J=X^(kappa+o(1))
```

consecutive intervals. Their length exponent is `1-kappa>19/25`, safely
inside the already checked baseline uniform PNT range. The original detector
belongs to the span of its block restrictions, so every large-value row has
block-subspace projection at least `rho=X^(-3/5-o(1))`.

Cycle 29's near-subspace exclusion is uniform at every fixed such `kappa`:
inside one block, the relevant phase differences have size

```text
|h|/J>=X^(3/5-kappa+o(1)) -> infinity,
```

while the upper logarithmic form remains stretched exponential and Matveev's
lower bound remains `exp(-O((log X)^3))`.

On the regular half-system, Cycle 28 consequently gives

```text
shift<=-k rho/4,
```

or approximate/exact reconstruction of a block-modulated detector direction,
or exact scaled-row dependence. The approximate reconstruction error is

```text
sqrt(2)exp(-k rho/(8J))
 =exp(-X^(6/25-kappa-o(1))).                            (1)
```

The exponent stays positive precisely for `kappa<6/25`.

## Exact tradeoff table

| `kappa` | block count | block-size exponent | reconstruction exponent |
|---|---:|---:|---:|
| `1/25` | `1/25` | `24/25` | `5/25` |
| `2/25` | `2/25` | `23/25` | `4/25` |
| `3/25` | `3/25` | `22/25` | `3/25` |
| `4/25` | `4/25` | `21/25` | `2/25` |
| `5/25` | `5/25` | `20/25` | `1/25` |

All exponents refer to powers of `X`; fixed constants and logarithms are
absorbed in the displayed `o(1)` terms.

## The self-dual choice `kappa=4/25`

At `kappa=4/25`,

```text
number of blocks       =X^(4/25+o(1)),
primes in one block    =X^(21/25-o(1)),
target skeleton rows   =X^(21/25+o(1)),
reconstruction error   =exp(-X^(2/25-o(1))).
```

Thus:

- the block-count exponent is exactly the missing skeleton saving `4/25`;
- one block contains, in exponent, exactly as many prime coordinates as the
  target number of separated rows;
- the reconstruction remains stretched-exponentially accurate.

This identifies a square generalized-prime-Vandermonde scale: after resolving
the reconstructed modulation's support, a one-block profile would compare
`X^(21/25)` rows against `X^(21/25)` prime samples. No lower bound for that
square system is asserted here.

## Gate effect

`PROVED`: the principal arithmetic experiment/theorem should use the
self-dual `4/25 : 21/25` decomposition, not the former arbitrary `1/25`
choice. The next target is a flat-support reduction for the reconstructed
block modulation followed by a prime-Vandermonde or multiplicative-energy
bound at the resulting support scale.
