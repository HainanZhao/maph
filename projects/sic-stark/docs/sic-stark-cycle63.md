# SIC--Stark research cycle 63: the \(q\)-gamma boundary correction

## Outcome

The rational-boundary characteristic route is valid after all, once the
zero cyclic factors are treated uniformly.  The obstruction found in cycle
33 was real, but it came from using a nonuniform asymptotic at its branch
locus.  Replacing the singular factor by its \(q\)-gamma asymptotic produces
a finite value for every nonzero level-six characteristic.

This is a genuine advance:

- all fractional formal boundary orders cancel exactly;
- the missing gamma and modular-scale factors are explicit;
- the Möbius curvature contributes one additional computable dilogarithmic
  phase;
- the resulting \(35\)-value tables converge to the real AFK ghost packet;
  and
- their reconstructed matrices converge rapidly toward idempotency and
  rank one.

The finite-level twisted-convolution identity is not yet proved.  The new
calculation supplies a legitimate sequence on which such a proof can be
attempted.

## Uniform asymptotic at a zero cyclic factor

Let

\[
 \tau=\frac mn+\frac{it}{2\pi n^2},\qquad
 q=e(\tau),\qquad
 w=e(r_2\tau-r_1).
\]

Factor the Pochhammer product into residue classes:

\[
 (w;q)_\infty
 =
 \prod_{j=0}^{n-1}(wq^j;q^n)_\infty.
\]

If \(w^n=1\), there is a unique residue \(j_0\) such that
\(w_0\zeta^{j_0}=1\), where

\[
 w_0=e(r_2m/n-r_1),\qquad \zeta=e(m/n).
\]

Along the radial path,

\[
 wq^{j_0}=Q^\alpha,\qquad
 Q=e^{-t/n},\qquad
 \alpha=\frac{r_2+j_0}{n}.
\]

The singular residue must therefore use

\[
 (Q^\alpha;Q)_\infty
 \sim
 \frac{\sqrt{2\pi}}{\Gamma(\alpha)}
 \left(\frac tn\right)^{\frac12-\alpha}
 \exp\!\left(-\frac{\pi^2}{6}\frac nt\right).
\]

Every nonsingular residue has the ordinary Euler--Maclaurin asymptotic

\[
 (\lambda Q^a;Q)_\infty
 \sim
 \exp\!\left(-\frac{\operatorname{Li}_2(\lambda)}{t/n}\right)
 (1-\lambda)^{\frac12-a}.
\]

The distribution identity for the dilogarithm makes the product of the
essential exponentials equal to
\(\exp(-\pi^2/(6t))\).  That common term cancels between the numerator and
denominator of the modular cocycle.

## Exact cancellation in dimension six

For

\[
 A=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}=L^3,
\qquad
 L=\begin{pmatrix}5&-1\\1&0\end{pmatrix},
\]

take the rational geodesic

\[
 t_k=\frac{T_{k-1}}{T_k},
\qquad
 T_{k+1}=5T_k-T_{k-1}.
\]

Then

\[
 A\cdot t_{k+3}=t_k.
\]

At each step exactly five nonzero characteristics have a zero cyclic
factor.  Their \(q\)-gamma parameters are

\[
 \left\{\frac16,\frac13,\frac12,\frac23,\frac56\right\}.
\]

For every one of them, the numerator parameter equals the denominator
parameter.  Hence:

\[
 \boxed{\text{boundary order}=0}
\]

and the factors \(\Gamma(\alpha)\) cancel.  The surviving radial-scale
term is

\[
 \left(\frac n{n'}\right)^{\frac12-\alpha}
 =
 j_A(m/n)^{\alpha-\frac12}.
\]

The five-characteristic pattern has period three and is transported from
one step to the next by \(L^{-1}\bmod6\), exactly matching the Zauner
cycle.

## The Möbius-curvature phase

There is one more constant that is invisible in a first-order radial
substitution.  If

\[
 A\cdot\frac mn=\frac{m'}{n'},
\]

then

\[
 A\cdot\tau
 =
 \frac{m'}{n'}
 +\frac{i(t+\kappa t^2+O(t^3))}{2\pi n'^2},
\qquad
 \kappa=-\frac{ic}{2\pi nn'}.
\]

Since the leading exponential is
\(\exp(-\operatorname{Li}_2(x)/t)\), with

\[
 x=e(r_2m-r_1n),
\]

the quadratic change of radial parameter leaves the constant

\[
 \boxed{
 \exp\!\left(
 -\frac{ic}{2\pi nn'}\operatorname{Li}_2(x)
 \right).
 }
\]

Direct product evaluation at the small-denominator test
\(\tau\to1/4\), \(A\tau\to19/4\), confirms this correction.  For the
singular characteristic \((2,2)/6\), the ratio of the direct product to
the corrected asymptotic approaches \(1\):

\[
\begin{array}{c|c}
t&\text{direct}/\text{corrected}\\ \hline
0.4&0.99856-0.02410i\\
0.2&0.99964-0.01210i\\
0.1&0.99991-0.00606i\\
0.05&0.99998-0.00303i.
\end{array}
\]

Without the curvature factor the ratio instead approaches
\(e^{-\pi i/8}\), so this term is decisive for phases.

## Full-table convergence

The AFK data for the canonical form

\[
 Q(p_1,p_2)=p_1^2-5p_1p_2+p_2^2
\]

give

\[
 \Phi_{\boldsymbol p}
 =
 (-1)^{s_6(\boldsymbol p)}
 e^{-\pi i\Psi(A)/12}
 \tau_6^{-Q(\boldsymbol p)},
\qquad
 \Psi(A)=6.
\]

Multiplying every regularized boundary cocycle value by this phase and
using the exceptional value \(\sqrt7\) at zero produces a full table.
The first four rational steps give:

\[
\begin{array}{c|c|c|c|c}
\text{denominator}&
\max|\operatorname{Im}\nu_p|&
\|K^2-K\|_{\max}&
\max|2\text{-minor}|&
\nu_{0,1}\\ \hline
527&
1.09\cdot10^{-1}&
2.18\cdot10^{-2}&
7.83\cdot10^{-3}&
-2.14960+0.01794i\\
2525&
5.02\cdot10^{-3}&
1.02\cdot10^{-3}&
3.56\cdot10^{-4}&
-2.20997+0.00084i\\
12098&
2.19\cdot10^{-4}&
4.44\cdot10^{-5}&
1.56\cdot10^{-5}&
-2.21276+0.00004i\\
57965&
9.60\cdot10^{-6}&
1.94\cdot10^{-6}&
6.78\cdot10^{-7}&
-2.21288+0.000002i.
\end{array}
\]

The limiting algebraic entry is

\[
 \nu_{0,1}=-2.212885289\ldots.
\]

Thus the corrected boundary table converges simultaneously toward:

1. the real AFK overlap table;
2. the isolated degree-\(12\) primitive root; and
3. the twisted-convolution rank-one locus.

## What is proved and what remains

Proved exactly in this cycle:

- the singular residues for all \(36\) characteristics;
- equality of numerator and denominator \(q\)-gamma parameters;
- cancellation of every nonzero boundary order;
- the period-three/Zauner transport of the singular patterns;
- the Rademacher invariant \(\Psi(A)=6\); and
- the form of the gamma, scale, and curvature corrections.

Numerically established:

- convergence of the defining infinite products to the corrected boundary
  constants for one singular and one nonsingular characteristic;
- convergence of the corrected full tables;
- convergence toward the isolated primitive unit;
- decreasing idempotency and minor residuals.

Still required:

> Express the finite twisted-convolution defect of the corrected table in
> cyclic-dilogarithm form and prove that it tends to zero along the rational
> geodesic.

This is now a well-posed analytic identity.  It would prove dimension-six
TCC directly, without first proving the mixed-signature Stark
algebraicity conjecture.

Kopp explicitly states that rational characteristic values require extra
treatment when cyclic factors vanish; the calculation above supplies the
missing local asymptotic in this example.  See
<https://arxiv.org/abs/2411.06763>, Section 4.11.  The scalar cyclic
geodesic is motivated by Yalkinoglu's construction:
<https://arxiv.org/abs/2508.18320>.

## Reproduction

```bash
python3 scripts/dimension_six_qgamma_boundary.py
```
