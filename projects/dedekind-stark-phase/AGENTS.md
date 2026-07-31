# Project instructions: Dedekind--Stark phase

The repository-wide instructions in `../../AGENTS.md` apply.

## Mandatory entry sequence

Before changing or extending this project, read in order:

1. `PLAN.md` in full;
2. `docs/final-project-report.md`;
3. the preregistration document controlling any branch proposed for
   reopening;
4. the evidence artifact linked from the relevant `PLAN.md` gate.

`PLAN.md` is the authoritative project memory. Chat summaries are
secondary.

## Current project status

This project is finished with status
`FINISHED_WITH_VERIFIED_NO_GO_FOR_FROZEN_MECHANISM`.

Do not resume coefficient fitting, enlarge the holdout, or reinterpret
the vanished Fourier resolvent as an engineering problem. Reopening
requires a genuinely new branch—currently the only plausible one is an
intrinsic metaplectic or spin orientation—and that branch must receive
its own objective, claim boundary, preregistration, and stop condition
in `PLAN.md` before computation.

## Reporting rule

Every block report must surface newly banked headline mathematics. For
this project, the standing headline results are listed in `PLAN.md`.
Their epistemic tags must be repeated accurately: the five-control
phase quantization is numerical against certified \(L'\)-balls, while
the gauge lemma, supplied-tuple arithmetic, class descent, and Fourier
cancellation are exact.

## Artifact discipline

- Do not edit banked JSON artifacts to accommodate a new convention;
  issue a versioned successor with a correction record.
- Preserve preregistrations and failed paths.
- Run `sha256sum -c MANIFEST.sha256` and the complete unit suite before
  committing.
- Recovery begins from `PLAN.md`, not from filenames guessed by date.
