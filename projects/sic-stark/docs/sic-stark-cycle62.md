# SIC--Stark research cycle 62: quadratic induction and the next \(d=6\) attack

## Outcome

The most attractive possible shortcut for dimension six has now been
eliminated exactly: the primitive Artin representation cannot be moved to an
imaginary quadratic abelian extension and evaluated by classical elliptic
units.

The computation also clarifies what should be attempted next.  Repeating
real-quadratic class-number, conductor, or cone calculations will not supply
the missing identity.  The narrowest unexplored analytic mechanism is a
uniform rational-boundary formula for the characteristic
Shintani--Faddeev cocycle, using \(q\)-gamma asymptotics at the cyclic factors
that vanish.

## Exact quadratic-base classification

Let \(N/\mathbf Q\) be the degree-\(24\) normal closure of the one-place
dimension-six ray field.  Exact Galois computation gives

\[
 \operatorname{Gal}(N/\mathbf Q)
 \simeq \operatorname{SmallGroup}(24,8).
\]

The unique normal subgroup of order two cuts out the faithful degree-\(12\)
quotient \(M/\mathbf Q\), whose Galois group is

\[
 \operatorname{Gal}(M/\mathbf Q)
 \simeq \operatorname{SmallGroup}(12,4)
 \simeq D_{12}.
\]

The three index-two subgroups of \(D_{12}\) give exactly three quadratic
subfields:

\[
\begin{array}{c|c|c}
\text{quadratic base}&\text{signature}&
 \operatorname{Gal}(M/\text{base})\\ \hline
\mathbf Q(\sqrt{21})&(2,0)&\text{abelian}\\
\mathbf Q(\sqrt{-3})&(0,1)&\text{nonabelian}\\
\mathbf Q(\sqrt{-7})&(0,1)&\text{nonabelian}.
\end{array}
\]

Thus the only quadratic base over which the faithful quotient becomes
abelian is the original real quadratic field.  Neither imaginary quadratic
subfield supports the abelian class-field structure required for an
elliptic-unit Kronecker-limit evaluation.

This supplies a direct subgroup-lattice version of the earlier
Katayama--Kida obstruction.  It does not merely say that a convenient
imaginary field has not been found: all quadratic bases have been exhausted.

The exact certificate is
`scripts/dimension_six_quadratic_induction_audit.gp`.

## Literature search

The source situation remains unchanged:

- Kopp proves the exact cone-to-cocycle Kronecker-limit formula, but treats
  the ray-field algebraicity statement conditionally outside the elementary
  half-integral cases.
- Ferrara constructs the \(p\)-adic \(L\)-function for precisely the
  mixed-signature real-quadratic setting, but the associated \(p\)-adic
  Stark identity is conjectural there.
- Yalkinoglu expresses the scalar Shintani invariant as a limit of cyclic
  quantum dilogarithms.  This gives cyclotomic/Kummer approximants, not an
  algebraicity theorem for their limit.

In particular, no new theorem located in the search proves

\[
 \exp(D_0/2)=x_{\mathrm{alg}}
\]

for the explicit modulus-six class over \(\mathbf Q(\sqrt{21})\).

Primary sources:

- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, <https://arxiv.org/abs/2411.06763>.
- J. W. Ferrara, *A \(p\)-adic Stark conjecture in the rank one setting*,
  <https://arxiv.org/abs/1904.10561>.
- B. Yalkinoglu, *Shintani's invariant via cyclic quantum dilogarithm*,
  <https://arxiv.org/abs/2508.18320>.

## A concrete new local mechanism

The failed finite cyclic-table experiment substituted the generic
root-of-unity asymptotic

\[
 (w;q)_\infty
 \sim R(w^n,t)D_\zeta(w)^{-1/n}
\]

at points where \(w^n=1\).  That formula is not uniform there; its factors
are singular, which produced the nonintegral formal boundary orders found
in cycle 33.

At a zero cyclic factor the correct local model is instead the
\(q\)-gamma asymptotic

\[
 (Q^a;Q)_\infty
 \sim
 \frac{\sqrt{2\pi}}{\Gamma(a)}
 (1-Q)^{\frac12-a}
 \exp\!\left(\frac{\pi^2}{6\log Q}\right),
 \qquad Q\longrightarrow1^-.
\]

For a characteristic \(\boldsymbol r=(r_1,r_2)\) and a rational point
\(\tau=m/n\), factorization into residue classes modulo \(n\) isolates the
unique singular term:

\[
 (e(r_2\tau-r_1);e(\tau))_\infty
 =
 \prod_{j=0}^{n-1}
 (e((r_2+j)\tau-r_1);e(n\tau))_\infty.
\]

When \((r_2+j)m-r_1n\in n\mathbf Z\), the corresponding factor is of the
form \((Q^a;Q)_\infty\), with

\[
 a=\frac{r_2+j}{n}.
\]

This identifies the missing correction structurally: gamma factors and
their powers of \(1-Q\) must be combined between the numerator and
denominator *before* the cyclic limit is taken.  The fractional exponents
from the earlier formal substitution were symptoms of omitting precisely
these uniform terms.

## What this could and could not prove

A complete uniform formula would provide:

1. well-defined rational-boundary values for every level-six
   characteristic;
2. their exact phases and gamma corrections;
3. a legitimate finite-level setting in which the cyclic five-term
   relation can be applied; and
4. a possible route to TCC by taking the modular-geodesic limit.

It would not automatically prove algebraicity of an arbitrary Shintani
limit.  Its value is that it offers a route to the **TCC identity directly**,
rather than trying to prove the full rank-one Stark conjecture first.
If the regularized finite tables satisfy twisted convolution, their limit
would force the degree-twelve polynomial relation for the scalar analytic
value and bypass the missing Stark identification.

## Recommended next proof target

The next technical lemma should be:

> Derive a uniform root-of-unity asymptotic for
> \(\operatorname{shin}^{\boldsymbol r}_A(\tau)\) when a cyclic factor
> vanishes, with all \(q\)-gamma constants, powers, and branches explicit,
> and specialize it to the \(36\) level-six characteristics along
> \(t_{n+3}\mapsto t_n\).

The first acceptance test is elementary but decisive: every resulting
boundary order for the meromorphic cocycle must be integral, and
reciprocity and Zauner covariance must hold before any finite TCC claim is
made.

This route is technically narrower than proving a new mixed-signature
Stark theorem and is more directly aligned with the north-star TCC goal.

## Reproduction

```bash
gp -q scripts/dimension_six_quadratic_induction_audit.gp
```
