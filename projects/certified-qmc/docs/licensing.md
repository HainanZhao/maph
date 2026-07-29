# Licensing and third-party data policy

Frozen: 2026-07-29

## Project artifacts

Certified-QMC engine code is released under Apache License 2.0.  The
patent grant and compatibility with the frozen QMCPy snapshot make it a
better fit than a bare MIT grant for a numerical engine intended for
reuse.  The complete text is in `LICENSE`.

Original merit tables, manifests, and project-authored data are released
under Creative Commons Attribution 4.0 International; the complete text
is in `LICENSE-DATA`.  This data license does not purport to relicense
third-party vectors or archived third-party web pages.

## Source classifications

| Source | Frozen evidence | Classification | Release disposition |
|---|---|---|---|
| UNSW lattice page | Page and response headers retrieved 2026-07-29T07:08:28Z | `UNCLEAR` | Keyed merits; do not embed vectors |
| Magic Point Shop | Page and response headers retrieved 2026-07-29T07:08:29Z | `UNCLEAR` | Keyed merits; do not embed vectors |
| QMCPy `a774f3a…` | Frozen `LICENSE` and response headers retrieved 2026-07-29T07:08:30Z | `REDISTRIBUTABLE` (Apache-2.0 conditions apply) | May redistribute with license and attribution |

The UNSW page makes the vector files available and documents their
construction, but states no license or express redistribution
permission.  Magic Point Shop asks users to cite related work and
displays a copyright notice, but likewise states no redistribution
license.  Neither absence is interpreted as prohibition; both are
conservatively `UNCLEAR`.

QMCPy's frozen license expressly grants reproduction and distribution
rights under Apache-2.0 conditions.

## Production mode

The v1 table release will not embed the UNSW generating vectors.
Instead, each merit is keyed by:

1. source citation;
2. frozen full-source snapshot hash;
3. entry index;
4. per-entry generator-prefix hash.

Users obtain the vector from its source and can replay a selected entry
after its hashes match.  Merit residues, bounds, certificates, and
reconstruction are project-authored and remain fully distributable.
This mode is mandatory unless a later explicit redistribution grant is
archived and a new release policy is issued.

## Numerical cross-check tooling

The FFTW/LatNet harness is under `tools/numerical-crosscheck/`, tagged
`NUMERICAL`, excluded from source-release exports, and outside the
trusted and distributable dependency graph.  The release build links no
FFTW object.

## Boundary

These are conservative engineering classifications of archived text,
not legal advice. `UNCLEAR` never authorizes embedded redistribution,
and `PROHIBITED` would halt any intended embedding.
