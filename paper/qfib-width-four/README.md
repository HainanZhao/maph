# The Width-Four q-Fibonomial Coefficients Are Unimodal

Author: hainzhao

DOI: <https://doi.org/10.5281/zenodo.21826970>

This archive accompanies the proof that

```text
[m+4 choose 4]_F
```

is unimodal for every integer `m >= 1`. The claim is limited to width four;
it does not resolve the full two-parameter q-Fibonomial conjecture.

## Exact replay

Requirements: CPython 3.12 or later, using only the standard library.

From the extracted archive root, run:

```sh
python3 proof/qfib_width4_unimodality_proof.py
```

The expected output is:

```text
PARTITION_FORMULA_PASSED_T0_TO_300
SMALL_CASES_PASSED_M1_TO_7
DIRECT_QUOTIENT_CROSSCHECK_PASSED_M1_TO_24
```

The proof uses only the finite cases `m=1,...,7`; the partition-formula and
direct-quotient lines are structurally separate consistency checks.

## Manuscript build

From `paper/qfib-width-four/`, run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archive manifest records the SHA-256 digest and byte length of every
included file. `verification.md` records the tested runtime and claim
boundary.
