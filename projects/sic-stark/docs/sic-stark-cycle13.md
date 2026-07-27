# SIC--Stark research cycle 13: reflection and the ghost involution

Date: 2026-07-27

## Outcome

Cycle 13 reduces the two-matrix equation from cycle 12 to one quadratic
matrix equation.  The reduction is exact; the remaining quadratic
identity is equivalent to TCC and is not proved here.

For the canonical rank-one family, let

\[
A=\mathcal Z_\sigma(F),\qquad
B=\mathcal Z_\sigma(V)
\]

be the two finite RM Zak matrices of cycle 12.  Let

\[
c_0=e^{-\pi i\Psi(A_t)/6},\qquad s^2=c_0,
\]

with the square root fixed by the Stark phase \(\phi_0(t)\), and set
\(C=sA\).  Kopp's fixed-point reflection theorem and the
Appleby--Flammia--Kopp phase formula imply

\[
\boxed{B=c_0A+\delta I.}
\]

The scalar correction \(\delta\) comes entirely from the zero
characteristic.  Retaining it gives

\[
\boxed{C^2-d\sqrt{d-3}\,C-d^2I=0.}
\]

Equivalently,

\[
\boxed{
H=\frac{2C-d\sqrt{d-3}\,I}{d\sqrt{d+1}}
\quad\text{must satisfy}\quad H^2=I.
}
\]

The trace is already forced:

\[
\operatorname{Tr}H=2-d.
\]

Thus a proof of the involution would give eigenvalue multiplicities
\(1\) and \(d-1\).  Up to entrywise complex conjugation and, in even
dimension, a Weyl conjugation, \(H\) is \(2\widetilde\Pi-I\) for the
normalized SIC ghost operator of the source paper.  The remaining
identity is therefore exactly ghost-projector idempotency, not a weaker
consequence of reflection.

## 1. The reflection reduction

Use the notation

\[
u(q)=\operatorname{shin}^{q/d}_{A_t}(\beta),\qquad
F(q)=\omega_d^{-mQ(q)}u(q),\qquad
V(q)=u(-q)^{-1}.
\]

The Stark phases obey

\[
\phi_q(t)^2=c_0\omega_d^{-mQ(q)}.
\]

For \(q\ne0\), the fixed-point reflection formula is

\[
u(q)u(-q)=\phi_q(t)^{-2}.
\]

Consequently

\[
V(q)=c_0F(q),\qquad q\ne0.
\]

It is essential not to insert \(q=0\) into this formula.  Write

\[
\nu_0=su(0)=-\lambda^{-1/2},
\qquad
\lambda=j_{A_t}(\beta)>1.
\]

The exceptional coefficient gives

\[
B=c_0A+\delta I,\qquad
\delta=u(0)^{-1}-c_0u(0)
=-s\left(\sqrt\lambda-\lambda^{-1/2}\right).
\]

As \(s^2=c_0\), the cycle-12 equation \(AB=d^2I\) is equivalent to

\[
C^2-t_0C-d^2I=0,\qquad
t_0=\sqrt\lambda-\lambda^{-1/2}.
\]

For a general admissible tuple \((d,r,Q)\sim(K,j,m,Q)\), the same
argument and the arithmetic relation

\[
(d_j+1)r(d-r)=d^2-1
\]

give

\[
t_0=d\sqrt{d_j-3},
\qquad
H=
\frac{2C-d\sqrt{d_j-3}\,I}
     {d\sqrt{d_j+1}},
\qquad
\operatorname{Tr}H=2r-d.
\]

Hence the general TCC is equivalent to \(H^2=I\).  Conditional on that
identity, the two algebraic multiplicities are \(r\) and \(d-r\).

## 2. Canonical radical audit

In the canonical rank-one family, \(d_j=d\) and
\(\lambda=\beta_d^{-3}\).  Since

\[
\beta_d+\beta_d^{-1}=d-1,
\]

the exact recurrence

\[
T_0=2,\quad T_1=d-1,\quad
T_n=(d-1)T_{n-1}-T_{n-2}
\]

computes \(T_n=\beta_d^n+\beta_d^{-n}\).  In particular,

\[
T_3=d^3-3d^2+2.
\]

Therefore

\[
\begin{aligned}
\left(\beta_d^{-3/2}+\beta_d^{3/2}\right)^2
&=T_3+2=(d-2)^2(d+1),\\
\left(\beta_d^{-3/2}-\beta_d^{3/2}\right)^2
&=T_3-2=d^2(d-3).
\end{aligned}
\]

The positive square root gives \(t_0=d\sqrt{d-3}\), exactly as required
by the one-matrix reduction.

## 3. Why reflection is not yet the proof

The reflection theorem determines \(B\) affinely from \(A\), but it does
not determine the minimal polynomial of \(A\).  In the ghost
normalization, the source paper proves parity-Hermiticity rather than
ordinary Hermiticity.  Parity-Hermiticity and the known trace do not
force \(H^2=I\).

This also rejects two tempting shortcuts:

1. Dropping the zero characteristic falsely gives \(B=c_0A\).
2. Replacing the coefficient reflection by an ordinary matrix adjoint
   loses a chirp and fails already in dimension four.

The determinant is also too weak.  A formal dimension-four model can
have the required determinant magnitude while its product matrix has a
large off-scalar defect.

## 4. Zauner blocks give no further equation reduction

The three Zauner eigenspace dimensions, as an unordered multiset, are

\[
\begin{array}{c|c}
d\bmod3&\text{multiplicities}\\ \hline
0&(k+1,k,k-1)\\
1&(k+1,k,k)\\
2&(k+1,k+1,k),
\end{array}
\qquad d=3k+(d\bmod3).
\]

Their squared sum is

\[
\begin{cases}
(d^2+6)/3,&3\mid d,\\
(d^2+2)/3,&3\nmid d.
\end{cases}
\]

This is exactly the number of Zauner characteristic orbits already
used in the scalar reduction.  Block diagonalization changes
coordinates but supplies no additional equations.

## 5. The retained off-grid factor

The analytic round expanded an interior Shintani--Faddeev quotient as
a double \(q\)-Pochhammer series.  If \(N=n+m\), the finite root filter
produces the cyclic polynomial

\[
K_j^\varepsilon(x)
=\sum_{b=0}^{d-1}
 \tau_d^{\varepsilon b^2-2jb}x^b
=\frac{g_\varepsilon}{d}(1-x^d)
 \sum_{\ell\bmod d}
 \frac{\tau_d^{-\varepsilon(\ell-j)^2}}
      {1-x\omega_d^{-\ell}}.
\]

The important multiplier is

\[
\boxed{1-\widetilde q^{\,n}q^m.}
\]

At the RM boundary,

\[
x^d=e^{2\pi i\beta_dN},
\]

which is not \(1\) for \(N>0\) because \(\beta_d\) is irrational.
Thus the off-grid factor cannot be discarded.

If the two radial bases are instead identified prematurely, then

\[
\sum_{n=0}^{N}
\frac{(-1)^nq^{n(n-1)/2}}
     {(q;q)_n(q;q)_{N-n}}=\delta_{N0}.
\]

This is the finite \(q\)-binomial theorem after multiplication by
\((q;q)_N\).  It erases every nonconstant coefficient and therefore
cannot prove the RM boundary identity.

The remaining analytic theorem would have to justify a uniform
root-filtered Stokes limit, including interchange of the double series,
the residue-class filter, and the irrational fixed-point boundary
limit.  The currently published characteristic-wise asymptotics do not
provide that theorem.

## 6. Claim ledger

Proved in this cycle:

- the exact affine reflection relation between the two Zak matrices;
- the necessity and exact value of the zero-characteristic correction;
- equivalence of TCC to the normalized involution \(H^2=I\);
- the unconditional trace of \(H\) and its conditional multiplicities;
- the canonical radical simplification;
- equality of Zauner-block and Zauner-orbit equation counts;
- the equal-base \(q\)-binomial collapse and the retained off-grid
  factor.

Still open:

- the involution \(H^2=I\) for the RM values;
- equivalently, idempotency of the normalized ghost operator;
- an additional modular-cocycle or additive inversion identity strong
  enough to imply that involution.

## Sources

- G. Kopp, *The Shintani--Faddeev modular cocycle*, Theorem 4.36,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- D. M. Appleby, S. T. Flammia, and G. S. Kopp, *A constructive approach
  to Zauner's conjecture via the Stark conjectures*, Theorem 5.6,
  Theorem 5.8, and Lemma 5.9,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
