# Stage 3 summary and creative directions

## Compressed state

We now have three nested reductions:

1. A strict hit needs at least three distinct prime factors unless a more
   complicated prime-power interaction is used.
2. Squarefree triples reduce to explicit single-prime Lucas witnesses.
3. If \(M-1\) is prime, then
   \[
   f(M(M-1))\in\{M-1,M\}.
   \]
   The smaller value occurs exactly when some
   \(\binom{M(M-1)}{Mt}\) is coprime to \(M\).

The third formulation is currently the most promising because
\[
M>\sqrt{M(M-1)}
\]
automatically. We only need to cover every multiplier \(t\) by at least one
prime divisor of \(M\).

## New proved construction

For a prime \(p\), let
\[
M=p(p^m-1).
\]
If \(M-1=p^{m+1}-p-1\) is prime, Proposition 13 proves
\[
f(M(M-1))=M.
\]

This shows that the binary construction was one instance of a base-\(p\)
digit-block phenomenon.

It remains conditional: no currently known theorem supplies infinitely many
prime values \(p^{m+1}-p-1\) with \(p\) prime.

## Failed affine generalization

The tempting replacement
\[
p^m-1\longrightarrow a p^m-1
\]
is false. For example,
\[
p=2,\quad m=3,\quad a=25
\]
gives \(M=398\), \(M-1=397\) prime, and multiplier \(t=47\) makes the gcd
equal to \(397\), not \(398\).

This failure is informative: preserving a block of trailing \(p-1\) digits
does not by itself control the higher blocks.

## High-leverage conjecture: the near-30 family

### Conjecture

If \(M\) is divisible by \(30\) and \(M-1\) is prime, then
\[
f(M(M-1))=M.
\]

Equivalently, for every \(1\leq t\leq(M-2)/2\), at least one prime divisor
of \(M\) divides
\[
\binom{M(M-1)}{Mt}.
\]

If this conjecture is true, Dirichlet's theorem supplies infinitely many
primes \(M-1\equiv-1\pmod{30}\), and the second question of Erdős Problem
700 has an unconditional affirmative answer.

### Evidence and falsification

- Exact reduced search found no counterexample for all \(b\leq10{,}000\)
  with \(M=30b\); this covers 3,260 prime values of \(M-1\).
- A stronger proposed lemma—that one of the fixed primes \(2,3,5\) always
  divides the binomial coefficient—is false. Its first sequential
  counterexample is
  \[
  M=33060,\qquad t=65.
  \]
  At this point the binomial coefficient is nonzero modulo \(2,3,5\), but
  it is zero modulo \(19\), another prime divisor of \(M\).
- Thus the data suggests a dynamic covering mechanism: factors introduced
  by \(b\) repair gaps left by \(2,3,5\).

The conjecture remains just that. The computational range is not a proof,
and the strength of its consequence demands especially skeptical checking.

## Composite-\(r\) lesson

For the earlier binary sequence
\[
n_m=2(2^m-1)(2^{m+1}-3),
\]
composite \(r=2^{m+1}-3\) behaves in two ways:

- \(m=6\), where \(r=125\), remains a strict hit;
- \(m=7\), where \(r=11\cdot23\), fails with \(f(n)=46\);
- \(m=17\), where \(r=11\cdot23831\), has a candidate gcd as small as \(22\).

Splitting \(r\) into separated prime factors can create very small gcds.
Prime powers appear less destructive, but there is not yet a theorem.

## Next creative attacks

### 1. Carry-cover theorem for \(M=30b\)

Translate the conjecture into Kummer carries. For every \(t\), prove that
the addition defining \(\binom{M(M-1)}{Mt}\) has a carry in at least one
base \(p\mid M\).

The failed fixed-\(\{2,3,5\}\) lemma suggests an induction on the prime
factors of \(b\): whenever a multiplier escapes the existing bases, show
that its escape pattern forces a carry in a newly introduced prime base.

### 2. Minimal counterexample descent

Assume a least \(M=30b\) and multiplier \(t\) for which the binomial is
coprime to \(M\). Lucas digit containment holds in every base \(p\mid M\).
Try to use a divisor \(d\mid M\) to construct a smaller counterexample,
contradicting minimality.

### 3. Finite automata and synchronized digits

For fixed primes \(2,3,5\), Lucas nondivisibility is recognized by a finite
digit automaton in each base. The intersection of different-base conditions
is difficult, but the special polynomial pair
\[
N=M(M-1),\qquad K=Mt
\]
may admit a smaller transducer operating on carries rather than full digits.
Machine-discovered invariants could then be translated into a proof.

### 4. Search for a smaller Dirichlet modulus

Experimentally identify residue classes \(M\equiv0\pmod L\) for which the
near-multiple conjecture always appears true. A smaller \(L\), or several
covering residue classes, may expose the actual invariant more clearly than
\(L=30\).

## Literature/status caution

The current Erdős Problems discussion already considers \(n=q(q+1)\) and
conditional digit constructions, but explicitly labels comments as
unverified. It does not presently contain a verified infinite family.
Before claiming novelty, every proposed theorem here needs external review
and a full literature check.
