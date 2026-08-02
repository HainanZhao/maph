# Cycle 33: the flat-support gate must be anchor-aware

## Claim boundary

`PROVED` correction: no universal positive distance or augmented-determinant
lower bound can separate a flat prime-supported vector from a prime-phase row
span. An actual restricted phase row is already a flat vector. Cycle 32's
flat-support theorem remains valid, but its proposed square-rung gate is
replaced by an anchor-versus-transverse alternative. No branch is yet bounded,
and no skeleton, density, or interval result is proved.

## Actual-prime counterexample

For any finite prime set `P` and any real `t_0`, define

```text
d_(t_0)(p)=|P|^(-1/2)p^(-it_0).
```

Every coordinate has magnitude `|P|^(-1/2)`, so this detector is exactly
flat. It is also exactly the normalized phase row at `t_0`. Any row family
containing that label satisfies

```text
dist(d_(t_0),span{x_t})=0.
```

Appending `d_(t_0)` to the row matrix repeats a row, so the augmented Gram
determinant is zero. Other labels may be arbitrarily far from `t_0`; their
separation does not repair the duplicate-row obstruction.

More generally, if a `k by N` phase matrix has full column rank and `k>=N`,
its row span is all of `C^N`. Every detector vector is then reconstructed
exactly. A nonsingular square minor proves reconstruction instead of
contradicting it. Therefore the exponent-square `lambda=0` rung cannot be
closed by invertibility alone.

## Anchor-aware replacement

For a reconstructed flat detector `d` and an anchor cap `r=X^o(1)`, define

```text
alpha_r(d)=min_(A subset C, |A|<=r)
             dist(d,span{x_t:t in A}).                 (1)
```

The live theorem must split into two genuinely different mechanisms.

### Anchor branch

If `alpha_r(d)` is small, represent `d` using at most `r` phase rows. In the
one-anchor model, if on the selected prime support

```text
d_p=c p^(-it_0),
```

then its value at another row is, up to the pinned conjugation convention,

```text
<x_t,d>=conjugate(c) K_S(t-t_0),
K_S(h)=sum_(p in S)p^(-ih).                            (2)
```

For `r` anchors, (2) becomes a weighted sum of `r` restricted prime kernels.
The original large detector values are thereby converted into an explicit
few-anchor recurrence problem.

### Transverse branch

If `alpha_r(d)` is bounded below but the full row span reconstructs `d` to
stretched-exponential accuracy, the reconstruction is intrinsically
many-row. This is the proper setting for restricted invertibility, exterior
volume, or multiplicative energy: the theorem must exploit transversality to
every small anchor span, not merely flatness.

## Gate effect

`PROVED`: the next arithmetic theorem is not a universal prime-Vandermonde
lower bound. It is an anchor-aware inverse theorem:

```text
few anchors -> weighted prime-kernel recurrence;
many-row transverse reconstruction -> arithmetic exterior-volume bound.
```

The actual-prime witness is a headline boundary for the proposed square-rung
approach, while leaving positive-support and transverse mechanisms open.
