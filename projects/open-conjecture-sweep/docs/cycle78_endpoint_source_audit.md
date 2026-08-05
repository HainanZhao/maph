# C78 endpoint source and scope audit

## Source theorem — PROVED

Song and Chen, *A counterexample to the strong spin alignment conjecture*,
arXiv:2603.25410, Conjecture 2, defines the compatible-marginal statement.
Its Proposition 3 states that for every three-qubit state \(\rho_{ABC}\) and
every \(a,b,c\ge0\) with \(a+b+c=1\),

\[
a\rho_{AB}\otimes I_C+b\rho_{AC}\otimes I_B+cI_A\otimes\rho_{BC}
\preceq
aP_{00,AB}\otimes I_C+bP_{00,AC}\otimes I_B+cI_A\otimes P_{00,BC}.
\]

This is exactly the \(Q=I/2\) endpoint after multiplication by \(1/2\).
The source permits arbitrary nonnegative weights and a mixed global state;
therefore it applies without a pure-state reduction.

## C78 algebra audit — PROVED

For a qubit state, a common local basis gives
\(Q_q=\operatorname{diag}(q,1-q)\), \(q\in[1/2,1]\), and
\(Q_q=(1-t)I/2+tP_0\), \(t=2q-1\).  Because each C78 support term has exactly
one complement qubit, both the compatible operator and its aligned target are
affine in \(t\).

At \(t=1\), the compatible operator is positive semidefinite of trace one;
the aligned target is \(P_{000}\), so it majorizes every density matrix.
After a subsystem permutation ordering \(a\ge b\ge c\), the target spectrum
is \((q,(1-q)a,(1-q)b,(1-q)c,0^4)\), in that order throughout the parameter
range.  Hence its Ky Fan sums are affine in \(t\), which is the equality
needed to combine the two endpoint inequalities by Ky Fan convexity.

## Novelty boundary — OBSERVED

An exact-statement and arXiv/title/citation screen through 2026-08-05 found
no source stating this compatible arbitrary-qubit extension.  This bounded
absence does not establish novelty.  The C78 theorem claim rests on the proof,
not on novelty; paper-stage literature audit remains required.
