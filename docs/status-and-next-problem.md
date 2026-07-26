# Status, effort estimate, and next problem

## Current status of Erdős Problem 700

The public problem remains open:

- characterize composite \(n\) with \(f(n)=n/P(n)\);
- decide whether \(f(n)>\sqrt n\) for infinitely many composite \(n\);
- prove or disprove the proposed logarithmic-power upper bounds.

This project has not solved any of those three questions. It has produced
exact reductions, proved structural lemmas, and substantial finite
evidence for a narrower near-multiple strategy.

The strongest current restricted targets are:

1. prove
   \[
   \mathcal A_2\cap\mathcal A_3=\varnothing
   \quad\text{for every }M=30^e;
   \]
2. prove pair isolation for every \(M=2^a3^b5^c\);
3. prove that negative reciprocal defect excludes a full common Lucas
   witness.

The first target is exactly certified through \(e=10\). The second is
exactly certified on all 1,000 exponent vectors in \([1,10]^3\).

## Remaining-effort estimate

Open-problem research cannot be estimated like implementation work. The
following ranges estimate the effort needed to reach a meaningful
milestone, not the time to a guaranteed proof.

| Milestone | Plausible focused effort | Main uncertainty |
|---|---:|---|
| Independent human audit of Propositions 25–35 | 3–7 days | Detecting a hidden hypothesis or literature overlap |
| Reproducible computational note | 1–3 weeks | Independent implementation and certificate archiving |
| Serious attack on the diagonal \(30^e\) conjecture | 2–8 weeks | Compressing the terminal digit blocks after a blind prefix |
| Restricted theorem for all \(2^a3^b5^c\) | 1–6 months | One base always remains in a moving-boundary regime |
| Reciprocal-threshold theorem | Not responsibly bounded; likely months or longer | Requires a new full-depth multi-base inequality |
| Full resolution of Erdős Problem 700 | No credible estimate | It contains three broad, independently difficult questions |

The computational infrastructure is mature. The remaining gap is
conceptual rather than a matter of scanning a larger range.

Before any external mathematical claim, the proofs should be read and
reconstructed independently by a human, the searches should be rerun by
an independent program, and relevant literature should be checked in
greater depth.

## Recommended easier follow-on: Erdős Problem 699

[Erdős Problem 699](https://www.erdosproblems.com/699) asks whether, for
every
\[
1\leq i<j\leq n/2,
\]
there is a prime \(p\geq i\) such that
\[
p\mid
\gcd\left(\binom ni,\binom nj\right).
\]

It is a better next target than another unrelated problem because:

1. **The machinery transfers directly.** Kummer valuations, Lucas digit
   tests, prime-support masks, and exact cross-checking are already
   implemented here.
2. **A counterexample is finite and decisive.** Failure is certified by
   one triple \((n,i,j)\) for which every common prime divisor is below
   \(i\).
3. **The quantifiers are cleaner.** Problem 700 minimizes a gcd over all
   \(k\), mixes all prime powers dividing \(n\), and asks for infinite
   families or uniform asymptotics. Problem 699 compares only two
   coefficients in one row.
4. **Restricted theorems are natural.** One can first treat fixed \(i\),
   special positions \(j\), prime-power rows, or regions such as
   \(j-i\) small.

This does not mean Problem 699 is easy. The public discussion reports an
independent search through \(n=10^7\) without a counterexample, and a
recent proposed proof was found invalid. A useful project should
therefore prioritize theory and near-miss classification over simply
repeating the same exhaustive scan.

### Proposed first phase

1. Implement two independent prime-support evaluators for
   \(\binom ni\): one using factorial valuations and one using Kummer
   carries.
2. Reproduce all published exceptional examples and cross-check small
   rows exhaustively.
3. For every \((n,i,j)\), record the largest common prime and the deficit
   below \(i\); preserve the closest near misses.
4. Search structured families suggested by base-\(p\) digit patterns,
   rather than scanning only by increasing \(n\).
5. Attempt restricted proofs for fixed \(i\) and for prime-power or
   near-prime-power rows.

A realistic initial milestone is a trustworthy classifier plus one new
restricted theorem or a substantially sharper structural reduction in
roughly one to three weeks of focused work.
