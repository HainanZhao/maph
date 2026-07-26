# Mathematical notebook

## 1. Parallel constant-product model

For pool \(i\), let \(a_i,b_i>0\) be the reserves of input and output token,
let \(\gamma_i\in(0,1]\) be the fee multiplier, and let \(q_i\geq0\) be the
fixed cost of using the pool.  Its output curve is

\[
f_i(x)=\frac{b_i\gamma_i x}{a_i+\gamma_i x},\qquad x\geq0.
\]

It is increasing and strictly concave:

\[
f_i'(x)=\frac{a_ib_i\gamma_i}{(a_i+\gamma_i x)^2},
\qquad
f_i''(x)=
-\frac{2a_ib_i\gamma_i^2}{(a_i+\gamma_i x)^3}.
\]

For a fixed input \(Q>0\), the gas-aware routing problem is

\[
\operatorname{OPT}(Q)=
\max_{\substack{x_i\geq0\\\sum_i x_i=Q}}
\sum_i\left(f_i(x_i)-q_i\mathbf1\{x_i>0\}\right).
\tag{P}
\]

## 2. Fixed-active-set water filling

Fix a candidate set of usable pools \(S\).  Conditional on the pools that
receive positive flow, the fixed costs do not affect allocation.  The
first-order condition is a common marginal output \(\lambda>0\):

\[
f_i'(x_i)=\lambda.
\]

Therefore

\[
x_i(\lambda)=
\left[
\frac{\sqrt{a_ib_i\gamma_i/\lambda}-a_i}{\gamma_i}
\right]_+,
\tag{1}
\]

where \(\lambda\) is the unique value satisfying
\(\sum_{i\in S}x_i(\lambda)=Q\).  This gives an exact and inexpensive
continuous subproblem for every candidate active set.

The unresolved difficulty is selecting \(S\) without enumerating \(2^m\)
subsets.

## 3. Equal-price aggregation

Suppose \(\gamma_i=1\) and every pool has the same initial price
\(b_i/a_i=p\).  For any nonempty active set \(S\), write

\[
A_S=\sum_{i\in S}a_i.
\]

The fixed-set optimum allocates proportionally to input reserves:

\[
x_i=\frac{a_i}{A_S}Q.
\]

Indeed, these allocations sum to \(Q\) and give the same marginal output in
every active pool.  Their aggregate output is

\[
\sum_{i\in S}f_i(x_i)
=\frac{pQA_S}{A_S+Q}.
\tag{2}
\]

Thus (P) reduces in this special case to the subset problem

\[
\max_{\varnothing\neq S\subseteq[m]}
\left\{
\frac{pQA_S}{A_S+Q}-\sum_{i\in S}q_i
\right\}.
\tag{3}
\]

This simplification is useful both algorithmically and for complexity
analysis.

## 4. Equal-price weak NP-hardness

Define the decision problem EQUAL-PRICE-GAS-ROUTING: given positive integer
input reserves \(a_i\), rational common price \(p>0\), rational fixed costs
\(q_i\geq0\), rational input \(Q>0\), and rational threshold \(K\), decide
whether (P), restricted to \(b_i=pa_i\) and common \(\gamma_i=1\), has value
at least \(K\).

**Theorem.**  EQUAL-PRICE-GAS-ROUTING is NP-hard.

**Proof by reduction from SUBSET-SUM.**  Given positive integer weights
\(w_1,\ldots,w_m\) and target \(T>0\), construct

\[
Q=1,\qquad
p=(T+1)^2,\qquad
a_i=w_i,\qquad
b_i=pw_i,\qquad
q_i=w_i.
\]

For a subset \(S\), set \(A=A_S=\sum_{i\in S}w_i\).  Equation (3) becomes

\[
G(A)=\frac{(T+1)^2A}{A+1}-A.
\]

Its derivatives are

\[
G'(A)=\frac{(T+1)^2}{(A+1)^2}-1,\qquad
G''(A)=-\frac{2(T+1)^2}{(A+1)^3}<0.
\]

Consequently \(G\) has its unique maximum over \(A>0\) at \(A=T\), with
\(G(T)=T^2\).  More directly, exact rational arithmetic gives

\[
T^2-G(A)=\frac{(A-T)^2}{A+1}.
\tag{4}
\]

Every feasible route has a nonempty support because \(Q=1\).  Conditional
on support \(S\), equal-price aggregation proves that its best value is
exactly \(G(A_S)\).  Equation (4) then shows that the routing optimum is at
least the decision threshold \(K=T^2\) if and only if some subset sums to
\(T\).

All constructed quantities are positive integers, and their binary
encoding length is polynomial in the SUBSET-SUM instance length:
\(p=(T+1)^2\) and \(b_i=pw_i\) require only polynomially many bits.  The
mapping is therefore a polynomial-time many-one reduction. \(\square\)

For the equal-price integer-reserve class, a proposed support is a
polynomial-size certificate and its aggregate objective (3) is rational and
polynomial-time evaluable.  The decision problem is therefore in NP as
well.  Together with the pseudo-polynomial dynamic program in
`docs/equal-price-algorithm.md`, this establishes the expected weak
NP-completeness boundary for that integer-data subclass.

### Remaining claim boundary

1. Check whether this exact special-case reduction already appears in the
   fixed-charge resource-allocation or AMM-routing literature.
2. Determine whether strong NP-hardness holds in a heterogeneous-price
   subclass, or whether weak hardness is the correct boundary.

The reduction is valid, but no novelty claim is made until the first item is
closed.

## 5. First algorithmic hypotheses

### Hypothesis A: pseudo-polynomial equal-price algorithm

If the \(a_i\) are integer multiples of a common unit and total reserve is
bounded, dynamic programming over attainable aggregate reserve \(A_S\) and
minimum gas cost should solve (3) exactly.  This is consistent with the
candidate weak-hardness result.

### Hypothesis B: equal-price FPTAS

Scaling the reserve weights or gas costs may yield a fully polynomial
approximation scheme for (3).  The approximation must be defined carefully
when the optimal net output is close to zero; an additive guarantee may be
more meaningful than a multiplicative one.

### Hypothesis C: certifying heterogeneous solver

For general parallel pools, Lagrangian relaxation of the input constraint
separates over pools:

\[
\lambda Q+
\sum_i\max\left\{
0,\ \sup_{x\geq0}[f_i(x)-\lambda x]-q_i
\right\}.
\tag{5}
\]

Minimizing (5) over \(\lambda\geq0\) gives a computable upper bound.  The gap
between this bound and a feasible water-filled route is an a posteriori
certificate.  The key questions are when this gap vanishes and whether it is
tight enough to guide branching or active-set repair.

The conjugate, activation thresholds, exact one-dimensional minimization,
and adversarial rounding examples are now derived in
`docs/certificates-and-counterexamples.md`.  The bound is implemented and
tested; only the branch-and-bound use remains a hypothesis.
