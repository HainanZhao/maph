# Gate B5 source and novelty audit

## Claim boundary

This audit supports attribution and prevents complexity claims from being
applied outside their hypotheses.  It does not establish novelty of the Lane B
twist tensor.

## Sources checked

1. David Cimasoni, *A generalized Kac--Ward formula*, Theorem 2.1,
   <https://arxiv.org/abs/1004.3158>.  The formula uses `2^(2g)` spin
   structures for a graph embedded in an orientable genus-`g` surface.
2. Christian Millichap and Fabian Salinas, *Embedding Grid Graphs on
   Surfaces*, Theorems 3 and 4 and Proposition 2,
   <https://arxiv.org/abs/2104.12270>.  Their parameter convention has
   `alpha_i+1` vertices.  Hence `P_n square P_3 square P_3` is
   `G(n-1,2,2)`, and Theorem 4 gives minimum genus `n-1` directly.
3. Sorin Istrail, *Statistical Mechanics, Three-Dimensionality and
   NP-completeness I*, Theorems in Sections 5.1--5.2,
   <https://istrail-lab.github.io/papers/Statistical%20Mechanics%2C%20Three-Dimensionality%20and%20NP-completeness.pdf>.
   The hardness construction concerns finite sublattices of nonplanar crystal
   lattices with selectable couplings such as `{0,+J}` or `{-J,0,+J}`.  It is
   not a theorem that one fixed homogeneous ferromagnetic strip is hard, nor
   that graph genus alone determines complexity.
4. Alexander Scott and Gregory Sorkin, *Polynomial Constraint Satisfaction,
   Graph Bisection, and the Ising Partition Function*,
   <https://arxiv.org/abs/cs/0604079>.  Exact tree-decomposition dynamic
   programming applies to Ising partition functions.  This supports treating
   a fixed-width strip as conventionally tractable.
5. Thierry Gobron, *Graph theory and Pfaffian representations of Ising
   partition function*, <https://arxiv.org/abs/1312.7289>, especially
   Theorem 3.2 and Corollary 3.4.  A single multicomplex-algebra Pfaffian can
   package the nonplanar calculation, but the algebra/Pfaffian expansion still
   grows exponentially with an embedding-genus parameter.

## Attribution decisions

- `PROVED`: the all-`n` minimum-genus statement at `w=3` cites
  Millichap--Salinas Theorem 4.  Our induction supplies a new explicit
  period-two embedding attaining their value, not an independent all-size
  lower bound.
- `PROVED`: the 256-state carrier is the ordinary global-flip quotient under
  an explicit Walsh intertwiner.  It is not independently novel topology.
- `OBSERVED`: no checked source states the same collective TT compression of
  the complete spin-structure component for this embedding family.
- `CONJECTURED`: novelty of that collective compression remains unclaimed
  pending a broader search on homology-resolved bounded-pathwidth algorithms.

## Istrail boundary

The tempting sentence "unbounded genus but solvable contradicts genus as the
hardness barrier" is too coarse.  The strip has bounded pathwidth, while
Istrail's reductions exploit selectable interactions across a family of
finite sublattices of a translationally invariant nonplanar crystal lattice.
The defensible prospective theorem is about width/frontier complexity, not a
counterexample to Istrail.

