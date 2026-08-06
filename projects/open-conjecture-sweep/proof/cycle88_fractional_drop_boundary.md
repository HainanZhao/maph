# C88 exact boundary: residual fractional-cover drop fails

`PROVED`: in the published 13-edge intersecting six-partite control, delete
the vertex \((1,6)\).  The resulting nine-edge residual has an exact
fractional transversal and fractional matching of common value \(23/8\).
Thus it satisfies the `CONJECTURED` FD\(_3\) premise.

`PROVED`: no vertex deletion from that residual has fractional transversal
number at most \(2\).  Exact rational primal and dual LP certificates check
all inequalities and equal objectives for the residual and every child.
Consequently this residual refutes
\[
 \mathrm{FD}_3:\quad \tau^*(G)\leq3\ \Longrightarrow\
 \exists v\;\tau^*(G\downarrow v)\leq2.
\]

The complete declared packet deduplicates residual edge sets through depth
five: its layers contain \(1,31,420,2582,5403,6101\) states.  All 6,102
distinct exact LPs reconstruct rational primal/dual certificates; 263 rows
violate their least applicable FD\(_k\) instance.

## Claim boundary

This refutes only C88's residual fractional-cover-drop mechanism.  It does
not refute intersecting Ryser at \(r=6\), nor does it rule out another global
rounding or partition mechanism.
