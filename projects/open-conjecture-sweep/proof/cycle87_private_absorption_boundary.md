# C87 exact boundary: private-region absorption fails at the minimum order

`PROVED`: if six private regions at a root are nonempty and no two are
absorbed by a third-color block, the system has at least 12 points.  With two
singleton regions, their witnesses cannot share either own color and pair
coverage puts them in a third-color block; hence at most one region is a
singleton.

`PROVED`: the exact 12-point root-normalized SAT instance is satisfiable.
Its independent partition replay verifies pair coverage, private regions of
sizes \((1,2,2,2,2,2)\), and no absorbed pair.  The displayed system has a
three-component cover, so it is not a Ryser counterexample.

## Claim boundary

This refutes only C87's two-private-region absorption invariant.  It neither
refutes intersecting Ryser at \(r=6\) nor rules out a different global
partition invariant.
