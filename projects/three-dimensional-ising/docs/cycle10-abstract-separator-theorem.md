# Cycle 10 decision: abstract separator compression

`PROVED`: For a surface-embedded zero-field Ising even-subgraph model, if all
cross-cut character and quadratic phases factor through the attainable even
mask on a separator of size `k`, every canonical handle-pair flattening has
rank at most `2^(k-1)`.  If the active longitude also factors through that
mask (H3), the same bound holds at the binary cut inside the handle;
otherwise the general bound is twice as large.

`PROVED`: The Cycle 7 checkerboard grid family is a corollary with `k=w^2`
and H3, recovering binary bond `2^(w^2-1)`.

`PROVED`: Oriented edge-two-sum chains of explicitly rotated toroidal
`K_(3,3)` gadgets form a non-grid, unbounded-genus corollary.  Their
four-state handle-site bond is at most two and their binary-coordinate bond
is at most four for arbitrary nonuniform weights.

`PROVED`: The non-grid bounds are generically sharp for an infinite family.
Every nontrivial pair cut has generic rank two, while every non-end internal
handle cut has generic rank four.  A zero-port two-gadget minor and a
zero-port three-gadget minor embed unchanged at any selected cut after all
exterior edge weights are set to zero.  The latter remains rank four under
all 24 local affine symplectic relabelings.

`CERTIFIED_NUMERICAL`: Exact topology via independent cup-product and
tree-cotree routes, plus exact all-q tensors over two primes for one through
four gadgets, supplies the replayable base minors and validates the explicit
rotation and canonical local handles.

The result completes Upgrade 2's theorem-and-non-grid-family criterion.  It
does not prove G1, compress the physical area carrier, or imply a cubic
thermodynamic limit.
