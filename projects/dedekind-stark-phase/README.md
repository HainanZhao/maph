# Dedekind-sum phase formula project

This project tests whether the quartic one-place Stark phase defect can
be expressed by a low-complexity Dedekind--Rademacher congruence.

The project is exploratory. `VERIFIED` means that a finite computation
or a logical scope statement has been replayed; it does not mean that
the conjectured phase formula exists.

Start after a crash with:

1. `PLAN.md`;
2. `data/preregistration-v1.json`;
3. `artifacts/control-phase-audit-v1.json`;
4. `docs/cycle-020-checkpoint.md`;
5. `python3 -m unittest discover -s tests -p 'test_*.py'`.

The certified control packets remain owned by
`../effective-stark-sweep`; this project records hashes and extracts
only the fields needed for the phase experiment.

The cycle-20 result is a disciplined feasibility halt, not a fitted
formula. The five controls prove route invariance and reject raw phase
quantization, but their archived comparison vectors are derived from
the same \(L'\)-data. The next experiment is the independently sealed
five-row Roblot screen in
`data/roblot-original-quartic-screen-v1.json`.
