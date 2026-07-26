# SIC--Stark research cycle 12: the finite RM Zak transform

Date: 2026-07-27

## Outcome

Cycle 12 constructed the noncommuting finite transform requested at the
end of cycle 11.

Let

\[
G=(\mathbb Z/d\mathbb Z)^2,\qquad
Z=I+L_d,
\]

and define the cocycle

\[
\sigma(\boldsymbol q,\boldsymbol r)
=
\omega_d^{\langle\boldsymbol r,Z\boldsymbol q\rangle}.
\]

After the explicit chirp

\[
\begin{aligned}
F(\boldsymbol q)
&=
\omega_d^{\langle\boldsymbol q,Z\boldsymbol q\rangle}
u_d(\boldsymbol q),\\
V(\boldsymbol r)
&=
u_d(-\boldsymbol r)^{-1},
\end{aligned}
\]

the Twisted Convolution Conjecture is exactly

\[
\boxed{
F*_\sigma V=d^2\delta_{\boldsymbol0}.
}
\]

The alternating bicharacter of \(\sigma\) is

\[
\sigma(\boldsymbol q,\boldsymbol r)
\sigma(\boldsymbol r,\boldsymbol q)^{-1}
=
\omega_d^{-\langle\boldsymbol q,\boldsymbol r\rangle},
\]

which is nondegenerate. Consequently the twisted group algebra
\(\mathbb C^\sigma[G]\) is a full matrix algebra \(M_d(\mathbb C)\).

Cycle 12 gives an explicit realization valid for every parity:

\[
\boxed{
\rho(a,b)
=
\tau_d^{a^2+b^2}X^aZ_0^{-b},
\qquad
\tau_d=-e^{\pi i/d},\quad \tau_d^2=\omega_d.
}
\]

Here \(X e_j=e_{j+1}\) and
\(Z_0e_j=\omega_d^je_j\). It satisfies

\[
\rho(\boldsymbol q)\rho(\boldsymbol r)
=
\sigma(\boldsymbol q,\boldsymbol r)
\rho(\boldsymbol q+\boldsymbol r).
\]

Define the finite RM Zak transform

\[
\mathcal Z_\sigma(f)
=
\sum_{\boldsymbol q\in G}
f(\boldsymbol q)\rho(\boldsymbol q).
\]

Then

\[
\mathcal Z_\sigma(f*_\sigma g)
=
\mathcal Z_\sigma(f)\mathcal Z_\sigma(g),
\]

and TCC becomes the single finite matrix equation

\[
\boxed{
\mathcal Z_\sigma(F)
\mathcal Z_\sigma(V)
=
d^2I_d.
}
\]

This is an exact reformulation, not a proof of the RM identity. It is
nevertheless the first candidate in the recent cycles to pass both
structural gates:

| Gate | Result |
|---|---|
| closes on finite data | yes: two \(d\times d\) matrices |
| rejects the cycle-9 deformation | yes |
| follows for the actual RM values | still open |

The next analytic target is therefore sharply defined: factor or
identify the two RM Zak matrices using the \(q\)-Pochhammer/Jacobi
cocycle so that their product is forced to be \(d^2I_d\).

## 1. From the primitive residual to a cocycle product

The canonical TCC residual is

\[
R_d(\boldsymbol p)
=
\sum_{\boldsymbol q\in G}
\omega_d^{\langle\boldsymbol p,Z\boldsymbol q\rangle}
\frac{u_d(\boldsymbol q)}
     {u_d(\boldsymbol q-\boldsymbol p)}.
\]

Set

\[
\boldsymbol r=\boldsymbol p-\boldsymbol q.
\]

Then

\[
\boldsymbol q-\boldsymbol p=-\boldsymbol r
\]

and

\[
\begin{aligned}
\langle\boldsymbol p,Z\boldsymbol q\rangle
&=
\langle\boldsymbol q+\boldsymbol r,Z\boldsymbol q\rangle\\
&=
\langle\boldsymbol q,Z\boldsymbol q\rangle
+
\langle\boldsymbol r,Z\boldsymbol q\rangle.
\end{aligned}
\]

Define

\[
\begin{aligned}
Q(\boldsymbol q)
&=\langle\boldsymbol q,Z\boldsymbol q\rangle,\\
C(\boldsymbol q,\boldsymbol r)
&=\langle\boldsymbol r,Z\boldsymbol q\rangle,\\
F(\boldsymbol q)
&=\omega_d^{Q(\boldsymbol q)}u_d(\boldsymbol q),\\
V(\boldsymbol r)
&=u_d(-\boldsymbol r)^{-1}.
\end{aligned}
\]

The phase splits exactly as

\[
\langle\boldsymbol p,Z\boldsymbol q\rangle
=
Q(\boldsymbol q)+C(\boldsymbol q,\boldsymbol r).
\]

Hence, with

\[
(f*_\sigma g)(\boldsymbol p)
=
\sum_{\boldsymbol q+\boldsymbol r=\boldsymbol p}
\sigma(\boldsymbol q,\boldsymbol r)
f(\boldsymbol q)g(\boldsymbol r),
\]

where

\[
\sigma(\boldsymbol q,\boldsymbol r)
=
\omega_d^{C(\boldsymbol q,\boldsymbol r)},
\]

we obtain

\[
\boxed{
R_d(\boldsymbol p)
=(F*_\sigma V)(\boldsymbol p).
}
\]

Therefore all TCC equations are equivalent to

\[
F*_\sigma V=d^2\delta_{\boldsymbol0}.
\]

The executable phase audit checks this identity coefficient by
coefficient through \(d=13\).

## 2. The cocycle is associative

Because \(C\) is bilinear,

\[
\begin{aligned}
C(\boldsymbol q,\boldsymbol r)
+C(\boldsymbol q+\boldsymbol r,\boldsymbol s)
&=
C(\boldsymbol r,\boldsymbol s)
+C(\boldsymbol q,\boldsymbol r+\boldsymbol s).
\end{aligned}
\]

Exponentiating gives the cocycle identity

\[
\sigma(\boldsymbol q,\boldsymbol r)
\sigma(\boldsymbol q+\boldsymbol r,\boldsymbol s)
=
\sigma(\boldsymbol r,\boldsymbol s)
\sigma(\boldsymbol q,\boldsymbol r+\boldsymbol s).
\]

Thus \(*_\sigma\) is associative.

This matters because TCC is no longer being viewed as an isolated
Fourier sum. It is an inverse equation in a finite associative algebra.

## 3. Nondegeneracy

For the canonical family,

\[
Z\equiv
\begin{pmatrix}
0&-1\\
1&1
\end{pmatrix}
\pmod d.
\]

Write

\[
\boldsymbol q=(a,b),\qquad
\boldsymbol r=(c,e).
\]

Then

\[
C(\boldsymbol q,\boldsymbol r)
=
-ac-bc-be.
\]

Interchanging the arguments gives

\[
C(\boldsymbol q,\boldsymbol r)
-C(\boldsymbol r,\boldsymbol q)
=
ae-bc
=
-\langle\boldsymbol q,\boldsymbol r\rangle.
\]

Thus

\[
\boxed{
\sigma(\boldsymbol q,\boldsymbol r)
\sigma(\boldsymbol r,\boldsymbol q)^{-1}
=
\omega_d^{-\langle\boldsymbol q,\boldsymbol r\rangle}.
}
\]

The standard symplectic pairing on
\((\mathbb Z/d\mathbb Z)^2\) is nondegenerate for every \(d\), including
composite \(d\). Therefore the center of the twisted group algebra is
one-dimensional.

Since the algebra has dimension \(d^2\), its irreducible
Stone--von Neumann representation has dimension \(d\), and the algebra
is isomorphic to \(M_d(\mathbb C)\).

## 4. An explicit all-parity representation

Let

\[
\tau_d=-e^{\pi i/d}.
\]

Then

\[
\tau_d^2=\omega_d
\]

and the order of \(\tau_d\) is

\[
\bar d=
\begin{cases}
d,&d\text{ odd},\\
2d,&d\text{ even}.
\end{cases}
\]

On \(\mathbb C^d\), define

\[
X e_j=e_{j+1},
\qquad
Z_0e_j=\omega_d^je_j.
\]

They satisfy

\[
Z_0X=\omega_dXZ_0.
\]

For \(\boldsymbol q=(a,b)\), put

\[
\rho(\boldsymbol q)
=
\tau_d^{a^2+b^2}X^aZ_0^{-b}.
\]

If \(\boldsymbol r=(c,e)\), then

\[
\begin{aligned}
\rho(a,b)\rho(c,e)
&=
\tau_d^{a^2+b^2+c^2+e^2}
\omega_d^{-bc}
X^{a+c}Z_0^{-(b+e)}\\
&=
\omega_d^{-ac-be-bc}
\rho(a+c,b+e)\\
&=
\sigma((a,b),(c,e))
\rho((a,b)+(c,e)).
\end{aligned}
\]

The use of \(\tau_d\), rather than division by two modulo \(d\), makes
the formula valid uniformly in odd and even dimensions.

On a standard basis vector the action is especially simple:

\[
\boxed{
\rho(a,b)e_j
=
\tau_d^{a^2+b^2-2bj}e_{j+a}.
}
\]

The implementation verifies the projective multiplication law on every
basis vector for every pair of characteristics through \(d=10\).

## 5. The finite Zak/Weyl transform

Define

\[
\mathcal Z_\sigma(f)
=
\sum_{\boldsymbol q\in G}
f(\boldsymbol q)\rho(\boldsymbol q).
\]

Using the projective multiplication law,

\[
\begin{aligned}
\mathcal Z_\sigma(f)\mathcal Z_\sigma(g)
&=
\sum_{\boldsymbol q,\boldsymbol r}
f(\boldsymbol q)g(\boldsymbol r)
\sigma(\boldsymbol q,\boldsymbol r)
\rho(\boldsymbol q+\boldsymbol r)\\
&=
\mathcal Z_\sigma(f*_\sigma g).
\end{aligned}
\]

The \(d^2\) Weyl matrices \(\rho(\boldsymbol q)\) are linearly
independent. For example, fixing the displacement \(a\) and varying
\(b\) gives the \(d\) Fourier characters along one matrix diagonal.
Hence

\[
\mathcal Z_\sigma:
\mathbb C^\sigma[G]\longrightarrow M_d(\mathbb C)
\]

is an algebra isomorphism.

Applying it to TCC gives

\[
\boxed{
\mathcal Z_\sigma(F)\mathcal Z_\sigma(V)
=d^2I_d.
}
\]

Equivalently,

\[
\boxed{
\mathcal Z_\sigma(V)
=d^2\mathcal Z_\sigma(F)^{-1}.
}
\]

This is the precise finite inverse theorem that remains to be proved for
the analytic RM values.

## 6. Explicit matrix entries

Let

\[
\mathcal A=\mathcal Z_\sigma(f).
\]

From the basis action, the \((k,j)\) entry receives contributions only
from characteristics whose first coordinate is

\[
a=k-j.
\]

Therefore

\[
\boxed{
\mathcal A_{k,j}
=
\sum_{b\bmod d}
f(k-j,b)
\tau_d^{(k-j)^2+b^2-2bj}.
}
\]

Every entry is a \(d\)-term chirped finite Fourier transform along the
second characteristic coordinate. There is no continuous integral and
no external level.

Conversely, Fourier inversion along each matrix diagonal recovers every
coefficient \(f(a,b)\). This makes the transform both computationally
explicit and lossless.

For the RM array,

\[
\begin{aligned}
\mathcal A_{k,j}
&=
\sum_{b\bmod d}
\omega_d^{Q(k-j,b)}
u_d(k-j,b)
\tau_d^{(k-j)^2+b^2-2bj},\\
\mathcal B_{k,j}
&=
\sum_{b\bmod d}
u_d(j-k,-b)^{-1}
\tau_d^{(k-j)^2+b^2-2bj},
\end{aligned}
\]

with indices interpreted modulo \(d\). The target is

\[
\mathcal A\mathcal B=d^2I_d.
\]

## 7. Relation to the operator trace from cycle 11

Cycle 11 wrote each residual as

\[
R_d(\boldsymbol p)
=
\operatorname{Tr}\!\left(
W_{\boldsymbol p}
D_uT_{\boldsymbol p}D_u^{-1}T_{\boldsymbol p}^{-1}
\right).
\]

The present twisted group algebra packages all \(d^2\) such traces into
one multiplication law. The coefficient of
\(\rho(\boldsymbol p)\) in

\[
\mathcal Z_\sigma(F)\mathcal Z_\sigma(V)
\]

is exactly \(R_d(\boldsymbol p)\).

Thus the trace and Zak formulations are complementary:

- the trace formula identifies the missing noncommuting translation;
- the Zak transform realizes that noncommutativity in an irreducible
  \(d\)-dimensional matrix algebra;
- the matrix inverse equation imposes every primitive trace
  simultaneously.

## 8. The deformation gate

For \(d=4\), multiply an arbitrary genuine baseline array by the formal
orbit

\[
\left(1,x,1,x^{-1},y,y^{-1}\right).
\]

Cycles 9 and 11 prove that this preserves the published multiplicative
identities and the weighted Floquet-transfer structure.

It does not preserve the Zak inverse equation. The coefficient of
\(\rho(1,0)\), equivalently the primitive residual, contains the forced
Laurent coefficient

\[
(1-i)\frac{c(0,1)}{c(0,3)}\ne0.
\]

The exact algebraic-unit specialization also produces a nonzero
residual packet. Therefore:

\[
\boxed{\text{The finite matrix target rejects the deformation.}}
\]

This is the decisive improvement over cell flatness, distribution,
Galois packets, and uncoupled Floquet spectra.

## 9. What has and has not been proved

The following statements are now exact:

1. TCC is the twisted inverse equation
   \(F*_\sigma V=d^2\delta_0\).
2. The cocycle has nondegenerate alternating bicharacter.
3. The twisted algebra is \(M_d(\mathbb C)\).
4. The displayed \(\rho(a,b)\) realizes the cocycle for all \(d\).
5. TCC is equivalent to
   \(\mathcal Z_\sigma(F)\mathcal Z_\sigma(V)=d^2I_d\).
6. The equation fails on the formal and algebraic-unit deformations.

The following statement remains open:

\[
\mathcal Z_\sigma(F_{\rm RM})
\mathcal Z_\sigma(V_{\rm RM})
=d^2I_d.
\]

The construction is therefore a reduction and a proof architecture, not
a solution of TCC.

## 10. Next analytic experiment

The matrix formulation suggests a focused experiment:

1. retain \(\tau\in\mathbb H\) and replace the RM values by
   \[
   U_{\boldsymbol q}(\tau)
   =
   \frac{\varpi_{\boldsymbol q/d}(A_d\cdot\tau)}
        {\varpi_{\boldsymbol q/d}(\tau)};
   \]
2. form the two analytic Zak matrices
   \(\mathcal A(\tau)\) and \(\mathcal B(\tau)\);
3. use the \(d\)-term entry formula to apply root-of-unity filtering
   before taking the RM boundary limit;
4. test whether the matrices factor into explicit diagonal,
   Fourier, and \(q\)-Pochhammer transfer matrices;
5. isolate the exact boundary term that would force
   \(\mathcal A(\beta)\mathcal B(\beta)=d^2I_d\).

Any factorization must be checked against the deformation: a derivation
using only generic matrix-algebra identities will not be sufficient.

A second, related route is to combine the reflection theorem with the
transpose or adjoint action on the Weyl basis. If
\(\mathcal Z_\sigma(V)\) can be identified with a known involution of
\(\mathcal Z_\sigma(F)\), TCC becomes a finite orthogonality or
unitarity theorem for a single RM Zak matrix.

## Executable checks

Cycle 12 adds:

- `canonical_zak_cocycle_exponent()`;
- `canonical_zak_quadratic_exponent()`;
- `canonical_zak_alternating_exponent()`;
- `canonical_zak_representation_action()`;
- `canonical_zak_representation_product_defect()`;
- `canonical_zak_matrix_entry_terms()`;
- `canonical_dimension_four_zak_gate_record()`.

The tests verify:

- the alternating bicharacter equals the negative standard symplectic
  form;
- the all-parity Weyl representation has zero target and phase defects;
- the chirp/cocycle phase is exactly the original TCC phase;
- the matrix entries contain precisely \(d\) terms;
- the dimension-four cocycle is nondegenerate;
- the finite matrix target rejects the formal deformation;
- the RM matrix inverse identity is still correctly marked open.

## Primary-source anchors

- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the original twisted convolution, Weyl--Heisenberg normalization, and
  its equivalence to candidate-projector idempotency.
- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  the analytic \(q\)-Pochhammer modular ratio whose RM values provide
  the coefficients.
- Ramakrishnan--Velsamy,
  [arXiv:2305.04488](https://arxiv.org/abs/2305.04488):
  broader Weyl/Zak-transform context for twisted translates and
  biorthogonality. The finite representation used here is derived
  explicitly above and does not depend on their analytic results.
