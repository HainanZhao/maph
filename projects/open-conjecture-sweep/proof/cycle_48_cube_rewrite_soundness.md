# Cycle 48 soundness boundary: Möbius gluing and cube repair

## Closed three-marginal extension

Let (P_{01},P_{02},P_{12}) be rational pair tensors whose singleton
marginals are the distinguished point masses
(delta_{d_0},delta_{d_1},delta_{d_2}).  Define

\[
 M=P_{01}\otimes\delta_{d_2}
   +P_{02}\otimes\delta_{d_1}
   +\delta_{d_0}\otimes P_{12}
   -2\delta_{(d_0,d_1,d_2)}.
\]

`PROVED`: the ((0,1))-marginal of the four summands is respectively
(P_{01}), (delta_{d_0}\otimesdelta_{d_1}),
(delta_{d_0}\otimesdelta_{d_1}), and
(-2delta_{d_0}\otimesdelta_{d_1}).  Their sum is (P_{01}); the other
two cases are identical.  Thus (M) is a closed formula extending all three
pair transports.  It may use forbidden owner triples, which is the only
defect addressed by the rewrite system.

## Universal cube kernel

Choose two distinct owners in each coordinate and orient the resulting
(2\times2\times2) cube by

\[
 C(a_i,b_j,c_k)=(-1)^{i+j+k}.
\]

`PROVED`: summing over any one coordinate pairs two entries with opposite
sign.  Hence every two-coordinate marginal of (C) is zero.  Adding any
rational multiple of a cube preserves all three prescribed pair transports.
This statement is independent of the p199 deletion pattern; deletions decide
only which cube cells are defects.

## Triangular orientation and termination

Order forbidden owner triples lexicographically.  A cube is admissible at
pivot (x) when it contains (x) and every other forbidden cube cell is
strictly later than (x).  Normalize its coefficient at the lexicographically
least cube cell to (+1).  At pivot (x), subtract the unique scalar multiple
that kills the current coefficient of (x).

`PROVED`: an admissible move changes no earlier forbidden coordinate and kills
its pivot exactly.  Scanning the finite forbidden list therefore terminates
after at most one nontrivial move per forbidden coordinate.  If every nonzero
pivot encountered has an admissible cube, the terminal tensor has allowed
support and retains the original three pair marginals.  No positivity is
claimed or required.

If every forbidden coordinate has a frozen reducer, the construction repairs
every rational tensor on that support product.  If only the pivots reached by
the Möbius tensor have reducers, the result is a targeted constructor for that
tensor, not a universal fiber theorem.

## Critical choices

Let (C_x) be the frozen reducer at pivot (x), and let (A_x) be another
admissible cube there.  After normalizing both at (x), their difference

\[
 D_x=A_x/A_x(x)-C_x/C_x(x)
\]

has zero pair marginals and zero coefficient at (x), with no forbidden
coefficient earlier than (x).  Reducing (D_x) by the frozen later rules
computes the exact difference between taking the alternative branch and the
frozen branch, followed by deterministic normalization.

`PROVED`: a nonzero allowed normal form of (D_x) is a literal nonjoinable
diamond for this normal-form notion.  It does not obstruct either branch from
producing a valid tensor, because their difference remains in the
zero-pair-marginal kernel.  Conversely, zero normal form for every critical
choice in a closed triangular rule domain makes every one-step choice agree
with the deterministic normal form; termination then gives confluence on that
domain by induction on the least remaining forbidden pivot.

## Claim boundary

`PROVED` by exact principal computation and a full reverse-order independent
reconstruction on the frozen 512-face corpus: all 512 Möbius tensors repair to
allowed support with their prescribed pair marginals.  The independent route
reconstructed the selector, Möbius tensors, forbidden sets, cube choices,
repairs, and reached critical diamonds without importing the principal rewrite
module.
Twelve patterns have a reducer at every forbidden cell (`STRONG_REPAIR`); the
remaining 500 repair along every pivot actually reached by their Möbius start
(`TARGETED_REPAIR`).  No reached pivot is unrepaired.  The 314 faces with a
nonzero initial forbidden coefficient all have a nonjoinable reached critical
diamond; the other 198 reach no such diamond.  Thus deterministic construction
survives, while literal order-independence is exactly refuted on every
nontrivial sampled start.

The finite computation classifies only its frozen structural face corpus.
`CONJECTURED`: the targeted triangular repair mechanism extends to all p199
face types, or admits a structural characterization broad enough to replace a
face census.  The corpus result does not prove that conjecture, every
quadruple fills, a full degree-four functional, a leaf certificate, or
LRC(13).  A future unrepaired Möbius defect would refute the frozen triangular
cube orientation, not arbitrary cube sequences or general linear extension.
