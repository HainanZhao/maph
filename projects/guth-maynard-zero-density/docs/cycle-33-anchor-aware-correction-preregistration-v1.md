# Cycle 33 anchor-aware correction preregistration v1

## Correction boundary

Cycle 32's flat-support theorem remains valid. Its proposed next step—a
universal prime-Vandermonde lower bound on the `lambda=0` rung—is too broad,
because a flat vector may be an actual restricted prime-phase row. This cycle
may prove that counterexample and replace the gate by an anchor-aware
alternative. It may not bound the anchor recurrence branch, prove transverse
distance, close the skeleton target, or promote density/interval consequences.

## Frozen actual-prime witness

For any finite prime support `P` and any real `t_0`, define

```text
d_(t_0)(p)=|P|^(-1/2)p^(-it_0).
```

Then `d_(t_0)` is exactly flat, has norm one, and is exactly the normalized
prime-phase row at `t_0`. Any row family containing `t_0` therefore has

```text
dist(d_(t_0), row span)=0.
```

The augmented Gram determinant with `d_(t_0)` is zero because it repeats a
row, independent of separation from all other labels. Register this as an
actual-prime counterexample to any universal positive flat-vector-to-row-span
distance or augmented-determinant lower bound.

## Frozen dimension direction

For a `k by N` row matrix of full column rank with `k>=N`, every detector
vector lies in the row span. Thus on an exponent-square rung, a nonsingular
square minor establishes reconstruction rather than excluding it. Record that
the proposed lower-bound direction was reversed unless additional anchor or
coefficient constraints are imposed.

## Frozen anchor-aware reformulation

Let `d` be a flat-support detector reconstructed within error `epsilon` by
the full row span. For a registered anchor cap `r`, define

```text
alpha_r(d)=min_(A subset C, |A|<=r) dist(d,span{x_t:t in A}).
```

The next theorem must distinguish:

1. `ANCHOR`: `alpha_r(d)` is small. Then represent `d` using at most `r`
   anchor rows and translate the original detector values into a weighted sum
   of restricted prime kernels `K_S(t-t_a)`;
2. `TRANSVERSE`: `alpha_r(d)` is bounded below, but the full row span still
   reconstructs `d`. Then prove a many-row exterior-volume, restricted
   invertibility, or multiplicative-energy contradiction.

This cycle registers the reformulation only. Freeze `r=X^o(1)` so anchor
coloring costs no fixed power.

## Checks

- Exact finite phase-row witness on primes `{2,3,5}` at `t_0=0`.
- Exact full-column-rank `k=3,N=2` span example.
- Exact symbolic kernel translation for a one-anchor coefficient vector.
- CPython `3.12.3`, `Fraction`/Gaussian rational arithmetic, no RNG/network;
  pin Cycles 31 and 32.
