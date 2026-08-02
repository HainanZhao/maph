# Cycle 26: inverse leverage is detector reconstruction

## Claim boundary

`PROVED`: Cycle 23's large inverse leverage has an exact dual formulation as
stretched-exponentially accurate reconstruction of the common coefficient
vector from scaled prime-phase rows. A singular residual gives either exact
reconstruction or exact row dependence. No source-valid complementary
detector, skeleton bound, zero-density gain, or interval gain is proved.

## Exact dual identity

Let `X` be the normalized row matrix and `b` the unit common coefficient
vector. With the Cycle 23 definitions,

```text
q=Xb,                 R=X(I-bb*),
D=diag(sqrt(1-|q_t|^2)),
W=D^(-1)R,            B=WW*,
s=D^(-1)q,
```

one has

```text
D^(-1)X=s b*+W.
```

Assume first that `B` is positive definite, and put

```text
c=B^(-1)s,   L=s*B^(-1)s.
```

Then

```text
c*s=L,              ||c*W||^2=c*Bc=L,
```

and consequently

```text
||(c*/L)D^(-1)X-b*||=L^(-1/2).
```

This is not merely an implication from a small eigenvalue: the same leverage
quantity that can cancel the negative determinant shift supplies the optimal
dual coefficients reconstructing the detector direction.

## Critical reconstruction scale

In Cycle 24's regular branch, failure of the negative-shift conclusion gives

```text
L >= exp(k rho/4)/2.
```

Therefore the reconstruction error is at most

```text
sqrt(2) exp(-k rho/8)
  = exp(-X^(6/25-o(1))/8+O(1)).
```

The obstruction is thus no longer an unspecified ill-conditioned residual.
It says that the original common coefficient vector is almost a linear
combination of the very phase rows on which it is large.

## Singular residual

If `B` is singular, then `ker(B)=ker(W*)`. For every `c` in this kernel,

```text
c*D^(-1)X=(c*s)b*.
```

There are two exact alternatives:

1. some `c` has `c*s!=0`, and division by `c*s` reconstructs `b*` exactly;
2. `s` is orthogonal to `ker(B)`, so every residual null relation is also an
   exact linear dependence among the scaled prime rows.

The second alternative is retained; no universal generalized-Vandermonde
nonvanishing theorem is asserted.

## Gate effect

`PROVED`: after Cycle 25, every target-sized skeleton yields one of three
surviving outcomes: a detectable negative residual shift, exponentially
accurate (possibly exact) detector reconstruction, or exact linear dependence
among scaled prime rows. The next E10 theorem should exploit reconstruction
by projecting the source detector onto complementary prime blocks and proving
that a power proportion of rows remains detectable. The exact-dependence arm
remains an E8/E9 arithmetic question.
