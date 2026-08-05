# Cycle 22: targeted width-four block deficits

Fix a canonical leaf and a partition \(\mathcal P\) of its thirteen
coordinates into one block of size four and three blocks of size three.  For
each block option \(o\), let \(b_{B,o,t}\) be one when at least one selected
coordinate in block \(B\) is bad at time \(t\).  The masks use the original
Cycle-11 direct clauses; the proved coupled CRT formula is only an equivalent
construction.

For nonnegative integer weights \(w_t\), define

\[
 W=\sum_t w_t,
 \qquad
 U_{\mathcal P}=\sum_{B\in\mathcal P}
   \max_{o\text{ allowed in }B}\sum_t w_t b_{B,o,t}.
\]

If a global leaf-admissible digit selection covers every time, it induces one
option per block and weighted counting gives \(W\le U_{\mathcal P}\).
Therefore a fully enumerated integer witness with \(U_{\mathcal P}<W\)
`PROVES` that the named leaf has no improper lift.  The argument is identical
for newly optimized weights and for weights transferred from another leaf;
only a fresh target-specific direct-clause replay can certify the target.

The partition-selection rule affects discovery but not soundness.  Failure of
the frozen ten-partition family, floating LP output, or a resource cap proves
nothing about the leaf or about other width-four families.

## Claim boundary

`PROVED`: every independently replayed strict integer deficit excludes its
named canonical leaf.  Even a successful leaf certificate does not close a
base, \(F_1\), \(J\), or LRC(13).
