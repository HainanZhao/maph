# Failure ledger: Cycle 6 / Gate B6.2

1. **KILLED:** `c=raw_new_b` completes the orthogonal new handle in the
   Cycle 4 recurrence.  Exact intersection pairing shows that `raw_new_b`
   pairs nontrivially with the old homology space.  The required correction is
   `c=old_second_last+raw_new_b`; `d=old_last+raw_new_a` was correct.

2. **KILLED:** ranks `480`, `512`, or larger obtained by applying the canonical
   quadratic form after only the `d` correction.  Those values used a
   non-symplectic coordinate system, so they are not ranks of the claimed
   Cimasoni `F` tensor.  The computations are preserved in session evidence
   but are excluded from promotion.

3. **KILLED:** the corrected canonical edge labels retain literal bounded
   four-bit support per slice.  Their raw support grows with the longitudinal
   position.  Every additional old-coordinate mode is, however, one of two
   exact transverse coboundaries; bounded locality survives only in
   `C^1/B^1`.

4. **CONTAINED:** the first corrected full replay reached 14,017,920 KiB peak
   RSS, violating the declared 8 GiB resource stop.  The arithmetic output is
   consistent but is not the canonical replay.  A gauge-reduced transfer
   absorbs all exact modes before caching; it is independently compared with
   the legacy engine on all 65,536 characters at `n=9` and must replay below
   the cap before sealing.

5. **SURVIVED:** after both symplectic corrections, the exact central rank
   sequence through `n=12` is `min(2^(n-1),256)` in the first full run for all
   three weight regimes, with an isotropic second-prime control.  Promotion
   remains conditional on the cochain factorization audit and compliant
   optimized replay.

6. **OPEN:** arbitrary-width closure.  Width three shows that nonlocal raw
   canonical labels can become local modulo coboundaries.  It is not yet known
   whether the analogous quotient leaves zero additional memory for every
   explicit `w` embedding, or whether an intrinsic `h(w)>0` appears.
