# P6 S06 ledger v2: polynomial-growth correction

## Outcome and boundary

`OBSERVED`: ledger v1 conservatively retained `L_POLY_A` as external because
no exact all-modulus source had then been matched.  The v1 artifact is
immutable and remains valid as a record of that bounded check.

`PROVED`: the pinned Thorner--Zaman primary source, specialized to
`K=Q`, supplies `L_POLY_A` for every Dirichlet character modulo `q` with a
fixed polynomial exponent.  This correction discharges only that named
growth premise.  It proves neither the source's fourth-moment input nor the
local multiplicity input, and it promotes no CGL theorem.

## Checked specialization

Thorner--Zaman, Lemma Rademacher (source TeX 642--651), applies to a
primitive Hecke character, `eta in (0,1/2]`, and
`-eta <= Re(s) <= 1+eta`.  For `K=Q`, `n_K=D_K=1`; a primitive Dirichlet
character of conductor `d` is the corresponding finite-order Hecke
character of conductor norm `d`.  Set `eta=1/2` and
`s=1/2+iv`.  The lemma yields

`|L(1/2+iv,chi*)| << [d(3+|v|)]^(1/2)`

for nontrivial primitive `chi*`.  For the trivial primitive character,
the displayed ratio factor is at most `3` on this line, so the same bound
holds with an absolute enlargement of the constant.

`PROVED`: if `chi mod q` is induced by `chi*` of conductor `d|q`, then the
finite Euler quotient at the critical line has modulus at most
`2^omega(q) <= q`.  Combining it with the primitive bound gives

`|L(1/2+iv,chi)| << q^(3/2)(3+|v|)^(1/2) << [q(2+|v|)]^(3/2)`.

Thus `L_POLY_A` holds with `A=3/2` (and an absolute implied constant) for
the precise all-character, all-real-height form used in the qT tail repair.
This coarse exponent is more than sufficient because the Mellin factor has
exponential gamma decay.

## Retained obligations

`CONJECTURED`: `FOURTH_MOMENT_H` remains open because the precise discrete
same-character-spaced theorem cited by CGL has not been read.  `CONJECTURED`:
the multiplicity-inclusive unit-strip input `LC` remains open, so the
low-height reduction from ledger v1 is still conditional on `LC`.

`OBSERVED`: the `q1`-sensitive intermediate formulae remain unrepaired;
this correction concerns only the separate polynomial growth input.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p6_s06_primary_input_ledger_v2_lpoly_correction.py --check
python3 -m unittest tests/test_p6_s06_primary_input_ledger_v2_lpoly_correction.py -v
```
