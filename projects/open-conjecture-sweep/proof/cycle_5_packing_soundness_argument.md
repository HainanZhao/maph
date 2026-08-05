# Cycle 5 uncovered-time packing argument

## Claim boundary

This lemma certifies one non-completability cut inside the finite cyclic-cover
engine. It does not imply that every non-completable state has such a witness,
or any (J(13,199))-empty or Lonely Runner claim.

Let (B\subseteq H) be the frozen bad-time set. Two times (u,v\in H) can be
covered by one center (x) only if both lie in (B-x), hence
(u-v\in B-B). For an uncovered set (W), join (u,v\in W) when
(u-v\notin B-B). Call a clique in this graph an incompatible packing.

**Lemma.** If (r) centers remain and (W) contains an incompatible packing
of size (r+1), the partial state cannot be completed.

**Proof.** Suppose (r) additional translates cover (W). Assign each of the
(r+1) packed times to one translate covering it. Two assigned times share a
translate by the pigeonhole principle. Their difference must then belong to
(B-B), contradicting that every pair in the packing is incompatible. ∎

The executable cut searches only when (r\le5). It may fail to find a
witness and retain a non-completable state; that affects speed only. It prunes
only after rechecking that the witness has (r+1) distinct uncovered vertices
and that every pair difference lies outside (B-B). Thus a search-order or
backtracking miss cannot create a false prune.
