# Draft correspondence: dimension-six lens-space factorization

Subject: A precise boundary-fusion question for the dimension-six
Shintani--Faddeev cocycle

Dear Dr. Kopp,

We have been studying the dimension-six AFK twisted-convolution packet
at

\[
 \beta=(5+\sqrt{21})/2,\qquad
 A=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}.
\]

The finite arithmetic side is complete: the ray labels, all 36
characteristic multipliers, both formal TCC frequency maps, and all 225
rank-two minor reductions are exact. The remaining primitive order-six
orientation is the familiar obstruction.

We found a representation that may give a cleaner analytic formulation.
With the Sarkissian--Spiridonov general modular parameters

\[
 (p,k,r,s)=(-115,24,5,24),
\]

the primitive AFK quotient is the \(g=Q,\ell=0\) two-gamma kernel in
their degenerate lens-space beta convolution. In the upper half-plane
the honest packet has independent bases

\[
 q=e^{2\pi i\tau},\qquad \widetilde q=e^{2\pi iA\tau}.
\]

At the RM point, \(A\beta=\beta\). Independently, the standard Faddeev
pair fuses because

\[
 \beta+\beta^{-1}=5.
\]

The resulting formal fusion is exactly the previously derived
well-poised \({}_2\psi_2\) packet at argument \(-q\). A dimension-five
control calculation instead lands on the \(+q\) summable locus and
recovers the proved dimension-five value.

The published meromorphic Fourier evaluation applies to the
dimension-six specialization, but it leaves the oriented product

\[
 \Gamma_M(-\alpha,4-N)\Gamma_M(\alpha,N)
\]

after canonical reflection and shift reductions. It therefore does not
by itself give the missing finite multiplicative relation. Moreover, at
\(g=Q\) the two Bernoulli asymptotics cancel, so the original vertical
contour is not absolutely convergent at either end. We have now checked
the full pole cones: no finite pinch occurs at \(g=Q\); the failure is
loss of decay at imaginary infinity.

Parametrize the attracting \(A\)-axis by
\[
 \gamma(s)=\frac52+
 \frac{\sqrt{21}}2\frac{1-s^2}{1+s^2}
 +i\frac{\sqrt{21}s}{1+s^2}.
\]
In the notation of your Definitions 4.7 and 4.9 and Proposition 7.20,
the weakest sufficient question is:

> Does the primitive order-six logarithmic spectral resolvent have a
> finite limit along \(\gamma(s)\) as \(s\downarrow0\), and does
> meromorphic spectral periodization commute in this component with
> trace-five base fusion while preserving the norm-\(37\)
> Frobenius/lens label?

No uniform or Hölder estimate is needed for the conditional theorem.
Existence makes the limit \(A\)-invariant because \(A\) translates the
same oriented axis toward \(\beta\).

We have checked exactly that \(A\equiv I\pmod6\), so it fixes all 36
characteristics, and that

\[
 (\psi^{-2}\chi_{\boldsymbol r}^{-1})(A)
 =\Phi_{\boldsymbol r}^{\,2}
\]

in every case. Thus a positive answer to the fusion-continuity question
would finish both formal dimension-six shifts without any further
finite computation.

Does this boundary statement match a version of the
Shintani--Faddeev cocycle continuation you already have, or is there a
natural correction term at the quadratic irrational fixed point?

Best regards,

Hainan Zhao
