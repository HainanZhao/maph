# Cycle 15 preregistration: paired-cycle width-extension probe

Date: 2026-08-08  
Budget ordinal: B15

## Decision question

Does the sparse width-three paired-cycle witness reveal an explicit
width-parametric tree-and-chord family whose left and right homology
projections both have rank `w^2-1`?

## Questioning the question and exclusion map

- Former question: arbitrary-width generic tightness.
- Outcome: already `PROVED` by the normal/opposite encoder and buffer route.
- Delta: this probe seeks only a shorter, encoder-independent lower-bound
  proof.  Failure cannot weaken G1.
- The eight width-three chords are all longitudinal, but occur at irregular
  layers and transverse positions.  Visual resemblance is not an invariant;
  the verifier is simultaneous left/right rank at width four.
- A materially different mechanism would be to search arbitrary cycle
  subspaces without a common fundamental tree.  That route is excluded from
  this short probe because it would not generalize the frozen certificate's
  stated mechanism.

## Frozen method and resource bound

1. Decode the eight edge indices into `(layer,y,z,direction)`.
2. Preserve the old `3 x 3` tree/chord core inside width four.
3. Add the seven new boundary sites using an L-boundary component tree with
   longitudinal rails, as implemented in
   `discovery/search_g1_width4_l_attachment.py`.
4. Run exactly 50,000 deterministic trials with seed 20260808.
5. Stop immediately if total simultaneous rank 15 is reached; otherwise stop
   after the fixed trials.  No wider search or new tree family is authorized
   in this cycle.

## Acceptance

An explicit width-four tree with 15 selected chords and both projected
`GF(2)` ranks 15.  The resulting Walsh determinant consequence must then be
replayed over primes 1,000,000,007 and 1,000,000,009 before promotion.

## Terminal negative

If no rank-15 witness occurs, record the best exact rank and the sampled
family/seed.  Classify only this structured extension probe as negative and
drop T5.  Do not infer that no parametric paired-cycle family exists.

## Falsifier

Loss of either old rank-eight projected core under embedding invalidates the
extension implementation.  A best score below 15 is not a mathematical
no-go; it is the preregistered timebox outcome.
