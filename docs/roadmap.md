# Research roadmap

## Objective

Develop rigorous partial results toward Erdős Problem 700, beginning with
prime powers and numbers of the form \(p^a q^b\). Maintain reproducible
code, data, proofs, failed ideas, and open questions.

## Phase 0 — foundations

- [x] Record the exact definition and scope.
- [x] Separate proved, computed, and conjectural claims.
- [x] Set up a dated progress log.

Exit criterion: another reader can identify the problem, our narrower target,
and the evidentiary status of every claim.

## Phase 1 — trustworthy computation

- [x] Factor \(n\) by exact trial division.
- [x] Compute \(v_p\binom{n}{k}\) with Legendre's formula.
- [x] Reconstruct \(\gcd(n,\binom{n}{k})\) from valuations without constructing
  the binomial coefficient.
- [x] Implement a direct `math.comb` reference calculation.
- [x] Cross-check the implementations on small inputs.
- [ ] Benchmark and optimize larger searches.

Exit criterion: exhaustive agreement of the independent implementations on
a documented range.

## Phase 2 — prime powers

- [x] Prove the valuation identity
  \[
  v_p\binom{p^a}{k}=a-v_p(k),\qquad 0<k<p^a.
  \]
- [x] Deduce \(f(p^a)=p\) for composite prime powers.
- [ ] Formalize boundary cases and add property tests.

Exit criterion: a short complete proof and computational tests agree.

## Phase 3 — two-prime families

- [x] Generate an initial table for \(p^a q^b\) through \(1000\).
- [x] Record minimizing \(k\), not only \(f(n)\).
- [ ] Compare minimizers with prime powers dividing \(n\).
- [ ] Formulate separate conjectures for squarefree \(pq\), \(p^a q\), and
  \(p^a q^b\).
- [x] Prove the squarefree \(pq\) case from first principles.

Exit criterion: at least one rigorously proved non-prime-power family and a
precise next conjecture supported by archived data.

## Phase 4 — the strict square-root question

- [x] Search for \(f(n)>\sqrt n\) without floating-point comparisons
  (use \(f(n)^2>n\)).
- [x] Prove that a strict hit needs at least three distinct prime factors.
- [x] Reduce squarefree three-prime hits to \(r<pq\) and \(f(pqr)=pq\).
- [x] Derive an explicit witness criterion for \(n=2qr\).
- [x] Classify \(2qr\) hits through \(q\leq1000\) by witness type.
- [x] Find a conditional parameterized family using binary blocks.
- [ ] Remove or weaken the simultaneous-primality condition in that family.
- [ ] Classify general hits by exponent vector and prime ratios.
- [ ] Attempt an infinite-family proof.

Exit criterion: either a proved infinite family, a new restricted theorem, or
a documented obstruction explaining why the observed families do not extend.

## Phase 5 — general bounds

- [ ] Study choices \(k=r^j\) for prime powers dividing \(n\).
- [ ] Translate simultaneous valuation constraints into base-\(p\) carry
  conditions via Kummer's theorem.
- [ ] Explore whether Chinese-remainder constructions can produce one \(k\)
  favorable for several primes at once.

## Phase 6 — near-multiple construction

- [x] Prove \(f(M(M-1))\in\{M-1,M\}\) when \(M-1\) is prime.
- [x] Prove the conditional prime-base family
  \(M=p(p^m-1)\).
- [x] Falsify the naive affine extension \(p^m-1\mapsto ap^m-1\).
- [x] Test the near-30 conjecture through \(b=15{,}000\).
- [x] Search alternative Dirichlet moduli and retain counterexamples.
- [x] Formulate and test the reciprocal-threshold conjecture.
- [x] Derive the exact nested Lucas-prefix condition for a witness.
- [x] Derive the primary-pseudoperfect subset-sum reduction.
- [x] Falsify the naive two-shifted-digit conjecture.
- [x] Prove a two-digit cover for one-prime inherited examples.
- [x] Reformulate the reciprocal threshold as an integer-defect statement.
- [x] Prove unbounded finite-prefix depth for the stronger all-\(M\) cover.
- [x] Derive the explicit third-prefix formulas at defect one.
- [x] Stress-test the unbounded power-\(5\) near-witness family.
- [x] Recast the complete digit towers as finite CRT boxes.
- [x] Build and cross-check a sparse smallest-box witness search.
- [x] Falsify the naive product-of-box-densities criterion.
- [x] Derive the character filter for divisible digit-box values.
- [x] Prove complement symmetry of every Lucas box.
- [x] Falsify the single-box cancellation hypothesis.
- [x] Falsify pairwise sufficiency and define the Lucas cover degree.
- [x] Derive the full multi-base Fourier formula.
- [x] Generalize the exact finite-box solver to selected prime bases.
- [x] Search structured exponent families for cover degree at least four.
- [x] Falsify the claim that the three smallest prime bases always suffice.
- [x] Extend the adaptive three-base falsifier through \(M=300000\).
- [x] Find unrestricted cover-degree-four examples.
- [x] Compute exact supercritical cover degrees through \(10^5\).
- [x] Formulate and test the pair-isolation conjecture.
- [x] Extend exact pair-isolation tests through \(M=300000\).
- [x] Derive the exact defect-port formula.
- [x] Prove complete vacuity of every fixed prefix depth.
- [x] Derive the second digit after a blind defect port.
- [x] Reduce all three-prime supercritical cases to \(2^a3^b5^c\).
- [x] Check the 2026 nine-factor primary pseudoperfect example.
- [x] Build a meet-in-the-middle positive-certificate adversarial search.
- [x] Quantify \(\Omega(\log\log M)\) prefix blindness at every fixed radical.
- [x] Characterize exactly when a shallow prefix is completely blind.
- [x] Derive the exponent-block decomposition and wildcard corridor.
- [x] Find the least synchronized blind exponent on \(M=30^e\).
- [x] Prove that two prime bases cannot stabilize their corridors together.
- [x] Derive fixed-depth periodicity on the three-prime exponent torus.
- [ ] Prove or disprove the near-30 conjecture.
- [ ] Prove or disprove the reciprocal-threshold conjecture.
- [ ] Find a multi-level packing interpretation of the prefix conditions.
- [ ] Eliminate all proper subset sums for primary pseudoperfect \(M\).
- [ ] Prove or disprove the three-shifted-digit conjecture.
- [ ] Relate Lucas failure depth to the primary-pseudoperfect port law.
- [ ] Find a defect descent or composition law compatible with witnesses.
- [ ] Determine whether prime predecessors can also have unbounded depth.
- [ ] Test whether a full witness descends to a positive-defect divisor.
- [ ] Bound the shortest positive representative of the Lucas CRT boxes.
- [ ] Compare Lucas-box entropy with the reciprocal defect.
- [ ] Bound the nontrivial character terms using negative defect.
- [ ] Search for reciprocal-supercritical cover degree at least four.
- [ ] Prove or disprove the adaptive three-base cover conjecture.
- [ ] Prove or disprove pair isolation under negative defect.
- [ ] Prove or disprove pair isolation for every \(2^a3^b5^c\).
- [ ] Prove or disprove \(\mathcal A_2\cap\mathcal A_3=\varnothing\) on \(M=30^e\).
- [ ] Compress exponent wildcard corridors into a two-base automaton.
- [ ] Rule out a full witness in the rigid singleton-pair case.
- [ ] Treat the Giuga boundary \(D=-1\) by full-depth methods.
- [ ] Build a two-base transfer-matrix counterexample search.
- [ ] Find a defect-controlled greedy rule for selecting three bases.
- [ ] Optimize the compiled three-base-cover falsifier beyond \(10^5\).
- [ ] Group and bound the Fourier expansion by interaction support.

## Working rules

1. Never infer an infinite statement solely from a finite search.
2. Cross-check optimized computations against the reference implementation.
3. Preserve counterexamples and failed conjectures in the progress log.
4. Recheck the public problem status and literature before claiming novelty.
