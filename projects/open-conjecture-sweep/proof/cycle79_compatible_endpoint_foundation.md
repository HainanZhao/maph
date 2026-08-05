# Independent foundation for the compatible three-qubit \(Q=I/2\) endpoint

## Theorem — PROVED

Let \(\rho_{ABC}\) be a three-qubit density matrix and let
\(a,b,c\geq0\) with \(a+b+c=1\). Then

\[
 a\rho_{AB}\otimes I_C+b\rho_{AC}\otimes I_B+cI_A\otimes\rho_{BC}
 \preceq
 aP_{00,AB}\otimes I_C+bP_{00,AC}\otimes I_B+cI_A\otimes P_{00,BC}.
 \tag{E}
\]

The \(AC\) term is in ambient \(ABC\) order. Multiplying (E) by \(1/2\)
is precisely the compatible, pair-support \(Q=I/2\) endpoint. This proof
does not invoke Song--Chen Proposition 3.

## Ordered prefixes

After permuting systems, take \(a\ge b\ge c\), define

\[
\begin{aligned}
X_1&=\rho_{AB}\otimes I_C,\\
X_2&=\rho_{AB}\otimes I_C+\rho_{AC}\otimes I_B,\\
X_3&=\rho_{AB}\otimes I_C+\rho_{AC}\otimes I_B+I_A\otimes\rho_{BC},
\end{aligned}
\]

and let \(T_j\) replace the marginals in \(X_j\) by \(P_{00}\). Then

\[
H=(a-b)X_1+(b-c)X_2+cX_3,\qquad
T=(a-b)T_1+(b-c)T_2+cT_3. \tag{1}
\]

We prove \(X_j\preceq T_j\).

For \(X_1\), every eigenvalue of \(\rho_{AB}\) is at most one, so its
first two Ky Fan sums after tensoring by \(I_C\) are at most \(1,2\), and
its trace is \(2\). Hence

\[
\lambda(T_1)=(1,1,0,0,0,0,0,0),\qquad X_1\preceq T_1. \tag{2}
\]

For a pure pair in \(X_2\), write the two extended rank-two projections as
\(P=VV^\dagger\), \(Q=WW^\dagger\), and write the two normalized
coefficient matrices as \(\Phi,\Psi\). The overlap \(V^\dagger W\) is a
transpose of \(\Phi^\dagger\Psi\). Its singular values \(s_1\ge s_2\ge0\)
satisfy

\[
s_1+s_2=\|\Phi^\dagger\Psi\|_1
 \le\|\Phi\|_F\|\Psi\|_F=1. \tag{3}
\]

A singular-value decomposition of \(V^\dagger W\) decomposes the two
ranges into principal-angle planes. On the plane for \(s_i\), \(P+Q\) has
eigenvalues \(1+s_i,1-s_i\) (with the usual one-dimensional limiting
interpretation at \(s_i=1\)). Thus its four principal-angle eigenvalues are

\[
1+s_1,\quad1+s_2,\quad1-s_2,\quad1-s_1. \tag{4}
\]

Its first three Ky Fan sums are at most \(2,3,4\), matching
\(\lambda(T_2)=(2,1,1,0,0,0,0,0)\). Independent spectral decompositions
of the two mixed marginals and convexity of each Ky Fan sum extend this to
\(X_2\preceq T_2\).

## Three-prefix bound

For each Ky Fan index, convexity reduces \(X_3\) to a pure global state.
Local unitaries give one-qubit marginals

\[
\rho_i=\operatorname{diag}(1-r_i,r_i),\quad 0\le r_i\le\tfrac12.
\]

The published Higuchi--Sudbery--Szulc polygon theorem gives
\(r_i\le r_j+r_k\). Set \(s=r_A+r_B+r_C\), \(\delta=(1-s)_+\), and

\[
D=\rho_A\otimes I\otimes I+I\otimes\rho_B\otimes I+
 I\otimes I\otimes\rho_C-I. \tag{5}
\]

The identity
\(\sigma_yM^T\sigma_y=(\operatorname{Tr}M)I-M\), expanded on all three
factors, gives

\[
X_3=D+\rho+\widetilde\rho,\quad
\widetilde\rho=(\sigma_y^{\otimes3})\rho^T(\sigma_y^{\otimes3})
\succeq0. \tag{6}
\]

The eight diagonal entries of \(D\) are

\[
2-s,\;1-s+2r_C,\;1-s+2r_B,\;1-s+2r_A,\;
s-2r_A,\;s-2r_B,\;s-2r_C,\;s-1. \tag{7}
\]

Let \(h_1\ge\cdots\ge h_8\) be these entries in nonincreasing order. The
polygon inequalities imply

\[
h_8=s-1,\qquad K_r(D)\le r+\delta\quad(r=1,2,3). \tag{8}
\]

The exact replay checks every affine row of (8) on both polygon-polytope
regimes. Since \(X_3\succeq D\), and \(X_3\succeq0\),

\[
\lambda_i(X_3)\ge h_i,\qquad
\lambda_8(X_3)\ge\max(h_8,0)=h_8+\delta. \tag{9}
\]

As \(\operatorname{Tr}D=4\) and \(\operatorname{Tr}X_3=6\), the bottom
\(8-r\) eigenvalues satisfy

\[
\sum_{i=r+1}^{8}\lambda_i(X_3)
 \ge\sum_{i=r+1}^{7}h_i+h_8+\delta
 =4-K_r(D)+\delta.
\]

Consequently,

\[
K_r(X_3)\le2+K_r(D)-\delta\le r+2\quad(r=1,2,3). \tag{10}
\]

For \(r\ge4\), positivity and trace give \(K_r(X_3)\le6\). These are the
Ky Fan sums of

\[
\lambda(T_3)=(3,1,1,1,0,0,0,0),
\]

so \(X_3\preceq T_3\).

## Assembly

Ky Fan subadditivity and (1) imply

\[
K_r(H)\le(a-b)K_r(T_1)+(b-c)K_r(T_2)+cK_r(T_3). \tag{11}
\]

The targets are diagonal with a common nested order, and the right side is
exactly \(K_r(T)\) for every \(r=1,\ldots,8\), where

\[
\lambda(T)=(1,a,b,c,0,0,0,0).
\]

The eight exact target rows are replayed. Equal trace proves (E).

## Exact replay

    python3 proof/check_cycle79_compatible_endpoint_foundation.py

The checker verifies the 64 matrix-unit spin-flip identities, the complete
finite target assembly, and every affine \(D\)-spectrum row on the exact
polygon polytope. It does not replace the published polygon theorem.
