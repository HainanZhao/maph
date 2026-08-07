# C(23,6,2) exact SAT toolchain

This note pins the independent checker required by
`cover_23_6_2_bounded_experiment.py`. It does not authorize or start the
bounded experiment.

## Solver

- CaDiCaL 1.7.3 at `/usr/bin/cadical` on the audited host.
- The coordinator records the executable's SHA-256 digest in each run.
- Proofs are requested in CaDiCaL's default binary DRAT format. `OBSERVED`:
  an initial 62-second instrumentation tranche produced 1,684,017,152 bytes
  of plain DRAT across three branches; keeping it would have wasted the fixed
  disk and compute allocation. The continuation conservatively charges 190
  core-seconds and 64 wall-seconds to that tranche.
- `OBSERVED`: a second 70.4-second binary-proof instrumentation tranche used
  206.4 charged slot-seconds and produced 951,573,046 output bytes. The final
  decision-first continuation conservatively charges both tranches together
  as 405 core-seconds and 140 wall-seconds.
- The final coordinator first runs all canonical branches without proof
  logging. A branch returning UNSAT is queued for proof regeneration and
  independent checking only after the decision screen. This preserves the
  possibility of finding and directly verifying a cover without making every
  undecided search pay continuous proof-I/O cost.

## Independent checker

- Upstream: `https://github.com/marijnheule/drat-trim.git`
- Release tag: `v05.22.2023`
- Commit: `2e5e29cb0019d5cfd547d4208dca1b3ec290349f`
- Build command: `make drat-trim` using GCC with `-std=c99 -O2`.
- Source `drat-trim.c` SHA-256:
  `f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26`.
- Local executable SHA-256:
  `a48ebed7b4b6b373d3ddbeb3368dae7622a9e17bab7fe6eb751ab996757f9fbe`.

The pinned local checkout is
`discovery/out/toolchain/drat-trim-v05.22.2023/`; `discovery/out/` is
noncanonical working storage. The coordinator records the exact checker
binary hash again in the run summary.

## Independent smoke control

`CERTIFIED_NUMERICAL`: CaDiCaL returned code 20 on the four-clause
two-variable contradictory control, emitted a binary DRAT proof, and the
pinned `drat-trim` binary returned code 0 with `s VERIFIED`. This validates
the solver-to-checker file-format interface only; it says nothing about
`C(23,6,2)`.
