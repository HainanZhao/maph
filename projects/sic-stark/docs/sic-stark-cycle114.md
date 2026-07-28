# SIC--Stark research cycle 114: standard cyclic normalization

Date: 2026-07-28

## Outcome

The moving-characteristic half-power found in cycle 66 has an exact
interpretation in the standard cyclic-dilogarithm normalization.
For a nonsingular characteristic, write \(c=z_0^n\) and let
\(D_{m/n}\) be the cyclic product with weights \(j/n\).  The complete
boundary constant is

\[
 C=
 \left(\frac12-\frac{b}{6n}\right)
 \sum_{j=0}^{n-1}\log(1-z_j)
 -\log D_{m/n}.
\]

The reciprocal standard cyclic dilogarithm has central exponent

\[
 \frac{n-1}{2n}.
\]

Consequently,

\[
\boxed{
 C=\log d_n^*(z_0)
 +\frac{3-b}{6n}\sum_{j=0}^{n-1}\log(1-z_j).
}
\]

This is coefficient-wise and therefore branch-safe.  It proves that the
regularized boundary table is not merely analogous to a cyclic
dilogarithm table: it is the standard table multiplied by one explicit
central correction.  The correction vanishes identically for \(b=3\)
and is \(O(n^{-1})\) for every characteristic.

The singular sector \(c=1\) is excluded from this formula and continues
to require the already-certified \(q\)-gamma regularization.
