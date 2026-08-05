# Endpoint interpolation for the compatible three-qubit gate

## Theorem — PROVED

Let \(\rho_{ABC}\) be any three-qubit state, let \(a,b,c\ge0\) with
\(a+b+c=1\), and let \(Q\) be any qubit state.  Then the compatible
two-body alignment operator is majorized by its aligned target:

\[
 a\rho_{AB}\otimes Q_C+b\rho_{AC}\otimes Q_B+cQ_A\otimes\rho_{BC}
 \preceq
 aP_{00,AB}\otimes Q_C+bP_{00,AC}\otimes Q_B+cQ_A\otimes P_{00,BC}.
\]

Every \(AC\) term is embedded in the ambient order \(A,B,C\): its first
factor occupies \(A,C\), while the displayed \(Q_B\) occupies the middle
slot.  The same convention applies to the target.

Consequently Song--Chen Conjecture 2 holds for all compatible three-qubit
states when \(\mu\) is supported on \(AB,AC,BC\), with arbitrary weights and
an arbitrary qubit state \(Q\).  This does not cover other subset supports,
more parties, or local dimension above two.

## Proof

Choose a one-qubit unitary \(U\) with \(UQU^\dagger=Q_q=
\operatorname{diag}(q,1-q)\), \(1/2\le q\le1\), and simultaneously conjugate
the global state by \(U^{\otimes3}\).  Its marginals remain compatible; both
alignment operators are conjugated by \(U^{\otimes3}\), so majorization is
unchanged.  It therefore suffices to prove the diagonal-\(Q_q\) statement.

Put \(t=2q-1\).  Since each supported term has exactly one complement qubit,

\[
Q_q=(1-t)I/2+tP_0,\qquad
H_q=(1-t)H_{1/2}+tH_1,\qquad
T_q=(1-t)T_{1/2}+tT_1.
\]

Song--Chen Proposition 3 gives \(H_{1/2}\preceq T_{1/2}\): their displayed
operator has \(I\) in the complement slot and is exactly twice ours at
\(Q=I/2\).  At the other endpoint, \(H_1\) is positive semidefinite of trace
one, whereas \(T_1=P_{000}\).  Hence \(H_1\preceq T_1\).

Permute the systems so \(a\ge b\ge c\).  In the computational basis the
target spectrum, already in nonincreasing order, is

\[
\lambda(T_q)=\bigl(q,(1-q)a,(1-q)b,(1-q)c,0,0,0,0\bigr).
\]

The order holds since \(q\ge1-q\ge(1-q)a\).  Thus all seven nontrivial Ky
Fan sums of \(T_q\) are affine in \(t\).  Ky Fan convexity therefore gives

\[
K_k(H_q)\le(1-t)K_k(H_{1/2})+tK_k(H_1)
\le(1-t)K_k(T_{1/2})+tK_k(T_1)=K_k(T_q)
\]

for every \(k\), with equal traces.  This proves the majorization. \(\square\)

## Exact replay

```sh
python3 proof/check_cycle78_endpoint_interpolation.py
```
