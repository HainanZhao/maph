# Cycle 23: residual spectral shift and inverse leverage

## Claim boundary

`PROVED`: after removing the actual common coefficient direction, the Gram
determinant has an exact bulk-plus-shift factorization. A target-sized
skeleton forces either a negative residual spectral shift at scale
`X^(6/25)` or exponentially large inverse leverage. `OBSERVED`: neither
prime-specific branch is yet bounded, and no density or interval result is
promoted.

## Canonical bulk subtraction

Let `H=UU*/M` and `q=Ua/sqrt(AM)`. Then

```text
Z=H-qq*=U(I-aa*/A)U*/M >= 0.
```

Writing `rho_t=|q_t|^2`, set

```text
D=diag(sqrt(1-rho_t)),
B=D^(-1)ZD^(-1),
s=D^(-1)q.
```

When `Z` is positive definite, `B` is a correlation matrix: it is positive
definite with diagonal one. It is the row Gram matrix after deleting the
common coefficient direction and renormalizing the lost diagonal mass.

## Exact determinant identity

Since `H=DBD+qq*`, the matrix determinant lemma yields

```text
det(H)/det(B)
 = product_t(1-rho_t)[1+s*B^(-1)s].
```

Thus the bulk-renormalized log volume is exactly

```text
Shift = sum_t log(1-rho_t)+log(1+L),
L=s*B^(-1)s.
```

The first term is the diagonal volume consumed by the common coefficient
direction. The second is the only possible compensation: inverse leverage
of that direction against the normalized residual.

## Critical dichotomy

If every large value gives `rho_t>=rho=V^2/(AM)`, then

```text
Shift <= k log(1-rho)+log(1+L).
```

For any fixed `0<epsilon<1`, either

```text
L > exp(epsilon k rho),
```

or

```text
Shift <= -(1-epsilon)k rho+log 2.
```

Conversely, avoiding a shift below `-c k rho` forces
`L>=exp((1-c)k rho)-1`. At
`k=X^(21/25)` and `rho=X^(-3/5)`, both branches live at the exact scale
`k rho=X^(6/25)`.

This repairs the raw E8 formulation: ordinary square-root spectral bulk is
inside `det(B)` and cancels from the comparison. The new arithmetic gate is
to rule out exponentially large residual inverse leverage or show that the
negative spectral shift itself is incompatible with prime-phase rows.

If `Z` is singular, it is retained as a separate `RESIDUAL_SINGULAR` branch;
the inverse identity is not applied.
