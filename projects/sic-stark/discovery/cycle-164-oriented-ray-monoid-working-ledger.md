# Cycle 164 working ledger: oriented ray-monoid section

## 2026-08-02 — preregistered design

- `CONJECTURED`: use the exact conductor-lowering state space specified in
  the canonical preregistration, with the full oriented ray group as the one
  common (C_6) coordinate target.
- The transition maps and least-exponent section are defined before output
  inspection. The finite prototype can only test totality, recovery on the
  full-modulus rows, and the two frozen anchors.
- A positive result does not construct the missing additive-to-logarithmic
  interface. A negative result only rejects this minimal section, leaving
  local-torsor/cocycle and wild-local engines open.

## 2026-08-02 — exact prototype result

- `PROVED`: the predeclared source has ray structure `C6` and the declared
  generator has discrete log `1`.
- `PROVED`: all 36 reduced ideals lie in the image of that source under their
  respective exact ray projections. The least-exponent section is total; 18
  rows retain the full modulus and recover their direct full-ray logs.
- `PROVED`: the two frozen anchors remain `(3,5)->1` and `(3,4)->2`.
- `OBSERVED`: the principal replay took 0.06 seconds and 14,592 KiB peak RSS
  on the pinned CPython/PARI pipeline.
- The result remains a finite set-theoretic section. It does not yet specify
  an additive-to-logarithmic operation or its AFK compatibility.
