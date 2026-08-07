# Oracle selection: C105 complement-translate autocorrelation obstruction

**`CONJECTURED` selection:** retain active F001 book-Ramsey and test the
global deterministic transition (C=A\sqcup Bs\) in (D_{2q}), with

\[
q\equiv7\pmod8,qquad 0\notin A=-A\subseteq\mathbb Z_q,qquad
B=\mathbb Z_q\setminus A.
\]

This leaves C101's fixed six-block signs, C103's local inversion bits, and
C104's four character-orbit bits. It is not an arbitrary-set census: the
proposed invariant is the rotation autocorrelation
\(P_A(t)=\sum_x1_A(x)1_A(x-t)\), compressed by the Seidel coefficient
condition, its zero-frequency sum, and the pairing
\((x,y)\mapsto(-y,-x)\) in the fiber (x-y=t).

The direct target coefficient condition is
\(1_C(g)+(1_C*1_C)(g)\in\{(q-1)/2,(q+1)/2\}\) for every (g\ne e).
For rotations it forces constant (P_A(t)=|A|-(q+1)/4). Summing produces
\(|A|=(q\pm1)/2\); symmetry forces the plus root, hence the constant is
\((q+1)/4\), which is even. The pairing then gives
\(P_A(t)\bmod2=1_A(t/2)\), forcing (A=\varnothing), a contradiction.
This remains a design claim until the two frozen exact routes verify every
algebraic step.

The smallest verifier checks group-ring coefficients and direct Seidel matrix
products for fixed q=7 and q=23 controls, and independently checks the scalar
quadratic and parity-pairing identities. Falsifiers: any route disagreement,
a failed pairing identity, or a symmetric nonzero (A) with complement (B)
passing the Seidel condition. Cap: one CPU, 60 seconds, 64 MiB RAM, 1 MiB disk.
No affine decimation, arbitrary (B), further orbit bits, or subset census.
