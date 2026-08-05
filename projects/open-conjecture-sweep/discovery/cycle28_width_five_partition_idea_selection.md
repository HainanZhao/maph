# Contingent Cycle-28 idea selection: change the width-five geometry

This scratch applies only if Cycle 27 seals its all-unresolved fixed-geometry
result.  It is the required pre-cycle idea selection, not a cycle record.

## Candidate questions

1. **Portfolio-capacity-selected width-five geometry.**  Starting from the
   fixed (5+4+4) partition, form the 13 cyclic coordinate relabellings.  For
   each target, score every partition by the sum of normalized exact direct
   capacities across a frozen small portfolio: the Cycle-22 base-4 leaf-952
   witness and the Cycle-21 base-4 leaves 83 and 104 plus base-3 leaf 94.
   Choose the lexicographically first minimum, then run the fresh time-weight
   LP only on that selected partition.  The selection is exact, finite, and
   deliberately permits a different geometry from Cycle 27.
2. **Exact rational primal lower-bound extraction.**  Convert Cycle 27 LP
   solutions to rational candidate lower bounds for the same partition.  This
   could diagnose numerical behavior but cannot by itself advance a survivor,
   because it leaves the fixed geometry unchanged.
3. **Semantic primal lift.**  Seek a theorem identifying the direct capacity
   model with the desired first-lift interface.  This could be powerful, but
   no equivalence has been proved and the first prototype already collapsed to
   the known mapping family.
4. **Further character refinement.**  Add individual/cyclotomic character
   coordinates to the CRT dual.  The eight- and twelve-class experiments were
   non-discriminating, so it has lower expected information gain than a true
   geometry change.

## Adversarial comparison and selection

Candidate 1 preserves the exact raw-time/direct-CNF interface and supplies a
specific falsifiable difference from Cycle 27: a target must select a
partition other than `0-1-2-3-4,5-6-7-8,9-10-11-12`, or the control family has
not changed anything material.  It also isolates the selection from the fresh
optimizer: the frozen portfolio chooses geometry before the fresh LP is
solved.  The portfolio answers the companion's strongest challenge to the
single Cycle-22 witness, whose direct transfer was nondeficit on all 60
targets in Cycle 26.  Candidate 2 is rejected as diagnostic only; Candidate 3
is rejected pending an equivalence theorem; Candidate 4 is rejected because
the previous class duals were non-discriminating.

The provisional choice is Candidate 1.  Its falsifier is any portfolio-source
recovery, cyclic-partition census, normalized-capacity score or tie-break,
target order, LP separation, or direct integer replay mismatch.  If all
selected partitions remain the Cycle-27 partition, the proposal is contained
rather than called a new engine; choose a genuinely heterogeneous family
before opening a cycle.
