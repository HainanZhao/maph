# C72 side-shape reduction

`PROVED.`  For the generalized rooted equality cores in the C72 model, the
existence of a core-vertex blocker of size at most five is invariant under
permuting the five witness lines and independently permuting the five
noncentral parts.  Consequently, it is enough to test one repeated-vertex
side restricted-growth string for each multiset of side-block sizes.

Indeed, a witness permutation carries its central equivalence relation, pair
of star indices, and map to the correspondingly relabelled data.  A
noncentral-part permutation carries side labels and map values.  These
operations preserve the six star lines, the five witness lines, incidences,
and the condition that an extension meets every core line exactly once.  They
therefore induce a vertex-labelled isomorphism between both the core-line
families and their full compatible-trace families.  A blocker and its size
are preserved in both directions.  Canonicalizing the transported side and
central partitions back to restricted-growth strings changes only block
names, and the C72 enumeration ranges over every central restricted-growth
string, every five-tuple of star pairs, and every compatible map tuple.

The feasibility census leaves exactly the side shapes
`[1,1,1,1,1]`, `[2,1,1,1]`, and `[2,2,1]`.  Representatives in the frozen
enumeration order are respectively side filters 51 (`[0,1,2,3,4]`), 14
(`[0,0,1,2,3]`), and 10 (`[0,0,1,1,2]`).

Claim boundary: this reduces only the finite generalized C71 equality-core
model.  It does not establish that the model captures a hypothetical Ryser
counterexample; that implication is the separate universal-blocker
reduction.
