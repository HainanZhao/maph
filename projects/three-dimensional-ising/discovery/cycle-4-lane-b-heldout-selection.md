# Cycle 4 selection — held-out symmetry-compatible growing-size test

## Former question and exclusion-map delta

- **Former question:** does any physical symplectic basis compress the
  genus-three `4 x 3 x 3` spin-structure tensor?
- **Outcome:** sealed Cycle 3 artifact
  `cycle-3-b3-lane-b-rank-seven-v1` gives an exact positive answer: generic TT
  profile `(2,4,7,4,2)`, derived from the `y <-> z` graph automorphism.
- **Delta:** the physical intersection-form bridge is closed. Repeating more
  bases or rational values on the same graph cannot establish a growing-size
  law. The unresolved invariant is compatibility of the automorphism with a
  minimum-genus cellular embedding as the long box direction grows.

## Question → question the questioning → brainstorm

**Question.** Does the symmetry-derived rank reduction survive on the held-out
free `5 x 3 x 3` cubic box, with an independently certified minimum-genus
embedding and exact sector tensor?

**Question the questioning.** A second rank-seven observation would still not
be an asymptotic theorem. The decisive information is whether the same graph
involution acts on the facial-boundary quotient of a minimum-genus embedding
and forces an exact flattening relation. Therefore the embedding symmetry and
the induced homology action must be tested before rank fitting.

**Materially different mechanisms considered.**

1. **Selected: symmetry-compatible `5 x 3 x 3` extension.** Preserve the
   transverse `y <-> z` involution and extend the long direction. This is the
   smallest held-out graph that tests the prospective size recurrence without
   changing the symmetry type.
2. **Alternative: `4 x 4 x 3` transverse-swap test.** This tests a different
   involution and may reveal greater genus/rank growth, but it changes two
   structural variables at once and is therefore deferred.
3. **Alternative: abstract involution theorem without new data.** Prove that
   an involution whose dual action restricts to a translation on an affine
   half-coset forces a TT row equality. This lemma is useful and will be
   derived inside the cycle, but without a held-out embedding it would not
   meet Gate 3.

## Frozen experimental contract

- **Input state:** sealed Cycle 3 physical intersection and rank-seven
  artifact; free `5 x 3 x 3` graph; involution `(x,y,z)->(x,z,y)`.
- **Invariant/map:** minimum orientable genus, facial-boundary space under the
  involution, induced symplectic homology action, exact `W_h`, physical
  quadratic refinements, and minimum TT profile over a rigorously specified
  symplectic search.
- **Smallest direct verifier:** an exact cellular rotation system attaining a
  proved lower bound, followed by equality of the two labeled intersection
  routes and a coefficientwise symmetry-derived flattening relation.
- **Resource stop:** never enumerate the `2^52` cycle space. Before sector
  computation, benchmark the frontier engine and stop above 2,000,000 live
  states, 8 GiB resident memory, or 30 minutes. Do not run an Sp group larger
  than the measured genus permits without an orbit/flag reduction.
- **Advance condition:** a minimum-genus embedding preserved at the quotient
  level by `y <-> z`, plus an exact held-out rank reduction and a stated
  recurrence candidate linking `4 x 3 x 3` to `5 x 3 x 3`.
- **Falsifier:** no minimum-genus embedding in the exact searched rotation
  family supports the involution, or the induced physical tensor has maximal
  rank at every rigorously exhausted symmetry-aligned cut.

## Claim boundary

Cycle 4 tests one held-out size and one symmetry family. Success would satisfy
the finite held-out part of Gate 3, not Gate 4 or a thermodynamic claim.

## Live decision update

- `CERTIFIED_NUMERICAL`: the independent minimum-genus-four embedding has 76
  exact `F(lambda)` polynomials, exactly its 76 coordinate-symmetry orbits.
  The direct Cycle 3 basis extension has maximal generic profile
  `(2,4,8,16,8,4,2)`; its old row identity is falsified.
- The materially different recursive-rotation repair was then tested rather
  than fitting another basis.  `CERTIFIED_NUMERICAL`: a compatible genus-four
  rotation exists, but its old facial-boundary image has a one-dimensional
  defect.  The defect yields the exact relative-sector identity in
  `cycle-4-relative-theta-bridge.md`; all changed labels lie in a three-bit
  adapted window.
- The growing-size decision remains live.  Its next direct falsifier is the
  compatible `5 x 3 x 3 -> 6 x 3 x 3` step, not a larger random symplectic
  basis census.

## Final decision update

- `PROVED`: Millichap--Salinas Theorem 4 applies exactly and gives minimum
  genus `L-1` for every free `L x 3 x 3` box.
- `CERTIFIED_NUMERICAL`: the `5->6` step repeats the one-dimensional defect,
  orthogonal new symplectic pair, and three-bit active label window.  The
  exact refined sector polynomials reunite coefficientwise with no increase
  in peak frontier-state count.
- `PROVED`: the two local rotation/label templates alternate, producing a
  minimum-genus family for every `L>=4`.  Its complete Walsh tensor and the
  locally equivalent `F(q)` tensor have uniform handle-site TT-rank upper
  bound `1024`, and uniform binary-site TT-rank upper bound `2048`.
- Gate decision: **SURVIVES** with exact recursive closure and bounded
  collective auxiliary rank for the fixed `3 x 3` transverse family.  No
  full three-dimensional thermodynamic-limit claim is made.
