# SIC--Stark research cycle 83: maximal-order ray groups

For \(K=\mathbb Q(\sqrt5)\), with the paper's \(\infty_2\) convention,
PARI gives
\[
\mathrm{Cl}_{(8)\infty_2}(K)\simeq C_2^2,\qquad
\mathrm{Cl}_{(8)\infty_1\infty_2}(K)\simeq C_2^3.
\]
The forgetful map has kernel two, so Kopp's exponent is
\[
n=\frac2{|\ker|}=1.
\]
The sign class is represented by the positive integer \(7\), which is
congruent to \(-1\pmod8\).  In PARI's one-place coordinates it is
\([0,1]\).  Consequently the Kopp difference is supported on the two
quadratic characters
\[
[0,1]\quad\text{and}\quad[1,1].
\]
There is no quartic orientation problem in this stratum.

All group structures, the forgetful map, and the Rademacher value
\(\Psi(A_t)=0\) are checked exactly in
`scripts/dimension_eight_maximal_tuple_audit.gp`.

