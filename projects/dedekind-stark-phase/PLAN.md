# Dedekind-sum phase formula — master plan

Last reconciled: 2026-07-31 UTC

## Status and recovery

**Status:** original mechanism
`FINISHED_WITH_VERIFIED_NO_GO_FOR_FROZEN_MECHANISM`; Roblot phase
clarification theorem `PROVED`, census screen
`BLOCKED_BEFORE_TARGET_OPENING`; withdrawn-replay correction
`PUBLISHED_IN_RESULTS_V1.4`; long Roblot message
`READY_AWAITING_AUTHORIZED_MAIL_CHANNEL`.

This file is the authoritative project memory. Read it completely before
reopening any branch.

Crash recovery:

1. read this file and `AGENTS.md`;
2. read `docs/final-project-report.md`;
3. run `sha256sum -c MANIFEST.sha256`;
4. run `python3 -m unittest discover -s tests -p 'test_*.py'`;
5. replay the controlling script linked from the gate being inspected.

The only authorized continuation is
`docs/cycles-063-070-preregistration.md`: a circularity audit, a
Roblot/Stark clarification lemma pair, and—only if its genuine-input
gates pass—a counterexample-oriented quartic census screen.

## Original objective

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

## High-level research graph

```text
Original Dedekind-phase conjecture
  |
  +-- Certified Engine-C controls
  |     |
  |     +-- initial controls were circular ------------------ CLOSED
  |     |
  |     +-- independent Roblot constructors
  |             |
  |             +-- 5/5 quarter-turn quantization ----------- POSITIVE
  |             |
  |             +-- raw labels gauge-dependent
  |                     |
  |                     +-- dominant-embedding gauge -------- PROVED
  |                     |
  |                     +-- field-only Dedekind family ------ EXACT NO-GO
  |
  +-- Ray/modulus-specific cocycle pivot
        |
        +-- exact supplied-tuple evaluator ------------------ PROVED
        |
        +-- ray character -> one Kopp tuple ----------------- ILL-TYPED
        |
        +-- class-level multiplier descent ------------------ PROVED
                |
                +-- multiplier is sign-class even
                +-- Stark difference support is sign-class odd
                +-- relevant Fourier resolvent = 0 ---------- EXACT NO-GO
                        |
                        +-- intrinsic metaplectic square root  NEW PROJECT
```

Closed branches remain in this graph deliberately. Do not silently
restart them.

## Headline results

These results must be surfaced in the first report after they are
banked and in any project-level summary:

1. **Five-control phase quantization (`NUMERICAL`).** Five independent
   Roblot weak solutions match certified \(L'\)-balls after a unique
   quarter turn for exactly one of the two conjugate character
   orientations. Cycle 064 found that the archived script selected that
   orientation from the opened target; the fully oriented
   “independent replay” is therefore withdrawn pending exact Artin
   transport. The retained existential two-orientation statement is
   numerical.
2. **Gauge-ambiguity lemma (`VERIFIED`).** Conjugating a cyclic-quartic
   weak solution rotates its character coefficient by \(\mu_4\); the
   raw quarter-turn label is not invariant.
3. **Dominant-embedding gauge (`VERIFIED`).** For nondegenerate log
   orbit \((a,b,-a,-b)\), the unique maximum selects a canonical weak
   solution representative. All five controls are nondegenerate.
4. **Field-only feature no-go (`VERIFIED_EXACT_NO_SOLUTION`).**
   RQ-000129 and RQ-001569 have identical frozen field-only features
   modulo four and different canonical phase labels.
5. **Supplied-tuple cocycle bridge (`VERIFIED`).** One exact formula
   replays five SIC Rademacher invariants, the dimension-four
   multiplier, all 24 dimension-five multipliers, and inversion
   covariance.
6. **Ray-to-form obstruction (`VERIFIED_SCOPE_OBSTRUCTION`).** A
   character-level input does not select the class-level auxiliary
   data required by Kopp's formula.
7. **Class descent (`VERIFIED`).** The 24 dimension-five
   characteristics descend exactly to eight class multipliers.
8. **Fourier parity no-go (`VERIFIED_NO_GO`).** The descended squared
   multiplier is sign-class even, while every character in the
   differenced Stark support is sign-class odd; all four relevant
   Fourier resolvents vanish exactly.
9. **Roblot phase clarification (`PROVED`).** In a certified cyclic
   quartic Stark case the weak/Stark ratio is
   \(\chi(h)^{-1}\in\mu_4\) for a trivial unit \(h\). In an uncertified
   (A1)--(A3) case, this quantization is equivalent to the quartic
   rank-one Stark conjecture itself.

The eighth item is the project's terminal theorem for the frozen
mechanism. It does not rule out a metaplectic square-root refinement.

## Preregistered gates and outcomes

| Gate | Frozen question | Outcome | Consequence |
|---|---|---|---|
| Independence | Is the comparison object independent of \(L'\)? | Initial controls failed; five Roblot constructors later passed | Fitting remained closed until cycle 035 |
| Phase opening | Do sealed independent controls quantize? | 5/5 passed | Positive phenomenon banked |
| Gauge | Is the quarter-turn label intrinsic? | Raw label failed; dominant gauge passed | Canonical response repaired |
| Frozen feature family | Are all preregistered features integral? | Failed on 2/5 rows | Rejected before fitting |
| Field-only repair | Can the natural integral repair fit? | Exact two-row collision | Field-only path closed |
| Cocycle availability | Is a generic extractor already present? | No | Pivoted from fitting to theory |
| Supplied-tuple replay | Does one exact arithmetic layer cover anchors? | Passed | Restricted bridge proved |
| Non-SIC bridge | Does \((K,\mathfrak m,\chi)\) determine one tuple? | No; input levels mismatch | General one-tuple bridge rejected |
| Class descent | Is the multiplier representative-independent? | Passed exactly | Character resolvent authorized |
| Fourier resolvent | Is it nonzero on Stark support? | All four coefficients vanish | Frozen mechanism rejected |
| Stop condition | Would repair require new noncanonical structure? | Yes: an intrinsic metaplectic lift | Project finished at cycle 062 |

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

## Complete cycle ledger

Each row records the task and resulting finding. `Evidence` is the
recovery pointer; failed, blocked, and unauthorized cycles are retained
because they constrain later work.

| Cycle | Task / finding | Status | Evidence |
|---:|---|---|---|
| 001 | Project skeleton and crash-recovery map created | BANKED | this file, `README.md` |
| 002 | Claim boundary and failure criteria frozen before data | BANKED | `data/preregistration-v1.json` |
| 003 | Primary-source perimeter frozen | BANKED | `docs/literature-perimeter-v1.md` |
| 004 | CM-route eligibility shown distinct from Roblot eligibility | BANKED | `docs/scope-audit-v1.md` |
| 005 | Five certified packet controls identified | BANKED | `artifacts/certified-controls-v1.json` |
| 006 | Ten route records extracted; two routes exist per control | BANKED | same |
| 007 | Exact sawtooth and Dedekind arithmetic implemented | BANKED | `src/dedekind.py` |
| 008 | Reciprocity and closed-form arithmetic controls passed | BANKED | tests |
| 009 | Plain Rademacher-\(\Phi\) convention fixed | BANKED | `src/dedekind.py` |
| 010 | Generator and cocycle arithmetic controls passed | BANKED | tests |
| 011 | Certified \(L'\)-phase balls extracted for ten routes | BANKED | `artifacts/control-phase-audit-v1.json` |
| 012 | Raw \(L'\) phases are not quarter-turn quantized | BANKED_NEGATIVE | same |
| 013 | Both proof routes give identical phase balls in all five cases | BANKED | same |
| 014 | Existing Engine-C comparison vectors found dependent on the same \(L'\) data | BANKED_NEGATIVE | `docs/identifiability-audit-v1.md` |
| 015 | Formula-family freeze blocked because no independent response existed | BLOCKED | independence gate |
| 016 | Feature-rank audit rejected fitting as circular | BANKED_NEGATIVE | `artifacts/control-phase-audit-v1.json` |
| 017 | Fifty-row holdout could not be defined independently | BLOCKED | response absent |
| 018 | Fitting withheld because it would be tautological | NOT_AUTHORIZED | independence gate |
| 019 | Holdout withheld because its target was absent | NOT_AUTHORIZED | independence gate |
| 020 | Feasibility halt banked; independent weak solution named as next gate | BANKED | `docs/cycle-020-checkpoint.md` |
| 021 | Roblot's quartic construction translated into executable exact steps | BANKED | source audit |
| 022 | All five original fields passed genuine Roblot (A1)--(A3) screening | BANKED | `artifacts/roblot-quartic-gate-sealed-v1.json` |
| 023 | First constructor exposed a fixed-lattice proxy error; failed version preserved | PRESERVED_FAILURE | v1 artifact |
| 024 | Genuine embedded \(K^+\)-unit lattice corrected the norm index to two | BANKED | `artifacts/roblot-rq000129-constructor-sealed-v2.json` |
| 025 | RQ-000129 gave the first independent quarter-turn phase match | BANKED | `artifacts/rq000129-phase-gate-v1.json` |
| 026 | Remaining constructors and feature protocol sealed before opening phases | BANKED | `docs/cycles-026-045-preregistration.md` |
| 027 | \(\mathbf Q(\sqrt{35})\) unit and norm data reconstructed exactly | BANKED | constructor transcript |
| 028 | RQ-001280 independent constructor sealed | BANKED | `artifacts/remaining-roblot-constructors-sealed-v1.json` |
| 029 | RQ-001569 relative class/Fitting data computed | BANKED | same |
| 030 | RQ-001569 independent constructor sealed | BANKED | same |
| 031 | RQ-007519 relative class/Fitting data computed | BANKED | same |
| 032 | RQ-007519 independent constructor sealed | BANKED | same |
| 033 | RQ-001894 norm index found to be four, giving exponent two | BANKED | same |
| 034 | RQ-001894 independent constructor sealed | BANKED | same |
| 035 | All four remaining constructors replayed byte-consistently | BANKED | same |
| 036 | Four remaining phase balls opened only after the seal | BANKED | `artifacts/all-five-phase-gates-v1.json` |
| 037 | A unique direct/inverse character orientation resolved every control | BANKED | same |
| 038 | Five of five independent controls passed quarter-turn quantization | BANKED | same |
| 039 | Gauge-ambiguity lemma proved: weak-solution conjugation rotates by \(\mu_4\) | BANKED | `docs/gauge-ambiguity-lemma-v1.md` |
| 040 | Gauge action replayed on all five controls | BANKED | same |
| 041 | Five fundamental-unit \(SL_2(\mathbf Z)\) matrices computed exactly | BANKED | `artifacts/frozen-feature-family-audit-v1.json` |
| 042 | Exact Rademacher/Dedekind features exposed two nonintegral rows | BANKED | same |
| 043 | Preregistered feature family rejected before fitting | BANKED_NEGATIVE | same |
| 044 | Dominant gauge proved; field-only repair failed by an exact two-row collision | BANKED_NEGATIVE | `artifacts/field-only-dedekind-family-no-go-v1.json` |
| 045 | Existing cocycle code found SIC-specific; project pivoted from fitting to theory | BANKED | `docs/cycle-045-checkpoint.md` |
| 046 | Ray-class cocycle target, conventions, anchors, and outcomes frozen | BANKED | `docs/cycles-046-055-preregistration.md` |
| 047 | Dimension-four supplied-tuple multiplier formula extracted exactly | BANKED | `docs/sic-bridge-extraction-v1.md` |
| 048 | Dimensions 5/7/8 separated universal arithmetic from SIC-specific tuple inputs | BANKED | same |
| 049 | Proposed ray-character-to-one-tuple map shown to mix character and class levels | BANKED_NEGATIVE | `docs/ray-to-form-obstruction-v1.md` |
| 050 | Exact supplied-tuple cocycle evaluator implemented | BANKED | `src/cocycle.py` |
| 051 | Five \(\Psi\) anchors and 25 full multipliers replayed exactly | BANKED | `artifacts/supplied-tuple-bridge-audit-v1.json` |
| 052 | RQ-000129 lacked canonical Kopp auxiliary data; generic one-tuple gate failed | BANKED_NEGATIVE | `artifacts/rq000129-ray-to-form-gate-v1.json` |
| 053 | Character inversion proved and replayed to conjugate the multiplier | BANKED | `docs/cocycle-covariance-v1.md` |
| 054 | Five-control feature test withheld after its prerequisite failed | NOT_AUTHORIZED | generic bridge gate |
| 055 | `RESTRICTED_SIC_BRIDGE` verdict banked; class Fourier resolvent proposed | BANKED | `docs/cycle-055-checkpoint.md` |
| 056 | Class-descent, resolvent, repair, and terminal stop conditions frozen | BANKED | `docs/final-block-preregistration.md` |
| 057 | All three representatives of each dimension-five ray class agreed | BANKED | `artifacts/class-descent-fourier-no-go-v1.json` |
| 058 | Exact eight-class multiplier table emitted | BANKED | same |
| 059 | Descended multiplier proved invariant under sign class \(R\) | BANKED | same |
| 060 | All four Fourier coefficients on the \(R\)-odd Stark support vanished exactly | BANKED_NEGATIVE | same |
| 061 | Odd square-root repair identified as a new metaplectic theorem, not an in-scope correction | OUTSIDE_FROZEN_MECHANISM | `docs/class-descent-fourier-no-go-v1.md` |
| 062 | Preregistered stop condition fired; project closed with terminal no-go | BANKED | `docs/final-project-report.md` |
| 063 | Roblot phase clarification branch preregistered; no old fitting or squared-multiplier path reopened | BANKED | `docs/cycles-063-070-preregistration.md` |
| 064 | Circularity audit: weak unit and dominant gauge pass, but the archived script selected direct/inverse orientation from the opened target | CONTAINED_CORRECTION | `docs/circularity-audit-v1.md`, `artifacts/circularity-audit-v1.json` |
| 065 | Certified-case lemma: the phase ratio equals \(\chi(h)^{-1}\in\mu_4\) by Roblot uniqueness | PROVED | `docs/roblot-phase-clarification-lemma-v1.md` |
| 066 | Uncertified-case lemma: phase quantization is equivalent to the cyclic-quartic rank-one Stark conjecture under (A1)--(A3) | PROVED | same |
| 067 | Census population audit: the 2,704-row H-stratum exists, but the genuine Roblot-eligibility column has not been constructed | BLOCKED_INPUT | `docs/quartic-census-readiness-audit-v1.md` |
| 068 | Rigorous-evaluator audit: \(L'\) balls exist, but weak-unit Fourier coefficients are point evaluations, not Arb balls | BLOCKED_INPUT | same, `artifacts/quartic-census-readiness-audit-v1.json` |
| 069 | Phase census halted before target opening under the preregistered population/evaluator gates | GATED_STOP | same |
| 070 | Long Roblot outreach draft prepared with three falsifiable questions, AI disclosure, replay hash, the exact \(\mu_4\) corollary, and the withdrawn-orientation boundary; no message sent | DRAFTED_NOT_SENT | `docs/roblot-email-long-draft-v1.md` |

| 071 | Results v1.4 was published; the official Lyon 1 and ICJ pages confirmed the recipient address; the long message and companion v17 pass readiness checks, but no authorized mail channel exists in the environment | READY_AWAITING_AUTHORIZED_MAIL_CHANNEL | `docs/cycle-071-roblot-outreach-readiness.md`, `artifacts/roblot-email-send-readiness-v1.json` |

## Final synthesis

The project first rejected its original controls as circular, then
constructed five independent Roblot weak solutions. All five exhibit a
unique fourth-root phase relation after character alignment
(`NUMERICAL` against certified \(L'\)-balls).

The clarification branch later found that the archived direct/inverse
orientation was selected from the opened target. The fully oriented
independent-replay wording is withdrawn; the weaker two-orientation
observation remains numerical. More importantly, the exact lemma pair
shows that the phenomenon is automatic in already certified Stark
cases and equivalent to the quartic Stark conjecture in uncertified
ones.

The raw label is gauge-dependent. A dominant-embedding gauge repairs
the response, but the field-only Dedekind family fails exactly. The
subsequent cocycle pivot proves a universal supplied-tuple evaluator
while showing that a ray character does not select one Kopp tuple.

The final block proves that the class multiplier nevertheless descends,
but is invariant under the sign class. Every character in the
differenced Stark support is odd on that sign class, so the proposed
Fourier resolvent vanishes identically. Arbitrarily choosing an odd
square-root lift would insert the desired orientation; constructing one
intrinsically requires a new metaplectic theorem outside the frozen
mechanism.

Therefore the project is finished with status
`FINISHED_WITH_VERIFIED_NO_GO_FOR_FROZEN_MECHANISM`: the phase
quantization phenomenon remains interesting, but this
Dedekind/squared-multiplier explanation is closed.

## Evidence map

- final report: `docs/final-project-report.md`;
- phase controls: `artifacts/all-five-phase-gates-v1.json`;
- gauge results: `docs/gauge-ambiguity-lemma-v1.md` and
  `docs/dominant-embedding-gauge-v1.md`;
- field-only no-go:
  `artifacts/field-only-dedekind-family-no-go-v1.json`;
- supplied-tuple theorem:
  `artifacts/supplied-tuple-bridge-audit-v1.json`;
- ray-to-form obstruction:
  `docs/ray-to-form-obstruction-v1.md`;
- terminal Fourier no-go:
  `docs/class-descent-fourier-no-go-v1.md` and
  `artifacts/class-descent-fourier-no-go-v1.json`.

## Next authorized action

For the correction/publication lane, results version 1.4 is public at
DOI `10.5281/zenodo.21712478`. All seven public downloads match the
frozen local byte counts, MD5 checksums, and SHA-256 checksums. Evidence
is in
`../effective-stark-sweep/artifacts/zenodo-results-publication-v5.json`.
The next authorized action is the long Roblot email in
`docs/roblot-email-long-draft-v1.md`: use the public DOI and companion
v17 and send through an authorized mail channel. The recipient was
verified on the official Lyon 1 homepage and ICJ directory. No mail
connector or local SMTP client is present in the current environment,
so no delivery is claimed. Readiness evidence is in
`artifacts/roblot-email-send-readiness-v1.json`.

For research, return to the census screen only after the census project
has banked a genuine Roblot-eligible quartic population, this project
has an anchor-validated Arb weak-coefficient evaluator, and exact
Artin transport fixes the analytic orientation before \(L'\) is read.

## Tags

`VERIFIED`, `NUMERICAL`, `CONJECTURAL`, `BLOCKED`, and
`BANKED_NEGATIVE` retain their literal meanings. No fitted formula
will receive a theorem tag without a written reciprocity proof.
