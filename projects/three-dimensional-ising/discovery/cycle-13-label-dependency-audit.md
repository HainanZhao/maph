# Cycle 13 label and dependency audit

## Propagation rule

A manuscript statement is 'proofpending' if and only if its displayed proof
has a named local gap or one of its named logical dependencies is pending.
Exact finite-field agreement never promotes a statement.  A completed lower
bound is not silently downgraded merely because the matching upper bound is
pending; the theorem environment names that one dependency.

## Acyclic graph

    canonical handle basis
        -> grid relative exactness
        -> grid polynomial TT
        -> generic minimality

    encoder lemma
        -> reachability/observability
        -> generic minimality

    abstract separator theorem + global phase telescoping
        -> grid polynomial TT

The constructed-genus proposition is a parallel calculation and is not used
to infer the co-core rank.  The K_(3,3) obstruction and the marginal
algorithm are independent of the pending grid branch.

## Statement audit

| Statement | Label | Reason |
|---|---|---|
| prop:genus | proved | The rotation, vertex links, face permutation, boundary continuation, face increments, Euler calculation, and minimum-genus subcase are all printed. |
| lem:canonical | proved | The cut collar retracts to the printed tree, giving planarity without the genus count; connected-sum induction and triangular correction give the nested symplectic basis. |
| lem:planar-arc | proved | A proper arc in the planar cut collar separates the disk; mod-two edge intersection is the coboundary of the component indicator. |
| lem:grid-exact | proved | The planar-arc lemma supplies the former exposed-longitude support gap uniformly in width, parity, and boundary position; the printed H1 and internal H2 formulas then close H1--H3. |
| lem:phase-telescoping | proved | The phase-potential rectangular identity, global character localization, path/even-subgraph bijection, and integer core expansion are printed. |
| thm:grid-upper | proved | The grid exactness and global phase-telescoping lemmas give denominator-free local cores. Its required two-prime direct-core audit is still a release gate, not a proof premise. |
| lem:encoders | proved | The arbitrary-width shell incidence proof and width-four bases are printed; Cycle 12 v2 is the audit. |
| lem:XYfull | proved | It follows algebraically from the proved two one-sided encoders and the explicit two-slab diagonal buffer. |
| thm:grid-tight | proved | The arbitrary-width upper bound and completed encoder/buffer lower bound now meet. |
| thm:k33 | proved | Rotation, gluing, edge lists, coordinates, fixed minors, embedded-chain argument, and all 24 relabellings are printed; both-prime replay is archived. |
| thm:marginals | proved | It is conditional only on being given a TT, which is its stated input, not on existence of the grid TT. |

## Remaining Phase 0 boundary

T1 is closed.  The mathematical part of T2 is closed by the global
phase-telescoping and planar-arc lemmas, but the prescribed direct local-core
replay at (6,3), (7,3), and (4,4) remains to be implemented.  T3 is complete:
the dependency graph is explicit and no theorem environment retains a
silent conservative downgrade.
