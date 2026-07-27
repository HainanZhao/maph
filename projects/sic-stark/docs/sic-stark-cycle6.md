# SIC--Stark research cycle 6: exact embedding and the pole-free-strip obstruction

Date: 2026-07-26

## Outcome

Cycle 6 tested the only quantum-dilogarithmic route left open by cycle 5:
could the general modular beta integral localize, by residues, to the
finite characteristic sum in primitive TCC?

The answer is no for the natural two-gamma specialization. The conclusion
is stronger than a numerical mismatch:

\[
\boxed{\text{Every TCC node lies strictly inside the integrand's
pole-free strip, so none can be a localization residue.}}
\]

The route produced two positive structural results before failing:

1. every canonical Shintani--Faddeev value embeds exactly into the
   unnormalized general modular gamma function;
2. in dimension four, the published beta-integral phase can be chosen to
   match the primitive TCC phase up to a single global eighth root of
   unity.

Thus the finite q-Pochhammer corrections, the larger discrete modulus,
and the quadratic phase are not the final obstruction. The obstruction
is analytic: the desired evaluation points are regular interior points,
whereas contour localization can only see the pole cones outside the
strip.

This closes the standard Fourier/pentagon/beta-integral route. Reviving it
would require inserting a new meromorphic sampling kernel, which is no
longer an application of the known identity.

## 1. General modular parameters of the canonical matrix

Sarkissian--Spiridonov use the convention

\[
M=
\begin{pmatrix}
-p&-s\\
k&-r
\end{pmatrix},
\qquad
pr+ks=1,\qquad k>0.
\]

For the canonical family,

\[
A_d=L_d^3=
\begin{pmatrix}
d^3-3d^2+d+1&-d(d-2)\\
d(d-2)&1-d
\end{pmatrix}.
\]

Hence

\[
\boxed{
k=d(d-2),\quad
p=-(d^3-3d^2+d+1),\quad
r=d-1,\quad
s=d(d-2).
}
\]

The relation \(pr+ks=1\) follows from \(\det A_d=1\).

At the fixed point \(\tau=\beta=\beta_d\), take

\[
\omega_2=1,\qquad
\omega_1=j_{A_d}(\beta)=k\beta+1-d=\beta^3.
\]

Then the parameter used in the general modular gamma definition is

\[
\frac{\omega_1+r\omega_2}{k\omega_2}
=\frac{k\beta+1-d+d-1}{k}
=\beta.
\]

Thus these are the periods that identify the general modular gamma
function with the actual Jacobi cocycle at its real-multiplication point.

## 2. Exact q-product dictionary

The unnormalized general modular gamma function is

\[
\gamma_M(\mu,h)=
\frac{(\widetilde q\,e^{2\pi i\widetilde u};
       \widetilde q)_\infty}
     {(e^{2\pi i u};q)_\infty},
\]

where

\[
u=\frac{\mu+h\omega_2}{k\omega_2},
\qquad
\widetilde u=\frac{\mu-ph\omega_1}{k\omega_1}.
\]

Kopp's Jacobi cocycle has the q-product

\[
\sigma_{\boldsymbol m,A}(z,\tau)
=
\frac{
\left(
e^{2\pi i(z/j_A(\tau)+m_2A\tau-m_1)},
e^{2\pi iA\tau}
\right)_\infty}
{
\left(e^{2\pi iz},e^{2\pi i\tau}\right)_\infty
}.
\]

Set

\[
h=m_2-1,\qquad
\mu=kz-h
\]

with \(\omega_2=1\). Then \(u=z\). The determinant relation
\(pr+ks=1\) gives

\[
A\tau+\widetilde u
=\frac{z}{j_A(\tau)}+(h+1)A\tau.
\]

The integer \(m_1\) does not affect the exponential. Therefore

\[
\boxed{
\sigma_{\boldsymbol m,A}(z,\beta)
=\gamma_A(kz-m_2+1,m_2-1).
}
\]

This equality first holds in the q-product domain and then at the RM
boundary value by meromorphic continuation.

## 3. The canonical characteristic embedding

For a TCC characteristic
\(\boldsymbol q=(q_1,q_2)\), let

\[
z_{\boldsymbol q}=\frac{q_2\beta-q_1}{d},
\qquad
n(\boldsymbol q)=q_2-(d-2)q_1.
\]

The modular-to-Jacobi relation has \(m_2=n(\boldsymbol q)\). Define

\[
D=(d-2)\beta-1.
\]

Substitution into the q-product dictionary gives the cancellation

\[
\begin{aligned}
\mu_{\boldsymbol q}
&=kz_{\boldsymbol q}-n(\boldsymbol q)+1\\
&=(d-2)(q_2\beta-q_1)
  -q_2+(d-2)q_1+1\\
&=1+q_2D,
\end{aligned}
\]

and

\[
h_{\boldsymbol q}
=q_2-(d-2)q_1-1\pmod{k}.
\]

Consequently

\[
\boxed{
u_d(q_1,q_2)
=\gamma_{A_d}
\left(1+q_2D,\,
q_2-(d-2)q_1-1\right).
}
\]

This explains how the \(d^2\) characteristic values fit inside the
larger modulus \(k=d(d-2)\):

\[
h_{\boldsymbol q}\equiv q_2-1\pmod{d-2}.
\]

For each fixed \(q_2\), varying \(q_1\) selects \(d\) points in one
congruence class of the \(k\)-valued discrete variable. The pair
\((\mu_{\boldsymbol q},h_{\boldsymbol q})\) is injective on the
\(d^2\)-point characteristic grid.

This corrects an overstatement in cycle 5: unequal moduli are a warning
against a direct identification, but they are not by themselves an
obstruction. The TCC grid has a natural sparse embedding in the modular
gamma cylinder.

## 4. The primitive quotient is exactly a two-gamma kernel

Replacing \(q_1\) by \(q_1-1\) leaves \(\mu_{\boldsymbol q}\) unchanged
and sends

\[
h_{\boldsymbol q}\longmapsto
h_{\boldsymbol q}+d-2.
\]

Thus

\[
\frac{u_d(q_1,q_2)}{u_d(q_1-1,q_2)}
=
\frac{\gamma_A(\mu,h)}
     {\gamma_A(\mu,h+d-2)}.
\]

The normalized modular gamma is

\[
\Gamma_A(\mu,h)
=Z(h)e^{-\pi iB_{2,2}(\mu)/(2k)}
\gamma_A(\mu,h).
\]

Its reflection formula is

\[
\Gamma_A(Q-\mu,r-1-h)\Gamma_A(\mu,h)=1,
\qquad Q=\omega_1+\omega_2.
\]

Because \(r-1=d-2\),

\[
\frac1{\Gamma_A(\mu,h+d-2)}
=\Gamma_A(Q-\mu,-h).
\]

The Bernoulli factors cancel in the quotient, giving

\[
\boxed{
\frac{\gamma_A(\mu,h)}
     {\gamma_A(\mu,h+d-2)}
=
\frac{Z(h+d-2)}{Z(h)}
\Gamma_A(\mu,h)\Gamma_A(Q-\mu,-h).
}
\]

The two gamma factors are exactly the kernel appearing in the published
degenerate beta identity

\[
\sum_{h\bmod k}\int
e^{\text{quadratic phase}}
\Gamma_A(y,h)\Gamma_A(-y+g,l-h)\,dy.
\]

Taking \(g=Q\) and \(l=0\) produces the primitive quotient kernel. This
is an exact alignment, not an analogy.

## 5. Dimension-four phase match

For \(d=4\),

\[
A_4=\begin{pmatrix}21&-8\\8&-3\end{pmatrix},
\qquad
(k,p,r,s)=(8,-21,3,8).
\]

Write

\[
\beta=\frac{3+\sqrt5}{2},\qquad
D=2\beta-1=2+\sqrt5.
\]

Then

\[
\omega_1=\beta^3=D^2,\qquad
\omega_2=1,\qquad
Q=D^2+1=4D+2.
\]

The 16 TCC nodes are:

| \(q_2\) | \(\mu=1+q_2D\) | allowed \(h\bmod8\) |
|---:|---:|:---|
| 0 | \(1\) | \(1,3,5,7\) |
| 1 | \(1+D\) | \(0,2,4,6\) |
| 2 | \(1+2D\) | \(1,3,5,7\) |
| 3 | \(1+3D\) | \(0,2,4,6\) |

Since

\[
h=q_2-2q_1-1\pmod8,
\]

the primitive TCC Fourier phase, expressed as a power of
\(\zeta_8=e^{\pi i/4}\), is

\[
i^{-(q_1+q_2)}
=\zeta_8^{\,h+1-3q_2}.
\]

The normalization quotient is

\[
\frac{Z(h+2)}{Z(h)}=\zeta_8^{5h}.
\]

Hence the normalized-gamma form of the TCC weight is

\[
\zeta_8^{\,6h+1-3q_2}.
\]

In the published two-gamma identity, choose

\[
N=3,\qquad g=Q,\qquad l=0,\qquad \alpha=-3D.
\]

The discrete phase is \(\zeta_8^{6h}\), while its continuous exponential
at \(y=1+q_2D\) is \(\zeta_8^{6-3q_2}\). Its total phase is therefore

\[
\zeta_8^{\,6h+6-3q_2}.
\]

It differs from the normalized TCC phase by the single global factor
\(\zeta_8^5\), independent of \(q_1,q_2\). Equivalently, the TCC weight
is \(\zeta_8^3\) times the beta-integral weight. A global nonzero factor
does not affect the desired vanishing.

The phase gate therefore passes.

## 6. The pole-free-strip obstruction

For positive real periods, the true poles of the unnormalized modular
gamma function are

\[
\mu=-j\omega_1-t\omega_2,
\qquad j,t\in\mathbb Z_{\geq0},
\]

subject to the published discrete congruence involving \(h\). In
particular, every pole of \(\Gamma_A(y,h)\) lies on or to the left of
\(y=0\).

The poles of the reflected factor
\(\Gamma_A(Q-y,-h)\) occur when

\[
Q-y=-j\omega_1-t\omega_2,
\]

so every one lies on or to the right of \(y=Q\).

The open real strip

\[
0<y<Q
\]

is therefore pole-free for the full two-gamma quotient kernel, for every
discrete \(h\).

But the characteristic nodes obey

\[
\mu_{\boldsymbol q}=1+q_2D>0
\]

and, using \(Q=dD+2\),

\[
Q-\mu_{\boldsymbol q}
=1+(d-q_2)D>0
\]

for \(0\leq q_2<d\). Thus

\[
\boxed{0<\mu_{\boldsymbol q}<Q}
\]

for every canonical characteristic in every dimension \(d\geq4\).

The external quadratic exponential in the beta identity is entire, so
the phase specialization creates no additional poles. Moving a contour
through the open strip crosses no poles and yields no residues. Closing
it beyond either boundary encounters an infinite pole cone, not the
finite \(d^2\)-point characteristic set.

The residue proof in the source works by making parameter-dependent pole
pairs pinch the contour. In the TCC specialization \(g=Q,l=0\), the
desired nodes remain regular interior evaluations; no corresponding
pinch occurs at them.

This fails the cycle's hard acceptance test.

## 7. What the q-Pochhammer factors were doing

Cycle 5 treated the finite q-Pochhammer corrections as a possible extra
multiplier that had to survive a transform. The exact q-product
dictionary shows a cleaner picture:

\[
h=n(\boldsymbol q)-1.
\]

The correction index is absorbed into the discrete variable of the
general modular gamma function. The primitive change
\(n\mapsto n+d-2\) is precisely the discrete shift
\(h\mapsto h+d-2\).

So the correction factors are compatible with the rarefied gamma
formalism. They do not solve the localization problem because that
problem is controlled by the continuous pole geometry.

## 8. Decision and next direction

The known quantum-dilogarithm identities now pass more gates than cycle 5
suggested:

- the actual special values embed exactly;
- the correction indices become the discrete gamma coordinate;
- the primitive ratio becomes the published two-gamma kernel;
- the \(d=4\) phase matches up to a global root of unity.

They fail at the last indispensable gate: residues cannot return regular
interior samples.

Therefore:

\[
\boxed{\text{Close the standard pentagon/localization route.}}
\]

One could manufacture a sampling kernel with poles at
\(\mu_{\boldsymbol q}\), but proving an identity for that new kernel would
be essentially equivalent to proving the missing finite Fourier identity
itself. It would not reduce TCC to a known beta integral.

The next lower-cost, higher-information direction is algebraic rather
than analytic:

> Can the primitive TCC coefficient be written as a character-weighted
> field trace of a Stark-unit ratio, so that ray-class Galois action and
> character orthogonality force its vanishing?

This asks the finite sum to vanish for the reason finite sums most
naturally vanish. It also directly targets the missing Shimura
reciprocity/Galois-action information identified in the source work.

Cycle 7 carries out this audit. Its exact local calculation shows that
ray-class multiplication moves the output direction together with the
summation characteristic, while the additive Fourier phase fails to
descend if the direction is held fixed. Thus character resolvents apply
to the full residual packet, not to one primitive coefficient; see
[`sic-stark-cycle7.md`](sic-stark-cycle7.md).

## Executable checks

The following functions implement the exact audit:

- `canonical_general_modular_parameters()`;
- `canonical_general_modular_characteristic()`;
- `canonical_general_modular_node_strip_margins()`;
- `canonical_dimension_four_localization_record()`.

The tests check the parameter dictionary and the injective
characteristic embedding, certify both positive strip margins for
\(4\leq d\leq500\), and verify all 16 dimension-four phase comparisons.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  definitions of the Jacobi and modular Shintani--Faddeev cocycles, their
  q-products, and the modular-to-Jacobi characteristic relation.
- Sarkissian--Spiridonov,
  [arXiv:1910.11747](https://arxiv.org/abs/1910.11747):
  definitions of \(\gamma_M,\Gamma_M\), the parameter convention
  \(M=[[-p,-s],[k,-r]]\), true pole sets, reflection and normalization
  formulas, and the two-gamma degeneration `namer2`.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the canonical family, special-value array, correction index, and TCC.
