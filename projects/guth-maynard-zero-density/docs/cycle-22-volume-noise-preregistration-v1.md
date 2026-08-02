# Cycle 22 volume-noise preregistration v1

## Claim boundary

This cycle may test the full-volume and full-operator E8 gates against an
exact deterministic square-root-noise Gram model. It may prove an abstract
scale obstruction and formulate a bulk-renormalized replacement. It may not
claim that actual prime rows realize the model, refute every determinant
method, prove the skeleton target, or promote density/interval consequences.

## Frozen block-unitary model

Let `k=2n<=2m`. Choose an `n by n` unitary matrix `U` all of whose entries
have modulus `n^(-1/2)`, and put

```text
Q = [[0,U],[U*,0]],
delta=sqrt(n/m),
H=I+delta Q.
```

Then `Q` is Hermitian unitary with zero diagonal. Register:

```text
diag(H)=1,
max_(r!=s)|H_rs|=m^(-1/2),
||H-I||_op=delta=sqrt(k/(2m)),
det(H)=(1-k/(2m))^(k/2).
```

## Frozen critical scales

Set `m=X` and `k=X^(21/25)`. Then:

```text
entry scale              X^(-1/2),
operator-noise scale     X^(-2/25),
log-volume-loss scale    k^2/m = X^(17/25).
```

Cycle 21 asks for operator discrepancy `o(X^(-3/5))`, a power gap of
`13/25` below this exact square-root-noise model. Cycle 20's common-vector
volume signature has scale `X^(6/25)`, smaller than the model's ordinary
volume loss by `11/25`.

## Registered route consequence

The cycle may conclude only that generic square-root cancellation is
insufficient for the full operator-comparison or absolute determinant-lower-
bound formulations of E8. The authorized replacement is a renormalized
statistic that subtracts or conditions on the ordinary spectral bulk and
detects the additional rank-one common-vector signature at scale `X^(6/25)`.

The first replacement target is to formulate a log-determinant excess or
spectral-shift inequality with an explicit reference bulk. Its prime-phase
control remains open.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
