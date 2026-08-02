# Cycle 61: cumulant saturation is a prime-coordinate annihilator

## Claim boundary

`PROVED`: the Cycle-57 Hilbert coefficients are exact tensor projections of
the integer-label fiber indicators. Their synthesis operator satisfies

```text
A^*A <= D_s I,
D_s=(1+floor(s/2))s!,
```

so `D_3=12` and `D_4=72`. More importantly, the exact norm lost under
coordinate centering is the sum of the proper coordinate-ANOVA components.
Near-saturation forces every powered and ordinary prime-coordinate marginal
of the lifted row-Fourier vector to be small.

This is an inverse formulation, not an exclusion theorem or a power saving.
It proves no `AMPR_s`, density, or interval improvement.

## Operator factorization

Let `Omega=P^(s+1)` be ordered tuples and

```text
L(q,p_1,...,p_s)=q^m p_1...p_s.
```

Lift a scalar vector on distinct labels by

```text
(B beta)_tau=beta_(L(tau)).
```

Let `P=I-J/M` on one prime-coordinate space and

```text
C=P_q tensor P_p1 tensor ... tensor P_ps.
```

The Cycle-57 coefficient attached to label `n` is

```text
a_n=C 1_(L^(-1)(n)),
```

hence its synthesis operator is exactly

```text
A beta=sum_n beta_n a_n=C B beta.                   (1)
```

Since `C` is an orthogonal projection,

```text
||A beta||^2<=||B beta||^2
 =sum_n |L^(-1)(n)| |beta_n|^2
 <=D_s sum_n|beta_n|^2.                             (2)
```

This strengthens Cycle 57's total coefficient-energy bound to a Bessel bound
for every scalar input vector.

## Exact centering defect

Write `Q=I-P=J/M`. Tensoring `I=P+Q` gives mutually orthogonal projections
`C_J`, indexed by the coordinates on which `P` rather than `Q` is chosen.
The full-centered projection is `C_all=C`. Therefore

```text
||B beta||^2-||A beta||^2
 =sum_(J proper)||C_J B beta||^2.                   (3)
```

There are 15 proper components for `s=3` and 31 for `s=4`. If

```text
||A beta||^2 >= (1-delta)||B beta||^2,              (4)
```

then every raw coordinate average `Q_j B beta` has energy at most
`delta||B beta||^2`, because its range lies in the orthogonal complement of
the full-centered tensor space.

## Actual Fourier-vector marginals

For the Cycle-60 edge weights, take

```text
beta_n=sum_e omega_e n^(-ih_e).
```

The lifted vector is

```text
(B beta)_(q,p_1,...,p_s)
 =sum_e omega_e q^(-imh_e)product_j p_j^(-ih_e).
```

Averaging the powered coordinate gives the explicit marginal

```text
sum_e omega_e k(mh_e) product_j p_j^(-ih_e),        (5)
```

while averaging ordinary coordinate `j` gives

```text
sum_e omega_e k(h_e)q^(-imh_e)
  product_(l!=j)p_l^(-ih_e).                        (6)
```

Thus saturation of the Hilbert edge cumulant is not an arbitrary
high-dimensional phenomenon. It says that all `s+1` lower-degree prime-log
polynomials (5)--(6) nearly annihilate simultaneously for the same edge
weights.

## Analytic consequences to pursue

`CONJECTURED` alternatives:

1. **marginal capture:** prove that actual hollow separated edge weights put
   a fixed-power proportion of their lifted energy into at least one marginal;
   by (3), this directly saves the fully centered cumulant;
2. **annihilator inverse:** if every marginal is small, use the common edge
   weights to derive a prime-log Vandermonde relation, two-scale recurrence,
   or a source-valid detector surgery.

The Guth--Maynard scalar theorem does not automatically prove either branch:
its coefficient vector is fixed, whereas scalarizing a Hilbert large value
may select a different direction on each row. Equations (1)--(6) identify the
extra tensor structure that a new theorem may use.

## Gate effect

The live gate becomes
`PRIME_COORDINATE_MARGINAL_CAPTURE_OR_ANNIHILATOR_INVERSE_OPEN`.
