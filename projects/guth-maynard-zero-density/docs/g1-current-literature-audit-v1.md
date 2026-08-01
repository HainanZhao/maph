# G1/P2 current literature audit v1

## Claim boundary

`OBSERVED`: This is a bounded source-provenance and overlap audit of exactly
Larry Guth, arXiv:2503.07410v1, and Bin Chen, Vishal Gupta, and Yung Chi Li,
arXiv:2507.08296v2. It proves no result in either preprint, makes no global
novelty claim, and does not select a G1/P2 route.

The exact PDFs, source archives, captured arXiv records, extracted canonical
TeX files, page-text anchors, hashes, and replay instructions are frozen in
[g1-current-literature-audit-v1.json](../artifacts/g1-current-literature-audit-v1.json).
The audit is intentionally separate from the frozen G1 experiment and does not
change `PLAN.md`.

## Guth v1: usable map and contained limits

`OBSERVED`: Guth's 49-page v1 is a survey, not a new zero-density theorem.
Its pinned arXiv record identifies Larry Guth as sole author, shows submission
on 10 March 2025, and contains no journal-reference field.

| Topic | Exact locator | Bounded conclusion |
|---|---|---|
| Numerical evidence | TeX 526--552; PDF p. 12 | Guth says there is no meaningful numerical evidence for the main large-value conjectures and says they are not checkable even at (N=200). This requires the G1 finite screen to remain `OBSERVED`/`RECOGNIZED`; it is not a ban on a preregistered finite screen. |
| Cubic and higher tensors | TeX 864--962; PDF pp. 20--22 | The survey says the Guth--Maynard paper studies (S_{M_{m Dir},3}), motivates (rge3), and describes tensor-complexity barriers. It gives no quartic no-go theorem. A commented-out TeX-only sentence about an unsuccessful (r=4) flattening is excluded from this source's published-PDF evidence. |
| Cyclic differences | TeX 1026--1137; PDF pp. 25--27 | It defines (D^rPhi), says (rge3) needs cancellation, and gives a qualitative (r=3) smooth-plus-curves account. This is not a quantitative (r=4) theorem. |
| Energy | TeX 988--1019; PDF pp. 23--24 | **Contained correction:** v1 defines energy with (t_1+t_2=t_3-t_4), then states the standard fourth-Fourier-moment identity. Those displayed conventions are inconsistent. This survey is not an authority for the project energy convention; the separately pinned published Guth--Maynard source is. |
| Complexity | TeX 1284--1484; PDF pp. 34--36 | The relevant no-go language is conjectural or for random/planted models. It does not rule out the present P2A/P2B architecture. |
| Kakeya | TeX 1516--1608; PDF pp. 37--40 | The Bourgain--Kakeya discussion is a conditional barrier; it expressly says a black-box form does not currently improve the known Dirichlet-polynomial bounds. It is not a saturation theorem. |

## Chen--Gupta--Li v2: exact prior-work overlap

`OBSERVED`: The pinned arXiv v2 record names Bin Chen, Vishal Gupta, and Yung
Chi Li; it was last revised 27 July 2026 and has no journal-reference field.
It remains a preprint in this audit. Its stated (7/3) Dirichlet-(L)
exponent has not been independently theorem-checked here.

The exact overlap is narrower than a generic “energy method” label:

- TeX 275--373 and 524--660 use the refined **cubic** trace; TeX 1979--2072
  closes an (S_3) bound.
- TeX 1129--1160 proves an affine-transformation estimate with a **GCD
  twist**; TeX 1688--1765 defines energy on character-time pairs and applies
  it in the (S_3) chain. This is prior work for a character-twisted cubic
  (S_3)+affine+energy mechanism, not a scale-sensitive un-twisted G1 energy
  theorem.
- TeX 2107--2140 begins a Dirichlet-(L) zero-detection application. It
  makes generic reuse of that template non-novel, but this audit does not
  compare it to the project's zeta six-factor short-interval decomposition.
- A literal full-TeX search has no occurrences of `quartic`, `cyclic
  difference`, or `Kakeya`. That is a bounded textual absence, never a claim
  that no related higher-trace method exists.

Thus P6 must concede this preprint and its stated result. Any future P2B or
P2C claim must explicitly differentiate its hypotheses and mechanism from the
character-twisted (S_3) work. The audit makes no route selection.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_g1_current_literature_v1.py --check
python3 -m unittest tests/test_g1_current_literature_audit_v1.py -v
```

`OBSERVED`: Replay checks the pinned bytes, canonical TeX extraction, page-text
anchors, locators, source-content conditions, and the frozen audit artifact.
It does not validate the analytical proofs in either preprint.
