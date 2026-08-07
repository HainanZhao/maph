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

## 2026-08-07 — Topic 2 record-location correction

- Classification: **Outcome A — resolved**, unchanged.
- Correction: the standalone `paper/qanalog-conjecture54/` manuscript was
  merged into the stronger combined paper
  `paper/qanalog-multispacer-criterion/main.tex` and `main.pdf`; its exact
  replay is now `python3 proof/qanalog_multispacer_criterion.py`.
- Evidence: `paper/qanalog-multispacer-criterion/verification.md` records
  1,680 two-route recursion identities, 15,163 one-spacer induction rows,
  43,002 nested recursion steps, the independent checks, and final status
  `COMBINED_CRITERION_PASS`.
- Superseded metadata: the old standalone manuscript path and its pending DOI
  statement above are historical. No DOI was assigned to the combined paper,
  and dissemination is not required by `GOAL.md`.
- Claim boundary: the universal sufficient-direction theorem and its Outcome
  A classification are unchanged; the combined paper adds a sufficient
  multi-spacer criterion but does not prove necessity.

## 2026-08-07 — Conjecture-project path relocation

- Classification: **administrative relocation; no research claim changed**.
- The legacy root trees `discovery/`, `experiments/`, `paper/`, and `proof/`
  moved intact under `projects/open-conjecture-sweep/`.
- Paths in earlier ledger entries are historical project-relative paths. Read
  and replay them from `projects/open-conjecture-sweep/`; for example,
  `proof/qfib_width4_unimodality_proof.py` now means
  `projects/open-conjecture-sweep/proof/qfib_width4_unimodality_proof.py`
  from repository root.
- This relocation changes no proof, outcome classification, claim boundary,
  manuscript content, or recorded checksum.

## 2026-08-07 — Exact covering number C(23,6,2)

- Classification: **Outcome C — killed by the fixed eight-hour wall cap**.
- `PROVED`: the exact reduction partitions every hypothetical 20-block cover
  into eleven canonical replication-five star cases. Independent orbit,
  replication-pattern, CNF-primitive, regenerated-DIMACS, manifest, and
  budget-chain checks pass.
- `OBSERVED`: CaDiCaL 1.7.3 returned `UNKNOWN_SOLVER_LIMIT` on all eleven
  cases. The final two each ran for 7,399.00 seconds; the coordinator recorded
  78,622.98 aggregate charged seconds and 28,800.07 aggregate wall seconds.
- Evidence: from `projects/open-conjecture-sweep/`, run
  `python3 proof/verify_cover_23_6_2_bounded_archive.py`; the terminal replay
  returns `ARCHIVE_TERMINAL_PASS` and derives `WALL_CAP_DERIVED` from the raw
  numeric meter. The readable record is
  `discovery/cover_23_6_2_bounded_outcome.md`.
- Claim boundary: this fixed-budget method found no 20-block cover and did not
  certify any branch UNSAT. It proves neither `C(23,6,2)=20` nor
  `C(23,6,2)=21`; the mathematical question remains open.
