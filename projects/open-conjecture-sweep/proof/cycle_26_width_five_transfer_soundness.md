# Cycle 26: compact width-five transferred-weight capacity test

Let \(w_t\) be the positive integer time weight from Cycle 22's named
base-4/leaf-952 certificate.  The direct replay establishes `PROVED` that it
has support 176, total \(W=65{,}528\), and width-four capacity
\(U=65{,}440\) on that row's frozen partition.

For any leaf and a coordinate partition \(\mathcal B\), define

\[
 U_{\mathcal B}(w)=\sum_{B\in\mathcal B}
 \max_{o\text{ allowed on }B}\sum_{t\text{ covered by }o}w_t.
\]

`PROVED`: a full allowed digit assignment covering every denominator time
would satisfy \(W\le U_{\mathcal B}(w)\): charge each weighted time to one
block that covers it and bound each block's charge by its maximum.  Thus a
fresh direct replay with \(U<W\) excludes its named leaf.

Cycle 26 selects the five coordinates with smallest allowed-digit counts
(ties by index), then the next four and final four, canonically ordered.
The complete target sweep and its independent option enumeration are
`OBSERVED`: the fixed source weight gives no strict deficit on any of the 60
Cycle-25 survivors.  This concerns one inherited sparse weight and one fixed
5+4+4 geometry only; it neither rules out width five nor fresh weights,
other partitions, semantic lifts, or LRC(13).
