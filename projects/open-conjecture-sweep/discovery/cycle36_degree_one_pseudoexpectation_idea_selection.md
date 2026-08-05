# Cycle 36 idea selection: degree-one pseudoexpectation

## Brainstorm

1. **Raw degree-one column elimination.** Form every
   \(x_{i,a}F_t\) column and test whether their rational span contains one.
2. **Rank-one degree-one pseudoexpectation (chosen).** Generalize Cycle 35's
   exact local-span CSP to seek a mass-one product functional annihilating
   every direct predicate and every coordinate-indicator multiple.
3. **Transfer the Cycle 35 normals to all 60 survivors.** Test breadth before
   understanding the mechanism.
4. **Add ownership auxiliaries.** Enlarge the semantic algebra now.

## Decision questions

- Idea 1: does a large degree-one matrix contain a certificate? This measures
  solvability but obscures why.
- Idea 2: can every multiplier constraint be killed locally by an ordinary
  contraction in another coordinate or by forcing the multiplied local entry
  of the normal to zero?
- Idea 3: is there a proved residue transport law for the normals, rather than
  60 independent target searches?
- Idea 4: which escaping multiplier type demonstrates that ownership is the
  missing semantic?

## Questioning the questioning

The obvious primal question—“does degree one prove the leaf?”—would recreate a
large linear system before using the strongest new information. Cycle 35 gives
a functional, so the discriminating question is whether it extends one degree
further. For coordinate indicators \(x_{i,a}\),

\[
L(x_{i,a}F_t)=u_i(a)b_{t,i}(a)
\prod_{j\ne i}\langle u_j,b_{t,j}\rangle.
\]

This vanishes if the local predicate entry is already zero, if another
coordinate kills \(F_t\), or if \(u_i(a)=0\). Each option is an exact local
linear condition. The global degree-one question therefore remains a finite
mass-avoiding matroid cover, not an uncontrolled monomial expansion.

## Choice, rejected alternative, falsifier

Choose Idea 2. Reject raw elimination until this structured dual is
classified. Defer cross-leaf transfer because no CRT transport theorem for the
normals is proved, and defer ownership until an escaping constraint points to
a specific missing local semantic.

A proposed pseudoexpectation is falsified by any local mass different from
one or any generator \(F_t\) or \(x_{i,a}F_t\) with nonzero product
contraction. An exhaustive no-go is falsified by any omitted feasible local
equation or memo/branch collision. A cap makes no algebraic claim.
