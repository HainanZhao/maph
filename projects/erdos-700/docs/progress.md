# Progress log

## Claim ledger

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | The valuation and direct implementations agree for \(4\leq n\leq250\), including every minimizing \(k\). | Computationally verified | Unit test |
| C2 | For \(0<k<p^a\), \(v_p\binom{p^a}{k}=a-v_p(k)\). | Proved | `mathematics.md`, Lemma 1 |
| C3 | For composite prime powers, \(f(p^a)=p\). | Proved | `mathematics.md`, Corollary 2 |
| C4 | There are infinitely many composite \(n\) with \(f(n)\geq\sqrt n\). | Proved | Take \(n=p^2\), using C3 |
| C5 | There are infinitely many composite \(n\) with \(f(n)>\sqrt n\). | Open | Original problem |
| C6 | If \(p^a\parallel n\), the choice \(k=p^a\) gives gcd \(n/p^a\). | Proved | `mathematics.md`, Lemma 3 |
| C7 | If \(n\) has at most two distinct prime factors, \(f(n)\leq\sqrt n\). | Proved | `mathematics.md`, Corollary 5 |
| C8 | If \(p<q\) are primes, then \(f(pq)=p\). | Proved | `mathematics.md`, Proposition 6 |
| C9 | For composite \(n\), \(f(n)\) is at least the smallest prime factor of \(n\). | Proved | `mathematics.md`, Lemma 4 |
| C10 | For primes \(p<q<r\), strict square-root inequality is equivalent to \(r<pq\) and \(f(pqr)=pq\). | Proved | `mathematics.md`, Proposition 7 |
| C11 | Computing \(f(pqr)\) requires only \(O(p+q+r)\) structured Lucas checks. | Proved and implemented | `mathematics.md`, Proposition 8; `f_squarefree_triple` |
| C12 | For eligible \(2qr\), gcd \(2\) is impossible and gcds \(q,r\) have explicit short witness criteria. | Proved and implemented | `mathematics.md`, Proposition 9; `eligible_2qr_witnesses` |
| C13 | If \(2^m-1\) and \(2^{m+1}-3\) are prime, their triple gives a strict hit. | Proved, conditional construction | `mathematics.md`, Proposition 10 |
| C14 | It suffices that \(2^{m+1}-3\) is prime; \(2^m-1\) may be composite. | Proved, stronger conditional construction | `mathematics.md`, Proposition 11 |
| C15 | If \(M-1\) is prime, \(f(M(M-1))\) is either \(M-1\) or \(M\), with an exact Lucas witness criterion. | Proved and implemented | `mathematics.md`, Proposition 12; `analyze_near_multiple` |
| C16 | For prime \(p\), \(M=p(p^m-1)\), and prime \(M-1\), one has \(f(M(M-1))=M\). | Proved, conditional construction | `mathematics.md`, Proposition 13 |
| Q1 | If \(30\mid M\) and \(M-1\) is prime, then \(f(M(M-1))=M\). | Conjecture; verified only in a finite range | `brainstorm-stage3.md` |
| C17 | A near-multiple witness satisfies an exact nested family of Lucas-prefix inequalities in every prime base. | Proved | `mathematics.md`, Proposition 14 |
| Q2 | If \(M-1\) is prime and \(\sum_{p\mid M}1/p>1\), then \(f(M(M-1))=M\). | Conjecture; verified only in finite ranges | `brainstorm-stage4.md` |
| C18 | For primary pseudoperfect \(M\), every possible near-multiple witness is a subset sum of the values \(M/p\). | Proved and implemented | `mathematics.md`, Proposition 15 |
| C19 | One-prime inheritance \(K\mapsto K(K+1)\) has a two-shifted-digit cover at the new prime \(K+1\). | Proved | `mathematics.md`, Proposition 16 |
| Q3 | Every primary-pseudoperfect subset candidate fails within three shifted Lucas digits in some prime base. | Conjecture; verified through the 2026 nine-factor example, with the inherited ten-factor example covered by Proposition 16 | `brainstorm-stage5.md` |
| C20 | The reciprocal threshold is separated by a nonzero integer defect; primary pseudoperfect numbers occupy the extremal subcritical layer. | Proved and implemented | `mathematics.md`, Proposition 17 |
| C21 | No fixed number of initial shifted Lucas digits can cover every reciprocal-supercritical \(M\). | Proved | `mathematics.md`, Proposition 18 |
| C22 | Primary-pseudoperfect subset candidates have explicit third-prefix residue formulas. | Proved | `mathematics.md`, Proposition 19 |
| C23 | Full near-multiple witnesses are exactly short representatives in an intersection of finite Lucas digit boxes modulo pairwise-coprime prime powers. | Proved and implemented in part | `mathematics.md`, Proposition 20 |
| C24 | Compatible values in one Lucas box are counted by an exact roots-of-unity filter of its digit polynomial. | Proved | `mathematics.md`, Proposition 21 |
| C25 | Each Lucas box has complement symmetry \(t\leftrightarrow M-1-t\). | Proved and computationally checked | `mathematics.md`, Proposition 22 |
| C26 | The complete witness count has an exact multi-base Fourier expansion. | Proved | `mathematics.md`, Proposition 23 |
| C27 | A singleton half-range subintersection has only three or four symmetric full-interval points. | Proved | `mathematics.md`, Proposition 24 |
| Q4 | Negative reciprocal defect forces some pair of prime-base pass sets to have at most one common multiplier. | Conjecture; verified only in finite and partially resolved structured ranges | `brainstorm-stage11.md`, `brainstorm-stage12.md` |
| C28 | The first shifted digit is determined exactly by reciprocal defect and an exponent twist. | Proved and implemented | `mathematics.md`, Proposition 25; `near_multiple_defect_port` |
| C29 | At any fixed depth there are supercritical examples where every multiplier passes every truncated base test. | Proved | `mathematics.md`, Proposition 27 |
| C30 | When the first shifted digit is blind, the second shifted digit has an exact affine port formula. | Proved and implemented | `mathematics.md`, Proposition 28; `near_multiple_blind_second_digit_port` |
| C31 | The only reciprocal-supercritical radical with exactly three prime factors is \(30\). | Proved | `mathematics.md`, Proposition 29 |
| C32 | Every fixed squarefree radical has an explicit family with total prefix blindness of order \(\log\log M\); in particular this occurs at fixed defect \(-37\). | Proved | `mathematics.md`, Proposition 30 |
| Q5 | Pair isolation holds for every \(M=2^a3^b5^c\). | Conjecture; all 1,000 exponent vectors in \([1,10]^3\) exactly certified | `mathematics.md`, three-prime core conjecture; `brainstorm-stage12.md` |
| C33 | For \(H\leq v_p(M)\), the first \(H\) shifted digits are blind exactly when \(M/p^{v_p(M)}\equiv1\pmod{p^H}\). | Proved | `mathematics.md`, Corollary 31 |
| C34 | Varying one prime exponent inserts an exact wildcard corridor between two fixed Lucas digit blocks. | Proved | `mathematics.md`, Proposition 32 |
| C35 | The least \(e\) making \(M=30^e\) blind through depth \(H\geq5\) in all three bases is \(2^{H-4}3^{H-2}5^{H-1}\). | Proved | `mathematics.md`, Corollary 34 |
| C36 | With at least three prime factors, at most one prime base can be in the stabilized wildcard-corridor regime. | Proved | `mathematics.md`, Proposition 33 |
| C37 | At fixed depth \(H\geq4\), all truncated predicates for \(2^a3^b5^c\), \(a,b,c\geq H\), are periodic on an exponent torus of period \(30^{H-1}/2\). | Proved | `mathematics.md`, Proposition 35 |
| Q6 | For every \(e\geq1\), the diagonal family \(M=30^e\) has \(\mathcal A_2\cap\mathcal A_3=\varnothing\). | Conjecture; exactly certified for \(1\leq e\leq10\) | `mathematics.md`, diagonal empty-pair conjecture; `brainstorm-stage12.md` |

## 2026-07-26 — project initialization

### Decisions

- Selected Erdős Problem 700 because its binomial gcd can be computed through
  prime-adic valuations and studied by factorization type.
- Narrowed the first proof target to \(p^a q^b\), rather than attempting the
  unrestricted problem immediately.
- Chose dependency-free Python so computations are easy to reproduce.

### Important correction

An early informal formula incorrectly moved the minimum over \(k\) inside a
product over primes. The correct formula is

\[
f(n)=\min_{2\leq k\leq \lfloor n/2\rfloor}
 \prod_{p^a\parallel n}
 p^{\min\left(a,v_p\binom{n}{k}\right)}.
\]

The same \(k\) must control every prime dividing \(n\); this simultaneous
constraint is a central difficulty.

### Next actions

1. Run and record the independent implementation cross-check.
2. Generate initial data for \(p^a q^b\).
3. Inspect all strict square-root hits in a moderate range.

### Failed expectation caught by cross-checking

The first handwritten test table claimed \(f(12)=2\). Both the direct and
valuation implementations instead give \(f(12)=3\); for example, \(k=4\)
gives \(\gcd(12,\binom{12}{4})=\gcd(12,495)=3\), and exhaustive checking of
the admissible \(k\)'s gives no smaller value. The test fixture was corrected.

### First computation

- The direct and valuation implementations agree for every \(4\leq n\leq250\),
  including the full set of minimizing \(k\)'s.
- Among the 404 composite integers through \(500\), there are 23 strict
  square-root hits and 8 equality hits.
- The first strict hit is \(n=30\), with \(f(30)=6>\sqrt{30}\), attained at
  \(k=5\).
- Every strict hit through \(500\) has at least three distinct prime factors.
  Corollary 5 now proves this last property for all \(n\), not just the
  computed range.

The generated table is `data/f_values_500.csv`.

### First two-prime investigation

For all 508 integers \(n\leq1000\) with exactly two distinct prime factors,
we compared \(f(n)\) with the smaller of the two full prime-power components.
They differ in 38 cases. The first counterexample to the naive equality is

\[
n=45=3^2\cdot5,\qquad f(45)=3<5,
\]

attained at \(k=15\). Thus Corollary 5 is an upper bound, not generally an
exact formula. The squarefree subfamily does have the exact formula
\(f(pq)=\min(p,q)\), proved in Proposition 6.

### Expanded computation through 2000

- Checked all 1696 composite \(n\leq2000\).
- Found 89 strict square-root hits and 14 equality hits.
- Of 302 squarefree integers with exactly three prime factors, 35 are strict
  hits.
- Proposition 7 turns the squarefree-three-prime part of the original
  question into the concrete task of finding infinitely many triples
  \(p<q<r<pq\) for which \(f(pqr)=pq\).

The generated table is `data/f_values_2000.csv`.

### Fast squarefree-triple evaluator

Proposition 8 reduces the squarefree triple search from \(O(pqr)\) candidates
to \(O(p+q+r)\) Lucas checks. The implementation `f_squarefree_triple` is
cross-checked against the general valuation implementation for all triples
drawn from \(2,3,5,7,11,13,17\).

Using every prime through \(200\), the fast evaluator checked all 13,972
eligible triples
\[
p<q<r<pq.
\]
Of these, 1,189 satisfy \(f(pqr)=pq\), and hence are strict square-root hits
by Proposition 7. This is a computational observation over a bounded prime
range, not evidence by itself for an infinite family. The archived table is
`data/squarefree_triples_p200.csv`.

The next proof target is to translate “none of the three single-prime gcds
occurs” into explicit base-\(p\), base-\(q\), and base-\(r\) digit conditions,
then find a parameterized family for which those conditions can be proved.

## 2026-07-26 — stage 2: explicit witnesses

### Specialized \(2qr\) criterion

For odd primes \(q<r<2q\), Proposition 9 proves:

- gcd \(2\) cannot occur;
- a gcd-\(q\) witness needs only a binary submask test over
  \(1\leq t\leq\lfloor(2q-r)/2\rfloor\);
- a gcd-\(r\) witness needs a binary submask test and one Lucas test modulo
  \(q\).

The specialized implementation agrees exactly with the general triple
analyzer over the test range.

### Witness census

For all 11,051 eligible prime pairs \(q<r<2q\) with \(q\leq1000\):

| Classification | Count |
|---|---:|
| strict hit (no witness) | 4,055 |
| gcd-\(q\) witnesses only | 1,409 |
| gcd-\(r\) witnesses only | 2,178 |
| both witness types | 3,409 |

The table, including every witness multiplier, is
`data/eligible_2qr_q1000.csv`.

### Simple patterns falsified

The witness data rejects several tempting unconditional guesses:

- “take \(r\) to be the next prime after \(q\)” first fails at
  \((q,r)=(11,13)\);
- “take \(r=2q-1\)” first fails at \((19,37)\);
- “take \(r=2q-3\)” first fails at \((23,43)\).

These failures are retained because they show that prime proximity alone is
not enough; binary digit structure is essential.

### Conditional binary construction

Proposition 10 proves that if
\[
q=2^m-1,\qquad r=2^{m+1}-3
\]
are both prime, then
\[
f(2qr)=2q>\sqrt{2qr}.
\]

The proof completely excludes the Lucas witnesses using the final \(m\)
binary digits. Simultaneous-prime examples occur for
\(m=2,3,5,13,19\). This is not an infinite-family solution because the
required simultaneous primality is not known infinitely often.

### Strengthening after testing composite factors

Exact computation showed that
\[
n_m=2(2^m-1)(2^{m+1}-3)
\]
is also a strict hit for \(m=4,8,9\), even though \(2^m-1\) is composite.
This led to Proposition 11: only \(2^{m+1}-3\) needs to be prime.

The key additional observation is that, modulo the prime
\(r=2^{m+1}-3\), Lucas's theorem permits a binomial coefficient nonzero
modulo \(r\) only at \(k=r\). Every other gcd contains \(r\), and the binary
argument rules out the only dangerous value, gcd \(r\).

For \(2\leq m\leq25\), the prime-\(r\) cases are
\[
m=2,3,4,5,8,9,11,13,19,21,23.
\]
This still does not prove infinitely many hits, because infinitude of primes
\(2^a-3\) is unknown.

### Next proof target

Try to remove the remaining primality requirement on
\(r=2^{m+1}-3\), or replace the exact binary form by intervals/congruence
classes where established prime-distribution theorems can supply \(r\).
When \(r\) is composite, record which proper prime-power component creates
the first small gcd; \(m=7\), where \(r=253=11\cdot23\) and \(f(n)=46\), is
the first obstruction.

## 2026-07-26 — stage 3: near multiples and a possible Dirichlet route

### Literature/status check

The current discussion for Erdős Problem 700 contains related
\(n=q(q+1)\) reductions and conditional digit constructions. It does not
claim a verified infinite family, and the page explicitly warns that forum
comments are unverified:
<https://www.erdosproblems.com/forum/thread/700?order=newest>.

### Near-multiple reduction

Proposition 12 proves that if \(M-1\) is prime, then
\[
f(M(M-1))\in\{M-1,M\}.
\]
This turns strictness into a covering problem for the prime divisors of
\(M\).

### Prime-base construction

Proposition 13 generalizes the binary-block proof. For prime \(p\),
\[
M=p(p^m-1),\qquad M-1\ \text{prime}
\]
implies \(f(M(M-1))=M\). The computation independently verifies 26 such
prime cases with \(M\leq2{,}000{,}000\).

The affine extension \(p^m-1\mapsto ap^m-1\) is false. The first recorded
counterexample in the \(p=2,m=3\) scan is \(a=25\), giving
\[
M=398,\quad M-1=397,\quad f(M(M-1))=397
\]
with witness multiplier \(t=47\).

### Near-30 conjecture

No actual counterexample was found for \(M=30b\), \(b\leq10{,}000\), among
the 3,260 cases where \(M-1\) is prime. If this finite pattern extends to
all \(b\), Dirichlet's theorem would settle the strict-square-root question.

A deliberately stronger fixed-prime cover was falsified at
\[
M=33060,\qquad t=65.
\]
Here the binomial is nonzero modulo \(2,3,5\), but the extra factor \(19\mid
M\) still divides it. This distinction is important: the proposed proof
failed, while the actual near-30 conjecture survived the current test.

All stage-three ideas, caveats, and next attacks are recorded in
`docs/brainstorm-stage3.md`.

## 2026-07-26 — stage 4: reciprocal threshold and prefix towers

Three research cycles are recorded in `docs/brainstorm-stage4.md`.

### Structural replacement for the near-30 conjecture

Alternative forced moduli revealed the candidate invariant
\[
H(M)=\sum_{p\mid M}\frac1p.
\]
This led to Q2, the reciprocal-threshold conjecture. It contains Q1 because
\(H(30)=31/30>1\).

The same scan falsified the weaker idea that three distinct prime factors
are sufficient. The first retained counterexample is
\[
M=2088=2^3\cdot3^2\cdot29,\quad M-1=2087\text{ prime},\quad t=13.
\]

### Computational evidence

- Q1 has no counterexample for \(M=30b\), \(b\leq15{,}000\), across 4,724
  prime values of \(M-1\).
- Q2 has no counterexample among all \(M\leq100{,}000\), across 4,147
  above-threshold cases, even without requiring \(M-1\) prime.
- Q2 has no counterexample among \(M\leq300{,}000\) with \(M-1\) prime,
  across 4,016 above-threshold cases.
- A survey of actual witnesses below the threshold found maximum reciprocal
  sum \(32131/36138\approx0.8891194864\) through \(M=100{,}000\), at
  \(M=36138,t=4\).

### Proof progress and obstruction

Proposition 14 expresses a witness as simultaneous nested residue-prefix
inequalities. Its one-level fractional-part consequence is too weak:
\(M=30,t=1\) passes that relaxation for every \(p\mid30\), but fails at a
higher binary digit.

The next proof target is therefore a multi-level packing lemma. A common
witness should force \(H(M)\leq1\); proving this implication would establish
Q2 and, via Dirichlet's theorem, solve the infinite strict-hit question.

### Primary-pseudoperfect boundary cycle

The exact boundary identity
\[
\frac1M+\sum_{p\mid M}\frac1p=1
\]
led to Proposition 15. It reduces as many as \((M-1)/2\) potential
multipliers to subset sums of \(M/p\). For \(M=47058\), this means 15
candidates instead of 23,528.

The known small boundary values \(M=6,42,1806,47058\) have no surviving
candidate. The predecessors of \(6,42,47058\) are prime, producing three
computationally verified strict hits after the reduced finite checks.

### Recent related work

A June 2026 preprint on
[restricted gcds of \(\binom{mn}{mk}\)](https://arxiv.org/abs/2606.20940)
uses Kummer carry arguments for the gcd over all multipliers. That aggregate
question is not the same as our dynamic covering question, but its methods
are close enough to include in the next literature pass.

## 2026-07-26 — stage 5: digit depth and inheritance

### Two-digit conjecture falsified cleanly

For the seven-factor primary pseudoperfect number
\[
M=52495396602,
\]
the candidate
\[
t=M/3+M/17=20586430040
\]
passes the first two shifted Lucas digits for every \(p\mid M\). It fails
at the third shifted digit. This is the first obstruction to the proposed
two-digit lemma.

### Inherited family theorem

Proposition 16 proves that if \(K\) is primary pseudoperfect and \(K+1\) is
prime, then every admissible subset candidate for \(M=K(K+1)\) fails at the
second shifted digit in base \(K+1\). The proof leaves only \(t=0\) and
\(t=M-1\), both inadmissible.

### Updated literature and computation

The May 2026 preprint
[Port Fillings for Primary Pseudoperfect Numbers](https://arxiv.org/abs/2605.21518)
constructs nine- and ten-prime-factor examples. Exact Lucas-prefix
computation finds no candidate surviving three shifted digits in those
examples or in the earlier examples with at most eight prime factors.
The full histograms and the resulting three-digit conjecture are recorded
in `docs/brainstorm-stage5.md`.

### Integer-defect reformulation

For \(R=\operatorname{rad}(M)\), set
\[
D(R)=R-\sum_{p\mid R}R/p.
\]
Proposition 17 shows that \(D(R)\neq0\). Thus the reciprocal-threshold
conjecture is exactly the assertion that a common witness implies
\(D(R)\geq1\). Primary pseudoperfect numbers have \(D(R)=1\), explaining
why they are the natural sharp boundary cases.

## 2026-07-26 — stage 6: unbounded hidden carry depth

### Bounded-depth strategy ruled out in the stronger setting

Proposition 18 constructs, for every \(H\), a reciprocal-supercritical
\(M=6\cdot5^a\) and admissible \(t=6^h\) that pass the first \(H\) shifted
digits in all prime bases. Base \(5\) passes completely; bases \(2,3\) have
long forced-zero prefixes.

The construction does not ensure \(M-1\) prime, so its logical scope is the
stronger all-\(M\) cover statement.

### Deep prime-predecessor control

The explicit case
\[
M=63150,\quad M-1=63149\text{ prime},\quad t=5126
\]
passes 16 shifted digits in every prime base before its first failures at
digit 17. This does not prove unbounded depth with prime predecessors, but
it rejects any very shallow version.

### Third-prefix formula

Proposition 19 gives exact residues modulo \(p^3\) for every
primary-pseudoperfect subset candidate. The proof and strategic split
between defect-one and negative-defect regimes are recorded in
`docs/brainstorm-stage6.md`.

## 2026-07-26 — stage 7: structured near-witnesses and CRT boxes

### Power-\(5\) adversarial search

The structured search through \(a\leq500\) checked 89,405 pairs
\[
M=6\cdot5^a,\qquad t=6^h
\]
without finding a full witness. At \(a=499,h=447\), the first cover is
postponed until shifted digit 448.

The verified-prime exponent \(a=479\) gives a prime predecessor and a
structured multiplier that first fails in both bases \(2\) and \(3\) at
shifted digit 430. The primality status is taken from OEIS A257790; the
Lucas depths were independently computed here.

### Packing idea refined

The depth examples rule out assigning the Kraft weight \(p^{-d}\) only to
the observed first-failure path: that weight can be arbitrarily small.
Any packing proof must aggregate all first-failure cylinders belonging to a
prime.

### Finite global formulation

Proposition 20 replaces every full digit tower by a finite Lucas residue
box modulo a prime power. A witness is exactly a short representative in
the CRT intersection of these boxes. This shifts the next proof target to a
structured shortest-representative or discrepancy problem.

## 2026-07-26 — stage 8: sparse-box counterexample search

### Conjecture challenged computationally

The smallest-box search completely resolved 400 exponent cases for
\(M=2^\alpha3^\beta5^\gamma\), \(1\leq\alpha,\beta,\gamma\leq15\), and
tested 46,721 compatible multipliers without finding a witness. Three
additional barely-supercritical prime kernels also produced no witness in
their completely resolved exponent cases.

### Entropy shortcut falsified

The product-of-box-densities heuristic can be far below \(1\) even when a
witness exists. The exact expected-mass values at \(M=2088\) and \(36138\)
are recorded in `docs/brainstorm-stage8.md`.

### Character-sum reformulation

Proposition 21 applies a roots-of-unity filter to the digit-box generating
polynomial. It isolates the nontrivial character terms responsible for the
large discrepancy between raw box size and the actual number of compatible
multipliers.

## 2026-07-26 — stage 9: multi-base interaction

### One-box cancellation assumption rejected

At \(M=2952450\), the exact compatible count in the pivot box differs from
its entropy main term by less than \(0.1\%\), yet cross-base sieving removes
every candidate. Thus negative defect need not create a strong bias in any
single selected box.

### Pairwise-cover assumption rejected

At \(M=2400\) and \(4500\), every pair of prime-base pass sets intersects,
but the three-way intersection is empty. The new script
`scripts/scan_lucas_helly.py` measures the minimum certificate size, called
the Lucas cover degree in `docs/brainstorm-stage9.md`.

Through \(M\leq10000\), the cover-degree histogram is
\[
\lambda=1:243,\qquad \lambda=2:176,\qquad \lambda=3:2.
\]

### Full Fourier formulation

Proposition 23 expands the exact witness count into mixed Fourier
frequencies across all prime bases. The next question is whether negative
defect forces a certificate of bounded interaction order.

## 2026-07-26 — stage 10: adaptive three-base covers

### Selected-base search implemented

The finite smallest-box solver now handles arbitrary subsets of prime
bases. A separate direct search supplies explicit nonemptiness certificates
when the selected box is too large. The generalized solver is covered by
28 passing unit tests.

### Radical and defect invariance rejected

The values \(M=30,90,2400\) have the same radical \(30\) and the same
reciprocal defect \(-1\), but Lucas cover degrees \(1,2,3\). Cover degree
therefore depends essentially on the prime-power exponents.

### Degree-four searches

Structured exponent searches over four- and five-prime kernels found no
degree-four example. In every completely resolved case with empty full
intersection, some triple already had empty intersection. Detailed ranges
and near-miss scores are recorded in `docs/brainstorm-stage10.md`.

The exhaustive scan through \(M\leq20000\) found
\[
\lambda=1:454,\qquad\lambda=2:372,\qquad\lambda=3:3.
\]
The new degree-three example is \(M=14580\).

### Fixed smallest triple falsified

The proposed rule “the three smallest primes always kill” fails at
\[
M=33060,\qquad t=65.
\]
This multiplier passes bases \(2,3,5,29\) and fails base \(19\).
Nevertheless, \(M\) still has cover degree three.

### Three-base cover conjecture

The surviving conjecture is adaptive: negative defect should imply that
*some* triple of prime divisors has empty pass intersection. The compiled
falsifier found no counterexample through \(M=100000\), across 4,147
reciprocal-supercritical cases. Its closest case was \(M=21300\), where
two of four triples survive.

This conjecture would imply the reciprocal-threshold conjecture, and hence
the desired near-multiple conclusion whenever \(M-1\) is prime.

## 2026-07-26 — stage 11: defect-sensitive Helly behavior

### Adaptive conjecture extended to \(300000\)

The sequential compiled falsifier checked 12,572
reciprocal-supercritical \(M\leq300000\) without finding a case in which
every triple intersection survives. Only \(33060\) and \(68040\) require
moving past the three smallest primes.

### Universal degree-three bound falsified

Two positive-defect examples have cover degree exactly four:
\[
26187=3\cdot7\cdot29\cdot43,\qquad
60515=5\cdot7^2\cdot13\cdot19.
\]
Every triple has an explicit witness, while the four-way intersection is
empty. Thus the negative-defect hypothesis cannot be discarded.

### Exact cover-degree histograms

Among \(M\leq100000\) with at least four prime divisors and empty full
intersection, the degree counts are
\[
7097,\ 10445,\ 144,\ 2
\]
for degrees \(1,2,3,4\), respectively. No degree-five example appeared.

Restricting to all 4,147 reciprocal-supercritical \(M\leq100000\), the
exact histogram is
\[
\lambda=1:2147,\qquad\lambda=2:1995,\qquad\lambda=3:5.
\]
The degree-three examples are \(2400,4500,14580,33060,46080\).

### Pair isolation conjecture

An exact greedy selector had no failure through \(100000\), and its first
two selected bases always left at most one multiplier. This motivates the
pair-isolation conjecture
\[
D(\operatorname{rad}M)<0
\quad\Longrightarrow\quad
\min_{p\ne q}|\mathcal A_p\cap\mathcal A_q|\leq1.
\]

Sparse-box searches certified the conjecture in 446 additional structured
large-\(M\) cases; 1,422 cases remained unresolved at the chosen box-size
limit. No unresolved case is counted as evidence.

Complement symmetry proves that a singleton pair intersection corresponds
to only three or four compatible points in the full interval. This
four-point rigidity is the next proof target.

## 2026-07-26 — stage 12: defect ports and deep pair geometry

### Pair isolation extended to \(300000\)

The exact pass-mask scan checked all 12,572 reciprocal-supercritical
\(M\leq300000\). Its histogram is
\[
\lambda=1:6146,\qquad\lambda=2:6421,\qquad\lambda=3:5.
\]
The greedy pair intersection always had size at most one, and the same
five degree-three examples remained.

### Defect port formula

Proposition 25 expresses the first shifted digit exactly through
\(D(\operatorname{rad}M)\) and an exponent twist. The implementation is
cross-checked on every \(M<250\).

At the squarefree defect-\(-1\) boundary—the Giuga identity—the first
shifted digit is vacuous in every base. Exact higher-digit computations
give cover degrees \(1,2,2,1\) for \(30,858,1722,66198\).

### Uniform bounded depth ruled out completely

Proposition 27 constructs, for every fixed \(H\), a
reciprocal-supercritical \(M=30^e\) for which every multiplier passes the
first \(H\) shifted digits in every prime base. A proof of pair isolation
must therefore use depth growing with \(M\) or the full finite boxes.

For a blind first digit, Proposition 28 supplies an exact affine formula
for the second digit. Proposition 29 reduces every three-prime
supercritical case to \(M=2^a3^b5^c\).

### Current primary-pseudoperfect examples checked

The nine-factor example \(N_9=5998279018951962402\) from the May 2026
preprint has 255 admissible subset candidates; every one fails at the
second shifted digit. The inherited ten-factor example is covered by
Proposition 16. Neither has prime predecessor.

### Adversarial certificate search

A meet-in-the-middle search now looks for explicit positive
counterexample certificates rather than inferring emptiness from an
incomplete box. On the 1,000 vectors
\[
M=2^a3^b5^c,\qquad1\leq a,b,c\leq10,
\]
all 1,000 are now exactly certified to satisfy pair isolation. No
counterexample or unresolved vector remains in this finite cube.

The original reproducible \(100000\)-side, \(50000\)-candidate baseline
accounted for 914 exact cases, 78 cases with no feasible pivot, and 8
truncated cases. Tiered larger-cutoff passes resolved all 86. Pivot
ordering was improved, and early positive-certificate stops are now
conservatively marked incomplete; a regression test covers that
accounting rule. A single \(4.2\)-million-side, \(2.1\)-million-candidate
run independently reproduced all 1,000 exact certifications with an
empty unresolved list.

The solver also recovers the expected non-supercritical obstructions at
\(M=26187\) and \(60515\), providing a useful adversarial validation of
the search direction.

### Quantitative fixed-radical prefix obstruction

Proposition 30 proves that every fixed squarefree radical \(R\) has an
explicit family
\[
M_H=R^{C_RR^{H-1}},
\qquad
C_R=\operatorname{lcm}_{p\mid R}(p-1),
\]
on which all first \(H\) shifted digits are blind in every prime base.
For supercritical \(R\), the radical and negative defect remain fixed,
and the obstruction has depth \(\Omega(\log\log M_H)\).

The especially clean specialization
\[
M_H=210^{210^{H-1}}.
\]
The radical and defect stay fixed at \(210\) and \(-37\), while all
multipliers pass the first \(H\) digits in bases \(2,3,5,7\). Thus deep
prefix blindness is not confined to defect \(-1\), and along this family
the necessary depth exceeds
\[
1+\log_{210}\log_{210}M_H.
\]

This falsifies the proposed proof heuristic that \(D\leq-2\) should be
uniformly shallow—and in fact exponent synchronization creates the same
phenomenon at every fixed supercritical radical. The next focused
conjecture is pair isolation for the only three-prime supercritical
family \(2^a3^b5^c\).

### Exact blindness criterion and exponent blocks

Corollary 31 characterizes a completely blind prefix of any depth
\(H\leq v_p(M)\) by the single congruence
\[
M/p^{v_p(M)}\equiv1\pmod{p^H}.
\]
On \(M=30^e\), this yields the exact least synchronized exponent
\[
e_H=2^{H-4}3^{H-2}5^{H-1}\qquad(H\geq5).
\]

Proposition 32 decomposes a Lucas upper bound, as one prime exponent
grows, into two fixed boundary blocks separated by an expanding run of
digits \(p-1\). This “wildcard corridor” is a concrete full-depth
structure that a future transfer matrix may compress without imposing a
fixed depth. Proposition 33 gives the key limitation: no two prime bases
can enter the stabilized corridor regime simultaneously.

At any fixed depth \(H\geq4\), Proposition 35 reduces the truncated
three-base problem to a finite exponent torus with common period
\(30^{H-1}/2\). The period grows exponentially with depth, so this is an
algorithmic reduction rather than a uniform proof.

### Diagonal empty-pair conjecture

Completed base-\(2\) or base-\(3\) meet-in-the-middle enumerations prove
\[
\mathcal A_2\cap\mathcal A_3=\varnothing
\]
for \(M=30^e\), \(1\leq e\leq10\). This motivates Q6 for every \(e\).
The individual base-\(2\) pass-set sizes are highly nonmonotone, so a
cardinality induction is not supported by the data.
