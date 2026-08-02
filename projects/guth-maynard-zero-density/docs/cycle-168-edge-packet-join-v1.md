# Cycle 168: exact cross-edge/local-packet join calculus

## Claim boundary

`PROVED`: for the frozen edge and target-local-packet interface, compatible
pairs give exact beta-seeded Cycle-67 propagation. The correct population
ledger is a bipartite compatibility form, and the frozen nonjoin alternatives
are exhaustive.

This does not prove any actual overlap of Cycle-167 edges with local packets.
It proves no target packet population bound, recurrence in the real census,
E7/E9 skeleton, density result, or prime-interval improvement.

## Exact composition

Let an edge at target label `L` retain a genuine target strip hit

```text
|j+beta-h alpha_L| <= C_E/X,                         (1)
```

and let a beta-free target-local packet retain

```text
|q alpha_L-a| <= C_P/(KX),    qK<=H.                 (2)
```

If the edge height is in the packet's frozen target range and `|k|<=K`, then

```text
j_k=j+k a,       h_k=h+k q,
j_k+beta-h_k alpha_L
 = (j+beta-h alpha_L)-k(q alpha_L-a).                (3)
```

Thus every compatible labelled pair realizes the usual seeded progression at
strip constant `C_E+C_P`, with the edge endpoint as its genuine beta seed.

## Compatibility, not a diagonal key

An edge and a packet do **not** need equal denominators, depths, or packet
constants. Their compatibility is the relation

```text
L_E=L_P,
h_E in I_P,
q_P K_P<=H,
K_P>=K_crit,
C_E+C_P<=C_join.                                    (4)
```

For complete labelled edge records `e` and packet records `p`, with retained
nonnegative weights, the exact join population is

```text
J = sum_(e,p) weight(e) weight(p) 1_Comp(e,p).       (5)
```

Neither a product of global totals nor a diagonal product over an artificial
common `(L,q,a,K,C)` key is justified.

## Exhaustive separation and loop containment

For every noncompatible pair, first failure in the fixed order is one of:

1. target-label mismatch;
2. target-range mismatch;
3. packet inadmissibility `qK>H` (or invalid packet data);
4. subcritical depth `K<K_crit`; or
5. strip-constant incompatibility `C_E+C_P>C_join`.

This gives a typed, label-preserving support-separation inverse if (5) cannot
be bounded below.

A direct affine cross-edge loop supplies no replacement packet: telescoping
gives `j_L-j_0=h_0-h_L`. At a common label, subtracting its two strip rows is

```text
(h_0-h_L)(1+alpha_ell)=O(X^(-1)),                    (6)
```

so integer forcing gives trivial holonomy for large `X`.

## Remaining bridge

The new mathematical need is a label-faithful lower bound on (5), or an
actual typed separation theorem for the Cycle-165--167 populations. The
compatibility calculus itself cannot turn their separate masses into overlap.
