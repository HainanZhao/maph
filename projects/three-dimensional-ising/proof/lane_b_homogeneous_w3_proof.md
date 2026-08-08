# Homogeneous width-three paired-cycle minor

## Claim boundary

`PROVED`: the exact `256 x 256` Cycle 8 paired-cycle minor for the canonical
cut after handle five of `G_(10,3)` is a nonzero polynomial after restriction
to `Z[tx,ty,tz]`, and its further restriction to `Z[t]` is nonzero.

This proves generic rank 256 on the width-three homogeneous anisotropic locus
and outside a finite algebraic exceptional set on the isotropic line.  It
does not prove nonvanishing at every physical temperature, at the critical
temperature, or for arbitrary width.

## Frozen minor

The edge ordering, spanning tree, chords, handle cut, and selected dual
coordinates are imported unchanged from
`proof/verify_g1_paired_cycle_w3.py`.  In particular, the rows are not chosen
after homogeneous specialization.  The character transfer uses the universal
checkerboard embedding, applies the exact inverse Walsh transform into cycle
homology, multiplies by the canonical quadratic sign, and applies the forward
Walsh transform into the pre-Arf tensor.  The same affine canonical reindexing
as Cycle 8 is then applied.

## Degree bounds

`G_(10,3)` has 81 longitudinal edges and 60 edges in each transverse
direction.  Thus every tensor entry has multidegree at most `(81,60,60)`.
A 256-dimensional determinant has multidegree at most
`(20736,15360,15360)`.  On the isotropic line it has degree at most
`256*(81+60+60)=51456`.

## Exact nonvanishing

For each of the primes 1,000,000,007 and 1,000,000,009, exact modular
spin-slice transfer and exact elimination were run at the preregistered
anisotropic points `(2,3,5)`, `(7,11,13)`, `(17,19,23)` and isotropic points
`t=2,3,5`.  All twelve determinant residues are nonzero.  The artifact stores
the pivot rows, pivot values before normalization, row swaps, canonical tensor
hash, coordinate sets, source hash, and normalization audit.

A nonzero modular value is the image of the integer-polynomial determinant
under a ring homomorphism, so it proves the restricted polynomial is not
identically zero.  Combining this with the polynomial grid upper bound gives
rank exactly 256 wherever the determinant is nonzero.  A nonzero real
polynomial cannot vanish throughout the physical anisotropic cube.  The
isotropic exceptional set is

    E = {t in C : D_iso(t)=0},

and has cardinality at most 51456.  The physical conclusion is therefore
"outside a finite exceptional set," not "at every temperature."

## Replay

    python3 proof/build_cycle14_homogeneous_w3.py --check

The finite calculation proves nonidentity of this finite determinant.  It is
not used as a substitute for any arbitrary-width argument.
