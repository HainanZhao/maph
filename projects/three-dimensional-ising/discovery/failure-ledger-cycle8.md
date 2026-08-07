# Failure ledger: Cycle 8 / G1

1. **KILLED:** exact transverse coboundary potentials at one slice span all
   `w^2-1` frontier characters.  Their audited ranks are much smaller; G1 must
   use propagation and nonexact handle modes.

2. **RESTRICTED NO-GO:** rectangular longitudinal detours can form a
   homology-injective separator spanning tree.  Randomized common-independent
   searches plateau at ranks `6,11,22,31` for `w=3,4,5,6`, below
   `8,15,24,35`, and the plateau persists with added depth.  This kills only
   that rectangle ground set, not arbitrary separator trees or G1.

3. **OPEN:** whether the canonical conditioned transfer cores generate the
   full Weyl algebra on `V_w`.  The unconstrained physical generators
   `{X_v,Z_u Z_v}` do generate the full global-flip-even matrix algebra, but
   it remains to derive those generators from the canonical `q` alphabet.

4. **KILLED AS A VERIFIER:** replace a canonical moving co-core cut by an
   ordinary plane between longitudinal slices.  At `w=3,n=10` the exact
   prefix/suffix audit finds no plane satisfying the simultaneous
   past-on-right/future-on-left exactness conditions.  This does not refute
   Cycle 7: its separator moves through each checkerboard slab and around the
   co-cores.  It does show that a G1 partial-chain relation or minor must be
   built on those moved separators; a flat slice is not a faithful proxy.

5. **CORRECTED BEFORE PROMOTION:** an initial paired-fundamental-cycle search
   reported common rank eight at `w=3,n=10`, but independent reconstruction
   gave left rank seven.  The augmenting graph had its M1 and M2 exchange
   arcs reversed.  The witness is withdrawn; the corrected implementation
   asserts both projection ranks before returning any result.

6. **RESTRICTED NO-GO:** literal nesting of the exact width-four lifted-
   matroid witness into width five.  Under the deletion-compatible vertex
   inclusion and an aligned spatial slab, the fixed set has left/right lifted
   ranks `174/173`; hence it is already dependent in the right matroid.
   Contracting it and adding the requested 99 edges cannot repair that lost
   rank (the resulting union has lifted ranks `250/250`, not `273/273`).  This
   rejects witness-set nesting under that canonical transport, not the
   existence of an independent width-five witness; a separate exact
   width-five common-independent set of the target size exists.

7. **KILLED AS A CONSTRUCTION FAMILY:** keep all longitudinal rails and put
   one transverse spanning tree on each end slice.  Although this subgraph is
   connected with exactly `w^2-1` cycles, 200 random end-tree pairs at `w=3`
   attained simultaneous projection rank only 3 of 8, and 300 pairs at `w=4`
   attained only 5 of 15.  The missing homology must be injected at internal
   checkerboard slabs; endpoint encoders alone do not see the canonical
   handle modes.

8. **RESTRICTED NO-GO:** force every longitudinal rail and optimize all
   transverse edges by exact contracted matroid intersection.  The maximum
   transverse extensions are `14<16`, `26<30`, and `46<48` at widths
   `3,4,5`.  Allowing rail deletion is essential; this does not affect the
   unrestricted lifted-matroid witnesses.

9. **RESTRICTED NO-GO:** tile and longitudinally repeat one exact `3x3`
   single-handle tree gadget.  One slab captures the full available homology,
   but naive repeated copies do not add ranks blockwise: the ranks stabilize
   at 5 for width three and 12 (under the fixed orientation) for width five.
   Searching all eight transverse dihedral orientations per selected slab
   improves some rows but still misses the available rank (`7<8` at
   `w=3,q=6`, `19<24` at `w=5,q=6`).  The slab recurrence needs adaptive
   tree exchanges, not a fixed repeated gadget.

10. **KILLED AS A PROOF SHORTCUT:** identify the artificial zero-label
    terminal completion tree with parallel copies of a comb embedded in an
    interface collar, and use cographic dual-complement connectivity.  In the
    resulting explicit augmented ribbon rotations the complement is already
    disconnected at width four (97 of 105 dual faces reached), while the
    actual zero-label lifted matrix is independent.  A geometric parallel
    copy carries a cochain extension not equivalent to keeping the original
    edge labels fixed and assigning zero to every new completion edge.  Thus
    the ordinary tree--cotree criterion cannot replace the relative lifted
    calculation without first constructing the correct relative cochain
    extension.

11. **KILLED AS A TWO-SIDED G1 CONSTRUCTION:** glue the explicit arbitrary-
    width left prefix encoder to its longitudinal reflection across the
    middle slice of `G_(9,w)`.  The left prefix ranks are full at widths
    `4,5,6` (`15,24,35`), but in the same global canonical labeling the
    reflected-right ranks are only `7,12,15`.  Independent side gauges cannot
    be chosen simultaneously: their completion-cycle discrepancy changes the
    actual right character map and is not a mask-only diagonal.  The
    one-sided common-basis theorem remains valid, but it does not imply a
    flattening lower bound.  G1 now requires an independently constructed
    globally compatible right encoder or a different mechanism.

12. **KILLED AS A GLOBAL-INCLUSION SHORTCUT:** replace the reflected normal
    prefix by an explicit encoder for the opposite checkerboard phase.  The
    opposite local five-layer rotation is exactly the reflected right-hand
    rotation, and its terminal map has full local homology rank through width
    twenty.  Nevertheless, after inclusion into the high canonical handle
    block of `G_(9,w)`, the ranks at `w=4,5,6,7` are only `10,16,21,30`,
    below `15,24,35,48`.  Capping the half-surface and including it into the
    global surface do not induce the same homology quotient.  A local
    encoder theorem therefore does not supply the required global right
    factor without a proved inclusion lemma.

13. **RESTRICTED NO-GO:** put the proved normal encoder on the first five
    layers of `G_(11,w)`, the opposite-phase encoder on the last five layers,
    and join corresponding terminals by the two straight longitudinal edges
    through the middle layer.  The union is connected and has exactly
    `w^2-1` cycles, but its left lifted ranks are `186<190` at `w=4` and
    `288<298` at `w=5`.  Optimizing over every longitudinal and transverse
    edge incident to the middle layer while freezing both endpoint trees
    gives maximum connector sizes `28<32`, `40<50`, and `60<72` at widths
    `4,5,6`.  Thus a one-layer connector cannot repair the trace mismatch
    without exchanging endpoint-tree edges.  This rejects only the frozen
    two-encoder connector family, not the unrestricted lifted-matroid
    criterion or G1.

14. **RESTRICTED NO-GO:** freeze only the `w^2-1` explicit common-basis
    chords from each endpoint encoder and optimize all remaining graph edges.
    Exact contracted matroid intersection still falls short by `4,8,12`
    edges at widths `4,5,6`.  The endpoint chord bases themselves are
    simultaneously independent, but forcing both prevents a full global
    common basis.  Any arbitrary-width construction must allow coordinated
    exchanges in the homology-bearing chords, not only in their spanning
    trees or connector.
