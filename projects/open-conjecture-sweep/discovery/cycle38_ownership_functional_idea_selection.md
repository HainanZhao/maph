# Cycle 38 idea selection: ownership-aware functional

## Candidate engines

1. **Rooted ownership pushforwards.** Push the Cycle 37 signed product measure
   through a total deterministic ownership map: choose a root coordinate,
   assign each covered time to the first covering coordinate in the rooted
   cyclic order, and assign uncovered times to the root. Totality and
   exclusivity then hold pointwise. A blocker away from the root also vanishes
   pointwise, so only the root's exact rank-one, rank-two, and rank-three
   blocker moments need evaluation. Test all thirteen roots and their linear
   span, preserving every time and coordinate label.
2. **Continue the polynomial-degree ladder.** Search for a product functional
   annihilating degree-three direct-predicate multiples.
3. **Generic blocker hypergraph coloring.** Ignore ownership labels and seek a
   coloring obstruction in the rank-at-most-three blocker hypergraph.
4. **Full ownership Nullstellensatz/SAT.** Encode all ownership variables and
   ask a general proof engine for a certificate.

## Question the questions

The tempting question is whether one more direct degree vanishes. That asks
the old calculus to repeat its previous success and does not approach the
missing ownership semantics. It is rejected.

Generic coloring is also rejected: Cycle 6 already showed that a necessary
hypergraph condition can be strong yet fail to preserve the lift. The Cycle
29 theorem says the coordinate labels and asymmetric blocker cells are the
semantic content, so quotienting them away asks a misleading easier question.

A full proof search is premature. It could emit another large certificate
without revealing whether the compact Cycle 37 obstruction survives the
ownership interface. The smallest discriminating test is the rooted
pushforward family. It turns the absent interface into an explicit
construction, preserves total ownership exactly, and makes its failure
diagnostic: the first nonzero labeled blocker moment identifies the first
relation that the direct functional cannot absorb.

The main risk is confusing a convenient deterministic ownership map with the
entire ownership dual space. Therefore failure rejects only the thirteen
rooted pushforwards and their linear span. Success proves only annihilation of
the unmultiplied ownership/blocker generators under that pushforward; it is
not a leaf certificate or a full ideal-functional obstruction.

## Choice and falsifier

Choose rooted ownership pushforwards. Compress concrete blocker enumeration
only by the complete global coverage type of each time, with exact
multiplicity; the local signature quotient alone is insufficient because
other coordinates distinguish times.

The branch is falsified by any mismatch between a compressed moment and a
direct concrete evaluation, any failure of pointwise totality/exclusivity or
off-root blocker vanishing, or any dropped rank, coordinate, signature
pattern, global type, or time multiplicity.
