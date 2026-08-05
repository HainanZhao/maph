# Cycle 18: conditional pair-choice Hall certificates

Fix a base, a canonical leaf, and a partition \(\mathcal P\) of the thirteen
coordinates into disjoint singleton or two-coordinate blocks.  For a block
\(B\), an allowed block option chooses one allowed digit at each coordinate in
\(B\).  Let \(b_{B,o,t}=1\) when at least one choice in option \(o\) is bad at
time \(t\).  Thus a time covered twice inside a pair is counted only once.

For nonnegative integer weights \(w_t\), define

\[
 W=\sum_t w_t,
 \qquad
 U_{\mathcal P}=\sum_{B\in\mathcal P}
   \max_{o\text{ allowed in }B}\sum_t w_t b_{B,o,t}.
\]

Any global digit selection that covers every time induces one option in each
block.  Weighted coverage gives

\[
 W\le \sum_{B\in\mathcal P}\sum_t w_t b_{B,o_B,t}
   \le U_{\mathcal P}.
\]

Therefore \(U_{\mathcal P}<W\) is an exact leaf contradiction.  Pair blocks
can be strictly stronger than the Cycle-17 single-coordinate bound because
overlap inside a pair is no longer double counted.  The converse is not
claimed.  Floating LP solutions propose weights only; every promoted result
requires an independently reconstructed integer inequality.
