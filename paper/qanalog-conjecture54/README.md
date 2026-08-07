# An Aligned-Center Recursion for Products of q-Integers

Author: hainzhao

DOI: <https://doi.org/10.5281/zenodo.21830407>

This archive proves the sufficient direction of Connelly--Ito--Martinez--
Shevchenko--Yang Conjecture 5.4 for every `k >= 1` and `r >= 2`:

```text
if some r divides a_i, or b <= 1 + sum_i floor(a_i/r),
then product_i [a_i]_q [b]_(q^r) is symmetric unimodal.
```

The result does not claim that the condition is necessary in general and
does not settle general q-Fibonomial unimodality.

## Exact replay

Requirements: CPython 3.12 or later, using only the standard library.

From the extracted archive root, run:

```sh
python3 proof/qanalog_conjecture54_sufficiency.py
```

Expected output ends with `"status": "PASS"`. The script checks the key
recursion through two independent coefficient constructions and compares the
inductive construction with direct multiplication over 15,163 bounded rows.
Those rows are regression evidence; the universal result is proved in the
paper.

## Manuscript build

From the extracted archive's `paper/` directory, run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archive manifest records the SHA-256 digest and byte length of every
included file. `verification.md` records the tested runtime, literature
boundary, and claim boundary.
