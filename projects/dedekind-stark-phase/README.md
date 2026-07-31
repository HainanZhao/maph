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
4. `docs/cycle-055-checkpoint.md`;
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

Cycles 046--055 isolated an exact supplied-tuple multiplier evaluator
and replayed the SIC anchors, but rejected a generic map from a ray
character to one tuple. The next possible theorem target is a Fourier
resolvent of representative-independent class-level cocycle
multipliers. No fitting or holdout is currently authorized.
