# C73 Oracle selection packet

## Question

Oracle first challenged the inherited low-hanging-fruit criterion. A compact
Boolean encoding, a recent conjecture, and a binary verifier do not imply a
credible closure path. In particular, \(\operatorname{ex}(Q_7,C_4)=304\) has
448 variables but 19,866 known optima and large symmetry; the source used an
exact ILP proof only for Q6. Verifier size was being confused with proof
probability.

## Question the questioning

Rejecting Q7 merely because its UNSAT proof may be hard could favor sunk cost
and inherited Ryser vocabulary. The hidden better question is: **which exact
decision converts already-proved structure into a reusable theorem even if the
full conjecture survives?** That criterion values a durable reduction rather
than either familiarity or a superficially small instance.

## Brainstorm and selection

1. **Selected: intersecting Ryser \(r=6\), defect-five closure.** `PROVED` C71
   reduces a hypothetical \(\tau=6\) example to the \(D=5\) equality
   interface. A direct bad-core SAT/CEGAR search plus blocker-template
   extraction can prove the durable scoped theorem that every counterexample
   has \(D\ge6\), even if full Ryser remains open.
2. **Q7 C4-free extremum.** Exact model/UNSAT outcomes are decisive, but the
   likely hard certificate is mostly one-off. Its Q6 calibration was stopped
   unfinished after this re-selection; no Q7 calculation began.
3. **Regular \(i(G)\leq\mu^*(G)\).** Exact falsifiers are cheap, but random
   null samples have little information without an exchange or augmenting-
   forest mechanism.
4. **Poset or line-graph finite searches.** Local verification is exact, but
   the route from a witness search to a global theorem is weak.

## Strongest flaw and pivot falsifier

The 1,167 feasible partition pairs may hide many map-level orbits, and the
universal blocker claim may fail even though all 19 sampled shape
representatives passed. The direct falsifier is an exactly realizable \(D=5\)
core whose compatible-extension hypergraph has core-vertex transversal number
at least six. A mutually compatible extension family completing to
\(\tau\ge6\) is the stronger headline falsifier.

If the first falsifier survives and one genuinely different global-cover
invariant also fails, Oracle's next selection is Q7. Otherwise continue C72 to
an exhaustive UNSAT certificate or a blocker-template theorem.

