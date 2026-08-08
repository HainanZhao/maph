# Tensor-network translation of Lane B

`PROVED` claims only; this note adds no mathematics.

## Dictionary

- A canonical handle `(a_i,b_i)` is a four-state physical MPS site.
- The complete pre-Arf function is the MPS amplitude, or the diagonal of a
  disorder-parameter MPO.
- An attainable even separator mask is the virtual bond index.
- H1 says a character gauge factors through the virtual index.
- H2 says the quadratic phase splits into left, right, and virtual terms.
- H3 says the internal `(a_i|b_i)` cut needs no additional virtual bit.
- An Arf or product-form spin-structure weight is a one-site contraction on
  the physical leg.

The exact TT/MPS bond equals the maximum rank of the successive unfoldings
(Oseledets 2011, Theorem 2.1).  Therefore the arbitrary-width upper theorem
gives bond at most `d_w=2^(w^2-1)`, and generic minimality gives equality for
independent nonuniform weights.  The homogeneous theorem gives equality on a
nonempty generic width-three anisotropic locus and on its isotropic line
outside a finite algebraic exceptional set.

## Environment sweep

The all-handle Walsh-marginal theorem is a left/right environment sweep.  It
requires `O(4*g*d_w^2)` dense ring operations and `O(g*d_w)` stored
environment entries.  This is a batch claim for all single-handle Walsh
marginals, not an improvement over ordinary transfer for one partition
function.

## Boundary

For cubic boxes `w=L`, the virtual carrier remains `2^(L^2-1)`.  The
translation does not assert sub-area compression, a thermodynamic limit, or
an exact solution of the cubic Ising model.
