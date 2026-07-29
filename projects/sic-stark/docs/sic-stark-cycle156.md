# SIC--Stark research cycle 156: the central integral does not control periodization

Date: 2026-07-29

## Question

Cycle 155 established that the meromorphic tilted sinh-integral
evaluator is uniformly well conditioned as
\(\tau=\gamma(s)\to\beta_6\).  Cycle 156 asked whether that stability
survives the helical spectral periodization in a conductor-lowered
growing component whose arithmetic overlap is already proved.

The test component is
\[
 (a,b)=(0,2),\qquad 4b-5a\equiv2\pmod6.
\]
It belongs to the modulus-three orbit and is conductor-lowered to the
quadratic character \(\chi_3\).  Its proved arithmetic reference is
\[
 \nu_{0,2}=\sqrt Y,\qquad
 Y^4-Y^3-3Y^2-Y+1=0,
\]
with
\[
 Y=2.369205407092466546286339432\ldots,\qquad
 \sqrt Y=1.539222338420433185692753170\ldots.
\]
The primitive comparison component is \((a,b)=(0,1)\).

## Repairs to the crashed WIP

The inherited script contained three material problems.

1. The endpoint \(\beta=(5+\sqrt{21})/2\) and
   \(\beta^{-6}\) were evaluated at import-time default precision.
   They are now recomputed at the active mpmath precision.
2. Deep \(A_6\)-return points were sent through the full bilateral
   alias sum even though the script itself noted that this would cause
   a tail explosion.  Full packets and raw-kernel return points are now
   separate ladders.
3. The raw fixed-label kernel ratio under the \(A_6\) return was
   incorrectly expected to be \(-1\).  The exact
   \(\psi^2(A_6)=-1\) is the automorphy multiplier of the transported
   Kopp/AFK cocycle, not of the untransported raw kernel.

The WIP also assumed without a bridge formula that the single raw
residue packet \(\mathscr S_{0,2,0}\) should equal \(\sqrt Y\).
Cycle 156 retains \(\sqrt Y\) only as an arithmetic reference.  It does
not assert that normalization identity.

## Validation

For \(s=1/8\), the telescoped alias ratio
\[
 \frac{K_{a,b}(3;\gamma(s))}{K_{a,b}(0;\gamma(s))}
\]
was compared with two independently evaluated tilted kernels.  The
agreement was \(48.16\) digits for \((0,2)\) and \(48.18\) digits for
\((0,1)\).

Every packet was evaluated at two precisions.  The primary ladder used
50 and 80 digits; the deep and residue-recombination ladders used 30 and
50 digits, each with 15 guard digits.  All records lost zero digits.
The weakest deep-packet agreement was \(41.97\) digits.

Thus the observed behavior is not the factorized q-Pochhammer
conditioning artifact of cycle 154.

## Raw-kernel return ladder

The raw fixed-label central kernels were evaluated at
\[
 s_k=\frac18\beta^{-6k},\qquad k=0,1,2.
\]
At
\[
 s_2=8.54049137833296\times10^{-10},
\]
the distances from the directly evaluated boundary kernels were
\[
 1.143\times10^{-7}\quad\text{for }(0,2),
 \qquad
 8.152\times10^{-8}\quad\text{for }(0,1).
\]
The corresponding tilted-value distances were
\[
 1.235\times10^{-6},\qquad 8.831\times10^{-7}.
\]

This reproduces the favorable cycle-155 fact: each central
sinh-integral kernel extends stably to the real-multiplication
boundary.

## Full helical packet: adverse outcome

For the proved component and residue \(r=0\), the packet magnitude was
\[
\begin{array}{c|c|c}
1/s & |\mathscr S_{0,2,0}(s)| & \arg(\mathscr S)/\pi\\
\hline
64   & 4.7825936701 & 0.221126\\
128  & 5.4978399923 & 0.155219\\
256  & 5.8249815543 & 0.115719\\
512  & 6.3806854554 & 0.093912\\
1024 & 6.9322965761 & 0.075601\\
2048 & 7.5561196489 & 0.055522\\
4096 & 9.9615715343 & 0.038928
\end{array}
\]
The magnitude grows by a factor \(2.08288\) from \(1/s=64\) to
\(4096\).  A descriptive power fit gives
\[
 |\mathscr S_{0,2,0}(s)|\asymp s^{-0.1552},
 \qquad R^2=0.943,
\]
on this finite window.  This exponent is diagnostic only.

The term cutoffs grow from about \(38\) at \(1/s=128\) to about \(214\)
at \(1/s=4096\).  Their log--log slope is \(0.5001\), indicating a
\(s^{-1/2}\) computational width on this ladder rather than the
previously asserted \(s^{-1}\) width.  Tail cutoffs are not by
themselves a proof of the analytic concentration scale, but the
discrepancy must be resolved.

## Recombining the three residue classes does not cure the growth

The raw sum
\[
 \mathscr S_{0,2,0}(s)+
 \mathscr S_{0,2,1}(s)+
 \mathscr S_{0,2,2}(s)
\]
was evaluated at four sparse points:
\[
\begin{array}{c|c|c}
1/s & |\mathscr S_0+\mathscr S_1+\mathscr S_2|
& \arg(\mathscr S_0+\mathscr S_1+\mathscr S_2)/\pi\\
\hline
64   & 3.6301778970 & 0.242817\\
256  & 8.8773113895 & 0.032820\\
1024 & 21.7017275261 & 0.368543\\
4096 & 185.4145900092 & 0.374891
\end{array}
\]
The magnitude increases by a factor \(51.0759\).  At the deepest point,
the \(r=1\) packet is already
\[
 68.7585507378+170.3751423081i.
\]
Plain residue recombination therefore supplies no cancellation.

## Verdict

`numerical`, adverse.

The cycle-155 row-(i) result applies to the central tilted integral,
not to spectral periodization.  Cycle 156 shows that this distinction
is essential:

- the raw central kernel has a stable boundary value;
- the bilateral alias evaluator is independently crosschecked and
  well conditioned;
- neither the proved \(r=0\) packet nor the unweighted sum of all three
  residues shows bounded convergence on the tested ladders.

Consequently the componentwise estimate BF\(_6(\eta)\), as presently
written for each raw \(\mathscr S_{a,b,r}\), is not numerically
supported.  Finite numerical growth is not a proof that no
meromorphically normalized limit exists, but the earlier claim that
BF\(_6\) should follow directly from central-integral continuity is
withdrawn.

The proved overlap \(\sqrt Y\) enters only after the exact
characteristic/ray and Fourier normalization.  A raw residue packet
cannot be equated to it without deriving that normalization.

## Next proof position

The next cycle should audit the periodization definition before seeking
an estimate:

1. derive the exact map from the three raw helical residue packets to
   the meromorphic spectral logarithms \(\mathscr P_j\), including every
   Fourier gauge and subtraction term;
2. identify whether the growing contribution is removed by that
   meromorphic normalization or only after the primitive
   \(C_6\)-Fourier combination \(\mathscr R_1\);
3. correct the claimed \(s^{-1}\) active range if the observed
   \(s^{-1/2}\) width reflects the true Gaussian envelope;
4. restate BF\(_6\) for the correctly normalized object, or retire it
   if componentwise convergence is genuinely false.

The weaker MFC\(_6\) primitive-component statement remains the honest
open target.  Cycle 156 does not decide whether cancellations in
\(\mathscr R_1\) yield a finite limit.

## Artifacts

- `scripts/dimension_six_cycle156_growing_component_dissection.py`
- `certificates/dimension-six-cycle156-growing-component.json`

Reproduction:

```bash
cd projects/sic-stark/scripts
python3 dimension_six_cycle156_growing_component_dissection.py \
  > ../certificates/dimension-six-cycle156-growing-component.json
```
