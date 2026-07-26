# Mathematical notes

## 1. Definition

For \(n\geq4\), let

\[
f(n)=\min_{2\leq k\leq\lfloor n/2\rfloor}
\gcd\left(n,\binom nk\right).
\]

Write \(v_p(m)\) for the exponent of the prime \(p\) in \(m\).
If \(n=\prod_{p\mid n}p^{a_p}\), then for a fixed \(k\),

\[
\gcd\left(n,\binom nk\right)
=\prod_{p\mid n}p^{\min(a_p,v_p(\binom nk))}.
\]

The outer minimum is numerical and must be taken after this product is
evaluated.

## 2. Computing binomial valuations

Legendre's formula gives

\[
v_p(m!)=\sum_{j\geq1}\left\lfloor\frac{m}{p^j}\right\rfloor,
\]

and hence

\[
v_p\binom nk=v_p(n!)-v_p(k!)-v_p((n-k)!).
\]

Kummer's theorem gives a complementary interpretation:
\(v_p\binom nk\) is the number of carries when adding \(k\) and \(n-k\) in
base \(p\).

## 3. Prime powers

### Lemma 1 — valuation identity

**Proved.** If \(n=p^a\) and \(0<k<p^a\), then

\[
v_p\binom{p^a}{k}=a-v_p(k).
\]

#### Proof

Use

\[
\binom{p^a}{k}=\frac{p^a}{k}\binom{p^a-1}{k-1}.
\]

It remains to show that \(p\nmid\binom{p^a-1}{k-1}\). In base \(p\),
\(p^a-1\) has every digit equal to \(p-1\). Lucas's theorem therefore gives

\[
\binom{p^a-1}{k-1}
\equiv
\prod_i\binom{p-1}{d_i}\not\equiv0\pmod p,
\]

where the \(d_i\) are the base-\(p\) digits of \(k-1\). Thus the second
factor has \(p\)-adic valuation zero, while \(p^a/k\) has valuation
\(a-v_p(k)\). ∎

### Corollary 2 — value on composite prime powers

**Proved.** If \(a\geq2\), then

\[
f(p^a)=p.
\]

#### Proof

Lemma 1 shows that every admissible \(k\) gives a positive valuation, so
\(\gcd(p^a,\binom{p^a}{k})\geq p\).

If \(p=2\), choose \(k=2^{a-1}=p^a/2\). If \(p\) is odd, choose
\(k=p^{a-1}<p^a/2\). In either case \(v_p(k)=a-1\), so Lemma 1 gives
\(v_p\binom{p^a}{k}=1\). The corresponding gcd is \(p\). ∎

### Consequence for the square-root threshold

For \(n=p^2\),

\[
f(n)=p=\sqrt n.
\]

This proves infinitely many examples at equality, but it says nothing by
itself about the strict inequality \(f(n)>\sqrt n\).

## 4. Immediate target: \(p^a q^b\)

For distinct primes \(p<q\), the next task is to understand

\[
\min_k
p^{\min(a,v_p(\binom{p^a q^b}{k}))}
q^{\min(b,v_q(\binom{p^a q^b}{k}))}.
\]

The difficulty is simultaneous: a \(k\) favorable at \(p\) need not be
favorable at \(q\). We will record the complete set of minimizing \(k\)'s to
look for compatible base-\(p\) and base-\(q\) digit patterns.

### Lemma 3 — a prime-power witness

**Proved.** If \(p^a\parallel n\), then

\[
\gcd\left(n,\binom{n}{p^a}\right)=\frac{n}{p^a}.
\]

Consequently,

\[
f(n)\leq \frac{n}{p^a}
\]

whenever \(p^a\leq n/2\).

#### Proof

Write \(n=p^a m\), where \(p\nmid m\). The identity

\[
\binom{n}{p^a}=m\binom{n-1}{p^a-1}
\]

shows that \(m\mid\binom{n}{p^a}\).

It remains to prove that \(p\nmid\binom{n-1}{p^a-1}\). The final \(a\)
base-\(p\) digits of both \(n-1\) and \(p^a-1\) are all \(p-1\), while all
higher digits of \(p^a-1\) are zero. Lucas's theorem therefore shows that
the binomial coefficient is nonzero modulo \(p\).

Thus the binomial coefficient contains the full factor \(m\) but no
additional factor \(p\), and its gcd with \(p^a m\) is exactly \(m\). ∎

### Lemma 4 — universal smallest-prime lower bound

**Proved.** If \(n\) is composite and \(p(n)\) is its smallest prime factor,
then

\[
f(n)\geq p(n).
\]

#### Proof

Suppose that \(\gcd(n,\binom nk)=1\) for some \(0<k<n\). For every
\(p^a\parallel n\), the binomial coefficient is then nonzero modulo \(p\).
The final \(a\) base-\(p\) digits of \(n\) are zero, so Lucas's theorem
forces the corresponding digits of \(k\) to be zero. Hence \(p^a\mid k\).

This holds for every full prime-power component of \(n\), which are pairwise
coprime, so \(n\mid k\). That contradicts \(0<k<n\). The gcd is therefore
a nontrivial divisor of \(n\), and so is at least its smallest prime
factor. ∎

### Corollary 5 — two prime-power components cannot cross the square root

**Proved.** If \(n=p^a q^b\) for distinct primes \(p,q\), then

\[
f(n)\leq\min(p^a,q^b)\leq\sqrt n.
\]

#### Proof

Apply Lemma 3 using the larger of the two numbers \(p^a,q^b\). It is
admissible because each prime-power component is at most \(n/2\). The
resulting gcd is the other, smaller component. Their minimum cannot exceed
their geometric mean \(\sqrt n\). ∎

In particular, every integer satisfying \(f(n)>\sqrt n\) must have at least
three distinct prime factors.

### Proposition 6 — the squarefree two-prime case

**Proved.** If \(p<q\) are primes, then

\[
f(pq)=p.
\]

#### Proof

For any \(0<k<pq\), suppose first that
\(\binom{pq}{k}\not\equiv0\pmod p\). Because the final base-\(p\) digit of
\(pq\) is zero, Lucas's theorem forces the final digit of \(k\) to be zero;
therefore \(p\mid k\). Similarly,
\(\binom{pq}{k}\not\equiv0\pmod q\) would force \(q\mid k\).

The binomial coefficient cannot be nonzero modulo both \(p\) and \(q\):
that would imply \(pq\mid k\), contradicting \(0<k<pq\). Hence its gcd with
\(pq\) is at least the smaller prime \(p\).

On the other hand, Lemma 3 with \(q^1\parallel pq\) and \(k=q\) gives a
gcd of \(p\). Thus the minimum is \(p\). ∎

### Proposition 7 — exact reduction for squarefree triples

**Proved.** Let \(p<q<r\) be primes. Then

\[
f(pqr)>\sqrt{pqr}
\quad\Longleftrightarrow\quad
r<pq\ \text{ and }\ f(pqr)=pq.
\]

#### Proof

Lemma 3 with \(k=r\) gives \(f(pqr)\leq pq\). By Lemma 4, \(f(pqr)\) is a
nontrivial divisor of \(pqr\).

If \(f(pqr)>\sqrt{pqr}\), then the upper bound \(f(pqr)\leq pq\) implies
\(pq>\sqrt{pqr}\), equivalently \(pq>r\). Under this inequality, all three
one-prime divisors are below \(\sqrt{pqr}\), while the two-prime divisors
\(pr\) and \(qr\) exceed the upper bound \(pq\). Hence the only possible
value of \(f(pqr)\) above the square root is \(pq\).

Conversely, if \(r<pq\) and \(f(pqr)=pq\), then
\[
pq>\sqrt{pqr}\quad\Longleftrightarrow\quad pq>r.
\]
Thus \(f(pqr)>\sqrt{pqr}\). ∎

### Proposition 8 — short Lucas search for a squarefree triple

**Proved.** Let \(p<q<r\) be primes. To determine \(f(pqr)\), it suffices
to begin with the upper bound \(pq\) and check candidates of the forms

\[
k=tqr\quad(1\leq t\leq p/2),\qquad
k=tpr\quad(1\leq t\leq q/2),\qquad
k=tpq\quad(1\leq t\leq r/2).
\]

For each candidate, Lucas's digit criterion determines whether the gcd is
respectively \(p\), \(q\), or \(r\). Therefore only
\[
\left\lfloor\frac p2\right\rfloor+
\left\lfloor\frac q2\right\rfloor+
\left\lfloor\frac r2\right\rfloor
\]
values need to be tested instead of \(O(pqr)\).

#### Proof

Lemma 3 gives \(f(pqr)\leq pq\), and Lemma 4 excludes gcd \(1\). The divisors
\(pr,qr,pqr\) are larger than \(pq\), so the only possible improvements are
the single primes \(p,q,r\).

Suppose the gcd is \(p\). The binomial coefficient is then nonzero modulo
both \(q\) and \(r\). Lucas's theorem, together with \(q\mid n\) and
\(r\mid n\), forces \(q\mid k\) and \(r\mid k\); hence \(k=tqr\).
The condition \(k\leq n/2\) gives \(t\leq p/2\). Lucas's full digitwise
criterion decides whether the binomial coefficient is nonzero modulo
\(q,r\) and zero modulo \(p\). The other two cases are identical. ∎

### Proposition 9 — explicit criterion for \(2qr\)

**Proved.** Let \(q<r<2q\) be odd primes and put \(n=2qr\). Then:

1. No admissible \(k\) has
   \[
   \gcd\left(n,\binom nk\right)=2.
   \]
2. A gcd equal to \(q\) occurs exactly when there is an integer
   \[
   1\leq t\leq\left\lfloor\frac{2q-r}{2}\right\rfloor
   \]
   such that
   \[
   rt\mathbin{\&}\mathord{\sim}(qr)=0.
   \]
   The corresponding \(k\) is \(2rt\).
3. A gcd equal to \(r\) occurs exactly when there is an integer
   \(1\leq t\leq\lfloor r/2\rfloor\) such that
   \[
   qt\mathbin{\&}\mathord{\sim}(qr)=0
   \]
   and
   \[
   \binom{2r}{2t}\not\equiv0\pmod q.
   \]
   The corresponding \(k\) is \(2qt\).

Consequently,
\[
f(2qr)=2q
\]
if and only if neither type of witness in parts 2 and 3 exists.

Here \(x\mathbin{\&}\mathord{\sim}y=0\) means that every \(1\)-bit of \(x\)
is also a \(1\)-bit of \(y\).

#### Proof

By Proposition 8, a gcd \(2\) could occur only at \(k=qr=n/2\). Write
\[
d=2q-r,
\qquad 0<d<q.
\]
In base \(r\), the final digits of \(n=2qr\) are \((0,d,1)\), whereas those
of \(k=qr\) are \((0,q)\). Since \(q>d\), Lucas's theorem shows that
\(\binom nk\equiv0\pmod r\). Thus the gcd cannot be \(2\).

For a gcd \(q\), Proposition 8 gives \(k=2rt\). After removing a trailing
base-\(r\) zero, Lucas's criterion modulo \(r\) compares the base-\(r\)
digits of \(2t\) with those of \(2q\). Because \(2q=r+d\) and
\(2t<r\), it is nonzero precisely when \(2t\leq d\). Divisibility modulo
\(q\) is automatic: \(q\mid n\) but \(q\nmid k\), since \(t<q\).
Nondivisibility modulo \(2\) is, after removing a binary trailing zero,
exactly the displayed bitwise condition on \(rt\) and \(qr\).

For a gcd \(r\), Proposition 8 gives \(k=2qt\). Divisibility modulo \(r\)
is automatic because \(r\mid n\) but \(r\nmid k\). Removing the common
trailing zero in base \(q\) reduces nondivisibility modulo \(q\) to
\[
\binom{2r}{2t}\not\equiv0\pmod q.
\]
The remaining nondivisibility condition modulo \(2\) is the displayed
bitwise condition on \(qt\) and \(qr\). ∎

For \(q\geq5\), the last Lucas condition has the simpler form
\[
(2t\bmod q)\leq(2r\bmod q).
\]
Indeed \(2r<4q\), \(2t<2q\), and the higher base-\(q\) digit of \(2t\) is
automatically no larger than that of \(2r\).

### Proposition 10 — a conditional binary family

**Proved.** Let \(m\geq2\), and suppose that
\[
q=2^m-1,\qquad r=2^{m+1}-3
\]
are both prime. Then
\[
f(2qr)=2q>\sqrt{2qr}.
\]

#### Proof

We have \(r=2q-1\), so \(q<r<2q\). Proposition 9 applies. Its range for a
gcd-\(q\) witness is empty because
\[
\left\lfloor\frac{2q-r}{2}\right\rfloor
=\left\lfloor\frac12\right\rfloor=0.
\]

It remains to exclude a gcd-\(r\) witness. First assume \(m\geq3\). Such a
witness would require, for some \(1\leq t\leq q-1\),
\[
qt\mathbin{\&}\mathord{\sim}(qr)=0.
\]
Now
\[
qr=(2^{m+1}-5)2^m+3.
\]
Thus its final \(m\) binary digits are zero except for the last two, which
are \(11\). On the other hand,
\[
qt=(t-1)2^m+(2^m-t).
\]
For its final \(m\) bits to be a submask of \(11\), and because
\(1\leq t\leq2^m-2\), we must have
\[
2^m-t\in\{2,3\}.
\]
Hence \(t=2^m-2\) or \(t=2^m-3\).

In the first case the upper block \(t-1=2^m-3\) has binary bit \(2\) set;
in the second case \(t-1=2^m-4\) also has bit \(2\) set. But the corresponding
bit of \(2^{m+1}-5\) is zero, since
\[
2^{m+1}-5\equiv3\pmod8.
\]
Thus neither candidate is a submask, a contradiction.

For \(m=2\), we have \((q,r)=(3,5)\); the two finite witness ranges in
Proposition 9 can be checked directly and are empty.

There are therefore no single-prime witnesses, so Proposition 9 gives
\(f(2qr)=2q\). Finally \(r<2q\) implies
\[
(2q)^2>2qr.
\]
∎

This is not yet an infinite-family proof: it is unknown whether both
\(2^m-1\) and \(2^{m+1}-3\) are prime for infinitely many \(m\). Exact
computation gives simultaneous-prime examples at least for
\[
m=2,3,5,13,19.
\]

### Proposition 11 — only the second binary factor must be prime

**Proved.** Let \(m\geq2\), set
\[
q=2^m-1,\qquad r=2^{m+1}-3=2q-1,
\]
and suppose only that \(r\) is prime. Then, even if \(q\) is composite,
\[
f(2qr)=2q>\sqrt{2qr}.
\]

#### Proof

The choice \(k=r\) and Lemma 3 give the upper bound \(f(2qr)\leq2q\).

Consider any admissible \(k\) for which
\(\binom{2qr}{k}\not\equiv0\pmod r\). Since \(r\mid2qr\), Lucas's theorem
first forces \(r\mid k\), say \(k=rt\). We have \(t\leq q<r\). In base \(r\),
\[
2qr=r(r+1)
\]
has digits \((0,1,1)\), while \(rt\) has digits \((0,t)\). Lucas's criterion
therefore forces \(t\leq1\), and hence \(k=r\). Lemma 3 says the gcd at this
unique value is exactly \(2q\).

Every other \(k\) gives a gcd divisible by \(r=2q-1\). If this gcd were
smaller than \(2q\), it would have to equal \(r\), since multiplying \(r\)
by any further prime factor gives at least \(2r>2q\).

Suppose for contradiction that the gcd equals \(r\). The binomial
coefficient is then nonzero modulo every prime dividing \(2q\). Applying
Lucas's theorem to every full prime-power component of \(2q\), as in
Lemma 4, forces \(2q\mid k\). Write \(k=2qt\); admissibility gives
\(1\leq t\leq q-1\). Nondivisibility modulo \(2\) would require
\[
qt\mathbin{\&}\mathord{\sim}(qr)=0.
\]
The binary-block argument in Proposition 10 proves that no such \(t\) exists
for \(m\geq3\). The case \(m=2\) is checked directly. Thus gcd \(r\) is
impossible, completing the lower bound \(f(2qr)\geq2q\).

Finally \(r<2q\), so \((2q)^2>2qr\). ∎

The remaining number-theoretic obstacle is external to the binomial-gcd
analysis: it is not known whether \(2^a-3\) is prime for infinitely many
exponents \(a\). For \(2\leq m\leq25\), exact trial division finds prime
\(r\) at
\[
m=2,3,4,5,8,9,11,13,19,21,23.
\]

## 5. Near-multiple construction

### Proposition 12 — two-value reduction

**Proved.** Let \(M\geq4\) and suppose \(r=M-1\) is prime. Then
\[
f(Mr)\in\{r,M\}.
\]
More precisely, \(f(Mr)=r\) if and only if there is an integer
\(1\leq t\leq r/2\) such that
\[
\binom{Mr}{Mt}
\]
is coprime to \(M\). Otherwise \(f(Mr)=M\).

#### Proof

The choice \(k=r\) and Lemma 3 give a gcd of \(M\). If a binomial
coefficient is nonzero modulo \(r\), Lucas's theorem first forces \(r\mid k\).
Writing \(k=rt\), admissibility gives \(t\leq M/2<r\). In base \(r\),
\[
Mr=r(r+1)
\]
has digits \((0,1,1)\), so Lucas's theorem forces \(t\leq1\). Thus \(k=r\)
is the only admissible value whose gcd does not contain \(r\).

At every other \(k\), the gcd is divisible by \(r=M-1\). It is below \(M\)
only if it equals \(r\). For this to happen the binomial coefficient must be
nonzero modulo every prime dividing \(M\). Lemma 4's digit argument then
forces every full prime-power component of \(M\) to divide \(k\), hence
\(k=Mt\). Conversely, coprimality to \(M\) at such a \(k\) gives gcd exactly
\(r\). ∎

This reduction is implemented by `analyze_near_multiple`.

### Proposition 13 — prime-base construction

**Proved.** Let \(p\) be prime and \(m\geq1\). Set
\[
M=p(p^m-1)
\]
and suppose
\[
r=M-1=p^{m+1}-p-1
\]
is prime. Then
\[
f(Mr)=M>\sqrt{Mr}.
\]

#### Proof sketch

By Proposition 12, it is enough to exclude a multiplier
\(1\leq t\leq r/2\) for which \(\binom{Mr}{Mt}\) is coprime to \(M\).
In particular it would have to be nonzero modulo \(p\). Removing the common
trailing base-\(p\) zero reduces this to the digitwise condition
\[
(p^m-1)t\preceq_p (p^m-1)r,
\]
where \(x\preceq_p y\) means every base-\(p\) digit of \(x\) is at most the
corresponding digit of \(y\).

For \(m\geq2\), put \(P=p^m\) and write \(t=cP+b\), \(0\leq b<P\).
The final \(m\) digits of
\[
(P-1)r=(pP-2p-1)P+(p+1)
\]
represent \(p+1\). Therefore the final block of \((P-1)t\) can pass Lucas's
test only when
\[
b\in\{0,P-1,P-p,P-p-1\}.
\]
In each of these four cases, direct subtraction in the next base-\(p\)
block gives digit \(p-1\) or \(p-2\) in position \(1\), whereas the same
digit of \(pP-2p-1\) is \(p-3\). Thus Lucas's test fails. The bounds on
\(c\) coming from \(t\leq r/2\) ensure no extra leading carry enters this
comparison.

When \(m=1\), the last three digits of
\[
(p-1)(p^2-p-1)
\]
are \((1,0,p-2)\). Passing Lucas would require
\((p-1)t\equiv0\) or \(1\pmod{p^2}\). The first case forces
\(t\equiv0\pmod{p^2}\), and the second forces
\(t\equiv p^2-p-1=r\pmod{p^2}\); both contradict \(1\leq t\leq r/2\).

The case \(p=2\) is also the binary-block argument of Proposition 11.
Hence the binomial coefficient is always divisible by \(p\), so no witness
from Proposition 12 exists. Finally \(M=r+1>\sqrt{Mr}\). ∎

### Proposition 14 — exact Lucas-prefix obstruction

**Proved.** Let \(p^a\parallel M\), put \(u=M/p^a\), and let
\(1\leq t\leq(M-1)/2\). Then
\[
\binom{M(M-1)}{Mt}\not\equiv0\pmod p
\]
if and only if, for every \(h\geq1\),
\[
ut\bmod p^h\ \leq\ u(M-1)\bmod p^h.
\]
In particular, nondivisibility implies the finite-level condition
\[
\left\{\frac{ut}{p^a}\right\}
+\left\{\frac{u}{p^a}\right\}\leq1.
\]

#### Proof

Both arguments of the binomial coefficient contain \(p^a\):
\[
M(M-1)=p^a u(M-1),\qquad Mt=p^a ut.
\]
Their final \(a\) base-\(p\) digits are therefore zero. Removing these
common trailing zeroes, Lucas's theorem says precisely that every base-\(p\)
digit of \(ut\) is at most the corresponding digit of \(u(M-1)\).
Comparing every suffix of \(h\) digits is equivalent to
\[
ut\bmod p^h\leq u(M-1)\bmod p^h
\]
for every \(h\geq1\).

At \(h=a\), since \(M=p^a u\),
\[
u(M-1)\equiv-u\pmod{p^a}.
\]
Because \(p\nmid u\), the least nonnegative residue on the right is
\(p^a-(u\bmod p^a)\). Thus
\[
(ut\bmod p^a)+(u\bmod p^a)\leq p^a,
\]
which is the stated fractional-part inequality. ∎

The last inequality is only a necessary relaxation, not a sufficient one.
For \(M=30,t=1\), it holds for every \(p\mid30\), but the full Lucas test
fails in base \(2\) at a higher digit. Any proof based on Proposition 14
must therefore use the nested system of prefix inequalities rather than
only the level \(h=a\).

### Proposition 15 — primary-pseudoperfect subset-sum reduction

**Proved.** Suppose \(M\) satisfies
\[
1+\sum_{p\mid M}\frac{M}{p}=M. \tag{1}
\]
If
\[
\binom{M(M-1)}{Mt}
\]
is nonzero modulo every prime divisor of \(M\), then there is a subset
\(S\) of the prime divisors of \(M\) such that
\[
t=\sum_{p\in S}\frac{M}{p}.
\]
Thus only a finite list of at most \(2^{\omega(M)}\) subset sums can be
near-multiple witnesses.

#### Proof

First, (1) forces \(M\) to be squarefree. If \(p^2\mid M\), then every
term \(M/q\) in (1) is divisible by \(p\), including the term with \(q=p\).
Reducing (1) modulo \(p\) would give \(1\equiv0\pmod p\), a contradiction.

Fix \(p\mid M\) and put \(u=M/p\). Reducing (1) modulo \(p\), every term
other than \(1\) and \(M/p\) vanishes, so
\[
u\equiv-1\pmod p. \tag{2}
\]
After removing the common trailing base-\(p\) zero from the two arguments,
the units-digit part of Lucas's criterion is
\[
ut\bmod p\leq u(M-1)\bmod p.
\]
By (2), the right side is \(1\), while the left side is
\(-t\bmod p\). Hence
\[
t\equiv0\ \text{or}\ -1\pmod p. \tag{3}
\]

Let \(S\) contain exactly the primes for which the second alternative in
(3) holds, and set
\[
T=\sum_{p\in S}\frac{M}{p}.
\]
Equation (2) shows that \(T\equiv-1\pmod p\) for \(p\in S\), while
\(T\equiv0\pmod p\) for \(p\notin S\). Therefore \(T\equiv t\pmod M\)
by the Chinese remainder theorem. Both lie in \([0,M-1]\), since (1) gives
\[
\sum_{p\mid M}\frac{M}{p}=M-1.
\]
Consequently \(T=t\). ∎

Numbers satisfying (1) are called **primary pseudoperfect numbers**. The
reduction is implemented by `primary_pseudoperfect_candidates`. It does not
by itself eliminate the subset sums: higher base-\(p\) digits must still be
checked.

### Proposition 16 — one-prime inheritance has a two-digit cover

**Proved.** Let \(K\) be primary pseudoperfect, suppose \(q=K+1\) is
prime, and put
\[
M=Kq.
\]
Then \(M\) is primary pseudoperfect, and for every
\[
1\leq t\leq(M-1)/2
\]
at least one prime divisor of \(M\) divides
\[
\binom{M(M-1)}{Mt}.
\]
In fact, after Proposition 15 reduces \(t\) to a subset sum, the new prime
\(q\) always supplies a Lucas failure at the second shifted base-\(q\)
digit.

#### Proof

The primary-pseudoperfect identity for \(K\) gives
\[
\sum_{p\mid K}\frac{K}{p}=K-1.
\]
Since \(q=K+1\),
\[
\frac1M+\sum_{p\mid M}\frac1p
=\frac1{Kq}+\sum_{p\mid K}\frac1p+\frac1q
=1,
\]
so \(M\) is primary pseudoperfect.

Suppose the displayed binomial coefficient is nonzero modulo every
\(p\mid M\). Proposition 15 writes its multiplier as
\[
t=qT+\varepsilon K,\qquad
T=\sum_{p\in S}\frac{K}{p},\qquad \varepsilon\in\{0,1\},
\]
where \(S\) is a subset of the prime divisors of \(K\). In particular,
\[
0\leq T\leq K-1=q-2.
\]

Apply Lucas's criterion in base \(q\). After removing the common trailing
zero, the upper argument is
\[
A=K(M-1)=(q-1)\bigl(q(q-1)-1\bigr)\equiv1\pmod{q^2}.
\]
The lower argument is \(B=Kt=(q-1)t\).

If \(\varepsilon=0\), then
\[
B\equiv-qT\pmod{q^2}.
\]
The two-digit prefix inequality \(B\bmod q^2\leq A\bmod q^2=1\) is possible
only when \(T=0\), which gives \(t=0\).

If \(\varepsilon=1\), then
\[
B\equiv1-q(T+2)\pmod{q^2}.
\]
The prefix inequality is possible only when \(T=q-2=K-1\), which means
that \(S\) contains every prime divisor of \(K\). It then gives
\(t=M-1\).

Both surviving formal possibilities lie outside
\(1\leq t\leq(M-1)/2\). Hence every admissible subset sum fails Lucas's
criterion modulo \(q\), proving the claim. ∎

If \(M-1\) is additionally prime, Proposition 12 immediately gives
\[
f(M(M-1))=M>\sqrt{M(M-1)}.
\]
The extra primality is not asserted by Proposition 16.

### Proposition 17 — the reciprocal threshold is an integer defect

**Proved.** Let \(R>1\) be squarefree and define
\[
\partial R=\sum_{p\mid R}\frac Rp,\qquad D(R)=R-\partial R.
\]
Then \(D(R)\neq0\), and
\[
\sum_{p\mid R}\frac1p>1
\quad\Longleftrightarrow\quad
D(R)\leq-1.
\]
Similarly, a primary pseudoperfect number is exactly a squarefree \(R\)
with
\[
D(R)=1.
\]

#### Proof

The equivalences follow by dividing the definition of \(D(R)\) by \(R\),
apart from the claim that equality cannot occur. If \(D(R)=0\), then
\[
\sum_{q\mid R}\frac Rq=R.
\]
Fix \(p\mid R\) and reduce modulo \(p\). Every summand with \(q\neq p\)
vanishes, leaving
\[
\frac Rp\equiv0\pmod p.
\]
This contradicts squarefreeness. Hence the integer \(D(R)\) skips zero.
The primary-pseudoperfect identity is precisely
\(\partial R=R-1\), or \(D(R)=1\). ∎

For arbitrary \(M\), take \(R=\operatorname{rad}(M)\). The
reciprocal-threshold conjecture can now be stated without fractions:

> If a common near-multiple Lucas witness exists, then
> \(D(\operatorname{rad}(M))\geq1\).

The function `reciprocal_defect` computes this quantity exactly.

### Proposition 18 — no uniform finite-prefix certificate

**Proved.** For every positive integer \(H\), there are \(M\) and an
admissible multiplier \(t\) such that
\[
\sum_{p\mid M}\frac1p>1
\]
and the first \(H\) shifted Lucas digits pass for every \(p\mid M\).
Consequently, no fixed finite number of initial digit levels can prove the
stronger reciprocal-threshold covering statement for all \(M\).

#### Proof

Choose \(h\geq H\) with \(h\not\equiv3\pmod5\), and then choose \(a\) so
large that
\[
5^a>6^{h+1}.
\]
Set
\[
M=6\cdot5^a,\qquad t=6^h.
\]
Certainly \(1\leq t\leq(M-1)/2\), and
\[
\frac12+\frac13+\frac15=\frac{31}{30}>1.
\]

For \(p=2\), after removing the single trailing base-\(2\) zero, the lower
argument is
\[
\frac M2t=3\cdot5^a\,6^h,
\]
which is zero modulo \(2^h\). Hence its first \(h\) shifted binary digits
are zero and pass Lucas's test. The same argument in base \(3\) uses
\(3^h\mid t\).

For \(p=5\), remove the \(a\) trailing zeroes. The two arguments become
\[
A=6(M-1)=36\cdot5^a-6,\qquad B=6t=6^{h+1}.
\]
Because \(B<5^a\), it occupies only the final \(a\) base-\(5\) positions.
Those digits of \(A\) are the digits of \(5^a-6\): all are \(4\), except
the \(5^1\)-digit, which is \(3\). Thus \(B\) passes digitwise unless its
\(5^1\)-digit is \(4\).

The powers of \(6\) modulo \(25\) cycle as
\[
6,11,16,21,1.
\]
The forbidden \(5^1\)-digit occurs only for residue \(21=(41)_5\), i.e.
when \(h+1\equiv4\pmod5\). Our choice \(h\not\equiv3\pmod5\) excludes it.
Therefore the full Lucas test passes modulo \(5\), while the first \(h\)
shifted digits pass modulo \(2\) and \(3\). ∎

This proposition does **not** impose primality of \(M-1\). It rules out a
bounded-prefix proof of the stronger all-\(M\) covering statement, but a
separate bounded-depth theorem restricted to prime predecessors is not
logically excluded.

### Proposition 19 — explicit third-prefix formula at defect one

**Proved.** Let \(M\) be primary pseudoperfect, let \(p\mid M\), and put
\[
u=\frac Mp=pc-1.
\]
For a subset candidate from Proposition 15, write
\[
t=pE\quad(p\notin S),\qquad
t=u+pE\quad(p\in S),
\]
where
\[
E=\sum_{q\in S\setminus\{p\}}\frac{M}{pq}.
\]
After removing the forced trailing zero, let \(A=u(M-1)\) and \(B=ut\).
Modulo \(p^3\),
\[
A\equiv1+p(1-c)-2p^2c,
\]
and
\[
B\equiv
\begin{cases}
-pE+p^2cE,&p\notin S,\\
1-p(2c+E)+p^2(c^2+cE),&p\in S.
\end{cases}
\pmod{p^3}.
\]

#### Proof

Since \(M=pu\),
\[
A=u(pu-1)=pu^2-u.
\]
Substituting \(u=pc-1\) and discarding multiples of \(p^3\) gives the first
formula. If \(p\notin S\), then \(B=u(pE)\); if \(p\in S\), then
\(B=u(u+pE)\). Expanding these expressions gives the other two formulas.
∎

Together with the corresponding reductions modulo \(p\) and \(p^2\), the
formula gives an exact three-shifted-digit certificate: a candidate passes
the first three shifted digits precisely when the prefix inequalities hold
at \(p,p^2,p^3\). A comparison only modulo \(p^3\) is not sufficient by
itself; all shorter prefixes must also pass.

### Proposition 20 — finite CRT-box formulation

**Proved.** Let \(p^a\parallel M\), put \(u_p=M/p^a\), and define
\[
A_p=u_p(M-1).
\]
Let \(Q_p\) be the least power of \(p\) strictly larger than \(A_p\), and
let
\[
\mathcal D_p(A_p)=
\{b\in[0,Q_p):\text{ every base-\(p\) digit of \(b\) is at most the
corresponding digit of \(A_p\)}\}.
\]
Finally set
\[
\mathcal T_p=u_p^{-1}\mathcal D_p(A_p)\pmod{Q_p}.
\]
Then a multiplier \(1\leq t\leq(M-1)/2\) is a common near-multiple witness
if and only if
\[
t\bmod Q_p\in\mathcal T_p
\qquad\text{for every }p\mid M.
\]
If \(A_p=\sum_i A_{p,i}p^i\), then
\[
|\mathcal T_p|=|\mathcal D_p(A_p)|
=\prod_i(A_{p,i}+1).
\]

#### Proof

Proposition 14 removes the \(a\) common trailing zeroes and reduces the
Lucas condition to
\[
u_pt\preceq_p A_p.
\]
Since \(t\leq M-1\), we have \(u_pt\leq A_p<Q_p\). Thus this condition is
equivalent to \(u_pt\in\mathcal D_p(A_p)\). Because \(p\nmid u_p\),
multiplication by \(u_p\) is invertible modulo \(Q_p\), giving the claimed
residue condition.

The moduli \(Q_p\) for distinct primes are pairwise coprime. Hence the
simultaneous conditions are an exact finite Chinese-remainder intersection,
not an approximation to the full digit towers. The cardinality formula
follows by choosing the digit \(b_i\) independently from
\(\{0,\ldots,A_{p,i}\}\). ∎

This formulation reconciles Proposition 18 with a finite computation: the
number of required digits is finite for each \(M\), but cannot be bounded
uniformly. The reciprocal-threshold conjecture asks why negative defect
prevents the CRT intersection from having a representative in the first
half-interval.

### Proposition 21 — character filter for compatible box values

**Proved.** Retain the notation of Proposition 20 for one prime
\(p^a\parallel M\), and write
\[
A_p=\sum_i A_{p,i}p^i,\qquad u=M/p^a.
\]
Define the digit-box polynomial
\[
F_p(x)=\prod_i\left(1+x^{p^i}+\cdots+x^{A_{p,i}p^i}\right).
\]
The number \(N_p\) of values \(b\in\mathcal D_p(A_p)\) divisible by \(u\)
is
\[
N_p=\frac1u\sum_{j=0}^{u-1}F_p(\zeta_u^j),
\]
where \(\zeta_u=e^{2\pi i/u}\).

#### Proof

Expanding \(F_p\) chooses one allowed digit in every base-\(p\) position.
Thus the coefficient of \(x^b\) is \(1\) exactly when
\(b\in\mathcal D_p(A_p)\), and is \(0\) otherwise. The standard
roots-of-unity identity
\[
\frac1u\sum_{j=0}^{u-1}\zeta_u^{jb}
=
\begin{cases}
1,&u\mid b,\\
0,&u\nmid b
\end{cases}
\]
then filters precisely the exponents divisible by \(u\). ∎

The \(j=0\) term is the naive entropy prediction
\[
\frac{|\mathcal D_p(A_p)|}{u}.
\]
All nonzero characters measure the arithmetic bias of the digit box. The
computations show that this bias can dominate the main term, so box
cardinality alone is not a deterministic substitute for the character
sum.

### Proposition 22 — complement symmetry of a Lucas box

**Proved.** The digit box in Proposition 20 satisfies
\[
b\in\mathcal D_p(A_p)
\quad\Longleftrightarrow\quad
A_p-b\in\mathcal D_p(A_p).
\]
Consequently, its compatible multipliers are paired by
\[
t\longleftrightarrow M-1-t.
\]
When \(M\) is even, if \(C_p\) is the number of positive compatible
multipliers in \(1\leq t\leq(M-1)/2\), then the total number \(N_p\) from
Proposition 21 is
\[
N_p=2(C_p+1).
\]

#### Proof

If the base-\(p\) digits of \(b\) satisfy \(0\leq b_i\leq A_{p,i}\), then
subtracting \(b\) from \(A_p\) requires no borrow. The resulting digits are
\(A_{p,i}-b_i\), which satisfy the same bounds. Since
\[
A_p=u_p(M-1),\qquad b=u_pt,
\]
the complementary box value is \(u_p(M-1-t)\).

If \(M\) is even, \(M-1\) is odd, so the involution has no integer fixed
point. Besides the paired positive half-intervals, it pairs the endpoints
\(t=0\) and \(t=M-1\), giving the formula. ∎

### Proposition 23 — Fourier formula for the full intersection

**Proved.** For each \(p\mid M\), let \(f_p\) be the indicator of
\(\mathcal T_p\) in the cyclic group \(\mathbb Z/Q_p\mathbb Z\), and define
\[
\widehat f_p(r)=
\sum_{x=0}^{Q_p-1}f_p(x)e^{-2\pi i rx/Q_p}.
\]
If \(H=\lfloor(M-1)/2\rfloor\), then the number \(W(M)\) of common witness
multipliers is
\[
W(M)=
\frac1{\prod_{p\mid M}Q_p}
\sum_{(r_p)}
\left(\prod_{p\mid M}\widehat f_p(r_p)\right)
\sum_{t=1}^{H}
\exp\left(
2\pi i t\sum_{p\mid M}\frac{r_p}{Q_p}
\right),
\]
where each \(r_p\) ranges from \(0\) to \(Q_p-1\).

#### Proof

Fourier inversion on each cyclic group gives
\[
f_p(t)=\frac1{Q_p}\sum_{r=0}^{Q_p-1}
\widehat f_p(r)e^{2\pi i rt/Q_p}.
\]
Now
\[
W(M)=\sum_{t=1}^{H}\prod_{p\mid M}f_p(t).
\]
Substituting the inversions, expanding the product, and interchanging the
finite sums gives the formula. ∎

The all-zero frequency contributes
\[
H\prod_{p\mid M}\frac{|\mathcal T_p|}{Q_p},
\]
the box-entropy main term. Known witnesses can occur when this quantity is
far below \(1\), so the mixed nonzero frequencies can dominate. Conversely,
a supercritical example may have almost no one-box character bias and still
have \(W(M)=0\). Thus the decisive cancellation is genuinely multi-base.

### Research conjecture — adaptive three-base cover

For each \(p\mid M\), let
\[
\mathcal A_p=
\left\{1\leq t\leq\frac{M-1}{2}:
\binom{M(M-1)}{Mt}\not\equiv0\pmod p\right\}.
\]
The **Lucas cover degree** \(\lambda(M)\), when the full intersection is
empty, is the least cardinality of a set \(S\) of prime divisors for which
\[
\bigcap_{p\in S}\mathcal A_p=\varnothing.
\]

The current working conjecture is:
\[
\sum_{p\mid M}\frac1p>1
\quad\Longrightarrow\quad
\text{some }S\subseteq\{p:p\mid M\},\ |S|\leq3,\text{ has empty
intersection}.
\]
This statement is **not proved**. It has been computationally checked for
all reciprocal-supercritical \(M\leq300000\). It would imply the
reciprocal-threshold conjecture because an empty subintersection forces
the full intersection to be empty.

The triple cannot always be chosen as the three smallest primes. At
\[
M=33060=2^2\cdot3\cdot5\cdot19\cdot29,
\]
\(t=65\) passes the Lucas tests in bases \(2,3,5,29\). An adaptive triple
containing \(19\), such as \(\{2,3,19\}\), is empty.

### Research conjecture — pair isolation

With the same notation, the current stronger structural conjecture is
\[
\sum_{p\mid M}\frac1p>1
\quad\Longrightarrow\quad
\min_{\substack{p,q\mid M\\p\ne q}}
|\mathcal A_p\cap\mathcal A_q|\leq1.
\]
This is **not proved**. It has been checked for all reciprocal-supercritical
\(M\leq300000\), and in completely resolved parts of several large
prime-power families.

The defect hypothesis is essential for this proposed statement. At the
positive-defect degree-four examples \(M=26187\) and \(60515\), the
smallest pair intersections have sizes \(2\) and \(28\), respectively.

### Proposition 24 — rigidity of a singleton subintersection

**Proved.** Let \(S\) be a nonempty set of prime divisors of \(M\), and
suppose
\[
\bigcap_{p\in S}\mathcal A_p=\{t_0\}.
\]
In the full multiplier interval \(0\leq t\leq M-1\), the simultaneous pass
set for the bases in \(S\) is
\[
\{0,t_0,M-1-t_0,M-1\},
\]
with the two middle points identified when
\(t_0=(M-1)/2\).

#### Proof

The endpoints \(0\) and \(M-1\) pass every Lucas box. By Proposition 22,
each selected box is invariant under
\[
t\longmapsto M-1-t.
\]
Hence \(t_0\) and \(M-1-t_0\) both belong to the full-interval
intersection.

Every nonendpoint multiplier belongs either to the lower half
\[
1\leq t\leq\left\lfloor\frac{M-1}{2}\right\rfloor
\]
or is the complement of one in that half. By hypothesis the only
lower-half member is \(t_0\), so no other full-interval members exist. ∎

Thus, if pair isolation leaves one multiplier and that multiplier were a
full witness, the simultaneous intersection of all bases would be forced
into the same three- or four-point configuration. Proving that negative
defect excludes this rigid configuration would finish the
reciprocal-threshold conjecture once pair isolation is established.

### Proposition 25 — the defect port formula

**Proved.** Let \(R=\operatorname{rad}(M)\), \(D=D(R)\), and
\(p^a\parallel M\). Define the exponent twist
\[
c_p=\frac{M}{p^{a-1}R}.
\]
After removing the \(a\) forced trailing base-\(p\) zeroes, the least
digit of the upper Lucas argument is
\[
\delta_p=(c_pD\bmod p)\in\{1,\ldots,p-1\}.
\]
The least shifted digit passes for a multiplier \(t\) exactly when
\[
(-\delta_p t\bmod p)\leq\delta_p.
\]
Consequently, precisely \(\delta_p+1\) residue classes of \(t\bmod p\)
pass the first shifted digit.

#### Proof

From
\[
D=R-\sum_{q\mid R}\frac Rq,
\]
reduction modulo \(p\) kills \(R\) and every summand except \(R/p\).
Therefore
\[
D\equiv-\frac Rp\pmod p. \tag{1}
\]
Put \(u=M/p^a\). The definition of \(c_p\) gives
\[
u=c_p\frac Rp,
\]
so (1) implies
\[
u\equiv-c_pD\pmod p. \tag{2}
\]

The shifted upper and lower arguments are
\[
A=u(M-1),\qquad B=ut.
\]
Since \(M\equiv0\pmod p\), equation (2) gives
\[
A\equiv-u\equiv c_pD\equiv\delta_p\pmod p,
\qquad
B\equiv-\delta_pt\pmod p.
\]
Lucas's least-digit condition is exactly the displayed inequality.

The digit \(\delta_p\) is nonzero because \(p\nmid u\). Finally,
multiplication by \(-\delta_p\) permutes the residue classes modulo \(p\);
exactly the \(\delta_p+1\) residues \(0,\ldots,\delta_p\) satisfy the
inequality. ∎

For squarefree \(M\), every \(c_p=1\). Thus defect \(D=1\) gives
\(\delta_p=1\), recovering the two-port condition behind Proposition 15.
At the opposite boundary \(D=-1\), one has \(\delta_p=p-1\), so the first
shifted digit imposes no restriction at all. This explains why
defect-\(-1\) examples require higher-digit arguments.

### Proposition 26 — no uniformly shallow proof of pair isolation

**Proved.** Let \(p,q\) be distinct prime divisors of \(M\), and let
\(h\geq1\). If
\[
2p^h q^h\leq\frac{M-1}{2},
\]
then there are at least two admissible multipliers that pass the first
\(h\) shifted Lucas digits in both bases \(p\) and \(q\).

Consequently, for every fixed \(h\) there are reciprocal-supercritical
\(M\) for which no pair can be certified to have at most one multiplier
using only its first \(h\) shifted digits.

#### Proof

Take
\[
t_1=p^h q^h,\qquad t_2=2p^h q^h.
\]
The displayed bound makes both multipliers admissible and distinct.

For \(p^a\parallel M\), write \(u_p=M/p^a\). After the \(a\) forced
trailing zeroes are removed, the lower Lucas argument is \(u_pt_j\).
Because \(p\nmid u_p\) and \(p^h\mid t_j\), its first \(h\) base-\(p\)
digits are zero. They therefore lie below the corresponding digits of the
upper argument \(u_p(M-1)\). The same argument works in base \(q\).

For the final assertion, fix \(h\) and take \(M=30^a\) with \(a\) large
enough that
\[
4\cdot15^h\leq30^a-1.
\]
Its prime kernel is \(\{2,3,5\}\), whose reciprocal sum is \(31/30>1\).
For every pair from this kernel, the preceding construction supplies two
admissible multipliers passing the first \(h\) shifted digits. Thus no
choice of pair is isolated at that fixed truncation depth. ∎

This does not refute pair isolation: later digits may still reduce every
candidate pair. It rules out a proof using a uniformly bounded number of
prefix digits and shows that the necessary depth must grow with \(M\).

### Proposition 27 — simultaneous vacuity at every fixed depth

**Proved.** Let \(R\) be squarefree and \(H\geq1\). There is an exponent
\(e\geq H\) such that, for
\[
M=R^e,
\]
the first \(H\) shifted Lucas digits pass for every multiplier
\(0\leq t\leq M-1\) and every prime \(p\mid R\).

In particular, \(R\) may be chosen reciprocal-supercritical, for example
\(R=30\). Thus no uniformly bounded-depth argument can obtain any
nontrivial candidate reduction, even after selecting several bases
adaptively.

#### Proof

For each \(p\mid R\), the integer \(R/p\) is invertible modulo \(p^H\).
Choose \(e\geq H\) divisible by the multiplicative order of \(R/p\) modulo
\(p^H\), simultaneously for every \(p\mid R\). Then
\[
\left(\frac Rp\right)^e\equiv1\pmod{p^H}. \tag{1}
\]

Because \(R\) is squarefree, \(p^e\parallel M\), and after removing those
forced trailing zeroes the complementary factor is
\[
u_p=\frac{M}{p^e}=\left(\frac Rp\right)^e.
\]
Also \(e\geq H\) gives \(M\equiv0\pmod{p^H}\). Hence (1) yields
\[
u_p(M-1)\equiv-1\pmod{p^H}.
\]
The first \(H\) base-\(p\) digits of the shifted upper argument are
therefore all \(p-1\). Every possible string of \(H\) lower digits lies
digitwise below this string, regardless of \(t\). This holds
simultaneously for all \(p\mid R\). ∎

This strengthens Proposition 18 and Proposition 26 at bounded depth:
their selected artificial multipliers are replaced here by the entire
multiplier interval. The obstruction remains compatible with pair
isolation because digits beyond \(H\) may eventually collapse the
intersections.

### Proposition 28 — the second digit after a blind first digit

**Proved.** Let \(p^a\parallel M\), put \(u=M/p^a\), and suppose
\[
u\equiv1\pmod p.
\]
Write
\[
u=1+pz,\qquad t\equiv t_0+pt_1\pmod{p^2},
\qquad0\leq t_0,t_1<p.
\]
Set
\[
\alpha_p=
\left(-z-1+\mathbf1_{a=1}\bmod p\right).
\]
Then the first two shifted digits pass exactly when
\[
(t_1+zt_0\bmod p)\leq\alpha_p.
\]
Precisely \(p(\alpha_p+1)\) residue classes \(t\bmod p^2\) pass.

#### Proof

The shifted lower argument satisfies
\[
ut=(1+pz)(t_0+pt_1)
\equiv t_0+p(t_1+zt_0)\pmod{p^2}. \tag{1}
\]
The shifted upper argument is
\[
A=u(M-1)=p^a u^2-u.
\]
If \(a=1\), then modulo \(p^2\),
\[
A\equiv p-1-pz;
\]
if \(a\geq2\), then
\[
A\equiv-1-pz.
\]
In both cases the units digit is \(p-1\), so the first comparison is
automatic, and the second digit is exactly \(\alpha_p\). Equation (1)
gives the stated inequality.

For each of the \(p\) choices of \(t_0\), translation by \(zt_0\)
permutes the \(p\) choices of \(t_1\), of which exactly
\(\alpha_p+1\) pass. ∎

For a squarefree Giuga radical, defect \(-1\) gives \(u\equiv1\pmod p\)
at every prime, so Proposition 28 supplies the first potentially
nontrivial local filter.

### Proposition 29 — the only three-prime supercritical kernel

**Proved.** If a squarefree radical has exactly three prime divisors and
their reciprocal sum exceeds \(1\), then those primes are
\[
\{2,3,5\}.
\]

#### Proof

Write the primes as \(p<q<r\). If \(p\geq3\), then
\[
\frac1p+\frac1q+\frac1r
\leq\frac13+\frac15+\frac17<1,
\]
so \(p=2\). If \(q\geq5\), then
\[
\frac12+\frac1q+\frac1r
\leq\frac12+\frac15+\frac17<1,
\]
so \(q=3\). Finally,
\[
\frac12+\frac13+\frac1r>1
\]
forces \(r<6\), hence \(r=5\). ∎

Thus the complete three-prime pair-isolation problem is the single
prime-power family
\[
M=2^a3^b5^c.
\]

### Proposition 30 — fixed-radical double-logarithmic prefix blindness

**Proved.** Let \(R>1\) be squarefree and put
\[
C_R=\operatorname{lcm}_{p\mid R}(p-1).
\]
For every \(H\geq1\), define
\[
e_H=C_RR^{H-1},
\qquad
M_H=R^{e_H}.
\]
Then every multiplier \(0\leq t\leq M_H-1\) passes the first \(H\)
shifted Lucas digits in every prime base \(p\mid R\).

The radical and reciprocal defect of all the \(M_H\) are the fixed values
\(R\) and \(D(R)\), while
\[
H
=1+\log_R\log_R M_H-\log_R C_R.
\]
Thus every fixed reciprocal-supercritical radical produces an explicit
fixed-negative-defect family on which any prefix method needs
\(\Omega(\log\log M)\) digits before it can obtain even one nontrivial
candidate reduction.

#### Proof

For every \(p\mid R\),
\[
\varphi(p^H)=p^{H-1}(p-1).
\]
The first factor divides \(R^{H-1}\), the second divides \(C_R\), and
they are coprime. Hence
\[
\varphi(p^H)\mid e_H.
\]
Euler's theorem gives
\[
\left(\frac Rp\right)^{e_H}\equiv1\pmod{p^H}.
\]
Also \(e_H\geq H\), so \(M_H=R^{e_H}\equiv0\pmod{p^H}\). With
\[
u_p=\frac{M_H}{p^{e_H}}=\left(\frac Rp\right)^{e_H},
\]
we obtain
\[
u_p(M_H-1)\equiv-1\pmod{p^H}.
\]
Its first \(H\) base-\(p\) digits are all \(p-1\), so every possible
lower prefix passes. This holds simultaneously for every \(p\mid R\).

Finally, \(\log_R M_H=C_RR^{H-1}\); taking another base-\(R\) logarithm
gives the displayed identity. ∎

There is an especially clean supercritical example away from the Giuga
layer. For \(H\geq3\), one may take
\[
M_H=210^{210^{H-1}}
\]
without the factor \(C_{210}\): each
\(\varphi(p^H)\) for \(p\in\{2,3,5,7\}\) already divides
\(210^{H-1}\). Here
\[
D(210)=210-(105+70+42+30)=-37
\]
and
\[
H=1+\log_{210}\log_{210}M_H.
\]

This rules out a tempting defect dichotomy for shallow proofs: the Giuga
layer \(D=-1\) makes the first digit blind without exponent tuning, but
arbitrarily deep blindness occurs at every fixed radical once exponents
are synchronized. Negative defect must influence a successful proof
through full-depth structure, not through a uniformly early local digit.

### Corollary 31 — exact criterion for a blind shallow prefix

**Proved.** Let \(p^a\parallel M\), put \(u=M/p^a\), and let
\(1\leq H\leq a\). The first \(H\) shifted Lucas digits in base \(p\)
pass for every residue class \(t\bmod p^H\) if and only if
\[
u\equiv1\pmod{p^H}.
\]

#### Proof

The shifted upper argument is \(A=u(M-1)\). Since \(H\leq a\),
\[
A\equiv-u\pmod{p^H}.
\]
The shifted lower prefix is \(ut\bmod p^H\). As \(t\) runs through a
complete residue system modulo \(p^H\), so does \(ut\), because
\(p\nmid u\). Every possible lower digit string lies below the upper
prefix exactly when every upper digit is \(p-1\), or equivalently
\[
A\equiv-1\pmod{p^H}.
\]
Together with \(A\equiv-u\), this is precisely the claimed congruence. ∎

For \(H=1\), this recovers the completely open port
\(\delta_p=p-1\) in Proposition 25. For \(H=2\leq a\), it isolates the
fully blind case inside Proposition 28. Proposition 30 constructs its
simultaneous solutions at every prime.

### Proposition 32 — exponent blocks and the wildcard corridor

**Proved.** Let \(p^a\parallel M\), put \(u=M/p^a\), and write
\[
u=s_ap^a+r_a,\qquad1\leq r_a<p^a.
\]
The shifted upper argument has the exact two-block decomposition
\[
u(M-1)
=(p^a-r_a)+p^a(u^2-s_a-1). \tag{1}
\]
If
\[
ut=x+p^ay,\qquad0\leq x<p^a,
\]
then the full base-\(p\) Lucas test passes exactly when
\[
x\preceq_p p^a-r_a
\quad\text{and}\quad
y\preceq_p u^2-s_a-1. \tag{2}
\]

Once \(p^a>u\), let \(L\) be the least integer with \(p^L>u\). Then the
base-\(p\) digits of the shifted upper argument consist of:

1. the \(L\)-digit block of \(p^L-u\);
2. \(a-L\) consecutive digits equal to \(p-1\);
3. the digit block of \(u^2-1\).

Thus increasing only the exponent \(a\), with \(u\) fixed, inserts an
exact corridor of unrestricted Lucas digits between two fixed boundary
blocks.

#### Proof

Substituting \(u=s_ap^a+r_a\) into
\[
u(M-1)=p^au^2-u
\]
gives (1). Both displayed blocks are nonnegative and the lower one is
strictly below \(p^a\), so their base-\(p\) digits concatenate without a
carry. The same block split for \(ut\) proves (2).

If \(p^a>u\), then \(s_a=0\), \(r_a=u\), and
\[
p^a-u=(p^L-u)+(p^a-p^L)
=(p^L-u)+(p-1)\sum_{j=L}^{a-1}p^j.
\]
Equation (1) now gives the three asserted blocks. ∎

This is the first exact exponent-recursive structure in the Lucas boxes.
The wildcard corridor grows predictably, but both interval admissibility
and the other prime bases still change, so it is not yet a proof of pair
isolation.

### Proposition 33 — two bases cannot stabilize together

**Proved.** Suppose \(M\) has at least three distinct prime divisors.
Then at most one prime power \(p^a\parallel M\) can satisfy
\[
p^a>\frac{M}{p^a}.
\]
Consequently, the stabilized wildcard-corridor description in
Proposition 32 can never apply simultaneously to both bases of a pair.

#### Proof

If distinct prime powers \(p^a,q^b\parallel M\) both satisfied the
inequality, write
\[
M=p^aq^bV.
\]
Because a third prime divides \(M\), \(V>1\). The two inequalities would
be
\[
p^a>q^bV,\qquad q^b>p^aV.
\]
Multiplying and cancelling \(p^aq^b\) gives \(1>V^2\), a
contradiction. ∎

This blocks a naive two-base induction using only stabilized corridors:
one member of every pair remains in the moving-boundary regime. A useful
transfer matrix must therefore accommodate one fixed corridor and one
changing boundary.

### Corollary 34 — least synchronized diagonal exponent

**Proved.** For \(H\geq5\), the least positive exponent \(e\) for which
\[
M=30^e
\]
has its first \(H\) shifted upper digits all maximal simultaneously in
bases \(2,3,5\)
is
\[
e_H=2^{H-4}3^{H-2}5^{H-1}.
\]

#### Proof

First suppose \(e<H\). In base \(5\), put \(u=6^e\). For \(e\geq2\),
LTE gives
\[
v_5(u-1)=1+v_5(e)<e.
\]
The two terms in
\[
u(M-1)+1=5^eu^2-(u-1)
\]
then have unequal valuations, so
\[
v_5\bigl(u(M-1)+1\bigr)=1+v_5(e)<H.
\]
For \(e=1\), the valuation is \(2<H\). Thus no \(e<H\) works.

It remains to take \(e\geq H\). Corollary 31 reduces the three
conditions to
\[
15^e\equiv1\pmod{2^H},\qquad
10^e\equiv1\pmod{3^H},\qquad
6^e\equiv1\pmod{5^H}.
\]
The lifting-the-exponent lemma gives, for even \(e\),
\[
v_2(15^e-1)=4+v_2(e),
\]
and for every \(e\),
\[
v_3(10^e-1)=2+v_3(e),\qquad
v_5(6^e-1)=1+v_5(e).
\]
For \(H\geq5\), the least required prime-power divisors of \(e\) are
therefore \(2^{H-4}\), \(3^{H-2}\), and \(5^{H-1}\). They are pairwise
coprime, so their product is necessary and sufficient. It also exceeds
\(H\), as required by Corollary 31. ∎

This sharpens the general construction on the exact three-prime core.
For this \(e_H\), the universally blind prefix has length exactly \(H\):
the base-\(5\) valuation is
\[
v_5(6^{e_H}-1)=1+v_5(e_H)=H,
\]
while \(H<e_H\), so the next upper digit in base \(5\) is not \(4\).
In particular, every possible lower prefix passes through depth \(H\),
but not through depth \(H+1\).

### Proposition 35 — a finite exponent torus at fixed depth

**Proved.** Fix \(H\geq4\), and consider
\[
M=2^a3^b5^c,\qquad a,b,c\geq H.
\]
The complete collection of first-\(H\)-digit pass predicates in bases
\(2,3,5\) depends on the exponent vector \((a,b,c)\) only modulo
\[
P_H=\frac{30^{H-1}}2.
\]

#### Proof

For \(p^d\parallel M\), put \(u_p=M/p^d\). Since \(d\geq H\), the
shifted upper and lower prefixes modulo \(p^H\) are
\[
-u_p\pmod{p^H},
\qquad
u_pt\pmod{p^H}.
\]
They depend only on the powers of the other two primes modulo \(p^H\).

The Carmichael exponent for \(2^H\), together with Euler's theorem for
the odd prime powers, supplies the following simultaneous exponent
periods:
\[
2^{H-2}\quad\text{for odd units modulo }2^H,
\]
\[
2\cdot3^{H-1}\quad\text{for units modulo }3^H,
\]
and
\[
4\cdot5^{H-1}\quad\text{for units modulo }5^H.
\]
For \(H\geq4\), their least common multiple is
\[
\operatorname{lcm}
\left(2^{H-2},2\cdot3^{H-1},4\cdot5^{H-1}\right)
=2^{H-2}3^{H-1}5^{H-1}
=P_H.
\]
Changing any of \(a,b,c\) by \(P_H\) therefore preserves every relevant
upper and lower prefix. ∎

This is a genuine finite-state reduction at each chosen depth, but not a
uniform one: \(P_H\) grows exponentially with \(H\), while Proposition
30 shows that the necessary depth itself is unbounded.

### Research conjecture — the three-prime core

For every \(a,b,c\geq1\), let \(M=2^a3^b5^c\). Then some pair
\(p\ne q\) in \(\{2,3,5\}\) satisfies
\[
|\mathcal A_p\cap\mathcal A_q|\leq1.
\]

This is the pair-isolation conjecture restricted to the only possible
three-prime reciprocal-supercritical radical. It is **not proved**.
Meet-in-the-middle enumeration exactly certified all 1,000 exponent
vectors \(1\leq a,b,c\leq10\). This closes that finite cube but does not
prove the conjecture for unbounded exponents.

### Research conjecture — the diagonal \(2\)-\(3\) empty pair

For every \(e\geq1\), let \(M=30^e\). Then
\[
\mathcal A_2\cap\mathcal A_3=\varnothing.
\]

This is **not proved**. A completed meet-in-the-middle enumeration in
base \(2\) or \(3\) certifies it exactly for \(1\leq e\leq10\). The
corresponding half-interval sizes of the individual base-\(2\) pass set
are
\[
0,\ 0,\ 18,\ 0,\ 1,\ 7,\ 188,\ 100,\ 209,\ 2.
\]
Their strong nonmonotonicity warns against induction on cardinality.
Bounded searches at larger exponents are not counted as evidence for the
unbounded statement.

This conjecture deliberately pairs two opposing phenomena. Corollary 34
makes arbitrarily long common prefixes completely blind on the diagonal,
yet the conjecture predicts that the full \(2\)-\(3\) intersection is
always empty. A proof would therefore have to exploit the terminal digit
blocks beyond the synchronized blind prefix.

### Computational warning

It is tempting to guess
\[
f(p^a q^b)=\min(p^a,q^b).
\]
This is false: \(f(45)=f(3^2\cdot5)=3<5\), attained at \(k=15\).
