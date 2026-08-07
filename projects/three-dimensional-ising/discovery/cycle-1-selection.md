# Cycle 1 selection: reconstruct the obstruction

## Question

Which exact compression step—not which informal physical metaphor—separates
the solvable planar Ising model from finite simple-cubic boxes?

## Question the questioning

The phrase “why 2D methods fail” risks presupposing a universal impossibility
theorem. That would be stronger than the evidence. The cycle therefore asks
for scoped failure statements about named mechanisms and records what remains
open after each one. It also treats intersections, knots, nonplanarity,
fermionic nonlocality, duality, and complexity as different propositions.

## Brainstorm before selection

Mechanisms considered:

1. Compare the high- and low-temperature chain complexes in dimensions two
   and three.
2. Quantify the orientable genus required by a cubic box and insert it into
   the surface Kac--Ward theorem.
3. Audit ordinary Jordan--Wigner ordering on a two-dimensional transfer
   layer.
4. Track the type change under Kramers--Wannier/Wegner duality.
5. Test whether published hardness statements actually cover uniform full
   boxes.

The selected mechanism is (2), accompanied by (1), (3), (4), and (5), because
it gives the smallest direct proof of a volume-exponential obstruction to the
standard Kac--Ward/Pfaffian surface formula without pretending to exclude a
new higher-form compression.

## Frozen decision data

- Input state: free `L x L x L` cubic graphs and signed seams on small wrapped
  boxes.
- Invariant/transition: orientable graph genus enters as the dimension
  `2g` of the spin-structure label space; high-/low-temperature expansions
  enter as exact binary chain spaces.
- Smallest verifier: Euler's formula plus the girth-four face bound, and exact
  coefficient enumeration on the declared small boxes.
- Stop criterion: no state space above `2^20` under naive enumeration; use an
  exact cycle-space basis for wrapped cases.
- Falsifier: a valid bounded-genus embedding of the free cubic boxes, a
  surface Kac--Ward theorem using fewer terms in the stated generality, or an
  exact coefficient mismatch in the replay.

## Exclusion map

There is no former project cycle. The initial exclusions are scope controls:

| Former question or shortcut | Outcome/falsifier | State or boundary delta |
|---|---|---|
| Guess `beta_c` from self-duality | Excluded by the user directive and by the 3D dual theory's change of degree type | Work begins at finite-lattice structure |
| Treat knots/intersections as a proof of impossibility | No such theorem was identified | Retain local enrichment and higher-form candidates |
| Invoke generic hardness against uniform boxes | Located hardness reductions use selectable sublattices/couplings | Complexity evidence is scoped, not terminal |
| Call any determinant an exact solution | Generalized Kac--Ward already supplies an exact but exponentially long determinant sum | Reduction, not syntax, is the gate |
