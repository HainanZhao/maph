# Gas-aware AMM routing

This project studies exact and certifiably near-optimal order routing across
parallel constant-product automated market makers (AMMs) when using a pool
incurs a fixed execution cost such as gas.

## Research question

A trader supplies a fixed amount \(Q>0\) of token \(X\).  Pool \(i\) has
input reserve \(a_i>0\), output reserve \(b_i>0\), proportional fee factor
\(\gamma_i\in(0,1]\), and fixed execution cost \(q_i\geq0\), denominated in
token \(Y\).  Sending \(x_i\geq0\) units to that pool returns

\[
f_i(x_i)=\frac{b_i\gamma_i x_i}{a_i+\gamma_i x_i}.
\]

The parallel-routing problem is

\[
\max_{x\geq0,\ \sum_i x_i=Q}
\left\{
\sum_i f_i(x_i)-\sum_iq_i\mathbf 1\{x_i>0\}
\right\}.
\]

Without the fixed costs, this is a separable concave resource-allocation
problem with a water-filling solution.  Fixed costs make pool selection
combinatorial.  The project asks:

> Which special structure of constant-product curves permits faster exact
> routing, useful approximation guarantees, or inexpensive a posteriori
> optimality certificates?

## Why this target

- It has a direct economic objective: additional net output after gas.
- It is sharply falsifiable against exhaustive search on small instances.
- Every proposed route can be paired with an upper bound, preventing a
  heuristic improvement from being misreported as optimal.
- Pool states and executed swaps can eventually be obtained from public
  blockchains.
- The target is narrower than the existing general mixed-integer
  formulations: parallel two-token constant-product pools and their special
  reciprocal response curves.

## Current status

Cycle 1 has a tested exact dynamic program for commensurate equal-price
pools, an additive reserve-rounding guarantee, and a closed-form
Lagrangian upper bound for heterogeneous pools.  A formal SUBSET-SUM
reduction establishes weak NP-hardness even for equal-price,
zero-proportional-fee pools.  The reduction is valid, but its novelty
relative to fixed-charge resource-allocation literature remains under
audit.

## Documents

- `src/parallel_cpmm.py`: fixed-set water filling and an exhaustive exact
  oracle for small instances.
- `src/equal_price_dp.py`: exact pseudo-polynomial equal-price routing and
  additive reserve rounding.
- `src/certifying_router.py`: analytic Lagrangian bounds and deliberately
  simple routing baselines.
- `src/branch_and_bound.py`: node-wise analytic bounds and best-bound search
  with optional early stopping.
- `tests/test_parallel_cpmm.py`: structural and reduction checks.
- `docs/mathematics.md`: formulation, exact fixed-set solution, and candidate
  complexity result.
- `docs/equal-price-algorithm.md`: dynamic program and rounding guarantee.
- `docs/certificates-and-counterexamples.md`: dual derivation and compact
  failures of naive activation rules.
- `docs/branch-and-bound.md`: partial-activation bounds, search logic, and
  seeded prototype results.
- `docs/progress.md`: claim ledger and research decisions.
- `docs/roadmap.md`: staged plan and early kill criteria.

## Claim discipline

1. A KKT point for a fixed active set is not a globally optimal route.
2. Better output before gas is not necessarily better net execution.
3. A numerical MIP solution is not an optimality certificate unless its
   bound and tolerances are reported.
4. A theorem for parallel constant-product pools is not a theorem for
   arbitrary CFMM networks.

## Quick check

```bash
python3 -m unittest discover -s tests -v
```

For deterministic small-instance benchmarks:

```bash
python3 scripts/benchmark_equal_price.py
python3 scripts/benchmark_certificates.py
python3 scripts/benchmark_branch_and_bound.py
```
