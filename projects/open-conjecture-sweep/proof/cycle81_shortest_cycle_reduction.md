# Shortest-cycle reduction for C81

## Claim boundary

**PROVED.**  Every simple directed \(k\)-cycle of the full
linear-extension-majority digraph \(D(P)\) contains, after repeatedly
shortening comparable edges, a simple directed cycle of
\(D_{\mathrm{inc}}(P)\) of length at most \(k\). Consequently the directed
girths of \(D(P)\) and \(D_{\mathrm{inc}}(P)\) agree, with both infinite
when the corresponding digraph is acyclic. This does **not** prove that the
two digraphs have the same cycle spectrum, which is Gupta's Question 14.

## Proof

Let \(C=(v_0,\ldots,v_{r-1})\) be a shortest simple directed cycle in
\(D(P)\).  Assume, for contradiction, that one of its edges is a comparable
pair; rotate the indices so that \(v_1<v_2\) in \(P\).  Every linear
extension with \(v_0\) before \(v_1\) also has \(v_0\) before \(v_2\).
Consequently

\[
 \Pr[v_0\prec v_2]\geq\Pr[v_0\prec v_1]>\tfrac12,
\]

so \(v_0\to v_2\) is an edge of \(D(P)\).  For \(r\geq4\), replacing
\(v_0\to v_1\to v_2\) by \(v_0\to v_2\) makes a shorter simple directed
cycle, a contradiction.  For \(r=3\), it gives both \(v_0\to v_2\) and the
cycle edge \(v_2\to v_0\), impossible because a strict majority relation is
asymmetric. Thus every edge of \(C\) joins incomparable elements and lies in
\(D_{\mathrm{inc}}(P)\). Applied without the minimality assumption, the same
bypass operation can be repeated until no comparable edge remains, proving
the first assertion with a final length at most the initial \(k\).

Since \(D_{\mathrm{inc}}(P)\) is a subdigraph of \(D(P)\), its directed
girth cannot be smaller.  The preceding paragraph supplies a directed cycle
of the full girth in the subdigraph, so the two girths are equal.

## Relation to the source

Gupta, *Balance Constants, Majority Cycles, and the Gold Partition
Conjecture through Fourteen Elements*, arXiv:2607.23926v2, lines 184--192,
states the same monotone bypass and notes that it shortens a \(k\)-cycle to a
\((k-1)\)-cycle.  The scoped girth corollary above is a direct formalization
of that observation, not a novelty claim.
