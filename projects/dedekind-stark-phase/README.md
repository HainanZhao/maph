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
4. `docs/cycle-045-checkpoint.md`;
5. `python3 -m unittest discover -s tests -p 'test_*.py'`.

The certified control packets remain owned by
`../effective-stark-sweep`; this project records hashes and extracts
only the fields needed for the phase experiment.

The cycle-45 result is a completed feasibility result, not a fitted
formula. Five independently constructed weak solutions all exhibit a
unique fourth-root phase relation. The raw phase label is gauge
dependent; after a canonical gauge repair, the simplest field-only
Dedekind family fails exactly. The missing datum is a generic
ray-character-to-cocycle bridge. Fitting and the 50-row holdout remain
unauthorized until that theorem-level bridge is built and a new feature
family is pre-registered.
