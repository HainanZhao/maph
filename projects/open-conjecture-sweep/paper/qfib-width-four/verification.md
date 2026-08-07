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

Measured principal replay: 1.86 seconds wall time and 99,312 KiB maximum
resident memory. The proof depends on the `m=1,...,7` line only; the other
two lines are independent consistency checks.

## Manuscript build

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian; BibTeX 0.99d.
Build from `paper/qfib-width-four/` with:

```sh
SOURCE_DATE_EPOCH=1785974400 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
SOURCE_DATE_EPOCH=1785974400 FORCE_SOURCE_DATE=1 bibtex main
SOURCE_DATE_EPOCH=1785974400 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
SOURCE_DATE_EPOCH=1785974400 FORCE_SOURCE_DATE=1 \
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The final four-page build completed with no undefined citations or references,
overfull boxes, underfull boxes, or package warnings. The rendered pages were
also inspected as images. A subsequent build with the same environment was
byte-identical. The visible proof/source archive DOI is
`10.5281/zenodo.21826970`.

## SHA-256

```text
e907f6c19b44cb498a87633226bcde4f277fe5737aed4e727abc06d32b655eda  proof/qfib_width4_unimodality_proof.py
cd5187682d999590a0d2897ae7f64029e4c7c74443b43ef3d9f433e93e1fc209  proof/qfib_width4_unimodality_proof.md
08130187fc851ed3f6c42153114df5691656e8ebece82369adb0462f5e4c95e4  paper/qfib-width-four/main.tex
7e2f8fd72a69e11d774ee1788c0ef73f4d0a6946c3a5d5c89e92359bebd6be77  paper/qfib-width-four/references.bib
fcf8fa20160a3bb2b6abd817d2de2d72d3530bbbafd309a483d37353cffd5063  paper/qfib-width-four/literature-audit.md
06f074112e59a185888ec2cdcd22367d56f9967179154d64afeb91e67d2fea87  paper/qfib-width-four/main.pdf
2d3b8abee2680f489d129048a792deb7f41ede4e404c4857e0b1afe87a5c8dcd  paper/qfib-width-four/README.md
157c4052069d914499cfaabbb63c9415da9c5f0d7bdf7ae375a1135a4056304d  paper/qfib-width-four/LICENSE.md
ee91c90be43d1d50547d21f65a5cc4babf2baaba5e5269bd5ef1de2faf068f23  paper/qfib-width-four/build_release.py
```
