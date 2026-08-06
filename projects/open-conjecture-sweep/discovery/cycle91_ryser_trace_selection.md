# C91 selection: deletion-cover trace rigidity

## Oracle packet and decision

`CONJECTURED` question: can edge-minimality in an intersecting six-partite
six-uniform τ=6 counterexample force its size-four deletion covers to form a
coordinate-compatible family?  The first gate is deliberately one rank lower:
the published 13-edge, six-partite, intersecting τ=5 equality control of
Abu-Khazneh--Pokrovskiy.

Oracle's first adversarial question was whether edge-minimality supplies a
coherent *integral family of covers*, rather than another fractional matching
reduction.  Its second was whether the sharp τ=5 control is too weak to
inform a hypothetical τ=6 core.  It is too weak for transfer evidence, but
is a sharp, cheap falsifier for a frozen gluing mechanism.  The selected gate
therefore does not tune an axiom to the control and cannot support a larger
census.

For every labelled edge \(e\), let \(\mathcal C_e\) be all four-vertex covers
of \(H-e\).  Edge-minimality and \(\tau(H)=5\) imply every member of
\(\mathcal C_e\) is disjoint from \(e\).  For \(C\in\mathcal C_e\) and
\(f\ne e\), define its trace
\[
 T_C(f)=\{i\in\{1,\ldots,6\}: C\cap f\text{ contains the part-}i
 \text{ vertex of }f\}.
\]
The frozen deletion-cover trace CSP asks for one \(C_e\in\mathcal C_e\) for
each edge such that every unordered pair \(\{e,f\}\) has a reciprocal shared
coordinate,
\[
 T_{C_e}(f)\cap T_{C_f}(e)\ne\varnothing.
\]
This is a proposed integral compatibility axiom based only on deleted-edge
minimality and the fixed six-partite coordinate system; it is **not** claimed
to follow from those hypotheses.

`PROVED` source scope: Abu-Khazneh--Pokrovskiy gives the labelled 13-edge
control and its \(\tau=5\) equality status.  Aharoni--Barat--Wanless prove a
fractional matching-reduction statement; this CSP contains neither a matching
nor a fractional cover and does not assert their integral strengthening.

## Alternatives and stop rule

The two-cut poset injection was rejected because it restates Peczarski's Gold
certificate inequality.  Frankl irreducible deletion was rejected because it
repeats Bouchard's lattice framework.  LRC has no source-defined exact bridge.

The falsifier is an exact UNSAT result for the frozen CSP on the source-verified
control; a cover-family disagreement or bad transcription also falsifies the
computation.  If SAT, C91 may spend one short proof cap only on an abstract
integral reduction using these same axioms.  If no such lemma is obtained, it
records the finite control and pivots.  There is no second control, altered
compatibility rule, Ryser census, private-region absorption, or fractional-drop
repair in C91.
