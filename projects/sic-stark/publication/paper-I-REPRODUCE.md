# Reproducing Paper I

## Environment

This package was tested with CPython 3.12.3, NumPy 1.26.4,
python-flint 0.9.0 linked against FLINT 3.6.0, PARI/GP 2.15.4, and
pdfTeX 3.141592653-2.6-1.40.24.

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

The smoke suite reports `Ran 80 tests` followed by `OK`.

Run the principal arithmetic certificates:

```bash
python3 scripts/generate_referee_certificates.py
python3 scripts/verify_referee_certificate.py
gp -q scripts/referee_pari_audit.gp
gp -q scripts/dimension_five_shintani_audit.gp
gp -q scripts/dimension_five_unit_lattice_audit.gp
gp -q scripts/dimension_five_embedding_certificate.gp
gp -q scripts/verify_dimension_five_conjugates.gp
PYTHONPATH=scripts python3 scripts/certify_dimension_five_double_sine.py
```

The archived exact-minor transcript is independently checked by the
Paper-I smoke suite in `tests/test_dimension_five_artifacts.py`.

Compile the manuscript twice:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-four-five.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-four-five.tex
```
