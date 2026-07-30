# Dedekind-sum phase formula — master plan

Last reconciled: 2026-07-30 UTC

## Objective

Test the conjectural implication

\[
\text{quartic Stark phase selection}
\quad\Longleftrightarrow\quad
\text{an exact Dedekind--Rademacher congruence}.
\]

The first target is deliberately narrower: determine whether the
existing certified quartic packets provide an independent calibration
dataset for such a congruence. A negative answer is a completed
feasibility result, not a reason to manufacture a formula.

## Non-negotiable claim boundary

- The absolute phase of \(L'(0,\chi)\) is not expected to be a rational
  multiple of \(\pi\).
- The proposed finite formula concerns a **phase defect** relative to
  an independently constructed canonical weak Stark solution.
- A logarithmic comparison object derived from the same \(L'\)-value is
  not independent calibration data.
- CM-descent through an imaginary quadratic field does not by itself
  place a case under Roblot's totally-real-base index theorem.
- Formula-family complexity and holdout rows are frozen before fitting.
- A five-point interpolation is rejected even when exact.

## Twenty-cycle ledger

| Cycle | Task | Status | Evidence |
|---:|---|---|---|
| 001 | Create project and recovery map | BANKED | this file, `README.md` |
| 002 | Freeze claim boundary and failure criteria | BANKED | `data/preregistration-v1.json` |
| 003 | Freeze primary-source perimeter | BANKED | `docs/literature-perimeter-v1.md` |
| 004 | Separate CM-route eligibility from Roblot eligibility | BANKED | `docs/scope-audit-v1.md` |
| 005 | Identify the five certified packet controls | BANKED | `artifacts/certified-controls-v1.json` |
| 006 | Extract ten route-level analytic records and hashes | BANKED | same |
| 007 | Implement exact sawtooth and Dedekind sums | BANKED | `src/dedekind.py` |
| 008 | Verify classical reciprocity and closed-form controls | BANKED | tests |
| 009 | Implement a fixed Rademacher-symbol convention | BANKED | `src/dedekind.py` |
| 010 | Audit generator and cocycle sanity checks | BANKED | tests |
| 011 | Compute certified-control \(L'\) phases | BANKED | `artifacts/control-phase-audit-v1.json` |
| 012 | Test raw phase quantization | BANKED_NEGATIVE | same |
| 013 | Test two-route phase invariance | BANKED | same |
| 014 | Locate an independent canonical comparison object | BANKED_NEGATIVE | `docs/identifiability-audit-v1.md` |
| 015 | Freeze the admissible low-complexity formula family | BLOCKED | independent defect unavailable |
| 016 | Rank/identifiability audit before fitting | BANKED_NEGATIVE | `artifacts/control-phase-audit-v1.json` |
| 017 | Freeze 50-row holdout | BLOCKED | no independent target variable |
| 018 | Fit on certified controls | NOT_AUTHORIZED | would be tautological |
| 019 | Run holdout | NOT_AUTHORIZED | target absent |
| 020 | Bank feasibility verdict and next gate | BANKED | `docs/cycle-020-checkpoint.md` |

## Current finding

The five certified packets provide ten excellent convention and
route-invariance controls, but not yet five independent values of the
proposed phase defect. Their Engine-C comparison vectors are obtained
by Fourier inversion of the same \(L'\)-values and then identified in
unit lattices. They certify the packet, but using them to fit a
Dedekind formula for the defect would be circular.

The next legitimate gate is to implement Roblot's canonical
index-formula solution on the **original cyclic-quartic subextension
over the real quadratic base**, verify his hypotheses row by row, and
construct its coefficient \(c(\eta)\) without reading the certified
packet or analytic \(L'\)-value. Only then does
\(\arg L'-\arg c(\eta)\) become a fit-worthy target.

## Tags

`VERIFIED`, `NUMERICAL`, `CONJECTURAL`, `BLOCKED`, and
`BANKED_NEGATIVE` retain their literal meanings. No fitted formula
will receive a theorem tag without a written reciprocity proof.
