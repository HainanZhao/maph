# C56 idea selection: one-orbit conjugacy smoothing

## Candidates

1. **Exact single-orbit smoothing packet (chosen).** For (S_3), replace the
   values on one fixed conjugacy class by their arithmetic mean while holding
   the other class values fixed. Evaluate the Cayley numerator before and
   after smoothing on a compact nonnegative integer function packet. A single
   strict increase after smoothing is a rational falsifier of the proposed
   universal contraction.

2. **Direct universal variance proof.** It is the intended positive route,
   but first needs a clean discriminator: orbitwise Schur-convexity is much
   stronger than Zhao's final all-at-once comparison and could fail. Deferred
   until the exact packet tells us whether the premise survives.

3. **More all-class Zhao packets.** C55 already closes that family. Rejected.

## Question the question

Why can a finite packet be useful? A negative row conclusively kills the
universal smoothing statement. Why can a pass mislead? It cannot establish
Schur-convexity, and fixed integer levels need not see a rational failure.
The packet therefore has no positive universal claim. The real target is a
one-class countermodel, not a favorable count.

## Choice

Use every (S_3) function (a:S_3\to\{0,1,2\}) and smooth exactly one
chosen nontrivial conjugacy class (transpositions or 3-cycles) at a time.
This is a bounded compact falsifier search; retain the first exact reversing
row and stop the universal smoothing route if found.
