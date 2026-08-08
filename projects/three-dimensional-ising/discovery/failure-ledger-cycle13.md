# Cycle 13 failure ledger

## F1 — A longitudinal-layer schedule is not the canonical handle filtration

**False step.**  Assign each transverse edge to the first canonical
nonexact a-atom occurring on that layer, assign connector and gauge-only
edges by longitudinal layer, and treat the ordinary slice mask as the virtual
state at every spin-coordinate cut.

**Exact falsifier.**  Using the pinned atomic cochains, the resulting prefix
already has a nonzero period for the next b character.  For (n,w)=(6,3),
the failed right-character bits at successive early cuts are 1,3,5,7,9.
For (4,4), they begin with 1, then 3,5,7, and later 9.  The naive
schedule also produces interfaces of sizes 13 and 26, respectively, rather
than w^2=9,16.

**Cause.**  Exact transverse modes are coboundaries only after their vertex
potentials are transported through the co-core move.  Freezing an ordinary
longitudinal plane before that move leaves the gauge jump on the wrong side.
The canonical separator is a deformed slice through the co-core collar, not
an undeformed spatial layer.

**Consequence.**  The release replay must encode the actual four-point
co-core edge exchange (or an equivalent transported-tree gauge).  It cannot
be obtained by merely sorting physical edges by their nonexact atomic label.
This does not affect the global phase-telescoping proof.

