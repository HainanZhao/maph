# Classical zero-density inputs: source ledger

## Claim boundary

`OBSERVED`: This Cycle-1 ledger freezes the sources used for the Ingham and
Huxley inputs in Guth--Maynard Section 13.1. It does not reprove either
zero-density theorem, resolve the historical Ingham pagination conflict, or
establish a new range of either estimate.

`OBSERVED`: Retrieval URLs, hashes, scan-to-print page mapping, failed original
Ingham retrieval attempts, and one modern restatement are pinned in
[`classical-zero-density-source-metadata-v1.json`](../artifacts/classical-zero-density-source-metadata-v1.json).

## Source availability and containment

`PROVED`: Huxley's original published article is locally frozen as the
Göttingen Digitization Center scan of *Inventiones mathematicae* 15. In the
356-page volume PDF, PDF pp. 173--179 are Huxley's article and visibly carry
the printed pages 164--170. The exact volume-file SHA-256 is recorded in the
metadata artifact.

`OBSERVED`: Ingham's original DOI is
[10.1093/qmath/os-11.1.201](https://doi.org/10.1093/qmath/os-11.1.201), but
the publisher PDF returned HTTP 403 to repeated direct retrieval attempts in
this run. It is therefore **not** stored locally and no direct-page claim from
the Ingham paper is made below.

`OBSERVED`: There is a real bibliographic discrepancy requiring containment:
the OUP metadata exposed by its landing/search page reports *Quarterly Journal
of Mathematics* old series 11(1), 201--202, whereas Huxley's printed reference
3, Guth--Maynard's bibliography, and multiple later bibliographies report 11
(1940), 291--292. The DOI agrees; the page discrepancy is unresolved without
an accessible original scan. Do not use either page pair as an exact
source-page locator pending resolution.

`OBSERVED`: Chourasiya--Simonič, arXiv:2507.15184v2, is frozen as a readable
modern restatement of Ingham's result. It remains a **preprint** and is not
upgraded to primary-source authority.

## Exact input map

| ID | Primary or fallback source locator | Definition and hypotheses checked | Result used by Guth--Maynard | Status and limits |
|---|---|---|---|---|
| HUX-D | Huxley, printed p. 164 = frozen GDZ-volume `PDF p. 173`, (1.4) | \(N(\alpha,T)\) is the number of zeros \(\rho=\beta+i\gamma\) of \(\zeta(s)\) in \(\alpha\le\beta\le1\), \(-T\le\gamma\le T\). | This convention agrees with the two-sided height convention adopted by Guth--Maynard Theorem 1.2. | `PROVED` by direct inspection of the published source. Multiplicity is not made explicit in the displayed definition; do not infer a multiplicity convention from this row alone. |
| ING-HUX | Huxley, printed p. 164 = frozen `PDF p. 173`, (1.8) | Huxley states that the range \(1/2\le\alpha\le3/4\) is supplied by Ingham's theorem, writing \[N(\alpha,T)\ll T^{3(1-\alpha)/(2-\alpha)}(\log T)^5.\] | Hence \(N(\sigma,T)\le T^{3(1-\sigma)/(2-\sigma)+o(1)}\) in the range needed for the Guth--Maynard crossover, namely \(1/2\le\sigma\le7/10\). | `PROVED` as a contemporaneous published restatement in Huxley's original paper; `OBSERVED` as to Ingham's original wording because that source was inaccessible. |
| ING-MOD | Chourasiya--Simonič, abstract and introduction, `PDF p. 1`; exact v2 source frozen | Their abstract states that Ingham proved the same bound with \((\log T)^5\), for nontrivial zeros with \(\Re\rho\ge\sigma\ge1/2\) and \(0<\Im\rho\le T\), counted with multiplicity. | It corroborates the exponent, explicit log factor, lower \(\sigma\) boundary, and one-sided convention. By zero symmetry, its one-sided count is compatible up to a factor of two with Huxley's two-sided count. | `OBSERVED`: modern preprint restatement, not an independent proof or a replacement for Ingham. The factor-two convention conversion affects only constants, not the density exponent. |
| HUX-1.9 | Huxley, printed p. 164 = frozen `PDF p. 173`, (1.9); proof announced printed p. 165 = `PDF p. 174` | With the above two-sided convention and \(\ell=\log T\), Huxley states \[N(\alpha,T)\ll T^{3(1-\alpha)/(3\alpha-1)}\ell^{44}\] uniformly for \(3/4\le\alpha\le1\), and immediately says “We prove (1.9) below.” | Hence the Guth--Maynard quoted form \(N(\sigma,T)\le T^{3(1-\sigma)/(3\sigma-1)+o(1)}\) is licensed on \(3/4\le\sigma\le1\). | `PROVED` by direct inspection of the published source. The printed ℓ-power is part of the theorem and must not be silently omitted in a finite-​(T) calculation; it is absorbed only in the stated asymptotic (o(1)) form. |
| GM-13.1 | Guth--Maynard Section 13.1, arXiv v2 `PDF p. 49` | The section states that Ingham covers \(\sigma\le7/10\), Huxley covers \(\sigma\ge8/10\), and the new work need only treat \([7/10,8/10]\). | This correctly uses only the ranges established above: \(7/10<3/4\) lies in Ingham's stated range and \(8/10>3/4\) lies in Huxley's stated range. | `PROVED` as a compatibility check of the exact intervals; it does not independently rederive the Section 13.1 proof. |

## Exact exponent checks

`PROVED`: At \(\sigma=7/10\), Ingham's coefficient is

\[
\frac{3}{2-7/10}=\frac{30}{13}.
\]

`PROVED`: At \(\sigma=8/10\), Guth--Maynard's coefficient and Huxley's
coefficient coincide:

\[
\frac{15}{3+5(8/10)}=\frac{3}{3(8/10)-1}=\frac{15}{7}.
\]

`PROVED`: The formula \(3/(3\sigma-1)\) is decreasing for
\(\sigma>1/3\), so Huxley is no weaker than the Guth--Maynard coefficient
above the meeting point \(4/5\). The formula \(3/(2-\sigma)\) is increasing,
so its coefficient is at most \(30/13\) for \(1/2\le\sigma\le7/10\).

## Replay

From the repository root:

```sh
sha256sum projects/guth-maynard-zero-density/artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf
mutool info projects/guth-maynard-zero-density/artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf
mutool draw -r 150 -o /tmp/huxley-%d.png \
  projects/guth-maynard-zero-density/artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf 173-179
sha256sum projects/guth-maynard-zero-density/artifacts/sources/chourasiya-simonic-2025-explicit-ingham.pdf
```

`OBSERVED`: Huxley's scan is image-only in the downloaded volume, so the
published formula/page checks above were made by rendering and visual inspection;
the replay command regenerates exactly the inspected pages. No OCR result is
promoted as source text.
