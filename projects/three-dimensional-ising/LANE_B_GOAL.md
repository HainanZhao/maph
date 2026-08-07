# Goal: upgrade canonical spin-structure compression beyond G0

**Author:** Hainan Zhao  
**Scope:** Lane B for `G_(n,w)=P_n square P_w square P_w` and its abstract
surface-separator generalization.

This is a user-owned goal file. Do not edit, rename, or delete it without a
new explicit instruction from the user.

## Sealed starting point

Cycle 7 establishes outcome `G0` for the explicit nested checkerboard
embedding:

\[
\operatorname{rank}\operatorname{Flat}_{A|B}(\mathcal F_{n,w})
\le d_w,
\qquad d_w=2^{w^2-1},
\]

at every canonical pair and internal cut, before the Arf sum and for arbitrary
nonuniform edge weights.  Width three is exactly saturated.  Generic
arbitrary-width tightness is not proved.

The authoritative record is
`artifacts/cycle-7-b7-lane-b-arbitrary-width-closure-v1.json`.

No goal below changes the claim boundary: for cubic boxes `w=L`, the remaining
carrier is still `2^(L^2-1)`.  This campaign does not claim an exact cubic free
energy, critical temperature, critical exponents, or a solution of the
three-dimensional Ising model.

## Upgrade 1 — Prove G1

Prove, for every fixed `w`, that sufficiently long strips have generic
nonuniform canonical rank

\[
R_\infty(w)=2^{w^2-1}.
\]

Separate the already proved universal upper bound from the new lower bound.
Acceptable proof routes include:

1. a single exact nonuniform specialization with a nonzero
   `d_w x d_w` projected minor;
2. a unique extremal monomial of that determinant;
3. generic reachability and observability of the two separator maps;
4. an induction or block recurrence in `w`.

The proof must specify how large `n` must be, or give an explicit sufficient
bound `n_0(w)`.  A finite-field minor is proof of symbolic nonvanishing only
when the specialization, normalization, projected indices, pivot transcript,
and lifting argument are frozen.  Width-by-width experiments do not prove
G1.

Homogeneous anisotropic and isotropic tightness are separate stronger
questions.  A nonzero polynomial on the isotropic line proves only generic
isotropic tightness, not nonvanishing at every temperature or at criticality.

**Completion criterion:** a proof valid for arbitrary `w`, or a rigorous
countermechanism showing why the generic rank is smaller for a specified
infinite width family.

## Upgrade 2 — Abstract separator theorem

Extract the grid argument into a reusable theorem.

Target criterion: let a zero-field Ising graph embedded in an orientable
surface admit

1. a spatial filtration with separator `S`;
2. a filtration-adapted Lagrangian/canonical spin-structure basis;
3. right-exact representatives for emitted modes;
4. left-exact representatives for future modes;
5. gauge traces and polarization corrections that factor through the even
   separator mask.

Then the complete pre-Arf spin-structure tensor has an exact TT/MPS with

\[
\operatorname{rank}\operatorname{Flat}_{A|B}(\mathcal F)
\le 2^{|S|-1}
\]

at pair and internal cuts.

The theorem must define every hypothesis intrinsically, prove necessity or
identify which hypotheses are merely sufficient, handle affine quadratic
corrections, and state boundary conditions.  The grid-strip result must be a
formally checked corollary with `|S|=w^2`.

**Completion criterion:** a complete abstract proof plus at least one
meaningful graph family not identical to the cubic grid strips.  A restatement
of the grid proof with renamed objects is insufficient.

## Upgrade 3 — Nontrivial all-spin-structure algorithm

Implement and certify at least one operation that uses the complete all-`q`
TT rather than merely computing the physical partition function once.

Preferred operations include:

- all single-handle Walsh marginals;
- a batch of defect partition functions;
- contraction against arbitrary product-form spin-structure weights;
- selected Fourier coefficients of `F(q)`;
- batched periodic/antiperiodic sector combinations.

For the selected task, give an exact algorithm, proof of correctness, replay
on nontrivial strips, and an explicit complexity comparison between

\[
O(4^g\,\text{sector-evaluation cost})
\]

and a compressed cost of the form

\[
O(g\,\operatorname{poly}(2^{w^2})).
\]

Do not claim an advantage over ordinary transfer for computing only `Z`;
ordinary transfer already has the same separator dependence.

**Completion criterion:** one certified operation with an asymptotic
all-sector advantage and a concrete exact validation table.

## Upgrade 4 — Embedding robustness

Determine exactly how much of G0 depends on the nested checkerboard rotation.
Test and classify:

1. all embeddings satisfying the abstract filtration criterion;
2. canonical stabilizations by gauge-redundant handles;
3. alternative rotation systems for the same grid graph;
4. nonminimum-genus cellular embeddings;
5. changes of canonical basis, including transformations that preserve pair
   cuts but can alter internal cuts.

Distinguish invariant rank statements from coordinate artifacts.  Every
negative result must name the first failed hypothesis, embedding, canonical
cut, and exact phase or minor.

**Completion criterion:** either a proved robustness class containing more
than the checkerboard family, or a sharp counterexample showing which
geometric condition is essential.

## Execution order

1. Pursue Upgrade 1 first through a reachability/observability or
   unique-monomial argument; do not start with a dense `32768 x 32768`
   width-four matrix.
2. Develop Upgrade 2 alongside it only where the abstraction clarifies the
   lower-bound invariant.
3. Implement Upgrade 3 once the abstract core interface is stable.
4. Use Upgrade 4 as an independent structural audit, not as post-hoc evidence
   for G1.

## Epistemic and replay requirements

- Label every material claim `PROVED`, `CERTIFIED_NUMERICAL`, `OBSERVED`, or
  `CONJECTURED`.
- Preserve raw-coordinate and noncanonical failures in the failure ledger.
- Freeze every promoted exact computation with two primes where practical,
  all coordinate conventions, projected indices, determinant transcripts,
  code hashes, wall time, and peak memory.
- Do not infer an arbitrary-width theorem from finitely many widths.
- Do not infer thermodynamic control from fixed-width linear complexity.

## Terminal outcome

This upgrade campaign is complete only when all four upgrades have their
stated completion criterion, or when an individual upgrade is closed by a
proof-grade countertheorem explicitly allowed above.  G0 alone does not
complete this goal.
