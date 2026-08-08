# Character-duality correction for the internal separator cut

## Status

`PROVED`: the `lambda_b` character is `beta_i=PD(a_i)`, its exposed
meridian representative is relative-exact in the checkerboard cut collar,
and it is invariant under the triangular longitude correction.  The former
longitude-H3 sentence is false and is not used.

## 1. The forced dual table

For a canonical symplectic basis with `B(a_i,b_j)=delta_ij`, write

    h=sum_i(x_i a_i+y_i b_i).

Then

    B(h,b_i)=x_i,   B(h,a_i)=y_i.

Consequently

    alpha_i=PD(b_i),   <alpha_i,h>=x_i,
    beta_i =PD(a_i),   <beta_i,h>=y_i.

Since `q_lambda(h)=sum_i x_i y_i+lambda_a dot x+lambda_b dot y`, the
`lambda_a` character is `alpha_i` and the `lambda_b` character is `beta_i`.
The discarded longitude assignment fails already on `h=a_i`:
`PD(b_i)(a_i)=1` although `y_i=0`.

## 2. Relative exactness at the midpoint

Cut the checkerboard slab collar along its displayed co-core meridians.  The
tile-incidence graph printed in the manuscript is a path, so the cut collar
is a disk.  At the midpoint of the current co-core move, the two half-band
tiles have not been re-identified.  Push the exposed copy of the meridian
slightly into the disk.  The result is a proper arc `a_hat_i` whose endpoints
are the two marked separator strands.

The meridian and its push-off cobound a vertex-free rectangle in the ribbon
collar.  If `s_rect` indicates the vertices swept by that rectangle, their
cellular intersection cocycles satisfy

    gamma_(a_i)+gamma_(a_hat_i)=delta s_rect.             (1)

The proper arc separates the disk.  If `s_far` indicates its far component,

    gamma_(a_hat_i)=delta s_far.                          (2)

Equations (1)--(2) show that the restriction of
`beta_i=PD(a_i)` is a coboundary.  Therefore, for every exposed relative
chain `c` with frontier mask `m`,

    <beta_i,c>=<s_i,partial c>=<s_i,m>=rho_i(m).          (3)

This proves H3.  Outer-boundary co-cores use the adjacent long tile in the
same path decomposition; no additional endpoint or component is introduced.
Thus the argument is independent of width, slab parity, and whether the
co-core is interior, on an edge, or at a corner.

## 3. Triangular transport

The preliminary longitudes are corrected by

    b_j=tilde b_j+sum_k U_(kj)a_k,

with `U` strictly upper triangular.  Linearity of Poincare duality gives

    alpha_j=tilde alpha_j+sum_k U_(kj) beta_k,
    beta_j=tilde beta_j.                                 (4)

Thus the H3 cochain and `rho_j` do not change.  Only the `lambda_a`
character acquires earlier meridian characters; those restrictions are H1
trace functions on the un-emitted side.  Equation (4) also fixes the column
index and prevents an inverse-transpose ambiguity.

## 4. Internal quadratic term

At the cut `lambda_(a_i)|lambda_(b_i)`, the coefficient of `a_i` on the
emitted side may depend on the left history, while every exposed `b_i`
coefficient is the mask function (3), up to fixed completion-mask terms.
Hence the current term

    (x_i+x_i^0(m))(y_i(m)+y_i^0(m))

is a left-and-mask phase.  It introduces no virtual bit beyond the even
frontier mask.  This is exactly the H2 internal-cut factor used by the global
phase-potential construction.

## 5. Independent firewalls

- `proof/verify_lane_b_character_duality.py` checks the dual table and (4)
  over exact `GF(2)` data through genus eight and rejects the former text.
- `proof/verify_lane_b_universal_canonical_ranks.py` recomputes all binary
  flattenings of the frozen `G_(10,3)` and `G_(4,4)` controls over both
  primes.
- `proof/verify_polynomial_tt_grid_cores.py` compares the denominator-free
  all-sector cores against an independently compiled spin-slice reference
  over both primes and two nonuniform evaluations.

The finite checks audit conventions and implementations.  The
arbitrary-width conclusion follows from Sections 2--4, not from those checks.
