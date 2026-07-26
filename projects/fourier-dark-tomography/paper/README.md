# Submission package

Proposed venue: **Physical Review A**, regular article.

## Current files

- `manuscript.tex`: self-contained RevTeX manuscript, including full proofs
  and appendices.
- `references.bib`: bibliography.
- `cover-letter.md`: draft editor cover letter.
- `submission-checklist.md`: metadata and upload checklist.
- `build/manuscript.pdf`: compiled manuscript.
- `arxiv-source-v1.1.tar.gz`: minimal arXiv TeX upload bundle.
- `arxiv-metadata.md`: copy-ready `quant-ph` metadata and author checklist.
- `zenodo-metadata.md`: copy-ready Zenodo preprint record and file checksums.
- `submission-source.tar.gz`: current manuscript, code, tests, documentation,
  reproduction guide, and code license.
- `legacy/`: pre-generalization supplement and source bundle, retained only
  for provenance and not intended for submission.

## Build

From this directory:

```sh
/tmp/tectonic -X compile manuscript.tex --outdir build --keep-logs
```

## Reproduce the calculations

From `projects/fourier-dark-tomography/`:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/certify_general_fourier_cat_tomography.py --max-modes 9
python3 scripts/search_su4_dark_tomography.py
python3 scripts/analyze_cat_finite_statistics.py
python3 scripts/analyze_general_resource_scaling.py
python3 scripts/simulate_f4_reconstruction.py --repetitions 5000
python3 scripts/generate_reconstruction_sweep.py --repetitions 1500
```

The exact rank certificates use symbolic integer, rational, or cyclotomic
arithmetic. Floating-point calculations are reserved for the finite-angle
statistical study and are checked against exact limiting formulas.

## Scope of the claims

The main result is an explicit, all-mode, dimension-saturating local frame
for off-diagonal coherent errors, constructed from Fourier-cat dark events
and signed calibrated probes. It is not a claim of global process
tomography, cheaper transfer-matrix reconstruction, diagonal-generator
identification, universal sample complexity,
or complete treatment of state-preparation, loss, and distinguishability
errors.
