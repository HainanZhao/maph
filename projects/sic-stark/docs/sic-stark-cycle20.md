# SIC--Stark research cycle 20: the quarter-period boundary

Date: 2026-07-27

## Outcome

The dimension-four quarter-period identity has been traced to a
ray-class arithmetic source, but not proved.

> **Cycle-21 clarification.** The ray modulus is \((4)\).  Its ray
> field has the correct degree for \(x^2\), the Stark invariant.  The
> cocycle value \(x\) is its square root and therefore has twice that
> relative degree.

It is not a consequence of the ordinary shift and reflection equations
for the double sine.  The three arguments

\[
\frac14,\qquad \frac{\beta}{4},\qquad \frac{\beta+1}{4},
\qquad \beta=\frac{3+\sqrt5}{2},
\]

form a quarter-period real-multiplication orbit.  Their quotient is a
Shintani ray-class invariant.  Evaluating it algebraically is therefore
the substantive Stark/Shintani step, rather than a residual special
function simplification.

The bounded dimension-four route has reached a useful theorem boundary:

> Dimension-four TCC follows from one explicit modulus-four
> Shintani invariant evaluation.

No unconditional evaluation of precisely this invariant was found in
the checked sources.

## 1. Exact algebraic target

Cycle 19 reduced all ghost minors to

\[
x+x^{-1}=t,\qquad t=\sqrt{3+\sqrt5}.
\]

Eliminating the radicals gives

\[
(t^2-3)^2=5
\]

and hence

\[
\boxed{x^8-2x^6-2x^4-2x^2+1=0.}
\]

Conversely, the double-sine integral gives \(x>1\).  Among the real
roots of this reciprocal polynomial, that branch is

\[
x=
\frac{
\sqrt{3+\sqrt5}
+
\sqrt{\sqrt5-1}
}{2}
=1.700015776\ldots .
\]

Thus an alternative exact proof target is:

1. prove that the modulus-four Stark invariant \(x^2\) is algebraic;
2. prove its minimal polynomial divides
   \(X^8-2X^6-2X^4-2X^2+1\);
3. use positivity and \(x>1\) to select the displayed root.

This formulation avoids any numerical root recognition in the final
argument.

## 2. What Shintani's theory supplies

Shintani's Kronecker-limit formula expresses derivatives of partial
zeta functions for real quadratic ray classes using products of Barnes
double gamma functions.  The associated double-sine quotients are the
ray-class invariants relevant here.

The later paper on ray-class invariants develops their class-field
interpretation, but this does not by itself evaluate every division
value as an explicit radical.  Modern work on basic double-sine special
values likewise treats algebraicity as a genuine arithmetic question.

Consequently, citing the general Kronecker-limit formula would identify
the invariant but would not prove the polynomial above.  Doing so would
silently assume the difficult step.

## 3. Status of the dimension-four proof

Proved exactly:

- the entire dimension-four TCC system is divisible by
  \(x^2-\sqrt{3+\sqrt5}x+1\);
- the required value is equivalently the positive \(>1\) root of
  \(X^8-2X^6-2X^4-2X^2+1\);
- the square of the remaining quotient is a modulus-four Stark
  ray-class invariant; the quotient itself is its cocycle square root,
  not a generic double-sine division value.

Numerically checked:

- the defining double-sine integral selects the predicted real root to
  the accuracy of the independent quadrature in cycle 19.

Not proved:

- algebraicity of this exact quotient with the asserted polynomial;
- the corresponding dimension-four TCC without that input;
- general TCC.

## 4. Recommendation

The generic functional-equation route should stop here: it has reached
a real arithmetic obstruction, and further rearrangements of shift and
reflection identities are unlikely to add information.

The project itself is not at a dead end.  The productive next route is
a finite modulus-four class-field computation:

1. enumerate the narrow ray classes of
   \(\mathbb Q(\sqrt5)\) for the exact modulus induced by the three
   quarter characteristics;
2. express the quotient as a difference of partial-zeta derivatives;
3. compute the predicted Artin orbit and norm relations;
4. derive the degree-eight class polynomial exactly;
5. identify it with
   \(X^8-2X^6-2X^4-2X^2+1\).

If this class polynomial cannot be derived without invoking an
unproved Stark algebraicity statement, dimension four should be
reported as a clean conditional theorem rather than presented as an
unconditional proof.

## Sources

- T. Shintani, *On a Kronecker limit formula for real quadratic
  fields*, J. Fac. Sci. Univ. Tokyo 24 (1977), 167--199.
- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, [JMSJ 30 (1978), 139--167](https://doi.org/10.2969/jmsj/03010139).
- N. Kurokawa and M. Wakayama, *Algebraicity and transcendency of
  basic special values of Shintani's double sine functions*,
  [DOI:10.1017/S0013091504001579](https://doi.org/10.1017/S0013091504001579).
- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
