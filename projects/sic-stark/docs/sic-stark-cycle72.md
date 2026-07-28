# SIC--Stark research cycle 72: normal closures in dimension eight

The two primitive quartic fields

\[
\begin{aligned}
P_0&=X^8-6X^6-30X^4-18X^2+9,\\
P_1&=X^8+6X^6-30X^4+18X^2+9
\end{aligned}
\]

have degree-sixteen normal closures with transitive Galois group
`SmallGroup(16,13)`.  Each normal closure has exactly seven quadratic
subfields:

\[
\mathbf Q(\sqrt5),\ \mathbf Q(\sqrt3),\ \mathbf Q(\sqrt{15}),
\ \mathbf Q(\sqrt{-2}),\ \mathbf Q(\sqrt{-6}),
\ \mathbf Q(\sqrt{-10}),\ \mathbf Q(\sqrt{-30}).
\]

Restricting the induced two-dimensional character to each index-two
subgroup gives character norm two precisely over
\(\mathbf Q(\sqrt5)\), \(\mathbf Q(\sqrt{-6})\), and
\(\mathbf Q(\sqrt{-30})\).  Thus the projective CM observation lifts to
two concrete candidates for linear quadratic reinduction.

Reproduction:

```bash
gp -q scripts/dimension_eight_linear_cm_reinduction.gp
```
