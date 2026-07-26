# SIC--Stark research sprint 1: isolate the actual target

Date: 2026-07-26

## Outcome

The most efficient first target is a restricted canonical form of the
Twisted Convolution Conjecture (TCC), not the full Stark conjecture and not
the full TCC as stated for every admissible tuple.

The source audit also exposed two convention hazards that are now covered by
tests:

1. in even dimension, displacement operators are periodic modulo \(d\)
   only up to signs, which is why the source paper works modulo
   \(\bar d=2d\);
2. the coefficient of \(D_{\boldsymbol p}\) in a projector expansion is
   \(\operatorname{Tr}(P D_{\boldsymbol p}^{\dagger})\), not a naively
   reduced negative-index overlap in even dimension.

## Exact dependency audit

In Appleby--Flammia--Kopp, the candidate normalized ghost overlaps have the
form

\[
 \widetilde\chi_t(\boldsymbol p)
 =
 \nu_t(\boldsymbol p)\,
 \mathfrak S^{\,d^{-1}\boldsymbol p}_{A_t}(\beta_t),
\]

where \(\nu_t\) is an explicit root-of-unity phase and
\(\mathfrak S\) is the Shintani--Faddeev modular cocycle.

The paper proves for these values:

- reality;
- reciprocal pairing
  \(\widetilde\chi_t(\boldsymbol p)
   \widetilde\chi_t(-\boldsymbol p)=1\);
- the required periodicity after combination with displacement operators.

The missing condition is idempotency of the ghost projector.  It is stated
as the TCC:

\[
\sum_{\boldsymbol q}
 \tau_d^{\,r\langle\boldsymbol p,
                 (\lambda I+F_t)\boldsymbol q\rangle}
 \mathfrak S^{d^{-1}\boldsymbol q}_{A_t^{-1}}(\beta_t)
 \mathfrak S^{d^{-1}(\boldsymbol q-\boldsymbol p)}_{A_t^{-1}}(\beta_t)
 =
 d^2\delta_{\boldsymbol p,\boldsymbol0}.
\]

The paper's Theorem `thm:ghstExist` says TCC implies that the candidate is a
ghost projector.  Theorem `thm:rayclassfieldrsicgen` adds the Minimalist
Real Multiplication Values Conjecture (itself implied by the relevant Stark
conjecture) to turn the ghost into a live \(r\)-SIC.

Thus the honest implication graph is

\[
\text{TCC}
\Longrightarrow
\text{ghost projector},
\qquad
\text{TCC}+\text{minimal RM values}
\Longrightarrow
\text{live SIC}.
\]

## Independent finite twisted-convolution reconstruction

For the convention

\[
D_{p,q}=\tau^{pq}X^pZ^q,\qquad \tau=-e^{\pi i/d},
\]

write

\[
P=\frac1d\sum_{\boldsymbol p}a_{\boldsymbol p}D_{\boldsymbol p}.
\]

The multiplication rule

\[
D_{p,q}D_{r,s}=\tau^{qr-ps}D_{p+r,q+s}
\]

reduces \(P^2=P\) to a finite twisted convolution of the coefficients.
`src/sic.py` now evaluates this equation, including the representative-wrap
signs required in even dimension.

This does not prove TCC: it independently confirms exactly what algebraic
property the special-value identity must supply and creates a small checker
for candidate coefficient tables.

## Canonical-family scope reduction

For every \(d\ge4\), take

\[
Q_d=\langle1,1-d,1\rangle,\qquad
L_d=
\begin{pmatrix}
d-1&-1\\
1&0
\end{pmatrix}.
\]

Direct calculation proves

\[
\operatorname{disc}(Q_d)
=(1-d)^2-4
=(d+1)(d-3),
\]

\[
\det L_d=1,
\qquad
L_d^2+L_d+I=dL_d.
\]

Consequently,

\[
L_d^2+L_d+I\equiv0\pmod d,
\qquad
L_d^3\equiv I\pmod d.
\]

The positive root

\[
\beta_d=\frac{d-1+\sqrt{(d+1)(d-3)}}2
\]

also satisfies \(L_d\cdot\beta_d=\beta_d\).  Thus this single uniform
family simultaneously supplies the correct real-quadratic discriminant and
an order-three Zauner-type stabilizer modulo \(d\).  These exact identities
are implemented in `src/sic_stark.py` and tested for \(4\le d\le500\);
the proof is the displayed symbolic calculation, not the finite test.

There is a further analytic simplification.  The quadratic equation gives

\[
\beta_d=d-1-\frac1{\beta_d},
\]

so its purely periodic Hirzebruch--Jung continued fraction is

\[
\beta_d=[\overline{d-1}]_-,
\qquad L_d=T^{d-1}S.
\]

It has period one for every dimension.  Since \(L_d^3\equiv I\pmod d\),
the level-\(d\) stabilizer used for rational characteristics is reached
after three copies of this same period-one step.  By the cocycle law, this
suggests that every canonical RM value can be organized as a product over
the three-element characteristic orbit

\[
\boldsymbol p,\quad L_d\boldsymbol p,\quad L_d^2\boldsymbol p
\pmod d.
\]

This is a structural reduction; the boundary values and phases still have
to be handled rigorously.  The orbit decomposition is exact:

- if \(3\nmid d\), only \(\boldsymbol0\) is fixed and all other orbits have
  length three;
- if \(3\mid d\), the fixed vectors are
  \((0,0),(d/3,d/3),(2d/3,2d/3)\), and every other orbit has length three.

Indeed, a fixed vector obeys \(p_1=p_2\) and \(3p_1=0\pmod d\).
`canonical_zauner_orbits()` verifies and exposes this decomposition.

The source data table includes this canonical form in every inspected
dimension.  Its Hirzebruch--Jung word length is uniformly minimal in the
table, making it the cheapest family on which to expand the modular
cocycle.

### Restricted target

The full TCC demands shifts \(0\) and \(1\) for every admissible tuple and
also compares tuples of equal discriminant.  Zauner existence needs much
less:

> **Canonical rank-one TCC target.** For every \(d\ge4\), prove the
> idempotency convolution for \(r=1\), the canonical form
> \(Q_d=\langle1,1-d,1\rangle\), and one shift compatible with the identity
> twist.

The source paper's twist function is

\[
f_t(\lambda)=r(2\lambda+d+d_j-1).
\]

In rank one \(r=1\), \(m=1\), and therefore \(d_j=d\).  Consequently

\[
f_t(1)=2d+1\equiv1\pmod{\bar d},
\qquad
f_t(0)=2d-1\equiv-1\pmod{\bar d}.
\]

The twist condition is
\(\det(G)f_t(\lambda)\equiv1\pmod{\bar d}\).  Hence the shift
\(\lambda=1\) is uniformly compatible with the identity twist \(G=I\);
\(\lambda=0\) is compatible with a determinant-\(-1\) twist.  This proves
that the restricted canonical target can use \(\lambda=1\) and \(G=I\) in
every dimension.

For this canonical form the paper defines

\[
F_t=\frac{d_j-1}{2}I+\frac{f_j}{f}SQ_d.
\]

Here \(d_j=d\) and the conductor \(f\) of \(Q_d\) is \(f_j\), so direct
matrix substitution gives \(F_t=L_d\).  Therefore the twist matrix appearing
in TCC is

\[
\lambda I+F_t=I+L_d
\equiv
Z_*:=
\begin{pmatrix}
0&-1\\
1&1
\end{pmatrix}
\pmod d.
\]

The matrix \(Z_*\) is independent of the dimension.

### Fully explicit restricted conjecture

Set

\[
\Delta_d=(d+1)(d-3),\qquad
\beta_d=\frac{d-1+\sqrt{\Delta_d}}2,
\]

\[
L_d=
\begin{pmatrix}d-1&-1\\1&0\end{pmatrix},
\qquad
A_d=L_d^3,
\qquad
Z_*=
\begin{pmatrix}0&-1\\1&1\end{pmatrix}.
\]

The canonical rank-one target becomes

\[
\boxed{
\sum_{\boldsymbol q\in(\mathbb Z/d\mathbb Z)^2}
\tau_d^{\langle\boldsymbol p,Z_*\boldsymbol q\rangle}
\mathfrak S^{\,\boldsymbol q/d}_{A_d^{-1}}(\beta_d)
\mathfrak S^{\,(\boldsymbol q-\boldsymbol p)/d}_{A_d^{-1}}(\beta_d)
=d^2\delta_{\boldsymbol p,\boldsymbol0}
}
\]

for every \(d\ge4\) and every
\(\boldsymbol p\in(\mathbb Z/d\mathbb Z)^2\), with the paper's specified
choice of representatives at the singular characteristics.

This is the current main research question.  The arithmetic matrices, the
quadratic point, the shift, and the twist are now all uniform and explicit.
Only the Shintani--Faddeev RM values and their convolution remain opaque.

Even the RM-values hypothesis can be weakened for mere SIC existence: the
paper notes that it suffices to have one sign-switching Galois automorphism
with the required unit-modulus property.

## Reproduced non-sporadic base case

The exact-radical \(d=4\) fiducial from Zhu--Teo--Englert,
[arXiv:1008.1138](https://arxiv.org/abs/1008.1138), is now implemented as
`dimension_four_fiducial()`.

The independent checker obtains:

- maximum SIC residual: \(1.11\times10^{-16}\);
- maximum frame residual: \(8.88\times10^{-16}\);
- maximum twisted-idempotency residual: \(2.75\times10^{-15}\).

These are floating-point reproductions of a known exact result, not a new
existence proof.

## Ranked research questions

### Q1. Can the canonical cocycle word be made uniform in \(d\)?

Because the HJ period is exactly one and the level stabilizer is \(L_d^3\),
expand
\(\mathfrak S_{A_t}\) into q-Pochhammer factors symbolically in \(d\).
Success would turn the all-dimensional TCC from a family of opaque special
values into a three-characteristic, parameterized finite-product identity.

This is the highest-priority question.

### Q2. Are the shifts \(0\) and \(1\) equivalent?

Search for an exact change of variables
\(\boldsymbol q\mapsto R\boldsymbol q+\boldsymbol c\), using reciprocal
pairing and the Zauner action, that maps one convolution to the other.
Proving equivalence would halve the analytic work and explain why the two
shifts always appear together in rank one.

### Q3. How many \(\boldsymbol p\)-orbits really require proof?

The convolution is indexed by \(d^2\) values of \(\boldsymbol p\), but
Zauner, Galois, parity, and unit actions may collapse these to divisor orbits
classified by \(\gcd(p_1,p_2,d)\).  Prove the covariance before performing
large numerical scans.

### Q4. Can idempotency propagate up a dimension tower?

For a fixed real quadratic field, the construction organizes dimensions
into towers.  Investigate norm/distribution relations of the modular
cocycle that might transfer the canonical TCC from one rung to the next.
A valid induction would be more valuable than verifying isolated
dimensions.

### Q5. Is TCC genuinely additional?

Reality and reciprocal pairing alone do not force idempotency; random
reciprocal arrays fail the executable convolution check.  The right question
is whether the *full cocycle functional equations*, including
characteristic shifts and modular covariance, already force TCC.  List
those axioms and try to construct a formal countermodel satisfying all but
TCC.  If such a countermodel exists, a genuinely new analytic identity is
required.

## Skeptical failure modes

- TCC may merely repackage the original SIC equations in special-function
  notation.
- The canonical family may simplify the quadratic form but not the real
  multiplication limit of the cocycle.
- Even a proof of canonical TCC leaves the minimal RM-values/Galois input
  conditional.
- Numerical agreement cannot distinguish a structural identity from
  high-precision coincidence.
- Even-dimensional sign conventions can manufacture false identities;
  all symbolic formulas must state whether indices live modulo \(d\) or
  \(2d\).

## Next executable sprint

1. Extract \(A_t\), \(F_t\), \(\beta_t\), the Rademacher phase, and the
   twist congruence explicitly for \(Q_d\).
2. Expand the canonical cocycle word for \(d=4,5,6\) directly from its
   q-Pochhammer definition.
3. Compare the three expansions structurally and conjecture a uniform
   parameterized identity.
