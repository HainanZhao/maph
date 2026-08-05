# C81 method boundary: LEM four-cycle spectrum

## Outcome and boundary

**PROVED.**  The full and incomparable-only LEM digraphs have equal directed
girth: bypassing a comparable edge of a shortest full cycle creates a shorter
full cycle, so no shortest cycle uses one.  See
`proof/cycle81_shortest_cycle_reduction.md`.  This is a direct formalization
of the source's bypass observation, not a novelty claim and not a proof of
equal cycle spectra.

**PROVED.**  Common-pivot XYZ positive correlations alone cannot prove the
length-four spectrum assertion.  The fixed 35-weight distribution checked by
`proof/check_cycle81_xyz_witness.py` is supported on rankings with \(0<1\),
satisfies every common-pivot XYZ inequality, has a full directed four-cycle,
and has no restricted directed four-cycle.  It is not claimed to be a uniform
linear-extension distribution, so it does not refute Gupta's Question 14.

**OBSERVED.**  The repaired frozen two-chain screen found 0, 1, and 3
unordered LEM triangles in its three 20,000-poset streams, respectively, and
no split mismatch.  Its ten-element outputs lie inside Gupta's exhaustive
order-14 agreement and are only regression evidence.

## C81 decision

Close C81.  The dominance and XYZ bridges are separately falsified as
sufficient, while the chain-split construction supplied no new mechanism.
Do not enlarge this sample or start a census.  The next cycle may instead
test an order-15-or-larger inverse modular realization, with exact generating
functions for pair margins fixed before construction.
