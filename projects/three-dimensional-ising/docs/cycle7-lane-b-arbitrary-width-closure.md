# Lane B arbitrary-width canonical closure

## Outcome first

`PROVED` (G0): for the explicit nested checkerboard ribbon embedding of
`G_(n,w)=P_n square P_w square P_w`, the complete tensor of Cimasoni
square-root values over all spin structures has an exact binary-coordinate
TT/MPS with bond

```
d_w = 2^(w^2-1).
```

The bound holds at pair cuts and inside every canonical handle.  No Arf sum is
performed before the TT is built.  Arbitrary nonuniform edge weights are
allowed.

`CONJECTURED`: generic tightness `R_infinity(w)=d_w` for every `w`.  It is
proved at `w=3`, not at arbitrary width.

This is not a solution of the cubic model.  Setting `w=L` leaves bond
`2^(L^2-1)`.

## Structural mechanism

The embedding comes from the oriented boundary of a checkerboard union of
unit cubes, restricted from the next-even box.  Its transverse checkerboard
plaquettes form a complete system of co-core disks.  Their boundary classes
are a nested Lagrangian in surface homology.  A deterministic symplectic
extension supplies the conjugate `b` cycles.

Moving a separator through those one-handles meets exactly `w^2` graph
strands.  A partial even subgraph therefore exposes only an even mask in

```
V_w={m in F_2^(w^2): |m| even}.
```

Coboundary phases evaluate on that mask by discrete Stokes.  Halfway through
a handle, the remaining `b` phase is already frontier-known, so splitting
`a_i|b_i` introduces no factor two.  This gives the factorization

```
Flat_(A|B)(F_(n,w)) = X_(A,w) Y_(B,w)
```

with shared index exactly `m in V_w` at every canonical cut.  The complete
construction, quadratic refinement, boundary conventions, cores, and
complexity statement are in
`proof/lane_b_arbitrary_width_closure_proof.md`.

## Explicit embedding genus

With `p=floor((w-1)/2)`, the constructed genus is

```
g(n,2)=0,
g(n,2p+1)=p^2(n-1),
g(n,2p)=sum_(i=0)^(n-2) r_i,
r_i=(p-1)^2 for even i and p^2-1 for odd i.
```

The embedding is minimum genus when `n,w` are even, since it is
quadrangular and attains the bipartite Euler lower bound.  Minimum genus for
the remaining parity cases is not required and is not claimed, except for
the separately audited `w=3` theorem.

## Exact validation

The coordinate firewall was run over `2<=w,n<=6`, then stressed at `w=7,8`
through `n=4`.  In every case:

- `S^T Omega S=J` exactly over `F_2`;
- quadratic polarization and Arf invariance hold;
- the explicit checkerboard meridians have rank `g` and zero mutual
  intersection;
- every transverse `b` mode is a coboundary;
- the adjacent two-slice window spaces form a direct sum of rank `g`;
- atomic normalization leaves at most one nonexact `a` class on an edge.

The observed window ranks agree with the proved formulas:

| `w` | successive window ranks |
|---:|:---|
| 2 | `0,0,...` |
| 3 | `1,1,...` |
| 4 | `1,3,1,3,...` |
| 5 | `4,4,...` |
| 6 | `4,8,4,8,...` |
| 7 | `9,9,...` |
| 8 | `9,15,9,15,...` |

Two-prime finite-field rank certificates use `1,000,000,007` and
`1,000,000,009`, with all selected denominators invertible.

| shape | weights | canonical binary rank profile (both primes) |
|:---|:---|:---|
| `10x3x3` | nonuniform | `2,4,8,16,32,64,128,256,256,256,128,64,32,16,8,4,2` |
| `10x3x3` | anisotropic `(2,3,5)` | same |
| `10x3x3` | isotropic `t=2` | same |
| `4x4x4` | nonuniform | `2,4,8,16,32,16,8,4,2` |
| `4x4x4` | anisotropic `(2,3,5)` | same |
| `4x4x4` | isotropic `t=2` | same |

Each central lower bound records rank-revealing rows and columns, a replayable
LU transcript, and a nonzero determinant.  Width four has only ten homology
bits at this size, so rank `32` is not saturation of `d_4=32768`.

The existing small-graph verification suite independently compares direct
spin enumeration, cycle-space enumeration, domain walls, Kac--Ward values,
and transfer evaluation.  The new firewall adds the arbitrary-width
embedding and coordinate maps; it does not replace those checks.

## Coordinate failure that was rejected

At `w=3,n=10`, the pinned raw coordinate tensor has apparent central
internal rank `512` modulo the primary prime.  After applying the full
raw-to-canonical symplectic and quadratic transformation, the exact central
pair/internal/pair ranks are `256,256,256`.  The raw value is therefore a
coordinate artifact.  It is preserved in
`discovery/failure-ledger-cycle7.md` and is not promoted as an obstruction.

## Complexity and supported operations

There are `O(nw^2)` binary cores of size at most `d_w x d_w`.  For fixed `w`,
the representation and contractions are linear in `n`.  It supports one
spin-structure evaluation, Arf-weighted contraction, partial sums, Walsh
projection, and fixed twist legs.  Explicitly outputting all `2^(2g)` values
still takes exponential output time.

## Novelty boundary

The generalized Kac--Ward theorem supplies the Arf-weighted sum of
`2^(2g)` square roots, but not this simultaneous TT compression.  Standard
bounded-treewidth Ising dynamic programming supplies the physical frontier,
but does not by itself identify the canonical spin-structure gauge quotient
or the internal-handle factorization.  The new claim is exactly their bridge:
surface genus creates no bond overhead beyond the ordinary frontier in this
explicit nested embedding.

A full paper-level priority claim remains conditional on theorem-by-theorem
comparison with the surface-Arf, bounded-pathwidth, and tensor-network gauge
literature.
