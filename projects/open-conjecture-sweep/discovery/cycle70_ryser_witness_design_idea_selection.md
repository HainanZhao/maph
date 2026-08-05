# C70 creative selection: deletion-witness incidence design

Candidate A — six-part Hall deficiency.  For each edge \(e\) of a hypothetical
edge-minimal \(\tau\ge6\) system, choose a five-cover \(C_e\) of \(H-e\),
necessarily disjoint from \(e\).  Build the bipartite incidence relation
between the six vertices of \(e\) and the five cover positions across all
witnesses. Seek a Hall deficiency forced by intersection and part labels.
Falsifier: an exact abstract labelled witness design meeting every derived
constraint but with no deficient subset.

Candidate B — pair-of-edges double count.  Count intersections of witness
essential-edge families with ordered pairs \((e,f)\), retaining which part
realizes each intersection. Seek an upper bound below the mandatory
intersecting-pair count. Falsifier: the known equality construction or a
synthetic labelled incidence design saturating the inequality.

Candidate C — SAT realizability first. Encode the deletion-witness axioms for
a small edge count and seek an abstract model before designing an inequality.
Falsifier: a model which realizes as an actual six-partite hypergraph with
\(\tau\ge6\), in which case Ryser is refuted; a capped UNSAT result alone is
not a theorem.

Question the questioning: A risks silently depending on an arbitrary witness
choice; B risks losing the cover information; C risks another census.  Choose
A only in its witness-choice-invariant form: derive an inequality valid for
every five-cover of every deletion, and use C solely as a small falsifier
generator.  B is rejected initially because its pair count is already largely
absorbed by the published non-linear equality construction.
