# The analytic-to-Stark bridge in dimension six

Date: 2026-07-28

Let

\[
 K=\mathbb Q(\sqrt{21}),\qquad
 \beta=\frac{5+\sqrt{21}}2,\qquad
 A_6=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}.
\]

Parametrize the attracting half of the \(A_6\)-axis by

\[
 \gamma(s)=\frac52+
 \frac{\sqrt{21}}2\frac{1-s^2}{1+s^2}
 +i\frac{\sqrt{21}s}{1+s^2},
 \qquad s>0.
\]

Then \(\gamma(s)\to\beta\) as \(s\downarrow0\). Kopp's
[Definition 4.7](https://arxiv.org/pdf/2411.06763) chooses the positive
stabilizer generator by this attracting direction and notes that it
translates the same geodesic toward \(\beta\). His Definition 4.9
defines the RM stable value by evaluating the meromorphic continuation
at the fixed point; Proposition 7.20 realizes that value as a limit from
the upper half-plane.

Let \(\mathscr P_j(\tau)\), \(j=0,1,2\), be the three primitive
ray-class logarithms of the verified meromorphic spectral
periodization, in the norm-\(37\) Frobenius order, and put

\[
 \mathscr R_1(\tau)=
 \mathscr P_0(\tau)+\zeta_6\mathscr P_1(\tau)
 +\zeta_6^2\mathscr P_2(\tau).
\]

The logarithm branch is continued from the two-base convergence chamber
along \(\gamma\).

Equivalently, in the interior let \(C_h=\{c+h(t)+it\}\) be any
admissible graph in the pole-free strip. The tilted integral is
independent of \(h\): truncate two graphs, close the region between
them, apply Cauchy's theorem, and let the two joining caps escape using
the common exponential majorant. Thus the finite part
\(\lim_{s\downarrow0}\mathscr P_j(\gamma(s))\), if it exists, has no
remaining contour-choice ambiguity.

For \(j=0,1,2\), define \(U_j^{\rm fus}\) by retaining the certified
level-\(24\) lens label through meromorphic spectral periodization,
then imposing \(\widetilde q_M=q_M\) at the fixed point and evaluating
with the 24-factor continuation—not with the divergent boundary
bilateral series. With the inherited logarithm branches, set

\[
 \operatorname{Fus}_5\mathscr R_1
 =\log U_0^{\rm fus}
 +\zeta_6\log U_1^{\rm fus}
 +\zeta_6^2\log U_2^{\rm fus}.
\]

Here the subscript \(5\) means trace five, not dimension five.

## Minimal sufficient hypothesis

The proof chain consumes neither uniform convergence nor Hölder
regularity. Its weakest sufficient analytic input is:

> **MFC\(_6\) (minimal fusion-continuity).** The scalar
> \(\mathscr R_1(\gamma(s))\) has a finite limit as \(s\downarrow0\),
> and meromorphic spectral periodization commutes with the
> trace-five base fusion in this primitive component, with the
> norm-\(37\) lens/Frobenius label preserved.

Equivalently, if \(\operatorname{Fus}_5\mathscr R_1\) denotes the
explicit alias-collapsed boundary value with the already certified
normalization, then

\[
 \lim_{s\downarrow0}\mathscr R_1(\gamma(s))
 =\operatorname{Fus}_5\mathscr R_1.
\]

Existence of the limit makes it \(A_6\)-invariant automatically because
\(A_6\) translates the same oriented geodesic toward its attracting
fixed point. Thus invariance is a consequence, not an extra hypothesis.
The zero-frequency auxiliary value is not part of MFC\(_6\); it is
supplied separately by the verified AFK endpoint
\(-4\sqrt7\). The tilted/Fresnel zero mode gives the reciprocal pair
\(-2\sqrt7\pm3\sqrt3\), whose trace is exactly that endpoint.

The sharp degeneration parameter is
\[
 A_6\tau-\tau=
 -\frac{24\tau}{24\tau-5}(\tau+\tau^{-1}-5).
\]
Along \(\gamma(s)\), the corresponding decay rate is
\[
 2\pi\sqrt{21}(1-\beta^{-6})s+O(s^2).
\]
Since \(\beta=[4;\overline{1,3}]\) and
\(\|n\beta\|\ge(\sqrt{21}n+\tfrac12)^{-1}\), the hard range is
\(n\asymp s^{-1}\).

## Standalone conditional theorem

> **Analytic-to-Stark theorem.** Assume MFC\(_6\). Then
> \[
> L'_S(0,\chi_1)
> =r_0+\zeta_6r_1+\zeta_6^2r_2.
> \]
> Consequently all thirty-six convention-matched AFK boundary values
> equal the certified algebraic packet, and both formal dimension-six
> TCC shifts hold for every admissible tuple.

The entire algebraic half is proved. The proof uses:

1. the exact characteristic-to-ray bridge;
2. primitive \(C_6\) Fourier projection;
3. the already proved quadratic component;
4. reciprocity \(D_{j+3}=-D_j\);
5. exact \(C_6\) Fourier inversion;
6. shift/reflection/duplication and conductor lowering;
7. the all-36 multiplier ledger with \(\psi^2(A_6)=-1\); and
8. the exact frequency, trace, and minor certificates.

No TCC identity or minor vanishing is used to derive the Stark equality.
They enter only after the complete packet has been recovered.

## Grade-2 equivalence verdict

At the level of the **endpoint value**, fusion and equation (33) are
reduction-equivalent. The reverse direction is explicit. If

\[
 \Lambda_1=A+\zeta_6B,\qquad Q=D_0-D_1+D_2,
\]

then

\[
 D_0=\frac{Q+2A+B}{3},\qquad
 D_1=\frac{-Q+A+2B}{3},\qquad
 D_2=\frac{Q-A+B}{3}.
\]

Equation (33) fixes \(\Lambda_1\), conjugation fixes
\(\Lambda_5\), and the proved conductor-three identity fixes \(Q\).
The displayed inversion recovers the primitive ray packet; the standard
relations and multiplier ledger recover all 36 values. Conversely, the
fused packet implies equation (33) by primitive Fourier projection.

This is conservation of obstruction for the rigid endpoint identity.

The literal MFC\(_6\) statement is stronger. Equation (33) recovers the
same endpoint value but does not, through the standard basis, prove
existence of the geodesic limit or commutation of periodization with
fusion. Thus:

- endpoint value: Grade-2 `EQUIVALENT`;
- full MFC\(_6\): converse `OPEN`;
- honest theorem label: a sufficient analytic regularity hypothesis,
  not a completed reduction of Stark to an already proved theorem.

## Grade-3 attack surface

Unlike the rigid equality (33), the two-base formulation supports:

- differentiation in the interior parameter \(\tau\);
- contour deformation and explicit residue accounting;
- pinch and Stokes analysis;
- variation of the lens label \(\ell\);
- iteration under the \(A_6\) geodesic return map;
- badly-approximable and bounded-partial-quotient estimates at \(\beta\);
- comparison with the dimension-five \(+q\) control family; and
- transfer-operator or spectral-regularity methods.

Thus the arithmetic obstruction has been transferred, without being
weakened, to a precise analytic/dynamical regularity problem. Proving
that regularity theorem would simultaneously prove a convention-fixed
rank-one Stark instance over \(\mathbb Q(\sqrt{21})\) and close both
dimension-six shifts.

## Endpoint contour status

The pole cones do not pinch at \(g=Q\): they remain separated by \(Q\).
There is therefore no finite-pinch residue correction. The obstruction
is at imaginary infinity, where the Bernoulli quadratic decay cancels.
MFC\(_6\) must consequently be attacked through meromorphic spectral
continuation or a canonical distributional finite part, not the
undeformed absolutely convergent vertical integral.
