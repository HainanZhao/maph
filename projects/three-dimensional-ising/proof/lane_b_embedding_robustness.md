# Embedding and coordinate robustness of separator compression

## Claim boundary

`PROVED`: The separator bound is invariant under filtration-compatible
changes of embedding, gauge representative, and canonical coordinates as
specified below.  It is not invariant under an arbitrary rotation system or
an arbitrary symplectic mixing of handles across a declared TT cut.

`PROVED`: A connected cellular embedding has no homologically unused surface
handle.  A stabilization disjoint from the graph is gauge-redundant but is
necessarily noncellular.

`CERTIFIED_NUMERICAL`: Two explicit rotations of the same abstract `K_(3,3)`
graph give genus one and genus two, hence 4-entry and 16-entry pre-Arf
tensors, while their normalized Arf sums agree with direct even-subgraph
enumeration over two primes.

## 1. The robust class

Call two embedded filtrations equivalent when a surface homeomorphism carries
each left subgraph, right subgraph, labelled separator, and ordered handle
block of one to the corresponding object of the other.  Allow additionally:

1. changing any character cochain by a coboundary;
2. changing completion chains by relative boundaries;
3. changing the quadratic origin by an explicitly transported affine linear
   correction;
4. applying an invertible coordinate change separately inside the complete
   left and right handle blocks at each pair cut;
5. at an internal cut, applying only changes that preserve H3, equivalently
   whose cross-half phase still factors through the same separator trace.

`PROVED` (robustness theorem): Every member of this class has the same
separator upper bound.  A homeomorphism merely relabels partial chains and
masks.  Discrete Stokes turns a coboundary change into a diagonal sign indexed
by the boundary mask.  A completion change alters `Q_L,Q_R,kappa` by
left-only, right-only, and mask-only terms.  Affine quadratic corrections are
linear characters and are covered by H1.  Finally, invertible transformations
supported entirely on one side of a flattening multiply that matrix on the
left or right by an invertible matrix and preserve rank.  These operations
therefore preserve the factorization hypotheses and its rank bound.

This class strictly contains the single checkerboard rotation: it contains
all filtration-preserving homeomorphic images, all cochain gauges and
completion trees, and every rotation/embedding for which the intrinsic
relative-chain hypotheses H1--H3 can be checked.  The toroidal `K_(3,3)`
chains are a non-grid member for pair cuts, while their failure of H3 gives
the sharp internal factor-two boundary.

## 2. Stabilization and cellularity

`PROVED`: Stabilize the surface in a disk disjoint from `G`.  The image of
every graph cycle has zero coordinate in the new handle, so the pre-Arf
tensor is independent of its two new spin-structure bits:

```
F_stab(lambda,alpha,beta)=F(lambda).
```

The new four-state site is the rank-one vector `(1,1,1,1)` and creates no TT
overhead.  The normalized Arf sum is unchanged because

```
(1/2) sum_(alpha,beta) (-1)^(alpha beta)=1.
```

This stabilization is not cellular.  Indeed, for a connected cellular
embedding the graph is the one-skeleton of a CW decomposition of the surface.
The cellular chain complex gives

```
H_1(G;F_2) -> H_1(Sigma;F_2) -> 0,
```

so inclusion is surjective.  Consequently every surface handle is detected
by graph cycles.  A purported cellular “gauge-redundant handle” contradicts
this surjectivity; recellularizing the stabilization must add graph edges or
make the old graph use the new homology.

## 3. Coordinate limits

`PROVED`: Pair-cut rank is unchanged by any invertible relabeling of complete
handle sites wholly on one side of that cut.  Internal binary rank is not a
four-state-site invariant: a general affine symplectic relabeling mixes the
two binary coordinates and need not factor as independent row and column
operations.  Hence H3 must be rechecked after such a change.

The `K_(3,3)` chain makes the distinction sharp.  Its pair cuts have generic
rank two.  Every non-end internal cut has generic rank four, and the local
zero-port witness remains rank four under all 24 affine symplectic
permutations.  Thus that failure is not removable by choosing a prettier
canonical basis.

## 4. Arbitrary rotation systems are outside the robust class

Use bipartition vertices `0,1,2 | 3,4,5`.  The rotations

```
R_1: 0,1,2 -> (3,4,5); 3,4,5 -> (0,1,2),
R_2: R_1 except 5 -> (0,2,1)
```

have respectively three hexagonal faces and one length-18 face.  Euler's
formula gives genus one for `R_1` and genus two for `R_2`.  Therefore the
complete pre-Arf tensors have respectively `4` and `16` entries and cannot be
related by an invertible transformation within one fixed state space.

`PROVED`: This is an exact obstruction to embedding independence of the
pre-Arf family.  It does not affect the physical Ising polynomial: the
normalized Arf identity contracts either family to the same even-subgraph
sum.  The replay checks the topology, homology rank, and this physical
equality at independent nonuniform specializations over two primes.

## Classification

`PROVED`: G0 is robust for filtration-compatible embeddings and all declared
gauge/completion changes.  Gauge-redundant noncellular stabilization adds
rank one.  Arbitrary cellular rotation changes can change genus and the size
of the pre-Arf tensor.  Pair ranks are handle-site invariants under local
invertible changes; internal ranks require H3 and are genuinely
coordinate/filtration sensitive.

