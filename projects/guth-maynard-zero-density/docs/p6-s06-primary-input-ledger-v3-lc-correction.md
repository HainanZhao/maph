# P6 S06 ledger v3: local multiplicity correction

## Outcome and boundary

`PROVED`: the multiplicity-inclusive local unit-strip input `LC` follows for every Dirichlet character from the pinned Thorner--Zaman circle argument plus the pinned primitive-to-all Euler-factor transfer. Consequently, the v1 reduction makes `LOW_HEIGHT_MULTIPLICITY_COUNT` fully `PROVED`.

`OBSERVED`: this versioned correction leaves the v1 and v2 records immutable. It proves no fourth-moment estimate, CGL density theorem, or short-interval theorem. `FOURTH_MOMENT_H` remains `CONJECTURED`.

## Exact local count

For primitive `chi*` of conductor `d`, set `s0 = 1 + 1/20 + i(u+1/2)` and `r = 3/4`.

`PROVED`: the closed rectangle `1/2 <= Re(rho) <= 1`, `u <= Im(rho) <= u+1` fits in this circle. At its furthest corner the squared distance is `(11/20)^2 + (1/2)^2 = 221/400 < 225/400 = (3/4)^2`. The Thorner--Zaman circle lemma applies because the center has real part greater than one and `r <= 1`. With `K=Q`, its right side is `O(log(d(|u|+3)))`.

`PROVED`: the circle lemma's displayed definition writes a cardinality, so this correction uses its proof rather than presuming that notation means multiplicity. In TeX 688--700 every zero contributes a nonnegative term to the logarithmic-derivative sum. The source's Hadamard/logarithmic-derivative derivation explicitly counts zero orders with multiplicity (TeX 614--638). Repeating the same per-zero inequality for that multiset therefore gives the same circle bound with multiplicities.

`PROVED`: if `0 < Re(rho) < 1/2`, the checked functional equation sends `rho` to `1-rho`, a zero of `L(s, conjugate(chi*))` of equal order and ordinate `-Im(rho)`. The reflected closed strip `[-u-1,-u]` is covered by the same circle estimate. This direct functional-equation map is the precise version of the lower-half reduction; the alternative `1-conjugate(rho)` is a zero of the original character, not of its conjugate. It also handles negative `u`. Zeros on the critical line are assigned to the upper half.

`PROVED`: the pinned Euler-factor transfer identifies the zero multisets of an imprimitive `chi mod q` and its primitive inducer in `Re(s)>0`, including multiplicity. Since its conductor `d` divides `q`, the result is `sum_{rho: sigma <= Re(rho) <= 1, u <= Im(rho) < u+1} m(rho,chi) << log(q(|u|+3))` for every `1/2 <= sigma <= 1` and real `u`. The target half-open strip is a subset of the closed strip used above, so endpoints do not create a loss.

## Remaining boundary

`CONJECTURED`: `FOURTH_MOMENT_H` is now the remaining named S06 external analytic input. The retained `q1` scope issue is `OBSERVED`; neither it nor any broader CGL claim is repaired here.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p6_s06_primary_input_ledger_v3_lc_correction.py --check
python3 -m unittest tests/test_p6_s06_primary_input_ledger_v3_lc_correction.py -v
```
