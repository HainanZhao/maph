# Reproducing the SIC--Stark companion papers

## Environment

The release was verified on Linux x86-64 with:

- CPython 3.12.3;
- NumPy 1.26.4;
- python-flint 0.9.0 linked against FLINT 3.6.0;
- PARI/GP 2.15.4; and
- pdfTeX 3.141592653-2.6-1.40.24.

Install the Python dependencies in an isolated environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-lock.txt
```

PARI/GP is a system dependency and must provide the `gp` executable.

## Verify all certificates

From this directory, run:

```bash
PYTHONPATH=scripts python3 -m unittest discover -s tests -v
sha256sum --check --strict certificates/SHA256SUMS
```

The expected result is `Ran 111 tests` followed by `OK`. On the
reference four-core virtual machine the suite normally takes about
three minutes when standard input is noninteractive.

## Compile the manuscripts

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-four-five.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-four-five.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-seven-eight.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-seven-eight.tex
cd ..
```

## Build deterministic archives

From a complete repository checkout, build the two
submission-specific packages:

```bash
scripts/build_companion_archives.sh
tests/test_companion_archives.sh
```

Build and test the complete project archive:

```bash
scripts/build_publication_archive.sh --strict-release-metadata
tests/test_publication_archive.sh
```

Every generated archive contains `ARCHIVE_CONTENTS.sha256`. Verify it
after extraction with:

```bash
sha256sum --check --strict ARCHIVE_CONTENTS.sha256
```

Inside either extracted package, run its independent smoke suite with:

```bash
PYTHONPATH=scripts python3 -m unittest discover -s tests -v
```

The package-specific `README.md` identifies the shortest command set
needed to reproduce that paper independently.
