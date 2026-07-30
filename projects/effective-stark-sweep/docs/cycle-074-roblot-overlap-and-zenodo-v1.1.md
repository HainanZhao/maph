# Cycle 074 — Roblot overlap audit and corrected Zenodo v1.1

Recorded 30 July 2026 UTC.

## Prior-work correction

Roblot, *Index formulae for Stark units and their solutions*,
Pacific J. Math. 266 (2013), Theorems 6.1 and 7.1, proves
unconditional weak quartic and sextic Stark results.  The logarithmic
identity is only up to complex absolute values and does not identify
the individual positive Artin-labelled components of the one-place
Shintani packet.

The manuscript now makes no first-result claim for weak quartic or
sextic Stark units.  Its distinction is the exact componentwise
packet: explicit ray-field polynomial, positivity, root isolation,
and Artin labels.  The remaining survey-bounded historical statement
concerns support order ten only.

## Exact sextic-hypothesis audit

`scripts/audit_roblot_sextic_overlap.gp` checks Roblot's (A1)--(A3),
the class number of the cyclic sextic ray field, and wild ramification
above 3.

| case | (A1)--(A3) | h_H | wild above 3 | Roblot Thm. 7.1 |
|---|---:|---:|---:|---:|
| RQ-000190 | pass | 1 | no | applies |
| RQ-000419 | pass | 1 | no | applies |
| RQ-000021 | pass | 1 | no | applies |
| RQ-002057 | pass | 1 | yes, e(H/K)=6 | does not apply |
| RQ-002955 | pass | 1 | no | applies |

The exact record is
`artifacts/roblot-sextic-overlap-audit-v1.json`.

## Publication

- corrected version: 1.1;
- DOI: `10.5281/zenodo.21707548`;
- concept DOI: `10.5281/zenodo.21703305`;
- companion: `effective-stark-results-companion-v11.tar.gz`;
- companion SHA-256:
  `c91e0bd2432f9c5de70a8c760553c0e012c9a304af7e00fbb59b62faab6401fa`;
- default preview: `effective-stark-results.pdf`;
- previous v1.0 DOI `10.5281/zenodo.21703306` remains preserved in
  the version chain.

The main PDF/TeX, supplement PDF/TeX, and companion archive are
top-level files.  Local MD5 values match the published record.

## Gates

- deterministic PDF rebuild: pass;
- full manuscript audit: pass;
- Engine A/B/C plus structural verifier: pass;
- regression suite: 125/125 pass;
- citation audit: no missing or uncited entries;
- manual equation tags: zero.
