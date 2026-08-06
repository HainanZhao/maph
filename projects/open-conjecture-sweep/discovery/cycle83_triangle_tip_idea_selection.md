# C83 idea selection: LEM triangle-tip interval

## Primary assessment

`PROVED` C81 reduces the first possible spectrum disagreement to length four;
`PROVED` C82 excludes only one 15-element modular realization.  In any full
cycle
\[
  x\to y\to z\to w\to x,\qquad x<y,
\]
linear-extension event containment forces the two chords \(x\to z\) and
\(w\to y\).  Proposition 7's triangle restriction then makes the two forced
triangles \(x\to z\to w\to x\) and \(y\to z\to w\to y\) incomparable-only.
Thus a counterexample must realize two incomparable triangles sharing an edge,
with their remaining tips ordered.  This reduction is an exact consequence of
the fixed conventions; it is not yet a proof that the configuration is
impossible.

## Question the question

The inherited question "find a 15-element realization" assumes construction
is the bottleneck.  C82's miss shows that a symmetric module substitution is
not an adequate proxy for uniform linear extensions.  But proving that ordered
tips cannot occur may be equally misleading: a configuration can occur and
still force a different incomparable 4-cycle elsewhere.  The discriminating
question is therefore whether the *ordered-tip fiber* has a uniform-extension
identity/injection that either produces an incomparable 4-cycle or yields a
small exact countermodel.

## Candidate comparison

1. **Triangle-tip interval identity (selected).** Condition the extension set
   on the relative positions of ordered tips \(x<y\) and the shared edge
   \(z\to w\); seek an injection between the complementary pair-ordering
   events or an order-ideal convolution identity.  It preserves uniformity and
   the actual poset order.  An exact poset realizing ordered tips with no
   restricted 4-cycle falsifies the engine.
2. **Marked ideal-flow cone (deferred).** Its rational flow dual could be
   exact after an integrality/lift theorem, but absent that bridge it risks
   reproducing C81's abstract ranking countermodel.
3. **Fresh poset census (rejected).** Gupta's order-14 census already supplies
   this bounded evidence; enlarging it does not expose the needed mechanism.

## Oracle comparison and decision

Oracle independently ranked the selected interval mechanism first: medium
cost, high information gain, and a direct path to closing the length-four
bridge.  It identified the strongest flaw as possible over-focus on the
ordered-tip configuration, and ranked a fresh portfolio screen second and the
flow cone third.  Its stop/pivot criterion is one cycle: pivot if no explicit
invariant/injection or exact countermodel emerges.

**Decision:** preregister the triangle-tip interval identity with a smallest
exact symbolic/order-ideal gate.  Do not widen C82, perform a census, or use a
relaxation without an exact realizability bridge.

## Post-control refinement

The frozen C81/C82 tip-gap control establishes only the partition identities;
it supplies no inequality.  The next candidate is **interval-conditioned
majority inheritance**: for (x<y), test whether a global arrow (z	o w)
must remain a strict majority after conditioning uniform linear extensions on
(xprec z,wprec y).  If true under the ordered-tip hypotheses, it offers a
direct injection target for the shared triangle edge.  If an exact frozen
control reverses the sign, the conditional-inheritance engine is falsified;
the unconditional pair margins then cannot simply be localized to the tip
interval.  This is a distinct order-ideal/fiber invariant, not a rank-pattern
inequality or a new-poset census.

## Post-result pivot

`PROVED` exact controls found 30 conditional sign reversals, so simple
interval-conditioned majority inheritance is closed.  The next
`CONJECTURED` engine is an **extension-graph interval pairing**: restrict the
adjacent-incomparable-swap graph of linear extensions to a marked tip fiber
and seek a pairing that exchanges the relative order of the shared vertices
while preserving its outside prefix/suffix.  A frozen fiber with an exact
component or boundary imbalance falsifies a proposed pairing; no census is
authorized.
