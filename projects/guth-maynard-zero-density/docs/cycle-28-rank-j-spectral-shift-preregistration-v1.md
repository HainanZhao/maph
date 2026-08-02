# Cycle 28 rank-J spectral shift preregistration v1

## Claim boundary

This cycle may generalize the rank-one residual shift and reconstruction
identities to an orthonormal detector subspace of dimension `J`, then insert
Cycle 27's threshold loss. It may not prove the multiblock prime-log bound,
exclude exact row dependence, close the skeleton target, or promote density
or interval consequences.

## Frozen subspace convention

Let `X` be a normalized `k by M` row matrix and let `E` be an `M by J`
matrix with `E*E=I_J`. Define

```text
Q=XE,                   R=X(I-EE*),
rho_t=||Q_(t,.)||^2,    D=diag(sqrt(1-rho_t)),
S=D^(-1)Q,              W=D^(-1)R,
B=WW*,                  L=S*B^(-1)S.
```

For positive definite `B`, freeze the exact identity

```text
det(XX*)/det(B)
 = product_t(1-rho_t) det(I_J+L).
```

## Frozen shift/reconstruction alternative

Put `K=sum_t rho_t`. If the logarithmic determinant shift is greater than
`-K/2`, then

```text
log det(I_J+L)>K/2,
lambda_max(L)>=exp(K/(2J))-1.
```

For a unit top eigenvector `y`, set `c=B^(-1)Sy`. The builder must verify

```text
c*S=lambda y*,
||c*W||^2=lambda,
||(c*/lambda)D^(-1)X-y*E*||=lambda^(-1/2).
```

If `K/(2J)>=log 2`, the reconstruction error is at most
`sqrt(2)exp(-K/(4J))`.

## Frozen Hadamard insertion

Cycle 27 supplies, on the surgery branch, at least one orthogonal detector
value `W_0>=V/(4J)` per row. Hence

```text
rho_t>=rho/(16J^2),
K>=k rho/(16J^2).
```

For `J=X^o(1)` and `k rho=X^(6/25-o(1))`, the negative-shift magnitude is at
least `k rho/(32J^2)` or a detector-subspace direction is reconstructed with
error at most

```text
sqrt(2) exp(-k rho/(64J^3)).
```

Both retain stretched-exponential scale `X^(6/25-o(1))`.

## Singular split

For singular `B`, `ker(B)=ker(W*)`. A null vector `c` obeys

```text
c*D^(-1)X=(c*S)E*.
```

If `c*S!=0`, this exactly reconstructs a detector-subspace direction; if
`c*S=0`, it is exact scaled-row dependence. Do not exclude the latter.

## Checks

- Exact rational `J=2` positive-definite determinant/reconstruction example.
- Exact singular reconstruction and annihilation examples.
- CPython `3.12.3`, `Fraction`, no RNG/network, 30 seconds/256 MiB.
- Pin Cycles 23, 26, 27 v1, and 27 v2.
