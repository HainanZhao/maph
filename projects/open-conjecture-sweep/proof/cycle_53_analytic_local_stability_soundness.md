# Cycle 53: directional local stability at (Wequiv 1/2)

## Theorem (`PROVED`)

Let (H=K_{5,5}\setminus C_{10}), with the frozen modulo-five convention.
Let (U:[0,1]^2\to[-1,1]) be measurable and symmetric, with
\(\iint U=0\), and assume (U\ne0) almost everywhere.  Then there is a
\(\delta(U)>0\) such that, for every
\(0<\epsilon<\min(\delta(U),1/2)\),

\[
t_H(1/2+\epsilon U)>2^{-15}.
\]

This is directional local stability at one constant graphon.  It is not a
uniform neighborhood theorem, and does not prove Sidorenko.

## Exact expansion

For a selected edge set (F\subseteq E(H)), write
\(I_F(U)=\int\prod_{xy\in F}U(x,y)\).  Finite expansion gives

\[
t_H(1/2+\epsilon U)-2^{-15}
=\sum_{\varnothing\ne F\subseteq E(H)}
 2^{-(15-|F|)}\epsilon^{|F|}I_F(U). \tag{1}
\]

The one-edge term vanishes by the zero-mean hypothesis.  Of the 105 two-edge
sets, the exact frozen enumeration finds 30 adjacent pairs and 75 disjoint
pairs.  A disjoint pair contributes \((\iint U)^2=0\).  For each adjacent
pair, integrating the two leaves gives
\(\int d_U(x)^2dx\), where \(d_U(x)=\int U(x,y)dy\).  Thus the quadratic
coefficient in (1) is exactly

\[
30\,2^{-13}\|d_U\|_2^2. \tag{2}
\]

If (d_U=0) a selected graph with a degree-one vertex has zero integral:
integrate that leaf, obtaining (d_U).  The complete 15-edge subset census
has no minimum-degree-two three-edge set.  At four edges it has exactly five
such sets, each a four-cycle; every other four-edge set has a leaf.  Each
cycle contributes

\[
\int U(x_1,y_1)U(y_1,x_2)U(x_2,y_2)U(y_2,x_1)
=\operatorname{tr}(T_U^4), \tag{3}
\]

where (T_Uf(x)=\int U(x,y)f(y)dy\).  Consequently the cubic coefficient is
zero on this kernel and the quartic coefficient is

\[
5\,2^{-11}\operatorname{tr}(T_U^4). \tag{4}
\]

Because bounded (U\) is Hilbert--Schmidt and symmetric, (T_U) is compact
self-adjoint.  If (U\ne0) then (T_U\ne0), so its real eigenvalues have
\(\sum\lambda_i^4=\operatorname{tr}(T_U^4)>0\).  Formula (2), or on its
kernel formula (4), is therefore the first nonzero coefficient in (1).
Since (1) is a finite degree-15 polynomial in \(\epsilon\), it is positive
for all sufficiently small positive \(\epsilon\).  Finally,
\(|U|\le1\) makes (1/2+\epsilon U\in[0,1]\) for
\(0<\epsilon\le1/2\), proving the theorem.

## Exact finite trace control

For the frozen (q=3) step matrix
\(B=\begin{pmatrix}1&-1&0\\-1&1&0\\0&0&0\end{pmatrix}\),
the raw fourth coefficient is 58,320.  The exact relation
\(58,320=5\cdot3^6\operatorname{tr}(B^4)\), with
\(\operatorname{tr}(B^4)=16\), checks the normalization used in (3).
