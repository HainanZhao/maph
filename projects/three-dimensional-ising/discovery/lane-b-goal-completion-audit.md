# Lane B goal completion audit

## Terminal claim

`PROVED`: terminal outcome 1 in `LANE_B_GOAL.md` is met for the declared free
minimum-genus family `P_L square P_3 square P_3`, `L>=4`: Gate 3 survives a
held-out growing-genus test with a proved complexity advantage, and Gate 4 has
both exact recursive closure and a uniform auxiliary-rank bound.

The broader three-dimensional Ising model is not solved.  Growing transverse
dimensions, periodic/antiperiodic closure, and the 3D thermodynamic limit are
not part of the proved terminal claim.

## Requirement-by-requirement evidence

| Goal requirement | Evidence | Audit result |
|---|---|---|
| Physical intersection pairing by two labeled routes | Cycle 3 artifact, `proof/verify_lane_b_intersection.py` | `PROVED` / exact replay |
| Alternating nondegenerate rank-six form and explicit symplectic transport | Cycle 3 artifact | `PROVED` / exact replay |
| Physical `F(q)` and finite symplectic compression | Cycle 3 artifact, exact profile `(2,4,7,4,2)` | Gate 2 success |
| Next graph chosen only after Gate 2 | Cycle 4 selection record | satisfied |
| Held-out minimum genus controlled | `5x3x3` and `6x3x3` exact checks; Millichap--Salinas Theorem 4 gives all-size genus `L-1` | `PROVED` |
| Exact sector data without cycle-space enumeration | homology frontier; peaks `65536` or lower on held-out computations | satisfied |
| Held-out recurrence test | exact `5->6` relative sectors and repeated local pattern | Gate 3 success |
| Complexity advantage | direct tensor has `4^(L-1)` entries; handle-site TT rank `<=1024`, binary-site TT rank `<=2048` | `PROVED` |
| Gate 4 exact closure | period-two rotation and homology-label recurrence for all `L>=4` | `PROVED` |
| Independent implementation control | sector-Walsh route versus 256-state slice transfer at two exact modular points | `CERTIFIED_NUMERICAL` |
| Failure ledger | direct basis extension and naive closed-homology inclusion retained as failures; label-description correction recorded | satisfied |
| Version-pinned one-command replay | sealed Cycle 4 artifact and successful `--check` | satisfied |
| No unsupported novelty claim | genus theorem conceded to prior work; recursive-compression priority explicitly withheld | satisfied |

## Boundary-condition clause

`LANE_B_GOAL.md` requires periodic, antiperiodic, low-temperature, and related
checks before a thermodynamic claim.  No thermodynamic claim is made.  These
items therefore do not support or weaken the terminal fixed-width structural
outcome; they remain explicit prerequisites for any future thermodynamic
promotion.

## Replays observed in the completion run

- Artifact check: passed, 68.05 s, peak RSS 360,656 KiB.
- Full suite: 37 tests passed, 187.75 s, peak RSS 365,888 KiB.
- Sealed artifact SHA-256:
  `3bbc61164f68eaaed3b1babcdd9e782da06aa0ccfc90637f81de27501c7dcb8d`.
