# C(23,6,2) bounded-experiment budget recommendation

Decision status: recommendation only. `GOAL.md` is user-owned, its budget
fields remain blank, and no new covering search is authorized by this note.

## Recommended fixed allocation

- Aggregate compute: **24 core-hours**.
- Wall-clock: **8 hours**.
- Parallelism: at most three solver processes/threads on this four-CPU host.
- Memory: at most 10 GiB aggregate.
- Temporary disk: at most 117 GiB, based on 122 GiB free at the 2026-08-06
  audit and the repository rule reserving 5 GiB.
- No extension.

This is large enough to measure the eleven exhaustive canonical-star
branches beyond their existing ten-minute probes, while remaining small
enough to enforce Topic 1's low-payoff kill discipline. Balanced dynamic
sharding should spend the aggregate cap across branches rather than granting
the cap independently to each branch.

## Evidence for the scale

`OBSERVED`: the exact neighborhood engine returned UNSAT at radii
`2,4,6,8,10` in respectively `0.04, 0.65, 3.21, 24.55, 315.02` seconds.
This superlinear growth rules out extrapolating the small radii as evidence
that the global problem is cheap.

`OBSERVED`: all ten canonical `(3+2)` and `(2+2+2)` star-support branches
reached their 600-second CaDiCaL limit without a decision. A broader labelled
run remained undecided after 1,800 seconds. Peak memory in these runs ranged
from roughly 130 MiB to 362 MiB; the alternate set-cover encoding reached
2.39 GiB at 600 seconds without a decision.

`PROVED`: the canonical-star cases are exhaustive for the three repeated-slot
patterns once a replication-five point is fixed, as recorded in
`cover_23_6_2_encoding.md` and `cover_23_6_2_star_cases.py`. A SAT result is
accepted only after direct recounting of all 253 pairs. An UNSAT claim still
requires a retained proof and an independent checker; CaDiCaL's status line
alone is insufficient.

## Stop interpretation

- A directly verified 20-block family gives Outcome A.
- If aggregate resources expire, record the encoding, branch inventory,
  observed scaling, and solver status, then take Outcome C exactly as
  `GOAL.md` permits.
- If proof logging projects more than **240 core-hours** (ten times the
  recommended allocation), take Outcome C without attempting that proof.
- A timeout, unchecked UNSAT line, or incomplete branch union is never a proof
  that `C(23,6,2)=21`.

Falsifier: a missing canonical-star orbit, an invalid decoded cover, a branch
receiving more than its share of the aggregate cap, or an UNSAT promotion
without independent proof checking invalidates the affected outcome.
