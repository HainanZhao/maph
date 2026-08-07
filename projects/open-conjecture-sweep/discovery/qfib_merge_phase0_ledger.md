# q-Fibonomial / aligned-center merge: Phase 0 ledger

Audit date: 2026-08-07 UTC.

Scope: ground-truth checks required by `MERGE_INSTRUCTIONS.md` v3. This is an
append-only research ledger, not manuscript text. No Phase 1--4 or R-cycle
work is authorized by an entry here.

## 0.1 — CIMSY Conjecture 5.4 transcription

**PASS — source statement matches Paper B's condition (1).**

Primary source: Connelly--Ito--Martinez--Shevchenko--Yang,
arXiv:2605.12822v1, source file `main.tex`, Section 5.2. The source archive
was retrieved from `https://export.arxiv.org/e-print/2605.12822`; SHA-256:

```text
085dd2ad7278821b71380ea3c2020f1f71a6eb988118f389ac0d31e304a9e5bf  source archive
f91a4d1a01e529b3a6e573167f5a323172d15427f1956a2dd8c63416513a78ed  main.tex
```

Verbatim source text:

> Let \(r \geq2, k \geq 1\) and let \(a_1,\ldots, a_k,b\) be positive
> integers. Then if \(r \mid a_i\) for any \(1 \leq i \leq k\) or
> \[
> b \leq 1+\sum_{i=1}^{k}\left\lfloor\frac{a_i}{r}\right\rfloor,
> \]
> the polynomial \([a_1]_q\dots[a_k]_q[b]_{q^r}\) is unimodal. Moreover,
> if \(k \leq 3\) or \(r \leq 3\), this condition is also necessary.

The source uses the macro `\pow` where the transcription above displays
`r`; this is only a notation expansion. Character-level comparison against
`paper/qanalog-conjecture54/main.tex`, lines 52--65:

- `r >= 2`: exact;
- `k >= 1`: exact;
- all `a_1,...,a_k,b` positive integers: exact;
- divisibility is existential over `1 <= i <= k`: exact;
- the disjunction is `or`: exact;
- the inequality is weak (`<=`): exact;
- the right side is `1 + sum_i floor(a_i/r)`: exact;
- no side condition was dropped.

Claim tag: **PROVED** (exact source transcription and direct diff).

## 0.2 — BCK Conjecture 2.5 and width convention

**PASS — Paper A's theorem is exactly the width-four subfamily, including
the source's positive-parameter convention.**

Primary source: Bergeron--Ceballos--Küstner, SIGMA 16 (2020), paper 076,
source file `sigma20-076.tex`. The source archive was retrieved from
`https://export.arxiv.org/e-print/1911.12785`; SHA-256:

```text
c264a4be028aebb7ab0e1367928cf1d32b17d27d3a0faf1a730105915f572b23  source archive
095f106cef00a29e2ff6f8d6970a31b7ece9fa8138c2e1a3bf5b0ceeb89b35e8  sigma20-076.tex
```

Verbatim Conjecture 2.5:

> The polynomials \(\left[\!\begin{smallmatrix}m+n\\n\end{smallmatrix}\!\right]_{\mathcal F}\)
> are unimodal.

The source defines `N := {1,2,3,...}` and, for `m,n in N`,

\[
\left[\!\begin{matrix}m+n\\n\end{matrix}\!\right]_{\mathcal F}
=\frac{[F_{m+n}]_q^!}{[F_m]_q^![F_n]_q^!},\qquad
[F_j]_q^!=\prod_{i=1}^j[F_i]_q.
\]

BCK's macro takes arguments `(m,n)` while displaying `(m+n choose n)`.
CIMSY and Paper A instead display `(m+n choose n)` directly. Thus "width"
is the fixed second parameter `n` in both manuscripts. Paper A's theorem
`[m+4 choose 4]_F` for every integer `m >= 1` is precisely BCK Conjecture
2.5 with `n=4`. Its domain agrees with BCK's positive-natural convention;
the explicit cases `m=1,...,7` include every small positive `m` omitted by
the uniform estimate. No `m=0` case belongs to the stated source domain.

Claim tag: **PROVED** (primary-source definitions and direct specialization).

## 0.3 — CIMSY status table

**PASS — proved, conjectured, and computationally verified statements are
separated below.**

| Source item | Exact status in CIMSY | Scope |
| --- | --- | --- |
| Theorem 1.2 | **PROVED** | q-Fibonomial unimodality for widths `n=1,2,3`. |
| Proposition 1.3 (proved later as the proposition labeled `lem:unimodal_iff_special_case`) | **PROVED** iff | `[a]_q[b]_q[c]_(q^2)` is symmetric unimodal iff `2c <= a+b`, or `a` or `b` is even. This is the `(k,r)=(2,2)` case of the proposed criterion. |
| Lemma `lem:unimodal_an` and Corollary `cor:divisionunimodal` | **PROVED** | The divisibility branch: if the spacer step divides an ordinary-factor length, the relevant product is symmetric unimodal. |
| Proposition `prop:unimodal` | **PROVED** iff | For one ordinary factor, `[a]_q[b]_(q^r)` is unimodal iff `a >= r(b-1)` or `r | a`. This is the `k=1` case. |
| Conjecture 5.4 | **CONJECTURED** | Sufficiency for all `k>=1,r>=2`; necessity when `k<=3` or `r<=3`. The already-proved `(2,2)` and `k=1` cases lie inside this conjectured necessity region. |
| Sentence after Conjecture 5.4 | **OBSERVED** | Exact finite verification for `k<=5`, `r<=6`, and `max({a_i},b)<=15`. |
| Counterexample after Conjecture 5.4 | **PROVED** by direct expansion / source-stated example | `([3]_q)^4[2]_(q^4)` is unimodal while violating the inequality, so necessity fails in general. |

Required attribution consequence: the merged introduction may say CIMSY
*conjectured* necessity for `k<=3` or `r<=3`, but it must immediately qualify
that CIMSY already proved the full iff at `(k,r)=(2,2)` and the `k=1`
characterization. Saying necessity is wholly open throughout that region
would be false.

Claim tag: **PROVED** for the classification table; the bounded computation
row remains **OBSERVED** because it reports CIMSY's finite verification.

## 0.4 — Paper A dependency audit

**FAIL — no Paper B lemma is used by Paper A, nor is a Paper A proof lemma a
special case of Paper B's aligned-center recursion machinery.**

Paper A's actual proof dependencies are:

| Paper A dependency | Classification against Paper B | Role in Paper A |
| --- | --- | --- |
| BCK Theorem 2.4 (polynomiality and nonnegative coefficients) | (iii) genuinely additional external input | Makes the rational q-Fibonomial expression a nonnegative polynomial. |
| q-reciprocity `[r]_(q^-1)=q^(1-r)[r]_q` | (iii) genuinely additional elementary input | Establishes symmetry and the exact degree of the quotient. |
| Restricted partition formula for `p(t)=[q^t]/((1-q)(1-q^2)(1-q^3))` | (iii) genuinely additional machinery | Supplies the period-six quasipolynomial and quadratic bounds. |
| Midpoint coefficient-difference formula | (iii) genuinely additional machinery | Inclusion--exclusion reduces each first difference to four translates of `p`. |
| Concave quadratic endpoint estimates | (iii) genuinely additional machinery | Proves all `m>=8`. |
| Exact checks for `m=1,...,7` | (iii) genuinely additional finite base | Covers all remaining positive parameters. |

Counts: category (i), identical to a Paper B lemma: **0**. Category (ii),
special case of a Paper B lemma: **0**. Category (iii), genuinely additional:
**6 dependency groups**.

Paper B's closure lemma is not invoked by Paper A. Paper A derives symmetry
from the complete rational quotient and proves unimodality through first
differences; it never decomposes the width-four polynomial into instances of
the one-spacer theorem. The denominator contributes the two steps `2` and
`3`, but Paper A absorbs them simultaneously through the generating function
`1/((1-q)(1-q^2)(1-q^3))`, not through one- or two-spacer aligned-center
recursion.

The planning note about bad residue classes `m = 9,10 mod 12` does not match
Paper A. The manuscript contains no residue-class split. Its only split is
`m>=8` versus the seven exact cases `1<=m<=7`.

Gate outcome: `MERGE_INSTRUCTIONS.md` says, "Phase 0.4 shows no shared
machinery: pause after Phase 0, escalate." That stop condition is met. A
two-part paper with a common introduction is the plan's stated fallback, but
selecting it requires the author's direction.

Claim tag: **PROVED** (complete manuscript dependency audit).

## 0.5 — Archive replay and DOI resolution

**FAIL — Paper A's deposited archive passes; Paper B's DOI does not resolve,
so both deposited archives cannot be replayed end to end.**

Paper A:

- DOI `10.5281/zenodo.21826970` resolved to the public Zenodo record.
- The downloaded file `03-width-four-q-fibonomial-replay.zip` matched the
  record's MD5 `8efefbf2aa6a7339ce3ab71078ad36fd` and had SHA-256
  `886e887208af57981b935a7a2d98a7797c18a154275a6b58d110fdd34941313c`.
- From a fresh extraction, the runner printed:

```text
PARTITION_FORMULA_PASSED_T0_TO_300
SMALL_CASES_PASSED_M1_TO_7
DIRECT_QUOTIENT_CROSSCHECK_PASSED_M1_TO_24
```

- Measured replay: 1.91 s wall time, 99,244 KiB peak RSS.

Paper B:

- DOI `10.5281/zenodo.21830407` and Zenodo record `/records/21830407` both
  returned HTTP 404 on 2026-08-07 UTC. `RESULTS_LEDGER.md` describes this DOI
  as reserved with public-file verification pending.
- Therefore the manuscript header does **not** currently resolve to an
  archive, and the required deposited-archive replay cannot be performed.
- As a quarantined local check only, the current deterministic release
  builder produced a prospective replay ZIP with SHA-256
  `2157ae9ac923db87d5d00d99d4587f2676dc3a6da74eeee9232f6cb82d1bf4eb`.
  From a fresh extraction its runner returned status `PASS`, checking 1,680
  identity rows by two routes and 15,163 direct induction rows.
- Measured prospective replay: 2.57 s wall time, 12,928 KiB peak RSS.

The local prospective replay is **OBSERVED** validation of the current tree;
it is not evidence that the DOI archive exists or matches the tree.

## Phase 0 gate outcome

Phase 0 is complete with `0.1 PASS`, `0.2 PASS`, `0.3 PASS`, `0.4 FAIL`, and
`0.5 FAIL`. Per the explicit stop condition attached to 0.4, manuscript
editing and Phases 1--R are paused. The two independent blockers are:

1. the proposed narrative spine claims shared proof machinery that the
   dependency audit does not find; and
2. Paper B's recorded DOI is not yet a resolvable replay archive.

## 2026-08-07 — R-cycle rebase authorized by the author

The Phase-0 stop remains binding for the proposed manuscript merge. The
author separately re-based R1--R3 as successor research independent of that
merge, preserving their budgets and gates. This entry supersedes only the
last paragraph's pause on R-cycle work; it does not alter any Phase-0 result
or authorize a merged manuscript.

### R1 — two-spacer recursion

**Gate outcome: SUCCESS under branch (a); R1(b) not opened.**

`discovery/two_spacer_aligned_recursion.md` proves a two-spacer sufficiency
theorem. Multiplying the aligned-center identity by the second spacer makes
the correction term a one-spacer product, which is closed by Paper B's proved
criterion. The theorem gives an allocation criterion and an explicit
gap-absorption corollary. Per the re-based gate, it is recorded as its own
future paper question and stops here; it is not inserted into either current
manuscript.

Exact regression:

```text
{"center_steps_checked": 5262, "exhaustive_rows": 4146, "random_rows": 500, "seed": 20260807, "status": "PASS"}
```

Claim tag: **PROVED** by the written induction; the finite corpus is
**OBSERVED** regression evidence.

### R2 — width-five and width-six denominator map

**Gate outcome: computational observation recorded; no conjecture stated.**

The exact structural census through `m=240` is in
`experiments/qfib_width_5_6_denominator_map.json`, with interpretation in
`discovery/qfib_width_5_6_denominator_assessment.md`.

- Width five has denominator atoms `2,3,5`. In the stable period-60 map, 18
  residue classes admit no injective bracket assignment; all other classes
  retain three nontrivial spacers.
- Width six has atoms `2,3,5,8`. Thirty stable classes admit no injective
  assignment; all other classes retain four nontrivial spacers.
- The first-difference restricted-partition kernels have parts `1,2,3,5`
  and `1,2,3,5,8`, respectively.

Assessment: Paper A's restricted-partition mechanism is the more plausible
width-five route. The direct one-/two-spacer cancellation route does not
cover a stable residue class in the enumerated decomposition model. This is
not a no-go theorem for other aligned-center decompositions.

Claim tag: **OBSERVED** exact computational structure; no unimodality claim
or conjecture is promoted.

### R3 — literature verification

**Gate outcome: closed; no Paper B framing change triggered.**

`discovery/qfib_successor_literature_audit.md` records the source checks.
Odlyzko--Richmond's relevant results concern almost unimodality of partition
products and eventual unimodality of high convolution powers. Almkvist's
located theorem concerns a structured Gaussian-type quotient. None supplies
the finite two-spacer estimate. No post-May-2026 CIMSY/BCK follow-up or prior
appearance of identity (3) was found in the bounded search. The last finding
is **OBSERVED**, not a priority claim; Paper B continues to frame the
contribution as the application and proof method rather than novelty of the
bare elementary identity.

## 2026-08-07 — W0 supersession and containment

The author imposed W0 as a new blocking closeout gate. This entry supersedes
the earlier R2 and R3 gate outcomes above.

- The earlier R2 entry is **NOT CLOSED**. Its proposal note was removed so no
  R2 interpretation remains outside this ledger. The raw deterministic JSON
  is retained only as W0.1's byte-comparison target.
- The earlier R3 closeout is withdrawn. The associated proposal note was
  removed; Odlyzko--Richmond, Almkvist, later-follow-up, and identity-prior-
  art claims revert to **UNVERIFIED** until W4 runs under the new protocol.
- W1--W4 have not started. W0 remains blocking.

### W0.1 — second-agent map recomputation

**PENDING / BLOCKING.** This side conversation is prohibited from spawning
or using another agent. The existing first-agent table has SHA-256
`f56797d77f607a6ad818cb1d24b5899cffd9629bdc20880ab09bfcc6e6138685`.
A different agent must independently write its own exact-arithmetic program,
recompute through `m<=240`, and establish byte-level agreement for the
width-five class table before W0 can close.

### W0.2 — bad-class unimodality

**FIRST IMPLEMENTATION PASS; awaits W0 closeout.** For every `m<=240` whose
residue modulo 60 lies in

```text
9, 10, 12, 16, 17, 18, 21, 27, 33,
36, 37, 38, 42, 44, 45, 56, 57, 58
```

the exact symbolic checker found every width-five midpoint coefficient
difference nonnegative. It checked 72 instances and 12,960 fixed-residue
polynomial intervals; the minimum difference was 1.

The checker represents the restricted partition function for parts
`1,2,3,5` by its 30 exact cubic quasipolynomials, validates those against
direct dynamic programming, and minimizes each signed-translate cubic using
exact rational arithmetic. Small feasible cases are independently checked
coefficient by coefficient. Replay:

```sh
python3 experiments/qfib_width5_bad_class_unimodality.py
```

Expected output:

```text
{"bad_residues": [9, 10, 12, 16, 17, 18, 21, 27, 33, 36, 37, 38, 42, 44, 45, 56, 57, 58], "instances_checked": 72, "maximum_m": 240, "minimum_difference_overall": 1, "quasipolynomial_period": 30, "status": "ALL_UNIMODAL", "symbolic_residue_intervals_checked": 12960}
```

Checker SHA-256:
`042f5d1bbf907af19e5aaf70d2b1d0c61ff7aac154d4760a1a43a24ff44d2ad3`.

Claim tag: **CERTIFIED_NUMERICAL** for this bounded first implementation. No
counterexample candidate was found, so the triple-implementation emergency
gate was not triggered.

### W0.3 — n=6 disposition

**CLOSED AS DEFERRED.** The prior R2 run produced a preliminary `m<=240`
map but did not satisfy the new independent-recomputation and factorization
requirements. The n=6 half is explicitly deferred to W2. No n=6 table may be
cited outside this ledger before W2's second-agent gate passes.

### W0.4 — R2 closeout

**PENDING.** R2 is not closed. W0.4 may be written only after W0.1 passes.

Tag correction for W0.2: because the computation is exact rather than an
enclosure calculation, and its independent implementation is still pending,
the bounded result is classified **OBSERVED (exact arithmetic)**, not
`CERTIFIED_NUMERICAL`. The W0.2 result is not promoted beyond this ledger.

## 2026-08-07 — W0 independence waiver and closeout

The author explicitly replaced the different-agent requirement with a
single-researcher requirement. W0.1 is therefore interpreted as two
independently implemented exact routes by the same researcher.

### W0.1 — PASS under the revised independence rule

The second implementation uses modular Fibonacci recurrences and a recursive
matching enumeration; it does not import or call the first implementation.
It reconstructed the stable width-five residue table and compared a canonical
JSON rendering byte for byte with the first table.

```text
{"bad_class_count": 18, "bad_classes": [9, 10, 12, 16, 17, 18, 21, 27, 33, 36, 37, 38, 42, 44, 45, 56, 57, 58], "canonical_table_sha256": "36acf985b6540715dcb77cb4294e172868a482545bec412b7eb19599291cbc22", "good_class_spacers": [2, 3, 5], "good_classes": 42, "status": "BYTE_IDENTICAL"}
```

Replay:

```sh
python3 experiments/qfib_width5_map_independent_check.py
```

Second-implementation SHA-256:
`2580d515c9c53320ba0effc714dfef91ec41b895966a56f77cdc41fe6c7464a8`.

### W0.4 — R2 CLOSED

W0.1 passed under the author-revised independence rule; W0.2 found all 72
computed bad-class instances unimodal; and W0.3 explicitly deferred the
unfinished n=6 half to W2. R2 is **CLOSED**. The evidence preserves full
plausibility of BCK Conjecture 2.5 at width five; it is not a proof.

W1 is now unblocked. W2 retains the n=6 work. W3 and W4 retain their stated
priority and budget restrictions.

## 2026-08-07 — W1 Outcome A

**PROVED.** For every integer `m>=1`, the width-five q-Fibonomial
`[m+5 choose 5]_F` is unimodal.

The proof extends Paper A's first-difference kernel from parts `1,2,3` to
parts `1,2,3,5`. The new restricted-partition function has the especially
rigid form

```text
p(t) = t^3/180 + 11*t^2/120 + 9*t/20 + rho_(t mod 30),
91/360 <= rho <= 1.
```

After exact subset-shift cancellation, every midpoint difference is a sum of
six translates. Worst-case use of the two error endpoints yields positive
piecewise-polynomial lower bounds for `m>=8`; the exact cases `m=1,...,7`
have minima `0,0,0,1,1,1,1`.

Outcome files:

- proof development: `discovery/qfib_width5_direct_attempt.md`;
- standalone mathematical draft: `paper/qfib-width-five/main.tex` and
  `main.pdf`;
- one-command replay: `proof/qfib_width5_unimodality_proof.py`;
- verification record: `paper/qfib-width-five/verification.md`.

The exact replay passed the kernel, inclusion--exclusion, direct quotient,
finite-case, lower-envelope, and `m<=240` symbolic regression checks. The
four-page manuscript compiled twice without warnings and was visually
inspected.

Claim boundary: width five only. Width six and the general BCK conjecture
remain open. W1 is closed at Outcome A; speculative strengthening stops here.

## 2026-08-07 — W2 structural prediction test

**PASS.** The width-six denominator lengths are `1,1,2,3,5,8`, and direct
cyclotomic factorization gives

```text
Phi_2^2 Phi_3 Phi_4 Phi_5 Phi_8.
```

The Fibonacci entry ranks are respectively `3,4,6,5,6`; hence the structural
modulus is `lcm(3,4,6,5,6)=60`. The discussion's extra working value 12 is
not an entry rank for the actual width-six denominator and is unnecessary;
including it happens not to change the lcm.

The first-difference kernel predicted from the denominator has parts
`1,2,3,5,8`, quasipolynomial degree four, and period dividing 120. Exact
arithmetic through `m=240` found at least one cyclotomic-factor assignment in
every residue class. A separately implemented modular-recurrence route
reproduced the 60-row canonical table byte for byte:

```text
{"canonical_table_sha256": "3c5b527b750cab599974d5e470835b72212fb01d075f7229abc769ec82ce613b", "residue_classes": 60, "status": "BYTE_IDENTICAL"}
```

Replays:

```sh
python3 experiments/qfib_width6_structural_test.py
python3 experiments/qfib_width6_structural_independent_check.py
```

Claim tag: **OBSERVED (exact arithmetic)** structural prediction. No
width-six unimodality claim is made. W2 is closed.

## 2026-08-07 — W4 carry-over audit

**CLOSED with no framing change.** The width-five follow-up sub-check was
mistakenly run immediately after, rather than before, W1. The violation was
contained before any dissemination or final manuscript gate. Fresh arXiv,
OpenAlex, and Crossref searches through 2026-08-07 found CIMSY's
arXiv:2605.12822 but no later width-five proof or Conjecture 5.4 resolution.
Thus no indexed overlap with W1 was found. This is **OBSERVED**, a bounded
search rather than a priority theorem.

The two memory claims resolve as follows:

- Odlyzko--Richmond (1982), DOI
  `10.1016/S0195-6698(82)80010-3`, proves almost unimodality for a wide class
  of products `prod(1+x^a_i)`, allowing a bounded exceptional edge region;
  it is not full arbitrary-product unimodality.
- Odlyzko--Richmond (1985), DOI `10.1214/aop/1176993082`, proves eventual
  unimodality for sufficiently high convolution powers under endpoint-
  support hypotheses. It gives no applicable finite multi-spacer threshold.
- Almkvist (1989), DOI `10.1016/0022-314X(89)90096-6`, treats the structured
  Gaussian quotient `prod_(nu=1)^r (1-t^(n nu))/(1-t^nu)` in specified n
  ranges, not arbitrary q-integer quotients.

Publisher full texts for the two Elsevier papers were access-blocked; exact
scope was checked against publisher abstracts, zbMATH review text, and
OpenAIRE metadata. No finer manuscript attribution is made.

No indexed prior appearance of identity (3) was found by exact-pattern,
q-integer-recursion, and citation searches. Because the identity is
elementary, this is weak negative evidence only. Paper B already claims the
application and method rather than priority for the bare identity, so no
Item-2 edit is triggered.

## 2026-08-07 — W3 multi-spacer criterion

**PROVED; record and stop.** For arbitrary spacer count `s` and arbitrary
steps `r_j` (coprimality is unnecessary), the product

```text
prod_i [a_i]_q prod_j [b_j]_(q^r_j)
```

is symmetric unimodal whenever there is a nonnegative integer allocation
matrix `d_(j,i)` whose row sums are `b_j-1` and which leaves

```text
a_i - sum_j r_j d_(j,i) >= 1
```

for every ordinary factor. The proof inducts on the number of spacers; the
same remaining allocation certifies every aligned-center correction term.
In particular, if some `a_i >= 1 + sum_j r_j(b_j-1)`, the product is
unimodal.

The proof and boundary are in
`discovery/multi_spacer_aligned_recursion.md`. Exact recursive regression
checked 400 deterministic random instances with up to four spacers and
43,002 nested recursion steps:

```text
{"random_rows": 400, "recursion_steps": 43002, "seed": 20260807, "spacers_max": 4, "status": "PASS"}
```

This is W3's full-strength success and becomes its own future topic. Per the
gate, no current manuscript is changed and work stops here.

## 2026-08-07 — W3 gate deviation, strengthening, and W1 relation

**AUTHORIZED DEVIATION RECORDED.** The original W3 gate was
proposal-note-and-stop.  After the first matrix theorem was written, the
author required an adversarial audit, the missing divisibility branch, and
an exact comparison with the completed width-five theorem.  Work therefore
continued within W3 beyond the first stop point.  The reason was material:
the bare matrix theorem does not recover the already-proved one-spacer
criterion, so freezing it would have overstated its scope and left an
avoidable weaker result.  No dissemination action was taken.

### Hybrid criterion

**PROVED.** Choose pairwise disjoint spacer/ordinary-factor pairs satisfying
`r_j | a_i`, remove those factors, and apply the allocation matrix to the
residual product.  Each removed pair is symmetric unimodal by

```text
[r_j e]_q [b_j]_(q^r_j)
  = [r_j]_q ([e]_z [b_j]_z)|_(z=q^r_j),
```

and closure under products combines these pair factors with the residual
matrix-certified factor.  Each ordinary column is consumed at most once.
For one spacer, this recovers both the divisibility and inequality branches
of the proved criterion.  The proof permits repeated steps and `r_j=1`.

The exact small-parameter regression checked 6,833 hybrid-certified products
and verified the one-spacer equivalence throughout the declared finite
range.  Claim tag: **PROVED** by factorization and closure; finite rows are
**OBSERVED** regression evidence.

### Adversarial boundary

**PROVED / OBSERVED.** The allocation matrix cannot certify
`[2]_(q^2)[2]_(q^3)`: after adjoining neutral `[1]_q`, the two required row
allocations would leave `1-2-3<1`.  Its coefficients are exactly
`1,0,1,1,0,1`, so it is not unimodal.

For `[a]_q[2]_(q^2)[2]_(q^3)`, the matrix activates exactly at `a=6`.
Exact coefficients show non-unimodality at `a=1,4`, unimodality at
`a=2,3,5`, and unimodality for every checked `6<=a<=15`.  Thus the matrix's
eventual threshold trails the observed tail threshold `a=5` by one; it is
not a necessity statement.  With equal steps
`[a]_q[2]_(q^2)[2]_(q^2)`, it activates at `a=5`, while `a=2` is already
unimodal.  If a nontrivial step exceeds `sum_i(a_i-1)`, its row cannot be
funded, so the criterion is silent.

### Width-five subsumption decision

**PROVED exact applicability census.** Every stable residue class modulo 60
and every injective assignment of the denominator atoms `2,3,5` was checked.
Matrix feasibility was decided by an exact bounded-weight residue algorithm,
independently compared with brute force on 93,618 small interval instances.

| Route | Stable classes reached |
| --- | --- |
| Matrix only | `2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54` |
| Divisibility absorption only | none |
| Hybrid | `2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54` |

The 24 decomposable but unreached classes are
`0,1,5,6,11,13,15,19,20,22,25,28,30,34,35,39,40,43,46,48,50,52,55,59`.
The remaining 18 classes have no injective bracket decomposition.  Hence W3
does **not** subsume the width-five theorem: it reaches 18 classes, while the
restricted-partition kernel proves all 60 uniformly.

Replay:

```sh
python3 experiments/multi_spacer_adversarial_and_width5_overlap.py
```

### Remaining W1 verification gates

**PASS.** An independently written SymPy 1.12 calculation reconstructed all
six explicit envelope constants and all six shape arguments for
`a>=34,d>=1`; it imports neither earlier width-five checker.

**PASS.** The width-five theorem is the exact `n=5` specialization of the
verbatim BCK Conjecture 2.5 transcription, including `m>=1`.  A fresh read of
the introduction alone correctly identifies the prior `n<=3` and `n=4`
results, the new width-five theorem, and the explicit nonclaims (width six,
the full conjecture, log-concavity, and a chain decomposition).

**PASS.** Case-insensitive search of all manuscript-bound `.tex`, `.bib`, and
`.sty` files found zero internal workflow terms from the declared grep list.

## 2026-08-07 — Paper B / W3 criterion-paper merge

**PROVED / LOCAL MERGE COMPLETE.** The author directed a single-researcher
merge of Paper B and W3. Gate 0.1 passed: W3 is the matrix lift of the same
aligned-center recursion, closure lemma, one-spacer increment, and `E+2r_j`
center calculation. The combined manuscript is
`paper/qanalog-multispacer-criterion/main.tex`.

The manuscript states the CIMSY sufficient direction first, then the hybrid
multi-spacer theorem. It proves disjoint divisibility absorption, the matrix
induction, the `r_j=1` case, and derives the named one-spacer theorem as a
corollary. The B3 positivity calculation, explicit closure citation in the
divisibility branch, source necessity boundary, correct arXiv identifier,
and AI-assistance statement are present.

The combined exact runner
`proof/qanalog_multispacer_criterion.py` passed all inherited and merged
checks. Principal counts include 1,680 two-route identities, 15,163
one-spacer induction rows, 400 multi-spacer rows with 43,002 nested steps,
6,833 small hybrid-certified products, 93,618 bounded-solver brute-force
comparisons, and the separately written direct corpus of 20 matrix, 10
absorption, and 20 identity cases. Measured runtime was 11.84 seconds with
16,000 KiB peak RSS.

The width-five route table remains matrix `18`, absorption `0`, hybrid `18`;
therefore the separate width-five paper is retained. The combined paper
compiled twice to a clean five-page PDF, passed the manuscript vocabulary
search, and was visually inspected page by page.

**Cleanup decision.** The superseded standalone working-paper directory
`paper/qanalog-conjecture54/` was deleted after its manuscript, README,
license, literature audit, hostile audit, and verification content were
absorbed into `paper/qanalog-multispacer-criterion/`. Its canonical proof
note and runner remain under `proof/`, and W3 discovery evidence remains
under `discovery/` and `experiments/`. The width-four and width-five papers
were untouched by this cleanup.

**External gate deferred.** No DOI was reserved and no deposit was created,
because dissemination is outside the authorized merge. Cold DOI fetch and
deposited-archive replay therefore remain unperformed. The combined paper is
a locally verified working manuscript, not a disseminated final archive.

## 2026-08-07 — Criterion-paper coverage clarification

**PASS under the author's single-researcher rule.** A newly written checker,
`proof/qanalog_width5_coverage_independent.py`, reconstructed the stable
width-five Fibonacci windows directly and imported neither the earlier class
table nor its labels. It confirmed the following disjoint partition modulo
60:

- matrix/hybrid reached, 18 classes:
  `2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54`;
- decomposable but unreached, 24 classes:
  `0,1,5,6,11,13,15,19,20,22,25,28,30,34,35,39,40,43,46,48,50,52,55,59`;
- no injective bracket decomposition, 18 classes:
  `9,10,12,16,17,18,21,27,33,36,37,38,42,44,45,56,57,58`.

The two counts of 18 are therefore coincidental, and the corresponding sets
are disjoint. Divisibility absorption alone reaches no stable class because
all three spacers are nontrivial while a decomposition leaves only two
ordinary factors. Hybrid absorption adds no width-five class, but remains
essential to the combined theorem because it recovers the one-spacer
divisibility branch.

The manuscript now states this boundary and asks which additional mechanism
reaches the 24 decomposable but unreached classes while retaining an
aligned-center proof. The necessity attribution was checked against the 0.3
table and now says explicitly that CIMSY proved the full iff for `k=1` and
for `(k,r)=(2,2)`. The companion-manuscript citation was removed to eliminate
a readiness coupling; only the stable restricted-partition method is
described.

## 2026-08-07 — P1 adaptive allocation probe

**KILLED AS A CURRENT-PAPER UPGRADE; successor lemma banked.** The smallest
adaptive condition compatible with the existing induction was formalized and
proved. If all increments of spacer `j` are assigned to one column `i`, set
`x_0=a_i-r_j(b_j-1)`. It suffices that the residual base at `x_0` is already
certified and that the smallest correction, with that length replaced by
`x_0+2r_j`, is matrix-certified. Later corrections only enlarge the same
length, so the first correction's matrix remains valid.

This condition certifies the near-miss
`[5]_q[2]_(q^2)[2]_(q^3)`. However, recursive exact testing over every stable
width-five decomposition adds zero classes beyond the hybrid theorem's 18.
The predeclared no-coverage-gain kill condition therefore fires before any
attempt to complicate Theorem 2. Broader adaptive certificate trees would
require a genuinely different search/proof interface and remain a successor
question. Proof and replay are in `discovery/adaptive_allocation_probe.md`
and `experiments/qanalog_adaptive_allocation_probe.py`.

## 2026-08-07 — P2 first-dip census

**OBSERVED exact finite regularity.** The census used `1<=k<=5`, `2<=r<=6`,
all `a_i,b<=15`, restricted to `k<=3 or r<=3`, and retained precisely rows
violating both branches of condition (1). All 33,728 violating rows had a
midpoint-side dip. For every one of the 4,576 fixed
`(r,a_1,...,a_k)` groups, the first-dip position was independent of `b`
throughout the violating range; its depth was always one or two.

The sliding-window construction was cross-checked against separately written
naive polynomial multiplication on 100 deterministic rows. Replay is
`experiments/qanalog_one_spacer_dip_census.py`. The manuscript includes one
bounded-data sentence and makes no boundary conjecture.

## 2026-08-07 — P1/P2 interpretation and targeted extension

**PROVED clarification (P1).** The adaptive lemma certifies
`[5]_q[2]_(q^2)[2]_(q^3)`, so the manuscript no longer describes this
example as uncertified in general. It now says precisely that the example
violates static condition (4), identifies the omitted adaptive certificate,
and reports that the refinement adds no stable width-five class. This does
not reopen P1: the predeclared coverage-gain kill condition remains met.

**OBSERVED mechanism (P2).** The first-dip data suggest that, once `b`
violates (1), the first obstruction lies in a low-exponent coefficient
window determined by `(r,a_1,...,a_k)` and is unchanged when further terms
of the lacunary bracket are appended. If this mechanism is correct, the
necessity question reduces to one explicit coefficient inequality at a
position computed from `(r,a_1,...,a_k)`, uniformly in `b`. This is a
candidate proof shape, not a theorem or conjecture.

Falsifiers are: a fixed `(r,a_1,...,a_k)` for which two violating values of
`b` have different first-dip positions; a violating row with no midpoint-side
dip; or failure of the proposed low-window inequality even though a later dip
exists. The observed depth range `{1,2}` is retained only as small-box data
and is not promoted as a pattern.

To probe the shallow `b<=15` range, a deterministic sample of 256 of the
4,576 parameter groups was extended exactly to `b=100`. Sliding-window
construction and separately written direct polynomial multiplication agreed,
and every endpoint retained the original first-dip position. This strengthens
the finite evidence but does not enlarge the manuscript's declared census
box or establish uniformity in `b`.
