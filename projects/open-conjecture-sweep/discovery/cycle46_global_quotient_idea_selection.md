# Cycle 46 idea selection: global closure quotient

## Brainstorm

1. **Relative-chain/Čech transgression.** Keep the 457 exact Morse residuals
   with their complete-type labels.  For each frozen pivot part, cover the
   residual support by the closed stars of *all* allowed owner vertices in
   that part, compute the exact Čech total complex, and project a residual to
   the first nonzero overlap row.  Import the globally reconstructed Cycle 41
   singleton/binary mediator relations into that row.
2. **Direct natural-fill interpolation.** Learn a sparse formula for the 457
   known fills from type masks and then verify it exactly.
3. **Small global signature universe.** Enumerate complete p199 signature
   quadruples and search for a finite forbidden-minor characterization.
4. **Keep extending the Morse schedule.** Optimize vertex order against the
   residual corpus.

## Decision questions and adversarial comparison

- For (1): does the global relation image span every transgressed residual,
  or does an exact dual survive?  It directly tests the state absent from the
  Cycle 45 countermodels.  The danger is that the chosen star cover could make
  the transgression zero or tautologically identify an already known fill.
  Therefore the map must be chain-level, label-preserving, and tested against
  synthetic nonboundary controls before interpreting a positive result.
- For (2): can one exact formula interpolate all residual fills?  This is
  cheaper, but a post hoc formula can memorize the corpus and gives no reason
  to generalize.  Reject as the main engine; retain only as a possible
  diagnostic after a quotient class is understood.
- For (3): is realizability itself enough to exclude the abstract
  countermodels?  This has useful falsification value, but it risks another
  large census with no theorem-shaped map.  Defer unless the exact quotient
  fails to expose usable relations.
- For (4): can a better local order erase the final 457?  Cycle 45 already
  proved local signature realizability insufficient and its nonboundary
  countermodels survive every valid homotopy.  Reject: it questions the wrong
  state space.

## Question the questioning

Why ask whether closure relations *span residuals* rather than whether another
fill exists?  Existence is already proved on the frozen rows.  The missing
information is why actual p199 rows avoid the exact local countermodels, so the
discriminating question must retain global type identities and admit a dual
obstruction.  Why use a Čech presentation?  Cycle 41's dense proof already
locates the obstruction in overlap homology; the total complex makes that
informal location an exact map.  What would make this misleading?  If the
global relations are merely re-encoded chosen fills, spanning would be
circular.  Freeze an input audit: relation columns may use only p199 type
supports, original rank-two deletions, singleton/binary mediator closure, and
the distinguished singleton marginals—never Cycle 43/44 fill coefficients.

The first proposed implementation used only the four distinguished stars and
added a generated remainder whenever they failed to cover the complex.  The
questioning pass rejects that formulation before executable work: the
remainder could absorb exactly the obstruction under test.  All owner-stars
of a pivot part are instead intrinsic to the p199 ownership geometry.  A
residual cell outside their union is retained as a relative obstruction; it
is never repaired by manufacturing another cover member.

A second conceptual audit separates degrees.  Cycle 41's singleton/binary
closure fixes zero cells, component balances, and the selected lower
marginals; it does not supply new degree-four columns.  The actual quotient
relations are boundaries of allowed p199 tetrahedra, transported through the
canonical Čech lift.  Adding the lower equations again as if they were
degree-four boundaries would be a category error and could manufacture a
false closure.  The useful new target is therefore the *shape* of the
owner-star quotient and a uniform symbolic reason its actual residual class
vanishes, not another numerical proof that the already known rows fill.

## Choice

Choose (1).  The main rejected alternative is (3), because realizability
enumeration has lower theorem yield unless the exact transgression first tells
us which global invariant matters.

Advance: construct a noncircular exact chain map and prove that every one of
the 457 transgressed residual classes lies in the frozen global-relation span,
with an independently reconstructed certificate.

Falsifier: a residual class and exact dual cochain that annihilates every
allowed global relation column but pairs nontrivially with that residual.  A
synthetic nonboundary control that is incorrectly killed is an implementation
error, not a mathematical negative.
