# Cycle 44 idea selection: stratified non-anchor coupling holdout

## Brainstorm

1. Challenge the Cycle 43 anchor bias with a deterministic stratified
   non-anchor holdout and test both exact filling and explicit cone identities.
2. Promote the observed seven-term cones directly to a universal contraction
   theorem.
3. Enter the full rank-three-literal ideal layer using the three-anchor lift.
4. Stop Problem 1 and bank the remaining allocation.

## Decision questions

- For 1: after stratifying independently of coupling outcomes, does any actual
  canonical moment cycle represent nonzero H2, and how often is a fill the
  literal cone over an opposite face?
- For 2: which support/deletion hypotheses make the proposed cone or acyclic
  matching well-defined, and have any non-anchor cases tested them?
- For 3: does the selected family span the labeled multiplier layer, or would
  the computation silently omit most constraints?
- For 4: is there still a bounded exact counterexample route with higher
  information value than moving to the next portfolio problem?

## Questioning the questioning

Cycle 43's all-fill outcome is unusually clean, but every interface contains
one of three triples chosen precisely because Cycle 41 found nonzero H1 there.
The anchor may supply a universal cone vertex. The most dangerous question is
therefore not “can we prove the cone theorem?” but “does filling persist after
the anchor is removed?” A theorem synthesized before that holdout could merely
formalize selection bias.

Ambient H2 alone is again insufficient, so the holdout must be stratified on
topology and deletion geometry but evaluated on actual moments. The candidate
pool and strata must be frozen without inspecting fill outcomes. Repeated-type
families need explicit injection because a hash sample almost never repeats a
type. Direct ideal-layer work is rejected until a coverage/span theorem exists.

## Choice and falsifier

Choose a hash-generated plus deterministically constructed candidate pool,
exclude all three anchor triples, preselect by support/deletion/density/repeat
strata, refine by exact ambient-H2 bins, and retain at most 2,000 hash-minimal
interfaces. Build one shared canonical face tensor per sampled face and test
every exact moment cycle. Independently label a fill cone-explained only when
the explicit cone over one opposite face reproduces the full oriented cycle.

Falsifier: selection depending on a coupling outcome, accidental anchor
retention, a missing stratum representative, inconsistent shared faces,
invalid fill or cone identity, nonzero dual pairing reported as a fill, or an
independent replay mismatch.
