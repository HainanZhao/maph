# Agent instructions: sic-stark

This file is the shared instructions file for coding agents working in
this project (`CLAUDE.md` and `GEMINI.md` in this directory are
symlinks to this file — edit only this file).

**For the generic Zenodo/PARI-GP/TeX toolchain knowledge** (API
mechanics, the macOS PARI/GP 2.15.4 stack-resize bug, GNU find/tar,
BasicTeX setup) **see the repository root `AGENTS.md`** — that
knowledge applies to any project in this monorepo that publishes to
Zenodo, not just this one. This file only covers what's specific to
sic-stark.

## Preregistration presentation

The embedded `research-freeze-v1` manifest is the sole authoritative list of
frozen parameters, formulas, selection rules, resource caps, and failure
rules. Keep the prose around it to the question, claim boundary, and a short
plain-language interpretation; do not repeat the same specification in a
second human-readable list.

## What this project is

A companion-paper series proving (or, for dimension six, exploring
without yet proving) cases of the formal Twisted Convolution
Conjecture. Each paper has:

- a manuscript in `paper/*.tex` / `paper/*.pdf`;
- exact certificates (PARI/GP `.gp` scripts, Python/python-flint/Arb
  scripts) under `scripts/`, with outputs recorded in `certificates/`;
- regression tests under `tests/`;
- a submission-specific reproducibility archive built by
  `scripts/build_companion_archives.sh` and described by files in
  `publication/paper-<N>-*`.

Current papers: I = dimensions four/five, II = dimensions seven/eight
(both unconditional, closed proofs), III = dimension six (a research
note; the central claim was retired pending a derivation, and the
result remains conditional on an open conjecture — see the paper's own
"Statement and proof status" and "Scope and reproducibility"
sections). **Always check a paper's own stated scope before writing
Zenodo metadata for it** — polished framing is fine, but the
description must stay truthful to what the paper actually claims.

**Note on Paper II's scope**: a commit (`46db8a0`, "prove
dimension-seven discriminant-eight stratum", authored by `hainzhao
<hainzhao@gmail.com>`) expanded Paper II's manuscript to also cover the
dimension-seven discriminant-8 stratum, previously explicitly out of
scope ("The discriminant-8 dimension-seven stratum is not claimed
there"). That commit landed *after* Paper II v1/v2 were already
published to Zenodo (`10.5281/zenodo.21681700` / `.21682196`) with the
narrower scope. If you're picking this up: check whether the
currently-published Zenodo record's manuscript matches the current
repo's manuscript scope before doing anything else — if it doesn't, a
new Zenodo version is needed to keep the public record honest. Also:
that commit (and others, e.g. `094b560`, `f5bb5ed`, `9f70d53`) came
from git identity `hainzhao <hainzhao@gmail.com>`, distinct from the
interactive session's configured `Hainan Zhao
<hainan.zhao@grasshopperasia.com>` — something else appears to be
actively committing and pushing to this exact repository outside of
any interactive session. Run `git log` and `git fetch && git log
HEAD..origin/main` before assuming the working tree only reflects your
own edits.

## Publishing a new companion paper: project-specific steps

Follow the root `AGENTS.md` for environment setup (PARI/GP, TeX, GNU
tools) and the Zenodo API mechanics (reserve DOI, upload, verify
checksums, publish, newversion). The sic-stark-specific parts are:

1. Confirm the paper's own claimed scope (proof vs. research note) by
   reading its abstract and "Scope and reproducibility"/similar
   section — don't infer from the series' other papers.
2. Create `publication/paper-<N>-{README.md,REPRODUCE.md,CITATION.cff,
   zenodo.json}`, modeled on the existing `paper-I-*` / `paper-II-*` /
   `paper-III-*` files. Keep the Zenodo `description` accurate to what
   the paper itself claims, even if the visual/structural style
   matches other papers in the series.
3. Extend `scripts/build_companion_archives.sh`: add a
   `paper_<n>_files()` function following the existing
   `paper_one_files`/`paper_two_files`/`paper_three_files` pattern
   (common release files + this paper's `publication/` metadata + its
   `.tex`/`.pdf` + relevant `docs/`, `certificates/`, `scripts/`,
   `tests/` via `add_matches` regexes), then wire it into
   `build_one()`'s dispatch, the `--paper` argument validation/usage
   text, and the `case "$selection" in ... all) ... esac` block.
   - **Watch for cross-paper script imports.** A naming-pattern regex
     (e.g. `scripts/dimension_six_.*`) will miss a shared helper script
     from a different dimension that a `.gp`/`.py` script imports
     (e.g. `dimension_six_cycle143_gate.py` imports
     `certify_dimension_five_double_sine`). These only surface as
     `ModuleNotFoundError` when you run the test suite against the
     **extracted** archive, not the live repo tree (the live repo has
     every file, so nothing looks missing until you check the tarball
     in isolation). Grep every new paper's scripts for `^import`/`^from`
     lines and add any file outside its own naming pattern explicitly.
4. Update `tests/test_companion_archives.sh`'s `for paper in I II III`
   loop and its per-paper membership assertions to include the new
   paper.
5. Cross-reference DOIs: this paper's own reproducibility section and
   `CITATION.cff` get its own DOI; its bibliography entries for other
   papers in the series get their DOIs; and (unless there's a reason
   not to) the other papers' bibliographies should cite this one back.

## Already-published records

| Paper | Concept DOI (latest) | v1 (cited in manuscripts) | Latest version (adds standalone PDF/tex) |
|---|---|---|---|
| I (dims 4–5) | `10.5281/zenodo.21680222` | `10.5281/zenodo.21680223` | `10.5281/zenodo.21682192` |
| II (dims 7–8) | `10.5281/zenodo.21681699` | `10.5281/zenodo.21681700` | `10.5281/zenodo.21682196` |
| III (dim 6, research note) | — | `10.5281/zenodo.21682631` | (same; standalone PDF/tex were included from the first publish) |

Manuscripts cite the v1 DOIs (the exact archive built and hash-verified
alongside the paper), not the latest-version DOIs — Zenodo's version
selector and the concept DOI both make the latest version reachable
regardless.
