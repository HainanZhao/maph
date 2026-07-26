# Submission package

Proposed venue: **Physical Review A**, regular article.

## Files

- `manuscript.tex`: main RevTeX manuscript.
- `supplement.tex`: standalone Supplemental Material.
- `references.bib`: shared bibliography.
- `cover-letter.md`: draft cover letter to the editor.
- `submission-checklist.md`: final metadata and upload checklist.
- `build/manuscript.pdf`: compiled main manuscript.
- `build/supplement.pdf`: compiled Supplemental Material.
- `submission-source.tar.gz`: source, code, and exact tests for upload or
  archiving.

## Build

The PDFs were compiled with Tectonic 0.16.9:

```text
tectonic -X compile manuscript.tex --outdir build --keep-logs
tectonic -X compile supplement.tex --outdir build --keep-logs
```

The only BibTeX message is the standard RevTeX bibliography-style control
warning. There are no undefined citations, references, TeX errors, or
overfull boxes.

## Reproduce the calculations

From the repository root:

```text
python3 -m unittest discover -s tests -v
python3 scripts/analyze_reciprocity_census.py
python3 scripts/analyze_unitary_leakage.py
python3 scripts/analyze_finite_shot_protocol.py
```

The phase-histogram, census, and leakage calculations use exact integer or
rational arithmetic. The finite-shot script uses floating point only for the
finite-angle nuisance model and independently certifies the exact
four-photon formula at several angles.

## Scope of the claims

The submission deliberately does not claim:

- a new Krawtchouk identity;
- a universal response invariant for every zero in a suppression class;
- generic persistence of Fourier darkness throughout the complex-Hadamard
  family;
- a full partial-distinguishability or internal-loss model;
- experimental validation.

Its central physical result is the coherent, event-level directional
response jet: specified dark event--generator pairs can remain exactly dark
or begin at quadratic or quartic order.
