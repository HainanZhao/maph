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
  absorption `0`, hybrid `18`. A further independently written program
  reconstructed the Fibonacci windows directly, without importing either
  prior table or its labels. It verified that the 18 reached classes and 18
  undecomposable classes have the stated memberships and are disjoint; the
  remaining 24 classes are decomposable but unreached. Thus the hybrid does
  not subsume the width-five theorem.

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
- an independently reconstructed three-set width-five coverage partition;
- the adaptive certificate for `[5]_q[2]_(q^2)[2]_(q^3)` and its zero
  width-five class gain;
- 33,728 exact violating one-spacer rows in the conjectured necessity
  regimes, grouped into 4,576 fixed `(r,a_1,...,a_k)` tuples;
- 100 independently constructed direct-polynomial cross-checks of that
  first-dip census;
- a deterministic 256-group endpoint extension to `b=100`, checked by both
  sliding windows and separately written direct multiplication;
- all threshold and width-five class regressions;
- final status `COMBINED_CRITERION_PASS`.

Measured wall time: 12.86 seconds. Peak resident memory: 16,768 KiB.

The bounded dip census found a first dip in every violating row. Within each
fixed `(r,a_1,...,a_k)` group its position was independent of `b` throughout
the violating range, and every first-dip depth was one or two. This is
`OBSERVED` exact finite data, not a universal necessity result. In a
deterministic sample of 256 groups, the original first-dip position also
persisted at `b=100` by two separately written exact constructions; this
does not enlarge the manuscript's declared census box.

## Statement diff

The primary-source transcription of Conjecture 5.4 requires `r>=2`, `k>=1`,
positive `a_1,...,a_k,b`, and the disjunction

```text
some r | a_i, OR b <= 1 + sum_i floor(a_i/r).
```

Theorem 1 has the same parameter domain, existential divisibility branch,
weak inequality, floor expression, and `OR`. No side condition was added or
dropped.

The introduction's necessity attribution was also diffed against the 0.3
ledger table: CIMSY conjectures necessity when `k<=3` or `r<=3`, while its
proved precursors include the full iff for `k=1` and for `(k,r)=(2,2)`.

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
264324e773e6a31c4e5c13a570434bb58c98f315242855abb495f5c2f747a5ac  paper/qanalog-multispacer-criterion/main.tex
e6715a9efa51652b32562f6d1748c0aa9aba9ce011561a6f55b9bcd68c86b16b  paper/qanalog-multispacer-criterion/main.pdf
b01e16c51f907dfba6b0a21b74426b7afedeaba1cc767b1144d7558a702e0f02  proof/qanalog_multispacer_criterion.py
85c16c9f64ac74562c07b3aad56301c18e5d738c4a218f2d02350171b740104e  proof/qanalog_width5_coverage_independent.py
47b01ebc4c5918c201b3febc757ec35faae6349a80bb93a895ca9753ab21f7d9  experiments/qanalog_adaptive_allocation_probe.py
44dd160267e8b555f5063ed0bb3c6fa8b75cc0d73e81bfebbe51a5cfa8aa9e1b  experiments/qanalog_one_spacer_dip_census.py
0c004dcaa80353a5ac6a4849b7149650065a6f569765b2c2b2e96df4dde263a6  proof/qanalog_conjecture54_sufficiency.py
7d921bfd30cb1d1a5ec88be6878c9b2f74f76b8439f08104c422aaa119486b61  discovery/multi_spacer_aligned_recursion_check.py
8c53dec1a7578d3d7ea52d16d9cc0747bc22f7701263bce2088fbf0d874397df  experiments/multi_spacer_adversarial_and_width5_overlap.py
```

## Deferred external gate

No DOI was reserved and no archive was deposited because dissemination is
outside this task. Consequently, cold fetch and replay from a deposited DOI
remain unperformed. The combined manuscript is a verified working draft,
not a disseminated final archive.
