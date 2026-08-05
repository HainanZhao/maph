# Cycle 19: exact symbolic coverage antichains

Fix a canonical leaf.  For each coordinate (i) and allowed digit (d), let
(B_{i,d}) be the set of denominator times covered by that selected lift.
For a coordinate set (S), let

\[
  \mathcal U_S=\left\{\bigcup_{i\in S}B_{i,d_i}:d_i\text{ allowed}\right\}.
\]

If (A\subseteq A'), then every completion that covers all times with (A)
also covers all times with (A').  Hence replacing any finite family of masks
by its inclusion-maximal antichain preserves the existence of a full-covering
completion.  Applying this replacement after each coordinate is therefore an
exact symbolic branch merge, not a heuristic prune.

Split the coordinates into (L=\{0,\ldots,6\}) and
(R=\{7,\ldots,12\}).  A full lift covers every time exactly when there are
(A\in\mathcal U_L) and (D\in\mathcal U_R) with (A\cup D=T), where (T)
is the full time set.  The same statement holds after replacing each family
by its maximal antichain.  Thus a complete construction of both antichains,
followed by an exact failure of every full-cover query, proves that the leaf
has no improper lift.  A capped frontier or incomplete query proves nothing
about that leaf.
