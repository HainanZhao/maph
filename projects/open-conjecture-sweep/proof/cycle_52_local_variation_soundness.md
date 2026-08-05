# Cycle 52 soundness note

`PROVED` finite statement only.  Let \(H\) have left vertices \(L_i\) and
right vertices \(R_j\), indexed modulo five, with \(L_iR_j\) present exactly
when \(j-i\notin\{0,-1\}\).  This gives the fifteen frozen edge factors.

For an equal \(q\)-block graphon and an enumerated integer matrix \(B\), C52
uses \(W_{ab}(\epsilon)=(1+\epsilon B_{ab})/2\).  Hence

\[
t_H(W(\epsilon))-2^{-15}
=\frac{Q_B(\epsilon)}{2^{15}q^{10}},\qquad
Q_B(\epsilon)=\sum_{f:V(H)\to[q]}
 \prod_{L_iR_j\in E(H)}(1+\epsilon B_{f(L_i),f(R_j)})-q^{10}.
\]

The enumerators use integer polynomial arithmetic for this displayed
polynomial.  Thus a first nonzero coefficient of `Q_B` has exactly the same
sign as the corresponding coefficient of the graphon density difference;
there is no floating-point subtraction.  Symmetry and weighted-zero-mean are
checked from the emitted matrix, and \(|B_{ab}|\le2\) makes every frozen
\(W(\epsilon)\) a graphon for \(0\le\epsilon\le1/2\).

The principal evaluator multiplies its fifteen factors in listed edge order.
The independent evaluator reconstructs the matrix corpus in reverse output
order and uses an out-of-place coefficient recurrence in reverse edge order.
Its recurrence is the dynamic grouping of the literal edge-subset expansion;
the latter is also evaluated explicitly for the frozen two-step hand matrix
\(\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\).  Agreement of all emitted
coefficient vectors therefore checks the finite census, not any claim about
arbitrary graphons.
