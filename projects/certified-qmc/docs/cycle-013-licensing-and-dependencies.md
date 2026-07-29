# Cycle 013 — licensing, vendoring policy, and release dependencies

Date: 2026-07-29

Status: `G1 PASSED`

## Dependency gate

The release target is now `make -C native release`.  Its graph contains
only the project-owned direct and frozen streaming kernels.  The
streaming binary's only ELF `NEEDED` entries are `libgomp.so.1` and
`libc.so.6`; the direct evaluator needs only `libc.so.6`.  No FFTW, GMP,
FLINT, or other third-party mathematical object is linked.

A clean-room copy containing only the release Makefile and two C sources
was compiled with an empty package-config path and a compiler wrapper
that rejects any FFTW argument.  Both binaries built successfully and
were byte-identical to the ordinary release build.  `ldd`, ELF
dependencies, build commands, source hashes, compiler, flags, and CPU
are banked in `certificates/cycle-013-dependency-manifest.json`.

The historical FFTW/LatNet harness has moved to
`tools/numerical-crosscheck/`.  It has an explicit `NUMERICAL` boundary,
its own opt-in Makefile, no edge from the release graph, and
`export-ignore` packaging status.

## Source terms and vector disposition

The exact response bodies and headers retrieved during this cycle are
archived under `third_party/terms/2026-07-29/`.

- UNSW lattice page: `UNCLEAR`.  It offers and documents vectors but
  states no redistribution license.
- Magic Point Shop: `UNCLEAR`.  It requests citation and displays
  copyright but states no redistribution license.
- QMCPy at frozen commit `a774f3a…`: `REDISTRIBUTABLE` under
  Apache-2.0 conditions.

No source is classified `PROHIBITED`.  The production vectors come from
the `UNCLEAR` UNSW source, so release v1 uses keyed merits without
embedded vectors.  Each entry binds its source citation, full snapshot
hash, index, and generator-prefix hash.  This is the default directive
path and requires no human escalation.

## Artifact licenses

- Engine code: Apache-2.0 (`LICENSE`).
- Project-authored tables and data: CC-BY-4.0 (`LICENSE-DATA`).
- Third-party terms snapshots and vectors are excluded from the
  project-authored data grant.

The choice and rationale are recorded in `docs/licensing.md`.

## Kernel freeze

The release Makefile hard-codes the passing pilot flags.  The frozen
production kernel remains `native/streaming_pilot.c` with SHA-256
`f21c5cc9ab825ea402258fd5832e7ee0b33ebf5f60c2c3fab9cec7484339dd42`.
No optimization or compiler-flag change is authorized before release.

## Exit gate

- dependency manifest: passed;
- per-source classification: passed;
- clean-room build without FFTW: passed;
- code and data license texts: present;
- embedding escalation: not triggered.

Cycle 014 may begin.
