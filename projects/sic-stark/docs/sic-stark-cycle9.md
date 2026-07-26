# SIC--Stark research cycle 9: distribution relations and multiplicative freedom

Date: 2026-07-26

## Outcome

Cycle 9 searched the published Shintani--Faddeev theory for an identity
that is both:

1. specific to the actual RM values, rather than generic Galois
   covariance; and
2. strong enough to force the primitive additive Fourier coefficient to
   vanish.

The source contains one genuinely stronger characteristic-coupling
identity: Kopp's conductor-lowering/level-raising product formula. Its
scalar specialization gives exact distribution relations inside a
composite-dimensional characteristic grid.

This identity passes the initial specificity test, but fails the
vanishing test. In dimension four it reduces to inverse-pair products
and is satisfied identically by the cycle-8 formal and algebraic-unit
models.

The stronger conclusion is baseline-independent. Given **any** nonzero
Zauner-invariant baseline array satisfying the published within-level
multiplicative identities audited here, it can be multiplied by the
cycle-8 formal unit orbit while preserving:

- inverse/reflection constants;
- fixed integral and half-integral values;
- Zauner and ray-unit covariance;
- all internal dimension-four distribution products.

Nevertheless, the resulting primitive TCC residual is a nonzero Laurent
polynomial. One coefficient is forced to be

\[
(1-i)\frac{u(0,1)}{u(0,3)}\ne0.
\]

Therefore:

\[
\boxed{\text{The published within-level multiplicative functional
equations cannot imply TCC.}}
\]

This does not rule out a new additive or exchange relation derived from
the analytic \(q\)-Pochhammer definition. It shows precisely what that
new identity must eliminate: a two-parameter multiplicative deformation
that is invisible to the existing theory.

## 1. Inventory of published identities

The source's functional-equation section gives:

| Identity | Effect on RM values | Prior status |
|---|---|---|
| cocycle law in \(A\) | relates products and powers in the stabilizer | multiplicative |
| pseudolattice invariance | integral characteristic shifts | periodicity already used |
| reflection | relates \(\boldsymbol r\) and \(-\boldsymbol r\) | inverse pairing after phase normalization |
| \(\mathrm{GL}_2(\mathbb Z)\) transformation | transports characteristic and form together | Zauner/Galois covariance |
| integral/half-integral evaluation | fixes the exceptional torsion values | multiplicative boundary data |
| conductor lowering/level raising | product over characteristic fibers | new distribution input |

The finite-difference formula for shifting the second characteristic by
an integer has a rational \(q\)-Pochhammer factor away from an RM point.
At a fixed point \(A\beta=\beta\), its numerator and denominator agree,
so it reduces to pseudolattice invariance. It supplies no fractional
grid recurrence.

The reflection theorem similarly becomes a two-term multiplicative
identity at an RM point. The samech/Stark-unit formulation squares and
normalizes this relation but does not turn it into an additive
convolution formula.

Thus the conductor-lowering theorem is the only published identity in
the source that couples more than two characteristic values in a new
way.

## 2. The conductor-lowering/level-raising theorem

Let \(B\) be an integral matrix of positive determinant \(f\), let
\(\alpha\) be fixed by \(A\), and suppose \(A\) stabilizes every
characteristic in the fiber. Kopp proves

\[
\operatorname{shin}^{\boldsymbol r}_{BAB^{-1}}(B\alpha)
=
\prod_{\substack{\boldsymbol s\in\mathbb Q^2/\mathbb Z^2\\
                  B\boldsymbol s-\boldsymbol r\in\mathbb Z^2}}
\operatorname{shin}^{\boldsymbol s}_{A}(\alpha).
\]

This follows from the exact \(q\)-Pochhammer multiplication formula. It
is not a conjectural Stark relation.

For the canonical array, take

\[
B=mI,\qquad m\mid d.
\]

Then \(B\beta_d=\beta_d\), \(B\) commutes with \(A_d\), and every
preimage lies on the \(d\)-grid. If

\[
u_d(\boldsymbol q)
=
\operatorname{shin}^{\boldsymbol q/d}_{A_d}(\beta_d),
\]

the theorem specializes to

\[
\boxed{
u_d(m\boldsymbol q)
=
\prod_{\boldsymbol k\in(\mathbb Z/m\mathbb Z)^2}
u_d\!\left(
\boldsymbol q+\frac d m\boldsymbol k
\right).
}
\]

All indices are interpreted modulo \(d\). This is the exact scalar
distribution relation sought in earlier cycles.

## 3. Prime dimensions obstruct a scalar-distribution proof

If \(d\) is prime, there is no proper divisor

\[
1<m<d.
\]

The choice \(m=d\) sends the whole characteristic grid to zero and gives
only a global product relation. It has no nontrivial coarse-grid target.

Consequently, same-array scalar distribution has no proper content in
every prime dimension \(d>3\). Since TCC is asserted independently in
those dimensions, this identity cannot by itself be a universal proof.

Level-raising with other \(B\) can link the canonical array to finer
levels, other quadratic points, or other forms. Those formulas introduce
new values. The published theory contains no additive elimination
identity that returns a fixed-level TCC Fourier coefficient.

## 4. Exact dimension-four specialization

For \(d=4\), the proper scalar divisor is \(m=2\). Multiplication by two
has four fibers, each containing four characteristics:

\[
\begin{aligned}
(0,0)&\leftarrow
\{(0,0),(0,2),(2,0),(2,2)\},\\
(0,2)&\leftarrow
\{(0,1),(0,3),(2,1),(2,3)\},\\
(2,0)&\leftarrow
\{(1,0),(1,2),(3,0),(3,2)\},\\
(2,2)&\leftarrow
\{(1,1),(1,3),(3,1),(3,3)\}.
\end{aligned}
\]

The map \(m=4\) has one sixteen-element fiber over zero.

For the cycle-8 formal unit orbit, the six Zauner-orbit values are

\[
\left(1,x,1,x^{-1},y,y^{-1}\right).
\]

Each of the four \(m=2\) fiber products equals the corresponding
coarse value \(1\), and the product over the full \(m=4\) fiber is also
\(1\). Thus every exact scalar distribution relation holds identically
in \(\mathbb Z[x^{\pm1},y^{\pm1}]\).

The algebraic-unit specialization in
\(\mathbb Q(\sqrt2,\sqrt3)\) satisfies the same equalities exactly.

## 5. Exhaustion of internal distribution maps in \(d=4\)

An endomorphism of

\[
\mathbb Z[\beta_4],\qquad
\beta_4^2=3\beta_4-1,
\]

is represented in characteristic coordinates by

\[
M_{a+b\beta_4}
=
\begin{pmatrix}
a&b\\
-b&a+3b
\end{pmatrix},
\]

with determinant

\[
N(a+b\beta_4)=a^2+3ab+b^2.
\]

For the complete torus kernel to lie in four-torsion, both Smith factors
must divide \(4\).

Modulo \(2\),

\[
a^2+3ab+b^2\equiv a^2+ab+b^2.
\]

This is even only when \(a,b\) are both even. After removing their
common divisor, the Smith-factor condition leaves:

- two times a norm-one unit;
- four times a norm-one unit.

The positive norm-one unit group is generated by \(\beta_4\). Modulo
the global-unit/Zauner action, the internal maps are therefore

\[
2I,\quad2M_{\beta_4},\quad2M_{\beta_4^2},\quad4I.
\]

Modulo four these are

\[
\begin{aligned}
&\begin{pmatrix}2&0\\0&2\end{pmatrix},\quad
\begin{pmatrix}0&2\\2&2\end{pmatrix},\quad
\begin{pmatrix}2&2\\2&0\end{pmatrix},\quad
\begin{pmatrix}0&0\\0&0\end{pmatrix}.
\end{aligned}
\]

The first three are Zauner relabelings of the same parity-fiber
relation; the last is the global product. Hence the scalar audit
exhausts all internal dimension-four distribution maps.

## 6. Multiplicative perturbation theorem

Let \(c(\boldsymbol q)\) be any nonzero Zauner-invariant baseline array
that satisfies the published within-level multiplicative identities,
including their exact root-of-unity and exceptional-value constants.

Define a perturbation \(v\), constant on Zauner orbits, by assigning

\[
\left(1,x,1,x^{-1},y,y^{-1}\right)
\]

to the six orbit representatives

\[
(0,0),(0,1),(0,2),(0,3),(1,1),(2,3).
\]

Set

\[
u'(\boldsymbol q)=c(\boldsymbol q)v(\boldsymbol q).
\]

The perturbation has the following homogeneous properties:

\[
\begin{aligned}
v(-\boldsymbol q)&=v(\boldsymbol q)^{-1},\\
v(L_4\boldsymbol q)&=v(\boldsymbol q),\\
v(\boldsymbol q)&=1
  &&\text{on the integral and half-integral fixed orbits},\\
v(2\boldsymbol q)&=
\prod_{2\boldsymbol t=2\boldsymbol q}v(\boldsymbol t),\\
v(\boldsymbol0)&=\prod_{\boldsymbol t}v(\boldsymbol t)=1.
\end{aligned}
\]

Therefore multiplying by \(v\) preserves:

- every reflection constant of \(c\);
- every exact integral or half-integral value of \(c\);
- Zauner covariance;
- every internal conductor-lowering distribution relation.

It also carries the faithful formal ray-unit action from cycle 8.

## 7. The primitive residual cannot vanish identically

Consider the primitive output

\[
\boldsymbol p=\boldsymbol e_1.
\]

Insert \(u'=cv\) into

\[
R_{\boldsymbol e_1}
=
\sum_{\boldsymbol q}
i^{-(q_1+q_2)}
\frac{u'(\boldsymbol q)}
     {u'(\boldsymbol q-\boldsymbol e_1)}.
\]

Regard the result as a Laurent polynomial in \(x,y\). The monomial
\(x^2\) receives contributions from exactly two characteristics:

\[
\boldsymbol q=(0,1),\qquad(1,3).
\]

For both terms, the baseline orbit ratio is

\[
\frac{c(0,1)}{c(0,3)}.
\]

Their phase exponents are \(3\) and \(0\), so the coefficient of \(x^2\)
is

\[
i^3\frac{c(0,1)}{c(0,3)}
+i^0\frac{c(0,1)}{c(0,3)}
=
\boxed{
(1-i)\frac{c(0,1)}{c(0,3)}
}.
\]

The baseline is nonzero, so this coefficient cannot vanish.
Consequently,

\[
\boxed{
R_{\boldsymbol e_1}(cv)
\text{ is never the zero Laurent polynomial.}
}
\]

Generic choices of the unit parameters \(x,y\) therefore give a nonzero
TCC residual while preserving the complete published package of
within-level multiplicative identities.

This argument does not require knowing a numerical or algebraic formula
for the baseline \(c\). It includes all exact phase and exceptional-value
constants carried by that baseline.

## 8. Why norm compatibility does not repair the problem

Stark norm relations and conductor lowering are multiplicative. After
taking logarithms they become additive sums over fibers, but TCC is a
Fourier sum of **exponentiated adjacent differences**:

\[
\frac{u(\boldsymbol q)}
     {u(\boldsymbol q-\boldsymbol p)}.
\]

The perturbation \(v\) lies in the kernel of the internal norm maps while
changing these adjacent ratios. Therefore norm compatibility cannot see
the deformation that changes TCC.

External level-raising relations might become useful only if combined
with a new rigidity theorem controlling the entire tower of finer-level
values. No such additive rigidity or uniqueness theorem is present in
the cited Shintani--Faddeev theory.

## 9. Decision and next direction

\[
\boxed{\text{Close the published distribution/norm-compatibility
route.}}
\]

The remaining target is now very precise:

> Find an additive or exchange identity for the analytic
> Shintani--Faddeev array that destroys the perturbation
> \((x^{-1},x,y,y^{-1})\).

The most concrete next experiment is to retain the off-grid
\(q\)-Pochhammer finite-difference factors instead of specializing
immediately to the RM fixed point. Introduce the neighboring
off-grid values required by a \(1/d\) characteristic step and attempt
to eliminate them around a closed lattice cell. A successful
elimination would produce a discrete exchange, Hirota, or \(Y\)-system
relation containing additions such as

\[
1-e^{2\pi i z},
\]

which arbitrary algebraic-unit perturbations do not satisfy.

Any candidate relation should first be checked against the perturbation
witness above. Failure on the witness is necessary before attempting a
proof that it forces TCC.

Cycle 10 performs this test and proves that ordinary scalar
fractional-cell elimination yields only deformation-invariant flatness,
while the first bilinear Hirota candidate is not a \(q\)-Pochhammer
identity. See
[`sic-stark-cycle10.md`](sic-stark-cycle10.md).

## Executable checks

Cycle 9 adds:

- `canonical_scalar_distribution_fibers()`;
- `canonical_proper_scalar_distribution_divisors()`;
- `canonical_dimension_four_internal_distribution_maps()`;
- `canonical_dimension_four_distribution_relation_record()`;
- `canonical_dimension_four_perturbation_witness()`.

The tests verify all \(m=2,4\) fibers, the internal-map classification,
the zero formal distribution defects, the exact algebraic-unit products,
the absence of proper scalar relations in prime dimensions, and the
forced nonzero \(x^2\) coefficient.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  functional equations at RM points and the exact
  conductor-lowering/level-raising theorem derived from the
  \(q\)-Pochhammer multiplication formula.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the canonical characteristic array, exceptional values, and the
  separate additive Twisted Convolution Conjecture.
