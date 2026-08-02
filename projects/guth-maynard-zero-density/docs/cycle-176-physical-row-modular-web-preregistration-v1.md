# Cycle 176 preregistration: physical-row modular web

## Question and boundary

Aggregate Cycle-175 residue avoidance only across states sharing a physical
source row `h`. The objective is a labelled eligible-mass lower bound or a
quantified support-separation/modular-avoidance web. Separate state marginals
or private affine parameters are explicitly insufficient. No recurrence,
density, or interval claim is preregistered.

## Frozen incidence object

Each complete state-row incidence retains

```text
(beta, ell, state_id, h, j, a, q, K),
```

with its Cycle-175 range/residue status and Cycle-174 capacity class. At the
physical row itself the residue condition is exactly `a|h`; the affine
`n0 mod m` representation is retained only as its proof certificate. Form
the bipartite incidence graph between physical labelled rows `(beta,ell,h,j)`
and state/modulus records. Freeze a row-codegree threshold `D>=2` and split
the total incidence weight into rows of codegree below `D` and at least `D`.

For every high-codegree row freeze the numerator-divisor complexity ledger

```text
V=# distinct numerators a,
E=# distinct a dividing h,
G=sum_(ordered distinct a,a') gcd(a,a')^2/(a a').
```

No deduplication may erase state or residue labels.

## Gates

1. Prove the exact weighted incidence decomposition. Low-codegree mass is a
   labelled physical-support-separation bank, not discarded mass.
2. Prove `E<=tau(|h|)`. On high-codegree rows, separate: eligible/range-valid
   mass; a high-multiplicity common numerator group with `a` not dividing `h`;
   large distinct-numerator divisor avoidance `V-E`; or high gcd energy `G`.
   Freeze all thresholds before data inspection.
3. Construct a finite countermodel with disjoint physical-row supports and
   high divisor entropy to show why state mass alone cannot imply aggregate
   breadth.

## Falsifier and advance condition

The falsifier is an incidence omitted from every branch, a claimed CRT
compression without compatible residues, or a support-separation claim that
forgets row labels. Advance only with a complete incidence classifier or a
genuine eligible-mass theorem.
