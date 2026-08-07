# Literature and novelty audit

Audit date: 2026-08-07 UTC.

Claim boundary: `PROVED` identifies exact source overlap. `OBSERVED` denotes
a bounded literature search, not a universal priority claim.

## Primary source

`PROVED`: Connelly, Ito, Martinez, Shevchenko, and Yang state Conjecture 5.4
in Section 5.2 of arXiv:2605.12822v1. For `r>=2`, `k>=1`, and positive
`a_1,...,a_k,b`, it asserts sufficiency of

```text
some r | a_i, OR b <= 1 + sum_i floor(a_i/r).
```

It additionally proposes necessity when `k<=3` or `r<=3`, while proving the
one-factor characterization and the `(k,r)=(2,2)` iff case. It reports
bounded verification and gives `([3]_q)^4[2]_(q^4)` as a unimodal example
outside the condition.

Theorem A of the combined manuscript proves exactly the universal sufficient
direction. Theorem B extends the mechanism to multiple spacers through a
hybrid of disjoint divisibility absorption and residual matrix allocation.
It makes no necessity claim.

## Later-overlap check

`OBSERVED`: bounded arXiv, OpenAlex, and Crossref searches through 2026-08-07
found no later indexed resolution of Conjecture 5.4 and no indexed
multi-spacer allocation theorem of this form. The elementary recursion is
not claimed as novel in isolation; the contribution is its application and
matrix lift.
