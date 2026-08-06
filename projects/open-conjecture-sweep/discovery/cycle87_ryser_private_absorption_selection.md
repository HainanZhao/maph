# C87 selection: private-region absorption in six pair-covering partitions

## Creative comparison

`CONJECTURED` candidates were an OR-entropy transport for Frankl, insertion
slot covariance for the 1/3--2/3 conjecture, a transfer operator for the
Möbius ladder, and a component-partition invariant for intersecting Ryser at
\(r=6\).  The first lacks a valid tensorization direction; the second risks
reopening C83's fiber vocabulary; the third risks repackaging C85.  The
selected invariant acts directly on the six pair-covering equivalence
relations and supplies an explicit five-component cover if true.

## Question the target

For a root \(v\), let \(B_i(v)\) be its block in partition \(\Pi_i\), and
\[
 U_i(v)=B_i(v)\setminus\bigcup_{j\ne i}B_j(v).
\]
If all six private regions are nonempty, C87 asks whether two regions are
contained in one component of a third color.  Such a component, together
with the four root blocks of the other colors, is a five-component cover.

## Question the critique

Singleton private witnesses automatically share a third-color component, but
nothing yet forces entire private regions into it.  The invariant can fail
without furnishing a Ryser counterexample.  The first gate therefore seeks
an exact partition countermodel, not a broad coloring census.

## Oracle selection and first lower bound

Oracle selected this global partition invariant.  `PROVED` by the elementary
pair-cover argument: if \(|U_i(v)|=|U_j(v)|=1\), their two witnesses cannot
share colors \(i\) or \(j\), so pair coverage puts them together in a third
block.  Thus no-absorption with six nonempty private regions has at most one
singleton private region, hence at least \(1+1+5\cdot2=12\) points including
the root.  C87 first checks this lower bound independently, then searches
the exact 12-point, root-normalized partition interface.

The falsifier is one exact 12-point pair-covering six-partition system with
all root private regions nonempty and no absorbed pair.  It rejects only the
private-region invariant.  A failure to find one under the frozen exhaustive
interface is not a theorem; no larger search follows without a direct
transitivity proof.
