# Cycle 20: exterior-volume collapse and a prime determinant target

## Claim boundary

`PROVED`: a target-sized family of rows sharing one critical large
coefficient vector must have stretched-exponentially small normalized Gram
volume, and the abstract determinant bound is sharp. `CONJECTURED`: actual
widely separated prime-phase rows have a stronger uniform volume lower bound.
No density or interval result is promoted.

## Sharp determinant theorem

Let `G` be the Gram matrix of `k` rows of squared norm `M`. If a vector of
squared norm `A` has projection at least `V` on every row, phase alignment
gives

```text
lambda_max(G) >= kV^2/A = kw.
```

Assume `kw>=M`. Since `trace(G)=kM`, fixing the top eigenvalue and applying
arithmetic--geometric mean to the remaining eigenvalues shows

```text
det(G)/M^k
 <= k rho [k(1-rho)/(k-1)]^(k-1),    rho=w/M.
```

The right side decreases once the top eigenvalue exceeds `kw`, so using the
minimum allowed top eigenvalue is optimal.

The bound is attained abstractly. With `z` the normalized all-ones vector,
put

```text
mu=k(M-w)/(k-1),
G=mu I+(kw-mu)zz*.
```

This positive semidefinite matrix has diagonal `M`, top eigenvalue `kw`, and
all remaining eigenvalues `mu`. A Gram realization has a common projection
witness whose minimum squared norm is exactly `A`. Thus no stronger volume
collapse follows from row norms and common large projections alone.

## Critical-scale consequence

At the prime skeleton scales,

```text
rho=X^(-3/5),    k=X^(21/25),    k rho=X^(6/25).
```

Using only `log(1-rho)<=-rho` and
`log(1+1/(k-1))<=1/(k-1)` gives

```text
log(det(G)/M^k) <= -X^(6/25+o(1)).
```

This turns E8 into a precise sufficient theorem: it is enough to show that
every `X^(3/5)`-separated set of `X^(21/25)` prime-phase rows in the frozen
time range has normalized Gram determinant

```text
det(G/M) >= exp(-X^(theta+o(1)))
```

for one fixed `theta<6/25` (or more generally `exp(-o(X^(6/25)))`). Such a
lower bound would contradict the volume collapse forced by a common critical
coefficient vector.

## Minor formulation

For the prime sampling matrix `U`, Cauchy--Binet gives exactly

```text
det(UU*)=sum_(|S|=k)|det(U_S)|^2.
```

The proof search can therefore pursue one generalized Vandermonde minor or a
collective lower bound. The horizon `|t|<=X^(12/5)` and separation
`X^(3/5)` are essential: mere linear independence or unbounded-time
nonvanishing gives no quantitative contradiction.
