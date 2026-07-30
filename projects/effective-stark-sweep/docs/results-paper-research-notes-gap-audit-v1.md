# Results-paper research-notes gap audit v1

Date: 2026-07-30 UTC

Status: read-only audit of the v3 paper freeze.  This note does not
modify or supersede `artifacts/results-paper-freeze-v3.json`.

## Scope and precedence

The audit covered all 93 top-level research notes in `docs/`, both
Markdown paper drafts, the current TeX manuscript, and every JSON
record whose claim tag contains `THEOREM`.  Chronological precedence
was applied:

1. genuine census v5 supersedes census declarations v1--v4;
2. R-13 genuine reconstruction supersedes every proxy-derived index or
   normal-closure interpretation;
3. Engine-C general-\(e\) v3 supersedes v1/v2 only in its corrected
   specialization signs; the theorem itself remains banked;
4. the positive-packet correction v2 and case record v3 supersede the
   earlier \(\mathbb Q(\sqrt6)\) packet interpretation;
5. results-paper freeze v3 supersedes freezes v1/v2.

## Present and correctly represented

All eight requested headline contributions are in the current paper:

1. the order-six \(\mathbb Q(\sqrt7)\) theorem and
   \(\mathbb Q(\sqrt{14})\) replication;
2. the order-ten \(\mathbb Q(\sqrt{33})\) theorem;
3. RQ-002057, the ramified-prime-\(3\) control;
4. the uniform Engine-A theorem;
5. RQ-000458 with two mathematical proofs and the conservative process
   tag `DUAL_ROUTED`;
6. the generic \(\mathbb Q(\sqrt{35})\) closure beyond class number
   one;
7. the corrected \(\mathbb Q(\sqrt6)\), \(e=(8,12)\), closure;
8. the absolute-abelian no-go lemma.

The seven Engine-B rows all have proof routes, candidates, margins,
and record pointers.  One \(e=6\) Engine-C polynomial is printed.  The
\(\mathbb Q(\sqrt6)\) anti-unit/positive-packet distinction and the
seal-order history are explicit.

## Genuine theorem-level omissions or under-promotions

### 1. General-\(e\) Engine-C theorem

Cycle 059 banks the normalization and torsion-invariant orientation
argument as `VERIFIED_THEOREM`, uniform in \(e=|\mu(E)|\), with
specializations \(e=6,8,12\).  The manuscript contains the formulas
and much of the proof inside Engine C, but it does not state a named
theorem or give this result an epistemic status in the theorem
inventory.

Authoritative records:

- `data/engine-c-general-e-theory-v1.json`,
  SHA-256
  `1067e3cd00cbbb5a33c55b698353a3554d991090f6c4e4997e8d5ebebdf68233`;
- corrected specialization display:
  `data/engine-c-general-e-theory-v3.json`,
  SHA-256
  `7dbc2bf3a1b2e0aa6be46cfe4391aacca40e4fe01b0c3a130d3d0c826ae44629`.

Required repair: promote equations (17)--(18) and the finite
coefficient/Artin orientation procedure to a named proposition or
theorem, state its boundary \(|S|\ge3\), and add the v3 record to the
reproducibility table and core manifest.

### 2. Index-parity theorem is outside the printed inventory

The parity lemma is proved in the body, leads the abstract's 446-case
consistency statement, and has its own `VERIFIED_THEOREM` record.
Nevertheless, the introduction says “the paper's contributions are
the following eight items” and omits it.

Authoritative record:
`artifacts/results-paper-index-parity-lemma-v1.json`,
SHA-256
`b5c0307aa82f57113c5f586509c8d8a10cc105e0de955608a342858e649c41f1`.

Required repair: either expand the inventory, or rename the existing
list “eight headline case-and-method contributions” and append the
general-\(e\) and index-parity results as supporting theorem-level
contributions.  Add the parity theorem record—not only its census
audit—to the reproducibility table and core manifest.

### 3. The core manifest is not yet the complete theorem manifest

`artifacts/results-paper-core-manifest-v1.json` includes Engine A and
the parity *audit*, but omits:

- the Engine-C general-\(e\) theorem/correction record;
- the index-parity theorem record;
- the written no-go theorem record.

The last item is a paper proof and need not have a computational
certificate, but if the JSON is called the “core file list,” the
theorem-source document or a manuscript-line pointer should be
included.

## Important explanatory facts present in records but missing from prose

These do not change a theorem, but they strengthen claims already made.

1. The \(\mathbb Q(\sqrt{14})\) replication is driven by the totally
   positive unit \(15+4\sqrt{14}\), of norm \(+1\), congruent to one
   modulo \(\mathfrak p_7\).  The paper calls the case a structural
   replication without printing this mechanism.
2. RQ-002955 over \(\mathbb Q(\sqrt{77})\) independently forces the
   same average of upper and lower half-open Shintani conventions as
   RQ-000021.  The paper explains the boundary rule only for
   RQ-000021.
3. The \(\mathbb Q(\sqrt{35})\) polynomial is the first
   mixed-signature output of the *generic Engine-C tranche*, not the
   first mixed-signature packet in the full corpus.  The current paper
   prints signature \([4,2]\) but not this precise methodological
   significance.
4. Empty differenced support gives \(Z'_{\mathfrak m}(0,A)=0\) and
   \(X_A=1\) directly by Fourier inversion.  This is implicit in
   Theorem 1 and the parity lemma.  A count-free corollary would make
   the quadratic/empty-support floor conceptually complete without
   importing census statistics.

## Prior-art obligations still open

The local literature freeze made four comparisons mandatory.  The
paper now distinguishes the Cohen--Roblot Hilbert-class-field objects
and the DST theorem class, but the background comparison note remains
explicitly incomplete:

- no case-by-case comparison with Tangedal's proved special cases;
- no exact alignment of DST 2003's \(S\), absolute-value
  normalization, and hypotheses with the uniform Engine-A theorem;
- Cohen--Roblot containment checks for the class-number-two promoted
  bases remain queued, although object *identity* is already excluded
  by the nontrivial ray modulus.

Until these close, “apparently first” must remain a bounded historical
observation, never a theorem or universal priority claim.  Removing
the priority sentence entirely is also safe.

The bibliography audit found eight uncited entries:
Yamamoto 2010, Tangedal 2007, Voutier 1996, Kopp 2025,
Dasgupta--Kakde 2023, Tangedal--Young 2013, PARI, and python-flint.
Yamamoto, Tangedal, Voutier, PARI, and python-flint are directly used
or named and should be cited in the relevant prose.  The remaining
entries should either be discussed in a related-work paragraph or
removed from this paper's bibliography.

## Correct exclusions and superseded material

The following should not be restored to the results paper:

- all v1--v4 census counts, the proxy-derived 88-row odd-index
  population, and its retracted 85/88 and 86/88 correlations;
- the rejected 276-case Engine-D population;
- RQ-007500, which genuinely re-passes W2 but has no promoted W3
  packet;
- the \(\mathbb Q(\sqrt{111})\) case, whose W2 safe exponent is
  \(13{,}810{,}176\) but whose W3 identification remains pending;
- the dimension-16 TCC diagnostic, which belongs to Paper III;
- W4 conductor trends, frontier counts, and completeness claims, which
  belong to the census paper;
- the ten additional B/C alignments, which are not dual proofs;
- the old zero-real-root \(\mathbb Q(\sqrt6)\) polynomial as a packet
  polynomial.

## Recommended repair order

1. Name and inventory the general-\(e\) theorem and index-parity
   theorem; repair the core manifest.
2. Add the three short explanatory facts for
   \(\mathbb Q(\sqrt{14})\), RQ-002955, and
   \(\mathbb Q(\sqrt{35})\).
3. Fix direct citations and decide whether to complete or remove the
   bounded priority claim before submission.
4. Issue paper freeze v4 only after those edits and the same
   deterministic-build/referee-audit gates.
