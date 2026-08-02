# Cycle 75: affine normalization exposes the denominator contract

## Claim boundary

`PROVED`: on a dyadic numerator-denominator block, the inverse-log surface
has two affine-normalized Hessian singular values comparable to

```text
Delta A/Q=X^(lambda+o(1)),
lambda=3/5+alpha-theta.                             (1)
```

Thus the former unscaled determinant loss `X^(theta-alpha)` is not an
intrinsic loss for E14: after scaling the actual rectangular lattice box to
unit size, the curvature scale is exactly the curve-index scale.

`PROVED`: combining Cycle 70 curve-index injectivity with Cycle 74's
fixed-denominator estimate gives the banked packet exponent

```text
B(theta,alpha)=min(lambda,theta+w(theta,alpha)),     (2)
w=min(alpha,max(0,alpha+1/10-theta/2)).
```

The exact live residual is `B+kappa>=6/25`. Relative to this best banked
bound, the largest additional saving needed for complete packet closure is
strictly more than `7/15`; the deficit `7/15` occurs uniquely at

```text
(theta,alpha,kappa)=(1/3,1/3,8/75).                 (3)
```

No denominator-average estimate, seed-extraction theorem, powered saving,
density gain, or interval gain is proved.

## Two exact coordinate systems

Put `C=Delta/(2pi)` and

```text
Y(a,q)=C log(1+a/q).
```

Direct differentiation in `(a,q)` gives

```text
H_(a,q)Y
 =C [[-1/(a+q)^2, -1/(a+q)^2],
     [-1/(a+q)^2,  1/q^2-1/(a+q)^2]],              (4)

det H_(a,q)Y=-C^2/[q^2(a+q)^2].                    (5)
```

In shifted coordinates `n=q+a`,

```text
Y=C(log n-log q),
H_(n,q)Y=C diag(-1/n^2,1/q^2).                     (6)
```

The linear substitution `a=n-q` has determinant one. Applying `J^T H J` to
(4) gives (6), and (5) is unchanged. The shifted form diagonalizes the saddle
while the original form keeps the short numerator direction explicit.

For the Fourier convention `e(z)=exp(2pi i z)`, (6) also gives the exact E15
factorization

```text
e(kY)=(n/q)^(i k Delta)=n^(i k Delta)q^(-i k Delta). (7)
```

## Affine-normalized curvature

Write

```text
a=A x, q=Q y, epsilon=A/Q,
0<epsilon<=1, 1<=x,y<=2,
s=y+epsilon x.
```

After dividing the scaled Hessian by its natural unit `C epsilon=C A/Q`,
the matrix is

```text
M=[[-epsilon/s^2,                    -1/s^2],
   [-1/s^2, x(2y+epsilon x)/(y^2s^2)]],            (8)

det M=-1/(y^2s^2).                                  (9)
```

On the frozen dyadic box, `|det M|>=1/64`, while the maximum absolute row sum
is at most `13`. Since the product of the two singular values is
`|det M|`, both singular values of the physical scaled Hessian satisfy the
explicit uniform bounds

```text
(C A/Q)/832 <= s_min <= s_max <= 13(C A/Q).         (10)
```

Equation (1) follows. In particular, small `A/Q` shrinks the variation and
the curvature together; it does not create a further condition-number loss
after the correct affine scaling.

The Cycle-74 vertical tube has size `Delta/(QKX)`. Dividing by the normalized
surface scale `Delta A/Q` gives

```text
relative tube width =1/(AKX)
                    =X^(-1-alpha-kappa+o(1)),       (11)
```

which is independent of `theta`. Equations (1), (10), and (11) are the exact
E14 unit-box contract.

## Primitivity removes the exact radial obstruction

The surface is homogeneous of degree zero:

```text
Y(da,dq)=Y(a,q).
```

This would produce arbitrarily repeated exact rays on the full integer
lattice. But if `(a,q)=1`, the ratio `a/q` is reduced, so two primitive
positive pairs on the same ray are identical. Moreover,

```text
gcd(n,q)=gcd(a+q,q)=gcd(a,q).                       (12)
```

Hence E15 retains primitivity exactly and has no nontrivial exact radial
repetition. Approximate rational webs remain possible and are the correct
inverse objects for E16.

## Combined residual atlas

Cycle 70 gives at most one packet per curve index, hence count exponent
`lambda`. Cycle 74 gives exponent `theta+w`. Taking the better bound proves
(2). Consequently only

```text
B(theta,alpha)+kappa>=6/25,
0<=alpha<=theta,
theta+kappa<=11/25                                 (13)
```

remains live. This strictly prunes the Cycle-73 residual superset; no prior
claim is invalidated.

On (13), `lambda>=B>=6/25-kappa`. Therefore every live block has normalized
curvature at least `X^(6/25-kappa+o(1))`. E14 should not pay the superseded
unscaled loss `theta-alpha` after unit-box normalization.

Define the additional count-saving deficit

```text
D=B+kappa-6/25.                                    (14)
```

Since `kappa<=11/25-theta`,

```text
D<=B+1/5-theta.                                    (15)
```

If `theta>=1/3`, then `B<=lambda<=3/5`, so
`D<=4/5-theta<=7/15`. If `theta<=1/3`, then
`B<=theta+w`, so `D<=w+1/5`. For `theta<=1/5`,
`w<=theta<=1/5`; for `1/5<=theta<=1/3`,
`w<=1/10+theta/2<=4/15`. Thus again `D<=7/15`.

Equality throughout forces `theta=alpha=1/3` and
`kappa=11/25-1/3=8/75`, proving (3). At this point the two banked bounds tie:

```text
lambda=theta+w=3/5.
```

On the upper Huxley--Sargos piece more generally,
`lambda-(theta+w)=1/2-3theta/2`, so `theta=1/3` is the exact switching wall
between fixed-denominator control and curve-index injectivity.

## Strategic implication

The first E14 theorem should be attempted on the affine unit box using
curvature unit `X^lambda` and relative tube `X^(-1-alpha-kappa)`. E15 should
use the diagonal factorization (7) on the same block. Any failure carrying
large mass must be tested for an approximate rational web, since primitivity
has already removed exact rays.

## Gate effect

E13 advances to
`AFFINE_CURVATURE_CONTRACT_EXACT_E14_E15_ANALYTIC_GAIN_OPEN`.
