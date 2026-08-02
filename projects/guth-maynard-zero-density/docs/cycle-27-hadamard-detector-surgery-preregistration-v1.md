# Cycle 27 Hadamard detector-surgery preregistration v1

## Claim boundary

This cycle may prove an exact algebraic E7/E10 dichotomy for a detector split
into equal-mass prime blocks and signed by a Hadamard system. It may not prove
that the multiblock branch is arithmetically impossible, bound the resulting
signed detector frame in the full Guth--Maynard architecture, prove the
skeleton target, or promote density/interval consequences.

## Frozen block convention

Let `J` be a power of two. Partition the prime coordinates into `J` blocks
such that the restricted coefficient vectors `b_j` are orthogonal and have
equal squared norm `A/J`. Let `H=(h_{ell,j})` be the Sylvester Hadamard matrix
with first row all `+1`, and define

```text
b^(ell)=sum_j h_(ell,j)b_j,
z_j=<x,b_j>,
S_ell=<x,b^(ell)>=sum_j h_(ell,j)z_j.
```

The builder must check

```text
<b^(ell),b^(m)>=A delta_(ell,m),
sum_ell |S_ell|^2=J sum_j |z_j|^2,
sum_(ell>=1)|S_ell|^2=J sum_j |z_j-S_0/J|^2.
```

## Frozen surgery dichotomy

Assume `|S_0|>=V` and freeze the complementary-energy threshold

```text
E_perp=V^2/(16J).
```

Exactly one of the following registered conclusions must be available:

1. if `sum_(ell>=1)|S_ell|^2>=E_perp`, then some `ell>=1` satisfies
   `|S_ell|>=V/(4 sqrt(J(J-1)))>=V/(4J)`;
2. otherwise every block satisfies
   `|z_j-S_0/J|<V/(4J)`, and after aligning `S_0` each block has real part
   at least `3V/(4J)`.

For `J=X^o(1)`, both branches lose only a subpower. In branch 1 the new
coefficient vector is exactly orthogonal to the original detector direction.
In branch 2 all prime blocks are simultaneously synchronized.

## Finite checks

- Use `J=4`, the Sylvester Hadamard matrix, and exact rational/complex-integer
  examples to check orthogonality, Parseval, the complement identity, and
  both branch constants.
- CPython `3.12.3`, optimization level zero, no RNG or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Pin Cycle 11 and Cycle 26 artifacts.
- Hostile audit remains deferred to paper stage.
