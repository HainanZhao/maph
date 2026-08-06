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
