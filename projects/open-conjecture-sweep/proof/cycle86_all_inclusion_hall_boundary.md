# C86 exact boundary: all-inclusion Hall transport fails

`PROVED`: among all 65,536 labelled subfamilies of \(\mathcal P([4])\),
exactly 2,034 are nontrivial, union-closed, full-universe, separating, and
dimension three.  In each retained family, some optimal element has an
inclusion-edge matching from \(\mathcal F_x^c\) into \(\mathcal F_x\).
The augmenting-path matcher and exhaustive Hall-subset verifier agree on
every tested optimal element.

`PROVED`: this finite pass cannot extend the mechanism.  In Colbert's
Example 3.20, the stated dimension-three family on \([5]\) has every
element optimal and abundant, yet for every \(x\) the all-inclusion graph
\(G_x\) has a Hall-deficient left subset.  For example, the exact checker
records a deficiency for each \(x\); its source-defined immediate-cover
failure is independently retained.  Thus abundance does not imply the
proposed inclusion-respecting matching even on the named source control.

`PROVED`: source Example 3.19 separately has an optimal nonabundant
element \(1\), whose all-inclusion graph has a Hall witness with four left
sets and three neighbors.  This is a control against the stronger false
statement that every optimal element could work.

## Claim boundary

This refutes only C86's all-inclusion Hall transport as a route to the
dimension-three (height-four) union-closed sets case.  It neither refutes
Frankl's conjecture nor disproves other injections, weighted transports, or
rank-layer arguments that do not require \(A\subseteq B\) edgewise.
