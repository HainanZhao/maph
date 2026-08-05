# C75 idea selection: the Holevo--Utkin \(d=4\) first gate

## Question

Can the \(d=4\) conjecture be reduced completely and exactly to finitely many
one-variable inequalities, including every zero-coordinate boundary stratum,
rather than merely numerically optimizing the multiplier equations?

## Question the questioning

The source already advertises a three-value multiplier observation. Treating
that as the proof would hide the real work: non-smooth coordinates, support
loss, and the equality-family switch. A direct numerical grid is seductive
because dimension four is small, but it cannot distinguish a true global
inequality from a narrow unobserved violation. Conversely, a general
majorization claim might be too coarse because the feasible squared vectors
must admit a signed square-root partition. The discriminating question is
therefore whether the zero-sum constraint itself yields an exhaustive exact
stratification.

## Candidate engines

1. **Selected: exact KKT plus support/sign stratification.** Separate support
   sizes two, three, and four; split the nonzero coordinates into positive and
   negative groups; use the multiplier equation only inside each smooth
   stratum. For each resulting multiplicity pattern, normalize the remaining
   parameter and establish an explicit one-variable objective comparison.
   Falsifier: a rigorously enclosed point outside both candidate values.
2. **Squared-mass majorization.** Describe feasible
   \(q_i=x_i^2\) by a signed relation \(\sum\varepsilon_i\sqrt{q_i}=0\)
   and attempt a Schur-convexity/concavity comparison. Rejected for this gate:
   it might prove more, but no correct total majorization order is presently
   evident and it can conceal the phase transition.
3. **Pair-smoothing under a preserved zero-sum partition.** Average equal-sign
   or opposite-sign coordinates to monotonically improve \(F_\alpha\).
   Rejected: a smoothing direction changes from improving to worsening near
   the switch, so it needs the classification it was meant to replace.
4. **Tangent-polynomial envelope.** Seek a two- or three-contact scalar bound
   for \(t^\alpha\) which sums using the first two moments and zero-sum
   relation. Rejected initially: it is a strong second-stage route, but no
   envelope is yet known to encode the signed constraint without an unjustified
   multiplier choice.

## Chosen decision and advance condition

Prove the exhaustive reduction before attempting global signs. The advance
condition is an exact finite list of support/sign/multiplicity families, with
a normalized interval and objective formula for each. The main rejected
alternative is squared-mass majorization. If an admissible stratum cannot be
placed in that list, its explicit parametrization is the headline obstruction
and this KKT engine fails; no numerical sweep may substitute for it.

## Post-reduction continuation

The KKT question closed with one residual profile,
\[
 p(r)=\frac{((r+2)^2,1,1,r^2)}{2(r^2+2r+3)}.
\]
The two other profiles, the \(\alpha\le\tfrac12\) range, and the
\(\alpha=2\) anchor have exact proofs. Direct differentiation of this
remaining profile has extra interior stationary points; treating only
\(r=1\) and the endpoint as competitors is therefore refuted as a proof
mechanism.

Oracle and the primary agent independently retain the same C75 decision
(the global \(d=4\) comparison) but choose a new route inside its exact
one-variable comparison stage: calculate the piecewise-linear
Lorenz/stop-loss differences of \(p(r)\) against the two endpoint
distributions, and integrate their signed differences against the power
kernel. Ordinary majorization is the main rejected alternative: the
candidate switch rules out a uniform majorization order. The falsifier for
this route is a stop-loss difference with an incompatible sign-variation
pattern; that falsifies the route, not the norm conjecture. A rigorous
\((\alpha,r)\) violation of the appropriate candidate bound falsifies the
conjecture itself.
