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

## Revised status of Erdős Problem 699

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

The initial recommendation below became stale almost immediately.  As of
2026-07-26, the problem page lists two partial proof claims:

1. Liam Price, using GPT-5.6, submitted a partial proof for
   \(j\leq3i/2\) or \(n=2j\).  The site marks this partial proof as
   accepted as correct.
2. Wouter Van Doorn and Stefano Rocca submitted a work-in-progress
   partial claim reducing possible counterexamples to \(i=3\) or an
   ineffective finite exceptional set with \(4\leq i\leq1475\).  Its
   authors say they are still digesting, verifying, and polishing it; the
   site does not currently mark it accepted.

Thus Problem 699 remains open, but it is now an active and crowded target.
It is no longer recommended as a clean independent follow-on.  A useful
contribution would instead be an audit/closure project: independently
reconstruct the second claim, make its finite exceptional set effective,
enumerate that set, or solve the residual \(i=3\) case.

This status correction motivated the physics pivot documented in
[`physics-pivot.md`](physics-pivot.md).

The public page remains the authoritative live source; neither a
site-accepted partial proof nor a work-in-progress manuscript is the same
thing as a refereed full solution.
