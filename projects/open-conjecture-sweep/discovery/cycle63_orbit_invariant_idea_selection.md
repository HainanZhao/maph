# C63 idea selection: continuous orbit space before elimination

## Serious candidates

1. **Exact joint-orbit invariant reduction (chosen).** Write the three
   transposition coordinates as `t+x,t+y,t+z`, where `x+y+z=0`, and the two
   cycle coordinates as `c+s,c-s`.  Conjugation permutes `(x,y,z)` and changes
   the sign of `s` under odd permutations.  Express the deficit using
   `r2=x^2+y^2+z^2`, `u=xyz`, `s2=s^2`, and
   `w=s(x-y)(y-z)(z-x)`, retaining the relation
   `w^2=s2*(r2^3/2-27*u^2)`.  Derive exact realizability inequalities and
   stratify any negative minimum before using elimination.
2. **Direct six-variable resultants.** Differentiate the existing homogeneous
   polynomial and eliminate five variables.  Rejected as the primary engine:
   it ignores symmetry, obscures boundary supports, and is likely to spend the
   degree budget proving multiplicities caused only by group orbits.
3. **Boundary-first support classification.** Recursively set coordinates to
   zero and solve every face.  This is a useful fallback after orbit reduction,
   but by itself repeats C62's face framing without controlling the continuous
   interior.
4. **Another coefficient cone or denser rational census.** Rejected.  C57,
   C59, and C62 already show that these mechanisms do not address the
   continuous stationary gap.

## Questioning the question

Why should orbit invariants help rather than merely rename the six variables?
The deficit is conjugation invariant, but the quotient is useful only if its
semialgebraic image and singular strata are stated exactly.  Variance alone is
misleading: the standard representation has the cubic invariant `u`, and the
cycle sign couples to the alternating discriminant through `w`.  Dropping
`w` could erase precisely the orientation information that permits a negative
minimum.

Why ask for all stationary points to be central?  That is stronger than the
comparison needs and C62 does not support it continuously.  The discriminating
question is instead whether every *negative minimum* can be forced onto an
explicit lower-dimensional boundary or into a finite exact stationary system.
Noncentral stationary points with nonnegative deficit are allowed.

Why now?  C61 excludes four local central patterns and C62 finds no rational
negative row but leaves the continuous KKT system open.  The orbit quotient is
the smallest state space that retains every invariant relevant to that gap.
The main rejected alternative is direct six-variable elimination because it
would hide rather than exploit the quotient singularities.

## Chosen question and falsifiers

Can the normalized nonnegative S3 Zhao deficit be expressed exactly on the
joint orbit space and can every hypothetical negative minimum be reduced to
explicit boundary strata or a zero-dimensional exact stationary system?

- A rational nonnegative S3 function with negative deficit falsifies Zhao's
  comparison directly.
- A positive-dimensional noncentral negative stationary component surviving
  the exact orbit constraints falsifies the proposed finite-minimizer engine.
- Failure of one elimination order or degree cap is only a computational
  boundary, not a mathematical no-go.
