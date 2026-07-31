# Dedekind-sum phase formula project

This project tests whether the quartic one-place Stark phase defect can
be expressed by a low-complexity Dedekind--Rademacher congruence.

The project is exploratory. `VERIFIED` means that a finite computation
or a logical scope statement has been replayed; it does not mean that
the conjectured phase formula exists.

Start after a crash with:

1. `AGENTS.md`;
2. `PLAN.md`;
3. `docs/final-project-report.md`;
4. `sha256sum -c MANIFEST.sha256`;
5. `python3 -m unittest discover -s tests -p 'test_*.py'`.

Project map:

- `PLAN.md`: authoritative research graph, gates, headline results, and
  complete cycle ledger;
- `docs/`: preregistrations, proofs, checkpoints, and final synthesis;
- `artifacts/`: immutable machine-readable evidence records;
- `scripts/`: replayable exact and numerical audits;
- `src/`: reusable exact arithmetic;
- `tests/`: artifact and arithmetic regression gates;
- `MANIFEST.sha256`: integrity map for controlling evidence.

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

The project is now finished. The final exact test shows that the
descended squared multiplier is sign-class even, whereas the
differenced Stark support is sign-class odd; every relevant Fourier
resolvent therefore vanishes. See
`docs/class-descent-fourier-no-go-v1.md`. This closes the frozen
mechanism without weakening the independent five-for-five phase
quantization observation.
