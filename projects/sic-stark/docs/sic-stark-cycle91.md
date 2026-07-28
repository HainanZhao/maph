# SIC--Stark research cycle 91: adversarial status audit

## What is exact

- AFK admissibility, stabilizers, and both dimension-eight strata;
- maximal-order ray groups and the two quadratic characters;
- unconditional class fields, regulators, and oriented ray units;
- the complete radical overlap table, assuming its displayed signs;
- both shifted Weyl matrices, all idempotency entries, and all minors;
- transport within discriminants \(5\) and \(45\).

## Publication-grade gate identified here

`certify_dimension_eight_maximal_cocycle.py` presently uses ordinary
floating-point quadrature to select the signs of the six-factor AFK
cocycle.  The values are well separated from zero (the smallest
absolute overlap is \(0.346\ldots\)), and the convention audit agrees
with all exact ray logarithms and both exact TCC systems.  Nevertheless,
an unconditional theorem should replace this sign selection by either:

1. Arb interval evaluation of the six-factor formula; or
2. a symbolic sign lemma derived from its finite Pochhammer and
   double-sine shift factors.

Thus the mathematical mechanism and exact finite theorem are closed.
The final gap is a bounded analytic certification task, not an
algebraic-number-theory or TCC obstruction.

## Resolution

Cycle 92 closes this gate by the second route.  The finite
\(q\)-Pochhammer phases and reciprocal-double-sine recurrence signs
are reduced exactly in \(\mathbb Q(\sqrt5)\).  All 63 total phases are
integral multiples of \(\pi\), and their parities reproduce the signed
radical table exactly.  No floating-point sign selection remains in
the theorem.
