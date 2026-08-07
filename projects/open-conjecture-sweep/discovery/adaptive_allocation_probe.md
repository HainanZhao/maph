# Adaptive allocation probe

Date: 2026-08-07 UTC.

## Outcome

The smallest proof-valid adaptive extension is **PROVED**, but it adds none
of the 24 decomposable width-five classes missed by the hybrid theorem.
Under the declared kill rule, it does not replace Theorem 2 in the current
paper. It is retained as a successor mechanism because it does certify the
sharpness near-miss `[5]_q[2]_(q^2)[2]_(q^3)`.

## Adaptive single-column lemma

Consider an ordinary-factor vector `a` and spacers `(b_j,r_j)`. Choose one
spacer `j` and one ordinary index `i`, and put

```text
x_0 = a_i - r_j(b_j-1).
```

Assume `x_0>=1`. Remove spacer `j` and replace `a_i` by `x_0`.
If

1. this residual base product is symmetric unimodal, and
2. the residual product obtained by replacing `x_0` by `x_0+2r_j` is
   matrix-certified,

then the original product is symmetric unimodal.

`PROVED`: reconstruct spacer `j` by assigning every increment to column
`i`. At current spacer length `c`, the aligned-center correction bracket has
length

```text
x_0 + 2r_j c.
```

The second hypothesis certifies the smallest correction, at `c=1`. The same
matrix remains valid for every later correction because only that ordinary
length increases. The translated old term was certified at the preceding
step, and the two terms have the usual common center. Induction on `c`
proves the lemma. The base may itself be certified recursively by the same
lemma, terminating at the hybrid theorem.

This formulation also records why unrestricted informal "charge later rows
against grown lengths" is insufficient: the translated base branch must be
certified before any growth occurs. Adaptive growth can fund correction
branches, not retroactively repair that base.

## Exact probe

`experiments/qanalog_adaptive_allocation_probe.py` recursively applies the
lemma to every stable width-five decomposition. It reports:

```text
hybrid classes:   2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54
adaptive classes: 2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54
new classes: none
```

It separately confirms that the adaptive lemma certifies
`[5]_q[2]_(q^2)[2]_(q^3)`, which the static hybrid criterion misses.

Claim tags: the adaptive lemma is **PROVED**; the width-five coverage result
is an exact finite applicability census; no claim is made that broader
adaptive certificate trees cannot reach more cases.
