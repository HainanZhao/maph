# Cycle 3 G1 envelope-sensitivity map v1

## Outcome and claim boundary

`PROVED`, conditional on the hash-pinned Guth--Maynard source formulas and
the sealed exact structural atlas v2: two independent exact rational routes
agree on the active-term map, all 11 zero-residual transfer rows, and the
critical-cell algebra below. This is a map of the published architecture, not
a new large-values inequality, zero-density estimate, saturation theorem, or
short-interval result. It does not select a G1 route.

The pinned source locations are Guth--Maynard, Theorem 1.1 (TeX lines
68--79), Proposition 11.1 (lines 1785--1820), and the Theorem 1.2
zero-detection transfer/final remark (lines 2307--2399).

The map isolates one necessary target at the published critical transfer:
the third Theorem 1.1 term

\[
  T N^{12/5}V^{-4}.
\]

No improvement to that term is claimed. A parameter \(\mu\) below is an
explicit `CONJECTURED` premise used only to calculate what a future proven
improvement would have to overcome.

## Exact critical cell

At the local coordinate
\((s,n,v,w)=(7/10,5/6,7/10,2/3)\), the exact terms are

\[
 (A_1,A_2,A_3)=(1/2,2/3,2/3),\qquad
 (C_1,C_2,C_3)=(1/2,2/3,5/6),
\]

and

\[
 (E_1,E_2,E_3)=(5/3,5/3,5/3).
\]

Thus `A2,A3` tie for the Theorem 1.1 large-values maximum; the classical
outer maximum is `min(C2,C3)` through `C2`; and all three permitted
diagonal energy labels tie. The exact loci used to audit every finite atlas
label are

\[
\begin{aligned}
A_1-A_2&=2n(v-4/5), & A_1-A_3&=n(2v-2/5)-1,& A_2-A_3&=6n/5-1,\\
C_1-C_2&=n-1, & C_1-C_3&=2n(2v-1)-1,& C_2-C_3&=n(4v-3),\\
E_1-E_2&=n(3-2s)-13w/8-1/4,& E_1-E_3&=n(3-2s)-2w,&
E_2-E_3&=1/4-3w/8.
\end{aligned}
\]

The complete finite activity counts, including every tie label and the 7,040
off-diagonal rows on which energy labels are forbidden, are sealed in the
route artifacts.

## Transfer bottleneck

At the distinct zero-detection coordinate
\((s,n_0,k,q)=(7/10,5/13,2,10/13)\),

\[
B=9/13,\qquad (\mathrm{LV1},\mathrm{LV2},\mathrm{LV3})=(6/13,8/13,9/13),
\]

so the signed residuals \(B-\mathrm{LV}j\) are \((3/13,1/13,0)\). `PROVED`:
only `LV3`, the displayed third Theorem 1.1 term, has zero residual here.

More strongly, all and only the 11 zero-residual rows in the frozen transfer
chart satisfy

\[
n_0=\ell(s)/2,\quad k=2,\quad q=\ell(s),\qquad
B-\mathrm{LV3}=(4s-12/5)(q-\ell(s))=0.
\]

No `LV1`, `LV2`, or mean-value residual vanishes on that chart. This
preserves the negative result: improving only either of the first two terms
has no first-order effect at the critical transfer.

## Conditional gain propagation and its obstruction

For bookkeeping only, suppose `CONJECTURED` that the \(N\)-exponent of the
third term changed from \(12/5\) to \(12/5-\mu\), and that this change were
proved in all ranges needed for zero detection. At the critical transfer the
absolute \(T\)-exponent gain would be \(10\mu/13\). It remains the active term
only for \(0\le\mu\le1/10\); at \(\mu=1/10\), `LV2` becomes the next barrier.
Formally, the pointwise coefficient at the critical point becomes

\[
\frac{30}{13}-\frac{100}{39}\mu.
\]

`PROVED` no-effect limitation: this pointwise calculation cannot by itself
lower the *uniform* \(30/13\) envelope. The existing Ingham side has

\[
\frac{30}{13}-\frac{3}{2-s}
=\frac{30(7/10-s)}{13(2-s)},\qquad s<7/10,
\]

whose left supremum at \(7/10\) remains \(30/13\). Therefore an improvement
confined to the critical point or to the published Guth--Maynard side
\(s\ge7/10\) has zero strict global-envelope margin. It is a contained,
exact P2C obstruction rather than a saturation theorem.

Under the additional `CONJECTURED` premise that the same strengthened term
propagates through a valid zero-detection proof on a left neighborhood
\([7/10-h(\mu),7/10]\), the new junction is determined exactly by

\[
300h^2+(90-50\mu)h-65\mu=0,
\]

using its positive root. The resulting formal expansions are

\[
 b(\mu)=\frac{30}{13}-\frac{50}{39}\mu+O(\mu^2),
 \qquad
 \theta_{\rm formal}(\mu)=\frac{17}{30}-\frac{13}{54}\mu+O(\mu^2).
\]

The final display is only density-to-threshold algebra. By the project plan,
it is not a new short-interval theorem: all explicit-formula ranges and
secondary errors would still require a complete proof replay.

## Evidence and replay

- Route A: direct exact term evaluation, then comparison against every atlas
  label: `artifacts/g1-envelope-sensitivity-route-a-v1.json`.
- Route B: cleared pairwise and transfer-residual identities, independently
  compared against every label:
  `artifacts/g1-envelope-sensitivity-route-b-v1.json`.
- Reconciliation: `artifacts/g1-envelope-sensitivity-reconciliation-v1.json`.

```sh
python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_a_v1.py --check
python3 projects/guth-maynard-zero-density/proof/derive_g1_envelope_sensitivity_route_b_v1.py --check
python3 projects/guth-maynard-zero-density/proof/reconcile_g1_envelope_sensitivity_v1.py --check
python3 projects/guth-maynard-zero-density/proof/run_g1_envelope_sensitivity_v1.py --check-performance
python3 -m unittest projects/guth-maynard-zero-density/tests/test_g1_envelope_sensitivity_v1.py -v
```

Any hash mismatch, activity-label disagreement, non-`LV3` zero residual, or
proposed gain lacking the required left extension refutes the corresponding
scoped conclusion.
