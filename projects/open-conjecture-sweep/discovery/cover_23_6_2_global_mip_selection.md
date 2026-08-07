# Global block-variable engine selection for C(23,6,2)

Decision question: does the complete set-cover model on all `C(23,6)=100947`
candidate blocks contain a solution using at most 20 blocks?

## Question the question

The earlier labelled-incidence SAT formulas ask a solver to invent every
entry of a `20 x 23` matrix while simultaneously learning block and point
symmetry. Ten-minute canonical star branches did not decide. Local repair
found two-pair-deficient families, but proximity to those families is not a
mathematical invariant and exact neighborhoods through four changed blocks
do not cover the search space.

The risk in changing representations is to confuse a MIP solver's status with
a proof. This engine is therefore discovery-asymmetric: a feasible incumbent
is a complete answer after direct pair checking; an infeasibility status is
only `OBSERVED` and must be translated to a proof-producing SAT split.

## Brainstorm and exclusion map

- Labelled incidence SAT: exact global semantics, but prior runs timed out;
  delta here is one Boolean per possible six-set and no block labels.
- Near-cover repair: excludes only bounded Hamming neighborhoods; delta here
  is global coverage with no incumbent geometry.
- Excess-spectrum route: proves `|{v:r_v>5}|>=3` and excludes excess
  partitions `(5)`, `(4,1)`, `(3,2)`; delta here is direct optimization over
  blocks rather than enumeration of excess multigraphs.
- Residual-star canonical augmentation: potentially proof-producing but
  requires many orbit cases; retained as the main alternative if the global
  model points to infeasibility.

Selected input state: all 100947 six-subsets of `{0,...,22}`.

Invariant/map: a binary variable selects a block; each of the 253 pair rows
has covering sum at least one; every point replication lies in `[5,8]` by the
counting and excess-spectrum reductions; the selected-block sum is at most 20.
Relabel a replication-five point as `0` and one incident block as
`{0,...,5}`; fix that block and the degree of point `0` to remove the full
point symmetry without losing any solution.

Smallest direct verifier: decode every positive variable and recount all 253
pairs independently of the optimizer.

Falsifier: any decoded family with at most 20 distinct six-subsets that fails
to cover a pair invalidates the claimed feasible result. Conversely, a
verified 20-block family settles the target at 20 using the known lower bound.

Resource stop: one 30-minute, three-thread run using at most 10 GiB resident
memory. If it produces no verified incumbent, stop this engine and use its
bound/status only to choose the next exact SAT decomposition.

Contained optimization after the first root run: fixing only one block and
the degree-five point still left HiGHS to rediscover the entire five-block
star. The three star-slot partitions have exactly eleven support orbits:
one `(4)` case, three `(3+2)` cases, and seven `(2+2+2)` cases. Run the same
global model separately behind these exhaustive canonical stars; their union
is equivalent to the original decision question.
