# SIC--Stark research cycle 61: the dimension-eight cone pilot

## Outcome

The direct Shintani-cone route does **not** close the two remaining
dimension-eight identities with currently proved inputs.  It gives an exact,
oriented formula for the analytic side, but it does not identify that
complex Fourier resolvent with the logarithmic resolvent of either explicit
quartic unit.

This is useful negative progress: the obstruction is no longer an omitted
continued-fraction calculation.  It is precisely an oriented cyclic-quartic
rank-one Stark identity.

## What Kopp's theorem gives exactly

For every relevant order-ray class \(\mathfrak A\), Kopp's Theorem 1.1 gives

\[
 \exp\!\left(n_{\mathfrak A}
 Z'_{\mathfrak m\infty_2}(0,\mathfrak A)\right)
 =
 (\psi^{-2}\chi_{\boldsymbol r}^{-1})(A_{\mathfrak A})
 \operatorname{shin}^{\boldsymbol r}_{A_{\mathfrak A}}(\beta)^2.
\]

The right side is positive real.  The proof expands the partial-zeta
difference into Shintani cones and telescopes their double-sine terms.
Consequently, carrying out those cone expansions explicitly would reproduce
the real numbers \(Z'(0,\mathfrak A)\), including their signs and
normalizations.

For an odd quartic ray character \(\chi\), the complex derivative is the
finite Fourier transform of these real differences:

\[
 L'_S(0,\chi)
 =
 \frac12
 \sum_{\mathfrak A}
 \overline{\chi(\mathfrak A)}
 Z'_{\mathfrak m\infty_2}(0,\mathfrak A),
\]

up to the harmless choice of using \(\chi\) or \(\bar\chi\) as the labeled
generator.  Substituting Kopp's formula is therefore exact, but it remains a
complex linear combination, with coefficients in
\(\{1,-1,i,-i\}\), of logarithms of positive cocycle values.

Kopp's limit formula thus removes the local double-sine sign ambiguity.  It
does not turn this quartic Fourier transform into the logarithmic resolvent
of a known algebraic unit.

Source: G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
\(q\)-Pochhammer ratios*, Theorem 1.1 and the cone-telescoping proof,
<https://arxiv.org/abs/2411.06763>.

## The two explicit phase quotients

Let

\[
\begin{aligned}
R_0&=\log|\eta_0|_{\rho_3}
     +i\log|\eta_0|_{\rho_4},\\
R_1&=\log|\eta_1|_{\rho_2}
     +i\log|\eta_1|_{\rho_1},
\end{aligned}
\]

and define

\[
q_0=\frac{L'_S(0,[1,0,0])}{R_0},
\qquad
q_1=\frac{L'_S(0,[1,1,0])}{R_1}.
\]

The exact class-field and unit computation proves:

- the two quotient extensions are cyclic quartic;
- the candidate anti-units have the required norm identity;
- their conjugates generate index \(4\) in the anti-unit lattice; and
- Roblot's theorem gives \(|q_0|=|q_1|=1\).

At 100-digit precision the audit finds

\[
q_0=1+O(10^{-114}),\qquad q_1=1+O(10^{-114}).
\]

This is excellent evidence for the desired orientation.  It is not an exact
proof: the available theorem does not say that \(q_j\) is algebraic, a root
of unity, or even a member of a discrete set.

The updated certificate prints this distinction explicitly:

```text
PHASE_QUOTIENT_UNIT_MODULUS_CERTIFIED=1
PHASE_QUOTIENT_NUMERICALLY_ONE=1
PHASE_QUOTIENT_ALGEBRAICITY_ESTABLISHED=0
ORIENTED_QUARTIC_STARK_IDENTITIES_UNCONDITIONAL=0
```

## Why the finite TCC orientation cannot finish the argument

The exact finite TCC equations select one of the \(64\) natural algebraic
orientation pairs.  Roblot's uniqueness theorem also makes the possible
unit resolvents discrete up to \(\{\pm1,\pm i\}\) and conjugation.

Neither statement places the *analytic* value \(L'_S(0,\chi)\) in that
discrete orbit.  From the proved equality of absolute values alone, its
quotient with the selected unit resolvent may be any point of the unit
circle.  Using TCC to assert that it is the selected point would assume the
analytic-to-algebraic identification that TCC needs.

Roblot explicitly retains absolute values in the analytic conclusion of
Theorem 6.1; see X.-F. Roblot, *Index formulae for Stark units and their
solutions*:
<https://math.univ-lyon1.fr/~roblot/resources/index.pdf>.

## Precise theorem boundary

Dimension eight will become unconditional if either of the following is
proved for these two explicit characters:

1. the oriented identities \(q_0=q_1=1\); or
2. a powered-algebraicity theorem that places the convention-matched
   Shintani--Faddeev values in the computed ray field.

A complete expansion into individual cones does not by itself supply either
input; Kopp's proof already performs that telescoping in general.  Further
work should therefore target the algebraicity/orientation theorem, not
repeat the cone evaluation at greater length.

## Research decision

The best next move is to treat dimension six as the primary theorem-design
laboratory while retaining dimension eight as the sharp index-four test
case.  Dimension six already exposes the need for a general analytic
descent theorem, whereas further dimension-eight numerical expansion would
only add digits to \(q_0\) and \(q_1\).

The reusable target is:

> prove a convention-matched powered-algebraicity or oriented reciprocity
> theorem for Shintani--Faddeev values beyond Shintani index two.

Such a theorem would close the current dimension-eight packet immediately
and would address the obstruction that recurs in higher dimensions.

## Reproduction

```bash
gp -q scripts/dimension_eight_quartic_bridge.gp
```
