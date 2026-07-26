# Stage 4: summarize, brainstorm, work, repeat

This note records three short research cycles. Each cycle ends by separating
what was proved, what was only tested, and what should be attacked next.

## Cycle 1 — replace “30” by a structural invariant

### Summary

Stage 3 reduced the infinite-family problem to the following covering
question. If \(M-1\) is prime, can every
\[
1\leq t\leq(M-1)/2
\]
be covered by a prime \(p\mid M\) for which
\[
p\mid\binom{M(M-1)}{Mt}?
\]
The first candidate was \(30\mid M\).

### Brainstorm

Rather than treating \(30\) as magic, vary the forced divisor \(L\mid M\).
The successful small moduli suggested measuring a squarefree kernel by
\[
H(L)=\sum_{p\mid L}\frac1p.
\]
This gives a natural “covering budget”: \(H(30)=31/30>1\).

### Work

The generalized C search `scripts/falsify_near30.c` produced the following
bounded evidence.

| Forced divisor \(L\) | \(H(L)\) | Search | Result |
|---|---:|---:|---|
| \(30=2\cdot3\cdot5\) | \(31/30\) | \(b\leq15{,}000\), 4,724 prime predecessors | no counterexample |
| \(858=2\cdot3\cdot11\cdot13\) | \(859/858\) | \(b\leq1{,}000\), 290 prime predecessors | no counterexample |
| \(1722=2\cdot3\cdot7\cdot41\) | \(1723/1722\) | \(b\leq1{,}000\), 269 prime predecessors | no counterexample |
| \(1806=2\cdot3\cdot7\cdot43\) | \(1805/1806\) | \(b\leq2{,}000\), 512 prime predecessors | no counterexample |
| \(174=2\cdot3\cdot29\) | \(151/174\) | \(b\leq1{,}000\) | counterexample at \(b=12\) |

The counterexample in the final row is
\[
M=2088=2^3\cdot3^2\cdot29,\qquad M-1=2087\ \text{prime},
\qquad t=13.
\]
All three prime bases pass Lucas's test, so
\[
f(2088\cdot2087)=2087.
\]
Thus “at least three distinct prime factors” is false as a sufficient
condition.

### Result

The experiment suggests the following much more coherent target.

**Reciprocal-threshold conjecture.** If \(M-1\) is prime and
\[
\sum_{p\mid M}\frac1p>1,
\]
then
\[
f(M(M-1))=M.
\]

This conjecture implies the near-30 conjecture. Consequently, if proved,
Dirichlet's theorem applied to \(M-1\equiv-1\pmod{30}\) would prove
infinitely many strict square-root hits.

## Cycle 2 — try hard to falsify the new threshold

### Summary

A high-leverage conjecture should first survive searches aimed at its
boundary, not merely dense examples containing many small primes.

### Brainstorm

Three tests are especially informative:

1. scan every \(M\), temporarily dropping the condition that \(M-1\) is
   prime;
2. scan farther when \(M-1\) is prime;
3. survey actual witnesses and maximize their reciprocal sum.

### Work

The new program `scripts/falsify_reciprocal.c` uses Lucas digit tests and an
exact integer comparison for the reciprocal threshold.

- Among all \(M\leq100{,}000\), no witness occurred in any of the 4,147
  cases above the threshold.
- Among \(M\leq300{,}000\) with \(M-1\) prime, no witness occurred in any
  of the 4,016 cases above the threshold.
- Among \(M\leq100{,}000\) with \(M-1\) prime, 1,205 values below the
  threshold did have a witness. The largest reciprocal sum among them was
  \[
  \frac12+\frac13+\frac1{19}+\frac1{317}
  =\frac{32131}{36138}\approx0.8891194864,
  \]
  at \(M=36138,t=4\).

These are computational observations, not an extrapolation to infinity.

The below-threshold kernel
\[
1806=2\cdot3\cdot7\cdot43
\]
is creatively suggestive:
\[
\frac12+\frac13+\frac17+\frac1{43}=1-\frac1{1806}.
\]
It is the Egyptian-fraction boundary immediately below \(1\). It still had
no counterexample for the tested prime predecessors, showing that the
threshold is likely sufficient rather than necessary.

### Result

No counterexample was found. More importantly, the failed cases below the
threshold provide controls: the conjecture is not a tautological artifact
of the code, because the same evaluator finds the witnesses at
\((M,t)=(2088,13)\) and \((36138,4)\).

## Cycle 3 — expose the proof obligation digit by digit

### Summary

For \(p^a\parallel M\), put \(u=M/p^a\). Proposition 14 proves that a
witness must satisfy the entire nested family
\[
ut\bmod p^h\leq u(M-1)\bmod p^h
\qquad(h=1,2,\ldots)
\]
simultaneously for every \(p\mid M\).

### Brainstorm

The reciprocal threshold strongly resembles a packing obstruction:
if one common multiplier \(t\) passes all prime bases, perhaps one can
associate disjoint arcs or digit cylinders of measure \(1/p\) to the primes
\(p\mid M\). Disjointness would immediately give
\[
\sum_{p\mid M}\frac1p\leq1.
\]
The missing object is the key mathematical problem.

Candidate objects include:

- the first forbidden base-\(p\) prefix along the orbit \(u,2u,\ldots,tu\);
- half-open arcs between consecutive residues of \(u j\bmod p^h\);
- cylinders in a product of \(p\)-adic digit trees, charged at the first
  digit where a carry would occur.

### Work

The script `scripts/carry_signatures.py` records, for every multiplier, the
first failing Lucas digit in each prime base.

- At \(M=2088\), it isolates \(t=13\) as the unique uncovered multiplier.
- At \(M=1806\), all 902 tested multipliers are covered.
- At \(M=30,t=1\), the single-level consequence
  \[
  \left\{\frac{ut}{p^a}\right\}
  +\left\{\frac{u}{p^a}\right\}\leq1
  \]
  passes for all three primes, but a later binary digit fails.

The last example falsifies the simplest packing attempt. A valid packing
lemma must encode the full prefix tower, or at least two strategically
chosen levels per prime.

### Result and next cycle

The project now has one clean conjecture and one exact local language for
attacking it. The next cycle should proceed in this order:

1. **Two-level lemma.** Search for the weakest pair of prefix levels whose
   simultaneous satisfaction by a witness forces a global inequality.
2. **Minimal witness descent.** Assume a counterexample with least \(M\),
   then use the first two prefix levels to try to construct a smaller
   counterexample.
3. **Cylinder-packing model.** Turn first-failure signatures into explicit
   intervals or digit cylinders and test disjointness computationally
   before attempting a proof.
4. **Boundary families.** Study Egyptian-fraction kernels such as \(1806\)
   and nearby supercritical kernels \(858,1722\). Their exact identities
   should make a symbolic proof easier than arbitrary \(M\).
5. **Independent review.** The June 2026 preprint
   [Computing the Greatest Common Divisor of Binomial Coefficients
   \(\binom{mn}{mk}\)](https://arxiv.org/abs/2606.20940)
   studies the gcd over a whole restricted family of coefficients. Its
   aggregate gcd is different from our “each term is covered by some
   prime” condition, but its carry methods may supply useful lemmas.

The decisive target for the next session is now precise:

> Prove, or find a counterexample to, the packing implication
> \[
> \exists t\text{ passing every Lucas tower}
> \quad\Longrightarrow\quad
> \sum_{p\mid M}\frac1p\leq1.
> \]

If it is true, the original infinite-family question is solved.

## Cycle 4 — mine the Egyptian-fraction boundary

### Summary

The identity
\[
\frac12+\frac13+\frac17+\frac1{43}=1-\frac1{1806}
\]
is the defining identity of a primary pseudoperfect number:
\[
1+\sum_{p\mid M}\frac{M}{p}=M.
\]
So the most interesting point just below the reciprocal threshold belongs
to a named arithmetic class, rather than being a numerical coincidence.

### Brainstorm

Reduce the identity modulo each \(p\mid M\). It gives
\[
\frac{M}{p}\equiv-1\pmod p.
\]
This is exactly the residue that appears in the first shifted Lucas digit,
so the Egyptian-fraction identity should collapse the witness search.

### Work

Proposition 15 carries this out. Any common witness must have the form
\[
t=\sum_{p\in S}\frac{M}{p}
\]
for a subset \(S\) of the prime divisors. The proof is a clean combination
of the first Lucas digit and the Chinese remainder theorem.

The implemented reduction gives:

| \(M\) | Factor set | Original multipliers | Subset-sum candidates | Outcome |
|---:|---|---:|---:|---|
| \(6\) | \(2,3\) | 2 | 1 | all covered computationally |
| \(42\) | \(2,3,7\) | 20 | 3 | all covered computationally |
| \(1806\) | \(2,3,7,43\) | 902 | 7 | all covered computationally |
| \(47058\) | \(2,3,11,23,31\) | 23,528 | 15 | all covered computationally |

For \(M=6,42,47058\), the predecessor \(M-1\) is prime, so these give
computationally verified instances of \(f(M(M-1))=M\). The case \(M=1806\)
is still a valuable digit-cover example even though
\(1805=5\cdot19^2\).

### Result and renewed proof target

The primary-pseudoperfect class supplies a structured boundary laboratory.
The next concrete lemma should try to show that every nonempty proper
subset sum in Proposition 15 fails at a second or later Lucas digit.
Proving that for all primary pseudoperfect \(M\) would not yet establish
infinitely many examples, but it would be a nontrivial family theorem and
could reveal the missing multi-level packing mechanism.
