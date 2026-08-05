# Cycle 6 forbidden-triple hypergraph argument

## Claim boundary

This gives a necessary completion condition inside the frozen finite cyclic
cover model. It does not assert that weak colorability is sufficient for a
translate cover, or any claim about (J(13,199)), (LRC(13)), lifting, or
higher arities.

Let (Bsubseteq H) be the frozen bad-time set. Define the 3-uniform
hypergraph (F) on (H) by putting ({u,v,w}) in (F) precisely when no
center (xin H) has (u,v,win B-x). For a partial state, let (W) be its
uncovered times and let (r) be its number of remaining centers.

**Lemma.** If (W) can be covered by (r) translates of (B), then the
induced hypergraph (F[W]) is weakly (r)-colorable.

**Proof.** For each (uin W), choose one of the (r) covering translates
and color (u) by its index. If an edge ({u,v,w}) of (F[W]) were
monochromatic, its three vertices would belong to the same translate
(B-x). This contradicts the definition of a forbidden triple. Hence every
edge is non-monochromatic. ∎

Consequently, an exact proof that (F[W]) is not weakly (r)-colorable is a
sound non-completability certificate. The implementation prunes only on that
result, and independently rechecks every forbidden triple involved. A found
coloring or a search-cap result retains the state. For (r=1), it directly
checks whether a common covering center exists, because absence of a
forbidden triple is not sufficient for a common center for arbitrary (W).

If the global (F) admits a verified weak 2-coloring, restricting it to any
(W) proves weak (r)-colorability for every (rge2). In that case this
specific cut is structurally vacuous at all multi-center states.
