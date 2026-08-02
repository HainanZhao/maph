# Cycle 75 discovery note: denominator geometry candidates

Status: `EXPLORATORY`. Nothing in this note is proof.

The Cycle-74 residual appears to simplify after scaling
`a=A x`, `q=Q y`. For

```text
Y(a,q)=Delta/(2pi) log(1+a/q),
```

the unscaled determinant seems to lose `X^(theta-alpha)`, but the Hessian on
the unit `(x,y)` box appears to have both singular values at the curve-index
scale

```text
Delta A/Q=X^(3/5+alpha-theta)=X^lambda.
```

Candidate consequence: E14 should be formulated after affine normalization;
paying the old unscaled determinant loss may be an artefact of coordinates.

Two further candidate observations:

1. `Y(da,dq)=Y(a,q)` is an exact radial degeneracy, but primitive integer
   pairs have no nontrivial repeated ray. In shifted coordinates `n=q+a`,
   `gcd(n,q)=gcd(a,q)`.
2. Combining Cycle 70's one-packet-per-`ell` bound with Cycle 74's
   fixed-denominator bound gives the candidate banked exponent
   `B=min(lambda,theta+w)`. The worst additional saving required over `B`
   appears to be `7/15`, uniquely at
   `(theta,alpha,kappa)=(1/3,1/3,8/75)`.

These candidates are to be independently derived and checked under the
Cycle-75 preregistration. Failure or correction is an allowed outcome.
