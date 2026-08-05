# C67 idea selection: exact fixed-S3 endpoint positivity

## Geometry first

C64's four fiber endpoints have radical-free representatives in the original
six `S3` function values:

1. the two cycle values are equal;
2. one cycle value is zero;
3. two transposition values are equal;
4. one transposition value is zero.

After grouping repeated values by their total mass, every family is a rational
four-simplex.  This is substantially better than treating the invariant
inequalities with square roots.

## Serious candidates

1. **Symmetry-adapted simplex Bernstein certification (chosen).** Pull the
   exact degree-15 Zhao deficit back to each of the four mass simplexes.  Check
   it independently against the C63 invariant polynomial.  Factor or blow up
   the known class-constant equality strata, then use exact rational Bernstein
   coefficients and adaptive simplex subdivision on the residual pieces.

   - Preserves: the exact original function values, normalization, endpoint
     exhaustiveness, and deficit sign.
   - Falsifier: one rational simplex point with negative exact deficit.
   - Proof output: a finite rational subdivision whose Bernstein lower bounds
     are nonnegative, together with exact equality-stratum handling.

2. **Full cylindrical algebraic decomposition.** It is complete in principle,
   but a degree-15 polynomial on four-dimensional simplexes is likely to spend
   the tranche eliminating irrelevant variables.  Retain only as a fallback
   on a lower-dimensional unresolved cell or factor.

3. **Floating SDP followed by rational SOS reconstruction.** Gram symmetry may
   be valuable, but the prior unpinned SDP route and domain multipliers create
   a large post-selection surface.  Reject as the first engine; use only if
   Bernstein exposes a small fixed Gram support.

4. **Dense rational or floating boundary search.** Useful only as a falsifier
   probe and control.  It cannot close positivity, so it is subordinate to the
   certificate engine and may not become a resolution ladder.

## Question the questioning

Why ask for all four endpoint families at once?  They are one theorem gate and
share the same pullback and certificate machinery.  Splitting them into four
cycles would be bookkeeping, not research cadence.

Why should Bernstein succeed near equality, where the deficit vanishes?
Unfactored subdivision may not.  The class-constant strata must be handled
symbolically first; a cell touching a zero stratum is not allowed to consume
an infinite subdivision ladder.  The engine must expose the vanishing ideal,
factor a nonnegative transverse form, or hand a fixed lower-dimensional piece
to exact CAD.

What inherited assumption is suspect?  Mixed monomial coefficients were
treated as evidence that positivity certificates are hard.  On a constrained
simplex, translated Bernstein coefficients can become positive even when the
global monomial cone fails.  Conversely, merely raising Bernstein degree is
the old Pólya idea and is not a new engine; spatial subdivision is essential.

What does this question hide?  Interior resultant branches.  They remain
blocked deliberately: a negative endpoint already falsifies the fixed-`S3`
comparison, while positive endpoint certificates sharply isolate the interior
obstruction.

## Chosen question

Is the exact Zhao deficit nonnegative on all four radical-free endpoint
simplexes, certified by symmetry-aware exact subdivision, or does one contain
an exactly reconstructible negative point?

Main rejected alternative: a monolithic four-dimensional CAD before using the
simplex and equality geometry.

Falsifier: a rational nonnegative six-value `S3` function on one endpoint
family with exact `N(a)-N(a^cl)<0`.
