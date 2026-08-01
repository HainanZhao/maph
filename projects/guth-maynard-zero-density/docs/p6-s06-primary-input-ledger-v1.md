# P6 S06 primary-input ledger v1

## Outcome and claim boundary

`PROVED`: conditional on the local multiplicity input `LC`, the detector's
principal-character low-height input `LOW_HEIGHT_MULTIPLICITY_COUNT` follows
at the required polylogarithmic scale from the pinned primary
Riemann--von Mangoldt source.  It is therefore not an independent S06
analytic premise.  This is a source-and-algebra reduction only: it proves no
CGL theorem, zero-density estimate, or short-interval result.

`OBSERVED`: exact statements matching the remaining all-modulus inputs
`L_POLY_A`, `FOURTH_MOMENT_H`, and `LC` were not present in the frozen local
primary corpus.  They remain explicitly `CONJECTURED` external premises for
this project.  In particular, the normal availability of a convexity bound is
not substituted for a checked theorem with the correct character and height
uniformity.

This is a research-stage source ledger.  It uses lightweight source and
algebra checks and does not initiate a paper-stage hostile audit.

## Frozen source readings

The CGL-v2 TeX says the following.

- `OBSERVED`: TeX 2138 claims that the principal residue leaves at most
  `N(sigma,A log(qT)) << (log(qT))^2` zeros, but does not specify a
  multiplicity convention.
- `OBSERVED`: TeX 2154--2158 passes from zero classes to cardinalities of
  well-spaced zero sets and invokes Davenport Chapter 16 for a unit-height
  difference bound.  Its exact theorem statement, character range, and
  multiplicity convention are not included in the frozen source.
- `OBSERVED`: TeX 2169--2171 cites Montgomery, *Topics in Multiplicative
  Number Theory*, Theorem 10.3 for its fourth-moment step.  The accessible
  publisher record identifies the cited book and its chapter pagination, but
  the theorem text is not frozen locally.
- `OBSERVED`: TeX 2140 needs a polynomial critical-line bound to quantify a
  `qT`-uniform Mellin tail; it gives no theorem or complete uniform statement
  for that purpose.

The frozen primary source of Hasanalizade--Shen--Wong, Corollary 1.2, gives
for every `T >= e` an explicit Riemann--von Mangoldt estimate for
`N_zeta(T)`, where its displayed definition counts zero locations with
`0 < Im(rho) <= T`.  This source is adequate for an upper bound on the
*distinct* zero locations regardless of whether its notation is read with a
multiplicity convention.

## Input ledger

| Input | Disposition | Exact scope |
|---|---|---|
| `L_POLY_A` | `CONJECTURED` external | Need one theorem uniform in every relevant primitive Dirichlet character and real `v`, giving `|L(1/2+iv,chi)| << [q(2+|v|)]^A` for some fixed `A`. The frozen CGL text invokes a functional equation elsewhere but does not state this bound; prime-modulus or restricted-conductor estimates do not close the all-modulus detector input. |
| `FOURTH_MOMENT_H` | `CONJECTURED` external | Need the discrete hybrid bound for selected pairs `(gamma_r,chi_r)` with `|gamma_r| <= H`, all characters modulo the fixed `q`, and spacing at least one within each character: `sum_r |L(1/2+i gamma_r,chi_r)|^4 <<_delta (qH)^(1+delta)`. A continuous average alone is not silently converted into this discrete statement. |
| `LC` / local multiplicity source | `CONJECTURED` external | Need a multiplicity-inclusive local unit-strip bound, with endpoints and all relevant Dirichlet characters fixed: `sum_{rho, sigma<=Re rho<=1, u<=Im rho<u+1} m(rho,chi) << log(q(|u|+3))`. This is exactly the hypothesis required by `p6-multiplicity-transfer-v1`; CGL's cardinality language does not establish it. |
| `LOW_HEIGHT_MULTIPLICITY_COUNT` | `PROVED` conditional on `LC` | It is a consequence of `LC` and the pinned HSW Corollary 1.2. It is not a standalone theorem extracted from CGL. |

## Low-height reduction

Let `Q=qT`, let `H0=A0 log(Q+3)`, and consider the principal character.  By
the already-proved finite-Euler-factor observation, all zeros in
`Re(s)>0` are zeta zeros.  HSW Corollary 1.2 gives

`# {distinct zeta zeros with |Im(rho)| <= H0} = O(H0 log(H0+3))`.

`PROVED` conditional on `LC`: split `[-H0,H0]` into unit strips.  Every
distinct zero has multiplicity at most the `LC` right side for its strip,
which is `O(log(H0+3))`; hence

`sum_{|Im(rho)|<=H0} m(rho) = O(H0 log(H0+3)^2) = O(log(Q+3)^2)`.

The final coarse square-log bound uses only `H0 = O(log(Q+3))` and
`log log(Q+3) <= log(Q+3)` for large `Q`; compact `Q` is finite and is
already handled separately by the detector repair.  This proves the
low-height premise in the form needed for an `(qT)^{o(1)}` zero-density
argument once `LC` is supplied.  It neither proves `LC` nor resolves the
well-spaced selection convention.

## Conductor-sensitive overlap retained

`OBSERVED`: CGL TeX 122--124 and 159--176 contains `q1`-sensitive
intermediate large-value and density expressions.  The primitive-to-all
transfer already proved in P6 applies to a monotone final envelope in the
primitive conductor, not term-by-term to these formulae: after passage to a
primitive conductor `d`, an originally chosen `q1 | q` need not be a divisor
of `d`, and the source range/case conditions need not persist.  This ledger
does not repair, reinterpret, or promote those expressions.

## Gate effect

`PROVED`: conditional on `LC`, the detector-tail repair may replace its
separate `LOW_HEIGHT_MULTIPLICITY_COUNT` premise by the HSW/`LC` consequence.
`OBSERVED`: the active external-source obligations are consequently
`L_POLY_A`, `FOURTH_MOMENT_H`, and `LC`, together with the retained
conductor-sensitive `q1` scope.  The P6 route remains
`RECONCILED_OPEN_INPUTS`.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p6_s06_primary_input_ledger_v1.py --check
python3 -m unittest tests/test_p6_s06_primary_input_ledger_v1.py -v
```
