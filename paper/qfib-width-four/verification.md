# Verification record

Verification date: 2026-08-06 UTC.

Claim status: `PROVED`. The manuscript proves unimodality of
`[m+4 choose 4]_F` for every integer `m >= 1`; no wider family is claimed.

## Exact replay

Runtime: CPython 3.12.3, standard library only.

Command, from the repository root:

```sh
python3 proof/qfib_width4_unimodality_proof.py
```

Observed output:

```text
PARTITION_FORMULA_PASSED_T0_TO_300
SMALL_CASES_PASSED_M1_TO_7
DIRECT_QUOTIENT_CROSSCHECK_PASSED_M1_TO_24
```

Measured principal replay: 2.02 seconds wall time and 99,292 KiB maximum
resident memory. The proof depends on the `m=1,...,7` line only; the other
two lines are independent consistency checks.

## Manuscript build

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian; BibTeX 0.99d.
Build from `paper/qfib-width-four/` with:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The final four-page build completed with no undefined citations or references,
overfull boxes, underfull boxes, or package warnings. The rendered pages were
also inspected as images.

## SHA-256

```text
e907f6c19b44cb498a87633226bcde4f277fe5737aed4e727abc06d32b655eda  proof/qfib_width4_unimodality_proof.py
cd5187682d999590a0d2897ae7f64029e4c7c74443b43ef3d9f433e93e1fc209  proof/qfib_width4_unimodality_proof.md
0d2e458647246f709c5a3b7bcf1304ad9942077edeb298928e56a2425098fb68  paper/qfib-width-four/main.tex
7e2f8fd72a69e11d774ee1788c0ef73f4d0a6946c3a5d5c89e92359bebd6be77  paper/qfib-width-four/references.bib
fcf8fa20160a3bb2b6abd817d2de2d72d3530bbbafd309a483d37353cffd5063  paper/qfib-width-four/literature-audit.md
76c24118df6aeb7cf9291a3f820e7dbdfce09b3e3a89f86eb60334dc6cbd79d6  paper/qfib-width-four/main.pdf
```
