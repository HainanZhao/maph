# P6 qT-uniform detector-tail repair v1

## Outcome and boundary

`PROVED_CONDITIONAL`: the specific `Z03_TAIL_X_RANGE` defect admits a
narrow repair for an amended CGL-style detector. Put \(Q=qT\), choose
\(X=Q^\eta\), \(Y=Q^{1/2}\), and truncate the shifted Mellin integral at

\[
 U=C\log(Q+3), \qquad
 C=\frac4\pi\left(A+\frac\eta2+B+2\right),
\]

where \(A\) is any available polynomial critical-line growth exponent for
Dirichlet \(L\)-functions and \(B>0\) is the desired tail-saving exponent.
The exponential \(\Gamma\)-decay then makes the omitted integral
\(O(Q^{-B})\), uniformly as \(qT\to\infty\), with no hypothesis
\(q\leq T^c\). This is a replacement by a \(qT\)-dependent cutoff, not the
prohibited after-the-fact substitution \(\log^2T\mapsto\log^2(qT)\).

This is neither validation nor correction of Chen--Gupta--Li v2 as written,
and proves no CGL theorem, zero-density estimate, or short-interval result.
It does not edit the P6 reconciliation. The fourth moment, local zero count,
and multiplicity-selection convention remain external inputs.

## Source scope

The replay pins the CGL-v2 tarball and checks TeX 2114--2175: the detector,
Mellin identity, old \(\log^2T\) tail, zero-spacing condition,
\(X=(qT)^\epsilon\), and the use of Montgomery's Theorem 10.3. The pinned
source's Montgomery citation is TeX 2456. The publisher record for
Montgomery's *Topics in Multiplicative Number Theory*, LNM 227 (1971), is
available at [DOI 10.1007/BFb0060851](https://doi.org/10.1007/BFb0060851),
but its theorem text was not in the local pinned corpus; its exact hypotheses
therefore remain `S06_EXTERNAL_INPUTS`.

The artifact records the exact conditional inputs:

- `L_POLY_A`: a polynomial bound
  \(|L(1/2+iv,\chi)|\ll[q(2+|v|)]^A\). Any fixed \(A\) suffices.
- `FOURTH_MOMENT_H`: the source-used fourth-moment estimate at height
  \(H=T+U\), for selected ordinates at least one apart for a fixed character.
- `LOW_HEIGHT_MULTIPLICITY_COUNT`: the source's separate count for the
  principal-character residue below \(A_0\log(Q+3)\).

Thus the proof is a rigorous conditional transport lemma, not a claim that
those cited analytic inputs were re-established here.

## The tail and the class-II shifts

For \(z=1/2-\beta+iu\), \(\beta\geq7/10\), the real part lies in the
pole-free compact strip \([-1/2,-1/5]\). Stirling gives

\[
 |\Gamma(1/2-\beta+iu)|\ll e^{-\pi|u|/2}.
\]

Also \(|M_X(1/2+iv,\chi)|\leq2X^{1/2}\),
\(|Y^z|\leq1\), and for \(|t|\leq T\), \(T\geq1\),

\[
 q(2+|t+u|)\leq3Q(1+|u|).
\]

The conditional polynomial \(L\)-bound therefore gives a tail bounded by

\[
 Q^{A+\eta/2}(1+U)^A e^{-\pi U/2}=O_{A,B,\eta}(Q^{-B}).
\]

The coefficient tail beyond \(Y\log^2Y\) is independently superpolynomially
small from \(c_n\ll_\delta n^\delta\) and \(e^{-n/Y}\). Both estimates now
depend on \(Q\), so they work when \(T\) is fixed and \(q\to\infty\).

If original class-II ordinates have gap \(Q^\eta\), then their maximizing
shifts \(|u_r|\leq U\) satisfy

\[
 |\gamma_r-\gamma_s|\geq Q^\eta-2U\geq\tfrac12Q^\eta
\]

once \(Q\) is large enough. The maxima lie at height \(H=T+U\), and

\[
 qH\leq Q(1+C\log(Q+3))=Q^{1+o(1)}.
\]

Consequently the same source-used fourth-moment estimate costs only a
\(Q^{o(1)}\) factor. In particular at \(T=1\), \(H=1+C\log(q+3)\) and
\(qH=q^{1+o(1)}\): the prior `T -> infinity` gap is absent.

## Residues, compact range, and multiplicity

At a zero, the \(z=0\) residue is exactly
\(L(\rho,\chi)M_X(\rho,\chi)=0\), including a multiple zero. For a principal
character, the \(z=1-\rho\) residue is made small for
\(|t|\geq A_0\log(Q+3)\) using \(|M_X(1,\chi_0)|\ll\log X\) and the same
\(\Gamma\)-decay. Below that height the finite Euler factors of
\(L(s,\chi_0)\) have no zeros in \(\Re s>0\), leaving exactly the source's
separate zeta-style low-height zero count. That count is not silently
claimed here.

For \(1\leq Q<Q_0\), \(q\leq Q_0\) and \(T\leq Q_0\), so the finite,
multiplicity-inclusive constant

\[
 \sum_{q\leq Q_0}\sum_{\chi\bmod q}N(7/10,Q_0,\chi)
\]

absorbs the compact range. The detector need not be invoked where the
original strict \(X,Y,T>1\) declaration is awkward.

The tail argument itself preserves multiplicity, but it does not prove that
the CGL well-spaced selection turns a multiplicity-weighted zero count into a
set of separated distinct ordinates. `S03_MULTIPLICITY_NOT_STATED` remains
open, as do `S06_EXTERNAL_INPUTS`, `F08_T_SMOOTH_UNDEFINED`, and all
\(q_1\)-sensitive intermediate obligations.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/p6_detector_qt_tail_v1.py --check
python3 -m unittest tests/test_p6_detector_qt_tail_v1.py -v
```
