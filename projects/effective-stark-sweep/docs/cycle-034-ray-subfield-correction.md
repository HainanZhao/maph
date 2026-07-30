# Cycle 034 — ray-subfield correction

Route 2 now uses the subgroup returned by `rnfconductor` and rebuilds
`bnrclassfield(bnr,H)`.  The corrected object is compared to the Route-1
normal closure by exact field isomorphism.  This restored agreement in
all eligible pilot cases.
