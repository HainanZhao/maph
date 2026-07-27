# A dimension-four twisted-convolution identity from a Shintani ray unit

**Draft for review — 27 July 2026**

## Abstract

We study the twisted-convolution condition that turns canonical
Shintani--Faddeev real-multiplication values into ghost projectors for
Weyl--Heisenberg symmetric informationally complete measurements.  For
the canonical family

\[
Q_d=\langle1,1-d,1\rangle,\qquad
\beta_d=\frac{d-1+\sqrt{(d+1)(d-3)}}2,
\]

we give exact finite Zak, determinantal, exterior-square, and
parity-moment formulations of the conjecture.  These formulations show
why covariance, reciprocity, low trace moments, distribution relations,
and generic double-sine functional equations do not by themselves
force twisted convolution.

In dimension four, the normalized double-sine table collapses to one
positive real number \(x\).  We prove that all 36 two-by-two minors of
the shifted ghost matrix are divisible by

\[
x^2-\sqrt{3+\sqrt5}\,x+1.
\]

We then identify the square of the relevant real-multiplication value
with the modulus-\((4)\infty_2\) Shintani ray unit

\[
x^2=\phi+\sqrt\phi,\qquad \phi=\frac{1+\sqrt5}{2},
\]

using the Shintani--Kopp Kronecker-limit formula, an elementary ray
class computation, and the analytic class-number formula for
\(\mathbb Q(\sqrt5,\sqrt\phi)\).  It follows that the canonical
dimension-four ghost has rank one and satisfies twisted convolution.
The result is unconditional relative to the cited principal-ghost and
Kronecker-limit formulas; no Stark conjecture is assumed.  The
general-dimensional conjecture remains open.

## 1. Introduction

A SIC in dimension \(d\) is a set of \(d^2\) equiangular lines in
\(\mathbb C^d\).  In the Weyl--Heisenberg covariant formulation, a
rank-one projector is reconstructed from its displacement overlaps.
Recent constructions attach candidate overlaps to special values of
the Shintani--Faddeev modular cocycle at real quadratic fixed points.
The arithmetic formulas supply reality, reciprocal pairing, Galois
structure, and the appropriate covariance.  The missing nonlinear
condition is a finite twisted convolution, abbreviated TCC.

The purpose of this paper is twofold.

1. We give several exact, equivalent formulations of canonical TCC
   that separate its genuinely missing fourth-order content from the
   identities already forced by reciprocity.
2. We prove the canonical condition in dimension four by reducing the
   complete minor system to one ray-unit evaluation.

The second result is deliberately modest in dimensional scope.  Its
value is that it provides a complete example in which the
special-function, class-field, and finite-projector sides can all be
matched without assuming Stark algebraicity.

### Main theorem

Let \(G_4\) be the canonical dimension-four principal ghost formed from
the normalized Shintani--Faddeev values using the phase and exceptional
zero-characteristic conventions of the published principal-ghost
construction.

**Theorem A.** The shifted Zak matrix associated with \(G_4\) has rank
one.  Equivalently, \(G_4\) is idempotent and satisfies the
dimension-four twisted-convolution condition.

The proof occupies Sections 5--8.  Its special-value core is

\[
\left(
\sqrt2\,
\frac{S_2(\beta/4\mid\beta,1)S_2(1/4\mid\beta,1)}
{S_2((\beta+1)/4\mid\beta,1)}
\right)^2
=\phi+\sqrt\phi,
\qquad
\beta=\phi^2.
\]

Our \(S_2\) convention is
\(\Gamma_2(z)/\Gamma_2(1+\beta-z)\); it is the reciprocal of the
double-sine convention used in some references.

## 2. Canonical arithmetic and the TCC target

For \(d\ge4\), set

\[
Q_d=\langle1,1-d,1\rangle,\qquad
L_d=
\begin{pmatrix}
d-1&-1\\
1&0
\end{pmatrix}.
\]

Then

\[
\operatorname{disc}(Q_d)=(d+1)(d-3),\qquad
\det L_d=1,
\]

and

\[
L_d^2+L_d+I=dL_d.
\]

Consequently \(L_d^3\equiv I\pmod d\).  The positive quadratic fixed
point is

\[
\beta_d=\frac{d-1+\sqrt{(d+1)(d-3)}}2,
\]

with period-one negative continued fraction
\(\beta_d=[\overline{d-1}]_-\).

For the displacement convention

\[
D_{p,q}=\tau^{pq}X^pZ^q,\qquad
\tau=-e^{\pi i/d},
\]

write

\[
P=\frac1d\sum_{\boldsymbol p}
a_{\boldsymbol p}D_{\boldsymbol p}.
\]

The equation \(P^2=P\) is equivalent to a finite twisted convolution of
the coefficients.  In even dimension, representative-wrap signs must
be retained; reducing displacement indices naively modulo \(d\) gives
the wrong equation.

The canonical rank-one problem considered here uses \(r=1\), the form
\(Q_d\), shift \(\lambda=1\), and identity twist.  It is weaker than
the full TCC over every admissible tuple, but sufficient for the
corresponding canonical ghost projector.

## 3. Equivalent finite formulations

### 3.1 Zauner reduction

The action of \(L_d\) on \((\mathbb Z/d\mathbb Z)^2\) has orbits of
length one or three.  When \(3\nmid d\), only zero is fixed.  When
\(3\mid d\), the fixed vectors are

\[
(0,0),\quad(d/3,d/3),\quad(2d/3,2d/3).
\]

Both the canonical phase and the RM special values are constant in the
required covariant sense on these orbits.  The zero-output
twisted-convolution equation follows from the inverse law; the
remaining equations reduce threefold.

### 3.2 Zak rank-one formulation

After a scalar shift, shear, and partial Fourier transform, TCC is
equivalent to a rank-one condition for a \(d\times d\) matrix \(K_d\).
Explicitly,

\[
\det (K_d)_{\{i,k\},\{j,\ell\}}=0
\]

for every pair of rows and columns.  Thus all TCC equations can be
written as partial-Fourier exchange identities.

### 3.3 Positive exterior-square certificate

For an arbitrary complex matrix \(K\), define

\[
\Delta_2(K)
=\frac12\left[
(\operatorname{Tr}K^\dagger K)^2
-\operatorname{Tr}\bigl((K^\dagger K)^2\bigr)
\right].
\]

The Cauchy--Binet identity gives

\[
\Delta_2(K)
=\sum_{\substack{|I|=2\\|J|=2}}
|\det K_{I,J}|^2.
\]

Hence \(K\) has rank at most one if and only if
\(\Delta_2(K)=0\).  This compresses TCC to one nonnegative scalar but
does not make the missing fourth-order identity automatic.

### 3.4 Parity fourth moment

The ghost satisfies parity-Hermiticity

\[
G^\dagger=PGP.
\]

Thus \(J=PG\) is Hermitian.  In the normalization used here, the
rank-one condition is equivalent to

\[
\operatorname{Tr}J^4=(\operatorname{Tr}J^2)^2.
\]

Reciprocity determines the lower trace moments but not this fourth
moment.

## 4. Obstructions to generic proofs

The following implications fail without additional RM-specific input.

- Covariance, reciprocal pairing, and cyclic telescoping do not force
  TCC: exact multiplicative countermodels preserve these identities
  while violating a primitive convolution coefficient.
- Ray-class multiplication moves the output direction together with
  the summation variable.  A fixed primitive TCC coefficient is not a
  single ray-class character projection.
- Same-level distribution relations leave formal multiplicative
  freedom; in prime dimensions there is no proper scalar
  conductor-lowering relation on the same characteristic grid.
- The natural equal-base \(q\)-binomial limit cancels every
  nonconstant coefficient and therefore erases the off-grid factor
  needed by TCC.
- The first two reciprocal trace moments and the Bos--Waldron
  holomorphic quartic do not imply the positive parity fourth moment.
  Exact full-rank countermodels demonstrate both failures.

These no-go results explain why the dimension-four proof below uses a
specific ray-unit evaluation rather than only formal identities of the
double sine.

## 5. The dimension-four common factor

Let

\[
\beta=\frac{3+\sqrt5}{2}=\phi^2,\qquad
\tau=-e^{\pi i/4}.
\]

The normalized signed double-sine table of the principal ghost reduces
to

\[
\begin{pmatrix}
\sqrt5&-x&1&-x^{-1}\\
-x^{-1}&-x^{-1}&-x^{-1}&-x\\
1&-x^{-1}&1&x\\
-x&-x^{-1}&x&-x
\end{pmatrix}.
\]

The entry \(\sqrt5\) at the zero characteristic is exceptional and
must not be replaced by the generic triple-double-sine expression.

Before imposing a relation on \(x\), 34 of the 36 minors of the shifted
ghost matrix are nonzero Laurent polynomials.  Exact reduction over
\(\mathbb Q(\sqrt2,\sqrt5)[x,x^{-1}]\) proves:

**Proposition 5.1.** Every minor belongs to

\[
\left(x^2-\sqrt{3+\sqrt5}\,x+1\right).
\]

Therefore the single identity

\[
x+x^{-1}=\sqrt{3+\sqrt5}
\]

implies dimension-four TCC.

The defining special value simplifies by shift and reflection to

\[
x=
\sqrt2\,
\frac{S_2(\beta/4)S_2(1/4)}
{S_2((\beta+1)/4)}.
\]

Independent quadrature gives \(x=1.700015776\ldots\), but numerical
recognition is not used in the proof.

## 6. The modulus-four ray field

The denominator of a primitive quarter characteristic is the ideal
\((4)\).  Let

\[
K=\mathbb Q(\sqrt5),\qquad
\mathcal O_K=\mathbb Z[\phi].
\]

Since \(2\) is inert, exact residue enumeration gives

\[
|\operatorname{Cl}_{(4)\infty_2}(K)|=2.
\]

The candidate ray field is

\[
L=K(\sqrt\phi).
\]

The relative discriminant is \((4)\).  At the identity embedding
\(\phi>0\), whereas at the conjugate embedding \(\phi'<0\); hence the
second real place ramifies.  The conductor is precisely
\((4)\infty_2\).  Since the corresponding ray class group has order
two, \(L\) is the full ray field.

Put

\[
u=\phi+\sqrt\phi.
\]

Its nontrivial Artin conjugate is

\[
u^\sigma=\phi-\sqrt\phi=u^{-1}.
\]

Consequently

\[
N_{L/K}(u)=1,\qquad
\operatorname{Tr}_{L/K}(u)=1+\sqrt5,
\]

and

\[
u^2-(1+\sqrt5)u+1=0.
\]

## 7. Class number and regulator

The absolute discriminant has magnitude

\[
|D_L|=5^2N_{K/\mathbb Q}(4)=400.
\]

The signature of \(L\) is \((2,1)\), so its Minkowski ideal-class bound
is

\[
\frac{4!}{4^4}\frac4\pi\sqrt{400}
=\frac{15}{2\pi}<2.4.
\]

There is no ideal of norm two: the rational prime \(2\) is inert in
\(K\), and the prime above it has norm four in \(L\).  Therefore

\[
h_L=1.
\]

Write \(t=\sqrt\phi\), so \(t^4-t^2-1=0\).  The units

\[
t,\qquad u=t^2+t
\]

form a fundamental system.  A certificate is obtained by placing a
hypothetical missing unit in the centered logarithmic parallelogram
generated by \(t\) and \(u\).  Its conjugate bounds force its
coefficients in the integral basis
\(1,t,t^2,t^3\) into a finite box.  Exact norm enumeration leaves only
\(\pm1\) in this cell.  Thus

\[
\mathcal O_L^\times
=\{\pm t^m u^n:m,n\in\mathbb Z\}
\]

and

\[
R_L=\log\phi\,\log u.
\]

For the nontrivial quadratic character \(\chi\) of \(L/K\),

\[
L(s,\chi)=\frac{\zeta_L(s)}{\zeta_K(s)}.
\]

Using \(h_K=h_L=1\), \(w_K=w_L=2\), and
\(R_K=\log\phi\), the analytic class-number formula at \(s=0\) yields

\[
L'(0,\chi)=\log u.
\]

## 8. Kronecker-limit normalization and proof of Theorem A

Exact residue enumeration with both infinite places gives

\[
|\operatorname{Cl}_{(4)\infty_1\infty_2}(K)|=4.
\]

The quotient to the one-infinite-place group has fibers of order two.
The exponent in Kopp's Kronecker-limit theorem is therefore

\[
n=\frac2{|\text{fiber}|}=1.
\]

For the two one-infinite-place ray classes \(A_0,A_1\),

\[
L(s,\chi)=\zeta(s,A_0)-\zeta(s,A_1).
\]

The generalized derivative in the Kronecker-limit formula is this
difference, and the normalized positive cocycle occurs squared.  Hence

\[
x^2
=\exp Z'(0,A_0)
=\exp L'(0,\chi)
=u.
\]

Now

\[
u+u^{-1}=1+\sqrt5,
\]

so

\[
(x+x^{-1})^2=u+u^{-1}+2=3+\sqrt5.
\]

Since \(x>0\),

\[
x+x^{-1}=\sqrt{3+\sqrt5}.
\]

Proposition 5.1 makes every shifted ghost minor vanish.  The shifted
matrix has rank one, which is equivalent to ghost idempotency and TCC.
This proves Theorem A.

## 9. Scope and consequences

The theorem proves the canonical dimension-four ghost-projector
condition.  It does not prove:

- TCC in every dimension;
- TCC for every admissible tuple in dimension four;
- the Minimalist RM Values Conjecture;
- the Stark conjecture;
- Zauner's conjecture in arbitrary dimension.

The implication toward a live SIC must retain the separate hypotheses
specified by the source construction.  The present theorem closes the
twisted-convolution step only for the canonical dimension-four ghost.

## 10. Referee audit points

The following items should be checked independently before submission.

1. **Double-sine convention.** Verify that the `Zauner.jl` convention
   is the reciprocal of Kopp's \(\operatorname{Sin}_2\) convention and
   that all three shift/reflection steps preserve the displayed branch.
2. **Exceptional characteristic.** Confirm that the zero
   characteristic is replaced by \(\sqrt5\) before the displacement
   chirp.
3. **Minor certificate.** Re-run the exact Laurent reduction of all 36
   minors and inspect the two structurally zero cases.
4. **Ring of integers and unit certificate.** Expand the finite
   coefficient box and norm table used to prove
   \(\mathcal O_L=\mathbb Z[t]\) and the fundamental-unit assertion.
5. **Ray normalization.** Check the chosen infinite place, the
   signature class exchanging \(A_0,A_1\), the fiber order, and the
   exponent \(n=1\) directly against Kopp's Theorem 1.1.
6. **Projector normalization.** Verify that rank one of the shifted Zak
   matrix implies the precise normalized ghost idempotency rather than
   only rank at most one.

These are convention and certificate audits, not appeals to an
unproved Stark statement.

## 11. Reproducibility

The repository contains:

- exact canonical arithmetic and finite certificates in
  `src/sic_stark.py`;
- unit and minor regression checks in `tests/test_sic_stark.py`;
- an independent standard-library quadrature in
  `scripts/explore_dimension_four_double_sine.py`;
- the complete chronological claim ledger in research cycles 1--24.

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/explore_dimension_four_double_sine.py
python3 scripts/verify_sic_fiducials.py --dimension 4 --show-residuals
```

## References

1. S. Flammia et al., *Zauner.jl*, principal-ghost and double-sine
   implementation, <https://github.com/sflammia/Zauner.jl>.
2. G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
   \(q\)-Pochhammer ratios*, arXiv:2411.06763.
3. T. Shintani, *On a Kronecker limit formula for real quadratic
   fields*, J. Fac. Sci. Univ. Tokyo 24 (1977), 167--199.
4. T. Shintani, *On certain ray class invariants of real quadratic
   fields*, J. Math. Soc. Japan 30 (1978), 139--167.
5. N. Kurokawa and M. Wakayama, *Algebraicity and transcendency of
   basic special values of Shintani's double sine functions*,
   Proc. Edinburgh Math. Soc. 49 (2006), 361--366.
6. S. Yamamoto, *Kronecker limit formula for real quadratic fields and
   Shintani invariant*, RIMS Kôkyûroku Bessatsu B4 (2007), 45--50.

## Appendix A. Summary of the general-dimensional findings

The investigation produced the following reusable results.

1. Canonical TCC has a uniform period-three Zauner reduction.
2. The zero-output equation is automatic.
3. Every remaining equation is a distinguished finite symplectic
   Fourier coefficient.
4. TCC is equivalent to rank one of a shifted RM Zak matrix.
5. The complete minor system is one nonnegative exterior-square
   scalar.
6. Parity-Hermiticity converts it to a fourth Schatten-moment
   saturation.
7. Reciprocity fixes lower moments but not the required fourth moment.
8. Distribution, covariance, ray-character, Floquet, and generic
   quantum-dilogarithm routes each admit exact countermodels or a
   precisely identified missing boundary factor.
9. Dimension four is exceptional because its complete minor ideal is
   principal with one double-sine generator.

The most promising general continuation is to search for dimensions in
which the complete minor ideal again factors through a small collection
of ray units whose logarithms can be evaluated by relative
class-number formulas.
