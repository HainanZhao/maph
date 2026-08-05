# Cycle 42 idea selection: four-partite horn filling

## Brainstorm

1. Lift Cycle 41's tripartite chain filling to a four-partite complex and
   test exact second homology before attempting a general recursion theorem.
2. Assemble the entire degree-four rational moment system immediately.
3. Search for another local ownership selector or a larger routing span.
4. Stop Problem 1 and preserve the remaining portfolio allocation.

## Decision questions

- For 1: after the actual rank-one, rank-two, and rank-three deletions, does a
  compatible oriented boundary of four triple moments always bound an allowed
  rational four-way tensor on the smallest discriminating interfaces?
- For 2: would a large solve distinguish a new obstruction from a quotient or
  implementation failure, and what structure would explain either answer?
- For 3: what information could another selector expose that the existing
  nonlocal signed moment construction does not already contain?
- For 4: has the new chain-filling mechanism actually reached a falsifiable
  higher-dimensional test, or would stopping now discard the best current
  information gain?

## Questioning the questioning

“Continue to degree four” is the wrong framing: a formal degree ladder would
only enlarge the same linear system. Cycle 41 instead exposed a topological
mechanism—allowed triple cells fill compatible edge data—but also exposed the
precise danger to recursion: pair intersections can have nonzero first
homology. The discriminating question is therefore whether those classes
survive as second-homology obstructions in an actual four-partite interface.

The full degree-four system is rejected because it would hide that mechanism
inside a large elimination and make a cap nearly uninterpretable. More routing
is rejected because the signed construction is already strictly broader.
Stopping is premature until the smallest exact higher-dimensional prototype
has either filled or produced a checkable nonboundary cycle.

## Choice and falsifier

Choose an exact four-partite horn-filling prototype. Reconstruct Cycle 41's
nonzero-H1 interface order, freeze its first, median, and last type triples as
anchors, append every complete type, and build the actual oriented chain
complex with rank-one vertex, rank-two edge, and rank-three face deletions.
Compute rational H2 exactly. If H2 is nonzero, extract the first canonical
integer 2-cycle and independently certify that it is not a boundary; then ask
whether the compatible Cycle 41 face moments pair nontrivially with that
class. If H2 vanishes throughout, record only the bounded prototype theorem
and seek the invariant that could make it general.

Falsifier: any disagreement in the reconstructed anchor order, deletion
semantics, boundary signs, the identity boundary-squared equals zero, rational
rank, extracted cycle, nonboundary pairing, or independent replay invalidates
the affected conclusion.
