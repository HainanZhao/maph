# SIC--Stark research cycle 53: ghost reconstruction after phase closure

## Result

The exact phase packet determines both standard-basis ghost matrices once
the eight independent positive ray-unit square roots are selected.

The \(48\) nonzero characteristics form:

\[
16\ \text{Zauner orbits of length }3,
\]

and reciprocity pairs these into

\[
8\ \text{independent orbit variables}.
\]

Thus the apparent \(48\)-value problem is an eight-variable algebraic
problem.  The exceptional zero characteristic remains fixed at
\(\sqrt8\) before Weyl reconstruction.

For the identity twist, numerical reconstruction gives

\[
|\operatorname{Tr}\Pi-1|<3.2\cdot10^{-16},\qquad
\|\Pi^2-\Pi\|_{\max}<4.8\cdot10^{-10}.
\]

For the determinant-minus-one twist the corresponding bounds are
\(8.1\cdot10^{-16}\) and \(4.8\cdot10^{-10}\).

## Interpretation

The singular norm is greater than one because the ghost is a rank-one
idempotent with parity adjoint symmetry, not necessarily an orthogonal
projector.  Rank is therefore tested through minors and idempotency, not
through a single singular value equal to one.

The two reconstructions are audited by
`scripts/dimension_seven_tcc_shifts.py`.

