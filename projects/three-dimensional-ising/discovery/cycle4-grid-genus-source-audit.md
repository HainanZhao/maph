# Cycle 4 source audit — minimum genus of `L x 3 x 3`

## Primary source

Christian Millichap and Fabian Salinas, “Embedding Grid Graphs on Surfaces,”
*Graphs and Combinatorics* **38** (2022), article 87,
DOI `10.1007/s00373-022-02488-w`; arXiv `2104.12270`.

- Publisher Theorem 4, pages 15–16: for every `alpha in N`,
  `gamma(G(alpha,2,2))=alpha`.
- Their convention defines `P_alpha` to have vertices `0,...,alpha`, so the
  repository graph with shape `L x 3 x 3` is exactly
  `G(L-1,2,2)`.
- Therefore `PROVED`: its minimum orientable genus is `L-1` for every `L>=2`.
  In particular, the recursive rotations of genera 3, 4, and 5 at
  `L=4,5,6` are minimum genus.
- Hypothesis check: the repository graph is the simple Cartesian product of
  three free path graphs, with no periodic identifications or parallel edges.
  These are exactly the graphs in the theorem.
- Proof mechanism checked: their lower bound contracts to a
  `K_{3,4 alpha}` minor and uses the exact complete-bipartite genus formula;
  their upper bound invokes the explicit embedding of Proposition 3.  No
  conjectural statement is used.  Their later Conjecture 1 concerns general
  parameter triples and is irrelevant to `G(alpha,2,2)`.

## Frozen retrieval data

- arXiv PDF URL: `https://arxiv.org/pdf/2104.12270`
- arXiv e-print URL: `https://export.arxiv.org/e-print/2104.12270`
- PDF SHA-256 retrieved 2026-08-07:
  `2510185b6c20cc164926c94a5a49cb27fd3fc6b565c59e47b179618526e92467`
- e-print archive SHA-256:
  `577aa7e51df367c9831572c999e0124ede6250a681dde15f95eedd8a12301d65`
- main TeX SHA-256:
  `d94e8f4785f5addd7b32393527ac7be906748d3da2948eb35f1ed1a06d73f18a`

## Relation to the current work

The minimum-genus formula is prior work and is not novel.  The current
candidate contribution is the independently found period-two rotation system,
its nested labeled homology, and the proposed bounded-rank collective
spin-structure transfer.  Any novelty claim about those structures still
requires a separate literature audit.
