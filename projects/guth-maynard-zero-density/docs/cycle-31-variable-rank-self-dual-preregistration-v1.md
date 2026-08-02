# Cycle 31 variable-rank self-dual block preregistration v1

## Claim boundary

This cycle may generalize Cycle 29 from `kappa=1/25` to every fixed
`0<kappa<6/25` and identify `kappa=4/25` as the self-dual scale. It may not
prove an annihilator determinant bound, exploit the self-dual square system,
close the skeleton target, or promote density/interval consequences.

## Frozen parameter family

For fixed rational `kappa` with `0<kappa<6/25`, set

```text
J=X^(kappa+o(1)),
block length=X^(1-kappa+o(1)).
```

The checked baseline PNT applies because
`1-kappa>19/25>17/30`. The Cycle 29 blockwise Matveev argument remains valid
because a skeleton difference satisfies

```text
|h|/J>=X^(3/5-kappa+o(1)) -> infinity.
```

The original detector remains inside the block subspace, so projection
strength is still `rho=X^(-3/5-o(1))` without a `J` loss.

## Frozen alternatives and tradeoff

After excluding a half-sized near-subspace packet, retain the rank-J regular
alternatives

```text
shift<=-k rho/4,
approximate/exact block-modulated detector reconstruction,
exact scaled-row dependence.
```

The approximate reconstruction error is

```text
sqrt(2)exp(-k rho/(8J))
 =exp(-X^(6/25-kappa-o(1))).
```

Freeze the admissible tradeoff table for

```text
kappa in {1/25,2/25,3/25,4/25,5/25}.
```

Record block-count exponent `kappa`, block-size exponent `1-kappa`, and
reconstruction exponent `6/25-kappa`.

## Frozen self-dual scale

At `kappa=4/25`, register

```text
J=X^(4/25+o(1)),
primes per block=X^(21/25-o(1)),
target skeleton rows=X^(21/25+o(1)),
reconstruction error=exp(-X^(2/25-o(1))).
```

Thus the block count equals the missing skeleton saving exponent `4/25`, and
one block has the same exponent `21/25` as the target number of rows. This is
an exact exponent identity, not yet a determinant theorem.

## Checks

- Exact `Fraction` table and identities.
- Reuse the pinned G0, Cycle 25, Cycle 28, Cycle 29, and Matveev inputs.
- CPython `3.12.3`, no RNG/network, 30 seconds/256 MiB.
