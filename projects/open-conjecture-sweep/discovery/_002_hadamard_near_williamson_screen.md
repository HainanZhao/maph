# _002 Hadamard-668 near-Williamson screen — `NO_SELECTION`

This is a non-credit discovery decision. It does not allocate D001, create a
preregistration, or authorize construction search.

## New source-defined state

`OBSERVED` from Kharaghani--Mohammadian--Tayfeh-Rezaie,
arXiv:2605.08661: a near-Williamson quadruple at order `n=167` consists of
four circulant sign matrices `A,B,C,D`, with `B,C,D` reversal-symmetric, such
that

```text
AA^T + BB^T + CC^T + DD^T = 4*167*I.
```

The Williamson block array then gives a real Hadamard matrix of order 668. In
sequence form the exact constraint is that the four periodic autocorrelations
sum to zero at every shift `1..83`; direct integer autocorrelation followed by
the block product is the smallest verifier. The source also supplies row-sum
and spectral pruning and an `A,B -> C,D` mod-4 reduction. Epoch's current
problem page still lists 668 as unresolved.

Sources: <https://arxiv.org/abs/2605.08661>,
<https://epoch.ai/frontiermath/open-problems/hadamard>.

## Delta and limit

This is a real delta from C96 and `_001`, which lacked a source-backed
structured family. But the source exhaustively classifies near-Williamson
objects only through order 35, supplies selected examples through 63, and
does not give a lift, recurrence, cyclotomic constructor, bounded quotient, or
reconstruction theorem for order 167. Its transition at 167 remains exhaustive
generation of `A` and symmetric `B`, then solution of the residual `C,D`
system.

An exhaustive/SAT/local-search run has a decisive positive outcome, but a
timeout or no-hit has no mechanism-level meaning. It would repeat the C96
forbidden census under a new name, so it is not an actionable D001 gate.

## Oracle packet

Oracle (`gpt-5.6-sol`, high effort) independently reviewed only the current
program, C96, `_001`, and the two sources above under the revised targeted
history rule. It agrees: the state and verifier are new, but the required
non-enumerative map and informative stop are absent. It ranked a cyclotomic
near-Williamson constructor on `Z_167` highest, requiring a class-level
convolution invariant and exact reconstruction; no such map is presently
specified. It returned `NO_SELECTION`.

## Decision

`NO_SELECTION`. Before D001 can be selected, supply an explicit
non-enumerative state map on `Z_167`, an invariant preserved by its transition,
an exact reconstruction of the four sequences, and a cap whose failure refutes
that construction rather than merely exhausting computation.
