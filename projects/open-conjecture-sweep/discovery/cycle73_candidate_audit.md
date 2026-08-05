# C73 candidate audit

| Target | Current screen | Exact interface | Decision |
| --- | --- | --- | --- |
| (i(G)\le\mu^*(G)) for regular (G) | `OBSERVED`: still listed open in the 2025 TxGraffiti survey and no refutation appeared in the current-source search. | Independent dominating sets and maximal matchings admit exact finite branch-and-bound checks. | Oracle rank 2; exploratory tranche contained. |
| Zero forcing (Z\le\alpha+1) for subcubic graphs | `PROVED` in a July 2026 preprint: an explicit 24-vertex counterexample has (Z=11,\alpha=9). | Cheap but stale. | Excluded. |
| (operatorname{ex}(Q_7,C_4)=304) | `CONJECTURED`: current source gives 19,866 304-edge constructions and no 305-edge example after 1,076 searches, not an upper bound. | 448 Boolean edge variables and 672 square constraints; a 305-edge witness or checked UNSAT certificate is decisive. | **Oracle-selected.** |
| Minimum order of connected (G) with (s(L(G))=2) | `CONJECTURED`: a 14-vertex example is known; global minimality is open. | Exact characteristic-polynomial/inertia check; lower bound requires graph enumeration. | Secondary target. |
| Hadamard order 668 | `OBSERVED`: current board records it as the smallest unresolved order. | A matrix is instantly checkable but construction search is enormous. | Excluded from this tranche. |

Sources reviewed: [TxGraffiti survey record](https://arxiv.org/abs/2507.17780),
[zero-forcing refutation](https://arxiv.org/abs/2607.23664),
[hypercube source](https://arxiv.org/abs/2603.29127), and
[line-graph signature source](https://arxiv.org/abs/2607.22874).

Oracle selected the Q7 target after independent ranking. Its falsifier is a
305-edge C4-free subgraph, checked by complete enumeration of all 672 squares.
An UNSAT claim requires a proof certificate and an independent exact route; a
timeout or failed heuristic search proves nothing. The earlier regular-graph
sample remains `OBSERVED` exploratory evidence only.
