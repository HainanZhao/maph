# Cycle 25: quadratic CRT class capacity dual

Write a time as \((\alpha,\beta)\in\mathbb Z_{199}\times\mathbb Z_{14}\).
The twelve classes are the products of alpha type (zero, nonzero quadratic
residue, nonresidue) and \(\gcd(\beta,14)\in\{1,2,7,14\}\).  `PROVED`:
the prescribed alpha functions \(1\), the Legendre character extended by
zero, and the alpha-zero indicator separate those three types.  Tensoring
them with the four divisor-Ramanujan functions on \(\mathbb Z_{14}\) gives
an invertible integral evaluation matrix (the replay checks its nonzero exact
Bareiss determinant).

For nonnegative class weights \(z_r\), let \(n_r\) be class cardinalities
and let \(v_{B,o,r}\) count class-\(r\) times covered by allowed option
\(o\) of coordinate block \(B\).  Put

\[
 W=\sum_r n_rz_r,\qquad U=\sum_B\max_o\sum_rv_{B,o,r}z_r.
\]

`PROVED`: any global digit choice which covers every time has \(W\le U\),
because each time is charged to one selected block that covers it, then each
block charge is at most its displayed maximum.  Thus integral weights with
\(U<W\), followed by a fresh direct-CNF replay, exclude the named leaf.
`PROVED`: after exhaustive separation finds no violated block option, the
cutting-plane LP has exactly all finite option inequalities for its selected
partition.

The partition score, floating LP values, and failed integerization are
`OBSERVED`.  An all-unresolved run constrains only this twelve-class,
one-selected-width-four-partition family; it is neither a Fourier nor an LRC
no-go theorem.
