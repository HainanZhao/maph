# C89 rank-one stationary Hessian theorem

`PROVED`: let \(H=K_{5,5}\setminus C_{10}\) in the pinned 3-regular
bipartite convention, and let \(W_0(x,y)=a(x)b(y)\) be a positive bounded
rank-one bigraphon (so \(0<a(x)b(y)\leq1\) almost everywhere).  Write
\(\Delta(W)=t_H(W)-(\int W)^{15}\).  For every bounded measurable direction
\(U\) satisfying
\[
 \int U=0\quad\hbox{and}\quad D\Delta(W_0)[U]=0,
\]
one has \(D^2\Delta(W_0)[U,U]\geq0\).

Indeed, with \(A_3=\int a^3\), \(B_3=\int b^3\),
\(R(x)=\int b(y)^2U(x,y)\,dy\),
\(C(y)=\int a(x)^2U(x,y)\,dx\), and
\(L=\int a(x)^2b(y)^2U(x,y)\,dxdy\), ordered distinct edge pairs give
\[
D^2t_H[U,U]=30A_3^4B_3^3\int aR^2+
30A_3^3B_3^4\int bC^2+150A_3^3B_3^3L^2.
\]
The three coefficients are the exact ordered edge-pair orbit counts
shared-left/shared-right/disjoint = \(30/30/150\).  On the density tangent,
\(D\Delta(W_0)[U]=15A_3^4B_3^4L\) and
\[
D^2(\int W)^{15}[U,U]=210\Bigl(\int W_0\Bigr)^{13}\Bigl(\int U\Bigr)^2=0.
\]
Thus stationarity gives \(L=0\) (the prefactor is strictly positive), and
the asserted nonnegativity follows.
`check_cycle89_rank_one_symbolic.py` audits the counts, and the independent
labelled-map replay compares every finite-step Hessian coefficient with this
formula at both frozen equal-atom and asymmetric rational controls.

`PROVED`: at the frozen equal-atom \(3\times3\) control
\[
r=(1/4,1/2,3/4),\qquad c=(1/3,1/2,2/3),\qquad W_0=rc^T,
\]
the density-tangent and first-deficit-stationary space has dimension seven
and its restricted Hessian has all 127 rational principal minors
nonnegative.  Direct enumeration of all \(3^{10}=59,049\) labelled maps
gives density \(1/4\) and base deficit
\(153275/8349416423424\).  Its independent degree-15 line expansion agrees
with the derivative route in the linear and quadratic coefficients.

## Claim boundary

This is a second-variation theorem only.  Semidefinite stationary curvature
does not establish a local minimum (higher-order flat directions remain), a
global Sidorenko inequality, or any counterexample.  The source screen is
`OBSERVED` rather than a novelty claim; publication requires a full primary
source and hostile-audit pass.
