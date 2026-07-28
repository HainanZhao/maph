# SIC--Stark research cycle 38: the minimal remaining theorem

Date: 2026-07-27

## Five-cycle synthesis

Cycle 34 proves the modulus of the primitive regulator unconditionally.
Cycles 35--37 show that ETNC, root numbers, and current \(p\)-adic Stark
theory do not supply its argument.

Write

\[
 \Lambda=L'_S(0,\chi_1),\qquad
 R=r_0+\zeta_6r_1+\zeta_6^2r_2,\qquad
 q=L'_S(0,\chi_3).
\]

We now know unconditionally that

\[
 |\Lambda|=|R|
 \quad\text{and}\quad
 q=r_0-r_1+r_2.
\]

The identity-ray differenced zeta derivative is

\[
 Z'_0=\frac{2\operatorname{Re}\Lambda+q}{3}.
\]

Consequently the entire complex equality can be reduced to

\[
 \boxed{Z'_0=r_0=2\log x}
\]

plus the sign of the imaginary part.  Indeed, the boxed real equality
gives

\[
 \operatorname{Re}\Lambda=\operatorname{Re}R.
\]

Together with \(|\Lambda|=|R|\), this leaves only
\(\Lambda=R\) or \(\Lambda=\bar R\).  The Artin direction is then selected
by proving

\[
 \operatorname{Im}\Lambda>0,
\]

which is amenable to a rigorous approximate-functional-equation bound and
is not an algebraicity problem.

Thus the irreducible arithmetic core is no longer a general complex
order-six identity.  It is one positive, identity-class Shintani value:

\[
 \exp(Z'_0/2)=x.
\]

This is exactly the scalar value approximated by Yalkinoglu's cyclic
quantum dilogarithms.  Unlike the invalid full-characteristic extension
closed in cycle 33, the scalar identity-class limit is inside the stated
scope of that work.

## Recommendation

The next proof project should be:

1. prove the scalar cyclic limit with complete error estimates from the
   announced theorem or directly from the \(q\)-Pochhammer asymptotic;
2. derive an exact renormalization or algebraic functional equation for
   that scalar limit, sufficient to show it is the isolated positive root
   of the certified degree-twelve polynomial;
3. certify \(\operatorname{Im}L'_S(0,\chi_1)>0\) analytically.

Do not reconstruct the full rational characteristic table.  Cycle 34
means only one scalar algebraicity identity is now needed; the remaining
phase follows from magnitude and sign.

## Current theorem boundary

\[
\boxed{
\begin{gathered}
\text{finite TCC certificate: exact conditional on the primitive bridge},\\
\text{lower conductor and quadratic component: unconditional},\\
\text{primitive modulus: unconditional by direct Roblot P1},\\
\text{identity-class algebraicity: still open},\\
\text{orientation sign: numerically clear and analytically certifiable}.
\end{gathered}}
\]
