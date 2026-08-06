# Verification record

Verification date: 2026-08-06 UTC.

Claim status: `PROVED`. The manuscript proves the sufficient direction of
Connelly--Ito--Martinez--Shevchenko--Yang Conjecture 5.4 for every `k >= 1`
and `r >= 2`. It does not claim general necessity or general q-Fibonomial
unimodality.

## Exact replay

Runtime: CPython 3.12.3, standard library only.

Command, from the repository root:

```sh
python3 proof/qanalog_conjecture54_sufficiency.py
```

Observed output:

```json
{"claim": "Conjecture 5.4 sufficient direction for all k>=1 and r>=2", "direct_induction_rows": 15163, "direct_polynomials_checked": 15163, "identity_rows_two_routes": 1680, "length_limit": 12, "nonnecessity_scope_example": "([3]_q)^4[2]_(q^4)", "python": "3.12.3", "status": "PASS"}
```

Measured principal replay: 2.49 seconds wall time and 12,800 KiB maximum
resident memory. The exact bounded rows are regression checks, not the basis
of the universal proof.

## Proof-route audit

- `PROVED`: the recursion is derived algebraically from q-integer identities.
- `PROVED`: an independent partition of exponent-weighted pairs gives the
  same recursion coefficientwise.
- `PROVED`: at every induction step, both symmetric unimodal summands have
  support endpoints summing to the new degree.
- `PROVED`: because no `a_i` is divisible by `r` in the induction branch,
  subtracting any allocated `r floor(a_i/r)` leaves a positive base length.
- `PROVED`: the divisibility branch repeats each coefficient of an ordinary
  symmetric unimodal product in a block of length `r`.
- `OBSERVED`: direct multiplication agrees with the induction for 15,163
  bounded rows across `2 <= r <= 6`, `1 <= k <= 4`, and non-divisible
  lengths at most 12.

## Manuscript build and hashes

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian; BibTeX 0.99d.
The final three-page build completed with no undefined citations or
references, overfull boxes, underfull boxes, or package warnings. All three
rendered pages were inspected as images. A subsequent build under the same
fixed timestamp was byte-identical. The visible proof/source archive DOI is
`10.5281/zenodo.21830407`.

```text
0c004dcaa80353a5ac6a4849b7149650065a6f569765b2c2b2e96df4dde263a6  proof/qanalog_conjecture54_sufficiency.py
0c8c327d288c483f13d7097f78e2ca15180d54318a05460c2697fdf6fbab284e  proof/qanalog_conjecture54_sufficiency.md
05b2d20c7640e890bb5c0aacabd873746efbacc63ceebe040976b9d483f6d3bc  paper/qanalog-conjecture54/main.tex
83bf726354cdfbdb456a5f4c59652c1550626c222a63d72763f17c8e74eb2a5e  paper/qanalog-conjecture54/references.bib
43c930cd70ebdf9baa290461191ac5ed7e23f1f9aff2533ab52809d7226a921b  paper/qanalog-conjecture54/literature-audit.md
986070e9c937bfb0a843640dcecc6205c2fea9851f1f6fe1ac5220301bd3ebcc  paper/qanalog-conjecture54/hostile-audit.md
700d56bd8433059fc871e6b85765d9de0610942236097a52eea30d955259e988  paper/qanalog-conjecture54/main.pdf
ba6d13d528d2adaacb676be2eed688805ac4112678c2f7d7350569379d0a041c  paper/qanalog-conjecture54/README.md
157c4052069d914499cfaabbb63c9415da9c5f0d7bdf7ae375a1135a4056304d  paper/qanalog-conjecture54/LICENSE.md
aa7667f26ab3cdda4de8f5a9426ec49cbd73cd02da6fc65a19e76c5ae83cc4ba  paper/qanalog-conjecture54/build_release.py
```
