# N=11 residual-zero mining

This note isolates the four-mode, eleven-boson residual examples from
the larger thesis scan.  All computations use the exact integer phase
histogram in `src/fourier_suppression.py`; no floating-point zero test is
used.

The affine certificates and hidden identity are reproduced with:

```console
python3 scripts/analyze_n11_affine.py
```

## 1. The 16 listed classes are four reflection classes

The current canonicalization uses independent cyclic rotations and
input/output exchange, but not reflection.  Reflection is a valid
zero-preserving operation for a Fourier matrix: replacing mode \(k\)
by \(-k\) conjugates the relevant Fourier phases.  Allowing independent
dihedral transformations on the input and output reduces the 16
rotation-canonical \(N=11\) residual classes to four:

\[
\begin{aligned}
A&:(0,1,3,7)\longrightarrow(1,3,2,5),\\
B&:(0,1,3,7)\longrightarrow(1,3,3,4),\\
C&:(0,3,3,5)\longrightarrow(1,1,2,7),\\
D&:(1,1,2,7)\longrightarrow(1,1,3,6).
\end{aligned}
\]

Each of these has four representatives under the older
rotation-only canonicalization.  Thus 16 is not the number of
independent mechanisms.

## 2. Natural affine continuations are finite-root phenomena

Keep all small coordinates fixed and vary the dominant coordinate
while preserving the total particle number on the two sides:

\[
\begin{array}{c|c|c|c}
\text{line}&r(x)&s(x)&\text{admissible }x\\ \hline
L_A&(0,1,3,x)&(1,3,2,x-2)&x\geq2\\
L_B&(0,1,3,x)&(1,3,3,x-3)&x\geq3\\
L_C&(0,3,3,x)&(1,1,2,x+2)&x\geq0\\
L_D&(1,1,2,x)&(1,1,3,x-1)&x\geq1.
\end{array}
\]

There is a useful general reason these lines are exactly decidable.  If

\[
r(x)=(r_0,r_1,r_2,x),\qquad
s(x)=(s_0,s_1,s_2,x+d),
\]

then, after division by \(x!\), the unnormalised Fourier amplitude is a
polynomial in \(x\) on each residue class modulo four.  Indeed, expand
the fixed product \(L_0^{s_0}L_1^{s_1}L_2^{s_2}\).  Every monomial leaves
a coefficient from \(L_3^{x+d}\) of the form

\[
\frac{(x+d)!}{(x-u_3)!}\times\text{(a fixed phase and rational
factor)}.
\]

The phase involving the growing fourth mode depends only on
\(x\bmod4\).  The polynomial degree is at most
\(r_0+r_1+r_2\).  Consequently finitely many exact values determine
each residue polynomial, and an exact polynomial gcd of its real and
imaginary parts decides all zeros on the line.

That calculation gives the following common factors, up to a nonzero
constant on each residue class:

\[
\begin{array}{c|c|c}
\text{line}&\gcd(\Re A_x,\Im A_x)&
\text{admissible dark parameters}\\ \hline
L_A&(x-2)(x-5)(x-7)&2,5,7\\
L_B&x-7&7\\
L_C&x(x-3)(x-5)(x+1)(x+2)&0,3,5\\
L_D&(x-1)(x-2)(x-7)&1,2,7.
\end{array}
\]

The cofactors are coprime over \(\mathbb Q\) on every residue class, so
the table is an exact, computer-assisted classification of these four
one-parameter lines, not merely a bounded scan.

The roots connect several earlier residual censuses:

- \(L_A\): \(N=6,9,11\);
- \(L_B\): \(N=11\);
- \(L_C\): \(N=6,9,11\);
- \(L_D\): \(N=5,6,11\).

In particular, all four \(N=11\) reflection classes occur as isolated
roots of low-degree affine amplitude polynomials.  None of these
natural lines is an infinite dark family.

## 3. A hidden identity between two lines

Exact histograms satisfy

\[
\operatorname{hist}\!\left(
(0,1,3,x+2),(1,3,2,x)\right)
=
\operatorname{hist}\!\left(
(0,3,3,x),(1,1,2,x+2)\right).
\]

This was checked directly for \(0\leq x\leq200\).  Together with the
quasipolynomial degree bound above, seven exact samples in each residue
class already suffice for a computer-assisted identity proof.  It
explains the shifted factors

\[
(x-2)(x-5)(x-7)\quad\leftrightarrow\quad
x(x-3)(x-5)
\]

and shows that the \(L_A\) and \(L_C\) \(N=11\) events have identical
phase histograms despite not being related by the elementary
occupation symmetries currently used.  A direct coefficient or
creation-operator proof of this identity is a promising small theorem.

## 4. Attempts to obtain an infinite ray

The following continuations did not preserve darkness:

- uniform scaling \(r\mapsto qr,\ s\mapsto qs\): only \(q=1\) was dark
  for each prototype, checked for \(1\leq q\leq12\);
- uniform occupation layers \(r\mapsto r+t(1,1,1,1)\) and similarly for
  \(s\): only \(t=0\), checked for \(0\leq t\leq12\);
- all nonnegative increment pairs \(v,w\) with
  \(\sum v=\sum w\in\{1,2,3\}\): none stayed dark for
  \(t=0,1,2,3,4\) along \(r+tv,\ s+tw\).

Two broader rays had isolated recurrences:

\[
\begin{aligned}
(0,3+2t,3,5)&\to(1,1+t,2+t,7)
&&\text{was dark at }t=0,1,5
\quad(0\leq t\leq200),\\
(1+t,1+2t,2,7)&\to(1,1,3+3t,6)
&&\text{was dark at }t=0,1,3
\quad(0\leq t\leq30).
\end{aligned}
\]

These are leads for hypergeometric factorization, not evidence of an
infinite family.

## 5. Consequence for the thesis direction

The \(N=11\) examples do not currently support the “finite generators
under uniform layers” hypothesis.  They instead suggest a sharper
mechanism:

> Fixed-offset occupation rays give residue-class quasipolynomials, and
> residual dark events can occur as arithmetic roots shared by their
> real and imaginary components.

This is structurally different from both cyclic suppression and the
odd-\(a\) reflection family.  The best next steps are:

1. prove the \(L_A/L_C\) histogram identity directly;
2. package the quasipolynomial lemma and gcd calculation as a formal
   proposition;
3. search for repeated common factors across the \(N=5,6,8,9\)
   residual censuses;
4. test whether robustness under phase perturbations distinguishes
   isolated polynomial-root zeros from symmetry- or parity-protected
   zeros.
