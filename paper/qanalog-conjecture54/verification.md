# Verification record

Verification date: 2026-08-07 UTC.

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

Measured principal replay: 2.65 seconds wall time and 12,928 KiB maximum
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
- `PROVED`: the statement transcribed from arXiv:2605.12822v1 has the
  inclusive inequality `b <= 1 + sum_i floor(a_i/r)`, joined by “or” to the
  divisibility condition, with no omitted parameter constraint.
- `OBSERVED`: direct multiplication agrees with the induction for 15,163
  bounded rows across `2 <= r <= 6`, `1 <= k <= 4`, and non-divisible
  lengths at most 12.

## Manuscript build and hashes

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian.
The final three-page build completed with no undefined citations or
references, overfull boxes, underfull boxes, or package warnings. All three
rendered pages were inspected as images. A subsequent build under the same
fixed timestamp was byte-identical. The visible proof/source archive DOI is
`10.5281/zenodo.21830407`.

```text
0c004dcaa80353a5ac6a4849b7149650065a6f569765b2c2b2e96df4dde263a6  proof/qanalog_conjecture54_sufficiency.py
0c8c327d288c483f13d7097f78e2ca15180d54318a05460c2697fdf6fbab284e  proof/qanalog_conjecture54_sufficiency.md
c7f8dd492f40cd1b3e9b57976e75cdceecb235cc1d43160376e496423f922507  paper/qanalog-conjecture54/main.tex
43c930cd70ebdf9baa290461191ac5ed7e23f1f9aff2533ab52809d7226a921b  paper/qanalog-conjecture54/literature-audit.md
6f5336dd67aea17a38264e71aafd6c030c98b4c596b6e8de9ed6ecc7736c1904  paper/qanalog-conjecture54/hostile-audit.md
97403b00e3169f8533ceb4c51bc640c42a9f0ae0a4256585ea5309a393e8ba77  paper/qanalog-conjecture54/main.pdf
23a253e11e68cbf07ebcf377c8884f6aedcd5336f9c0b5e46244a11098c6f56b  paper/qanalog-conjecture54/README.md
d017acb57dbef190cbda3e9a5228dfc7d35a3d7b1f8b304c4e6da18d0ac5c6eb  paper/qanalog-conjecture54/LICENSE.md
658367c8d7a7edea102bea297041cc5c70c73e02306f5c67ae29de877ec77402  paper/qanalog-conjecture54/build_release.py
```
