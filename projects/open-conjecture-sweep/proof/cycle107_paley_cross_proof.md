# C107 fixed-Paley-cross bi-translation obstruction

**`PROVED` claim (conditional only on the stated state).**  Let \(q\equiv
7\pmod8\) be a prime power and \(G=(\mathbb F_q,+)\).  Let
\(T_{xy}=\chi(y-x)\), with \(\chi(0)=0\), and \(Q=I-T\).  There are no
symmetric translation Seidel blocks \(P_0,P_1\) with zero diagonal,
off-diagonal entries \(\{\pm1\}\), and row sum \(-2\), for which
\[
 S=\begin{pmatrix}P_0&Q\\Q^{\mathsf T}&P_1\end{pmatrix}
\]
has every off-diagonal entry of \(S^2\) in \(\{0,-4\}\).

For \(q\equiv3\pmod4\), \(T^{\mathsf T}=-T\), \(T\mathbf1=0\), and
the quadratic-character correlation identity gives
\(TT^{\mathsf T}=qI-J\).  Therefore
\[
 Q\mathbf1=\mathbf1,\qquad QQ^{\mathsf T}=(q+1)I-J,
 \qquad Q^{-1}=\frac{Q^{\mathsf T}+J}{q+1}. \tag{1}
\]

All translation matrices commute.  Thus the upper-right block of \(S^2\) is
\[
 (S^2)_{01}=P_0Q+QP_1=Q(P_0+P_1). \tag{2}
\]
Its every row has sum \(-4\).  If its entries lie in \(\{0,-4\}\), each
row has exactly one \(-4\).  Translation invariance makes their locations a
single shift, so for some translation permutation matrix \(R_c\),
\[
 Q(P_0+P_1)=-4R_c. \tag{3}
\]
Multiplying (3) by the inverse in (1) gives
\[
 P_0+P_1=-\frac4{q+1}(Q^{\mathsf T}+J)R_c. \tag{4}
\]
Every entry of the left side is an even integer.  Since the entries of
\(Q^{\mathsf T}+J\) are \(0\) or \(2\), while each row contains a \(2\),
the right side has a nonzero entry \(-8/(q+1)\).  At \(q=7\) it is \(-1\);
for \(q>7\), \(q+1\ge16\), so it is nonintegral.  Either case contradicts
the even-integral left side.

This closes only the displayed fixed-Paley-cross two-layer translation family.
It does not exclude a different cross block, nontranslation states, a
conference/PC-graph construction, or the general book-Ramsey problem.
