# Cycle 50 idea selection: actual deleted-diagonal packets

## Evidence that fixes the question

- `PROVED` Cycle 49: the frozen pairwise-distinct relative packet formula
  closes 382,453,314 of 382,453,319 raw-valid unordered p199 type triples.
  Its five remaining labels have only two structural support patterns:
  `(2,2,2)` and `(2,2,4)`.
- `PROVED` Cycle 49: the first `(2,2,2)` exception `(4,4,5)` has a
  one-dimensional cube kernel.  Its unique full-support cube uses alternatives
  `(10,10,12)`, so two alternatives coincide, yet every resulting nonzero
  cell is allowed by the *actual* deletion masks and the defect vanishes.
- `PROVED`: pairwise-distinct alternatives are sufficient for no spill but not
  necessary.  A direct use of unrestricted Gaussian elimination would only
  recover ordinary local boundary membership and is prohibited.

## Serious candidates and their decision questions

### A. Deletion-aware triple-packet theorem

Permit repeated alternate owners only after every vertex of the selected cube
is checked against the actual pair and triple deletion masks.  A cube may meet
other forbidden vertices only when its uniquely scaled packet discharges
*every* such vertex simultaneously; it may leave neither a new nor residual
forbidden coefficient.  For each active exception, select the lexicographically
least cube with that actual-mask discharge property.

- Preserves: all three pair marginals, the cube-kernel mechanism, and an
  explicit formula independent of a linear solver.
- Falsifier: a forbidden cube spill, unchanged nonzero forbidden terminal,
  any failed `(2,2,2)`/`(2,2,4)` interface, or a new residual pattern.
- Cost/information: low.  It either supplies a real pattern theorem correcting
  the overstrong surrogate or proves the natural relaxation insufficient.

### B. Solve each exceptional restriction by exact elimination

Compute the cube-kernel image on each exceptional interface and choose a
solution basis-by-basis.

- Falsifier: a nonzero dual class.
- Cost/information: low but rejected: it is a per-face solver and therefore
  cannot establish the desired natural packet rule.

### C. Pause immediately after the C49 boundary

Treat five exceptions as saturation and hand off Problem 1.

- Falsifier: a single uniform deletion-aware packet rule covering both
  patterns.
- Cost/information: low, but premature because C49 supplied exactly such a
  local mechanism on its first exception.

### D. Search for a global lift map before local closure

Try to define a degree-four or arithmetic lift from the affine face data.

- Falsifier: representative dependence or lack of a necessary direct-cover
  interface.
- Cost/information: high and rejected because no coherent lift object exists
  yet; it would evade the active local clarity signal.

## Question the questioning

Why is a deletion-aware rule not simply five post hoc repairs?  It is a
theorem candidate only if one uniform admissibility predicate is frozen before
the other four labels are inspected, and if the complete full-domain census of
the two structural patterns has no additional residue.  Enumerating cubes is
legitimate only as verification of that declared formula, never as an
outcome-selected solver.

Why must every cube vertex be checked rather than only its pivot?  The move is
a signed tensor identity.  A forbidden companion is allowed only when the
same uniquely scaled packet makes its post-packet coefficient exactly zero;
otherwise it is a real spill.  Thus each packet boundary, rather than every
formal cube vertex, has allowed support.

Why not retain pairwise distinction for the pair-fiber stage?  C49's first
failure occurs at the triple packet and shows the exact logical defect there.
Changing other packet stages before this theorem is tested would confound the
falsifier.

## Choice

Choose A.  Freeze a lexicographic deletion-aware *triple* packet selector and
leave the C49 pair-fiber rule unchanged.  Prove the cube-marginal identity and
the actual-mask support criterion, then apply the selector to every
full-domain `(2,2,2)` and `(2,2,4)` interface selected without outcome data.
If one interface fails or any new residual pattern appears, do not add a
second rule: pause and hand off Problem 1.
