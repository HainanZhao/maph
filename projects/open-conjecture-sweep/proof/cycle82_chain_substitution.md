# C82 exact certificate: one 15-element inverse chain substitution

## Statement

Let \(P\) be the poset whose nine base-block predecessor masks are
\((0,0,2,0,1,8,25,7,42)\).  Replace precisely base blocks \(0,1,3\) by
three-element chains, retain the six other blocks as singletons, and impose
every relation induced by the base masks.  Call the resulting poset \(P_{82}\).

`PROVED`: \(P_{82}\) has exactly 571,725 linear extensions.  Its strict
pair-majority digraph has no directed 4-cycle.  Consequently it cannot realize
a full LEM 4-cycle whose incomparable-only subdigraph has none.

This is a theorem only about the named substitution family.  It neither proves
nor refutes Gupta's LEM spectrum question, nor rules out another inverse
realization family.

## Exact routes and conventions

The primary route is the order-ideal prefix/suffix recurrence: each transition
from an ideal records every pair in which a prior vertex precedes the newly
adjoined vertex.  This counts each linear extension exactly once.  The frozen
checker returns the extension count and exhaustively tests all ordered
four-tuples of distinct vertices.

The independent route recursively deletes every currently minimal vertex and
explicitly visits each complete linear extension.  It accumulates all ordered
pair counts directly.  For the restricted graph it computes transitive closure
of the predecessor relation before declaring vertices incomparable.  Closure
adds three relations created inside the substituted chains.  The two routes
agree on the count and both find `full_has_4_cycle = false`; hence the primary
negative conclusion does not depend on the restricted-graph convention.

## Falsification

This certificate is refuted by either an incorrect extension count, or a
specific ordered four-tuple whose four strict pair-count inequalities form a
full directed cycle.  The direct replay is a separate algorithmic route for
both tests.
