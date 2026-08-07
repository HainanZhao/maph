# Verification record

Verification date: 2026-08-07 UTC.

## Claim boundary

- `PROVED`: the sufficient direction of CIMSY Conjecture 5.4 for every
  `k>=1`, `r>=2`.
- `PROVED`: the hybrid allocation criterion for any finite number of
  spacers and arbitrary positive steps, without a coprimality assumption.
- Not claimed: necessity, an exact characterization, or general
  q-Fibonomial unimodality.

## Gate 0

- G0.1 `PASS`: the matrix proof is structurally Paper B's induction. It uses
  the identical recursion, increments one spacer once per step, invokes the
  same closure lemma, and retains the center calculation `E+2r_j`. The only
  lift is the outer induction on spacer rows; unused rows certify every
  correction term.
- G0.2 `PASS`: the hybrid theorem was frozen with disjoint divisibility
  absorption followed by residual allocation. Exact checks exclude
  `(1+q^2)(1+q^3)`, reproduce activation at `a=6` for steps `2,3` and `a=5`
  for repeated step `2`, and check `r_j=1`.
- G0.3 `PASS` under the author's single-researcher instruction: a separately
  implemented exact bounded-weight solver was compared with brute force on
  93,618 small instances. The stable width-five counts are matrix `18`,
  absorption `0`, hybrid `18`. Thus the hybrid does not subsume the
  width-five theorem.

## Exact runner

Runtime: CPython 3.12.3, standard library only.

```sh
python3 proof/qanalog_multispacer_criterion.py
```

The runner reported:

- 1,680 recursion identities by two routes;
- 15,163 one-spacer induction rows;
- 400 allocated multi-spacer products and 43,002 nested recursion steps;
- 6,833 small hybrid-certified products;
- 93,618 brute-force comparisons for the bounded-weight solver;
- 20 separately written direct identity checks;
- 20 separately written direct matrix checks;
- 10 separately written divisibility-absorption checks;
- all threshold and width-five class regressions;
- final status `COMBINED_CRITERION_PASS`.

Measured wall time: 11.84 seconds. Peak resident memory: 16,000 KiB.

## Statement diff

The primary-source transcription of Conjecture 5.4 requires `r>=2`, `k>=1`,
positive `a_1,...,a_k,b`, and the disjunction

```text
some r | a_i, OR b <= 1 + sum_i floor(a_i/r).
```

Theorem 1 has the same parameter domain, existential divisibility branch,
weak inequality, floor expression, and `OR`. No side condition was added or
dropped.

## Introduction gate

A fresh read of Section 1 alone identifies:

- Theorem 1 as the result settling the sufficient direction of the named
  CIMSY conjecture;
- Theorem 2 as the new multiple-spacer result beyond it;
- no claim of necessity, exact characterization, or general q-Fibonomial
  unimodality.

This passes the cold-reader content test under the author's instruction that
the work be performed by one researcher.

## Manuscript build and vocabulary

Builder: pdfTeX 3.141592653-2.6-1.40.25, TeX Live 2023/Debian.
Two clean builds produced a five-page PDF with no undefined references,
missing citations, box warnings, or package warnings. All five pages were
inspected as rendered images.

Case-insensitive search of manuscript-bound `.tex`, `.bib`, and `.sty` files
found zero internal workflow terms from the declared list. The old Paper B
DOI and page-local layout hack are absent.

## Hashes

```text
684ceb3800e2f296775186456a47ee428ba99ebc4ee28192b86cfb8c9da054b9  paper/qanalog-multispacer-criterion/main.tex
63671174cf2cb4c622aec26f4208e752b3a420b85961924d691c1093ec81b071  paper/qanalog-multispacer-criterion/main.pdf
13e9bb8be9c856fe8960d73d313fb9af018344b8f7b8aafac0bb074d683971f1  proof/qanalog_multispacer_criterion.py
0c004dcaa80353a5ac6a4849b7149650065a6f569765b2c2b2e96df4dde263a6  proof/qanalog_conjecture54_sufficiency.py
7d921bfd30cb1d1a5ec88be6878c9b2f74f76b8439f08104c422aaa119486b61  discovery/multi_spacer_aligned_recursion_check.py
8c53dec1a7578d3d7ea52d16d9cc0747bc22f7701263bce2088fbf0d874397df  experiments/multi_spacer_adversarial_and_width5_overlap.py
```

## Deferred external gate

No DOI was reserved and no archive was deposited because dissemination is
outside this task. Consequently, cold fetch and replay from a deposited DOI
remain unperformed. The combined manuscript is a verified working draft,
not a disseminated final archive.
