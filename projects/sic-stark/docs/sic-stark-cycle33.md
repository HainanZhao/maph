# SIC--Stark research cycle 33: the cyclic full-table route closes

Date: 2026-07-27

## Outcome

The cyclic-quantum-dilogarithm experiment still gives a strong numerical
and convention check for the positive identity-class factor in dimension
six.  It does **not**, with presently published formulas, give the
oriented characteristic packet or a finite twisted-convolution identity.

The proposed characteristic-dependent boundary renormalization in cycle
32 was based on an invalid extrapolation.  Correcting it closes that route
and returns the proof target to the single oriented order-six regulator
identity isolated in cycle 27:

\[
 L'_S(0,\chi_1)
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2.
\]

## 1. What remains valid

For

\[
 \beta=\frac{5+\sqrt{21}}2,\qquad
 T_{n+1}=5T_n-T_{n-1},\qquad
 t_n=\frac{T_{n-1}}{T_n},
\]

Yalkinoglu's announced formula specializes to an absolute-value limit of
finite cyclic quantum dilogarithms.  The executable values converge to
the reciprocal positive identity-class overlap:

\[
 0.451898708435006
 \quad\hbox{versus}\quad
 x^{-1}=0.451898706617609.
\]

This remains useful independent evidence for the selected reciprocal
double-sine convention and the positive root.  It is not an algebraicity
proof.

## 2. The exact domain error

Kopp proves a cyclic-dilogarithm formula for the rational **Jacobi**
cocycle under a restriction avoiding its branch points.  He then states
explicitly that evaluation of the modular cocycle with characteristics
at rational \(\tau\) is subtler because cyclic factors can vanish, and
defers the details.

Cycle 32 formally inserted a level-six characteristic into that Jacobi
formula and assigned a common imaginary regulator to the zero factors.
The resulting exponents include, for example,

\[
 \frac{72}{58075},\qquad
 \frac{144}{58075},\qquad
 \frac{216}{58075}.
\]

These cannot be orders of zeros or poles of a meromorphic function:
meromorphic orders are integers.  The fractional numbers diagnose the
missing branch-locus asymptotics in the excluded specialization.  They
are not valuations of
\(\operatorname{shin}^{\boldsymbol r}_A(\tau)\).

Consequently:

- the proposed characteristic-wise leading coefficients were undefined;
- the associated tropical minimum test had no mathematical TCC meaning;
- no conclusion may be drawn from its apparently balanced subsequences.

The revised executable audit retains those fractions only as a
reproducible contradiction proving that the formal substitution is
invalid.

## 3. Why the scalar theorem does not repair the packet

Yalkinoglu's Theorems 3.1--3.2 are stated with absolute values and the
paper is an announcement whose complete proofs are deferred.  In the
specialized principal-ideal form used here, the formula approximates the
identity-class Shintani invariant.  It does not provide all thirty-six
level-six characteristic values with their AFK phases and Artin labels.

Even accepting the announced scalar limit, a sequence of algebraic cyclic
products may converge to a transcendental number.  Thus the limit does
not prove that the identity-class value is the certified ray unit, and it
does not prove the complex primitive-character equality.

## 4. A failed stronger finite test

For diagnosis only, principal-branch leading coefficients were assembled
from the excluded formal substitution and inserted into

\[
 \sum_{\boldsymbol q}
 \omega_6^{\langle\boldsymbol p,(I+L)\boldsymbol q\rangle}
 \frac{C_n(\boldsymbol q)}
      {C_n(\boldsymbol q-\boldsymbol p)}.
\]

They did not vanish at finite level.  More importantly, because the
\(C_n\) themselves came from the invalid fractional-order prescription,
even the observed decrease of residuals along later convergents has no
proof value.  The diagnostic code was therefore removed rather than
retained as a misleading experiment.

## 5. Correct recommendation

Do not attempt another full characteristic table from the currently
published rational cyclic formula.  That calculation requires the
branch-locus theorem that Kopp explicitly leaves for later work.

There are now three honest options:

1. prove the missing rational-characteristic asymptotic, including the
   \(R(w^n,t)\) terms at \(w^n=1\), and only then revisit a cyclic TCC
   limit;
2. prove the single modulus-six oriented Shintani regulator identity
   directly from the period-one cone; or
3. state dimension six conditionally and move the unconditional program
   to a packet whose characters are quadratic.

Option 1 is broader than dimension six and essentially develops a missing
piece of the source theory.  For closing dimension six, option 2 remains
the narrowest valid target.

## Reproducibility

- `scripts/explore_dimension_six_cyclic_dilog.py`
- `scripts/dimension_six_primitive_fourier_audit.gp`
- `scripts/analyze_dimension_six_orientation_obstruction.py`

## Primary sources

- B. Yalkinoglu, *Shintani's invariant via cyclic quantum
  dilogarithm*, arXiv:2508.18320 (2025).
- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units
  from \(q\)-Pochhammer ratios*, arXiv:2411.06763.
