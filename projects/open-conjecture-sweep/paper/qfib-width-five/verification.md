# Verification record

Verification date: 2026-08-07 UTC.

Claim status: `PROVED`. For every integer `m>=1`, the width-five
q-Fibonomial `[m+5 choose 5]_F` is unimodal.

The author directed that the research and verification be performed by one
researcher. Independence below therefore means independently implemented or
derived routes, not a second agent.

## Exact replay

Runtime: CPython 3.12.3, standard library only.

From the repository root:

```sh
python3 proof/qfib_width5_unimodality_proof.py
```

The replay checks:

1. the 30 cubic kernel formulas against direct restricted-partition dynamic
   programming;
2. the six-shift identity against full symbolic inclusion--exclusion for
   `m<=240`;
3. the same identity against independently constructed exact quotient
   coefficients for `m=1,...,8`;
4. all frozen worst-error envelopes for `20<=m<=240`;
5. exact symbolic minima for `m=1,...,19`;
6. all 72 previously designated bad-class instances through `m=240`, using
   exact residue-polynomial minimization.

Observed final line:

```text
WIDTH5_QFIBONOMIAL_UNIMODALITY_PROOF_CHECK_PASSED
```

Measured replay: 5.09 seconds wall time and 22,332 KiB peak RSS.

The universal range rests on the algebraic lower-envelope proof in the
manuscript; the `m<=240` rows are regression evidence.

## Independent envelope calculation

An independently written SymPy 1.12 checker reconstructs the six
piecewise envelopes directly from

```text
Q(t)=t^3/180+11t^2/120+9t/20,
91/360 <= rho <= 1,
```

and the six signed shifts.  It does not import either prior width-five
checker.  It verifies all six printed constants in (5), the derivative or
concavity assertion used on every interval, and positivity after the exact
substitution `a=A+34`, `d=D+1` by nonnegative polynomial coefficients.

```sh
python3 proof/qfib_width5_envelope_independent.py
```

Observed output:

```text
{"constants_checked": 6, "domain": "a>=34,d>=1", "shape_checks": 6, "status": "PASS", "sympy_version": "1.12"}
```

## Statement and cold-reader gates

The primary-source transcription of BCK Conjecture 2.5 says that, for
positive integers `m,n`, every `[m+n choose n]_F` is unimodal.  Substituting
`n=5` gives exactly Theorem 1: `[m+5 choose 5]_F` is unimodal for every
integer `m>=1`.  The inequality and the positive-parameter edge convention
match exactly.

A fresh read of the introduction alone yields:

- previously known: polynomiality and nonnegativity for all widths,
  unimodality for `n<=3`, and the subsequent width-four theorem;
- contribution: unimodality for width five and every positive `m`;
- excluded claims: width six, the full two-parameter conjecture,
  log-concavity, and a combinatorial chain decomposition.

The introduction therefore passes the cold-reader content gate under the
author's single-researcher instruction.

## Manuscript vocabulary gate

Case-insensitive search of every manuscript-bound `.tex`, `.bib`, and `.sty`
file found no internal workflow identifiers from the gate list: `ledger`,
`certificate`, `C7`, `C8`, `REPLAY`, `phase`, `TCC`, `GOAL`, `outcome`,
`R1`, `R2`, `R3`, `W0`, `W1`, `W2`, `W3`, or `W4`.

## Manuscript build

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian.

```sh
cd paper/qfib-width-five
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The four-page manuscript compiled with no undefined citations or references,
overfull boxes, underfull boxes, or LaTeX warnings. All four rendered pages
were inspected as images.

## SHA-256

```text
2d2a93bf317e45d180fae8e974016b54b7072de4b10ae2a652709cb75417d017  proof/qfib_width5_unimodality_proof.py
99f0457a69c02e567af97ddfae284589b0f692236091730fc374f050494de1b0  experiments/qfib_width5_candidate_lemmas.py
042f5d1bbf907af19e5aaf70d2b1d0c61ff7aac154d4760a1a43a24ff44d2ad3  experiments/qfib_width5_bad_class_unimodality.py
17bee755727aaea55e733917dbcb566f89cecc8fa615495fd2a3524286213e4c  proof/qfib_width5_envelope_independent.py
8c53dec1a7578d3d7ea52d16d9cc0747bc22f7701263bce2088fbf0d874397df  experiments/multi_spacer_adversarial_and_width5_overlap.py
a0fd08a4a6522806e34c727f4de04930fd124df135f380b8f117dd943a7039e2  discovery/multi_spacer_aligned_recursion.md
82b062e1e67d9a3843f9bbaf64149594ac52771d32d61aa7397a68f150de3466  paper/qfib-width-five/main.tex
fd2f38f7cf4e1bc0df4ff6fd2136402e29d7931819755bf0f405baa9f3d7cd50  paper/qfib-width-five/main.pdf
```
