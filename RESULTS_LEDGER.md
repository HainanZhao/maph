# Results ledger

This file is append-only. Entries classify each shipped research claim by the
Outcome A/B/C ladder in `GOAL.md` and point to its independently replayable
evidence.

## 2026-08-06 — Width-four q-Fibonomial unimodality

- Classification: **Outcome A — resolved**.
- Claim: for every integer `m >= 1`, `[m+4 choose 4]_F` is unimodal.
- Evidence: `proof/qfib_width4_unimodality_proof.md` and the standard-library
  replay `python3 proof/qfib_width4_unimodality_proof.py`.
- Manuscript: `paper/qfib-width-four/main.tex` and `main.pdf`.
- Public archive: <https://doi.org/10.5281/zenodo.21826970>.
- Claim boundary: no assertion is made for widths `n >= 5`, the full
  two-parameter conjecture, log-concavity, or a chain decomposition.
- External-uptake status: awaiting a third-party citation, reuse, or
  correspondence; publication alone does not satisfy the primary goal.

## 2026-08-06 — Conjecture 5.4 at k = r = 4

- Classification: **Outcome B — reduced (proof attempt remains live until
  the 2026-10-31 review)**.
- Claim: the non-divisible sufficient-condition branch reduces to the
  four-section/window-dominance inequality stated in
  `discovery/qanalog_k4_r4_reduction.md`; the divisible branch follows from
  the source's published results.
- Community check: this is Connelly--Ito--Martinez--Shevchenko--Yang
  Conjecture 5.4 and its first corner outside both proved regimes `k <= 3`
  and `r <= 3`.
- Boundary evidence: exact sharp-boundary testing through `a_i <= 64` found
  no counterexample; this is `OBSERVED`, not proof. Replay with
  `python3 discovery/goal_qanalog_k4r4_boundary.py --limit 64`.
- Evidence note: `discovery/qanalog_k4_r4_audience_boundary.md`.
- Kill criterion: if no proof exists by 2026-10-31, ship Outcome B as the
  final short note and do not extend the date.

## 2026-08-06 — Conjecture 5.4 sufficient direction, all k and r

- Classification: **Outcome A — resolved**, superseding the live Outcome B
  entry above.
- Claim: for every `k >= 1`, `r >= 2`, and positive
  `a_1,...,a_k,b`, the product `product_i [a_i]_q [b]_(q^r)` is symmetric
  unimodal whenever some `r | a_i` or
  `b <= 1 + sum_i floor(a_i/r)`.
- Evidence: `proof/qanalog_conjecture54_sufficiency.md` and the
  standard-library replay
  `python3 proof/qanalog_conjecture54_sufficiency.py`.
- Manuscript: `paper/qanalog-conjecture54/main.tex` and `main.pdf`.
- Breakthrough: the aligned-center identity
  `[a+r]_q[b+1]_(q^r) = q^r[a]_q[b]_(q^r) + [a+r(b+1)]_q`
  turns every authorized parameter increment into a sum of two symmetric
  unimodal polynomials with the same center.
- Claim boundary: this proves sufficiency, including and strictly generalizing
  the `k=r=4` target. It does not claim general necessity or general
  q-Fibonomial unimodality.
- Publication status: DOI reserved at
  <https://doi.org/10.5281/zenodo.21830407>; public-file verification is
  pending.
