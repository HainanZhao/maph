# C65 idea selection: one fixed direct graphon family

## Serious candidates

1. **Complete unequal-weight 2x2 bipartite step family (chosen).** Let the
   left and right atom weights be `(p,1-p)` and `(q,1-q)` and let the four
   kernel entries range independently in `[0,1]`.  Homogeneity and atom
   relabeling put a maximal entry at `W00=1`, leaving five compact parameters.
   Optimize the actual ratio `t_H(U)/t_K2(U)^15`, then reconstruct every
   apparent negative point exactly.  A bipartite violation transfers to a
   symmetric graphon by the tensor symmetrization
   `W((x,y),(x',y'))=U(x,y')U(x',y)`.
2. **Continue the C64 resultant branches.** This could prove the stronger S3
   Zhao comparison, but the candidates still vary over a three-dimensional
   outer continuum and boundary signs remain as hard as the original
   inequality.  Rejected at this portfolio fork in favor of a direct target
   falsifier.
3. **A 3x3 or adaptive step ladder.** Rejected.  More blocks increase search
   flexibility but turn a discriminating fixed family into an indefinitely
   enlarging census.
4. **Equal-weight 2x2 search.** Rejected as primary because C52 already tested
   extensive equal-block local directions; unequal weights are part of the
   genuinely new nonlocal state space.

## Questioning the question

Why can one matrix entry be fixed to one?  The ratio is homogeneous under
positive scaling of the kernel.  Every nonzero matrix can be scaled until its
maximum is one, and independent row/column atom relabeling moves a chosen
maximum to `(0,0)` without changing either density.  The zero kernel satisfies
the inequality trivially and is excluded from ratio optimization.

Why use a bipartite kernel when the target is stated for symmetric graphons?
For `Z=X x Y`, the symmetric kernel
`W((x,y),(x',y'))=U(x,y')U(x',y)` has edge density `t_K2(U)^2` and, for the
fixed bipartite graph H, homomorphism density `t_H(U)^2`.  Therefore an exact
negative bipartite deficit yields an exact symmetric counterexample.

Why search rather than immediately derive KKT equations?  A negative point is
decisive and cheap to verify, while a global stationary classification in five
variables is expensive.  The fixed search first determines whether that cost
is justified.  A pass remains bounded evidence unless it exposes a reusable
exact extremal structure.

## Chosen question, falsifier, and hard stop

Does `t_H(U)>=t_K2(U)^15` hold throughout the complete normalized unequal-
weight 2x2 bipartite step family, or is there an exactly reconstructible
negative point?

- An exact rational negative point is a Sidorenko counterexample after tensor
  symmetrization.
- A floating negative candidate is `RECOGNIZED` only until exact arithmetic
  confirms it.
- Failure to find a negative point proves nothing globally.
- If this one fixed family yields neither a counterexample nor reusable exact
  extremal structure, pause Problem 2 and bank its remaining cycles.  Do not
  open a block-size or resolution ladder.
