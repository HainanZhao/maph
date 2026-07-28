# SIC--Stark research cycle 39: the scalar normalization is exact

Date: 2026-07-27

## Outcome

The remaining dimension-six scalar has now been normalized from
Yamamoto's definition together with the proved, convention-matched Kopp
specialization.  There is no unresolved square, sign, or reciprocal:

\[
 \boxed{\exp(D_0/2)=x_{\mathrm{an}}.}
\]

Here

\[
 D_0=\zeta'(0,C)-\zeta'(0,\bar C)
\]

is the differenced derivative for the identity class \(C\), and
\(x_{\mathrm{an}}>1\) is the positive principal three-double-sine overlap
in the reciprocal convention used by the SIC calculation.

## Derivation

Yamamoto defines

\[
 X(C)=
 \exp\bigl(-\zeta'(0,C)+\zeta'(0,\bar C)\bigr)
 =\exp(-D_0)
\]

and proves the factorization

\[
 X(C)=X_1(C)X_2(C).
\]

For the rational principal ideal \((6)\), the initial cone pair is

\[
 (x_0,y_0)=(1,1/6).
\]

The already-audited specialization of Kopp's proved Kronecker-limit
theorem gives the decisive relation directly:

\[
 \exp(D_0)=|\widetilde\nu_{0,1}|^2=x_{\mathrm{an}}^2.
\]

Consequently

\[
 \exp(-D_0)=x_{\mathrm{an}}^{-2},
 \qquad
 D_0=2\log x_{\mathrm{an}}.
\]

This is also consistent with Yalkinoglu's rational-modulus cyclic
specialization \(X_1((6))=X_2((6))=x_{\mathrm{an}}^{-1}\).
Thus the normalization does not depend on the announced
cyclic-quantum-dilogarithm theorem.

## What remains

Let \(x_{\mathrm{alg}}\) be the isolated root in
\((2.212885,2.212886)\) of

\[
\begin{aligned}
Q(X)={}&X^{12}+3X^{11}-6X^{10}-16X^9+3X^8+27X^6\\
&+3X^4-16X^3-6X^2+3X+1.
\end{aligned}
\]

The missing theorem is exactly

\[
 \boxed{x_{\mathrm{an}}=x_{\mathrm{alg}}.}
\]

The normalization audit does not prove this algebraicity statement.  It
does prove that this one equality is neither stronger nor weaker than the
identity-class bridge required in cycle 38.

## Sources

- S. Yamamoto, *On Kronecker limit formulas for real quadratic fields*,
  Theorem 5.1 and the definition preceding it,
  <https://arxiv.org/abs/math/0602615>.
- B. Yalkinoglu, *A note on Shintani's invariants*, especially the
  principal rational-ideal specialization,
  <https://arxiv.org/abs/2408.07309>.
- G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, <https://arxiv.org/abs/2411.06763>.
