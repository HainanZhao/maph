# C87 source and convention audit: six component partitions

`PROVED` from the project-local C71 encoding: a six-color complete-graph
component system is represented by six equivalence partitions of the edge
set; every pair of points lies together in at least one partition block.
Choosing blocks is the exact component-cover semantics, with repeated colors
allowed.  See `proof/cycle71_component_cover_semantics.py` and
`proof/cycle71_partition_control.py`.

`PROVED` from the published 13-edge \(r=6\) equality control as replayed in
`discovery/cycle69_r6_extremal_control.py`: its induced six partitions are
pair-covering and have a five-block cover.  It is a convention control, not
a counterexample or a general Ryser theorem.

`CONJECTURED`: the private-region absorption invariant is not a consequence
of the cited partition semantics or C72's D=5 blocker theorem.  C87 tests it
as a new global mechanism.
