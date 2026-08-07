# Gate B5: spin/parity intertwiner and first width-rank certificates

## Claim boundary

`PROVED`: the even-parity homology-frontier carrier on a `w x w` slice is
exactly Fourier dual to the conventional zero-field spin-slice carrier modulo
global spin flip.  This identifies the 256 states at `w=3` with an ordinary
quasi-one-dimensional transfer space; it is not a new Ising solution method.

`CERTIFIED_NUMERICAL`: in the pinned homology coordinates and bit ordering,
the central `8 x 8` flattening for `G_(4,3)` and the central `32 x 32`
flattening for `G_(4,4)` have full rank for nonuniform, homogeneous
anisotropic, and homogeneous isotropic specializations.  Two prime fields
give independent arithmetic controls.  These finite cases do not prove an
area-exponential asymptotic law or an optimal rank over all homology bases.

## 1. Conventional quotient transfer

Put `m=w^2` and let

```
S = F_2^m / <1>,                 |S|=2^(m-1),
P = {x in F_2^m : |x|=0 mod 2}, |P|=2^(m-1).
```

Represent a spin class by the unique bit vector `s` with `s_0=0`.  The
pairing

```
H[s,x]=(-1)^(s dot x),  s in S, x in P,
```

is well defined because replacing `s` by `s+1` does not change its value on
an even mask.  Character orthogonality gives

```
H H^T = 2^(m-1) I.
```

Let `B` be the transverse edges of one slice, with high-temperature variables
`a_e`, and let `u_j` be the longitudinal variables.  Define

```
b(z) = sum_(A subset B, boundary A=z) product_(e in A) a_e,
c(y) = product_(j:y_j=1) u_j,
K[x,y] = b(x+y)c(y).
```

`K` is precisely the parity-frontier transfer.  The normalized conventional
spin transfer, restricted to flip-even functions, has quotient entries

```
Q[s,t] = product_(e=ij in B) (1+a_e sigma_i(s)sigma_j(s))
         * [product_j(1+u_j sigma_j(s)sigma_j(t))
            + product_j(1-u_j sigma_j(s)sigma_j(t))].
```

In `(H K H^T)[s,t]`, substitute `z=x+y`.  The `z` sum factors over transverse
edges.  The even-`y` sum is half the sum of the connector products for `t`
and `-t`.  Since `H^{-1}=2^{-(m-1)}H^T`, coefficientwise in arbitrary signed
edge variables,

```
Q H = 2^m H K.                                      (1)
```

Equation (1) is an explicit invertible intertwiner.  The scalar `2^m` is the
spin-summation normalization per slice.

## 2. What each ingredient contributes

- `PROVED` fixed pathwidth supplies the carrier `|P|=2^(w^2-1)`.
- `PROVED` global `Z2` symmetry is exactly the reduction from `2^(w^2)` spin
  configurations to `2^(w^2-1)` quotient states.
- `PROVED` the Walsh transform in (1) changes basis and does not reduce rank.
- `PROVED` the local Arf/Walsh transform within already selected handle sites
  preserves handle-cut flattening ranks; in a non-handle coordinate split,
  quadratic cross terms can change the displayed rank.
- `PROVED` repeated handle attachment is the only source of locality in the
  twist variables along the length direction.
- `PROVED` translation invariance repeats bulk cores and reduces parameter
  count, but is not needed for the Cycle 4 fixed-width rank bound, which holds
  for arbitrary inhomogeneous edge variables.

## 3. Genus attribution and width table

`PROVED`: our face-surgery induction constructs the `w=3` embedding with
genus `n-1`; it does not independently prove minimality for all `n`.
Minimum genus uses Millichap--Salinas, Theorem 4, after the exact identification
`G_(n,3)=G(n-1,2,2)`.  Thus the all-size minimum-genus statement is a corollary
of their theorem, not a new theorem here.

The proved minimum-genus information used at B5 is

| width | physical frontier | minimum-genus information |
|---:|---:|---|
| 2 | 8 | `g(n,2)=0` |
| 3 | 256 | `g(n,3)=n-1` |
| 4 | 32768 | `g(n,4)=2n-3` for even `n`; `2n-3 <= g(n,4) <= 2n-2` for odd `n` |

For even `n,w=4`, `checkerboard_boundary_rotation` independently constructs
the quadrangular embedding as the boundary of the Millichap--Salinas union of
unit cubes.  Euler's formula gives genus `2n-3`, meeting the girth lower bound.

## 4. Exact rank certificates at `n=4`

The edge order is the canonical lexicographic order from `cubic_box`.  The
homology basis is the deterministic quotient basis returned by
`_edge_homology_labels`.  A bit-cut flattening uses the low bits as ascending
binary row indices and the high bits as ascending binary column indices.

For each character, an optimized quotient-spin transfer computes `G(mu)`.
An independent parity transfer checks all 64 characters at `w=3,t=2`.
Inverse Walsh transformation gives homology sectors; multiplication by the
pinned quadratic-refinement sign and a forward Walsh transformation gives
`F(lambda)`.

At both primes `1000000007` and `1000000009`, the complete profiles are:

| `(n,w)` | weights | binary flattening profile |
|---|---|---|
| `(4,3)` | nonuniform | `(2,4,8,4,2)` |
| `(4,3)` | anisotropic `(2,3,5)` | `(2,4,8,4,2)` |
| `(4,3)` | isotropic `t=2` | `(2,4,8,4,2)` |
| `(4,4)` | nonuniform | `(2,4,8,16,32,16,8,4,2)` |
| `(4,4)` | anisotropic `(2,3,5)` | `(2,4,8,16,32,16,8,4,2)` |
| `(4,4)` | isotropic `t=2` | `(2,4,8,16,32,16,8,4,2)` |

The replay payload records every central determinant, pivot row, pivot column,
pivot value, row swap, edge label, label hash, normalization factor, and weight
specialization.

All entries before specialization are integer polynomials in edge variables.
The only inverse operations in reconstruction are Walsh divisions by powers of
two, invertible in both odd prime fields.  Consequently a nonzero modular
determinant proves that the corresponding integer polynomial determinant is
not identically zero.  In particular, the isotropic `t=2` certificate proves
that the determinant restricted to the isotropic line is a nonzero polynomial
in `t`; it does not prove nonvanishing at every real `t` or at a critical point.

## 5. Basis warning and unresolved asymptotics

Flattening rank is invariant under invertible transformations acting
separately on the two sides of a cut, but not under a homology basis change
that mixes the sides.  The older Cycle 3 isotropic `w=3` search found a
different ordered symplectic basis with middle rank seven.  Therefore the
full-rank certificates above are exact statements in the frozen coordinates,
not lower bounds on the best rank over every symplectic basis and ordering.

`CONJECTURED`: the conditional repeated-handle estimate

```
R(w)=2^(w^2-1+4 floor((w-1)^2/4))
```

is not an unconditional all-width theorem.  Gate B6.2 must first determine
longitudinal saturation at `w=3,4`; no conclusion about cubic boxes follows
from the two width values.

