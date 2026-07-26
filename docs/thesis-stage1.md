# Thesis stage 1: challenge the mechanism

Date: 2026-07-26

## Revised thesis question

The first proposal asked for a classification of dark many-boson
transitions in Fourier multiports.  That is still the broad setting, but
the thesis needs a sharper organizing question:

> Which exact zeros of a Fourier multiport are caused by the standard
> cyclic selection rule, which are embedded two-mode Hong--Ou--Mandel
> effects, and which require a genuinely multi-mode path-cancellation
> mechanism?

A working title is:

> **Beyond cyclic suppression: reducible and irreducible dark
> transitions in Fourier multiports**

“Irreducible” is provisional.  It must ultimately be defined in terms of
the absence of a lower-dimensional factorization of the occupied
scattering matrix, not merely failure of one known rule.

## Assumption audit

### A1. Every residual pair is evidence of a new mechanism

**False.** Two of the three \(m=N=4\) residual families reduce to
balanced two-mode interference after unoccupied modes and proportional
row types are removed.  They escape the implemented cyclic rule but are
instances of extended Hong--Ou--Mandel interference.

### A2. The 2018 permutation framework classified every zero

**False, but it classified every suppression law then known.** Dittel et
al. explicitly state in their detailed paper that some further Fourier
zeros remain unpredicted and that the origin of suppressed outputs for
non-periodic input states was open for future investigation:

- [Phys. Rev. A 97, 062116 / arXiv:1801.07019](https://arxiv.org/abs/1801.07019).

This is the most relevant published statement of the gap found so far.
It does not prove that no later paper has closed the gap.

### A3. Cyclotomic phase balance alone is a paper-level theory

**False.** The prime-power histogram criterion is a useful exact
certificate, but it is an elementary consequence of the cyclotomic
polynomial.  A contribution must predict balance from occupation data or
classify its mechanisms.

### A4. Generic robustness analysis will automatically be novel

**False.** Dittel et al. already analyze weak unitary disorder and
partial distinguishability for symmetry-forced zeros.  A new robustness
result must distinguish cancellation mechanisms, not merely show that a
zero becomes nonzero under noise.

### A5. The Mersenne photon-number conjecture should be central

**Unsupported.** It rests on only \(N=1,3,7\).  It is retained in the
ledger but is not a current thesis pillar.

### A6. The odd-\(a\) line is itself a new physical mechanism

**Probably false.** The line \(b=2a\) reduces to the central
Krawtchouk value

\[
C_{a,2a}=\binom{2a}{a}K_a(a;2a),
\]

whose odd-degree parity zero is standard.  It is physically aligned
with the extended Hong--Ou--Mandel central nodal line, even though the
four-mode coefficient reaches it through a nested reduction.  The
project should not sell T1 alone as a new suppression principle.

The potentially new content is the **completeness statement** T3: within
the full reflection-symmetric plane, the familiar parity line supplies
all positive-integer zeros.  This distinction changes the paper
threshold materially.

## Exact generating-function representation

Use the unnormalised four-mode Fourier matrix

\[
F_4(j,k)=i^{jk},\qquad 0\leq j,k<4.
\]

For input occupation \(r\) and output occupation \(s\), put

\[
G_s(x_0,x_1,x_2,x_3)
=
\prod_{j=0}^3
\left(\sum_{k=0}^3 i^{jk}x_k\right)^{s_j}.
\]

Then

\[
\operatorname{per}F_4[r,s]
=
\left(\prod_{k=0}^3 r_k!\right)
[x_0^{r_0}x_1^{r_1}x_2^{r_2}x_3^{r_3}]G_s.
\]

This follows by expanding each labelled output row.  A fixed assignment
of input modes occurs \(\prod r_k!\) times in the permanent because the
columns belonging to particles in the same mode are identical.

The formula is the main bridge between optical amplitudes, coefficient
identities, and integer path counts.

## The two reducible pilot families

### Family R1 — balanced input and odd output

After rotation, the first pilot pair is

\[
(0,0,2,2)\longrightarrow(0,1,0,3).
\]

More generally, for \(q\geq1\) and odd \(b\),

\[
(0,0,q,q)\longrightarrow(0,b,0,2q-b)
\]

is dark whenever \(0\leq b\leq2q\).

**Proof.** Restriction to the two occupied inputs and two occupied
outputs gives, up to row and column phases, a balanced two-mode beam
splitter.  The amplitude is proportional to

\[
[x^qy^q](x+y)^b(x-y)^{2q-b}.
\]

Exchanging \(x\) and \(y\) multiplies the polynomial by
\((-1)^{2q-b}=-1\), while leaving the target monomial fixed.  Its
coefficient is therefore zero. ∎

This is an embedded extended Hong--Ou--Mandel effect, not a new
four-mode mechanism.

### Family R2 — central nodal line after row collapse

The second pilot pair is

\[
(0,1,0,3)\longrightarrow(0,1,2,1).
\]

For input \(r=(0,u,0,v)\), Fourier rows \(0,2\) restrict to one effective
row type on occupied input modes \(1,3\), and rows \(1,3\) restrict to a
second type.  If

\[
s_0+s_2=s_1+s_3=(u+v)/2,
\]

the amplitude is proportional to

\[
[x^u z^v](x+z)^{(u+v)/2}(x-z)^{(u+v)/2}.
\]

When \(u,v\) are odd, this is a coefficient of an odd-power monomial in
\((x^2-z^2)^{(u+v)/2}\), so it vanishes.

Again, this is an embedded two-mode central-nodal-line effect.

## First infinite non-periodic family

### Theorem T1

**Proved.** For every positive odd integer \(a\), the four-mode Fourier
transition

\[
(0,a,2a,a)\longrightarrow(0,a,2a,a)
\]

has exactly zero amplitude.

The occupation has no nontrivial cyclic stabilizer, so the standard
Fourier cyclic suppression law does not predict this zero.

### Proof

Since the target exponent of \(x_0\) is zero, set \(x_0=0\) and rename
\(x_1=x\), \(x_2=y\), and \(x_3=z\).  The relevant coefficient is

\[
C_a=[x^ay^{2a}z^a]
\left(y^2+(x-z)^2\right)^a
\left(y-x-z\right)^{2a}.
\]

Indeed, the Fourier row forms with indices \(1,2,3\) are

\[
-y+i(x-z),\qquad y-x-z,\qquad -y-i(x-z),
\]

and the first and third multiply to \(y^2+(x-z)^2\).

Expanding both factors and selecting total \(y\)-degree \(2a\) gives

\[
C_a
=
\sum_{k=0}^a
\binom ak\binom{2a}{2k}T_k,
\]

where

\[
T_k=[x^az^a](x-z)^{2k}(x+z)^{2a-2k}.
\]

Replacing \(z\) by \(-z\) shows

\[
T_{a-k}=(-1)^aT_k.
\]

The binomial weight of \(T_{a-k}\) equals that of \(T_k\):

\[
\binom a{a-k}\binom{2a}{2a-2k}
=
\binom ak\binom{2a}{2k}.
\]

When \(a\) is odd, the indices \(k\) and \(a-k\) are distinct.  Pairing
their summands cancels the entire sum, so \(C_a=0\).  Multiplication by
the nonzero input factorials and Fourier normalization does not change
vanishing. ∎

### Why T1 is more interesting than R1 and R2

For \(a>0\), both sides of T1 occupy three modes and their restricted
scattering matrix has three distinct row and column types.  It does not
collapse immediately to one balanced \(2\times2\) transition.  Its first
proof instead pairs coefficient sectors \(k\leftrightarrow a-k\).

The stronger evaluation below shows that the sectors themselves are
Krawtchouk coefficients.  The best current description is therefore a
**nested Krawtchouk cancellation**, intermediate between a single
embedded beam splitter and a genuinely new multi-mode special function.

This is an independently derived theorem of this project, but the
literature audit indicates that its arithmetic core is an established
central Krawtchouk/parity zero, physically aligned with extended
Hong--Ou--Mandel nodal lines:

- [Alsing et al., *Generalized Hong--Ou--Mandel experiments with
  bosonic particles*](https://arxiv.org/abs/2110.02089).

A July 2026 paper studies generalized multiphoton zeros in symmetric
\(SU(N)\) beam splitters, principally for equal-occupation coincidence
outputs:

- [Alsing, Birrittella, and Kaulfuss, Phys. Rev. A 114,
  012409](https://doi.org/10.1103/bnzx-znhf).

T1 has a nonuniform output, so it is not obviously one of that paper's
central families.  Nevertheless, T1 by itself is no longer treated as
the novelty claim.

## Exact parity classification

### Theorem T2

**Proved.** For every nonnegative integer \(a\),

\[
C_a=
\begin{cases}
0,&a\text{ odd},\\[3pt]
(-1)^{a/2}\binom{2a}{a}\binom{a}{a/2},&a\text{ even}.
\end{cases}
\]

### Proof

Define the unnormalised Krawtchouk coefficient

\[
K_n(x;N)
=[t^n](1-t)^x(1+t)^{N-x}.
\]

The quantity

\[
T_k=[x^az^a](x-z)^{2k}(x+z)^{2a-2k}
\]

from the proof of T1 is \(K_a(2k;2a)\).  Krawtchouk duality gives

\[
\binom{2a}{2k}K_a(2k;2a)
=
\binom{2a}{a}K_{2k}(a;2a).
\]

But

\[
\sum_n K_n(a;2a)t^n
=(1-t)^a(1+t)^a
=(1-t^2)^a,
\]

and hence

\[
K_{2k}(a;2a)=(-1)^k\binom ak.
\]

Substitution into the expression for \(C_a\) yields

\[
C_a
=
\binom{2a}{a}
\sum_{k=0}^a(-1)^k\binom ak^2.
\]

The remaining sum is the coefficient of \(t^a\) in

\[
(1-t)^a(1+t)^a=(1-t^2)^a.
\]

It is zero when \(a\) is odd and equals
\((-1)^{a/2}\binom{a}{a/2}\) when \(a\) is even. ∎

Thus T1 is exactly the odd half of a closed amplitude formula, while the
even members of the same occupation family are provably bright.

## Lifting theorem: arbitrarily large Fourier multiports

### Theorem T2b

**Proved.** Let \(d\mid m\) and \(q=m/d\).  Every dark transition of
\(F_d\) produces a dark transition of \(F_m\) by retaining input modes
\(0,\ldots,d-1\) and mapping output mode \(j\) to \(qj\).

### Proof

On the selected rows and columns,

\[
F_m(qj,k)
=m^{-1/2}\exp(2\pi i qjk/m)
=m^{-1/2}\exp(2\pi i jk/d)
=\sqrt{d/m}\,F_d(j,k).
\]

The repeated scattering matrix is therefore multiplied by the same
nonzero scalar in every entry.  For \(N\) particles its permanent is
multiplied by \((d/m)^{N/2}\), which preserves whether it is zero. ∎

In particular, for every \(m\) divisible by four and every positive odd
\(a\), place the input occupation \((0,a,2a,a)\) on modes
\(0,1,2,3\), and place the same four entries on output modes
\(0,m/4,m/2,3m/4\).  The transition is dark.

This does not provide a new cancellation mechanism beyond T1/T2, but it
shows that the mechanism occurs in arbitrarily large Fourier devices.

## Next conjecture: the reflection-symmetric plane

The same calculation works for the two-parameter self-transition

\[
(0,a,b,a)\longrightarrow(0,a,b,a).
\]

Its coefficient is

\[
C_{a,b}
=
\sum_{\substack{0\leq k\leq a\\2a-2k\leq b}}
\binom ak\binom{b}{2a-2k}
[x^az^a](x-z)^{2k}(x+z)^{2a-2k}.
\]

**Conjecture T3.** For positive integers \(a,b\),

\[
C_{a,b}=0
\quad\Longleftrightarrow\quad
a\text{ is odd and }b=2a.
\]

The initial scan verified this for \(1\leq a\leq20\) and
\(0\leq b\leq80\).  The stronger certificate below now covers
\(1\leq a\leq1000\) and every positive \(b\).  Theorem T2 proves the
claimed behavior on the line \(b=2a\), but it does not by itself exclude
off-line integral zeros.

This is a better next target than complete \(F_4\) classification.  It
is a precise two-parameter nonvanishing problem, and the literature on
integral zeros of Krawtchouk polynomials warns that apparently simple
zero classifications can encode serious arithmetic.  For example,
integral Krawtchouk zeros have been studied using elementary number
theory, Diophantine methods, and even quantum-entanglement criteria:

- [Heo and Kiem, *Linear Algebra and its Applications* 567
  (2019)](https://doi.org/10.1016/j.laa.2019.01.005);
- [Jooste, Jordaan, and Tookos, *Zeros of Meixner and Krawtchouk
  polynomials*](https://arxiv.org/abs/0901.0817).

This makes “classify every \(F_4\) zero” an unsafe thesis promise.  A
mechanism hierarchy with several exact families is more credible.

## New reduction of the reflection plane

### Theorem T3a — binomial sum and generating function

**Proved.** For all nonnegative integers \(a,b\),

\[
C_{a,b}
=
(-1)^a
\sum_{j=0}^{\min(a,\lfloor b/2\rfloor)}
(-1)^j
\binom{2(a-j)}{a-j}
\binom b{2j}\binom{2j}{j}.
\]

Equivalently, its mixed ordinary/exponential generating function is

\[
\boxed{\quad
\sum_{a,b\geq0}C_{a,b}u^a\frac{t^b}{b!}
=
\frac{e^t I_0(2t\sqrt{u})}{\sqrt{1+4u}}.
\quad}
\]

Here \(I_0\) is the modified Bessel function.  Consequently,

\[
bC_{a,b}
=(2b-1)C_{a,b-1}
-(b-1)C_{a,b-2}
+4(b-1)C_{a-1,b-2},
\qquad b\geq2,
\]

with

\[
C_{a,0}=C_{a,1}=(-1)^a\binom{2a}{a}.
\]

There is also an exact recurrence in the other parameter (terms with a
negative index are zero):

\[
\begin{aligned}
(a+1)^2C_{a+1,b}
={}&b(b-1)C_{a,b-2}
-(8a^2+4a+2)C_{a,b}\\
&+8b(b-1)C_{a-1,b-2}
-(16a(a-1)+4)C_{a-1,b}\\
&+16b(b-1)C_{a-2,b-2}.
\end{aligned}
\]

This follows by applying the \(u\)-form of the same Bessel differential
equation to \(H\).  It supplies a possible induction route for T3,
although its mixed signs prevent an immediate nonvanishing proof.

Two further aliases may be useful for importing special-function
results.  Directly from the finite sum,

\[
C_{a,b}
=(-1)^a\binom{2a}{a}\,
{}_3F_2\!\left(
\begin{matrix}-a,-b/2,(1-b)/2\\[2pt]1/2-a,1\end{matrix};-1
\right).
\]

For fixed \(b\), its ordinary generating function in \(a\) is

\[
\sum_{a\geq0}(-1)^aC_{a,b}u^a
=
\frac{(1+4u)^{b/2}
P_b\!\left((1+4u)^{-1/2}\right)}
\sqrt{1-4u}},
\]

where \(P_b\) is the Legendre polynomial.  These forms do not solve the
integer-zero problem, but they identify more precise bodies of
literature to search than the generic term “Fourier permanent.”

### Proof

In the original finite sum, the inner coefficient is
\(K_a(2k;2a)\).  The duality calculation used for T2 gives

\[
\binom{2a}{2k}K_a(2k;2a)
=
\binom{2a}{a}(-1)^k\binom ak.
\]

Substituting this identity, simplifying factorials, and putting
\(j=a-k\) gives

\[
C_{a,b}
=
\sum_j(-1)^{a+j}
\binom{2(a-j)}{a-j}
\frac{b^{\underline{2j}}}{(j!)^2},
\]

which is the stated binomial convolution because

\[
\frac{b^{\underline{2j}}}{(j!)^2}
=\binom b{2j}\binom{2j}{j}.
\]

For fixed \(a\), summing over \(b\) uses

\[
\sum_{b\geq0}\binom b{2j}\frac{t^b}{b!}
=\frac{t^{2j}e^t}{(2j)!}.
\]

The remaining two series are

\[
\sum_{n\geq0}(-1)^n\binom{2n}{n}u^n
=\frac1{\sqrt{1+4u}},
\qquad
\sum_{j\geq0}\frac{u^jt^{2j}}{(j!)^2}
=I_0(2t\sqrt u),
\]

which proves the boxed generating function.

Let \(H(u,t)\) denote that generating function.  The Bessel equation
for \(e^{-t}\sqrt{1+4u}\,H=I_0(2t\sqrt u)\) is

\[
t^2(H_{tt}-2H_t+H)+t(H_t-H)-4ut^2H=0.
\]

Coefficient extraction of \(u^at^b/b!\), followed by division by
\(b\), gives the recurrence. ∎

The recurrence changes the computational problem from repeatedly
expanding permanents to filling a two-dimensional integer table.  More
importantly, the generating function identifies the reflection plane
with a central-binomial/Bessel convolution rather than an unspecified
“complicated permanent.”

### Theorem T3b — a rigorous positive region

**Proved.** The coefficient \(C_{a,b}\) is positive in the following
region:

\[
\begin{array}{c|c}
a&\text{sufficient condition}\\ \hline
1&b\geq3,\\
2&b\geq6,\\
a\geq3&b\geq4a-3.
\end{array}
\]

### Proof

For \(b\geq2a\), write the convolution from T3a as

\[
C_{a,b}=(-1)^a\sum_{j=0}^a(-1)^j A_j,
\qquad
A_j=
\binom{2(a-j)}{a-j}
\frac{b^{\underline{2j}}}{(j!)^2}.
\]

Put \(n=a-j\).  Consecutive absolute terms satisfy

\[
\frac{A_{j+1}}{A_j}
=
\frac{
n(b-2a+2n)(b-2a+2n-1)
}{
2(2n-1)(a-n+1)^2
}.
\]

Suppose \(a\geq3\) and \(b\geq4a-3\).  At \(n=1\), the ratio is at
least

\[
\frac{(2a-1)(a-1)}{a^2}>1.
\]

For \(n\geq2\), it is strictly larger than

\[
\frac{2a(2a+1)}{4(a-1)^2}>1.
\]

Thus \(A_0<A_1<\cdots<A_a\).  Pairing the alternating sum from its
largest end gives \(C_{a,b}>0\), whether \(a\) is even or odd.  The
small cases follow from

\[
C_{1,b}=(b-2)(b+1)
\]

and the same ratio argument for \(a=2,b\geq6\). ∎

This proves a genuine zero-exclusion region.  Any counterexample to T3
must lie in the linearly wide strip

\[
1\leq b<4a-3
\qquad(a\geq3).
\]

The bound is still not expected to be sharp.  Its value is conceptual:
the infinite two-parameter conjecture has been reduced to an arithmetic
wedge of linear width.

### Theorem T3c — the lower adjacent diagonal

**Proved.** For every positive integer \(a\),

\[
C_{a,2a-1}
=
\binom{2a}{a}
\begin{cases}
\displaystyle
(-1)^{a/2}\frac12\binom a{a/2},
&a\ \text{even},\\[7pt]
\displaystyle
(-1)^{(a+1)/2}\binom{a-1}{(a-1)/2},
&a\ \text{odd}.
\end{cases}
\]

In particular, the diagonal immediately below the conjectured zero
line never vanishes.

For a short proof, the factorial sum at \(b=2a-1\) reduces to

\[
\frac{C_{a,2a-1}}{\binom{2a}{a}}
=
\frac1a\sum_{k=0}^a(-1)^k k\binom ak^2.
\]

Using \(k\binom ak=a\binom{a-1}{k-1}\), the numerator is

\[
-a[t^{a-1}](1-t)^{a-1}(1+t)^a
=
-a[t^{a-1}](1-t^2)^{a-1}(1+t).
\]

Separating even and odd \(a\) gives the displayed formula.

### Theorem T3d — arithmetic restrictions on any counterexample

**Proved.** Define the polynomial

\[
Q_a(b)=(a!)^2C_{a,b}.
\]

Then \(Q_a\in\mathbb Z[b]\) is monic of degree \(2a\), with

\[
Q_a(0)=(-1)^a(2a)!.
\]

Every positive integral root must satisfy

\[
\boxed{\quad b(b-1)\mid(2a)!.\quad}
\]

For odd \(a\), polynomial continuation also gives

\[
Q_a(-1)=Q_a(2a)=0
\]

and hence

\[
Q_a(b)=(b+1)(b-2a)R_a(b),
\qquad
R_a\in\mathbb Z[b]\ \text{monic},
\qquad
R_a(0)=(2a-1)!.
\]

Thus any additional positive integral root for odd \(a\) must divide
\((2a-1)!\).

### Proof

The falling-factorial form in T3a gives

\[
Q_a(b)=
\sum_{j=0}^a
(-1)^{a+j}
\binom{2(a-j)}{a-j}
\frac{(a!)^2}{(j!)^2}
b^{\underline{2j}}.
\]

Every coefficient is integral; the \(j=a\) term makes the polynomial
monic, and the \(j=0\) term gives its constant.  At a positive integer
\(b\), every term with \(j\geq1\) is divisible by \(b(b-1)\), proving
the boxed condition if the total is zero.

For the value at \(-1\), generalized binomial coefficients give

\[
C_{a,-1}
=
(-1)^a
\sum_{j=0}^a(-1)^j
\binom{2(a-j)}{a-j}\binom{2j}{j}.
\]

The convolution on the right has generating function

\[
\frac1{\sqrt{1-4z}}\frac1{\sqrt{1+4z}}
=\frac1{\sqrt{1-16z^2}},
\]

so it vanishes for odd \(a\).  The root \(2a\) is T2.  Division by the
two monic integer linear factors preserves integrality, and evaluation
at zero gives \(R_a(0)=(2a-1)!\).  The last divisibility is the rational
root theorem applied to \(R_a\). ∎

T3b and T3d suggest complementary attacks: sign control removes the
high-\(b\) cone, while divisibility sieves act on the remaining
oscillatory wedge.

### Conjecture T3e — the stronger irreducibility pattern

The polynomial reformulation suggests a sharper algebraic conjecture:

\[
\begin{cases}
Q_a(b)\ \text{is irreducible over }\mathbb Q,
&a\ \text{even},\\[3pt]
Q_a(b)=(b+1)(b-2a)R_a(b),\
R_a\ \text{is irreducible over }\mathbb Q,
&a\ \text{odd}.
\end{cases}
\]

Exact finite-field certificates prove the stated irreducibility pattern
for every \(1\leq a\leq38\), with the degree-zero quotient understood at
\(a=1\).  The standard-library command

```text
python3 scripts/audit_reflection_irreducibility.py
```

reconstructs \(Q_a\) over \(\mathbb Z\) and verifies each residual
polynomial as irreducible modulo a recorded prime using Rabin's
criterion.  Because the polynomials are monic, irreducibility modulo
one prime certifies irreducibility over \(\mathbb Q\) by Gauss's lemma.
An optional `--exact-factor` flag repeats direct factorization when
SymPy is installed.

T3e strictly strengthens the physical zero conjecture.  For even \(a\),
irreducibility excludes every integral root.  For odd \(a\), it says
that the already proved roots \(-1\) and \(2a\) are the only rational
roots at all.  The conjecture also points toward established tools:
Newton polygons, reduction modulo carefully chosen primes, and
irreducibility results for factorial or falling-factorial polynomials.

This is currently the most promising proof target, but also potentially
harder than T3 itself.  A failed irreducibility conjecture would not
falsify T3; a higher-degree factor could exist without having a positive
integral root.

### Exact computational certificate

The recurrence, the positive-tail theorem, and two modular primes give
an exact finite certificate for every fixed range of \(a\).  Running

```text
python3 scripts/certify_reflection_conjecture.py --a-limit 1000
```

finds no off-line zero for \(1\leq a\leq1000\).  Because T3b handles
the infinite positive tail separately for each row, this certifies
**every positive \(b\)** in those 1,000 rows, not merely a rectangular
sample.  A nonzero modular residue rigorously implies a nonzero integer
coefficient; a candidate vanishing modulo both primes is evaluated by
the exact binomial sum.  No off-line double-residue candidate occurs in
this range.

This is strong evidence, not a proof of T3 for unbounded \(a\).

### Focused novelty audit

Exact searches found no source stating the family
\((0,a,b,a)\to(0,a,b,a)\), the boxed Bessel generating function, or
Conjecture T3.  That absence is only moderate evidence and is not a
novelty proof.  Several boundaries are now clear:

- Fock-state amplitudes as generating-polynomial coefficients and
  recurrences are standard; see
  [Bezerra and Shchesnovich (2023)](https://arxiv.org/abs/2301.02192).
- Symmetric tensor powers of unitary matrices are established
  multivariate Krawtchouk territory; see
  [Genest, Vinet, and Zhedanov
  (2013)](https://arxiv.org/abs/1306.4256).
- Integral Krawtchouk zeros have a substantial arithmetic literature,
  including
  [Habsieger and Stanton
  (1993)](https://doi.org/10.1007/BF02988302) and
  [Heo and Kiem
  (2019)](https://doi.org/10.1016/j.laa.2019.01.005).
- Later work does find suppression families beyond simple symmetry
  principles, while not evidently covering this fixed four-mode
  collisional slice; relevant comparisons include
  [Bezerra and Shchesnovich
  (2023)](https://arxiv.org/abs/2301.02192) and
  [Dufour and Buchleitner
  (2026 revision)](https://arxiv.org/abs/2409.15079).

The correct provisional novelty statement is therefore:

> For one reflection-symmetric four-mode self-transition family, we
> derive an explicit polynomial, Bessel generating function, and
> zero-free region.  To our knowledge this specialization has not been
> stated previously.  We do not claim a new general suppression
> principle, and the known zero line is an established parity mechanism.
> The potentially novel theorem would be that no other positive-integer
> zeros occur in the family.

Until T3 is proved, that last sentence remains a conjectural target, not
a paper claim.

## Structural census beyond the pilot

As a first filter, two occupied Fourier rows are assigned the same
support type when their restrictions to the occupied input modes are
proportional; columns are treated dually.  An event with at most two row
types and two column types is a candidate for reduction to a single
two-mode polynomial.  This condition is necessary for the simple
reduction being tested, not a sufficient proof of physical \(SU(2)\)
equivalence.

Among residual families not caught by the cyclic rule:

| photons | residual families | at most two types | three or more types |
|---:|---:|---:|---:|
| 4 | 3 | 2 | 1 |
| 5 | 8 | 0 | 8 |
| 6 | 10 | 4 | 6 |
| 7 | 0 | 0 | 0 |
| 8 | 33 | 12 | 21 |
| 9 | 72 | 26 | 46 |
| 11 | 16 | 0 | 16 |

Thus the multitype residue grows immediately; T1/T2 is not the only
phenomenon that survives the basic two-type filter.  These counts are
exact computational observations, not yet classifications by mechanism.

### The \(N=11\) residue is smaller than it first appears

Independent Fourier-valid reflections reduce the 16 rotation-canonical
\(N=11\) classes to four prototypes.  Continuing the dominant
occupation coordinate along its natural fixed-offset affine line shows
that the amplitudes are polynomials on each residue class modulo four.
Exact real/imaginary polynomial gcds classify the admissible dark
parameters on those four lines:

\[
\begin{array}{c|c}
\text{prototype line}&\text{common polynomial factor}\\ \hline
L_A&(x-2)(x-5)(x-7)\\
L_B&x-7\\
L_C&x(x-3)(x-5)(x+1)(x+2)\\
L_D&(x-1)(x-2)(x-7).
\end{array}
\]

Thus the observed \(N=11\) points are isolated arithmetic roots on
these natural lines, not members of an infinite affine family.  The
calculation also found the unexpected histogram identity

\[
\operatorname{hist}\bigl((0,1,3,x+2),(1,3,2,x)\bigr)
=
\operatorname{hist}\bigl((0,3,3,x),(1,1,2,x+2)\bigr).
\]

A finite residue-class degree argument supplies a computer-assisted
proof; a direct coefficient proof remains a good small target.  Full
parameters, degree reasoning, negative searches, and reproduction work
are recorded in
[the \(N=11\) mining note](agent-n11-findings.md).

This suggests a second organizing mechanism: **isolated common roots of
affine amplitude quasipolynomials**.  It is structurally different from
both cyclic symmetry and a parity-protected infinite line, but it is not
yet a paper-level classification theorem.

## Revised contribution ladder

1. **Completed:** exact phase-histogram computation and prime-power
   cancellation certificate.
2. **Completed:** classification of the three four-photon residual
   families into two embedded two-mode effects and one sector-pairing
   effect.
3. **Completed:** Theorem T1, an infinite family of non-periodic dark
   self-transitions.
4. **Completed:** Theorem T2, the exact parity classification and closed
   coefficient formula.
5. **Completed:** lifting to arbitrary mode counts divisible by four.
6. **In progress:** T3a--T3e reduce Conjecture T3 to a linear wedge,
   add arithmetic and irreducibility structure, certify the conjecture
   for \(a\leq1000\), and certify the stronger irreducibility pattern
   for \(a\leq38\).
7. **Completed first multitype case study:** the \(N=11\) residue
   reduces to four isolated affine quasipolynomial-root classes.
8. **Paper threshold:** prove T3/T3e in general, or add a broader
   structural theorem or mechanism-specific physical prediction.  T1/T2
   alone no longer meet this threshold.
9. **Master's-thesis threshold:** a substantial \(F_4\) mechanism
   classification, or a substantial partial classification together
   with extension to \(F_{2^d}\) and robustness analysis.

## Immediate experiments

1. Attack T3e uniformly using Newton polygons and primes adapted to
   \(a\); fall back to T3d divisibility if full irreducibility is too
   strong.
2. Prove the \(L_A/L_C\) histogram identity directly.
3. Search the \(N=5,6,8,9\) residue for repeated affine common factors.
4. Formalize reducibility under Fourier-valid dihedral operations and
   lower-dimensional tensor decompositions.
5. Compare leakage under unitary perturbations for cyclic, parity-line,
   and isolated affine-root zeros.
6. Confirm the focused novelty audit through MathSciNet or Zentralblatt
   access before drafting a paper.

## Claim ledger

| ID | Claim | Status |
|---|---|---|
| R1 | First pilot family is an embedded balanced two-mode zero | Proved; known mechanism |
| R2 | Second pilot family is an embedded central-nodal-line zero | Proved; known mechanism |
| T1 | \((0,a,2a,a)\to(0,a,2a,a)\) is dark for every odd \(a\) | Proved here; arithmetic core is a known parity/Krawtchouk mechanism |
| T2 | Exact all-\(a\) coefficient formula | Proved using Krawtchouk duality |
| T2b | Every \(F_d\) zero lifts to \(F_m\) when \(d\mid m\) | Proved; elementary embedding |
| T3 | In the positive reflection plane, zeros occur exactly at odd \(a\), \(b=2a\) | Conjecture; exactly certified for \(a\leq1000\) and every \(b>0\) |
| T3a | Closed binomial sum, Bessel generating function, and recurrence for \(C_{a,b}\) | Proved |
| T3b | \(C_{a,b}>0\) for \(a\geq3,\ b\geq4a-3\), with explicit small-\(a\) bounds | Proved |
| T3c | Exact nonzero formula on \(b=2a-1\) | Proved |
| T3d | Monic integer polynomial structure and divisibility restrictions on integral roots | Proved |
| T3e | \(Q_a\) is irreducible for even \(a\); after the two known linear factors, irreducible for odd \(a\) | Conjecture in general; exactly certified for \(a\leq38\) |
| T4 | T1 is irreducible in an appropriate formal sense | Probably false if nested reductions count; definition still required |
