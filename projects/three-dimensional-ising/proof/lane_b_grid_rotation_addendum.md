# Grid-graph rotation obstruction for embedding robustness

## Claim boundary

`PROVED`: the abstract cubic grid graph

```
G_(2,2)=P_2 square P_2 square P_2
```

has orientable cellular rotation systems of genera zero, one and two.
Consequently its complete pre-Arf spin-structure family is not invariant
under arbitrary changes of rotation system.  This strengthens the Cycle 11
`K_(3,3)` obstruction by keeping the abstract graph inside the cubic-grid
family.

It does not alter the physical Ising even-subgraph polynomial, and it does
not contradict robustness under filtration-compatible embedding changes.

## Exact rotations

Order the eight vertices lexicographically.  At each vertex, order its three
neighbours lexicographically; a bit `1` reverses that cyclic order and a bit
`0` retains it.  The two bit strings

```
01011010,
00000001
```

give respectively six quadrilateral faces and faces of lengths 6 and 18.
Since the cube graph has eight vertices and twelve edges, Euler's formula
gives

```
g=(2-|V|+|E|-|F|)/2=0,2.
```

The first rotation is the planar cube embedding and hence minimum genus; the
second is a nonminimum, maximum-genus cellular embedding.

`PROVED`: enumerating the two possible cyclic orientations at all eight
degree-three vertices exhausts all `2^8` choices relative to the fixed local
orders.  Their genus census is

```
genus 0:   2 rotations,
genus 1:  54 rotations,
genus 2: 200 rotations.
```

Thus the two selected cases are members of an exact exhaustive census, not
post-selected numerical embeddings.

## Pre-Arf consequence

A genus-`g` cellular embedding has `2^(2g)` quadratic refinements.  The two
selected rotations therefore produce complete pre-Arf families of sizes one
and sixteen.  They cannot be related by an invertible coordinate change in a
common fixed-dimensional sector space.

For each rotation, the graph-to-surface homology labels, symplectic
normalization, quadratic signs and normalized Arf contraction are constructed
exactly.  Character orthogonality proves that the normalized contraction is
the embedding-independent even-subgraph sum.  The replay checks this identity
at one independent nonuniform integer specialization modulo both
`1000000007` and `1000000009`.

This supplies the explicitly requested same-grid-graph rotation test and
also realizes a nonminimum-genus cellular embedding on that graph.
