# C89 symbolic rank-one Hessian identity

Let \(W_0(x,y)=a(x)b(y)\), with \(H=K_{5,5}\setminus C_{10}\) in the
frozen 3-regular bipartite convention.  Differentiating two distinct labelled
edges partitions the 210 ordered pairs into 30 sharing a left endpoint, 30
sharing a right endpoint, and 150 disjoint pairs.  Direct factorization of
the remaining rank-one edge weights gives
\[
D^2t_H[U,U]=30A_3^4B_3^3\int aR^2+30A_3^3B_3^4\int bC^2
+150A_3^3B_3^3L^2,
\]
where \(A_3=\int a^3\), \(B_3=\int b^3\),
\(R(x)=\int b(y)^2U(x,y)dy\), \(C(y)=\int a(x)^2U(x,y)dx\), and
\(L=\int a(x)^2b(y)^2U(x,y)dxdy\).

Although \(d(W_0+\epsilon U)\) is affine, \(d^{15}\) need not have zero
second derivative: it is
\(210d(W_0)^{13}(\int U)^2\).  On the density tangent \(\int U=0\), however,
both its first and second directional derivatives vanish.  There,
\[
D\Delta[U]=15A_3^4B_3^4L,
\]
so stationarity imposes \(L=0\).  Therefore the restricted Hessian is
nonnegative.

## Claim boundary

This is a `PROVED` scoped derivation.  The three edge-pair orbit counts are
audited by `check_cycle89_rank_one_symbolic.py`; factoring the surviving
rank-one weights yields the displayed three terms, and
`check_cycle89_rank_one_symbolic_replay.py` independently compares every
finite-step Hessian coefficient against that formula at two positive rational
controls.  It concerns only second variation in stationary density-preserving
directions at positive rank-one bases, not a local or global Sidorenko
theorem.
