# Cycle 008 — Engine C projective screen

Date: 2026-07-29

The one-place characters are pulled back through the exact forgetful
matrix to the two-place ray group.  Base conjugation is computed on
PARI ray generators.  For every supported quartic character the
quotient \(\chi/\chi^\sigma\) is required to have exact order two.

The historical ray-24 CM packet passes this screen with no projective
failure.  The bounded pilot finds five further structural C
candidates:

- \(D=6\), ideal HNF `[[4,0],[0,2]]`, norm 8;
- \(D=10\), HNFs `[[3,1],[0,1]]`, `[[3,0],[0,3]]`,
  `[[9,1],[0,1]]`, and `[[6,2],[0,2]]`.

These are candidates only.  The two CM bases, linear reinduction,
local factors, \(|S|\ge3\), root-of-unity factor, and orientation have
not yet been certified.  Status: `VERIFIED_STRUCTURAL_SCREEN`.
