# SIC--Stark research cycle 103: exact adjoint decomposition

Date: 2026-07-28

## Question

What arithmetic packet does a proved adjoint or self-Rankin theorem
actually recover for the dimension-six representation?

## Character calculation

Projectively,

\[
 \rho|_{G_K}\simeq \chi_1\oplus\chi_1^{-1}.
\]

The rotation weights of \(\rho\) are therefore \(1,-1\) modulo \(6\).
The four weights of
\(\rho\otimes\rho^\vee=\operatorname{End}(\rho)\) are

\[
 0,\ 0,\ 2,\ -2.
\]

Reflection splits the two zero-weight lines into the scalar line and the
quadratic character \(\epsilon_{21}\); the \(\pm2\) lines form the
induction of the order-three character \(\chi_1^2\).  Hence

\[
\boxed{
 \rho\otimes\rho^\vee
 \simeq
 \mathbf1\oplus\epsilon_{21}
 \oplus\operatorname{Ind}_{K}^{\mathbf Q}(\chi_1^2),
}
\]

and

\[
 \operatorname{Ad}^0\rho
 \simeq
 \epsilon_{21}
 \oplus\operatorname{Ind}_{K}^{\mathbf Q}(\chi_1^2).
\]

The exact weight calculation is recorded in

```text
scripts/dimension_six_adjoint_decomposition.py
```

## Consequence

Every constituent is unchanged under
\(\chi_1\leftrightarrow\chi_1^{-1}\).  Thus adjoint theorems recover
quadratic/order-three norm information—the same inversion-even layer
already controlled by the finite certificates and Roblot's \(P1/P2\)
relations.  They do not contain a copy of the oriented \(\chi_1\) line.

This sharpens cycle 97: the mismatch is not merely that an available
theorem is phrased for an adjoint representation.  The adjoint
representation decomposes explicitly into pieces that have already
forgotten the sole missing datum.

