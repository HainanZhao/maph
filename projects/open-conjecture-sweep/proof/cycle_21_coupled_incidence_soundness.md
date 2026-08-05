# Cycle 21: coupled CRT incidence and width-three deficiency certificates

## Exact row-fiber incidence

Fix coprime positive integers \(p,c\), put \(q=pc\), and fix a selected
speed \(s\).  For a time \(a\), use its CRT coordinates
\(\alpha=a\bmod p\) and \(\beta=a\bmod c\).  Define

\[
  x_p=(\alpha(s\bmod p))\bmod p,
  \qquad w=s\bmod c.
\]

By Cycle 20, this speed is bad at \((\alpha,\beta)\) exactly when

\[
  w\beta\equiv x_p\pmod c,
  \quad\text{or}\quad
  x_p\ne0\text{ and }w\beta\equiv x_p-p\pmod c.
\]

These are coupled relations: the same selected residue \(w\) occurs in every
row \(\alpha\).  When \(w\) is not a unit modulo \(c\), either relation may
have zero or several solutions in \(\beta\); it must not be replaced by a
permutation graph.  Since CRT is a bijection between times and
\((\alpha,\beta)\), the row-fiber incidence is exactly the direct time mask.

## Width-three block inequality

Fix one canonical gcd-witness leaf and partition the coordinates into blocks
of size at most three.  An allowed block option chooses one leaf-admissible
digit at every coordinate in the block.  Let \(b_{B,o,t}\) be one exactly
when at least one selected coordinate in block \(B\) is bad at time \(t\),
computed from the coupled incidence above.

For nonnegative integer time weights \(w_t\), put

\[
  W=\sum_t w_t,
  \qquad
  U_{\mathcal P}=\sum_{B\in\mathcal P}
    \max_{o\text{ allowed in }B}\sum_t w_t b_{B,o,t}.
\]

Any global digit selection that covers every time induces one option in each
block.  Counting the covered weight, with overlap within a block counted only
once, gives \(W\le U_{\mathcal P}\).  Therefore an independently replayed
integer witness with \(U_{\mathcal P}<W\) proves that the named leaf has no
improper lift.  Blocks of size three strictly extend the frozen Cycle-18
formula family, although failure to find a deficit is not a no-go theorem.

## Direct certificate transfer

The inequality does not require weights or a partition to have been optimized
for the leaf being certified.  A weight vector obtained from one leaf may be
applied to any other leaf, and any coordinate permutation of its blocks is
another valid partition.  The target leaf is excluded only if its own allowed
digits and direct time masks give a freshly enumerated strict inequality
\(U_{\mathcal P}<W\).  Similarity of ordinals, clauses, or gcd patterns is
not evidence.

## Claim boundary

`PROVED`: the coupled row-fiber formula is equivalent to the direct bad-time
mask, and every exact strict width-three deficit excludes its named canonical
leaf.  Floating LP solutions and failed searches prove nothing.  A leaf
certificate does not by itself close a base, \(F_1\), \(J\), or LRC(13).
