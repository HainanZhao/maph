# Bounded experiment for C(23,6,2) — Outcome C

Claim boundary: this resource-bounded exact search establishes neither
`C(23,6,2)=20` nor `C(23,6,2)=21` without a verified SAT/UNSAT result.

## Exact reduction and encoding

`PROVED`: A hypothetical 20-block cover has minimum replication five and
total replication excess five. The excess-spectrum argument excludes excess
support sizes one and two, leaving four exact replication patterns. At a
replication-five point, its five-block star contains three repeated
incidences. Modulo its block action their multiplicities have types `4`,
`3+2`, or `2+2+2`, giving respectively one, three, and seven orbits. These
eleven cases exhaust every possible cover.

Each CNF fixes one canonical star, twenty rows of size six, one surviving
replication pattern, and coverage of all 253 pairs. It sorts only blocks and
points interchangeable under the fixed star. In the multiplicity-four case,
the available replication-five star singletons justify the additional fixed
labels. Thus the symmetry constraints are label quotients, not heuristic
restrictions. A SAT assignment is accepted only after direct pair recounting;
UNSAT requires a fresh binary proof and independent `drat-trim` acceptance.

## Fixed experiment and observations

The single nonextendable allocation is 24 aggregate core-hours, eight
wall-hours, 10 GiB memory, at most three solvers on the four-CPU host, and a
temporary-disk cap preserving 5 GiB for the system. CaDiCaL 1.7.3 ran four
waves with per-branch internal limits. Stopped proof-format probes and
coordinator overhead were charged conservatively; solver-written terminal
lines govern whenever a stale summary says `SOLVING`.

`OBSERVED`: the first nine branches (`4`, the seven `222-*` cases, and
`32-overlap0`) reached their limits without a SAT or UNSAT line. The first six
ran for 6,900.00 real seconds and the next three for 6,800.00. Peak RSS was
298.55--340.10 MB. Each branch processed 47.6--55.8 million conflicts and
92.6--107.6 million decisions before returning `exit 0`.

Wave 3 froze all earlier work as 43,300 aggregate core-seconds and 14,500
wall-seconds. After its three terminal runs, Wave 4 conservatively charged
63,800 prior core-seconds and 21,400 prior wall-seconds. Its final branches,
`32-overlap1` and `32-overlap2`, each received a 7,399-second internal limit.
A no-decision Wave 4 therefore exhausts the eight-hour allocation without
requiring exhaustion of the 24-core-hour ceiling.

## Replay

Run from `projects/open-conjecture-sweep/`:

```sh
python3 proof/verify_cover_23_6_2_branch_partition.py
python3 proof/verify_cover_23_6_2_cnf_primitives.py
python3 proof/verify_cover_23_6_2_bounded_archive.py
```

These independently check the orbit and replication reductions, all eleven
canonical stars, 4,826 exhaustive CNF-primitive controls, regenerated DIMACS
and log hashes, resource priors, frozen inputs, and available tool binaries.

## Final outcome

`OBSERVED`: both final branches returned `exit 0` after exactly 7,399.00
real seconds, without a SAT or UNSAT line. `32-overlap1` used 7,395.28
process seconds, 327.34 MB RSS, 54,690,829 conflicts, and 100,273,508
decisions; `32-overlap2` used 7,395.36 process seconds, 301.17 MB RSS,
53,940,597 conflicts, and 102,179,763 decisions. All eleven exhaustive
branches therefore ended `UNKNOWN_SOLVER_LIMIT`.

`PROVED`: the coordinator recorded 78,622.98 aggregate charged seconds
(21.840 core-hours) and 28,800.07 aggregate wall seconds, exceeding the fixed
eight-hour wall cap. Peak aggregate RSS was 599,113,728 bytes (571.36 MiB),
and peak known output was 5,934,955 bytes (5.66 MiB), both below their caps.
The raw summary says `INCOMPLETE` because both internally limited children
exited between polls before the coordinator assigned a stop reason. The
independent archive verifier preserves that summary and returns
`WALL_CAP_DERIVED` only after checking its numeric cap meter and every
terminal log.

Classification: **Outcome C — killed by the preassigned wall-clock cap.**

Cost boundary: censored limits support only the projection that this exact
method needs more than the fixed allocation; remaining cost is indeterminate.
Budget exhaustion without a cover is Outcome C, not evidence that
`C(23,6,2)=21`. An all-UNSAT claim would require accepted proofs for all
eleven branches.
