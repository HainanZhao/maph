# SIC--Stark research cycle 11: Floquet monodromy and the missing translation

Date: 2026-07-26

## Outcome

Cycle 11 treated the canonical Shintani--Faddeev values as Floquet
multipliers of Kopp's real-multiplication boundary asymptotic.

The proposed vector-valued route does not create new coupling:

1. evolution by the common level stabilizer
   \(A_d=L_d^3\) is diagonal in the characteristic basis;
2. resolving it into one \(L_d\)-step gives a weighted permutation;
3. weighted-permutation gauge invariants are only products around
   Zauner cycles;
4. the cycle-9 deformation lifts exactly to such a weighted transfer;
5. a discrete Fourier transform makes the matrix dense but only by
   conjugation, so it creates no new invariant;
6. Kopp's periodic asymptotic amplitudes are componentwise and supply no
   off-diagonal Stokes matrix.

Thus Floquet spectra and the available RM asymptotic cannot imply TCC.

The useful positive result is an exact operator reformulation. Let

\[
D_u e_{\boldsymbol q}
=u(\boldsymbol q)e_{\boldsymbol q},
\qquad
T_{\boldsymbol p}e_{\boldsymbol q}
=e_{\boldsymbol q+\boldsymbol p},
\]

and let

\[
W_{\boldsymbol p}e_{\boldsymbol q}
=
\omega_d^{\langle\boldsymbol p,(I+L_d)\boldsymbol q\rangle}
e_{\boldsymbol q}.
\]

Then the canonical residual is

\[
\boxed{
R_d(\boldsymbol p)
=
\operatorname{Tr}\!\left(
W_{\boldsymbol p}
D_uT_{\boldsymbol p}D_u^{-1}T_{\boldsymbol p}^{-1}
\right).
}
\]

Therefore the missing theorem is not a spectral identity for RM
monodromy alone. It must control the interaction of RM monodromy with an
independent Heisenberg translation.

\[
\boxed{\text{Close uncoupled Floquet/Stokes vectorization.}}
\]

The next credible target is a non-pure-gauge, rank-greater-than-one
translation connection or RM Zak-transform intertwiner whose curvature
has the displayed twisted trace.

## 1. Kopp's scalar Floquet equation

Fix a rational characteristic
\(\boldsymbol r\) and a positive stabilizer \(A\) of the real quadratic
point \(\beta\). Along Kopp's modular orbit

\[
\tau_t=A^t\cdot\omega,
\]

the defining modular relation is

\[
\varpi_{\boldsymbol r}(\tau_{t+1})
=
\operatorname{shin}_{A}^{\boldsymbol r}(\tau_t)
\varpi_{\boldsymbol r}(\tau_t).
\]

The coefficient has the RM limit

\[
\operatorname{shin}_{A}^{\boldsymbol r}(\tau_t)
\longrightarrow
u(\boldsymbol r)
=
\operatorname{shin}_{A}^{\boldsymbol r}(\beta).
\]

Kopp consequently obtains

\[
\varpi_{\boldsymbol r}(\tau_t)
=
u(\boldsymbol r)^t
\left(f_{\boldsymbol r}(t)+o(1)\right),
\qquad
f_{\boldsymbol r}(t+1)=f_{\boldsymbol r}(t).
\]

This is a scalar first-order Floquet equation. The multiplier is the RM
value itself.

## 2. The common canonical evolution is diagonal

For the canonical \(d\)-grid, take the common level stabilizer

\[
A_d=L_d^3\equiv I\pmod d.
\]

Every characteristic
\(\boldsymbol r=\boldsymbol q/d\) is fixed modulo \(\mathbb Z^2\).
Collect the \(d^2\) products into

\[
\boldsymbol P(t)
=
\left(
\varpi_{\boldsymbol q/d}(A_d^t\cdot\omega)
\right)_{\boldsymbol q}.
\]

The exact evolution is

\[
\boldsymbol P(t+1)
=
D(t)\boldsymbol P(t),
\]

where

\[
D(t)
=
\operatorname{diag}\left(
\operatorname{shin}_{A_d}^{\boldsymbol q/d}
(A_d^t\cdot\omega)
\right)_{\boldsymbol q}.
\]

Its limiting monodromy is

\[
D(t)\longrightarrow
D_u
=
\operatorname{diag}
\left(u_d(\boldsymbol q)\right)_{\boldsymbol q}.
\]

Vectorization has therefore produced a direct sum of \(d^2\) scalar
systems, not a coupled system.

The periodic amplitude vector

\[
\boldsymbol f(t)
=
\left(f_{\boldsymbol q/d}(t)\right)_{\boldsymbol q}
\]

does not change this conclusion. Kopp constructs each component from
its own normalized scalar orbit. No equation in the source relates
\(f_{\boldsymbol q/d}\) to
\(f_{\boldsymbol s/d}\) for distinct characteristics.

## 3. Resolving one \(L_d\)-step

The factorization \(A_d=L_d^3\) gives a more refined system. Put

\[
z_{\boldsymbol r}(\tau)=r_2\tau-r_1.
\]

The Jacobi transformation law has the form

\[
\varpi_{L_d\boldsymbol r}(L_d\cdot\tau)
=
\kappa_{\boldsymbol r}(\tau)
\varpi_{\boldsymbol r}(\tau),
\]

where \(\kappa_{\boldsymbol r}\) is the corresponding
Shintani--Faddeev Jacobi-cocycle factor, including the integral
characteristic correction needed when representatives are reduced
modulo \(\mathbb Z^2\).

On the finite characteristic vector this is

\[
\boldsymbol P(L_d\cdot\tau)
=
K(\tau)\boldsymbol P(\tau),
\]

where \(K(\tau)\) has exactly one nonzero entry in every row and every
column:

\[
K(\tau)e_{\boldsymbol q}
=
\kappa_{\boldsymbol q}(\tau)e_{L_d\boldsymbol q}.
\]

Thus \(K\) is a weighted permutation. Its three-step product is the
diagonal common-stabilizer transfer:

\[
K(L_d^2\cdot\tau)
K(L_d\cdot\tau)
K(\tau)
=
D(\tau).
\]

This explains the three universal \(S\)-kernels found in cycle 2, but
does not introduce addition.

## 4. Classification of weighted Zauner transfers

Let

\[
\mathcal O
=
\{\boldsymbol q_0,\ldots,\boldsymbol q_{\ell-1}\}
\]

be a Zauner orbit, with
\(\ell\in\{1,3\}\). Restrict \(K\) to this orbit and write its edge
weights as \(a_0,\ldots,a_{\ell-1}\).

A diagonal basis change rescales individual edge weights but preserves

\[
c_{\mathcal O}
=
\prod_{j=0}^{\ell-1}a_j.
\]

Conversely, choose the basis rescaling recursively around the cycle.
All but one edge weight can be set to one. Hence
\(c_{\mathcal O}\) is the complete diagonal-gauge invariant of the
block, whose characteristic polynomial is

\[
\boxed{\lambda^\ell-c_{\mathcal O}.}
\]

The entire weighted transfer is therefore classified by one
multiplicative scalar per Zauner orbit.

The number of such invariants is

\[
\begin{cases}
(d^2+2)/3,&3\nmid d,\\
(d^2+6)/3,&3\mid d.
\end{cases}
\]

This is exactly the Zauner-orbit count already governing the
characteristic array. The transfer matrix has not reduced the
multiplicative freedom.

## 5. Exact dimension-four deformation lift

For \(d=4\), the orbit degrees are

\[
\boxed{1,3,3,3,3,3.}
\]

They correspond to

\[
\begin{aligned}
&\{(0,0)\},\\
&\{(0,1),(3,0),(1,3)\},\\
&\{(0,2),(2,0),(2,2)\},\\
&\{(0,3),(1,0),(3,1)\},\\
&\{(1,1),(2,1),(1,2)\},\\
&\{(2,3),(3,2),(3,3)\}.
\end{aligned}
\]

The cycle-9 monodromy deformation assigns the orbit products

\[
\left(1,x,1,x^{-1},y,y^{-1}\right).
\]

It lifts to a weighted one-step transfer over
\(\mathbb Z[x^{\pm1},y^{\pm1}]\): on each three-cycle, assign the
desired monomial to one edge and assign one to the other two edges.
Assign one to the fixed edge at \((0,0)\).

The product around every orbit is then exactly the desired deformed
monodromy. The executable audit verifies the three-step equality at all
sixteen characteristics.

Therefore:

\[
\boxed{\text{Weighted-transfer structure does not reject the
deformation.}}
\]

Neither sparsity, three-step factorization, block degrees, determinants,
nor characteristic polynomials can supply TCC without an additional
analytic relation among different blocks.

## 6. Fourier filtering creates no new coupling

Let

\[
F(w;q)=(w;q)_\infty
=
\sum_{n\ge0}
\frac{(-1)^nq^{n(n-1)/2}}{(q;q)_n}w^n.
\]

For \(\zeta=e^{2\pi i/d}\), the discrete Fourier filter across
horizontal characteristics gives

\[
\sum_{a=0}^{d-1}
\zeta^{ak}F(\zeta^{-a}w;q)
=
d
\sum_{\substack{n\ge0\\n\equiv k\pmod d}}
\frac{(-1)^nq^{n(n-1)/2}}{(q;q)_n}w^n.
\]

This is exact and additive, but it is an invertible Fourier change of
basis. The right side consists of \(d\) independent residue-class
series; it does not vanish and is not another member of the original
finite characteristic array.

Conjugating the diagonal Floquet matrix by the Fourier matrix gives

\[
\widehat D(t)=\mathcal F D(t)\mathcal F^{-1}.
\]

Although \(\widehat D(t)\) is generally dense, it is similar to
\(D(t)\). Its spectrum, characteristic polynomial, and invariant
subspaces contain exactly the same information.

The irrational RM parameter prevents the additional finite cyclic
closure available for root-of-unity quantum dilogarithms.

## 7. There is no source Stokes matrix between characteristics

At the RM boundary, each scalar product has a periodic amplitude
\(f_{\boldsymbol r}(t)\). Calling the collection a vector does not
produce a canonical Stokes matrix:

- every component solves its own first-order multiplicative equation;
- analytic continuation of the defining products is componentwise;
- the source gives no connection with off-diagonal coefficients;
- a Fourier-conjugated diagonal matrix is a basis artifact.

A genuine Stokes mechanism capable of constraining TCC would have to be
rank greater than one before vectorization. It would need a shared
linear or noncommutative equation whose different solutions are the
characteristic components. That object is not present in the published
RM asymptotic.

Accordingly, the suggestion at the end of cycle 10 must be corrected:
the existing periodic amplitudes alone cannot furnish the needed
transfer matrix.

## 8. TCC as a twisted commutator trace

The Floquet formulation nevertheless reveals precisely what is
missing.

Work on the \(d^2\)-dimensional characteristic space with basis
\(e_{\boldsymbol q}\). Define

\[
\begin{aligned}
D_u e_{\boldsymbol q}
&=u_d(\boldsymbol q)e_{\boldsymbol q},\\
T_{\boldsymbol p}e_{\boldsymbol q}
&=e_{\boldsymbol q+\boldsymbol p},\\
W_{\boldsymbol p}e_{\boldsymbol q}
&=
\omega_d^{\langle\boldsymbol p,(I+L_d)\boldsymbol q\rangle}
e_{\boldsymbol q}.
\end{aligned}
\]

Direct calculation gives

\[
D_uT_{\boldsymbol p}D_u^{-1}T_{\boldsymbol p}^{-1}
e_{\boldsymbol q}
=
\frac{u_d(\boldsymbol q)}
     {u_d(\boldsymbol q-\boldsymbol p)}
e_{\boldsymbol q}.
\]

Taking the twisted trace,

\[
\begin{aligned}
\operatorname{Tr}\!\left(
W_{\boldsymbol p}
D_uT_{\boldsymbol p}D_u^{-1}T_{\boldsymbol p}^{-1}
\right)
&=
\sum_{\boldsymbol q}
\omega_d^{\langle\boldsymbol p,(I+L_d)\boldsymbol q\rangle}
\frac{u_d(\boldsymbol q)}
     {u_d(\boldsymbol q-\boldsymbol p)}\\
&=R_d(\boldsymbol p).
\end{aligned}
\]

Thus TCC is exactly

\[
\boxed{
\operatorname{Tr}\!\left(
W_{\boldsymbol p}
[D_u,T_{\boldsymbol p}]_{\mathrm{mult}}
\right)
=d^2\delta_{\boldsymbol p,\boldsymbol0},
}
\]

where

\[
[D,T]_{\mathrm{mult}}=DTD^{-1}T^{-1}.
\]

The zero-output identity is immediate. Primitive outputs require an
identity about the interaction of the two transports \(D_u\) and
\(T_{\boldsymbol p}\).

## 9. Why Floquet spectral data cannot force the trace

The spectrum of \(D_u\) knows the multiset of RM values but not their
placement relative to characteristic translations. TCC depends on
adjacent ratios

\[
u(\boldsymbol q)/u(\boldsymbol q-\boldsymbol p)
\]

and on the symplectic phase attached to the labeled node
\(\boldsymbol q\).

Permuting the same eigenvalues among characteristic labels preserves
the Floquet spectrum while changing the twisted commutator trace.
More strongly, the cycle-9 formal deformation lifts to the weighted
one-step transfer and has a forced nonzero primitive trace coefficient

\[
(1-i)\frac{c(0,1)}{c(0,3)}.
\]

The exact algebraic-unit specialization likewise gives four nonzero
commutator-trace packet components.

Consequently:

\[
\boxed{\text{No invariant of RM monodromy alone can imply TCC.}}
\]

The required new input must mention characteristic translation,
Heisenberg phase, or an equivalent noncommuting operation explicitly.

## 10. Decision and next direction

\[
\boxed{\text{Close uncoupled Floquet/Stokes vectorization.}}
\]

The next concrete research target is:

> Construct an RM Zak transform or rank-greater-than-one
> \(q\)-difference system in which modular transport and finite
> characteristic translation form a genuine noncommuting pair, then
> seek a trace, determinant, or curvature identity equal to the TCC
> twisted commutator trace.

Such a construction must pass three gates:

1. **analytic:** it follows from the actual Shintani--Faddeev or modular
   quantum-dilogarithm function;
2. **finite:** it closes on the \(d^2\) characteristic space without an
   uncontrolled continuous integral;
3. **specific:** it fails on the cycle-9 deformation.

Faddeev's Weyl-pair pentagon supplies the right kind of noncommutativity,
but cycles 5 and 6 showed that its published scalar/integral form does
not localize to the canonical finite grid. The new formulation suggests
revisiting it through a finite Zak-transform or operator-trace
intertwiner rather than through pointwise specialization.

## Executable checks

Cycle 11 adds:

- `canonical_floquet_transfer_support()`;
- `canonical_floquet_block_degrees()`;
- `canonical_floquet_commutator_trace_signature()`;
- `canonical_dimension_four_floquet_gate_record()`.

The tests verify:

- one nonzero transfer entry per source and target through \(d=30\);
- only one- and three-dimensional Zauner blocks;
- the dimension-four block degrees \(1,3,3,3,3,3\);
- the exact lift of the formal deformation to one-step edge weights;
- zero three-step monodromy defects at all sixteen nodes;
- equality of the operator trace signature and the existing TCC
  signature;
- the forced nonzero primitive trace coefficient and exact nonzero
  algebraic trace packet.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  multiplicative modular transport, stable RM values, and the scalar
  Floquet-type asymptotic with periodic amplitude.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the canonical level stabilizer, characteristic convolution, and the
  independent TCC idempotency requirement.
- Faddeev,
  [arXiv:1201.6464](https://arxiv.org/abs/1201.6464):
  the genuinely noncommuting Weyl pair and quantum \(A_2\)
  \(Y\)-system that illustrate the type of additional structure needed.
