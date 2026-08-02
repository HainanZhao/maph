# Cycle 98 source ledger: Gaudron's algebraic-coefficient logarithmic form

## Primary source

Éric Gaudron, *Minorations simultanées de formes linéaires de logarithmes de
nombres algébriques*, arXiv:1004.3652, Theorem 1.1, pages 2--3.

## Checked statement used

Theorem 1.1 takes a number field `k` of degree `d=[k:Q]`, logarithms
`u_j` with algebraic exponentials `alpha_j=exp(u_j) in k`, and coefficients
`beta_(i,j) in k`, including an affine coefficient `beta_(i,0)`. Under the
displayed height conditions and `Q`-linear independence of the logarithms,
it bounds the nonzero forms

```text
Lambda_i=beta_(i,0)+sum_j beta_(i,j)u_j
```

from below. For `n=2,t=1`, its logarithmic lower-bound cost is, up to the
absolute constant `(4n)^(91n^2)`,

```text
a0 (log b+a0 log e) (1+d log a/log e)^2,
```

where

```text
a0=floor[d/(log e) log(e+d/(log e)+log a)]+1.
```

## Hypothesis map

- Choose `u_1=log(alpha)` for a positive algebraic root from Cycle 97 and
  `u_2=log(-1)=i*pi`.
- Choose coefficients `beta_1=D` and `beta_2=2i`; then
  `Lambda=D log(alpha)-2pi`.
- Take `k=Q(i,alpha)`, so `[k:Q]<=2 deg(alpha)<=4M`.
- If `alpha!=1`, `u_1` is real nonzero and `u_2` is purely imaginary, hence
  they are linearly independent over `Q`. The case `alpha=1` is elementary
  and is not charged to this theorem.
- The archimedean branch permits the required complex logarithms.
- The coefficient heights include `h(D)=log D`; the root height is supplied
  by Cycle 97.

The source was read at the theorem and hypothesis level. No claim is made
that this general theorem is optimal for the sparse trinomial family.
