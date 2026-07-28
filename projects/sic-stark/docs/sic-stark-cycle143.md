# SIC--Stark research cycle 143: enclosure gate and hard halt

Date: 2026-07-28

## Verdict

\[
\boxed{\text{complete chain not enclosed; downstream cycles halted}}
\]

The fresh Arb implementation separates a sound upstream packet from a
missing analytic continuation step.

- The four positive double-sine generators are enclosed.
- The primitive value encloses the isolated algebraic root
  \[
  x_{\mathrm{alg}}
   =2.212885289017182609068716603734\ldots .
  \]
- All \(225\) analytic rank-two minor balls contain zero.
- The exceptional characteristic agrees with AFK's unconditional
  endpoint:
  \[
  \nu_0+\nu_0^{-1}=-4\sqrt7.
  \]

These statements tag the double-sine packet `ENCLOSED` and the exact
endpoint specialization `VERIFIED`. They do not enclose the proposed
end-to-end lens/Slater chain.

## Located broken link

Let

\[
 A_6=\begin{pmatrix}115&-24\\24&-5\end{pmatrix},
 \qquad
 \beta_6=\frac{5+\sqrt{21}}2,
\]

and put

\[
 q(\tau)=e^{2\pi i\tau},\qquad
 \widetilde q(\tau)=e^{2\pi i A_6\tau}.
\]

The ordinary one-base bilateral packet derived in cycles 133--142
requires the equal-base specialization
\(\widetilde q=q\).  But

\[
 A_6\tau-\tau
 =\frac{-24(\tau^2-5\tau+1)}{24\tau-5}.
\]

It is therefore not identically integral on any open segment of the
\(A_6\)-axis. Arb excludes \(\widetilde q=q\) at the three rationally
parametrized axis points \(t=20,10,5\). At the fixed endpoint
\(\tau=\beta_6\), equality returns, but \(|q|=1\).

For

\[
 {}_2\psi_2(x,w^2x;-qw^2x,-qx;q,-q)
\]

the ordinary bilateral convergence annulus is

\[
 |q|^2<|-q|<1.
\]

It is nonempty for \(|q|<1\) and collapses at the RM endpoint. Hence
the equal-base \( {}_2\psi_2\)-to-Slater expression is not an
off-boundary evaluation of the two-base lens packet. Using it at three
interior radii would already assume the modularly completed connection
formula that the program calls “the Lemma.”

The obstruction is consequently not a failed numerical identity. It is
a missing map

\[
 \text{two-base lens packet }(q,\widetilde q)
 \longrightarrow
 \text{completed equal-base boundary packet}.
\]

That map must be stated and justified before an end-to-end radial Arb
enclosure is mathematically defined.

## Calibration details

The Arb run at 40 decimal digits and tolerance \(10^{-7}\) returned:

\[
\begin{array}{c|c}
\text{quantity}&\text{enclosure summary}\\ \hline
x&2.2128853\pm2.67\cdot10^{-8}\\
y&1.5392223\pm5.28\cdot10^{-8}\\
z&0.35942820\pm7.31\cdot10^{-9}\\
w&0.33571313\pm5.09\cdot10^{-9}\\
\max |\text{minor ball}|&\le 2.55\cdot10^{-8}\\
\nu_0+\nu_0^{-1}+4\sqrt7&0\pm9.41\cdot10^{-40}.
\end{array}
\]

The shared tail majorant was widened from the proved strip
\((1/100,5)\) to \((1/100,6)\). For \(v\ge36\) and \(z<6\),
\(v/z+1>7\), so both absolute exponential denominators exceed
\(7/8\), their product exceeds \(3/4\), and the existing
\(e^{-36}/9\) remainder remains valid. The publication-precision
dimension-five Voutier certificate was rerun and still passes.

## Status ledger

| Item | Status |
|---|---|
| Double-sine \(x_{\rm alg}\) comparison | `ENCLOSED` |
| All 225 analytic minor balls | `ENCLOSED` |
| AFK endpoint \(-4\sqrt7\) | `VERIFIED` |
| Equal bases at three interior axis points | `EXCLUDED` |
| Standard \( {}_2\psi_2\) convergence at \(\beta_6\) | `EXCLUDED` |
| Complete Zak-to-Slater radial chain | `NOT ENCLOSED` |
| Cycles 144--152 under the stated gate | `HALTED` |

## Required restart

The next cycle must precede the requested regime-(i) scan. It should:

1. write the genuine two-base interior lens packet;
2. state the proposed \((q,\widetilde q)\)-to-boundary completion as an
   independent identity;
3. test that identity at generic \(\tau\in\mathfrak H\); and
4. only after it is enclosed, specialize to the equal-base RM boundary
   and resume Cycles 144--152.

## Reproduction

Use the pinned `python-flint` environment:

```bash
PYTHONPATH=scripts python \
  scripts/dimension_six_cycle143_gate.py \
  --digits 40 --tolerance 1e-7

SIC_STARK_RUN_ARB=1 PYTHONPATH=scripts python -m unittest \
  tests.test_dimension_six_cycle143_gate -v
```

The concise transcript is
`certificates/dimension-six-cycle143-gate.txt`.
