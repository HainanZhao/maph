# C100 rolling pivot audit

`OBSERVED` audit of the last 100 numbered cycles (C1--C100), using the
selection packets, no-selection decisions, boundary headers, and the current
`PROGRAM.md`.  A pivot is counted only when the program authorizes a materially
different target or problem-level engine.  Routine continuation, a failed
subtest, a resource cap, a correction, and a no-selection screen are not
counted as pivots.

## Result

The window contains **16 material pivots**, well above the three-pivot
threshold:

| cycle | transition |
|---:|---|
| 66 | S3 Zhao fixed-group route after the C65 hard stop |
| 69 | Sidorenko → intersecting Ryser (r=6) |
| 73 | Ryser defect route → fresh Q7 / portfolio re-selection |
| 75 | ineligible Holevo--Utkin (d=4) reconstruction |
| 76 | Holevo--Utkin → compatible-marginal spin alignment |
| 80 | spin alignment → quaternary Legendre pairs |
| 84 | LEM → LRC composite-polynomial bridge |
| 85 | LRC → Möbius-ladder Sidorenko tensor route |
| 86 | Sidorenko → height-four Frankl Hall transport |
| 87 | Frankl → Ryser private-region absorption |
| 89 | Ryser → Sidorenko rank-one escape |
| 91 | Sidorenko → Ryser deletion-cover trace |
| 92 | Ryser → Frankl temperature witness |
| 93 | Frankl → LEM free amalgam |
| 95 | LEM → Bollobás--Meir Boolean (Q_4) gate |
| 100 | Diophantine screen → Erdős--Szekeres (ES(7)) gate |

C98 was a continuation within the Diophantine target, and C99 was
`NO_SELECTION`; neither is counted.  The count is therefore conservative:
counting every newly named method packet rather than only problem changes
would be higher.

## Decision

The rolling-window guard in `PROGRAM.md` is now active.  C100 must remain in
the same Erdős--Szekeres question and frozen SAT method family while the
resource continuation is completed; the observed OOM is a contained resource
result, not a pivot trigger.
