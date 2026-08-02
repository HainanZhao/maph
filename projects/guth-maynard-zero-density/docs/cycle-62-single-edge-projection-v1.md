# Cycle 62: coordinate centering has no pointwise power saving

## Claim boundary

`PROVED`: for a single Fourier edge `beta_n=n^(-ih)`, the fraction retained
by full coordinate centering is exactly

```text
(1-|k(mh)|^2)(1-|k(h)|^2)^s.                       (1)
```

If `|k(h)|<=X^(-alpha)` and `|k(mh)|<=X^(-beta)` for fixed positive
`alpha,beta`, the lost fraction is at most

```text
sX^(-2alpha)+X^(-2beta)=o(1).                       (2)
```

Thus pointwise projection cannot supply a fixed-power saving in the generic
small-kernel regime. This does not obstruct a theorem using the genuine
multi-edge, nonnegative convolution vector from phase-aligned rows.

## Exact calculation

The ordered lift of one edge is

```text
q^(-imh) product_(j=1)^s p_j^(-ih).
```

Each normalized coordinate vector has constant-mode square `|k(ch)|^2`.
Projection by `P=I-J/M` therefore retains square norm `1-|k(ch)|^2` in that
coordinate. Tensor multiplication gives (1).

For numbers `0<=u,v<=1`,

```text
1-(1-v)(1-u)^s <= v+su,
```

which gives (2).

## Why the valid edge vector is different

Cycle 60's phase-aligned weights have

```text
omega_(t,u)=z_t conj(z_u).
```

Consequently their scalar label vector is not an arbitrary Fourier edge:

```text
beta_n
 =sum_(t,u)z_t conj(z_u)n^(-i(t-u))
 =|sum_t z_t n^(-it)|^2 >=0.                       (3)
```

Equation (3) couples all `R^2` edges, is nonnegative on every monomial label,
and has rank-one autocorrelation structure. The single-edge vector used in
the stress test does not satisfy (3), except in the trivial one-row case
where there is no nonzero edge.

## Strategic consequence

The Cycle-61 “marginal capture” branch must be stated only for vectors of the
form (3), with a row set large enough to violate the target. A universal
operator improvement `A^*A<=X^(-gamma)D_s I` is false in the relevant
small-kernel regime.

`CONJECTURED` next theorem: nonnegative autocorrelation vectors (3) arising
from an `X^(3/5)`-separated set cannot simultaneously concentrate in the full
coordinate-centred tensor space and meet the Cycle-39 large-value lower
bound; failure should force additive structure or two-scale recurrence.

## Gate effect

The live gate becomes
`NONNEGATIVE_AUTOCORRELATION_ANOVA_OR_RECURRENCE_OPEN`.
