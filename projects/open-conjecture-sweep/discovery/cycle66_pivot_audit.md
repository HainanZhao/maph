# C66 S3 Zhao pivot audit

Audit date: 2026-08-05 UTC.

## Exact logical leverage

- `PROVED` from Zhao, Theorem 1.3: for a fixed bipartite graph `H`, the
  comparison

  ```text
  t_Cay(H; Gamma, a) >= t_Cay(H; Gamma, a^cl)
  ```

  for every finite group `Gamma` and nonnegative function `a` implies that
  `H` is strong Sidorenko, hence Sidorenko.  The proof actually needs only
  `Gamma=S_n` and subgroup-product indicators `a=1_(T1 T2)` for every `n`.
  Source: Yuqi Zhao, *Conjugacy Class Averages and Sidorenko's Conjecture*,
  arXiv:2606.15368v1, Theorem 1.3 and proof, lines 157--174 and 635--667 of
  the HTML version: <https://arxiv.org/html/2606.15368v1>.
- `PROVED`: C63--C64 concern this exact comparison for the fixed graph
  `H=K_{5,5} minus C_10`, the fixed group `Gamma=S_3`, and every nonnegative
  real function `a:S_3 -> R`.  Completing its sign would therefore prove a
  full continuous nonabelian case of Zhao's comparison.  It would **not**
  verify the all-`n` subgroup-product condition used by Theorem 1.3.
- `PROVED` from Zhao, Theorem 1.4: the paper's positive arbitrary-group result
  applies to 1-subdivision graphs.  The target Möbius graph is 3-regular and
  is not covered by that theorem.  Source: same paper, Theorem 1.4, lines
  180--198.
- `PROVED` from Lee--Schülke, Theorem 1.3: the Möbius graph is not weakly
  norming; their result does not settle Sidorenko.  Source:
  <https://arxiv.org/abs/1910.08454>.
- `PROVED` from Lovász, Theorem 3.1 / the paper's local-Sidorenko result: every
  simple bipartite graph satisfies the Sidorenko inequality in a neighborhood
  of constant graphons.  Consequently C53--C54's directional local theorem is
  an explicit jet calculation and consistency check, not the pivot result.
  Source: <https://arxiv.org/abs/1004.3026>.

## Bounded novelty search

The frozen searches used the exact paper title, arXiv identifier, theorem
number, `S3`, “conjugacy averaging”, “Cayley homomorphism density”, and the
Möbius-graph names.  The inspected primary items were Zhao's v1 paper and its
June 2026 two-sided-correlation sequel, Lee--Schülke, and Szegedy's determinant
paper.  Search results returned no primary theorem for the fixed-`S3` Zhao
comparison and no invariant or semialgebraic reduction of it.

- `OBSERVED`: within this bounded current search, C63's exact six-coordinate
  quotient and C64's uniform degree-26 fiber reduction are not subsumed by a
  located primary result.
- `CONJECTURED`: the reduction is novel.  The search is too recent and too
  bounded for an unconditional priority claim.

## Materiality test

`PROVED`: before C63--C64, the fixed-`S3` comparison is a homogeneous
degree-15 inequality over six nonnegative function values.  C63 gives its
exact realizable joint-invariant quotient.  C64 then eliminates the two fiber
variables uniformly: every fixed outer fiber has four explicit endpoint
families or at most 156 isolated algebraic stationary pairs, with no
genericity exception because the resultant's `u^26` coefficient is a nonzero
constant.  This removes a genuine continuous minimization obstacle rather
than merely sampling it.

The limitation is equally exact: the candidates vary over a three-dimensional
outer continuum.  One `S3` theorem does not imply the Möbius graph is
Sidorenko, and no transfer from the `S3` invariant ring to all symmetric
groups is presently proved.

The companion independently identified scalability as the strongest flaw:
the actually decisive family in Zhao's proof is `(S_n,1_(T1 T2))` for every
`n`, while the invariant ring used here is special to `S3`.  Any eventual
paper claim must therefore present the fixed-group theorem as a nonabelian
viability result, not as quantitative progress through the all-`n` gate.

## Pivot decision and next lemma

The finding clears the user's leverage threshold: it supplies a new exact
reduction for a nontrivial continuous special case of a published sufficient
condition for an open Sidorenko instance.  The pivot is to the **fixed-`S3`
Zhao comparison**, not back to finite group or step-graphon censuses.

The smallest next decision lemma is boundary positivity:

> For every feasible outer tuple `(e,t,c,r2)`, the Zhao deficit `P` is
> nonnegative on each of C64's four fiber endpoint families.

This lemma is directly falsifiable by one exact feasible negative point.  If
proved, it removes every endpoint minimum and isolates the at-most-156
resultant branches as the sole remaining obstruction.  If falsified, it gives
an exact counterexample to the fixed-`S3` Zhao comparison.  The new engine
should be domain-aware exact Bernstein subdivision or CAD on the four boundary
families, not another coefficientwise Pólya multiplier: the latter was already
closed at its frozen cap and ignores the semialgebraic domain.

## Claim boundary

`PROVED`: the logical implication and C64 reduction stated above.
`OBSERVED`: no overlapping fixed-`S3` theorem was found in the bounded search.
`CONJECTURED`: novelty and likely publishability.  Neither the fixed-`S3` sign,
Zhao's universal comparison, strong Sidorenko, nor Sidorenko is proved.
