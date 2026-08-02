# Cycle 78: critical packets carry an exact Freiman phase web

## Claim boundary

At the Cycle-77 critical cell, `PROVED`: if four packet hits satisfy

```text
ell_1+ell_2=ell_3+ell_4,                            (1)
```

then their reduced rational labels `r_i=n_i/q_i` satisfy the exact identity

```text
r_1 r_2=r_3 r_4.                                   (2)
```

The integer-forcing margin is `X^(-8/75+o(1))` after clearing denominators.
Consequently, the labels on any complete arithmetic progression of hit
indices form a rational geometric progression, and such a progression has
length `O(log Q)`.

This does not prove that a packet set at the target cardinality contains any
nontrivial additive quadruple or long progression. Sparse Sidon-type index
sets remain possible. No ACSI, packet closure, powered saving, density gain,
or interval gain is proved.

## Integer forcing

Cycle 77 gives

```text
|r_i-E_i|<<eta/Q=X^(-36/25+o(1)),
E_i=exp(2pi ell_i/Delta),
Q=X^(1/3), eta=X^(-83/75).                          (3)
```

Condition (1) gives `E_1E_2=E_3E_4`. Since all values stay in a fixed compact
positive interval, (3) implies

```text
|r_1r_2-r_3r_4|<<eta/Q.                            (4)
```

After multiplication by `q_1q_2q_3q_4`, the left side is an integer whose
absolute value is

```text
<<Q^4 eta/Q=Q^3 eta=X^(-8/75+o(1)).                (5)
```

For sufficiently large `X`, this integer is zero, proving (2). This is an
exact algebraic identity, not numerical recognition.

## Valuation representation

For every prime `p`, write `v_p(r)` for the signed exponent of `p` in the
reduced rational `r`. Equation (2) is equivalent to

```text
v_p(r_1)+v_p(r_2)=v_p(r_3)+v_p(r_4)                (6)
```

for every `p`. Thus the packet labels form an exact Freiman homomorphism from
the additive relations of their index set into the free abelian valuation
lattice.

Suppose all indices

```text
ell_j=ell_0+jh, 0<=j<L,
```

are hits. Applying (2) to `j+1+0=j+1` gives inductively

```text
r_j=r_0 g^j, g=r_1/r_0.                            (7)
```

If `g=1`, primitive reduced-fraction uniqueness forbids two different packet
indices with the same label. Otherwise write `g=u/v` reduced. Since
`max(u,v)>=2`, and writing `r_0=x/y`, cancellation in `xu^j/(yv^j)` is at
most the fixed factor `xy<<Q^2`, the reduced height obeys

```text
height(r_j) >= 2^j/(C^2Q^2).                       (8)
```

But every critical label has height `O(Q)`. Hence
`2^j<<Q^3`, proving `L=O(log Q)`.

## Structural split

`CONJECTURED` ACSI inverse split:

1. relation-rich packet sets yield a low-dimensional valuation web through
   (6), which E16 should convert into a phase-bearing seed or rule out by the
   height bound;
2. relation-poor packet sets are quantitatively Sidon-like and should be the
   minor-arc input for a sublattice-aware projective-duality estimate.

The target size `X^(2/15)` is below the generic `Delta^(1/2)=X^(3/10)` Sidon
threshold, so elementary additive-energy pigeonholing cannot force branch 1.
That limitation is kept inline: (2) is a rigidity theorem for relations that
exist, not a theorem producing relations.

## Gate effect

E16 advances to
`EXACT_FREIMAN_WEB_OR_SPARSE_ACSI_OPEN`.
