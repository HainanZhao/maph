# Cycle 12: reusable UNSAT-core templates

Every accepted Cycle-11 core is a clause multiset extracted by the pinned
`drat-trim` checker from a CNF whose complete DRAT proof was independently
verified.  The extractor output is accepted only if each core clause occurs in
the corresponding frozen input CNF and the core itself is independently
certified UNSAT.

For `c=14`, rename each choice variable from its lift digit `d` to the lifted
residue

```
s = v_i + 199 d (mod 14).
```

Because 199 is a unit modulo 14, this is a bijection within every coordinate.
It makes the divisibility labels intrinsic: `s` records divisibility by 2 and
7 without reference to the base-dependent digit numbering.  Auxiliary
divisibility variables retain their prime label and coordinate.

A permitted template map is a permutation of coordinate blocks.  It sends
`x(i,s)` to `x(pi(i),s)` and `y(r,i)` to `y(r,pi(i))`, preserving signs,
prime labels, and every clause.  The exact embedding checker applies the map
to each clause of a certified core and requires the resulting clause multiset
to be contained in the target CNF clause multiset.  If it is contained, the
target CNF contains an unsatisfiable subformula and is therefore unsatisfiable.
By Cycle 11's proved CNF equivalence, that target base has no improper first
lift.

Clustering, refinement hashes, and backtracking order are discovery devices
only.  They may propose a coordinate permutation but cannot certify it.  The
literal-level mapped-clause containment check is the proof step.  A timeout or
failed embedding makes no claim.  Results concern only named first-lift fibers
and imply neither full retained-set emptiness nor the Lonely Runner
Conjecture.
