# Literature and novelty audit

Audit date: 2026-08-06 UTC.

Claim boundary: `PROVED` identifies the source and the exact relationship of
the new theorem to its Conjecture 5.4. `OBSERVED` describes the bounded search
for later overlap; it is not an exhaustive priority claim.

## Primary source

`PROVED`: Connelly, Ito, Martinez, Shevchenko, and Yang state Conjecture 5.4
in Section 5.2 of *Unimodality of q-Fibonomial coefficients for small cases*,
arXiv:2605.12822v1 (May 12, 2026). It asserts that

```text
product_i [a_i]_q [b]_(q^r)
```

is unimodal if some `r | a_i` or
`b <= 1 + sum_i floor(a_i/r)`, and additionally proposes necessity when
`k <= 3` or `r <= 3`. The paper reports finite verification for `k <= 5`,
`r <= 6`, and all parameters at most 15. It explicitly gives
`([3]_q)^4[2]_(q^4)` as evidence that the condition is not necessary in
general.

The present theorem proves the universal sufficient direction for all
`k >= 1`, `r >= 2`. It neither claims nor uses the proposed necessity
direction. Its `k=r=4` specialization strictly contains the live Topic 2
target in `GOAL.md`.

Primary text checked at:
<https://arxiv.org/html/2605.12822#S5.SS2>.

## Later-overlap check

`OBSERVED`: an arXiv API query for q-Fibonomial work through 2026-08-06
returned the source above and the earlier combinatorial-interpretation paper,
but no later paper claiming Conjecture 5.4. The source authors' public
`Fibonomial-Conjecture-Tests` repository was last pushed on 2026-05-10; its
visible history contains the finite-test code and paper revision, not the
aligned-center recursion proved here.

This is a bounded search over reachable primary records, not a universal
priority claim. The manuscript therefore states what it proves relative to
the named conjecture and makes no broader first-proof assertion.
