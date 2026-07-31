# Dedekind-sum phase formula — master plan

Last reconciled: 2026-07-31 UTC

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
| 021 | Translate Roblot's quartic construction exactly | BANKED | source audit and executable formula |
| 022 | Genuine (A1)--(A3) screen on five original quartic fields | BANKED | `artifacts/roblot-quartic-gate-sealed-v1.json` |
| 023 | Seal the first independent constructor | PRESERVED_FAILURE | v1 fixed-lattice proxy |
| 024 | Replace proxy by genuine embedded \(K^+\)-unit lattice | BANKED | `artifacts/roblot-rq000129-constructor-sealed-v2.json` |
| 025 | Open the first independent phase defect | BANKED | `artifacts/rq000129-phase-gate-v1.json` |
| 026 | Freeze remaining constructors and feature protocol | BANKED | `docs/cycles-026-045-preregistration.md` |
| 027 | Reconstruct the \(\mathbf Q(\sqrt{35})\) unit data | BANKED | sealed constructor artifact |
| 028 | Seal RQ-001280 constructor | BANKED | `artifacts/remaining-roblot-constructors-sealed-v1.json` |
| 029 | Compute RQ-001569 relative class/Fitting data | BANKED | same |
| 030 | Seal RQ-001569 constructor | BANKED | same |
| 031 | Compute RQ-007519 relative class/Fitting data | BANKED | same |
| 032 | Seal RQ-007519 constructor | BANKED | same |
| 033 | Compute RQ-001894 relative class and norm index | BANKED | same |
| 034 | Seal RQ-001894 constructor | BANKED | same |
| 035 | Demonstrate deterministic constructor replay | BANKED | same |
| 036 | Open the remaining certified phase balls | BANKED | `artifacts/all-five-phase-gates-v1.json` |
| 037 | Resolve character orientations | BANKED | same |
| 038 | Bank five-for-five phase quantization | BANKED | same |
| 039 | Prove weak-solution gauge ambiguity | BANKED | `docs/gauge-ambiguity-lemma-v1.md` |
| 040 | Replay gauge action on all controls | BANKED | same |
| 041 | Compute fundamental-unit \(SL_2(\mathbf Z)\) matrices | BANKED | `artifacts/frozen-feature-family-audit-v1.json` |
| 042 | Compute exact Rademacher/Dedekind features | BANKED | same |
| 043 | Reject the frozen feature family before fitting | BANKED_NEGATIVE | same |
| 044 | Fix dominant gauge; prove field-only no-go | BANKED_NEGATIVE | `artifacts/field-only-dedekind-family-no-go-v1.json` |
| 045 | Audit cocycle availability; declare theory pivot | BANKED | `docs/cycle-045-checkpoint.md` |
| 046 | Freeze ray-class cocycle bridge target and conventions | BANKED | `docs/cycles-046-055-preregistration.md` |
| 047 | Extract dimension-4 bridge | BANKED | `docs/sic-bridge-extraction-v1.md` |
| 048 | Extract dimensions 7/8 and compare | BANKED | same |
| 049 | Formulate ray-to-form existence proposition | BANKED_NEGATIVE | `docs/ray-to-form-obstruction-v1.md` |
| 050 | Implement universal supplied-tuple arithmetic | BANKED | `src/cocycle.py` |
| 051 | Replay frozen SIC anchors | BANKED | `artifacts/supplied-tuple-bridge-audit-v1.json` |
| 052 | Attempt RQ-000129 from ray data alone | BANKED_NEGATIVE | `artifacts/rq000129-ray-to-form-gate-v1.json` |
| 053 | Audit gauge and character covariance | BANKED | `docs/cocycle-covariance-v1.md` |
| 054 | Test any authorized feature on five controls | NOT_AUTHORIZED | generic bridge gate failed |
| 055 | Bank general/restricted/no-bridge verdict | BANKED | `docs/cycle-055-checkpoint.md` |
| 056 | Freeze final descent/resolvent stop conditions | IN_PROGRESS | `docs/final-block-preregistration.md` |

## Current finding

The five certified packets provide ten excellent convention and
route-invariance controls, but not yet five independent values of the
proposed phase defect. Their Engine-C comparison vectors are obtained
by Fourier inversion of the same \(L'\)-values and then identified in
unit lattices. They certify the packet, but using them to fit a
Dedekind formula for the defect would be circular.

The independence gate has now passed for all five controls, and every
control exhibits a unique fourth-root phase relation after its
character orientation is aligned. The raw quarter-turn index is not
invariant under the allowed weak-solution gauge. A canonical
dominant-embedding gauge repairs that defect, but the simplest
field-only Dedekind--Rademacher family then fails exactly on a
two-control collision.

The missing variable is ray/modulus-specific cocycle data. The current
repository computes such data only for special SIC tuples; it does not
contain a generic extractor from an oriented ray character. Therefore
the empirical fitting track is stopped. The next authorized project is
a theorem-level ray-class cocycle bridge, not a larger fit.

Cycles 046--055 found that the exact arithmetic does generalize once a
Kopp tuple is supplied, but the proposed ray-character-to-one-tuple map
is ill-typed: characters are Fourier objects on all classes, whereas
the cocycle inputs are class-level. The current verdict is
`RESTRICTED_SIC_BRIDGE`. The corrected target is a
representative-independent class multiplier followed by a
character-level Fourier cocycle resolvent.

## Tags

`VERIFIED`, `NUMERICAL`, `CONJECTURAL`, `BLOCKED`, and
`BANKED_NEGATIVE` retain their literal meanings. No fitted formula
will receive a theorem tag without a written reciprocity proof.
