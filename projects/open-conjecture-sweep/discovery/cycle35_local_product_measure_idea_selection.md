# Cycle 35 idea selection: coordinate-local product measure

## Brainstorm

1. **Factor the particular Cycle 34 witness.** Compute exact flattening and
   tensor-train ranks of its sparse coefficient tensor.
2. **Construct a rank-one local obstruction directly (chosen).** Seek local
   signed vectors \(u_i\) such that every uncovered predicate is killed in at
   least one coordinate while every local mass is nonzero. Then
   \(y(d)=\prod_i u_i(d_i)\) is a full-grid left-null signed measure and all
   global annihilations factor into local dot products.
3. **Degree-one monomial census.** Measure the enlarged column family before
   attempting elimination.
4. **Ownership auxiliaries.** Add semantic state only if a local analysis
   identifies the missing factor.

## Decision questions

- Idea 1: does this solver-selected sparse witness happen to have low exact
  ranks across coordinate cuts?
- Idea 2: do the finite local pattern matroids admit one mass-preserving
  annihilator hyperplane per coordinate whose killed-time sets cover every
  predicate?
- Idea 3: is positive-degree width materially smaller than the prior SAT
  interface?
- Idea 4: which local semantic factor, if any, is absent from direct masks?

## Questioning the questioning

The companion's proposed factorization question is structurally promising,
but the particular Cycle 34 witness was created by the first 1,228 modular
pivots and one target row. Its coefficient complexity can therefore reflect
row order rather than the mathematical obstruction. A high tensor rank for
that one vector would not refute a low-rank vector elsewhere in the large
left-null space.

The better question quantifies over the rank-one mechanism itself. For
\(F_t(d)=\prod_i b_{t,i}(d_i)\) and a product signed measure
\(y(d)=\prod_i u_i(d_i)\),

\[
\sum_d y(d)F_t(d)=\prod_i\langle u_i,b_{t,i}\rangle,
\qquad
\sum_d y(d)=\prod_i\langle u_i,\mathbf1\rangle.
\]

Thus the construction reduces exactly to a finite cover by local hyperplanes
that avoid the all-ones vector. This is a new local-to-global invariant, not a
larger replay of global elimination.

## Choice, rejected alternative, falsifier

Choose Idea 2. Enumerate the closed pattern spans avoiding the mass vector and
solve the resulting one-candidate-per-coordinate cover exactly. Reject Idea 1
because an arbitrary certificate is not a fair test of the mechanism; retain
it only as a later diagnostic.

A proposed product measure is falsified by any zero local mass, any predicate
with no annihilating coordinate, or any mismatch in the exact global product
check. A completed subspace enumeration plus exhaustive cover search can
prove this rank-one mechanism absent; a state or node cap cannot.
