# Cycle 22: square-root volume noise and E8 renormalization

## Claim boundary

`PROVED`: a deterministic square-root-noise Gram model has ordinary operator
and determinant fluctuations much larger than the E8 common-vector signal.
This is an abstract architecture boundary, not a theorem that actual prime
rows realize the model. `CONJECTURED`: a bulk-renormalized spectral statistic
can isolate the smaller common-vector signature.

## Exact noise model

Let `k=2n`, take a flat `n by n` unitary matrix `U`, and define

```text
Q=[[0,U],[U*,0]],
H=I+sqrt(n/m)Q.
```

The matrix `Q` is Hermitian unitary with zero diagonal. Thus `H` has diagonal
one, every nonzero off-diagonal entry has modulus `m^(-1/2)`, and

```text
||H-I||_op=sqrt(k/(2m)),
det(H)=(1-k/(2m))^(k/2).
```

This is the deterministic analogue of square-root sampling noise.

## Critical mismatch

For `m=X`, `k=X^(21/25)`, the model has

```text
entry size:                 X^(-1/2),
operator deviation:         X^(-2/25),
negative log-volume scale:  X^(17/25).
```

Cycle 21's sufficient full-operator gate asks for `o(X^(-3/5))`, which is
smaller by `13/25` powers. Cycle 20's common-vector determinant signature has
negative log scale `X^(6/25)`, while ordinary volume noise is larger by
`11/25` powers.

Therefore square-root cancellation does not merely fall slightly short: the
absolute determinant and full operator norm are dominated by the wrong
phenomenon. A prime proof of those gates would need exceptional rigidity far
beyond pseudorandom sampling.

## Replacement object

E8 should not compare raw volume with the continuum volume. The live
replacement is a bulk-renormalized statistic, schematically

```text
log det(H_P) - Bulk(C,X),
```

or a spectral-shift functional that removes the ordinary `k^2/X` loss and
retains the additional common-vector loss at scale `kX^(-3/5)=X^(6/25)`.
The reference bulk, its uniformity over separated sets, and the required
prime-phase concentration are open. Direct Cauchy--Binet remains available
only if it incorporates the same bulk subtraction rather than seeking an
absolute lower bound.
