# Cycle 28: rank-J spectral shift and detector-subspace reconstruction

## Claim boundary

`PROVED`: the residual spectral-shift identity, reconstruction duality, and
singular split extend exactly from one detector direction to an orthonormal
detector subspace. Cycle 27's Hadamard loss preserves the critical
stretched-exponential scale for `J=X^o(1)`. No prime-log bound, skeleton
bound, density improvement, or interval improvement is proved.

## Rank-J determinant identity

Let `X` be the normalized row matrix and let the columns of `E` be an
orthonormal family of detector directions. Put

```text
Q=XE,                  R=X(I-EE*),
rho_t=||Q_(t,.)||^2,   D=diag(sqrt(1-rho_t)),
S=D^(-1)Q,             W=D^(-1)R,
B=WW*.
```

Then

```text
D^(-1)X=S E*+W,
XX*=D(B+SS*)D.
```

If `B` is positive definite, the matrix determinant lemma and Sylvester's
identity give

```text
det(XX*)/det(B)
 = product_t(1-rho_t) det(I_J+S*B^(-1)S).             (1)
```

This removes the ordinary residual spectral bulk while retaining all `J`
orthogonal detector directions at once.

## Shift or reconstructed detector direction

Write

```text
K=sum_t rho_t,   L=S*B^(-1)S.
```

Since `sum log(1-rho_t)<=-K`, failure of a determinant shift at most `-K/2`
forces

```text
log det(I_J+L)>K/2.
```

Consequently

```text
lambda_max(L)>=exp(K/(2J))-1.                          (2)
```

Let `y` be a unit top eigenvector, let `lambda=lambda_max(L)`, and set
`c=B^(-1)Sy`. Direct multiplication gives

```text
c*S=lambda y*,   ||c*W||^2=lambda,
||(c*/lambda)D^(-1)X-y*E*||=lambda^(-1/2).             (3)
```

Thus the compensating leverage reconstructs an explicit direction `Ey`
inside the entire detector subspace; it need not reconstruct one of the
preselected Hadamard basis vectors.

## Hadamard exponent ledger

On Cycle 27's orthogonal-surgery branch, each row has some detector value at
least `V/(4J)`. Therefore its squared projection onto the Hadamard detector
subspace obeys

```text
rho_t>=rho/(16J^2),
K>=k rho/(16J^2).
```

Equations (1)--(3) imply either a negative shift of magnitude at least

```text
k rho/(32J^2),
```

or, once `K/(2J)>=log 2`, detector-direction reconstruction with error at
most

```text
sqrt(2) exp(-k rho/(64J^3)).
```

For `J=X^o(1)` and `k rho=X^(6/25-o(1))`, both quantities retain the full
stretched-exponential exponent `X^(6/25-o(1))`. Treating the Hadamard system
as a subspace therefore avoids the crude `J`-colour trace loss.

## Singular residual

If `B` is singular, `ker(B)=ker(W*)`. Every `c` in the nullspace satisfies

```text
c*D^(-1)X=(c*S)E*.
```

If `c*S` is nonzero, this is exact reconstruction of a detector-subspace
direction. If it vanishes, it is exact linear dependence among the scaled
prime rows. The latter remains open.

## Gate effect

`PROVED`: orthogonal detector surgery can be inserted into the
bulk-renormalized E8 engine without losing the critical exponent. The live
alternatives are now a rank-`J` negative shift, reconstruction of an adaptive
Hadamard-subspace direction, exact prime-row dependence, or Cycle 27's
multiblock synchronization. The next step is to iterate this subspace update
or obtain prime arithmetic on the last two branches.
