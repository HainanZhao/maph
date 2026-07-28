# SIC--Stark research cycle 89: exact shifted matrices

The exact quotient ring has basis \(z^a x^b\) with
\[
0\le a<4,\qquad 0\le b<8,
\]
after imposing the shared-subfield relations from cycle 88.  The
signed overlap \(d\) is represented inside this ring, so no additional
radical generator is needed.

For determinant \(+1\), the Weyl reconstruction is the shift-one
matrix.  For determinant \(-1\), the even-dimensional wrap sign
\((-1)^p\) for nonzero second index is included; this is the shift-zero
matrix.

`scripts/dimension_eight_maximal_exact_tcc.py` verifies for each matrix:

- trace exactly one;
- all 64 entries of \(M^2-M\) exactly zero;
- all 784 two-by-two minors exactly zero.

