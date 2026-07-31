# Census-paper preregistration amendment v1: trace-descent synthesis

Frozen: 2026-07-31 UTC, after the compositum-free recurrence was
proposed and before using it on any census row.

## Superseded policy

The degree-32 absolute-compositum cap in
`data/census-paper-preregistration-v1.json` remains part of the
historical record but no longer controls packet-polynomial synthesis.
It is superseded only by this staged gate; the old policy is not
rewritten.

No full Q-stratum polynomial run is authorized until a versioned
coefficient-height cap has been calibrated and frozen from the
predeclared height predictor.  The present amendment authorizes the
algebraic implementation, anchor validation, benchmark, and height
calibration only.

## Exact trace-descent recurrence

Let \(v_i\) be a norm-one relative unit in a quadratic extension
\(L_i/K\), after applying the exact nonnegative integer exponent
belonging to the denominator-cleared Engine-A formula.  Then
\[
 t_i=v_i+v_i^{-1}=\operatorname{Tr}_{L_i/K}(v_i)\in K.
\]
Starting with \(P_0(Z)=Z-1\), define
\[
 P_i(X)=\operatorname{Res}_Z
 \left(P_{i-1}(Z),\,X^2-t_iXZ+Z^2\right).
\]
The roots of \(P_i\) are exactly the sign products
\(\prod_{j\le i}v_j^{\pm1}\), counted with multiplicity.  Every
coefficient lies in \(K\), so no compositum of the \(L_i\) is
constructed.  For \(i\ge1\), inversion-stability gives a reciprocal
polynomial.

The implementation must obtain the sign of every trace from the
shared Engine-A place convention.  It may not hardcode a numerical
root.  In PARI's ordering for the frozen source modulus
`[finite_ideal,[1,0]]`, the convention module must explicitly relate
the ramified real-place flag to the complementary split real place.

## Denominator-clearing correction

If the Engine-A exponents have common denominator \(q\), the recurrence
above constructs the orbit polynomial for \(X_A^q\), not automatically
for \(X_A\).  This distinction is mandatory.

- When \(q=1\), the synthesized polynomial is the packet-orbit
  polynomial.
- When \(q>1\), form \(P_N(X^q)\), factor it exactly over \(K\), and
  require a separate exact lift gate using positivity at the selected
  split embedding and the frozen Artin labels.
- A factor may be called the packet polynomial only after the lift
  gate passes.
- A packet polynomial may be called minimal only after exact
  irreducibility and full orbit-cardinality checks.  The raw
  resultant is otherwise an exact sign-orbit polynomial, possibly
  with repeated roots.

The dimension-eight anchor is a mandatory nontrivial lift control:
both relative indices are two, the cleared-power traces are
\(2y\) and \(8y+6\) for \(y^2-y-1=0\), and \(q=2\).  The exact
positive factor selected from \(P_2(X^2)\) must contain the
independently archived value \(7.3889768541\) as a numerical
cross-check.  That decimal may validate the selected factor but may
not choose it.

## Complexity and claim boundary

The recurrence has output-linear degree growth: the degree doubles at
each trace.  This does not by itself prove linear bit complexity.
Coefficient arithmetic and factor lifting depend on coefficient
height and on \(q\).  Runtime and memory ratios are therefore tagged
`OBSERVED`; the algebraic recurrence and coefficient-field statement
are tagged `PROVED` once their exact tests and written proof pass.

The final feasibility cap will be expressed in coefficient-height
terms, calibrated before the corpus run from the frozen
\(\sum_\chi L'(0,\chi)\) predictor.  Rows over that cap remain explicit
resource-frontier rows; none may be silently dropped.

## Gates

1. conventions module fixes and tests the selected split embedding;
2. recurrence replays by exact brute-force resultants for small
   \(N\);
3. dimension-eight \(q=2\) lift passes exact factorization,
   positivity, reciprocity, irreducibility, and archived-value
   containment checks;
4. benchmark preserves the old-route stack failure and reports
   runtime/peak-memory observations without promoting them to a
   complexity theorem;
5. coefficient-height predictor is calibrated and a numeric cap is
   frozen in a versioned successor before any full Q-stratum run.
