# SIC--Stark research cycle 82: the second dimension-eight stratum

AFK Definition 1.27 says that the form conductor need only divide
\(f_j\).  For \(d=8\), \(K=\mathbb Q(\sqrt5)\), \(j=2\), and
\(f_2=3\).  There are therefore two genuine strata:

- conductor \(3\), discriminant \(45\), treated in the canonical closure;
- conductor \(1\), discriminant \(5\), treated in cycles 82--91.

For \(Q=\langle1,-3,1\rangle\), put
\[
C=\begin{pmatrix}3&-1\\1&0\end{pmatrix}.
\]
The AFK matrices are
\[
L_t=C,\qquad L_{z,t}=C^2=
\begin{pmatrix}8&-3\\3&-1\end{pmatrix},\qquad
A_t=C^6=\begin{pmatrix}377&-144\\144&-55\end{pmatrix}.
\]
Thus \(A_t\equiv I\pmod8\), while \(L_{z,t}\) has 22 orbits on
\((\mathbb Z/8)^2\): the zero orbit and 21 orbits of length three.

The exact audit is
`scripts/dimension_eight_maximal_tuple_audit.gp`.

