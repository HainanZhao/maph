# SIC--Stark research cycle 10: the fractional-cell exchange gate

Date: 2026-07-26

## Outcome

Cycle 10 retained the unspecialized \(q\)-Pochhammer factors and
attempted to eliminate neighboring values around a closed
\(1/d\)-characteristic cell.

The result is a sharp two-gate obstruction:

| Candidate | Exact for the analytic \(q\)-product? | Rejects the cycle-9 deformation? |
|---|---:|---:|
| closed-cell zero curvature | yes | no |
| scalar bilinear Hirota determinant | no | yes |

Thus neither candidate can imply TCC.

The exact closed-cell equation is only the flatness identity for ratios
of a vertex potential. It holds for **every** nonzero array and
therefore survives multiplication by the formal unit deformation.

The simplest genuinely additive candidate,

\[
F(w)F(stw)-F(sw)F(tw)=0,
\qquad
F(w)=(w;q)_\infty,
\]

does detect that deformation. However, Euler's expansion gives

\[
[w]\left(F(w)F(stw)-F(sw)F(tw)\right)
=
\frac{-1+s+t-st}{1-q}
=
-\frac{(1-s)(1-t)}{1-q},
\]

which is nonzero for a genuine fractional cell.

Iterating \(d\) fractional steps does not repair the problem. It either
recovers ordinary characteristic periodicity or changes the modulus to
\(\tau/d\) or \(d\tau\), returning to the external-level distribution
structure closed in cycle 9.

Therefore:

\[
\boxed{\text{Ordinary scalar \(q\)-Pochhammer cell elimination cannot
produce the missing TCC exchange law.}}
\]

The remaining escape is narrower and genuinely analytic: a relation
that exists only in the singular real-multiplication boundary limit and
uses its Stokes/Floquet asymptotics. Such a relation is not a consequence
of the ordinary \(q\)-difference recursion on the upper half-plane.

## 1. Unspecialized characteristic transport

Write

\[
F(w;q)=(w;q)_\infty
\]

and, for a characteristic
\(\boldsymbol r=(r_1,r_2)\), put

\[
\begin{aligned}
z&=r_2\tau-r_1,&
w&=e^{2\pi i z},&
q&=e^{2\pi i\tau},\\
\widetilde z&=r_2(A\!\cdot\!\tau)-r_1,&
\widetilde w&=e^{2\pi i\widetilde z},&
\widetilde q&=e^{2\pi i(A\cdot\tau)}.
\end{aligned}
\]

Kopp's defining modular ratio is

\[
U_{\boldsymbol r}(\tau)
=
\frac{F(\widetilde w;\widetilde q)}
     {F(w;q)}.
\]

For the canonical level stabilizer \(A_d\equiv I\pmod d\), this ratio is
defined at every \(d\)-grid characteristic
\(\boldsymbol r=\boldsymbol q/d\). Its RM boundary value is the
canonical Shintani--Faddeev value \(u_d(\boldsymbol q)\).

The important point for this cycle is that the formula is retained at
\(\tau\in\mathbb H\), before sending \(\tau\) to the real quadratic
fixed point.

## 2. Exact fractional edge factors

Let

\[
h=\frac1d,\qquad
s=e^{-2\pi i h},\qquad
t=q^h,\qquad
\widetilde t=\widetilde q^h.
\]

A horizontal characteristic step
\(\boldsymbol r\mapsto\boldsymbol r+h\boldsymbol e_1\) sends

\[
w\mapsto sw,\qquad
\widetilde w\mapsto s\widetilde w.
\]

A vertical step
\(\boldsymbol r\mapsto\boldsymbol r+h\boldsymbol e_2\) sends

\[
w\mapsto tw,\qquad
\widetilde w\mapsto\widetilde t\widetilde w.
\]

Consequently the exact edge transports are

\[
\begin{aligned}
H_{\boldsymbol r}
&=
\frac{U_{\boldsymbol r+h\boldsymbol e_1}}
     {U_{\boldsymbol r}}
=
\frac{F(s\widetilde w;\widetilde q)}
     {F(\widetilde w;\widetilde q)}
\frac{F(w;q)}
     {F(sw;q)},\\
V_{\boldsymbol r}
&=
\frac{U_{\boldsymbol r+h\boldsymbol e_2}}
     {U_{\boldsymbol r}}
=
\frac{F(\widetilde t\widetilde w;\widetilde q)}
     {F(\widetilde w;\widetilde q)}
\frac{F(w;q)}
     {F(tw;q)}.
\end{aligned}
\]

Unlike an integral vertical step, neither fractional edge has a finite
factor \(1-w\). Each introduces a new infinite-product value.

## 3. Closed-cell elimination is pure-gauge flatness

The four denominator \(q\)-products at a fractional cell are

\[
F(w),\quad F(sw),\quad F(tw),\quad F(stw).
\]

Following the two paths from \(w\) to \(stw\) gives

\[
\frac{F(sw)}{F(w)}
\frac{F(stw)}{F(sw)}
=
\frac{F(stw)}{F(w)}
=
\frac{F(tw)}{F(w)}
\frac{F(stw)}{F(tw)}.
\]

The numerator products obey the identical equation with
\((w,q,t)\) replaced by
\((\widetilde w,\widetilde q,\widetilde t)\). Hence

\[
\boxed{
H_{\boldsymbol r}
V_{\boldsymbol r+h\boldsymbol e_1}
=
V_{\boldsymbol r}
H_{\boldsymbol r+h\boldsymbol e_2}.
}
\]

This is not a special \(q\)-Pochhammer identity. If \(c(v)\) is any
nonzero function on the vertices and

\[
H(v)=\frac{c(v+\boldsymbol e_1)}{c(v)},
\qquad
V(v)=\frac{c(v+\boldsymbol e_2)}{c(v)},
\]

the same equation holds by cancellation. Conversely, on a simply
connected grid every flat multiplicative edge field is locally of this
form. Closed-cell elimination therefore imposes no constraint on the
vertex potential.

## 4. The deformation gate

In dimension four the cycle-9 perturbation assigns

\[
\left(1,x,1,x^{-1},y,y^{-1}\right)
\]

to the six Zauner orbits.

For every one of the sixteen elementary cells, write the perturbation
exponents at the vertices as

\[
E_{00},E_{10},E_{01},E_{11}\in\mathbb Z^2.
\]

The edge-holonomy defect is

\[
(E_{10}-E_{00})+(E_{11}-E_{10})
-(E_{01}-E_{00})-(E_{11}-E_{01})=(0,0).
\]

This vanishes identically, independently of the chosen exponents.
The executable audit verifies it on all sixteen cells. Therefore:

\[
\boxed{\text{Closed-cell flatness does not reject the deformation.}}
\]

It fails the necessary specificity gate before any TCC calculation is
attempted.

## 5. The first scalar Hirota candidate

The natural next attempt is a rank-one bilinear equation

\[
F(w)F(stw)=F(sw)F(tw).
\]

This is no longer a tautology. For the perturbation, the exponent defect
at a cell is

\[
\Delta E
=
E_{00}+E_{11}-E_{10}-E_{01}.
\]

The dimension-four audit finds

\[
\Delta E\ne(0,0)
\]

on every one of the sixteen cells. Thus this candidate passes the
deformation gate.

It fails the analytic gate. Euler's identity begins

\[
F(w;q)
=
1-\frac{w}{1-q}+O(w^2).
\]

Therefore

\[
\begin{aligned}
F(w)F(stw)-F(sw)F(tw)
&=
\frac{-1-st+s+t}{1-q}w+O(w^2)\\
&=
-\frac{(1-s)(1-t)}{1-q}w+O(w^2).
\end{aligned}
\]

For a fractional cell \(s\ne1\) and \(t\ne1\), so the coefficient is
nonzero. The proposed bilinear equation is not an identity of the
analytic \(q\)-Pochhammer function.

The obstruction also applies directly to the modular ratio \(U\). Away
from an RM fixed point, \(w\) and \(\widetilde w\) are locally
independent because

\[
\det
\begin{pmatrix}
-1&\tau\\
-1&A\cdot\tau
\end{pmatrix}
=\tau-A\cdot\tau\ne0.
\]

In the bilinear determinant of \(U\), the coefficient linear in
\(\widetilde w\) is

\[
-\frac{(1-s)(1-\widetilde t)}{1-\widetilde q},
\]

while the coefficient linear in \(w\) is

\[
\frac{(1-s)(1-t)}{1-q}.
\]

Neither vanishes generically. Hence there is no upper-half-plane scalar
Hirota identity whose RM specialization was merely overlooked.

## 6. Iterating \(d\) fractional steps

One might hope that a \(d\times d\) block activates the elementary
recursion after the intermediate products have been eliminated.
The exact products show what actually happens.

For horizontal shifts,

\[
\prod_{j=0}^{d-1}F(s^jw;q)
=
F(w^d;q^d).
\]

For vertical shifts,

\[
\prod_{j=0}^{d-1}F(t^jw;q)
=
F(w;q^{1/d}).
\]

Thus product elimination changes the modular parameter to \(d\tau\) or
\(\tau/d\). These are external-level values, not a closed relation
among the original \(d^2\) RM values.

Following a single function through a complete horizontal circuit gives

\[
F(e^{2\pi i(z-1)};q)=F(e^{2\pi iz};q).
\]

Following it through a complete vertical circuit gives the ordinary
recursion

\[
F(wq;q)=\frac{F(w;q)}{1-w}.
\]

For the modular ratio this becomes

\[
\frac{U_{\boldsymbol r+\boldsymbol e_2}(\tau)}
     {U_{\boldsymbol r}(\tau)}
=
\frac{1-w}{1-\widetilde w}.
\]

At the RM fixed point \(\widetilde w=w\), so the factor becomes one
outside the known exceptional characteristics. This is precisely
pseudolattice invariance, not a new exchange equation.

The block calculation therefore returns to the periodicity and
level-raising identities already audited in cycle 9.

## 7. Why the quantum \(Y\)-system does not descend

Faddeev's quantum-dilogarithm \(Y\)-system contains the desired addition:

\[
X_iX_{i+2}=1+qX_{i+1}.
\]

But its derivation starts with a Weyl pair

\[
UV=q^2VU
\]

and treats the \(X_i\) as noncommuting operators. The pentagon identity
is an operator identity; the addition is created by the Weyl algebra and
Fourier conjugation.

The scalar characteristic samples \(U_{\boldsymbol r}(\tau)\) commute.
The fractional edge construction supplies no canonical Weyl partner and
no operator trace or matrix element turning the noncommutative
\(Y\)-system into a finite \(d^2\)-term scalar identity.

This agrees with cycles 5 and 6: using the operator pentagon requires a
new RM localization theorem, not a formal substitution of scalar
special values.

## 8. The only remaining escape from the no-go result

At an RM point,

\[
A\cdot\beta=\beta,
\]

so \(w\) and \(\widetilde w\) coalesce while the individual
\(q\)-products become singular boundary objects. The RM value is a
ratio of their asymptotic multipliers, not a quotient of two convergent
identical products.

Kopp's asymptotic description has the form

\[
\varpi_{\boldsymbol r}(\tau(t))
=
u_{\boldsymbol r}^{\,t}
\left(f_{\boldsymbol r}(t)+o(1)\right),
\qquad
f_{\boldsymbol r}(t+1)=f_{\boldsymbol r}(t).
\]

Ordinary cell elimination controls only exact endpoint ratios before
this singular limit. It does not control the periodic amplitudes
\(f_{\boldsymbol r}\), their relative Stokes constants, or cancellations
between different characteristics.

Accordingly, a boundary-only additive identity is not logically ruled
out. Proving one would require new information such as:

1. a uniform vector-valued RM asymptotic for all \(d^2\)
   characteristics;
2. an explicit transfer or Stokes matrix relating neighboring
   amplitudes;
3. a finite-rank invariant of that matrix whose Fourier projection is
   the TCC coefficient.

Without one of these ingredients, taking the RM limit of cell flatness
cannot manufacture an additive equation.

## 9. Decision and next direction

\[
\boxed{\text{Close ordinary scalar fractional-cell elimination.}}
\]

This closes a method, not the possibility of an analytic TCC theorem.
The recommended next cycle is:

> Treat the \(d^2\) RM values as Floquet multipliers of a
> vector-valued boundary asymptotic problem and search for a finite
> transfer/Stokes relation whose determinant or Fourier invariant
> rejects the cycle-9 deformation.

The first gate remains unchanged: any proposed boundary relation must
fail on the formal unit orbit before it is tested against TCC.

Theta/Fay addition formulas are a lower-priority route. In the available
normalization they first control products
\(u(\boldsymbol r)u(-\boldsymbol r)\), on which the perturbation cancels.
They need an additional unsquared phase-sensitive input to pass the
same gate.

## Executable checks

Cycle 10 adds:

- `q_pochhammer_fractional_cell_determinant_coefficient()`;
- `canonical_dimension_four_fractional_cell_record()`.

The tests verify:

- all sixteen formal cell holonomies vanish;
- flatness does not reject the deformation;
- the bilinear determinant rejects the deformation on every cell;
- the first \(q\)-Pochhammer coefficient of that determinant is
  nonzero;
- neither candidate passes both the analytic and specificity gates.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  the modular ratio of \(q\)-Pochhammer symbols, its characteristic
  recursion, and the RM asymptotic with a periodic amplitude.
- Faddeev,
  [arXiv:1201.6464](https://arxiv.org/abs/1201.6464):
  the Weyl-pair hypothesis, quantum \(A_2\) \(Y\)-system, and operator
  pentagon for the modular quantum dilogarithm.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the canonical RM characteristic array and the separate additive TCC
  requirement.
