# Cycle 38: rooted ownership functional obstruction

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78, none of the thirteen cyclic rooted
pushforwards of the Cycle 37 signed product measure, nor any mass-one linear
combination of them, annihilates every unmultiplied Cycle 29 ownership/blocker
generator.

This is not a statement about arbitrary ownership functionals, generator
multiples, the full ownership ideal, leaf infeasibility, or (LRC(13)).

## Rooted ownership maps

Fix a root (r) and cyclically order the coordinates starting at (r). For a
digit assignment, assign a time to the first coordinate in this order whose
chosen digit covers it; if no coordinate covers it, assign it to (r).

`PROVED`: every time has exactly one owner, so totality and pairwise
exclusivity hold pointwise. If (B) is a blocker at coordinate (i\ne r),
then every time owned by (i) is covered by the one chosen digit at (i).
The event that (i) owns every time of (B) is therefore empty by the
definition of a blocker. Thus all off-root blocker monomials vanish pointwise.

## Root moment factorization

For a blocker (B) at (r), split an ownership event according to the subset
(S\subseteq B) of times that are globally uncovered. The root digit must
miss (S) and cover (B\setminus S); every other chosen digit must miss all
of (S). Under the product signed measure, the contribution factorizes as

\[
 \left(\sum_{d_r}u_r(d_r)
  1[d_r\text{ misses }S\text{ and covers }B\setminus S]\right)
 \prod_{j\ne r}\left(\sum_{d_j}u_j(d_j)
  1[d_j\text{ misses }S]\right).
\]

`PROVED`: summing this expression over all (S\subseteq B) is exactly the
root blocker moment. The formula is a disjoint partition of the ownership
event and uses only finite distributivity. Rank at most three gives at most
eight terms.

## Complete-type quotient

A time's complete type is its labeled vector of thirteen coverage masks over
the allowed digit offsets. `PROVED`: the factorized moment depends only on the
ordered complete types of the blocker times. Inside each local signature
class, grouping raw times by complete type is therefore exact. Cycle 29
blocker patterns contain distinct local signatures, so a type tuple has
multiplicity equal to the product of its type-class counts.

The primary exact enumeration projects all complete types back to the Cycle 29
local classes and recovers all 12,264 symbolic patterns and all 190,867,444
concrete blockers. It evaluates 26,348,103 complete-type tuples. Every root
has a nonzero rank-two moment; rank-three moments are retained for roots where
they occur.

## Independent obstruction certificate

The independent replay reconstructs the raw coverage interface and enumerates
all 14,406 nonzero-support assignments of the Cycle 37 signed measure. For
each root it verifies directly that the recorded pair is a minimal blocker and
recomputes its nonzero ownership moment. The resulting diagonal entries are

\[
(150,100,1,1,5,5,5,-1,-25,100,-20,4,1).
\]

Let (alpha_r) be the coefficient of rooted measure (r). Off-root
pointwise vanishing makes the selected blocker matrix diagonal with these
entries, while mass one requires (sum_r\alpha_r=1). The independently
generated integer left-null multipliers

\[
(-2,-3,-300,-300,-60,-60,-60,300,12,-3,15,-75,-300;300)
\]

annihilate every (alpha_r) coefficient in the augmented system and send its
right-hand side to (300\ne0). `PROVED`: the augmented system is inconsistent,
so no mass-one functional lies in this thirteen-measure span.

## Falsifiers

Any wrong owner, coverage label, local signature, blocker minimality, complete
type, multiplicity, factorized moment, direct-support moment, off-root zero,
or augmented left-null product invalidates the affected claim. Failure of this
rooted span does not falsify a root-free or nonlocal ownership routing kernel.
