# Cycle 49 soundness: contraction by diagonal fibers

## State and invariant

Let (S_0,S_1,S_2) be finite owner supports.  A pair-diagonal fiber is

\[
 F_{ij}(w)=\{x:x_i=x_j=w\}.
\]

An alternating (2\times2\times2) cube has zero marginal on every coordinate
pair.  Thus every packet below preserves the three pair marginals exactly.

`PROVED`: if the (ij) pair diagonal at (w) is deleted, then every admissible
input tensor has

\[
 \sum_{x_k\in S_k}T(w,w,x_k)=P_{ij}(w,w)=0.
\]

This zero fiber total, rather than an isolated pivot coefficient, is the
contraction invariant.

## Triple-intersection packet

At a forbidden triple cell ((w,w,w)), choose pairwise distinct alternatives
(a_i\in S_i\setminus\{w\}).  The alternating cube on
({w,a_0}\times{w,a_1}\times{w,a_2}) has no other triple cell.

`PROVED`: its only possibly forbidden vertices besides ((w,w,w)) are
((w,w,a_2)), ((w,a_1,w)), and ((a_0,w,w)), according as the corresponding
pair diagonal at (w) is deleted.  Every remaining vertex has three distinct
owner labels.  Scaling this cube kills the triple coefficient and moves its
effect into the incident pair fibers without changing any pair marginal.

## Pair-fiber packet

Fix a nontriple pivot in (F_{ij}(w)), with complementary coordinate (c).
Choose a terminal (t\ne w,c) in the complementary support and buffers
(a\in S_i,b\in S_j) so that (w,c,t,a,b) are pairwise distinct.  The
corresponding cube contains exactly two forbidden vertices: the pivot and the
terminal cell in the same (F_{ij}(w)) fiber.

`PROVED`: all six other vertices have three distinct owner labels, so no pair
or triple diagonal can delete them.  A scaled packet transfers the pivot
coefficient to the terminal without spill into another stratum.  Repeating
this for all nonterminal cells leaves only the terminal coefficient.  It is
zero because it equals the unchanged fiber total (P_{ij}(w,w)=0).

## Sufficient support theorem

`PROVED`: if every (|S_i|\ge5), the required buffers exist.

- After deleting (w), each of the three triple-buffer lists has at least
  four elements.  Three such lists admit distinct representatives: every
  one- or two-list union has size at least four, and the three-list union has
  size at least four, so Hall's conditions hold.
- Choose any terminal (t\in S_k\setminus\{w,c\}) when (c\ne w), and any
  (t\in S_k\setminus\{w\}) for the triple leaf.  An active support contains
  an (a) outside ({w,c,t}); the other active support contains a (b)
  outside ({w,c,t,a}), because it has at least five elements.

Consequently the frozen two-stage algorithm contracts every forbidden tensor
whose deleted pair marginals vanish whenever all three supports have size at
least five.  The proof is a formula using cube packets and fiber sums; it is
not Gaussian elimination.

## Full p199-domain classification

`PROVED` by the principal exact audit and a separately implemented reverse-
order full residual reconstruction: there are 382,453,319 raw-multiplicity-
valid unordered p199 type triples.  The symbolic support theorem closes
340,918,175.  Exact
pair-deletion signatures close another 29,326,638 without inspecting a
Möbius tensor.  Of the remaining 12,208,506 triples, 3,070,480 satisfy the
correlated structural buffers, 9,138,020 have no forbidden Möbius coefficient,
one uses two frozen packet moves successfully, and five reach
`BUFFER_INCOMPLETE`.  Thus the preregistered formula closes exactly
382,453,314 of 382,453,319 type triples; it is not a universal theorem.

`PROVED`: the first exceptional triple, types `(4,4,5)` with supports
`({9,10},{9,10},{9,12})`, is not a relative-homology obstruction.  Its cube
kernel is one-dimensional, and the unique full-support alternating cube with
alternatives `(10,10,12)` cancels all three forbidden coefficients exactly.
The frozen triple-buffer rule rejected this cube only because its alternatives
are not pairwise distinct; its alternative triple is nevertheless allowed.
This classifies the result as `BUFFER_INCOMPLETE`, not
`TERMINAL_OBSTRUCTION`.  The independently confirmed exception labels are
`(4,4,5)`, `(4,4,6)`, `(4,4,64)`, `(4,5,35)`, and `(4,6,35)`.  The other four
have not been promoted beyond exact `BUFFER_INCOMPLETE` classifications.

## Controls and boundary

`PROVED` by exact finite controls: 7,680 triple-packet support cases, 2,520
pair-packet support cases, and 1,296 support-five buffer cases pass on owner
universes of sizes five and six.  A repeated-buffer injection creates the
predicted cross-stratum spill.  A support ((1,1,2)) state with zero 01-fiber
total has a nonzero forbidden defect and zero cube-kernel dimension, giving an
exact negative terminal class.

The generic theorem plus two full residual routes leaves five explicit
exceptional interfaces.  The first is exactly fillable beyond the frozen
formula; the remaining four are not claimed fillable or obstructed.  Even a
future universal face contraction would not define the next lift or prove
LRC(13).
