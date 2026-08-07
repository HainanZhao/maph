# Stage 1: what actually breaks between two and three dimensions

## Claim boundary

`PROVED`: The finite-graph high-temperature and low-temperature identities
below hold in every dimension and for the pinned free, periodic, and
antiperiodic conventions. `PROVED`: the standard surface
Kac--Ward/Fisher--Kasteleyn compression requires exponentially many
spin-structure terms on free cubic boxes when used without an additional
collective reduction. `PROVED`: ordinary ordering-based fermionization and
ordinary scalar self-duality lose the properties that close the 2D solution.

Not proved: that every exact 3D representation is exponentially large, that
intersections or knots are a universal obstruction, that no commuting family
exists, that the thermodynamic limit is controlled, or that any critical
quantity has been determined. The three-dimensional Ising model is not
solved.

Here `COMPUTATIONALLY VERIFIED` denotes an exhaustive exact-integer finite
check; those particular finite statements also meet the repository's
`PROVED` standard. Nonrigorous patterns would be tagged `OBSERVED`, but none
is promoted here.

## 1. Exact identities that do not fail in 3D

Let `G=(V,E)` be a finite graph, let `eta_e in {+1,-1}` encode a periodic or
antiperiodic seam, and put

```text
Z_G(K;eta) = sum_{sigma in {+1,-1}^V}
             exp(K sum_{e=uv} eta_e sigma_u sigma_v).
```

Write `t=tanh K`. Expanding
`exp(K eta_e sigma_u sigma_v)=cosh(K)(1+t eta_e sigma_u sigma_v)`
and summing each spin independently gives

```text
Z_G(K;eta)
 = 2^|V| cosh(K)^|E|
   sum_{A subset E : partial A=0 mod 2}
   t^|A| product_{e in A} eta_e.                         (HT)
```

`PROVED`: this is an algebraic identity on every finite graph. The surviving
objects are mod-2 **one-cycles** (even subgraphs), in 3D just as in 2D. It is
therefore inaccurate to say that the high-temperature loops themselves turn
into surfaces in three dimensions.

For `q=exp(-2K)`, let
`D_eta(sigma)={e=uv : eta_e sigma_u sigma_v=-1}`. Since the energy exponent
is `|E|-2|D_eta(sigma)|`, fixing one root spin on each connected component
removes only global spin flips and gives

```text
Z_G(K;eta)
 = 2 e^(K|E|) sum_{S subset V, root notin S}
   q^|delta S symmetric-difference T|,                  (LT)
```

for a connected graph, where `T={e:eta_e=-1}`. `PROVED`: this is the exact
cut/twist-coset form. On a cubic cellulation with a flat seam twist, dual
plaquettes to `D_eta` meet every dual edge an even number of times, because
the product of bond variables around each primal square is `+1`. Thus the
low-temperature objects are mod-2 closed domain-wall surfaces (relative
surfaces at a free boundary).

`PROVED`: changing spins by `sigma_v -> g_v sigma_v` changes `eta` only by a
cut and leaves `Z` invariant. Hence on a torus the physically distinct seam
data are cohomology sectors, not arbitrary seam placements.

`COMPUTATIONALLY VERIFIED` (exact exhaustive check): spin enumeration, (HT)
cycle-space enumeration, and (LT) cut-coset enumeration agree coefficient by
coefficient on free `2x2x2` and `2x2x3` boxes; a `3x2x2` box with a periodic
or antiperiodic wrap; and periodic/twisted `3x3x1` reductions. Replay:

```bash
python3 proof/verify_stage1_baseline.py
```

For example, the normalized high-temperature polynomial for the free cube is

```text
1 + 6 t^4 + 16 t^6 + 9 t^8.
```

`PROVED`: for every finite real `K`, the original spin sum is positive and is
an entire finite sum of exponentials in complex `K`. Negative coefficients in
a twisted high-temperature polynomial are therefore harmless intermediate
signs, not negative physical weights.

## 2. The planar determinant/Pfaffian mechanism

For a planar embedded graph, turning phases on oriented nonbacktracking edges
make the signed closed-walk expansion cancel unwanted intersections. The
result is one chosen square root of a determinant of a `2|E|`-dimensional
Kac--Ward matrix. Equivalently, Fisher's local decoration converts even
subgraphs to dimers and a Kasteleyn orientation evaluates the planar dimer sum
by one Pfaffian. Cimasoni's Theorem 2.1 proves both mechanisms are instances of
the same spin-structure formula; see the [source audit](../discovery/stage1-source-audit.md).

The genuine obstruction is not that edges cross in a drawing in `R^3`.
Kac--Ward phases live on a **two-dimensional oriented surface**. For a graph
embedded in a genus-`g` surface, the exact formula is an Arf-weighted sum over
all `2^(2g)` spin structures. Planarity is `g=0`, so there is one term. A 2D
periodic lattice embeds on a torus with `g=1`, so four terms suffice
independently of lattice size.

Now let `G_L` be the free `LxLxL` cubic graph. It is simple, bipartite, and
bridgeless for `L>=2`. In any cellular embedding in an orientable surface,
every face has length at least four, so `4F <= 2E`. Euler's formula gives

```text
2 - 2g = V - E + F <= V - E/2,
g >= 1 - V/2 + E/4.
```

With `V=L^3` and `E=3L^2(L-1)`, this becomes

```text
g(G_L) >= ceil(1 + (L^3 - 3L^2)/4) = Omega(L^3).
```

`PROVED`: inserted directly into the generalized Kac--Ward formula, this is
at least

```text
2^(2g) >= 2^(2 + (L^3 - 3L^2)/2)
```

determinant/Pfaffian terms before any new cancellation or symmetry reduction.
The exact formula therefore survives, but its planar computational reduction
does not. This is a scoped obstruction to the standard term-by-term surface
formula—not a no-go theorem for a Fourier transform over spin structures, a
higher-form determinant, or a special collapse at uniform coupling.

## 3. Transfer matrices and free fermions

A transfer step always survives. For an `LxL` layer, the exact transfer matrix
has dimension `2^(L^2)`, already exposing the area-width cost. The 2D classical
model is special because its transfer row is one-dimensional: after the
Kaufman/Jordan--Wigner construction, the relevant operators lie in the Lie
algebra of quadratic Majorana forms. Products act by finite-dimensional
orthogonal transformations, Fourier modes pair, and the spectrum reduces to
independent free fermions.

For a 3D transfer plane, choose any one-dimensional ordering of its `L^2`
spins. The layer has `2L(L-1)` nearest-neighbour edges, whereas an ordering
has only `L^2-1` consecutive pairs. For `L>=2`, some interacting pairs are
nonconsecutive. Under the ordinary Jordan--Wigner map those terms carry the
intervening fermion-parity string. `PROVED`: the naive transformed layer is
therefore not a local collection of quadratic nearest-neighbour terms, and
the 2D free-fermion diagonalization does not close in the same algebra.
Schultz--Mattis--Lieb explicitly identify this ordering restriction in their
Section VI.

What this does **not** prove is that fermions are useless. A local 2D
fermionization can trade parity strings for gauge fields or constraints. That
possibility is a Stage 2 direction, provided the enlarged state space is
actually reduced rather than hidden.

## 4. Domain walls: local ambiguity versus true obstruction

At a dual edge of the cubic lattice, zero, two, or four selected domain-wall
plaquettes may meet. Four plaquettes define an unambiguous mod-2 2-cycle but
not a unique pairing into locally smooth sheets. Different resolutions can
change connectedness and genus. `PROVED`: a representation that assigns a
weight depending on resolved components or genus must therefore add pairing,
framing, or equivalent local data and prove independence or the correct sum
over resolutions.

The fourfold meeting itself is not an impossibility theorem. The original
spin configuration already supplies a valid mod-2 boundary, and local
auxiliary data might encode its resolutions. Likewise, knotting is not the
source of failure of identity (HT) or (LT); it becomes relevant only when a
candidate weight depends on an embedding invariant.

## 5. Duality changes the kind of variables

In two dimensions, primal bonds are dual to bonds. The low-temperature
contours of one scalar Ising model match the high-temperature loops of another
scalar Ising model, up to finite-volume sector bookkeeping. This same-type
duality, combined with further analytic input, helps locate the square-lattice
critical point.

In three dimensions, a primal bond is dual to a plaquette. Wegner duality maps
the nearest-neighbour Ising model to a `Z2` lattice gauge theory with plaquette
interactions, with dual couplings conventionally related by
`exp(-2K*)=tanh K`. On a torus, one must also match or sum the correct flux and
twist sectors. `PROVED`: ordinary duality is not a scalar Ising self-duality,
so there is no same-model fixed-point equation from this step alone.

Again this is a type change, not a dead end. Gauge constraints may be exactly
the local language needed for surface topology; Stage 2 must demand more than
the formal dual partition sum.

## 6. Integrability and complexity: what is not established

The ordinary Yang--Baxter equation organizes commuting row-to-row transfer
matrices for many 2D models. A 3D classical model has a two-dimensional layer
operator, so copying the same equation is not a complete integrability test.
`PROVED`: failure to find an ordinary Yang--Baxter/free-fermion closure is not
a theorem excluding tetrahedron equations, higher commuting structures, or
noncommutative spectral data.

Published hardness results are also easy to overstate. The checked 3D
reductions encode arbitrary graphs by selecting finite sublattices or by
choosing coupling signs/zeros. `PROVED`: these results obstruct an exact
polynomial algorithm that handles those full instance families (subject to
their stated complexity assumptions), but their hypotheses do not equal the
single uniform ferromagnetic sequence of complete cubic boxes. They therefore
do not settle this project's objective.

## Stage 1 outcome

`PROVED`: the strongest clean boundary is **extensive spin-structure
complexity** for the uncompressed surface Kac--Ward/Pfaffian method, supported
by the exact genus lower bound. The ordinary free-fermion route separately
loses quadratic locality, and duality separately changes scalar spins into a
gauge theory. None is a universal impossibility theorem.

The admissible opening for Stage 2 is consequently precise: a successful
candidate must collectively compress the extensive topology, replace the
quadratic Clifford closure, or exploit the gauge/surface constraints without
merely renaming an exponential sum.
