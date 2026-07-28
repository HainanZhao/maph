# SIC--Stark research cycle 70: cyclic-dilogarithm theorem coverage

## Outcome

The newest cyclic-dilogarithm formulation of Shintani invariants does not
currently close dimension six.

Bora Yalkinoglu's announcement, *Shintani's invariant via cyclic quantum
dilogarithm* (arXiv:2508.18320, current version dated 22 March 2026),
announces a scalar limit formula for a Shintani invariant along a modular
geodesic.  In the principal-modulus specialization it has the form

\[
 X_i((u))
 =
 \lim_{n\to\infty}
 \left|
 \frac{D_{\mathfrak t_n}(1/u)}
      {D_{\mathfrak t_{n+g}}(1/u)}
 \right|.
\]

This is directly relevant to the dimension-six modulus \(u=6\), and the
project's cyclic approximants reproduce the reciprocal of the positive
primitive overlap.  However, it does not imply TCC:

- the displayed theorem retains only an absolute value;
- it concerns the identity-class scalar invariant, not all thirty-six
  oriented characteristics;
- it does not identify the order-six Artin component with the certified
  ray unit; and
- the announcement explicitly says that a complete account with proofs is
  forthcoming.

More decisively, its final Question 4.2 asks how the cyclic
quantum-dilogarithm formulation connects to Manin's real-multiplication
program.  The operator-level connection needed here is therefore not a
published corollary of that work.

## Pentagon parameter gate

Root-of-unity pentagon identities are genuine operator identities for
noncommuting quantum-torus variables.  The finite-dimensional versions
require:

1. a Weyl commutation relation at one fixed root of unity;
2. coefficient data satisfying the associated cluster mutation or Fermat
   curve constraints; and
3. a branch-compatible cyclic dilogarithm operator, not only its scalar
   absolute value.

The dimension-six boundary calculation presently has two coupled levels:
the convergent denominator \(n\) and the Weyl level \(6\).  No proved
identification has yet been made between its characteristic table and the
five operator factors in a cyclic pentagon.  Consequently, citing the
pentagon identity without that map would only rename the missing TCC
calculation.

## Sharpened research target

An operator proof must construct, for every convergent coprime to \(6\),
an explicit \(6\)-dimensional quotient or partial trace of the
root-of-unity quantum-torus representation and show that:

\[
 \text{its matrix coefficients}
 =
 \text{the corrected rational-boundary characteristic table}.
\]

Only then may the pentagon identity be used to annihilate the thirteen
nonzero Zauner-representative defects before taking the limit.

Until that parameter match is supplied, the cyclic approach is strong
structural evidence but not a proof.

## Primary sources

- B. Yalkinoglu, *Shintani's invariant via cyclic quantum dilogarithm*,
  arXiv:2508.18320.
- I. C.-H. Ip and M. Yamazaki, *Quantum Dilogarithm Identities at Root of
  Unity*, IMRN 2016, 669--695; arXiv:1412.5777.
- L. D. Faddeev and R. M. Kashaev, *Quantum Dilogarithm*, Modern Physics
  Letters A 9 (1994), 427--434; arXiv:hep-th/9310070.

