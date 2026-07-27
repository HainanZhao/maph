# SIC--Stark research cycle 14: cyclic boundaries and moment obstruction

Date: 2026-07-27

## Outcome

Cycle 14 does not prove the Twisted Convolution Conjecture.  It finds
one new analytic route and puts two stronger rejection gates around it.

First, the cyclic-quantum-dilogarithm approximation announced by
Yalkinoglu aligns unexpectedly well with the canonical family.  If

\[
S_n=\beta_d^n+\beta_d^{-n},\qquad
\mathfrak t_n=\frac{S_{n-1}}{S_n},
\]

then the reduced rational approximants at indices \(n\) and \(n+3\)
have identical numerator and denominator residues modulo \(d\).  This
is exactly the arithmetic step \(L_d^3\in\Gamma(d)\).  Along either
universal subsequence \(n\equiv1,2\pmod3\), the reduced denominator is
coprime to \(d\), for every parity of \(d\).

The rational approximants also retain the off-grid multiplier that was
lost by the equal-base specialization in cycle 13.  If
\(\mathfrak t_n=M_n/N_n\) is reduced, then

\[
1-\exp(2\pi i\mathfrak t_nJ)\ne0
\quad\Longleftrightarrow\quad
N_n\nmid J.
\]

Thus every fixed \(J>0\) survives for all sufficiently large \(n\).

This does not yet prove TCC.  The announced cyclic theorem supplies an
absolute-value limit for an identity-class Shintani invariant, not the
full signed \(d^2\)-characteristic Shintani--Faddeev packet.  It also
does not provide the uniform finite five-term identity whose
root-filtered limit would have to vanish off zero.

Second, reciprocity already forces

\[
\operatorname{Tr}\widetilde\Pi
=\operatorname{Tr}\widetilde\Pi^2=1,
\qquad
\operatorname{Tr}H=2-d,
\qquad
\operatorname{Tr}H^2=d.
\]

These moments are not progress toward the involution: an exact
ordinary-Hermitian, reciprocal, Zauner-invariant countermodel has all
four and still has \(H^2\ne I\).

Third, a June 2026 quantum-dilogarithm Fourier identity has exactly the
quotient--Fourier shape of TCC, but the actual RM values fail its
defining inversion law at the exceptional zero characteristic.
Moreover, its finite Fourier kernel is degenerate when \(3\mid d\),
and where it is nondegenerate the published right-hand side is a
nonzero gamma quotient rather than a delta function.  A new singular
RM boundary theorem is still required.

## 1. Exact period-three cyclic approximants

The small fixed point satisfies

\[
\beta_d+\beta_d^{-1}=d-1.
\]

Consequently

\[
S_0=2,\qquad S_1=d-1,\qquad
S_n=(d-1)S_{n-1}-S_{n-2}.
\]

Modulo \(d\), the recurrence begins

\[
S_0,S_1,S_2,S_3\equiv2,-1,-1,2\pmod d
\]

and therefore

\[
\boxed{S_{n+3}\equiv S_n\pmod d.}
\]

Consecutive terms have constant gcd

\[
g=\gcd(S_{n-1},S_n)=\gcd(2,d-1).
\]

Set

\[
M_n=S_{n-1}/g,\qquad N_n=S_n/g.
\]

Then \(\gcd(M_n,N_n)=1\) and

\[
(M_{n+3},N_{n+3})\equiv(M_n,N_n)\pmod d.
\]

When \(d\) is even, \(g=1\), and \(N_n\equiv-1\pmod d\) for
\(n\equiv1,2\pmod3\).  When \(d\) is odd, \(g=2\) is invertible
modulo \(d\), so all three residue classes have denominator coprime to
\(d\).  Hence

\[
\boxed{n\equiv1,2\pmod3}
\]

is a parity-independent safe subsequence.

The same period is visible on the matrix side:

\[
L_d=
\begin{pmatrix}d-1&-1\\1&0\end{pmatrix},
\qquad
L_d^3\equiv I\pmod d.
\]

This is not a numerical coincidence.  In the canonical principal
modulus, the modular-geodesic step entering the RM value is the same
threefold stabilizer used in the TCC reduction.

## 2. The off-grid factor survives before the limit

At the rational approximant \(\mathfrak t_n=M_n/N_n\), the cycle-13
factor becomes

\[
1-\exp(2\pi iM_nJ/N_n).
\]

Because \(M_n\) and \(N_n\) are coprime, this vanishes exactly when
\(N_n\mid J\).  For fixed \(J>0\), \(N_n>J\) eventually, so the factor
is nonzero and tends to

\[
1-\exp(2\pi i\beta_dJ)\ne0.
\]

This supplies a clean way to avoid the false equal-base cancellation.
It does not justify interchanging the characteristic sum, a
five-term identity, and the \(n\to\infty\) limit.

## 3. Scope of the announced cyclic theorem

Yalkinoglu's announced formula writes a Shintani invariant as

\[
X_1(\mathfrak f)
=
\lim_{n\to\infty}
\left|
\frac{D_{\mathfrak t_n}(y,x)}
     {D_{\mathfrak t_{n+g}}(y,x)}
\right|,
\]

with an analogous expression for \(X_2\).  In the principal
\(\mathfrak f=(u)\) case this simplifies to a one-characteristic
formula involving \(D_{\mathfrak t_n}(1/u)\).

For the canonical modulus \(u=d\), the conductor step is three, so the
arithmetic in Section 1 is directly relevant.  Three gaps remain:

1. TCC needs every characteristic \(\boldsymbol p/d\), not only the
   identity-class invariant.
2. TCC uses signed square roots with the explicit
   Shintani--Faddeev phase, while the announced limit is an absolute
   value.
3. The announcement states that a full account with proofs is
   forthcoming; it does not itself supply a uniform five-term limit.

The correct analytic target is therefore a characteristic-wise,
phase-retaining extension of the cyclic approximation followed by a
finite identity that remains uniform on the safe subsequences.

## 4. The first two trace moments are automatic

Write the canonical ghost Weyl coefficients as

\[
a_{\boldsymbol0}=1,\qquad
a_{\boldsymbol p}=c\,u_{\boldsymbol p},
\quad
c^2=\frac1{d+1},
\quad
u_{\boldsymbol p}u_{-\boldsymbol p}=1.
\]

Weyl orthogonality gives

\[
\operatorname{Tr}\widetilde\Pi^2
=\frac1d\sum_{\boldsymbol p}
 a_{\boldsymbol p}a_{-\boldsymbol p}
=\frac1d\left(1+\frac{d^2-1}{d+1}\right)=1.
\]

For \(H=2\widetilde\Pi-I\),

\[
\operatorname{Tr}H=2-d,\qquad
\operatorname{Tr}H^2
=4\operatorname{Tr}\widetilde\Pi^2
 -4\operatorname{Tr}\widetilde\Pi+d=d.
\]

Thus reciprocity forces the identity coefficient of \(H^2\), but none
of its traceless coefficients.

Newton's identity also makes the second elementary symmetric function
automatic:

\[
e_2(H)
=\frac{(\operatorname{Tr}H)^2-\operatorname{Tr}H^2}{2}
=\frac{(d-1)(d-4)}2.
\]

The first possible spectral obstruction is therefore \(e_3\).  A
characteristic polynomial would still be insufficient for a
non-Hermitian ghost because it does not exclude Jordan blocks.

There is a sharper determinantal reformulation.  Since
\(\operatorname{Tr}\widetilde\Pi=1\),

\[
\boxed{
\widetilde\Pi^2=\widetilde\Pi
\iff
\operatorname{rank}\widetilde\Pi=1
\iff
\text{every }2\times2\text{ minor of }\widetilde\Pi\text{ vanishes}.
}
\]

Indeed, rank one gives
\(\widetilde\Pi=uv^{\mathsf T}\), and its trace
\(v^{\mathsf T}u=1\) then implies idempotency.  Conversely a
trace-one idempotent has rank one.  Equivalently, every \(2\times2\)
minor of \(H+I\) must vanish.  This is a smaller and
Jordan-insensitive target for a future Fay or Plücker identity.

## 5. Exact Hermitian moment countermodel

Let \(d\ge5\) be odd and set every nonzero normalized overlap to one:

\[
u_{\boldsymbol p}=1,\qquad
c=\frac1{\sqrt{d+1}}.
\]

Define

\[
\Pi_*=\frac1d
\left(I+c\sum_{\boldsymbol p\ne0}D_{\boldsymbol p}\right).
\]

The data are real, reciprocal, periodic, Zauner-invariant, and have
the correct overlap magnitude.  They are even ordinarily Hermitian.
For odd \(d\), character orthogonality gives

\[
\sum_{\boldsymbol p}D_{\boldsymbol p}=dP,
\]

where \(P|j\rangle=|-j\rangle\).  Hence

\[
\Pi_*=\frac{1-c}{d}I+cP.
\]

The parity multiplicities are \((d+1)/2\) and \((d-1)/2\), and the two
eigenvalues are

\[
\lambda_+=\frac{1+(d-1)c}{d},
\qquad
\lambda_-=\frac{1-(d+1)c}{d}
=\frac{1-\sqrt{d+1}}d<0.
\]

Therefore

\[
\Pi_*^2\ne\Pi_*,
\]

despite

\[
\operatorname{Tr}\Pi_*=\operatorname{Tr}\Pi_*^2=1.
\]

In coefficient form, the zero residual vanishes exactly,

\[
R_{\boldsymbol0}
=1+(d^2-1)c^2-d=0,
\]

while every nonzero residual is

\[
\boxed{
R_{\boldsymbol t}=(2-d)c-2c^2<0.
}
\]

This closes every route based only on reality, reciprocity, Zauner
covariance, parity-Hermiticity, ordinary Hermiticity, determinant, or
the first two trace moments.

## 6. A quotient--Fourier quantum-dilogarithm near-hit

Bazhanov, Kashaev, Mangazeev, and Sergeev prove for a Fourier
self-dual quantum dilogarithm \(\varphi\) on a Pontryagin group
\(\mathcal S\) an identity of the form

\[
\int_{\mathcal S}
\frac{\varphi(w+x)}{\varphi(w+y)}
\mathcal F(z,w)\,dw
=
\text{an explicit quotient of three shifted }\varphi\text{-values}.
\]

This is the closest published shape found so far to a TCC residual.
For the canonical quadratic chirp, its symmetric Fourier matrix has
determinant \(3\).  Thus:

- when \(3\mid d\), the proposed finite kernel is degenerate;
- when \(3\nmid d\), the identity evaluates the residual to a
  generally nonzero quotient, not to \(d^2\delta_{\boldsymbol p,0}\);
- the defining inversion law fails at the exceptional zero
  characteristic by the factor
  \(\lambda=\beta_d^{-3}>1\).

The zero exception is the same correction that produced the affine
term in cycle 13.  Replacing only the zero value by
\(\sqrt\lambda\,u(\boldsymbol0)\) repairs the inversion equation, but
this is not a global normalization: it changes every Fourier
coefficient and is not covered by the published five-term or
self-duality theorem.  A useful future theorem would have to be a
point-defect or boundary version of the quotient--Fourier identity
whose exceptional term becomes precisely the ghost-projector delta.

## 7. Claim ledger

Proved in this cycle:

- period-three congruence of the reduced Chebyshev approximants;
- a parity-independent coprime-denominator subsequence;
- exact retention of every fixed positive off-grid degree along that
  subsequence;
- automatic values of
  \(\operatorname{Tr}\widetilde\Pi^2\) and
  \(\operatorname{Tr}H^2\), hence of \(e_2(H)\);
- equivalence of TCC to the rank-one determinantal equations for the
  ghost operator;
- an exact odd-dimensional Hermitian countermodel with all coarse
  moments but nonzero off-identity residuals;
- the zero-characteristic and \(3\mid d\) obstructions to the new
  quotient--Fourier identity.

Still open:

- a characteristic-wise, phase-retaining cyclic approximation;
- a uniform finite five-term identity producing a delta function;
- the RM involution \(H^2=I\), hence TCC.

## Sources

- B. Yalkinoglu, *Shintani's invariant via cyclic quantum
  dilogarithm*, Theorems 3.1--3.2,
  [arXiv:2508.18320](https://arxiv.org/abs/2508.18320).
- V. V. Bazhanov, R. M. Kashaev, V. V. Mangazeev, and
  S. M. Sergeev, *Quantum Dilogarithms and New Integrable Lattice
  Models in Three Dimensions*, equations (2.18a)--(2.18b),
  [arXiv:2512.23338](https://arxiv.org/abs/2512.23338).
- G. Kopp, *The Shintani--Faddeev modular cocycle*, Theorem 4.36,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, Conjecture 1.35,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
