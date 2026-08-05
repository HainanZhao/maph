# Cycle 47 idea selection: global affine descent

## Brainstorm

1. **Shared-face affine sheaf.**  Give every unordered labeled type triple one
   affine space of admissible owner tensors.  Give every type quadruple its
   affine space of allowed tetrahedral chains.  Glue them by the four signed
   boundary maps and ask for one rational section on a densely overlapping,
   outcome-blind p199 patch.
2. **All-interface ambient homology census.**  Extend Cycle 42's individual
   H2 calculation to many more type quadruples and look for a rare positive
   class.
3. **Locality inverse theorem.**  Try to prove that any natural face tensor
   with the frozen pair marginals must be a cone or must have bounded local
   support.
4. **Symbolic prime-product lift.**  Return directly to the analytic
   p199-to-next-prime lifting interface and seek a new CRT closure identity.

The companion independently proposed (1), with (2) as a lower-information
fallback and (3) as a later theorem route.  The primary proposal was also
(1), but only after adding a raw-label descent audit and excluding the already
solved Cycle 43/44 interfaces from the principal patch.

## Decision questions and adversarial comparison

- For (1): after a face shared by several quadruples is represented by one
  variable, do the locally solvable boundary equations possess one global
  rational section?  A negative answer has an exact syzygy/cocycle witness;
  a positive answer is an explicit compatible degree-four construction.
  Cost is moderate because the incidence patch is sparse and connected.
- For (2): does ambient H2 alone discriminate actual moment data?  Cycle 42
  already answered no on one actual class and Cycles 43--44 filled thousands
  of positive-H2 cases.  More census rows would measure prevalence but would
  not repair that missing link.  Reject as the main engine.
- For (3): is locality forced by the marginal equations?  This could yield a
  theorem, but Cycles 45--46 show that purely local geometry admits exact
  countermodels and coordinate reformulations.  Defer until the global
  compatibility system reveals which locality statement could be true.
- For (4): can arithmetic closure bypass the topological interface?  It is
  genuinely distinct but currently blocked by the absence of a degree-four
  compatible state.  The descent system is the smaller discriminating test.

## Question the questioning

Why ask for a global section when Cycles 43 and 44 already used one tensor per
triple?  On their frozen rows, they did: rerunning that union would be old work
under a new name.  The principal patch must therefore contain no previously
tested quadruple and must be selected to have many incidence cycles, not as a
random collection of nearly isolated rows.

Why quotient by repeated types at all?  A quotient can invent compatibility
if it loses which occurrence, orientation, or stabilizer action a face has.
The theorem must start with occurrence-labeled face coordinates, impose the
literal equality and permutation equations, and only then prove equivalence
with the compressed unordered-triple system.  A rank match alone is not an
equivalence proof; solutions and left-null witnesses must transport both
ways on exact controls.

Why could a positive solve still be misleading?  Independent local fills can
always be juxtaposed if faces are not shared, and the old canonical face rule
could solve the new patch without exposing a new theorem.  Connectivity alone
is too weak.  Selection therefore prefers a candidate adjoining through the
largest number of already present triple faces, and the result must report the
incidence cycle rank.  Promotion is limited to the frozen patch unless the
computed section yields a symbolic local-to-global construction.

Could the affine system fail for a merely local reason?  Yes.  Test every
quadruple separately first.  Distinguish a `LOCAL_OBSTRUCTION` from the new
target, a `DESCENT_OBSTRUCTION` in which all stalks are nonempty but their
shared-face gluing is inconsistent.

## Choice

Choose (1): a raw-labeled affine sheaf with a proved compressed descent map.
The main rejected alternative is (2), because another ambient-homology census
does not test the globally missing state.

Advance: on a new outcome-blind connected patch, either construct one exact
global section after every local stalk is shown nonempty, or produce a
primitive exact global cocycle separating the shared boundary data from all
local fill relations.

Falsifier: an exact left-null vector annihilating the full global coefficient
matrix and pairing nontrivially with its affine right-hand side.  Any failure
to transport raw and compressed solutions or duals is instead an
implementation error and blocks interpretation.
