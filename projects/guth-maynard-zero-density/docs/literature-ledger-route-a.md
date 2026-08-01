# Route A literature ledger: Guth--Maynard baseline

## Claim boundary

`OBSERVED`: This ledger freezes primary-source locations and hypotheses for
Cycle 1 / P0. It proves no new large-values, zero-density, or short-interval
result, and it does not certify that any future candidate meets the hypotheses
below.

`OBSERVED`: The source hashes, retrieval URLs, tool commands, and page-count
evidence are pinned in
[`guth-maynard-source-metadata-v1.json`](../artifacts/guth-maynard-source-metadata-v1.json).

## Editions and pagination policy

`PROVED`: The published article is Larry Guth and James Maynard, *New large
value estimates for Dirichlet polynomials*, *Annals of Mathematics* **203**(2)
(2026), 623--675, DOI
[10.4007/annals.2026.203.2.6](https://doi.org/10.4007/annals.2026.203.2.6).
The Annals landing page supplies the bibliographic range and publication
metadata.

`OBSERVED`: The locally frozen arXiv v2 PDF is dated 7 April 2026 and has 52
PDF pages; the Oxford repository's accepted manuscript has 52 PDF pages. Their
rendered text differs in layout-level details and the arXiv header, so their
PDF bytes are not identical. The Annals article range contains 53 numbered
print pages (623--675 inclusive), and no publisher-layout PDF was retrievable
in this run.

**Rule.** Every exact page in this ledger is therefore an **arXiv v2 PDF page**
(`PDF p.`), independently reproducible from the frozen PDF. `Annals print
pp. 623--675` is a bibliographic citation only; a putative conversion such as
`623 + PDF-page - 1` is an **unverified locator**, not an exact printed-page
claim. This distinction is deliberate: downstream writing must cite theorem,
equation, section, and PDF page unless it independently obtains the publisher
PDF.

## Dependency map

```text
Theorem 1.1 (large values)
        |
        +--> Theorem 1.2: 15(1-sigma)/(3+5sigma)
        |       + Ingham (1.2), sigma <= 7/10
        |       `--> (1.4): 30/13 envelope
        |                + zero-free region / stronger near-1 input
        |                +--> Corollary 1.3: uniform intervals
        |                `--> Corollary 1.4: almost-all intervals
        |
        +--> cubic trace; stated r >= 4 limitation
        `--> Proposition 11.1; stated leading-energy-term limitation

Remark after Corollary 1.4: separate six-factor direct route.
```

`PROVED`: This is the paper's stated proof architecture: Theorem 1.2 is proved
in Section 13.1 from zero detection and the large-values theorem; the two
corollaries are proved in Section 13.2 from (1.4), with additional cited
near-​1/zero-free-region inputs. The final arrow is a remark about a possible
different direct treatment, not a theorem used in Corollaries 1.3--1.4.

## Exact source map and checked hypotheses

| ID | Exact source locator | Statement / hypotheses checked from the primary text | Status and permitted use |
|---|---|---|---|
| GM-T1.2 | Theorem 1.2, `PDF p. 2`; source label `thrm:ZeroDensity`; proof §13.1, `PDF pp. 49--50` | (N(\sigma,T)) counts zeros \(\rho\) of \(\zeta(s)\) with \(\Re\rho\ge\sigma\) and \(|\Im\rho|\le T\). The stated bound is \(N(\sigma,T)\le T^{15(1-\sigma)/(3+5\sigma)+o(1)}\). The statement itself gives no additional displayed range for \(\sigma,T\); Section 13.1 reduces the new proof to \(7/10\le\sigma\le8/10\), invoking Ingham below and Huxley above. | `PROVED` as a published theorem statement. Use only with this zero-count convention and the source's asymptotic \(o(1)\) convention. |
| GM-I | Equation (1.2), `PDF p. 2`; Section 13.1, `PDF p. 49` | The paper attributes to Ingham \(N(\sigma,T)\le T^{3(1-\sigma)/(2-\sigma)+o(1)}\). It explicitly says this supplies Theorem 1.2 for \(\sigma\le7/10\). | `PROVED` as the primary paper's quoted published input. Before a proof replay, independently inspect Ingham or the cited modern formulation for its original hypotheses. |
| GM-X | Text immediately after Theorem 1.2 and equation (1.4), `PDF p. 2` | Combining Theorem 1.2 with Ingham for \(\sigma\le7/10\) yields \(N(\sigma,T)\le T^{(30/13)(1-\sigma)+o(1)}\). Exact algebra: \(3/(2-\sigma)=15/(3+5\sigma)\) iff \(\sigma=7/10\); both values equal \(30/13\). Moreover \(3/(2-\sigma)\le30/13\) for \(\sigma\le7/10\), and \(15/(3+5\sigma)\le30/13\) for \(\sigma\ge7/10\). | `PROVED` for the algebra and the stated combination. This is a density-envelope comparison, not a claim that Theorem 1.2's coefficient is constant. |
| GM-C1.3 | Corollary 1.3, `PDF pp. 2--3`; proof §13.2, `PDF pp. 50--51` | For \(y\in[x^{17/30+\epsilon},x^{0.99}]\), \(\pi(x+y)-\pi(x)=y/\log x+O_\epsilon(y\exp(-\sqrt[4]{\log x}))\). The proof sets \(T=xy^{-1}\exp(2\sqrt[4]{\log x})\), uses (1.4) together with a cited stronger bound near \(\sigma=1\), and requires \(T<x^{13/30-\epsilon/2}\). | `PROVED` as the published corollary, with all displayed interval and error hypotheses retained. A downstream \(\theta\)-claim must replay the additional near-1 input and the zero-free region; it cannot follow from the bare (30/13) algebra alone. |
| GM-C1.4 | Corollary 1.4, `PDF p. 3`; proof §13.2, `PDF pp. 51--52` | For \(y\in[X^{2/15+\epsilon},X^{0.99}]\), the same asymptotic holds for all but \(O(X\exp(-\sqrt[4]{\log x}))\) choices of \(x\in[X,2X]\cap\mathbb N\), exactly as printed. The proof chooses \(\delta=X^{-13/15+\epsilon/2}\) and (T=\delta^{-1}\exp(4\sqrt[4]{\log X})\). | `PROVED` as the published corollary. The source's exceptional-set display retains `log x`; this ledger preserves it rather than silently normalizing it to `log X`. |
| GM-R4 | Introduction, trace discussion, `PDF p. 11`; source around lines 535--559 | For the matrix \(M_W\), the authors say a sharp high-​(r) trace bound would imply their Conjecture 1.5, but: “we do not know how to obtain good bounds when \(r\ge4\), so we work with \(r=3\).” They also state that even the displayed sharp cubic-trace bound alone only gives \(|W|\lessapprox N^{3-3\sigma}\), worse than prior bounds. | `PROVED` as an accurately located statement of the authors' methodological limitation. It is **not** a no-go theorem for all quartic traces, all higher-moment arguments, or all extensions of the method. |
| GM-P11.1 | Proposition 11.1, equation (11.1), `PDF p. 38`; explanatory text `PDF pp. 38--39`; notation §1, `PDF p. 5` | If \(D(t)=\sum_{n\sim N}b_n n^{it}\), \(|b_n|\le1\), \(W\) is 1-separated in an interval of length \(T\), \(|D(t)|\ge N^\sigma\) on \(W\), and \(T^{3/4}\le N\le T\), then \[E(W)\lessapprox |W|N^{4-4\sigma}+|W|^{21/8}T^{1/4}N^{1-2\sigma}+|W|^3N^{1-2\sigma}.\] Here \(A\lessapprox B\) means \(|A|\le C(\epsilon)T^\epsilon B\) for every \(\epsilon>0\) and all large \(T\). Under the paper's comparison \(|W|\approx TN^{1-2\sigma}\), it rewrites the terms as \((N/T)^2|W|^3+(|W|^{5/8}T^{-6/8})|W|^3+|W|^4/T\). | `PROVED` as Proposition 11.1 and its stated hypotheses. The authors say the **first** rewritten term “will be the most important” and “generally sets the limitations on our bounds”; this is a methodological assessment, not a sharpness theorem. |
| GM-6F | Final unnumbered Remark after §13.2, `PDF p. 52`; source lines 2475--2477 | By a prime decomposition (e.g. Heath--Brown identity) and Mellin inversion, the authors state that the critical situation for both corollaries is a product of six Dirichlet polynomials, each of size about \(x^{1/6}\). They state that, as in [HB4], a sieve treatment of six almost equal primes *could* give ranges \(y\ge x^{17/30-\epsilon}\) and \(y\ge X^{2/15-\epsilon}\), with error roughly \(O(\epsilon^4y/\log x)\). | `CONJECTURED` / prospective route exactly as worded by the authors. It is not an established strengthening of either corollary and must never be entered as a current frontier theorem without a separate proof. |

## Route-A implications and constraints

`PROVED`: The proof of Theorem 1.2 itself explicitly handles the middle range
(7/10\le\sigma\le8/10), and it describes the global (30/13) envelope as a
combination with Ingham below (7/10). Thus the frozen Crossover target is
exactly (sigma=7/10), rather than an unspecified “density exponent.”

`PROVED`: Proposition 11.1's condition (T^{3/4}\le N\le T) and coefficient
condition (|b_n|\le1) are mandatory if the project later applies that
proposition; the discussion of its leading term may guide a research path but
does not license treating the term as universally sharp.

`CONJECTURED`: The quoted (r\ge4) and Proposition 11.1 comments identify
specific places to test for saturation. They do not prove that the
Guth--Maynard architecture saturates at (30/13).

## Evidence replay

From the repository root:

```sh
sha256sum projects/guth-maynard-zero-density/artifacts/sources/arxiv-2405.20552v2.pdf
mutool info projects/guth-maynard-zero-density/artifacts/sources/arxiv-2405.20552v2.pdf
mutool draw -F txt \
  projects/guth-maynard-zero-density/artifacts/sources/arxiv-2405.20552v2.pdf 1-52 \
  | rg -n 'Theorem 1.2|Corollary 1.3|Corollary 1.4|when r ≥ 4|Proposition 11.1|six Dirichlet polynomials'
```

`OBSERVED`: The command is a source-location replay, not an independent
mathematical proof of Guth--Maynard's theorems.
