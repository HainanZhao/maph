# Cycle 9 decision: all-q Walsh marginals

`PROVED`: For an exact four-state spin-structure TT of bond at most `d`, all
four single-handle Walsh marginals at every handle, with arbitrary
product-form weights on the other handles, require `O(g*4*d^2)` dense ring
operations after the TT is supplied.

`CERTIFIED_NUMERICAL`: The implementation agrees with explicit enumeration
on `G_(6,3)` and `G_(7,3)` over `GF(1000000007)` and `GF(1000000009)`.  The
tests cover 1024 and 4096 spin structures respectively and freeze every
output residue.

The result completes Upgrade 3 in `LANE_B_GOAL.md`.  It demonstrates an
all-family use of the TT with `4g` output values, versus inspecting `4^g`
sector entries.  It does not claim an advantage over ordinary transfer for
computing the physical partition function once, and it has no thermodynamic
or critical-temperature implication.
