# Cycle 45 idea selection: critical-projection homotopy

## Brainstorm

1. **Distinguished-owner algebraic Morse matching.**  In each part, mark the
   delta owner selected by the frozen singleton marginal.  Lexicographically
   match a simplex with the simplex obtained by adjoining the first available
   distinguished vertex.  Prove acyclicity and compute the exact chain
   homotopy identity
   \(\partial h+h\partial=I-\pi\).  The complex itself need not be
   contractible; the target is \(\pi z=0\) for the canonical moment cycle.
2. **Filtration/spectral-sequence defect.**  Filter by the number and first
   position of distinguished owners.  Identify the first differential with
   the same cone operation and seek a closed formula for later differentials
   supported on deleted diagonal corners.
3. **Abstract countermodel first.**  Enumerate small four-partite complexes
   with distinguished vertices, diagonal rank-two/rank-three deletions,
   allowed selected pairs, and solvable signed face marginals.  Seek a
   canonical moment class with positive critical projection or no cone.
4. **Full actual-tuple census.**  Extend the shared canonical face assignment
   to every valid four-type multiset and test fillings directly.
5. **Global local-fill overlap audit.**  Assemble selected local tetrahedral
   fills into one affine system and search for a descent cocycle.

## Decision questions

- For 1: does the lexicographic matching give a well-defined acyclic partial
  matching, and is the canonical moment cycle killed by its critical
  projection even when ambient H2 is nonzero?
- For 2: does the filtration expose a defect formula more informative than
  the explicit matching, or merely rename its reduction steps?
- For 3: are the proved local support/marginal axioms alone sufficient for
  critical-projection vanishing; if not, what is the smallest exact
  countermodel and which actual invariant excludes it?
- For 4: would another finite all-fill result distinguish a theorem mechanism
  from increasingly broad sampling?
- For 5: do different four-type multisets actually share any degree-four
  variable after the common faces are fixed?

## Question the questioning

Asking whether the allowed complex contracts is wrong: Cycle 42 proves that
many actual complexes have nonzero H2.  The homotopy may only retract onto a
critical complex.  The meaningful bridge is whether the *specific moment
cycle* has zero critical projection, not whether ambient topology vanishes.

The inherited language of “another filling interface” is also misleading.
It makes a successful table look like progress while leaving the operator
that explains the table unspecified.  A new cycle must expose a reusable
operator or a countermodel to its proposed invariant.

Idea 5 initially sounds like the missing local-to-global theorem, but its
premise is false in the present graded model.  Degree-four variables decompose
by unordered four-type multiset.  Once degree-three faces are fixed, distinct
multisets have disjoint interiors; repeated-type symmetry is recovered by
averaging a fill over its stabilizer.  There is no further cross-multiset
descent equation to compute.

Idea 4 has high cost and low information gain.  Even an exhaustive finite
census would not itself explain the cancellation, and it risks applying the
old table-building approach to the new theorem-design problem.

Idea 2 may become the proof language after a matching is understood, but it
does not yet offer a smaller falsifiable prototype.  Idea 3 is highly
discriminating but diagnoses insufficiency rather than constructing the
bridge.  It should therefore serve as the adversary to Idea 1 inside the same
decision block.

## Choice

Choose Idea 1, with Idea 3 as a required falsification route.  First prove the
generic acyclic-matching and critical-projection identities independently of
LRC data.  Then instantiate the smallest exact actual and abstract models.
The proposed mechanism must preserve allowed support, orientation, repeated-
type equivariance, and the already frozen face boundary.  It may leave
ambient critical H2, but must kill the canonical moment cycle.

The companion independently proposed a global overlap audit before a Morse
construction.  The direct-sum/stabilizer argument above resolves its stated
compatibility concern, so the primary decision is to proceed to the genuinely
new operator rather than open a cycle for an automatic decomposition.

## Main rejected alternative

Reject a full actual-tuple fill census.  It is a larger instance of the
Cycle 43/44 engine and does not identify why the cycle avoids ambient H2.

## Falsifier

Any of the following refutes the proposed matching family: a directed cycle
in the frozen matching; a matched pair containing a forbidden simplex; failure
of \(\partial h+h\partial=I-\pi\); failure of repeated-type equivariance after
averaging; or an allowed actual structural interface whose canonical moment
cycle has nonzero exact critical projection.  A smallest abstract model with
positive critical projection does not refute the actual theorem, but proves
that the frozen local axioms are insufficient and identifies the additional
invariant the next construction must use.
