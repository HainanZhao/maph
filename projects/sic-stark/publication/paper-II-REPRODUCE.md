# Reproducing Paper II

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

The smoke suite reports `Ran 16 tests` followed by `OK`.

Run the principal exact certificates:

```bash
gp -q scripts/dimension_seven_admissible_strata.gp
gp -q scripts/dimension_seven_exact_tcc.gp
PYTHONPATH=scripts python3 scripts/certify_dimension_seven_double_sine.py \
  --tolerance 1e-10
gp -q scripts/dimension_eight_linear_cm_reinduction.gp
gp -q scripts/dimension_eight_cm_unit_lattice.gp
PYTHONPATH=scripts python3 scripts/certify_dimension_eight_cm_orientation.py
gp -q scripts/dimension_eight_cm_real_unit_bridge.gp
gp -q scripts/dimension_eight_exact_tcc.gp
gp -q scripts/dimension_eight_maximal_tuple_audit.gp
gp -q scripts/dimension_eight_maximal_quadratic_units.gp
python3 scripts/dimension_eight_maximal_sign_audit.py
python3 scripts/dimension_eight_maximal_exact_tcc.py
```

Compile the manuscript twice:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-seven-eight.tex
pdflatex -interaction=nonstopmode -halt-on-error \
  sic-stark-dimensions-seven-eight.tex
```
