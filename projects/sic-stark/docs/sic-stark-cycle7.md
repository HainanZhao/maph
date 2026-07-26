# SIC--Stark research cycle 7: the ray-class trace obstruction

Date: 2026-07-26

## Outcome

Cycle 7 tested whether the primitive twisted-convolution coefficient can
be expressed as a character-weighted field trace of Stark-unit ratios,
with vanishing forced by ray-class Galois action and character
orthogonality.

There is a natural character-resolvent construction, but it applies to
the **whole vector of TCC residuals over output directions and quadratic
forms**, not to one fixed primitive coefficient. The fixed-direction
coefficient is a transversal through the relevant Galois orbits.

Four independent obstructions prevent the proposed proof:

1. the Stark Artin law controls normalized squared special values,
   whereas TCC uses coherently signed square roots and their ratios;
2. ray-class multiplication sends both the summation characteristic
   \(\boldsymbol q\) and output direction \(\boldsymbol p\) to new
   values;
3. the additive TCC Fourier phase is not a multiplicative ray-class
   character and does not even descend through the global-unit quotient
   when \(\boldsymbol p\) is held fixed;
4. the characteristic grid contains imprimitive ray-monoid strata, and
   the full Artin action can also change the associated quadratic form.

The first obstruction is a missing reciprocity theorem. The second and
third are exact algebraic incompatibilities, not gaps that the desired
theorem would automatically repair.

Therefore:

\[
\boxed{\text{A fixed primitive TCC coefficient is not a
character-weighted ray-class trace.}}
\]

Character orthogonality can decompose the residual vector into
isotypical components. It cannot force those components to vanish
without an additional identity equivalent in strength to TCC.

## 1. The primitive coefficient

Write the special-value array as

\[
u(\boldsymbol q)
=
\operatorname{shin}^{\boldsymbol q/d}_{A_d}(\beta_d),
\qquad
\boldsymbol q\in(\mathbb Z/d\mathbb Z)^2.
\]

After the reductions in cycles 3--5, the first primitive residual has
the form

\[
R_{\boldsymbol e_1}
=
\sum_{\boldsymbol q}
\psi_{\boldsymbol e_1}(\boldsymbol q)
\rho_{\boldsymbol e_1}(\boldsymbol q),
\]

where

\[
\rho_{\boldsymbol p}(\boldsymbol q)
=\frac{u(\boldsymbol q)}
       {u(\boldsymbol q-\boldsymbol p)}
\]

and, in the canonical convention,

\[
\psi_{\boldsymbol e_1}(\boldsymbol q)
=\omega_d^{-(q_1+q_2)}.
\]

The desired TCC equation is

\[
R_{\boldsymbol e_1}=0.
\]

The proposed trace route would need the summands, including their
Fourier weights, to be a Galois orbit of a single algebraic number.

## 2. What the Stark Artin law supplies

The source construction assigns each characteristic
\(\boldsymbol q\) a ray-monoid class \(\mathcal A_{\boldsymbol q}\).
After normalization, the square \(u(\boldsymbol q)^2\) is expressed by
a Stark class invariant attached to that class. The Stark conjecture
gives, for a primitive ray class \(\mathcal B\),

\[
\operatorname{Art}(\mathcal B)
  \bigl(\epsilon_{\mathcal A}\bigr)
=
\epsilon_{\mathcal A\mathcal B}.
\]

Consequently, the conjectural Artin action naturally permutes the
**squares** of the special values. It does not by itself determine a
coherent law

\[
\sigma_{\mathcal B}\bigl(u(\boldsymbol q)\bigr)
=
\kappa(\mathcal B,\boldsymbol q)
u(\mathcal B\boldsymbol q)
\]

for the chosen square roots. Such a law needs a sign or root-of-unity
cocycle \(\kappa\). The source paper explicitly treats the corresponding
unsquared Galois action as empirical or conditional rather than as the
proved reciprocity theorem needed here.

Even granting the strongest favorable signed law, the fixed-direction
trace still fails for the reasons below.

## 3. Exact local multiplication dictionary

Let

\[
\mathcal O_d=\mathbb Z[\beta_d],
\qquad
\beta_d^2=(d-1)\beta_d-1.
\]

Represent a residue by

\[
\alpha=a+b\beta_d\in\mathcal O_d/d\mathcal O_d.
\]

The TCC coordinate convention associates
\(\boldsymbol q=(q_1,q_2)\) with
\(q_2\beta_d-q_1\). Multiplication by \(\alpha\) is therefore represented
by

\[
\boxed{
M_\alpha=
\begin{pmatrix}
a&b\\
-b&a+(d-1)b
\end{pmatrix}
\pmod d.
}
\]

Its determinant is the residue norm:

\[
\det M_\alpha
=
N(\alpha)
=a^2+(d-1)ab+b^2
\pmod d.
\]

Thus \(\alpha\) is a local unit precisely when
\(\gcd(N(\alpha),d)=1\).

The global unit \(\beta_d\) has order three modulo \(d\):

\[
B=\langle\beta_d\rangle
=\{(1,0),(0,1),(d-1,d-1)\}.
\]

Its multiplication matrix is the inverse Zauner action modulo \(d\).
Quotienting by \(B\) is therefore exactly the global-unit/Zauner
identification expected in the ray-class description.

## 4. Artin action moves the output direction

In the most favorable fixed-form model, the squared ratio transforms as

\[
\boxed{
\sigma_\alpha
\left(\rho_{\boldsymbol p}(\boldsymbol q)^2\right)
=
\rho_{M_\alpha\boldsymbol p}
     (M_\alpha\boldsymbol q)^2,
}
\]

up to the explicit normalization and cyclotomic factors.

The action transports the difference
\(\boldsymbol q-(\boldsymbol q-\boldsymbol p)=\boldsymbol p\).
It cannot move \(\boldsymbol q\) while leaving
\(\boldsymbol p\) fixed.

For \(\boldsymbol p=\boldsymbol e_1\),

\[
M_\alpha\boldsymbol e_1=(a,-b).
\]

Hence

\[
M_\alpha\boldsymbol e_1=\boldsymbol e_1
\quad\Longleftrightarrow\quad
\alpha=1\pmod d.
\]

The stabilizer up to Zauner action is only \(B\). Therefore no
nontrivial class in the local quotient

\[
(\mathcal O_d/d\mathcal O_d)^\times/B
\]

preserves the primitive output direction.

This is the main orbit obstruction: the Galois conjugates of
\(R_{\boldsymbol e_1}\) are residuals in other directions, not the
individual summands making up \(R_{\boldsymbol e_1}\).

## 5. The Fourier phase is not a ray-class character

The TCC weight

\[
\psi_{\boldsymbol p}(\boldsymbol q)
\]

is an additive finite Fourier character in \(\boldsymbol q\).
Ray-class Galois action is multiplicative in
\(\alpha\in(\mathcal O_d/d\mathcal O_d)^\times\).

These are different group laws. A multiplicative ray-class character
\(\chi(\alpha)\) cannot simply be identified with the additive weight
\(\psi_{\boldsymbol p}(\boldsymbol q)\).

There is a sharper descent test. Since \(\beta_d\in B\) is trivial in the
ray-class quotient, a fixed-direction phase on that quotient must be
unchanged by \(\boldsymbol q\mapsto M_{\beta_d}\boldsymbol q\).
It is not.

In \(d=4\), take

\[
\boldsymbol p=\boldsymbol q=\boldsymbol e_1.
\]

Then

\[
M_{\beta_4}\boldsymbol e_1=(0,3).
\]

The exact phase exponents modulo \(4\) are

\[
\begin{aligned}
E(\boldsymbol e_1,\boldsymbol e_1)&=3,\\
E(\boldsymbol e_1,M_{\beta_4}\boldsymbol e_1)&=1,\\
E(M_{\beta_4}\boldsymbol e_1,
  M_{\beta_4}\boldsymbol e_1)&=3.
\end{aligned}
\]

Thus:

- holding the output direction fixed changes the phase, even under an
  element identified with the ray-class identity;
- moving the direction and characteristic together preserves the phase.

The phase is compatible with covariance of the whole residual vector,
not with a trace formula for one component.

## 6. Exact dimension-four quotient

For \(d=4\),

\[
\left|(\mathcal O_4/4\mathcal O_4)^\times\right|=12,
\qquad |B|=3.
\]

The four cosets are

\[
\begin{aligned}
&\{(0,1),(1,0),(3,3)\},\\
&\{(0,3),(1,1),(3,0)\},\\
&\{(1,2),(1,3),(2,3)\},\\
&\{(2,1),(3,1),(3,2)\}.
\end{aligned}
\]

Every nonidentity coset has order two, so

\[
(\mathcal O_4/4\mathcal O_4)^\times/B
\cong C_2\times C_2.
\]

A Galois orbit of a ratio has one member in each of four
output-direction Zauner orbits. A fixed-\(\boldsymbol p\) coefficient
selects one slice across such orbits; it is not one of their orbit sums.
This is already enough to rule out the proposed direct trace in the
smallest dimension.

## 7. The correct character-resolvent formulation

Let \(L/K\) be a hypothetical field containing coherently signed special
values, with abelian Galois group \(H\). For a character
\(\chi:H\to\mathbb C^\times\), define the resolvent

\[
\mathcal R_\chi(x)
=
\sum_{h\in H}\chi(h)^{-1}h(x).
\]

For the trivial character this is the ordinary field trace. For general
\(\chi\), it is the \(\chi\)-isotypical projection, up to normalization.

Applying this to a primitive residual gives

\[
\mathcal R_\chi(R_{\boldsymbol e_1})
=
\sum_{h\in H}\chi(h)^{-1}
R_{h\boldsymbol e_1}^{(hQ)},
\]

with the expected cyclotomic correction. This is a weighted sum over
conjugate directions and, in the full action, possibly conjugate forms.
It is not the original sum over \(\boldsymbol q\) at fixed
\(\boldsymbol e_1\).

Character orthogonality gives Fourier inversion:

\[
R_{\boldsymbol e_1}
=
\frac1{|H|}
\sum_{\chi\in\widehat H}\mathcal R_\chi(R_{\boldsymbol e_1})
\]

after evaluating at the identity component with the conventional
character factors. Therefore all resolvents vanish if and only if the
entire residual orbit vanishes. Orthogonality decomposes the problem; it
does not prove the needed vanishing.

## 8. Imprimitive strata and changing forms

The full characteristic array is indexed by ray-monoid classes, not a
single free ray-class orbit. Characteristics with different divisibility
data can lie in different imprimitive strata.

Moreover, the complete Artin action in the source construction is not
confined to one binary quadratic form. It can transport a special value
to a value attached to a Galois-related form. Any genuine trace formula
must therefore enlarge the state space from one canonical \(Q_d\) array
to the full packet of forms and monoid strata.

This enlargement strengthens the vector-resolvent interpretation and
weakens the prospect of a one-coefficient trace shortcut.

## 9. Decision

The proposed route would require both:

1. a signed Shimura-type reciprocity law for the unsquared
   Shintani--Faddeev RM values;
2. an independent theorem that every character resolvent of the TCC
   residual packet vanishes.

The first would be an important arithmetic theorem, but it would not
imply TCC. By Fourier inversion, the second is essentially the original
vanishing problem expressed in a different basis.

Therefore:

\[
\boxed{\text{Close the direct ray-class trace/orthogonality route.}}
\]

The useful output is the exact Galois representation target: future
work should study the complete residual packet under signed reciprocity,
not try to identify a fixed primitive coefficient with a field trace.
A promising next computational test is to determine whether that packet
satisfies an additional low-degree algebraic relation, beyond covariance,
whose isotypical projections vanish for a genuine structural reason.

## Executable checks

The following functions implement the exact local audit:

- `canonical_quadratic_residue_multiply()`;
- `canonical_quadratic_residue_norm()`;
- `canonical_residue_multiplication_matrix()`;
- `canonical_quadratic_residue_units()`;
- `canonical_global_unit_residues()`;
- `canonical_local_unit_cosets()`;
- `canonical_primitive_direction_unit_stabilizers()`;
- `canonical_dimension_four_trace_obstruction_record()`.

The tests verify the norm/determinant dictionary, the multiplication
representation, the exact and Zauner stabilizers for
\(4\le d\le100\), the \(d=4\) quotient, and the phase-descent
counterexample.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  the ray-monoid-class/characteristic correspondence, RM special values,
  and the statement that a complete Shimura-reciprocity analogue remains
  future work.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the Stark and Monoid Stark conjectures, Artin action, squared ghost
  overlaps, the empirical unsquared Galois action, and the TCC formula.
