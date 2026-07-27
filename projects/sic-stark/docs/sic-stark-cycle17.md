# SIC--Stark research cycle 17: parity and the fourth moment

Date: 2026-07-27

## Outcome

Cycle 17 removes the main caveat of the cycle-16 positive
certificate.  On the actual ghost family, parity-Hermiticity converts
the adjoint-dependent singular-value identity into a polynomial
fourth-moment identity.

Let \(G=\widetilde\Pi\) be the normalized ghost and let

\[
P|j\rangle=|-j\rangle.
\]

The source construction gives

\[
G^\dagger=PGP.
\]

Consequently

\[
J=PG
\]

is ordinarily Hermitian and

\[
G^\dagger G=PGPG=J^2.
\]

The cycle-16 exterior-square certificate therefore becomes

\[
\boxed{
\Delta _2(G)
=\frac12\left[
  \bigl(\operatorname{Tr}J^2\bigr)^2
  -\operatorname{Tr}J^4
\right].
}
\]

Since \(\operatorname{Tr}G=1\), the ghost is nonzero, and hence

\[
\boxed{
\mathrm{TCC}
\iff
\operatorname{Tr}J^4
=\bigl(\operatorname{Tr}J^2\bigr)^2.
}
\]

This is one quartic polynomial identity in the RM Zak entries and the
fixed rational permutation \(P\).  Complex conjugation is no longer
present in the formula once parity-Hermiticity has been imposed.

## 1. Spectral meaning

Write the real eigenvalues of \(J\) as
\(\lambda_1,\ldots,\lambda_d\).  Then

\[
\Delta _2(G)
=\sum_{i<j}\lambda_i^2\lambda_j^2\ge0.
\]

Equality holds exactly when at most one eigenvalue is nonzero.
Multiplication by \(P\) preserves rank, so this is equivalent to
\(\operatorname{rank}G=1\), and hence to TCC by cycle 15.

This is a Schatten-moment saturation statement:

\[
\|J\|_4^4=\|J\|_2^4.
\]

It is stronger than the algebraic identity
\(\operatorname{Tr}G^2=1\), because \(G^2\) and \(G^\dagger G=J^2\)
are different products.

## 2. What reciprocity says about the quadratic norm

Write the Weyl coefficients as

\[
\mu_{\boldsymbol0}=1,\qquad
\mu_{\boldsymbol p}
=\frac{u_{\boldsymbol p}}{\sqrt{d+1}}
\quad(\boldsymbol p\ne\boldsymbol0),
\]

where the normalized RM values are real and satisfy

\[
u_{\boldsymbol p}u_{-\boldsymbol p}=1.
\]

Weyl orthogonality gives

\[
\operatorname{Tr}J^2
=\operatorname{Tr}G^\dagger G
=\frac1d\sum_{\boldsymbol p}\mu_{\boldsymbol p}^2.
\]

For every non-self-inverse pair,

\[
u_{\boldsymbol p}^2+u_{-\boldsymbol p}^2
=x+x^{-1}\ge2,\qquad x=u_{\boldsymbol p}^2>0.
\]

A self-inverse characteristic has \(u_{\boldsymbol p}^2=1\).
There are

\[
\gcd(2,d)^2
=
\begin{cases}
1,&d\text{ odd},\\
4,&d\text{ even}
\end{cases}
\]

self-inverse characteristics.  Summing the pair inequalities yields

\[
\boxed{\operatorname{Tr}J^2\ge1.}
\]

Equality holds precisely when
\(u_{\boldsymbol p}^2=1\) for every characteristic.

This lower bound is exact but does not prove TCC.

## 3. The minimum-norm countermodel

The constant-overlap countermodel from cycle 14 takes
\(u_{\boldsymbol p}=1\) off zero.  It therefore attains

\[
\operatorname{Tr}J^2=1.
\]

Nevertheless it has more than one nonzero eigenvalue, so

\[
\operatorname{Tr}J^4<1
=\bigl(\operatorname{Tr}J^2\bigr)^2.
\]

Thus even all of the following together remain insufficient:

- reality and reciprocal pairing;
- Zauner covariance;
- parity-Hermiticity;
- the exact minimum Frobenius norm;
- \(\operatorname{Tr}G=\operatorname{Tr}G^2=1\).

The genuinely missing datum is the fourth-moment saturation, not a
quadratic normalization or positivity statement.

## 4. Consequence for the analytic route

Cycle 16 appeared to require a non-holomorphic identity involving
\(K^\dagger K\).  Parity-Hermiticity shows that this is not the true
obstruction.  The analytic target can be written entirely with four
copies of the signed RM matrix \(J=PG\):

\[
\operatorname{Tr}J^4
=\sum_{i,j,k,\ell}
J_{i,j}J_{j,k}J_{k,\ell}J_{\ell,i}.
\]

After inserting the sheared partial-Fourier entries, this is a finite
fourfold root-filtered RM sum.  A viable cocycle theorem need only
evaluate this scalar sum, rather than every characteristic-wise TCC
residual.

There is still a strict gate: any proposed derivation based only on
reciprocity or on the second moment also applies to the constant
countermodel and cannot force the required equality.

## 5. Claim ledger

Proved in this cycle:

- parity-Hermiticity makes \(J=PG\) Hermitian;
- the Gram matrix \(G^\dagger G\) is exactly \(J^2\);
- TCC is equivalent to the polynomial fourth-moment saturation
  \(\operatorname{Tr}J^4=(\operatorname{Tr}J^2)^2\);
- reciprocal pairing gives the sharp bound
  \(\operatorname{Tr}J^2\ge1\);
- the constant-overlap countermodel attains that bound while failing
  the fourth-moment identity.

Still open:

- evaluation of the fourfold root-filtered RM trace;
- an independent cocycle identity forcing fourth-moment saturation;
- TCC itself.

## Sources

- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- R. A. Horn and C. R. Johnson, *Topics in Matrix Analysis*,
  sections on singular values and compound matrices.
