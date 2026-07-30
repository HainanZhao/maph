# Cycle 073 — Fourier convention, layout, and chronology repair

Recorded: 2026-07-30 UTC

## Engine-C convention correction

The declared convention is
\[
L(s,\chi)=\sum_A\chi(A)\zeta(s,A),\qquad
\zeta(s,A)=|G|^{-1}\sum_\chi\chi(A)^{-1}L(s,\chi).
\]
With \(\psi(\sigma)=i\),
\(\zeta'_S(0,\sigma^r)=-(2/e)\ell_{\sigma^r}\), and
\((\ell_{\sigma^2},\ell_{\sigma^3})=(-\ell_1,-\ell_\sigma)\),
the exact transform is
\[
L'_S(0,\psi)=-\frac4e(\ell_1+i\ell_\sigma).
\]
Consequently
\[
Y_{\bar s^r}=N_{E/E^+}(\sigma^r u)^{-1}.
\]

The earlier minus sign and \(\sigma^{-r}\) exponent were inconsistent
with the convention paragraph.  The exact bridge implementation was
already using positive powers: it applies `normal_sigma` exactly
`label_index - 1` times before taking the CM norm.  Therefore:

- the Artin-label formula is corrected;
- packet polynomials and unlabeled root sets are unchanged;
- no case tag changes;
- the earlier theory and tranche normalization prose remain preserved
  as superseded records.

Evidence:

- `data/engine-c-general-e-theory-v4.json`;
- `scripts/audit_engine_c_fourier_convention.py`;
- `artifacts/engine-c-fourier-convention-correction-v1.json`.

## Shintani hypothesis exposition

The paper now restates the operational content of (0-3), (0-6), and
(0-9): the two unit-congruence exclusions and the required one-place
splitting/index-two condition.  Source numbering remains for
traceability but no longer substitutes for a definition.

## Layout separation

- Both main theorem tables use `\footnotesize`.
- Short modulus labels replace HNF matrices in the theorem tables.
- A normal-sized appendix gives every exact HNF matrix.
- The complete record map is Supplementary Table S1.
- The complete Artin interval replay is Supplementary Table S2.
- Only the representative RQ-000190 interval row remains in the main
  paper.
- Engine-A queue statistics are supplement-only; the theorem remark
  retains only the mathematical \(E_\chi=0\) consequence.

The main PDF has 17 pages and the supplement has 2.  Both build
deterministically without LaTeX reference or box warnings.

## Prior-work chronology

The historical discussion now cites:

- *Twisted-Convolution Identities in Dimensions Four and Five from
  Shintani Ray Units*, DOI `10.5281/zenodo.21680223`;
- *Twisted-Convolution Identities in Dimensions Seven and Eight:
  Shintani Height Rigidity and CM Descent*, DOI
  `10.5281/zenodo.21681700`.

The prior \(\mathbb Q(\sqrt3),(5)\infty_2\) support-order-eight packet
with safe exponent \(5760\) is identified as another specialization
of the present transfer and rigidity framework.  RQ-000021 is
described as an effective reidentification of a dimension-seven
arithmetic input.  No new order-six priority claim remains.  The
bounded knowledge statement is retained only for order ten.

## Frozen state

- full freeze: `artifacts/results-paper-full-freeze-v6.json`;
- local companion: `dist/effective-stark-results-companion-v9.tar.gz`;
- companion SHA-256:
  `0168a3882afb3e0eda89e597088cf6d8b297257b213fef5ee2fce3bc854bef4a`;
- public DOI: none;
- publication action: none.
