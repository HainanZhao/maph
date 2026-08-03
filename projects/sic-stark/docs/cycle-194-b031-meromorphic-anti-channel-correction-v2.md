# Cycle 194 / B031 correction v2: true-pole condition on the helical orbit

## Correction

`cycle-194-b031-meromorphic-anti-channel-v1` correctly establishes the six
local source principal parts and the Fourier-stable `B_(1,-)` complement.  It
incorrectly promoted an affine divisor-collision orbit to an infinite orbit
of **true** poles.  Sarkissian--Spiridonov, arXiv:1910.11747v4,
equations (9)--(10), require a pole indexed by `(j,n,m)` to satisfy

\[
j\geq0,\qquad 24n+5j+m\geq0.
\]

On the recorded collision representative

\[
(z,j,n)=(-3k,k,-k),\qquad m=N-6z=N+18k,
\]

this is exactly `N-k >= 0`.  Thus the source orbit at the canonical odd
label `N` has the finite index set `0 <= k <= N`, not an infinite tail.

## Affected and retained claims

- **Retained (`PROVED`):** all six local odd antisymmetric principal parts;
  `F_24(B_(1,-))=B_(1,-)`; and retention of the six raw spectral
  differences.
- **Corrected (`PROVED`):** each canonical odd pole has a finite coincident
  true-pole orbit of cardinality `N+1`; the six cardinalities are
  `2,4,6,8,10,12`, for 42 true-pole summands in total.  The reflected gamma
  factor is finite and nonzero at every listed summand, so every individual
  summand has a nonzero simple residue.
- **Withdrawn:** the asserted infinite residue orbit, its strict-interior
  tail convergence, and the resulting non-identically-zero sector statement.
  The affine functional-equation relation remains an identity, but it cannot
  create source poles once the displayed true-pole inequality fails.
- **Open:** whether the finite combined residues cancel, and any
  distributional/contour continuation to the real-multiplication endpoint.

This correction does not alter the sealed v1 artifact.  Its v2 record
supersedes only the affected claims and is the required input for Cycle 195.
