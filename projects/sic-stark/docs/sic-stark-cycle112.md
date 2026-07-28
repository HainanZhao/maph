# SIC--Stark research cycle 112: cyclic quantum-dilogarithm frontier

Date: 2026-07-28

## Current primary source

Yalkinoglu's 2025 announcement rewrites Shintani invariants as limits of
cyclic quantum dilogarithms
([arXiv:2508.18320](https://arxiv.org/abs/2508.18320)).  Under its
length-one continued-fraction hypothesis, the theorem gives root-of-unity
approximants in Kummer extensions of cyclotomic fields.

This matches the dimension-six rational-boundary machinery unusually
well: the base unit

\[
 \beta=\frac{5+\sqrt{21}}2=[[5]]
\]

has length one, and cycles 64--68 already supply the singular
\(q\)-gamma corrections needed at the level-six characteristics.

## Exact limitation

The source explicitly presents itself as an announcement; the complete
proof is deferred.  More importantly, its result is a limit formula and
an approximation by Kummer extensions.  It does not prove that the
limit is algebraic, nor that the finite cyclic tables satisfy the AFK
twisted convolution identity.  Current descriptions of the program
continue to call algebraicity of Shintani invariants mysterious.

Therefore the source validates the chosen analytic machinery but does
not close the constant term:

\[
 \lim_n\bigl(K_{6,n}^2-K_{6,n}\bigr)=0.
\]

## Live proof target

After the descent audit, the most concrete unconditional route is:

1. place all \(36\) regularized level-six characteristics in the same
   cyclic quantum-dilogarithm algebra;
2. match the level-six Weyl phase with the coefficient mutation
   parameters in the cyclic pentagon identity;
3. prove the thirteen signed Zauner defect representatives have zero
   constant term; and
4. pass to the already controlled \(O(n^{-2})\) boundary limit.

The decisive missing object is thus not another scalar asymptotic.  It is
one finite operator identity compatible with both the cyclic pentagon
parameters and the AFK Weyl chirp.

## Status

\[
\boxed{\text{the cyclic route is structurally compatible and still
open; the available theorem supplies limits, not TCC cancellation.}}
\]

