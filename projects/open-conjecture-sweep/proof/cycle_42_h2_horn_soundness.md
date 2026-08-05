# Cycle 42 soundness boundary

## Headline

`PROVED`: among the 3,954 preregistered four-type interfaces obtained by
appending every complete type to the first, median, and last Cycle 41
nonzero-H1 type triples, 3,893 have nonzero rational second homology. The raw
interfaces reduce exactly to 409 structural complexes; rational and GF(2)
dimensions agree on every complex and range up to 40.

This is an ambient-topology theorem. It is not evidence that the Cycle 41
signed functional fails to extend. On the preregistered first nonzero
interface, types `(2,5,14,5)`, the deterministic Cycle 41 face moments form an
oriented rational two-cycle that is the boundary of one allowed tetrahedron.

## Exact interface

For an ordered four-type tuple, vertices are its rank-one-allowed owners.
Cross-part edges omit exactly the original rank-two blocked equal-owner
diagonals. Triangles have all three edges and omit exactly original rank-three
blocked equal-owner diagonals. Tetrahedra have all four faces. The standard
alternating simplicial boundary is used, and both routes verify
`boundary_squared = 0` exactly.

The selected interfaces contain no rank-three diagonal deletion. This is an
outcome of the frozen raw census, not an assumption. Repeated types denote
separate parts and occur within the frozen raw-type multiplicities.

## Exact routes

The primary route reconstructs the complete Cycle 41 small-boundary order,
enumerates relevant rank-three blocker tuples from raw patterns, deduplicates
by owner supports and all pair/face deletion masks, and performs lowest-pivot
GF(2) and rational sparse elimination.

The independent route starts from direct type/signature membership rather
than raw tuple enumeration, deduplicates in reverse order, and uses
highest-pivot elimination. It agrees on all 409 structural ranks,
multiplicities, aggregate simplex counts, and the 3,893/40 homology census.
All rational elimination coefficients have height one.

For `(2,5,14,5)`, exact rational ranks are `rank(d2)=11` and `rank(d3)=4`
on 16 triangles, so `dim H2=1`. A primitive eight-triangle cycle has a
two-entry dual cochain pairing `-1`, certifying it is not a boundary. This
canonical ambient class is distinct from the actual Cycle 41 moment cycle.

The moment route independently checks rank-one support, original and forced
pair support, singleton marginals, all four face fills, oriented cancellation,
and the final tetrahedral fill. Its four-term moment cycle equals the boundary
of tetrahedron column zero.

## Claim boundary

Cycle 42 does not classify all four-type interfaces, does not show that every
actual Cycle 41 moment cycle fills, does not construct a full degree-four
functional, and proves neither a leaf certificate nor LRC(13). Conversely,
the nonzero ambient homology must not be called a functional obstruction: the
only coupled moment class tested here is zero in homology.

The next discriminating question is the exact moment-class census across the
frozen 409 structural complexes / 3,954 raw selected interfaces. A nonzero
actual class obstructs this canonical Cycle 41 transport extension only; it
would not rule out another signed degree-four functional.
