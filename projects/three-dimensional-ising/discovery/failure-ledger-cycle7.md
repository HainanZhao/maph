# Failure ledger: Cycle 7 / arbitrary-width canonical closure

1. **KILLED:** slice-wise exactness of every `b` cochain implies exactness on
   every longitudinal prefix.  The exact prefix audit finds nonzero prefix
   cohomology already at `w=3`.  Prefix exactness is stronger than necessary;
   the valid gluing condition is two-sided and tied to the moving canonical
   separator.

2. **KILLED:** a filtration-adapted symplectic basis alone is a safe basis for
   binary spin-structure cuts.  At `w=3,n=10`, applying the standard quadratic
   form directly in the pinned raw coordinates gives central rank `512`
   modulo `1,000,000,007`.  After the full atomic canonical transport and its
   quadratic affine audit, the same tensor has central pair/internal/pair
   ranks `256,256,256`.  The raw `512` is a coordinate artifact, not a G3
   obstruction.

3. **KILLED:** the long edge support of the first atomic basis disproves local
   handle attachment.  Taking plaquette curls shows that each atomic class is
   nonexact only in one adjacent two-slice window.  For `w<=8` in the exact
   audit, these window spaces are a direct sum of total dimension equal to the
   surface genus.

4. **CONTAINED:** the finite audit `w<=8` is not the arbitrary-width proof.
   Promotion instead uses the explicit checkerboard co-core disk system and
   the separator lemma; the finite computation is only a coordinate firewall
   and regression test.

5. **OPEN:** generic tightness for arbitrary `w`.  Width three is certified
   tight.  The `w=4,n=4` tensor reaches rank `32`, the largest allowed by its
   ten available binary spin-structure coordinates, but this is far below the
   carrier cap `d_4=32768`.  No area-exponential lower theorem is inferred.
