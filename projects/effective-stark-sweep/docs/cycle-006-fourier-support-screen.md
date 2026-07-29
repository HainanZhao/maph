# Cycle 006 — exact sign class and Fourier support

Date: 2026-07-29

`scripts/screen_w1_case.gp` now constructs the one-place and two-place
ray groups, represents the Kopp sign class by the least positive
rational integer in the ideal minus one, and enumerates the dual group
exactly.  A character is retained precisely when
\(1-\overline{\chi(R)}\ne0\); its order is computed from exact dual
coordinates.

No floating \(L\)-values enter this screen.  A seven-anchor structural
regression checks the historical ray structures, support orders, and
the necessary route predicates.  It passed 7/7 and is banked as
`artifacts/w1-anchor-regression-v1.json`.  Status: `VERIFIED`.
