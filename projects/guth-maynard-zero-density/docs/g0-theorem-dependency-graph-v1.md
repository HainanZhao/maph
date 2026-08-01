# G0 theorem dependency and hypothesis graph, v1

## Claim boundary

`OBSERVED`: This graph records the dependencies asserted in the frozen
Guth--Maynard arXiv v2 text. It is a source-audit artifact, not an independent
reconstruction of Theorems 1.1--1.2 or Corollaries 1.3--1.4.

`OBSERVED`: The machine-readable edge list and all locators are frozen in
[`g0-theorem-dependency-graph-v1.json`](../artifacts/g0-theorem-dependency-graph-v1.json).
All PDF page references below are arXiv v2 PDF pages; all TeX lines refer to
`artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex`, whose parent
source-tar and PDF hashes are recorded in the existing source metadata ledger.

## Graph

```text
GM Theorem 1.1 ----> zero-detection large-values branch ----\
                                                           \
MP Lemma 24 -------> Type-II control -----------------------> GM Theorem 1.2
                                                           /
mean-value theorem -> complementary large-values branch --/
Huxley ----------------------------------------------------/

Ingham + GM Theorem 1.2 ----> (1.4), 30/13 envelope
                                          |
             +----------------------------+---------------------------+
             |                                                        |
explicit formula; near-1 density; VK zero-free                 same three inputs
             |                                                        |
        Corollary 1.3                                           Corollary 1.4
        uniform intervals                                      almost-all intervals
```

`PROVED`: This matches the order of the published exposition: Theorem 1.1 is
used in the Type-I branch of Section 13.1; MP Lemma 24 controls Type II; Ingham
and Huxley remove the outer σ-ranges; and Section 13.2 uses (1.4), an explicit
formula, a near-​1 density input, and a zero-free region for both corollaries.

## Nodes, locators, and hypotheses

| Node | Frozen location | Checked statement or role | Audit state |
|---|---|---|---|
| GM-T1.1 | Theorem 1.1, `PDF p. 1`, TeX lines 68--81 | For 1-separated `t_r ∈ [0,T]`, `|b_n| ≤ 1`, and values at least `V` of a polynomial supported on `N ≤ n ≤ 2N`, the theorem gives `R ≤ T^{o(1)}(N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4})`. | `PROVED`: published theorem and its displayed hypotheses are frozen. Its internal proof is not rederived here. |
| GM-ZD-TYPE-SPLIT | §13.1, `PDF p. 48`, TeX lines 2305--2318 | A zero with `β ≥ σ`, `γ ∈ [T,2T]` is Type I if a dyadic `N ∈ [T^{1/100}, T^{1/2}(log T)^2]` makes the specified detector large; otherwise it is Type II. | `PROVED`: source definition checked. Its adequacy depends on MP Lemma 24. |
| EXT-MP-L24 | cited at TeX line 2317, `PDF p. 48` | The paper claims Type-II count `≤ T^{2-2σ}(log T)^{O(1)}`. | `OBSERVED`: external result is **unread**. Exact Type-II definition, σ/T range, multiplicity convention, and uniformity remain unchecked. |
| GM-ZD-SMOOTH-SEPARATE | §13.1, `PDF p. 49`, TeX lines 2319--2337 | A β-dependent smooth function ψ, Fourier inversion, rapid decay, and a local `O(log T)` zero count produce a 1-separated `W` of comparable dyadic size, with `|D-tilde(t)| ≳ N^σ`. | `OBSERVED`: an internal source step, not yet independently checked. The ψ construction, Fourier normalization/truncation, local zero count, and interval translation are indirect hypotheses. |
| GM-ZD-APPLY-T1.1 | §13.1, `PDF pp. 49--50`, TeX lines 2338--2364 | With `N^k` in the stated interval and `α = 15(1-σ)/((3+5σ)(18/5-4σ))`, apply Theorem 1.1 to `D-tilde^k` if `N^k ≤ T^α`; use a mean-value bound otherwise. | `OBSERVED`: exponents are explicitly displayed; application hypotheses are not yet fully checked. In particular, normalize the detector and convolution coefficients to the theorem's ℓ-infinity bound, split `[N^k,(2N)^k]` dyadically, transfer the threshold, and verify the integer-`k` existence argument. |
| EXT-MVT | cited only as “usual Mean Value Theorem,” TeX line 2353, `PDF p. 50` | Supplies the two terms in the `N^k > T^α` branch. | `OBSERVED`: external theorem and its hypotheses are unread. |
| INGHAM | GM (1.2), `PDF p. 2`, TeX lines 96--101; classical ledger `ING-HUX` | `N(σ,T) ≪ T^{3(1-σ)/(2-σ)}(log T)^5` for the published Huxley-restated range `1/2 ≤ σ ≤ 3/4`. | `PROVED` for the reachable Huxley restatement; original Ingham text remains inaccessible, as contained in the classical ledger. |
| HUXLEY | GM (1.3), `PDF p. 2`, TeX lines 103--110; classical ledger `HUX-1.9` | `N(σ,T) ≪ T^{3(1-σ)/(3σ-1)}(log T)^{44}`, uniformly `3/4 ≤ σ ≤ 1`. | `PROVED`: direct original-source check. |
| GM-T1.2 | Theorem 1.2, `PDF p. 2`, TeX lines 118--125; proof begins `PDF p. 48` | `N(σ,T) ≤ T^{15(1-σ)/(3+5σ)+o(1)}`, with the source's two-sided count. Section 13.1 treats `[7/10,8/10]`. | `PROVED`: published conclusion and source convention frozen. |
| GM-ENV-30-13 | GM (1.4), `PDF p. 2`, TeX lines 127--132 | Combine GM-T1.2 with Ingham below `7/10`; exact crossover coefficient is `30/13`. | `PROVED`: algebra and source-stated combination. |
| EXT-EXPLICIT-FORMULA | Davenport Ch. 17, cited at TeX lines 2407--2417, `PDF p. 50` | Truncated explicit formula with error `O(x(log x)^3/T)`. | `OBSERVED`: unread external input. Endpoint conventions, uniformity, prime-power treatment, and zero conventions remain unchecked. |
| EXT-NEAR-ONE-DENSITY | Jutila or Montgomery *Topics*, Theorem 12.1; TeX lines 2419--2423, `PDF p. 50` | Needed to strengthen (1.4) near σ=1 with only logarithmic loss. | `OBSERVED`: a disjunctive citation, so no single theorem/range/log factor is frozen. |
| EXT-VK-ZERO-FREE | Montgomery *Topics*, Cor. 11.4; TeX lines 2425--2432, `PDF p. 51` | Used in the stated Vinogradov--Korobov zero-free form before taking the σ-supremum. | `OBSERVED`: unread external input; the cutoff conversion used by GM is not yet checked. |
| GM-C1.3 | Cor. 1.3 `PDF pp. 2--3`, TeX lines 140--150; proof `PDF pp. 50--51`, TeX lines 2405--2432 | Uniform PNT for `x^{17/30+ε} ≤ y ≤ x^{0.99}`. | `PROVED`: published corollary. Full proof replay awaits all three preceding external inputs. |
| GM-C1.4 | Cor. 1.4 `PDF p. 3`, TeX lines 155--164; proof `PDF pp. 51--52`, TeX lines 2434--2473 | Almost-all PNT for `X^{2/15+ε} ≤ y ≤ X^{0.99}`. | `PROVED`: published corollary. Full proof replay awaits the same external inputs plus the displayed second-moment manipulations. |

## Blocker matrix

`PROVED`: None of the unread dependencies blocks **G0 arithmetic**: exact
comparison of published exponent functions, their crossover, or a rational
replay of the displayed σ- and (k)-inequalities can proceed using the
frozen theorem statements.

`OBSERVED`: The following do block a **full analytic reconstruction** of the
published downstream theorems: MP Lemma 24; the mean-value theorem branch; the
unexpanded smoothing/separation steps; the local zero-in-unit-strip estimate;
the explicit formula; a pinned near-​1 density theorem; and the stated
Vinogradov--Korobov zero-free input. The Ingham original-page issue blocks a
direct original-source audit but not use of its published Huxley restatement in
the G0 arithmetic branch.

`CONJECTURED`: An improvement to Theorem 1.1 can be propagated through the
displayed Type-I exponent algebra, but it should not be promoted to an improved
short-interval theorem until the full downstream external-input chain has been
replayed with its hypotheses checked.

## Replay

```sh
cd /root/projects/maph
rg -n 'thrm:LargeValues|thrm:ZeroDensity|Lemma 24|Type I zero|Type II zero|Mean Value Theorem|Chapter 17|Theorem 12.1|Corollary 11.4' \
  projects/guth-maynard-zero-density/artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex
jq . projects/guth-maynard-zero-density/artifacts/g0-theorem-dependency-graph-v1.json
```

`OBSERVED`: This replay locates the frozen dependency declarations; it does not
validate the external results.
