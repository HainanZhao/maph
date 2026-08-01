# Cycle 4 P6 CGL-v2 reconstruction preregistration v1

## Claim boundary

`OBSERVED`: this document preregisters a bounded reconstruction audit of Bin
Chen, Vishal Gupta, and Yung Chi Li, arXiv:2507.08296v2. It does not execute
the reconstruction, prove any theorem in the preprint, repair any source
argument, make a novelty claim, promote the stated (7/3) exponent, select a
P7 family, or authorize a new zero-density or short-interval theorem.

The preprint remains prior work and an arXiv preprint. The expected audit
outcome is `OPEN_ANALYTIC_INPUT`, not `PASS`, because the frozen source audit
already exposes unresolved analytic obligations listed below. A source gap
must remain open; no replay may silently add (q\leq T^C), replace
\(\log^2T\) by \(\log^2(qT)\), define “(T)-smooth” after seeing the result,
or supply an omitted primitive-to-all-character argument.

## Registry-count correction

`OBSERVED`: the draft registry was internally inconsistent. The proposed
ranges `S01-S06`, `L01-L13`, `M01-M08`, `Z01-Z10`, `F01-F10` contain

\[
6+13+8+10+10=47
\]

rows, not 46. The inconsistency is resolved before sealing as follows:

- the canonical registry is `S01-S06`, `L01-L12`, `M01-M08`, `Z01-Z10`,
  `F01-F10`, exactly 46 rows;
- canonical `L12` has two separately mandatory subchecks,
  `L12.odd_prime` and `L12.two_power`;
- draft `L13` is preserved as the retired alias `L12.two_power`, not silently
  deleted and not counted as a 47th row.

No analytic obligation is dropped by this schema correction. Either L12
subcheck failing makes the whole L12 row fail.

## Frozen source and conventions

The historical replay pins the canonical CGL-v2 TeX, its arXiv source tar,
the rendered PDF, the immutable authorization snapshot, this document, and
the bounded prior-work audit/correction. It verifies that the named tar member
is byte-identical to the canonical extracted TeX. It does not read or hash the
mutable research plan; any later operational eligibility check is separate
and excluded from historical identity.

The reconstruction must freeze and check these conventions rather than infer
them opportunistically:

- `N(sigma,T,chi)` counts zeros in
  `sigma <= Re rho <= 1`, `|Im rho| <= T`; multiplicity must be audited because
  the displayed source definition does not explicitly state it;
- the large-values theorem uses primitive characters modulo (q),
  (|a_n|\leq1), and pair separation by character inequality or a height gap;
- (q_1\mid q), all logarithms in the exponent normalization use
  \(\log(qT)\), and `o(1)` means (qT\to\infty);
- `lessapprox` absorbs ((qT)^\epsilon) only in that asymptotic sense;
- the Fourier transform is
  \(\widehat f(\xi)=\int_{\mathbb R}f(x)e(-\xi x)\,dx\), with
  (e(x)=e^{2\pi ix});
- the zero detector states (X,Y,T>1), while the headline theorem is stated
  uniformly in (q,T); endpoints and low-(T) cases must be reconciled, not
  assumed away;
- sums over all characters and sums over primitive characters are distinct
  objects until rows Z05 and Z06 close.

For Route B, freeze

\[
\alpha=\frac{\log q}{\log(qT)},\quad \tau=1-\alpha,
\quad\lambda=\frac{\log q_1}{\log(qT)},\quad
\beta=\lambda+\tau=\frac{\log(q_1T)}{\log(qT)}.
\]

When \(q_1\geq\sqrt q\), the route must prove \(\beta\geq1/2\). The four
middle-range coefficient functions are frozen as

\[
\begin{aligned}
C_1(\sigma)&=\frac{3(1+\lambda/3)}{1+\sigma},\\
C_2(\sigma)&=\frac{3(1-\beta/2)}{\sigma},\\
C_3(\sigma)&=\frac{(21-20\sigma)/6-\beta/2}{1-\sigma},\\
C_4(\sigma)&=\frac{15}{3+5\sigma}.
\end{aligned}
\]

Their crossings with (3/(2-\sigma)) must independently yield

\[
\begin{gathered}
(q_1^{1/3}q^2T^2)^{1-\sigma},\qquad
(q^3T^{9/4}q_1^{-3/4})^{1-\sigma},\\
20\sigma^2-(43-3\beta)\sigma+24-6\beta=0,\\
B=\frac{37+3\beta-\sqrt{9\beta^2+222\beta-71}}{12},\qquad
C_4(7/10)=30/13.
\end{gathered}
\]

For \(q_1=q\), hence \(\beta=1\), the four bases/coefficient constants must
reduce to (q^{7/3}T^2), (9/4),
((10-\sqrt{10})/3), and (30/13). The proposed uniform (7/3) comparison
must use exact inequalities: (2\leq7/3),
(7/3-9/4=1/12),
(7/3-(10-\sqrt{10})/3=(\sqrt{10}-3)/3>0), and
(7/3-30/13=1/39).

## Canonical 46-row registry

Every row begins `UNEXECUTED`. Locators are frozen against the canonical TeX;
reconstruction may refine a locator only through a versioned
correction. `EXPECTED_OPEN` records a preregistered blocker, not a theorem
finding.

| ID | Obligation | Frozen TeX locator | Preregistered disposition |
|---|---|---|---|
| S01 | TeX/tar-member/PDF identity and complete-source boundary | entire TeX; tar member; PDF | `UNEXECUTED` |
| S02 | authors, collaboration/version statement, title, and preprint status | 77--105 | `UNEXECUTED` |
| S03 | zero-count definition, two-sided height, rectangle, and multiplicity audit | 95--101, 141--148, 158--185 | `UNEXECUTED` |
| S04 | domains for (q,T,X,Y,\sigma), endpoints, and (qT\to\infty) interpretation | 114--128, 158--187, 268--270, 2114 | `UNEXECUTED` |
| S05 | `o(1)`, epsilon, `lessapprox`, constants, and limiting-order convention | 122--126, 268--273 | `UNEXECUTED` |
| S06 | complete external-input inventory with exact theorem hypotheses and primary-source locators | 133--140, 537--560, 1691--1695, 2112, 2158, 2169, 2414--2467 | `EXPECTED_OPEN:S06_EXTERNAL_INPUTS` |
| L01 | Partial-LVE hypotheses: primitive characters, coefficients, separation, threshold, and length | 114--123 | `UNEXECUTED` |
| L02 | divisor-sensitive four-term Partial-LVE formula | 122--124 | `UNEXECUTED` |
| L03 | all-case four-term Partial-LVE formula | 125--127 | `UNEXECUTED` |
| L04 | low-value comparator and valid range from the (qT) mean-value theorem | 133--136, 421 | `UNEXECUTED` |
| L05 | intermediate-value reduction, three-piece smoothing, and separation thinning | 375--443 | `UNEXECUTED` |
| L06 | high-value HMH comparator and valid range | 137--140, 421, 487--500 | `UNEXECUTED` |
| L07 | (qT\leq N) case and epsilon-limit step | 445--448 | `UNEXECUTED` |
| L08 | (N\leq qT\leq N^{6/5}) Auxiliary-proposition case | 449--452 | `UNEXECUTED` |
| L09 | subdivision case (q_1>N^{6/5}) | 454--478 | `UNEXECUTED` |
| L10 | subdivision case (N^{6/5}/T<q_1<N^{6/5}) | 454--470, 480--485 | `UNEXECUTED` |
| L11 | subdivision case (q_1<N^{6/5}/T), including HMH combination | 454--470, 487--504 | `UNEXECUTED` |
| L12 | character subdivision with mandatory `odd_prime` and `two_power` subchecks; draft L13 is the retired second-subcheck alias | 507--519 | `UNEXECUTED` |
| M01 | smoothed Auxiliary proposition, bump normalization, hypotheses, and conclusion | 375--387 | `UNEXECUTED` |
| M02 | matrix and singular-value reductions, trace subtraction, constants, and inherited hypotheses | 528--550 | `UNEXECUTED` |
| M03 | Hilbert--Schmidt/cubic-trace expansion, Poisson conventions, diagonal subtraction, and errors | 552--660 | `UNEXECUTED` |
| M04 | (S_1) partition and estimate with all ranges | 661--733 | `UNEXECUTED` |
| M05 | (S_2), approximate functional equation, dyadic variables, and bound | 734--1128 | `UNEXECUTED` |
| M06 | affine-transformation estimate with GCD twist, induction, Fourier decay, and norm comparisons | 1129--1686 | `UNEXECUTED` |
| M07 | character-time energy definition, Heath--Brown input, hypotheses, and closing estimate | 1688--1709, 1963--1971 | `UNEXECUTED` |
| M08 | (S_3) estimate and dominance calculation closing the Auxiliary proposition | 1974--2105 | `UNEXECUTED` |
| Z01 | Mellin identity, contour shift, and both residues | 2114--2134 | `UNEXECUTED` |
| Z02 | weighted Dirichlet-series sum tail beyond (Y\log^2Y) | 2140--2143 | `UNEXECUTED` |
| Z03 | integral tail, (X)-versus-(T) hypothesis, uniform (q,T) scope, and (T=1) endpoint | 2140, 2169, 2411--2413 | `EXPECTED_OPEN:Z03_TAIL_X_RANGE` |
| Z04 | principal-character residue and low-height-zero contribution after primitive restriction | 2134--2138 | `UNEXECUTED_WITH_WATCH` |
| Z05 | induced-character Euler factors and zero-set equality in (sigma>1/2) for primitive-to-all transfer | 2109, 2136--2138 | `EXPECTED_OPEN:Z05_PRIMITIVE_EULER_FACTORS` |
| Z06 | unique conductor partition, multiplicity/divisor loss, and (q_1)-sensitive termwise domination | 2109, 2148--2152 | `EXPECTED_OPEN:Z06_CONDUCTOR_SUM_Q1` |
| Z07 | saturated well-spacing selection and local zero-count input | 2154--2158 | `UNEXECUTED` |
| Z08 | class-II maximizers, shifted-ordinate separation, fourth moment, and (Y=(qT)^{1/2}) | 2160--2173 | `UNEXECUTED_WITH_WATCH` |
| Z09 | class-I dyadic selection, coefficient normalization, representative loss, and length range | 2176--2197 | `UNEXECUTED` |
| Z10 | existence of bounded (k), powered coefficient control, and complete length-case coverage | 2199--2258 | `UNEXECUTED_WITH_WATCH` |
| F01 | outer range (sigma\leq0.7) via the stated Ingham analogue | 141--149, 2109 | `UNEXECUTED` |
| F02 | outer range (sigma\geq0.8) via the stated Huxley analogue | 145--149, 2109 | `UNEXECUTED` |
| F03 | middle-range four-term zero-density lemma and hypotheses | 2261--2270 | `UNEXECUTED` |
| F04 | divisor Case 1 and complete interval coverage | 2276--2310 | `UNEXECUTED` |
| F05 | divisor Case 2 and complete interval coverage | 2276--2282, 2311--2325 | `UNEXECUTED` |
| F06 | divisor Case 3, feasibility, and complete interval coverage | 2276--2282, 2326--2336 | `UNEXECUTED` |
| F07 | divisor Case 4 and comparison with the desired terms | 2276--2282, 2337--2345 | `UNEXECUTED` |
| F08 | definition of (T)-smooth, divisor-chain existence, endpoints, and coverage | 182--185, 2266--2269, 2346--2350, 2410 | `EXPECTED_OPEN:F08_T_SMOOTH_UNDEFINED` |
| F09 | all four coefficient crossings with Ingham, including the quadratic/radical branch | 2357--2410 | `UNEXECUTED` |
| F10 | (q_1=q) reductions, exact inequalities, uniform (7/3), and worst-(T) scope | 178--187, 2371--2413 | `UNEXECUTED` |

## Expected blockers and gate rule

The preregistered expected blockers are `S06_EXTERNAL_INPUTS`,
`Z03_TAIL_X_RANGE`, the primitive-to-all group
`Z05_PRIMITIVE_EULER_FACTORS` plus `Z06_CONDUCTOR_SUM_Q1`, and
`F08_T_SMOOTH_UNDEFINED`.

`OBSERVED` source-audit rationale, not a theorem verdict:

- Z03: line 2140 truncates the integral as (T\to\infty) when (X) is
  polynomially bounded in (T), while line 2169 takes (X=(qT)^\epsilon)
  and the stated result is uniform in unrestricted (q,T); line 2412 calls
  (T=1) the worst case.
- Z05/Z06: line 2109 says nonprimitive characters are recovered by summing
  over factors of (q), but the Euler-factor zero comparison, conductor
  partition, divisor loss, and preservation of the (q_1)-sensitive terms
  are not supplied there.
- F08: “(q) is (T)-smooth” is used but not defined in the complete pinned
  TeX, so the divisor-chain claim and endpoints cannot yet be checked.
- S06: the package does not yet close the cited Iwaniec--Kowalski mean-value
  theorem, Huxley 1975, Montgomery Chapters 10/12, Davenport Chapter 16,
  Heath--Brown, the cited Guth--Maynard lemmas, or every other dependency
  actually reached by the 46 rows.

The eventual adjudicator must return `OPEN_ANALYTIC_INPUT` if any mandatory
row is open, any expected blocker remains, an external hypothesis is unread,
the two routes disagree on a label/subcheck, or a source locator fails. `PASS`
requires all 46 rows and both L12 subchecks to close by both independent
routes. No failed or open row may be omitted from the reconciliation.

## Independent routes

Route A is a literal theorem-chain reconstruction. It follows the TeX in
source order, expands every cited hypothesis, preserves the primitive/all
distinction, and derives each displayed exponent using exact rational and
exact radical algebra.

Route B is independent exponent-polytope/conductor reconstruction. It starts
from the frozen ((\alpha,\tau,\lambda,\beta)) coordinates, clears
denominators, checks signs by exact integer/rational arithmetic, and audits
conductor transfer prime by prime. It may read the frozen source and this
preregistration, but must not import Route A code, artifacts, intermediate
values, labels inferred from Route A, or repaired formulas.

Reconciliation compares canonical IDs, L12 subcheck labels, hypotheses,
locators, formulas, valid regions, blocker labels, and final disposition—not
merely an unlabeled list of exponents.

## Runtime, resources, and replay

Historical sealing and each future reconstruction route require
non-optimized CPython 3.12.3, wall time strictly below 60 seconds, and peak
RSS strictly below 262144 KiB (256 MiB). They use no floating-point values,
RNG, or network access. A cap breach, optimized mode, missing source, byte
mismatch, self mutation, source mutation, or attempted overwrite fails
closed. No unregistered method substitution is allowed after a cap failure.

From the project directory:

```sh
python3 proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py --check
python3 -m unittest tests/test_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py -v
```

`--write` is one-shot and refuses to replace the sealed JSON artifact.
