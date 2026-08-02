# Cycle 59: crossing the diagonal is not yet strong recurrence

## Claim boundary

`PROVED` conditional ledger: if a trigger-only hybrid crosses the adjusted
diagonal by surplus `mu`, generic phase-aligned counting forces popular
correlations at deficit `eta` only when

```text
eta>r-mu,
```

where `R=X^r`. It supplies at least `X^(r+mu-o(1))` ordered popular edges,
of average-degree exponent `mu`.

At `r=21/25`, forcing Cycle-48 deficit `eta=7/50` requires `mu>7/10`.
Uniformly over the generic separated range `r<=1`, it requires `mu>43/50`.
A hybrid that merely saves `3/50+epsilon` has `mu=epsilon` and does not
automatically reach this strong recurrence.

This is an exponent interface, not an analytic theorem. No cumulant bound,
`AMPR_s`, density, or interval gain is proved.

## Derivation

Let the coefficient energy and residual support exponents be `a,n`. After
the adjusted diagonal is crossed by `mu`, write

```text
r+2v=a+n+mu.
```

The phase-aligned inequality forces total off-diagonal correlation mass at
least

```text
X^(2r+2v-a-o(1))=X^(r+n+mu-o(1)).
```

If every one of at most `X^(2r)` ordered pairs had correlation below
`X^(n-eta)`, their total would be at most `X^(2r+n-eta)`. This is smaller
than the forced mass exactly when

```text
2r+n-eta < r+n+mu,
```

or `eta>r-mu`. Removing the low edges under this strict condition and using
the maximum correlation `X^n` leaves at least `X^(r+mu-o(1))` popular edges.

## Exact benchmarks

For desired `eta=7/50`:

| row exponent | surplus required | total penultimate hybrid saving required |
|---:|---:|---:|
| `r=21/25` | `mu>7/10` | `gamma>19/25` |
| all `r<=1` | `mu>43/50` | `gamma>23/25` |

The “total hybrid saving” includes Cycle 58's initial penultimate gap
`3/50`. These are trigger-only requirements, not requirements for a direct
restriction theorem that already controls the full quadratic form.

The full final ordinary contraction has surplus `47/50`. It forces
`eta=7/50` uniformly for `r<=1`; at the target `r=21/25`, its forced edge
count would exceed `R^2`, so that row class is already impossible.

## Strategic fork

E12 now has two mathematically distinct targets:

1. `CONJECTURED` **direct restriction:** bound the complete Hilbert-valued
   edge-cumulant quadratic form with saving `>3/50`, closing the penultimate
   route without a separate recurrence extraction;
2. `CONJECTURED` **trigger plus amplifier:** obtain a smaller strict surplus,
   then prove a prime-specific graph/additive-energy amplification improving
   the generic `eta>r-mu` conversion before applying Cycle 52/E13.

Calling a diagonal crossing alone an `AMPR_s` proof is invalid. The full
off-diagonal estimate or the amplification theorem must be explicit.

## Gate effect

The live gate becomes
`DIRECT_CUMULANT_RESTRICTION_OR_GRAPH_AMPLIFIED_RECURRENCE_OPEN`.
