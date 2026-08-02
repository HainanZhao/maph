# Cycle 141 preregistration: divisor-seed recurrence compiler

Date frozen: 2026-08-02 UTC.

Fix one Cycle-140 class `(u,v,A,B)` and write its input/output rational
columns in the common core `(p0,q0)`.  Suppose two distinct edges have the
same integral transition matrix.  Solve the resulting two-vector linear
system exactly and check compatibility with unimodularity and nonzero mode
difference.

Whether transition repetition succeeds or fails, retain the class-colored
fixed-difference graph.  Compute its longest guaranteed chain and the exact
number of length-two continuations from its edge count.  Compare fiber
saturation with graph edge density and state whether one implies the other.
Success may be a correction/no-go for transition repetition, but must name
the replacement invariant needed for recurrence.
