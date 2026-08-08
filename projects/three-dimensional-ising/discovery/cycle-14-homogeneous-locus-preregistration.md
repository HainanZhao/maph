# Cycle 14 preregistration: homogeneous width-three locus

Date: 2026-08-08  
Budget ordinal: B14

## Decision question

Does the exact `256 x 256` paired-cycle minor frozen in Cycle 8 remain a
nonzero polynomial after restricting the `G_(10,3)` edge variables first to
the homogeneous anisotropic ring `Z[t_x,t_y,t_z]` and then to the isotropic
ring `Z[t]`?

## Questioning the question

The existing rank table already reports full width-three rank at the single
anisotropic point `(2,3,5)` and isotropic point `2`, but it used a
rank-revealing minor selected after specialization.  That does not prove that
the previously frozen paired-cycle minor survives either restriction.  This
cycle therefore fixes the Cycle 8 row and column sets before seeing the new
determinants and does not substitute a different minor.

## Exclusion map

- Former question: generic tightness for independent nonuniform weights.
- Outcome: `PROVED` for every width by the arbitrary-width encoder theorem;
  the width-three paired-cycle specialization is an independent sparse
  witness.
- Falsifier already banked: the sparse specialization uses zero and
  independently variable edge weights, so it gives no homogeneous result.
- Claim-boundary delta: only the width-three restriction of the same frozen
  determinant is at issue.  No arbitrary-width or fixed-temperature claim is
  licensed.

## Frozen objects and conventions

- Graph: `G_(10,3)=P_10 square P_3 square P_3`, with `P_k` having `k`
  vertices and the edge order from `src/conventions.py::cubic_box`.
- Embedding and canonical coordinates: the universal checkerboard embedding
  and atomic basis used by the Cycle 8 verifier.
- Cut: after five canonical handle pairs (`shift=10`).
- Rows and columns: exactly the paired-cycle character sets derived from the
  frozen tree, chords, and selected dual coordinates in
  `proof/verify_g1_paired_cycle_w3.py`.
- Primes: `1,000,000,007` and `1,000,000,009`.
- Anisotropic points, fixed in advance: `(2,3,5)`, `(7,11,13)`, and
  `(17,19,23)`.
- Isotropic points, fixed in advance: `t=2,3,5`.
- Arithmetic: exact modular spin-slice character transfer, exact Walsh and
  canonical coordinate transformations, then deterministic modular
  elimination of the frozen minor.

## Input state, map, and smallest verifier

The input is the frozen Cycle 8 paired-cycle row/column index set.  The map is
restriction of every edge weight by its lattice axis, followed by restriction
to the diagonal `t_x=t_y=t_z`.  The smallest direct verifier computes the
pre-Arf tensor at each frozen point and eliminates only the selected
`256 x 256` matrix.

## Acceptance

- Anisotropic branch A: at least one nonzero determinant modulo either prime;
  the same points are nevertheless replayed over both primes.  This proves the
  trivariate integer determinant is not identically zero.
- Isotropic branch A: at least one nonzero determinant modulo either prime;
  both-prime replay is required for promotion.  This proves the univariate
  determinant is nonzero and its physical exceptional set is finite.
- Branch B: if every fixed point vanishes, run exact interpolation or symbolic
  elimination before deciding that a restriction is identically zero.

## Kill and escalation criteria

- A mismatch in the canonical tensor hash or full-rank profile at the already
  certified controls `(2,3,5)` or `t=2` kills the implementation, not the
  theorem.  Vanishing of this preselected minor alone is not such a mismatch,
  because an independently selected minor may still be full rank.
- If the frozen paired-cycle determinant vanishes while another minor is full
  rank, report this as failure of that witness; do not replace its rows after
  seeing the result.  A separately preregistered rank-revealing restriction
  may then address locus-wide tightness.
- Vanishing at all six fixed points is not proof of an identity and triggers
  the symbolic/interpolation branch.

## Resource stop

Compile one parameterized transfer executable per prime.  Stop the cheap gate
after the six fixed specializations.  Do not begin an arbitrary-width
homogeneous encoder calculation in this cycle.
