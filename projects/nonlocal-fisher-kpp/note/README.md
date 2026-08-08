# Review note: critical exponential-moment dissipation

This directory contains a short, self-contained research note for external
mathematical review:

- `critical-moment-dissipation.tex` — manuscript source.

The main result is labelled `PROVED` under its stated regularity and weighted
integrability assumptions. It gives an exact Lyapunov identity and rules out
an exact finite-critical-moment packet recurring at the pulled speed. It does
**not** prove wake-wavelength selection, P1/P2, or a biological prediction.

Build with:

```sh
pdflatex -interaction=nonstopmode -halt-on-error critical-moment-dissipation.tex
pdflatex -interaction=nonstopmode -halt-on-error critical-moment-dissipation.tex
```

The proof-grade top-hat specialization and exact coefficient audit remain in
`../proof/critical_exponential_moment.md` and the sealed `B004` artifact. The
general even-kernel statement is frozen in
`../proof/general_exponential_moment.md` and sealed as `B005`.

## Publication assessment

As it stands, this is worth circulating as a short research note or arXiv
preprint. The identity is exact, clean, and gives a useful obstruction, but
the proof is brief and the present literature audit has not established a
priority claim. A stronger standalone journal paper should add at least one
of the following:

1. a rigorous critical-tail/wake decomposition;
2. a quantitative bound or asymptotic formula for the tilted competition
   delay;
3. a theorem showing that the delay retains longer history, or closes on a
   finite state;
4. a broader application where the identity changes an established front or
   pulse theorem.

Recommended current description: **a paper seed with a complete short-note
theorem**, not yet a full pattern-selection paper.
