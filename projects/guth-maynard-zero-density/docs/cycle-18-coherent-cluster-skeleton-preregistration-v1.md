# Cycle 18 coherent-cluster skeleton preregistration v1

## Claim boundary

`OBSERVED`: Cycle 17's finite crossings occur in short consecutive clusters.
This cycle freezes a source-checked covering lemma that removes all such
local clusters at a quantified cost.

The cycle may prove an abstract cluster/skeleton reduction using the checked
classical large-values inequality. It may not bound the separated skeleton,
prove the rank-one semiprime conjecture, or promote a density result.

## Frozen source and scales

Use the classical estimate stated in the pinned Guth--Maynard source,
SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`:

```text
R <= X^o(1)[X^2 V^-2 + Y min(X V^-2,X^4 V^-6)]
```

for a one-separated large-value set in an interval of length `Y`.

Freeze `V=X^(7/10)` and cluster radius `D=X^(3/5)`. Exact exponent
substitution gives

```text
R(J) <= X^o(1)[X^(3/5)+Y X^(-2/5)].
```

In every interval of length `2D`, this is `X^(3/5+o(1))`.

## Frozen skeleton theorem

Let `W` be any one-separated critical large-value set. Choose a maximal
subset `C subset W` whose distinct elements are more than `D` apart. Then
the intervals `[c-D,c+D]`, `c in C`, cover `W`. The local estimate gives

```text
|W| <= X^(3/5+o(1)) |C|.
```

Consequently the desired prime-atom count

```text
|W| <= X^(36/25+o(1))
```

reduces to the separated-recurrence bound

```text
|C| <= X^(21/25+o(1)),      separation(C)>X^(3/5).
```

The implication is one-way and sufficient. No claim is made that every
large-value set saturating the target has local clusters of maximal size.

## Registered comparisons

- Generic GM count exponent: `8/5`.
- Local cluster exponent: `3/5`.
- Skeleton exponent needed for the generic baseline: `1`.
- Skeleton exponent needed for the new target: `21/25`.
- Required skeleton saving: `4/25`, exactly the original saving.

Thus cluster removal does not itself create the saving. It quarantines local
coherence and transfers the full analytic burden to an `X^(3/5)`-separated
recurrence set, where prime-phase arithmetic has more room to act.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic,
  no RNG, third-party libraries, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
