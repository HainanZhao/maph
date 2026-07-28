# SIC--Stark research cycle 147': interior factorization

Date: 2026-07-28

## Verified spectral identity

Sarkissian--Spiridonov equation (66) is the meromorphic Fourier
transform of the continuous-discrete two-gamma kernel. Restriction to
the dual of

\[
 X=(\mathbb R\times\mathbb Z/24)/
   \langle(\omega_1-\omega_2,6)\rangle
\]

collects four discrete lifts and all continuous lifts for each finite
frequency.

For \(z\in\mathbb Z\), the exact reindexing is

\[
 N_z=p_a+2-6z,\qquad
 \ell_z=p_b-6z,
\]

\[
 \frac{\alpha_z}{D}
 =\frac{4p_b-5p_a}{3}+2z.
\]

Three \(z\)-steps give the helical translation. The three resulting
bibasic bilateral classes are locally uniformly and absolutely
convergent in the tested chamber

\[
 |q_M|<|\widetilde q_M|<1
\]

by the geometric bounds in Cycle 144'. Therefore the periodized
identity holds as a meromorphic Fourier-series identity:

\[
\boxed{\text{interior meromorphic spectral identity `VERIFIED`.}}
\]

## Named-corpus audit

Garoufalidis--Kashaev, *From state integrals to \(q\)-series*,
Theorem 1.1, assumes

\[
 I_{A,B}(b)=\int\Phi_b(x)^B e^{-A\pi i x^2}\,dx,
\qquad B>A>0.
\]

It contains no lens label and uses the standard \(S\)-modular partner.
Our integrand is a \(\mathbb Z/24\) sum of two general-\(A_6\) lens
gamma factors. The theorem does not specialize to it.

Beem--Dimofte--Pasquetti gives a physics block-factorization framework,
not a rigorous theorem for this general-lens kernel.

Garoufalidis--Zagier's root-of-unity asymptotics assumes a rational
boundary point. The RM point \(\beta_6\) is quadratic irrational.

Thus none of these sources can be cited as the missing theorem.

## Remaining pointwise gap

The literal contour-periodization statement still requires:

1. one pole-separating contour for every helical translate near
   \(g=Q\);
2. a translate-uniform integrable majorant permitting exchange of the
   helical sum and contour integral; and
3. identification of that pointwise result with the meromorphic
   spectral continuation.

These questions are addressed at the boundary in Cycle 148'.

## Sources

- S. Garoufalidis and R. Kashaev, *From state integrals to
  \(q\)-series*, Theorem 1.1,
  <https://arxiv.org/abs/1304.2705>.
- S. Garoufalidis and D. Zagier, *Asymptotics of Nahm sums at roots of
  unity*, <https://arxiv.org/abs/1812.07690>.
