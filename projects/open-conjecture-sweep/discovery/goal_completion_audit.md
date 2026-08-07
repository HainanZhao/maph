# GOAL.md completion audit

This audit maps each requirement to authoritative evidence so completion does
not rely on chat memory.

Goal specification:
`../docs/completed-goal-three-topic-closure-2026-08-07.md`.

## Primary and secondary goals

Requirement: every listed topic reaches Outcome A, B, or C under its stated
stop condition, with at most one open-ended proof search at a time.

- Topic 3: **proved complete** below.
- Topic 2: **proved complete** below.
- Topic 1: **proved complete** below.
- `PROGRAM.md` separately names the user-selected F001 book-Ramsey problem as
  active. Git records its selection in `01945bc4`, before `591c1b13`
  introduced this three-topic GOAL, so it was not opened while this queue was
  unresolved. No F001 executable search is concurrent with this run, and
  Topic 1 is a fixed resource-bounded experiment rather than open-ended proof
  search. The secondary limit of at most one open-ended search is therefore
  met; this audit does not claim that no fourth project problem exists.

## Topic 3 — width-four q-Fibonomial unimodality

- Required outcome: uniform proof or refutation, replayable and written.
- Evidence: `proof/qfib_width4_unimodality_proof.md` proves unimodality for
  every `m >= 1`; `paper/qfib-width-four/main.tex` is the written manuscript.
- Replay: `python3 proof/qfib_width4_unimodality_proof.py`.
- Expected anchors: partition formula through 300, finite proof bases
  `m=1,...,7`, direct quotient cross-check through 24.
- Current SHA-256 values for the proof script, proof note, manuscript source,
  and PDF exactly match `paper/qfib-width-four/verification.md`.
- Git reports the complete Topic 3 evidence tree clean; `591c1b13` introduced
  the proof and `63cfe267` contains the archived manuscript state.
- Fresh post-relocation replay from `projects/open-conjecture-sweep/` on
  2026-08-07 returned all three expected anchors in 1.85 seconds wall time
  and 99,368 KiB peak RSS.
- Ledger: `../../RESULTS_LEDGER.md`, 2026-08-06 Topic 3 entry, Outcome A.
- Postmortem: `../../POSTMORTEMS.md`, Topic 3 entry.
- Audit status: **COMPLETE**.

## Topic 2 — Conjecture 5.4 at k=r=4

- Required outcome: prove the target by 2026-10-31 or retain the stated
  self-contained Outcome B reduction.
- Stronger evidence: `proof/qanalog_conjecture54_sufficiency.md` proves the
  full sufficient direction for every `k >= 1`, `r >= 2`, hence the target.
  The proof has independent algebraic and coefficient-partition derivations
  of its aligned-center identity.
- Written record: `paper/qanalog-multispacer-criterion/main.tex`, the combined
  paper that retains the full sufficient-direction theorem.
- Replay: `python3 proof/qanalog_multispacer_criterion.py`.
- Expected anchors include 1,680 two-route recursion identities, 15,163 exact
  one-spacer induction rows, 43,002 nested recursion steps, and final status
  `COMBINED_CRITERION_PASS`.
- Current SHA-256 values for the combined manuscript source, PDF, and replay
  script exactly match `paper/qanalog-multispacer-criterion/verification.md`.
- Git reports the combined manuscript and replay tree clean; `dd26d7f7`
  contains the merge and `2a5c01a6` the current refined evidence.
- The preparatory community-value and numerical-boundary checks named in the
  archived goal are recorded in `discovery/qanalog_k4_r4_audience_boundary.md`;
  they were completed before the stronger proof.
- Fresh post-relocation replay from `projects/open-conjecture-sweep/` on
  2026-08-07 returned all expected component passes and final
  `COMBINED_CRITERION_PASS` in 12.29 seconds wall time and 16,760 KiB peak
  RSS.
- Ledger: later 2026-08-06 entry in `../../RESULTS_LEDGER.md`, Outcome A,
  explicitly superseding the earlier Outcome B entry.
- Postmortem: `../../POSTMORTEMS.md`, Topic 2 entry.
- Audit status: **COMPLETE**.

## Topic 1 — C(23,6,2)

- Required experiment: one fixed allocation of 24 aggregate core-hours and
  eight wall-hours, ending on a directly verified cover or budget exhaustion.
- Exact branch equivalence: `discovery/cover_23_6_2_encoding.md` and the
  eleven-case inventory produced by
  `discovery/cover_23_6_2_bounded_experiment.py --inventory`.
- Independent replay
  `python3 proof/verify_cover_23_6_2_branch_partition.py` returned
  `STAR_ORBIT_ENUMERATION_PASS: 1 + 3 + 7 = 11`: one multiplicity-four
  orbit, three `3+2` intersection orbits, and all seven loopless
  three-edge-multigraph orbits for `2+2+2`. It enumerates the multigraph
  orbits independently and then compares them with the encoder's cases. The
  same replay independently enumerates the four surviving partitions of
  total replication excess five and matches the CNF's degree selectors. It
  also reconstructs all eleven canonical stars and verifies five rows of size
  six, coverage of all 23 points, and exactly three repeated incidences.
- Independent finite replay
  `python3 proof/verify_cover_23_6_2_cnf_primitives.py` returned
  `CNF_PRIMITIVES_EXHAUSTIVE_PASS` on 4,826 rows in 0.36 seconds. A separate
  DPLL implementation exhaustively checks the encoder's sequential
  cardinality, exact and guarded-exact, lexicographic, and conjunction
  primitives on all frozen small controls.
- Fresh SHA-256 recomputation of the coordinator, both encoding modules, and
  both mathematical notes exactly matches Wave 3's embedded frozen-input
  manifest; the completed run did not drift from its recorded inputs.
- Byte comparison of all five regenerated Wave 3/4 CNFs against their
  independently generated balanced-run copies returned
  `CROSS_WAVE_CNF_BYTES_PASS`.
- All 16 CNF files in the canonical archive set—eleven selected copies plus
  five earlier independent copies—match their recorded SHA-256 values,
  DIMACS variable/clause headers, and complete clause terminators:
  `CNF_MANIFEST_AND_DIMACS_PASS`.
- The replayed CaDiCaL executable reports version 1.7.3 and hashes to
  `7b73df0a...b8b33e`; the pinned `drat-trim` hashes to
  `a48ebed7...f9fbe`. Both full hashes exactly match Wave 3's summary.
- Independent terminal archive replay
  `python3 proof/verify_cover_23_6_2_bounded_archive.py` returned
  `ARCHIVE_TERMINAL_PASS` after checking all eleven terminal logs,
  regenerating all eleven canonical DIMACS byte streams, matching all 16
  canonical/cross-wave manifest entries, both resource priors, all frozen
  input hashes, and both locally available tool hashes. It requires no derived
  CNF files in a fresh checkout and rejects any unfinished log.
- Wave 1/2 evidence:
  `discovery/out/cover-23-6-2-bounded-balanced-20260807/`. Its first three
  statuses were captured by the coordinator; the next three are classified
  from their solver-written terminal lines because the host terminated the
  coordinator while its independently limited children remained alive.
- Budget-chain audit: the stopped runs' recorded aggregate
  core/wall seconds are `398.15/134.37` and `1788.70/601.73`; their successor
  priors round upward to `405/140` and `1800/610`. Six exact 6,900-second
  terminal logs plus file timestamps and coordinator allowance fit below the
  Wave 3 priors `43300/14500`. No stopped work was reset or undercharged.
  The archive verifier reconstructs every handoff inequality and returns
  `CONSERVATIVE_PRIORS_PASS`.
- Wave 3 evidence:
  `discovery/out/cover-23-6-2-wave3-20260807/`; `222-triangle`,
  `222-triple`, and `32-overlap0` all reached 6,800.00 seconds with no
  decision and terminal `exit 0`.
- Final Wave 4 launched exactly `32-overlap1` and `32-overlap2`, each with a
  7,399-second internal limit, under
  `discovery/out/cover-23-6-2-wave4-20260807/`.
- Mechanical set comparison returned `BRANCH_PARTITION_PASS`: the nine
  terminal and two final-wave names are disjoint and their union is exactly
  the runner's eleven-branch inventory.
- All eleven branches report `UNKNOWN_SOLVER_LIMIT`. The final branches each
  ran for exactly 7,399.00 real seconds; their SHA-256 log hashes are
  `da351553...f99666` and `b9c416ad...b3ed8d`. Exact per-branch runtimes,
  memory, conflicts, decisions, and complete hashes are regenerated by the
  terminal archive replay and summarized in
  `discovery/cover_23_6_2_bounded_outcome.md`.
- The raw Wave 4 summary records 78,622.98 aggregate charged seconds and
  28,800.07 aggregate wall seconds. Although its status is `INCOMPLETE`
  because both internally limited children exited between coordinator polls,
  the independent verifier checks the numeric meter and all terminal logs,
  derives `WALL_CAP_DERIVED`, and returns `ARCHIVE_TERMINAL_PASS`.
- The fixed eight-hour wall stop condition is therefore met without a
  verified cover. Topic 1 is **Outcome C**. This proves only resource-bounded
  closure; it proves neither `C(23,6,2)=20` nor `C(23,6,2)=21`.
- Ledger: `../../RESULTS_LEDGER.md`, 2026-08-07 Topic 1 entry, Outcome C.
- Postmortem: `../../POSTMORTEMS.md`, Topic 1 entry.
- Audit status: **COMPLETE**.

## Final verification commands

```sh
python3 proof/qfib_width4_unimodality_proof.py
python3 proof/qanalog_multispacer_criterion.py
python3 proof/verify_cover_23_6_2_branch_partition.py
python3 proof/verify_cover_23_6_2_cnf_primitives.py
python3 proof/verify_cover_23_6_2_bounded_archive.py
python3 discovery/cover_23_6_2_bounded_experiment.py --inventory
python3 -m unittest tests.test_cover_23_6_2_verifiers -v
```

Run these from `projects/open-conjecture-sweep/`. On the terminal repository
state, the two topic proofs, independent orbit verifier, 4,826-row CNF control,
11-branch archive regeneration, inventory, and all nine regression tests
passed. The fresh-checkout test copied only summaries and logs to a CNF-free
temporary archive and reproduced the terminal result by regenerating all
eleven DIMACS streams in memory. Every wave summary was reconciled with its
solver-written terminal lines, every recorded hash passed, and no solver or
coordinator process remained.
