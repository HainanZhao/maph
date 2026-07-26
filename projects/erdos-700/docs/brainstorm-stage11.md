# Stage 11: defect-sensitive Helly behavior and pair isolation

## Cycle 1 — accelerate the adaptive falsifier

The original all-triples scan evaluated every base at every multiplier.
The new sequential falsifier instead tests triples lexicographically and
stops for a given \(M\) as soon as one triple is proved empty.

This raised the exhaustive range from \(100000\) to \(300000\). Across
12,572 reciprocal-supercritical cases, no \(M\) had witnesses for every
triple.

Only two \(M\leq300000\) defeat the rule “use the three smallest primes”:

\[
\begin{array}{c|c|c}
M&\text{smallest triple}&\text{next empty triple}\\ \hline
33060&(2,3,5)&(2,3,19)\\
68040&(2,3,5)&(2,3,7)
\end{array}
\]

At \(33060\), the first triple has the unique witness \(t=65\). At
\(68040\), it has the witness \(t=867\). The second case has cover degree
two because, for example, \(\mathcal A_2\cap\mathcal A_7\) is already
empty.

## Cycle 2 — challenge universal Helly dimension

### Assumption challenged

Perhaps every family of near-multiple Lucas pass sets has cover degree at
most three, independently of reciprocal defect.

### Falsification

The unrestricted scan found
\[
M=26187=3\cdot7\cdot29\cdot43
\]
with cover degree exactly four. Its four triple witnesses form a perfect
diagonal:

\[
\begin{array}{c|c}
\text{triple}&\text{witness}\\ \hline
\{3,7,29\}&792\\
\{3,7,43\}&63\\
\{3,29,43\}&980\\
\{7,29,43\}&140
\end{array}
\]

No multiplier passes all four bases. Its reciprocal defect is \(12205>0\).

A second example is
\[
M=60515=5\cdot7^2\cdot13\cdot19,
\]
with defect \(4561>0\) and respective triple witnesses
\[
2100,\quad385,\quad37,\quad111.
\]

Thus Lucas boxes have no universal Helly bound of three. Negative defect
must play an essential role in any three-base theorem.

## Cycle 3 — exact unrestricted degree histogram

For every \(M\leq100000\) with at least four distinct prime divisors and
empty full intersection, the exact histogram is:

| Cover degree | All cases | Negative-defect cases |
|---:|---:|---:|
| 1 | 7,097 | 2,084 |
| 2 | 10,445 | 1,935 |
| 3 | 144 | 1 |
| 4 | 2 | 0 |

There were 17,688 empty-full cases, eight full-witness cases, and no
degree-five example. The only degree-four examples were \(26187\) and
\(60515\).

The negative-defect column contains only numbers with at least four prime
divisors; three-prime cases were excluded from this particular table.

## Cycle 4 — add the missing reciprocal mass

The two degree-four examples collapse when small primes are added:

\[
\begin{array}{c|c|c}
M& D(\operatorname{rad}M)&\text{empty certificate}\\ \hline
26187&12205&\{3,7,29,43\}\\
52374=2\cdot26187&-1777&\{2,3\}\\
60515&4561&\{5,7,13,19\}\\
121030=2\cdot60515&477&\{2,5\}\\
363090=6\cdot60515&-15859&\{2,3\}
\end{array}
\]

This is not a monotonicity theorem—multiplying \(M\) changes every pass
set—but it illustrates the phenomenon a defect-sensitive proof must
explain: adding small reciprocal mass can create a very low-order
obstruction.

## Cycle 5 — exact supercritical degrees

The compiled exact scan through \(M\leq100000\) gives
\[
\lambda=1:2147,\qquad
\lambda=2:1995,\qquad
\lambda=3:5.
\]

The five degree-three examples are
\[
2400,\quad4500,\quad14580,\quad33060,\quad46080.
\]
The last one has factorization
\[
46080=2^{10}3^2 5
\]
and pair witnesses
\[
t_{\{2,3\}}=20591,\quad
t_{\{2,5\}}=3647,\quad
t_{\{3,5\}}=17000.
\]

## Cycle 6 — greedy compression

For each prime base let \(\mathcal A_p\) be its half-interval pass set.
Apply the following exact greedy rule:

1. choose \(p\) minimizing \(|\mathcal A_p|\);
2. choose \(q\) minimizing
   \(|\mathcal A_p\cap\mathcal A_q|\);
3. choose \(r\) minimizing the remaining triple intersection.

The rule had no failure among the 4,147 supercritical \(M\leq100000\).
More strongly, after the first two choices the number of remaining
multipliers was always at most one.

For the five degree-three cases, the greedy intersection counts were:

\[
\begin{array}{c|c}
M&\text{successive counts}\\ \hline
2400&18\to1\to0\\
4500&8\to1\to0\\
14580&28\to1\to0\\
33060&6\to1\to0\\
46080&66\to1\to0
\end{array}
\]

This motivates the **pair-isolation conjecture**:

> If \(\sum_{p\mid M}1/p>1\), then some two prime divisors \(p,q\mid M\)
> satisfy
> \[
> |\mathcal A_p\cap\mathcal A_q|\leq1.
> \]

It is false without the defect hypothesis. At \(M=26187\), the smallest
pair intersection has size \(2\); at \(M=60515\), it has size \(28\).

Sparse-box searches found no counterexample in the completely resolved
parts of these large families:

- \((2,3,5)\), exponents \(1,\ldots,10\): 323 certified cases;
- \((2,3,7,41)\), exponents \(1,\ldots,5\): 82 certified cases;
- \((2,5,7,11,13)\), exponents \(1,\ldots,3\): 41 certified cases.

The remaining 677, 543, and 202 cases respectively were unresolved at box
size \(500000\), so they are not evidence either way.

## Cycle 7 — four-point rigidity

Pair isolation alone does not prove that the full intersection is empty:
the isolated multiplier could conceivably pass every other base.
Complement symmetry nevertheless makes this case rigid.

If a pair intersection in the lower half consists only of \(t\), then its
full interval intersection consists only of
\[
0,\quad t,\quad M-1-t,\quad M-1,
\]
except that the middle two coincide when \(t=(M-1)/2\).

Therefore the reciprocal-threshold problem can be split into two concrete
targets:

1. prove pair isolation from negative defect;
2. rule out a full common intersection of exactly these three or four
   symmetric points.

The second target is a finite rigidity problem rather than an
unstructured search over all multipliers.

## Next repetition

1. Try to falsify pair isolation using randomized high-exponent sparse
   boxes and by enlarging the unresolved structured cases.
2. Relate the greedy first choice to the character-filter count
   \(N_p=2(|\mathcal A_p|+1)\).
3. Seek an inequality forcing
   \(\min_{p\ne q}|\mathcal A_p\cap\mathcal A_q|\leq1\) from
   \(D(\operatorname{rad}M)<0\).
4. Analyze the exact four-point intersection through the CRT moduli
   \(Q_p\). A full witness would force every additional box to contain the
   same symmetric pair.
5. Search for degree five outside the supercritical regime; its existence
   would further clarify whether cover degree can grow without bound.
