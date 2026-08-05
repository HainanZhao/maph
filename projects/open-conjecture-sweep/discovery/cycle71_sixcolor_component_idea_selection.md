# C71 creative selection: six-color component covers

Target: every six-edge-coloring of a complete graph has a vertex cover by at
most five monochromatic connected components (the exact Gyárfás/Ryser
equivalent form).

Candidate A — component-incidence contraction.  Contract every maximal
monochromatic component into a colored incidence hypergraph, retain the
forbidden pattern “no five components cover”, and seek a forced dominated
component or a six-part transversal. Falsifier: a finite reduced incidence
pattern satisfying the contraction axioms without a dominated component.

Candidate B — color-deletion induction. Choose a largest color component,
delete it, and prove the residual coloring admits four components through a
forced palette reduction. Falsifier: an exact coloring whose every largest
component leaves all six colors essential in the residual.

Candidate C — finite obstruction construction. SAT-search small colorings
with no five-component cover, quotienting by vertex/color symmetry, to obtain
a genuine counterexample or a minimal obstruction pattern. Falsifier: a
verified coloring with the stated property; bounded UNSAT alone proves
nothing.

Question the questioning: B assumes “largest” is structurally meaningful and
can recreate the local-exchange trap. C risks a blind census. Choose A: it
keeps the exact global component geometry and supports both a proof reduction
and a small countermodel. C is retained solely as a falsifier generator for
the proposed contraction lemma.
