# SIC--Stark research cycle 151: queued obligations

Date: 2026-07-28

## Dimension sixteen: exact Shintani gate

The anticipated shortcut does not occur. Exact maximal-order and local
order-ray calculations give

\[
 \operatorname{Cl}_{(16)\infty_2}(\mathcal O_{\mathbb Q(\sqrt{221})})
 \simeq C_{16}\times C_4\times C_2,
\]

\[
 |\operatorname{Cl}_{(16)\infty_2}|=128,\qquad
 [H:H\cap\mathbb Q^{\mathrm{ab}}]=16.
\]

The group is a \(2\)-group, but it is not elementary abelian and
Shintani's quadratic-over-absolutely-abelian condition (0-9) requires
index \(2\), not merely a power of two. Thus:

\[
 \boxed{d=16\text{ fails the Shintani (0-9) gate.}}
\]

The base class group and units are unconditional:
`bnfcertify` returns \(1\). The exact computation is reproduced by
`scripts/screen_higher_dimension_theorem_coverage.py`.

## Dimension seven: conductor-two stratum

The queue item was already mathematically complete, and it has now been
rerun rather than assumed:

- canonical discriminant \(32\), order conductor \(2\);
- order-ray and maximal multiplier-ray orders both \(12\);
- Shintani index \(2\);
- all phase, ray-label, and height certificates pass;
- for each formal shift, trace one, idempotency, and all \(441\)
  rank-two minors are exact;
- the wide form class is unique under
  \(\mathrm{GL}_2(\mathbb Z)\).

The main theorem of Paper II explicitly states both
\(0,1\in\mathcal Z_t\) and equality of shift sets for forms of the same
discriminant. No scope correction is needed.

## Release packages

The deterministic archive test passes for both papers. The current
release candidates are:

| Archive | Files | SHA-256 |
|---|---:|---|
| `sic-stark-paper-I.tar.gz` | 52 | `228cd921a5051296c8a28f4a26bef97ddba25e6b5884a39022fb35700924b7d3` |
| `sic-stark-paper-II.tar.gz` | 101 | `292ca88e161201898463e20a1a3aa5fcde9d23422e724aee4490ac9fe62df7c1` |

The metadata files `CITATION.cff` and `.zenodo.json` are present.
No Zenodo access token is available in this workspace, so no external
deposit or DOI has been claimed. The packages are ready for the
author's authenticated upload.

## Correspondence

`docs/kopp-correspondence-draft.md` has been refreshed with the
dimension-six two-base lens-space identification, the precise boundary
failure, and the single arithmetic fusion-continuity question.

## Status

| Obligation | Status |
|---|---|
| \(d=16\) Shintani (0-9) audit | `VERIFIED: FAILS (index 16)` |
| Paper II \(d=7\), discriminant \(32\) | `VERIFIED: COMPLETE` |
| Companion archive regression | `VERIFIED` |
| Zenodo payload preparation | `COMPLETE` |
| Zenodo external deposit | `BLOCKED: no credentials` |
| Kopp correspondence draft | `COMPLETE` |
