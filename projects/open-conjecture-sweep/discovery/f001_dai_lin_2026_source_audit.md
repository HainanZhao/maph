# F001 source audit: Dai--Lin 2026 algebraic constructions

**Status:** `OBSERVED` primary-source overlap screen, 2026-08-06 UTC.  This
records the stated results of the reachable v1 preprint; it is not an
independent verification of its proofs and creates no new research cycle.

## Primary source and exact scope

Lulu Dai and Qizhong Lin, *Book Ramsey numbers via algebraic constructions*,
arXiv:2606.07214v1 (2026-06-05), Theorem 1.1, Corollary 1.1, and Lemmas
2.2--2.3.  The source defines a PC-graph of order \(\nu\) as
\[
 \operatorname{srg}\!\left(\nu,(\nu-1)/2,(\nu-5)/4,(\nu-1)/4\right)
\]
and proves its equivalence with a symmetric conference matrix of order
\(\nu+1\).  From a PC-graph of order \(2n-1\), its Theorem 1.1 constructs a
graph on \(4n\) vertices, with clone pairs, for which both colours avoid
\(B_n\), giving \(R(B_n,B_n)\geq4n+1\).

Its Corollary 1.1 states the exact equality \(R(B_n,B_n)=4n+1\), subject to
\(4n+1\) not being a sum of two squares and either:

1. \(2n-1\equiv1\pmod4\) is a prime power; or
2. \(2n-1=pq^2\), where \(p\) is the order of a PC-graph and
   \(q\equiv3\pmod4\) is a prime power.

The source's Lemma 2.3 attributes the second family to Mathon's product:
a PC-graph of order \(p\) yields one of order \(pq^2\).  These are concrete
infinite exact diagonal families, not an all-\(n\) theorem.

Source links: <https://arxiv.org/html/2606.07214v1#Thm1>,
<https://arxiv.org/html/2606.07214v1#Cor1>, and
<https://arxiv.org/html/2606.07214v1#Lem2>.

## F001 overlap map

| prior record | former state / boundary | delta required of any successor |
|---|---|---|
| C103 | six fixed cyclic blocks plus inversion bits | no fixed six-block character placement |
| C104--C106 | inverse-closed degree-\(q\) Cayley states on \(D_{2q}\) | no dihedral Cayley connection-set parametrisation |
| Dai--Lin v1 | symmetric conference / PC-graph lift to \(4n\) vertices | no reproof of the stated conference-matrix construction or its two PC-graph families |

## Consequence for the next F001 cycle

`OBSERVED`: F001's prior all-\(n\) framing materially overlaps known 2026
infinite exact families.  It is not a global closure: the source leaves the
all-\(n\) diagonal problem open.  A successor must either (a) establish a
new sufficient construction condition not implied by the cited PC-graph and
Mathon routes, or (b) provide a proof-grade reduction that discriminates a
specified remaining parameter class.  A finite graph census, an unbounded
conference-matrix search, or a restatement of the cited lift is not an
admissible delta.
