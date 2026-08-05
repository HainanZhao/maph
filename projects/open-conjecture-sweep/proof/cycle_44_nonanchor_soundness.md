# Cycle 44 soundness boundary

## Headline

`PROVED`: on the frozen outcome-blind holdout of 2,000 non-anchor four-type
interfaces, Cycle 43's globally shared face assignment extends rationally on
every interface. Exactly 1,528 cycles have an explicit distinguished-vertex
cone fill. The other 472 lie in complexes with exact
\(H_2(-;\mathbf F_2)=0\), which proves that they are rational boundaries.

All 29 selected interfaces with nonzero \(H_2(-;\mathbf F_2)\) are in the
explicit-cone class. This is a finite cone-or-acyclic dichotomy, not a
universal contraction theorem.

## Outcome-blind selection

The selector generated 100,000 SHA-256 candidates and three frozen
constructed families, then deduplicated to 103,289 valid non-anchor type
multisets. Structural stratification retained 7,928 preliminary interfaces.
Exact GF(2) homology refined those strata before any moment face was solved;
the final list contains 2,000 interfaces and excludes every Cycle 42 anchor.

The final set has 1,971 interfaces with GF(2) H2 dimension zero and 29 with
positive dimension. Repeated-type partitions and all four frozen density bins
occur. These are properties of the frozen sample, not population estimates.

## Exact construction

The 2,000 interfaces use 7,754 unordered face tensors and 11,387 oriented
pair moments. Each face is solved once and reused wherever it occurs;
repeated-type stabilizers are averaged. The alternating boundary of the four
faces gives an exact rational two-cycle.

For 1,528 interfaces, adjoining the frozen delta owner in one distinguished
part to the opposite canonical face gives an allowed tetrahedral chain whose
boundary is exactly the full cycle. These cone chains contain 8,291 nonzero
coefficients in total and have support at most 23.

For each remaining interface, the independently checked simplicial chain
complex has \(H_2(-;\mathbf F_2)=0\). Universal coefficients give

\[
  \dim_{\mathbf Q} H_2(-;\mathbf Q)
  \leq \dim_{\mathbf F_2} H_2(-;\mathbf F_2)=0,
\]

so its rational two-cycle is a boundary. No arbitrary rational witness is
needed for that existence claim.

## Coherence on the selected family

`PROVED`: the local existence statements can coexist on the selected family.
Degree-four cells decompose by their unordered four-type multiset, while the
degree-three face values have already been fixed globally. Distinct selected
type multisets therefore have disjoint interior variables and introduce no
additional overlap equation. For a multiset with repeated types, the allowed
complex and its canonical boundary are invariant under the type stabilizer;
averaging any rational fill over that finite stabilizer produces an invariant
fill with the same boundary. This is a direct-sum and averaging argument, not
an empirical compatibility assumption.

It does not extend the result to an unselected type multiset.

## Independent verification

An independently written route reverses candidate generation and raw pattern
orders, uses lowest-bit rather than highest-bit GF(2) pivots, and reproduces
the same 103,289 candidates, 7,928 preliminary interfaces, and ordered list of
2,000 selected interfaces. It reconstructs every selected H2 value and checks
all 29,557 shared-face coefficients, 30,677 cycle coefficients, and 8,291 cone
coefficients. Every rank-one, rank-two, and rank-three support restriction,
shared marginal, repeated-type stabilizer, cycle boundary, cone boundary, and
H2-zero existence classification passes.

The initial implementation attempted unnecessary explicit rational fills on
the 1,971 H2-zero rows and crossed its first wall cap without producing a
result. It was contained in the same cycle. The optimized route used the exact
H2 comparison above and completed independently; no conclusion relies on the
capped attempt.

## Structural clue and claim boundary

`OBSERVED` within the `PROVED` census: positive ambient H2 never obstructed
the actual canonical moment cycle because every such case admitted a cone.
This suggests a chain homotopy whose defect is confined to rank-three deletion
corners and killed by a distinguished vertex.

Cycle 44 does not cover all four-type multisets, prove that cone-or-acyclic is
universal, construct a natural chain homotopy, span the complete
rank-three-literal multiplier layer, produce a leaf certificate, or prove
LRC(13).
