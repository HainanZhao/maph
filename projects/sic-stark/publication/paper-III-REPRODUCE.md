# Reproducing Paper III

## Environment

This package was tested with CPython 3.11 (Debian bookworm; also
verified compatible with CPython 3.12.3), NumPy 1.26.4, mpmath 1.3.0,
SymPy 1.14.0, python-flint 0.9.0 linked against FLINT 3.6.0, PARI/GP
2.15.4, and pdfTeX 3.141592653-2.6-1.40.24.

Install the Python dependencies in an isolated environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-lock.txt
```

## Verify the package

From the extracted package root:

```bash
sha256sum --check --strict ARCHIVE_CONTENTS.sha256
PYTHONPATH=scripts python3 -m unittest discover -s tests -v
```

The smoke suite reports `Ran 104 tests` followed by `OK`. Three of
those tests require the pinned python-flint/Arb environment and are
otherwise skipped; enable them with:

```bash
SIC_STARK_RUN_ARB=1 PYTHONPATH=scripts python3 \
  -m unittest tests.test_dimension_six_two_base_lens -v
```

Regenerate the full certificate packet:

```bash
bash scripts/generate_dimension_six_amendment_certificates.sh
```

Compile the manuscript twice:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimension-six-boundary-fusion.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimension-six-boundary-fusion.tex
```

## Scope note

This package documents a research note, not a closed proof. See the
manuscript's own "Statement and proof status" and "Scope and
reproducibility" sections, and `docs/dimension-six-state-notes-v3.md`,
for exactly what is verified and what remains conditional on the
fusion-continuity conjecture.
