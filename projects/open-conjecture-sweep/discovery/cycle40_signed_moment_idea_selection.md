# Cycle 40 idea selection: signed ownership-moment completion

## Candidate engines

1. **Homological signed moment completion.** Choose mass-one singleton owner
   marginals supported outside rank-one blockers. Realize every distinct-time
   pair marginal on the off-diagonal owner graph by signed transportation, so
   every rank-two same-owner blocker vanishes. Complete each distinct-time
   triple from its three pair marginals by an inclusion--exclusion tensor, then
   correct all blocked diagonal entries inside the tensor kernel with zero pair
   marginals.
2. **Sparse exact LP on type-pair variables.** Materialize only pair variables
   touched by blocker/type incidences and solve by CEGAR.
3. **Positive Sherali--Adams relaxation.** Add nonnegativity to first and pair
   moments and seek a feasible local distribution.
4. **Stop Problem 1.** Treat Cycle 39 as saturation of ownership routing and
   bank the remaining cycles.

## Question the questions

The obvious question is whether a 147-million-variable pair system is
feasible. That asks a computer to rediscover linear algebra that can be
eliminated symbolically. Over a signed field, transportation feasibility is
controlled by connected components, not Hall inequalities. The graph of all
off-diagonal owner pairs is connected for thirteen owners, so compatible
marginals always lift.

Positivity is rejected at this gate. Cycles 35--39 use signed functionals, and
a positive Sherali--Adams outcome would answer a different question. Stopping
is premature because the pair-correlated construction has not yet been
tested and is genuinely outside every priority/fallback span.

Questioning the homological framing: a feasible degree-three moment system is
not a global ownership distribution and says nothing about arbitrary ideal
multiples. Its value is diagnostic. If the construction works, it proves that
all unmultiplied rank-at-most-three ownership generators are universally too
weak against signed local moments, forcing the next engine to use multiplied
relations or global consistency. If it fails, the precise failure identifies
the first genuine nonlocal obstruction.

## Proposed construction

For each raw time (t), let (A_t) be the coordinates at which (t) is not a
rank-one blocker and put any rational mass-one vector (a_t) on (A_t). For
distinct times (s,t), the bipartite graph of allowed pair entries contains
all off-diagonal owner pairs. It is connected for thirteen owners, so a signed
matrix with row marginal (a_s), column marginal (a_t), and zero diagonal
exists; use one fixed off-diagonal spanning tree and leaf elimination.

Given compatible pair matrices (M_{st},M_{su},M_{tu}), the tensor

\[
M_{st}\otimes a_u+M_{su}\otimes a_t+M_{tu}\otimes a_s
-2a_s\otimes a_t\otimes a_u
\]

has exactly those three pair marginals. Corrections in
(U^{\otimes3}), where (U) is the zero-sum owner space, preserve every pair
marginal. The blocked diagonal evaluations are independent on this kernel for
thirteen owners: if \(\sum_r c_r x_r^3\) vanishes whenever
\(\sum_r x_r=0\), two-coordinate tests make all (c_r) equal and a
three-coordinate test forces that common value to zero. Hence arbitrary
blocked diagonal values can be cancelled exactly.

## Choice and falsifier

Choose homological signed moment completion. Prove it abstractly, then replay
the frozen leaf: exact rank-one supports, every rank-two and rank-three raw
blocker label, spanning-tree transport, pair marginals, kernel corrections,
and repeated-time one-hot reductions.

The construction is falsified by a time blocked at every owner, a disconnected
allowed pair graph after exact rank-one restrictions, any transport marginal
mismatch, a triple base-tensor marginal mismatch, a nonzero correction pair
marginal, a singular blocked-diagonal restriction, or any surviving raw
rank-at-most-three blocker moment.
