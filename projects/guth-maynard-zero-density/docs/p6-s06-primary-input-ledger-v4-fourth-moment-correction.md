# P6 S06 ledger v4: primitive fourth-moment correction

## Outcome and boundary

`PROVED`: the discrete fourth-moment input used by the `q >= 2` primitive-character CGL detector is supplied. For same-character one-separated selected pairs `(gamma_r, chi_r)` of height at most `H >= 1`,

`sum_r |L(1/2+i gamma_r,chi_r)|^4 <<_delta (qH)^(1+delta)`.

`OBSERVED`: this is a versioned correction, not a validation of CGL-v2. It leaves its `q1`-sensitive formulae, tail range, undefined smoothness condition, zero-density claim, and short-interval consequences unpromoted.

## Continuous-to-discrete route

The published Bui--Heath-Brown theorem (Acta Arith. 141 (2010), Theorem 1) gives the primitive-family critical-line fourth moment for every `q,T >= 2`. Its displayed main and error terms imply `<<_delta (qT)^(1+delta)` after the standard divisor bound; negative ordinates follow by character conjugation.

`PROVED`: a self-contained finite Gaussian three-lines lemma extends this to `1/2 <= Re(s) <= 3/2`. The left boundary is Bui--Heath--Brown; the right boundary is the absolutely convergent Dirichlet series. Primitive characters modulo `q >= 2` are nonprincipal, so there is no pole at `s=1`. Gaussian damping makes the vertical-boundary limit legitimate; the pinned Thorner--Zaman Rademacher lemma supplies the needed strip growth. The submitted Chourasiya--Simonič manuscript records the same finite Gabriel mechanism, but is used only as corroboration.

Set `U=H+1` and `r=1/(10 log(q(H+3)))`. The `r`-disks centred on selected points are disjoint for each fixed character. Subharmonicity bounds their point values by the area integral over `1/2-r <= Re(s) <= 1/2+r`, `|Im(s)| <= U`. On the right this is the finite three-lines bound. On the left, the checked functional equation maps to the conjugate primitive character on the right and costs only `[q(H+3)]^(4r)=O(1)` after fourth powers. The `r^(-2)` loss is polylogarithmic and is absorbed by `delta`.

## Exact scope and retained boundary

`PROVED`: the repair has exactly the primitive scope stated by CGL at TeX 2109, before its conductor transfer. The immutable v1 ledger’s generic all-character wording is not silently relabelled as a separate theorem, and the `q=1` zeta-only case is not asserted here.

`PROVED`: `L_POLY_A`, `LC`, and the derived low-height count are supplied by v2 and v3. `OBSERVED`: P6 nevertheless remains `RECONCILED_OPEN_INPUTS`, because retained independent gates have not been repaired.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p6_s06_primary_input_ledger_v4_fourth_moment_correction.py --check
python3 -m unittest tests/test_p6_s06_primary_input_ledger_v4_fourth_moment_correction.py -v
```
