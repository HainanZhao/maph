# Conjecture 5.4 audience and sharp-boundary gate

Claim boundary: this note satisfies the two pre-proof checks required by
`GOAL.md`. It does not promote bounded computation to a proof and does not
change Topic 2's current Outcome B status.

## Whose conjecture, and why this slice matters

`PROVED` (primary-source attribution): Conjecture 5.4 is due to Brendan B.
Connelly, Ezekiel Ito, Thomas C. Martinez, Olha Shevchenko, and Kacey Yang in
*Unimodality of q-Fibonomial coefficients for small cases*, arXiv:2605.12822v1,
Section 5.2. The authors state it as a common generalization of their
Corollary 4.3, Proposition 4.5, and Proposition 5.3.

`PROVED` (source-checked scope): their theorem covers the necessity direction
when `k <= 3` or `r <= 3`, and their finite verification covers `k <= 5`,
`r <= 6`, and all parameters at most 15. Thus `(k,r)=(4,4)` is the first
corner outside both proved small-dimension regimes, not an arbitrary slice
chosen only by this repository.

`PROVED` (source-checked limitation): the source explicitly says Conjecture
5.4 does not directly settle q-Fibonomial unimodality at width at least four,
because that factorization is not of the conjectured product form. The value
of this slice is therefore a first theorem beyond the source's `k <= 3` or
`r <= 3` regimes and a possible general product-unimodality mechanism—not a
claimed corollary for all q-Fibonomials.

`OBSERVED` (audience assessment): the natural immediate audience is the same
q-analog/unimodality community and the five conjecture authors targeted by
the width-four paper. A proof would answer a named conjecture in its first
jointly unsettled parameter corner and could expose machinery usable for
larger `k,r`. This is externally legible enough to justify the proof-search
slot; no broader impact claim is made.

Primary source: <https://arxiv.org/html/2605.12822#S5.SS2>.

## Exact sharp-boundary test

For every nondecreasing quadruple `a_i <= 64` with no `4 | a_i`, the script
sets

```text
b = 1 + sum_i floor(a_i/4),
```

the largest value authorized by the conjectured inequality. It independently
constructs the direct product and the formal quotient

```text
Q(q) = product_i [a_i]_q / [4]_q,
```

requires the two coefficient-difference routes to agree, and checks both
clauses of the stronger four-section dominance lemma in
`qanalog_k4_r4_reduction.md`.

Replay:

```sh
python3 discovery/goal_qanalog_k4r4_boundary.py --limit 64
```

`OBSERVED` exact result:

```text
quadruples:                       249900
boundary coefficient differences: 30676772
lemma positivity coefficients:     30676772
lemma dominance pair checks:       245644966
status:                             NO_COUNTEREXAMPLE
wall time:                          37.60 seconds
peak resident memory:               12800 KiB
```

All minima were zero, so the data show no hidden positive margin. The first
zero boundary difference occurs at `a=(1,1,1,3), b=1, degree=1`; the first
zero dominance gap occurs at `a=(1,1,1,9), m=0, n=4`.

`OBSERVED` independent implementation check: a separate literal all-pairs
loop verified the four-section comparisons for every nondecreasing
non-divisible quadruple through length 11.

Falsifier: any negative direct midpoint difference, negative required
coefficient of `Q`, four-section decrease under the stated diagonal bound, or
disagreement between direct and reduced differences invalidates the affected
claim. No such row occurred in the stated ranges.
