# Cycle 54: bipartite directional local stability

## Theorem (`PROVED`)

For every fixed \(p\in(0,1)\), every nonzero bounded measurable kernel
\(U:X\times Y\to[-1,1]\) with \(\iint U=0\) has a
\(\delta(p,U)>0\) such that

\[
t_H(p+\epsilon U)>p^{15}
\quad\text{for }0<\epsilon<\min(\delta(p,U),p,1-p).
\]

Here \(H=K_{5,5}\setminus C_{10}\), and the density is the ordinary
bipartite-kernel homomorphism density. This is still directional local
stability only, not a uniform neighborhood or Sidorenko.

Let \(a(x)=\int_YU(x,y)dy\) and \(b(y)=\int_XU(x,y)dx\). The same exact
edge-subset expansion as C53 has 15 adjacent pairs sharing a left vertex and
15 sharing a right vertex; its quadratic coefficient is therefore

\[
15p^{13}(\|a\|_2^2+\|b\|_2^2).
\]

If either degree function is nonzero this is the positive first surviving
coefficient. If both vanish, integrating any leaf of a selected subgraph
vanishes. C53's complete frozen subset census then leaves no cubic term and
only five four-cycles at degree four. For the integral operator
\(T_U:L^2(Y)\to L^2(X)\), each contributes

\[
t_{C_4}(U)=\operatorname{tr}((T_UT_U^*)^2)=\sum_i s_i^4>0,
\]

where the \(s_i\) are singular values. Bounded nonzero \(U\) is a nonzero
Hilbert--Schmidt kernel, so at least one singular value is nonzero. The
quartic coefficient is consequently \(5p^{11}\sum_i s_i^4>0\). A finite
polynomial with this positive first nonzero coefficient is positive for all
sufficiently small positive \(\epsilon\), and the displayed bound on
\(\epsilon\) preserves \([0,1]\)-valuedness.

The frozen 2-by-3 zero-row/zero-column-sum control matrix has
\(\operatorname{tr}((BB^T)^2)=16\). Direct enumeration gives its raw fourth
coefficient as \(17,280=5\cdot2^3\cdot3^3\cdot16\), checking the
rectangular normalization.
