# Thesis stage 1: challenge the mechanism

Date: 2026-07-26

## Revised thesis question

The first proposal asked for a classification of dark many-boson
transitions in Fourier multiports.  That is still the broad setting, but
the thesis needs a sharper organizing question:

> Which exact zeros of a Fourier multiport are caused by the standard
> cyclic selection rule directly, which lie in its closure under
> Krawtchouk histogram reciprocity, which are embedded two-mode
> Hong--Ou--Mandel effects, and which remain outside all three
> explanations?

A working title is:

> **The reciprocity closure of suppression laws in four-mode Fourier
> interferometers**

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

**False.** The line \(b=2a\) reduces to the central
Krawtchouk value

\[
C_{a,2a}=\binom{2a}{a}K_a(a;2a),
\]

whose odd-degree parity zero is standard.  It is physically aligned
with the extended Hong--Ou--Mandel central nodal line, even though the
four-mode coefficient reaches it through a nested reduction.  The
project should not sell T1 alone as a new suppression principle.

More strongly, Corollary T4a proves that the entire line is a
histogram-reciprocity image of an ordinary cyclic-symmetry zero.

The potentially new content is the **completeness statement** T3: within
the full reflection-symmetric plane, the familiar parity line supplies
all positive-integer zeros.  This distinction changes the paper
threshold materially.

### A7. Failure of the cyclic rule means a non-cyclic mechanism

**False.** The cyclic rule is only a direct sufficient test on the
given occupation pair.  Theorem T4 below preserves the complete phase
histogram while changing the pair.  Under this reciprocity and elementary
mode symmetries, the entire T1 family maps to a transition caught
directly by the cyclic rule.

The correct object is therefore the **closure** of elementary
suppression laws under exact histogram-preserving transformations.  A
zero should be called unexplained only after this closure has been
applied.

### A8. Reciprocity-equivalent zeros have the same robustness

**False without transporting the perturbation as well.** Reciprocity
equates ideal amplitudes or histograms after changing the occupation
pair.  Applying the same laboratory mixer to the same named output
modes does not commute with that transformation.  Direct cyclic and
reciprocity-cyclic representatives therefore have different
directional leakage fingerprints, as shown by Theorem P1 and the exact
tables below.

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
Krawtchouk coefficients.  The coefficient proof therefore exhibits a
nested Krawtchouk cancellation.  Theorem T4 later shows that this
nesting is an exact transport of a cyclic-symmetry zero, not a new
irreducible suppression mechanism.

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
for every \(1\leq a\leq59\), with the degree-zero quotient understood at
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

The extended audit also weakens the originally proposed proof strategy.
Every finite-field certificate prime must exceed \(2a\), because the
constant term is a factorial and reduction modulo a smaller prime
acquires a factor \(b\).  Certificate primes are correspondingly
irregular.  Moreover:

- no unshifted primitive one-edge Newton/Dumas case occurs through
  \(a=60\);
- no shifted case occurs for \(a\leq25\),
  \(|c|\leq2a\), and tested primes \(p\leq4a+10\);
- ordinary and naively shifted Eisenstein arguments are therefore not a
  credible uniform route without new valuation structure.

These are exact finite diagnostics, not impossibility theorems.  They
support keeping T3e as a strong algebraic conjecture while attacking the
weaker integral-root statement T3 directly.  Details and reproduction
commands are in
[the irreducibility challenge audit](agent-irred-extension.md).

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

### Theorem N1 — direct proof of the hidden identity

**Proved.** The displayed histogram identity holds for every
nonnegative integer \(x\).

### Proof

The four entries of a phase histogram are determined by its evaluations
at \(q=1,i,-1,-i\).  It therefore suffices to prove equality of the two
unnormalized repeated-matrix permanents at those four values.

Write the parameter as \(n\), set \(M=n+3\), and use variables
\(X,Y,Z\) for input modes \(1,2,3\).  At \(q=i\), put

\[
S=X+Z,\qquad D=X-Z.
\]

The four Fourier row forms restricted to these modes are

\[
Y+S,\quad -Y+iD,\quad Y-S,\quad -Y-iD.
\]

Both transitions contain

\[
A=(Y+S)(Y-S)^2
=\sum_{m=0}^3 a_mY^{3-m}S^m,
\qquad
(a_0,a_1,a_2,a_3)=(1,-1,-1,1).
\]

The remaining factors are

\[
B_r=(-Y+iD)^r(-Y-iD)^{M-r},
\]

with \(r=3\) on the left and \(r=1\) on the right.  Using

\[
K_m(r;M)=[t^m](1-t)^r(1+t)^{M-r},
\]

the coefficient of \(Y^m\) in \(B_r\) is

\[
p_mK_m(r;M)D^{M-m}.
\]

The phase \(p_m\) is the same for \(r=3\) and \(r=1\), since

\[
(-1)^mi^3(-i)^{n-m}
=
(-1)^mi(-i)^{n+2-m}.
\]

Moreover,

\[
[X^kZ^{M-k}]S^mD^{M-m}
=(-1)^{M-m+k}K_k(m;M).
\]

The required exponents have \(k=1\) on the left and \(k=3\) on the
right.  These have the same parity, so every factor in the resulting
four-term sums agrees except

\[
K_m(3;M)K_1(m;M)
\quad\text{versus}\quad
K_m(1;M)K_3(m;M).
\]

Krawtchouk duality gives, term by term,

\[
\binom M3 K_m(3;M)K_1(m;M)
=
\binom M1 K_m(1;M)K_3(m;M).
\]

Hence, if \(c_L,c_R\) denote the two polynomial coefficients,

\[
\frac{c_L}{c_R}
=
\frac{\binom M1}{\binom M3}
=
\frac6{(n+1)(n+2)}.
\]

The input-occupation factorials are

\[
1!\,3!\,(n+2)!
\quad\text{and}\quad
3!\,3!\,n!,
\]

whose ratio is the reciprocal factor.  Thus the permanents agree at
\(q=i\), and conjugation gives equality at \(q=-i\).

At \(q=-1\), both output products reduce to

\[
(Y+S)^3(Y-S)^{n+3}.
\]

After selecting \(Y^3S^{n+3}\), the two \(X,Z\) coefficients have ratio

\[
\frac{\binom{n+3}{1}}{\binom{n+3}{3}}
=\frac6{(n+1)(n+2)},
\]

again canceled by the input factorials.  At \(q=1\), both repeated
matrices contain only ones and their permanents equal \((n+6)!\).
All four Fourier evaluations therefore agree, and invertibility of the
four-point discrete Fourier transform proves equality of the complete
histograms. ∎

### Theorem T4 — sectorwise histogram reciprocity

**Proved.** Let \(N,d\geq0\), let \(s_0+s_2=d\), let
\(0\leq\alpha\leq d\), and let \(0\leq p,k\leq N\).  The two \(F_4\)
transitions

\[
\begin{aligned}
(\alpha,k,d-\alpha,N-k)&\longrightarrow(s_0,p,s_2,N-p),\\
(\alpha,p,d-\alpha,N-p)&\longrightarrow(s_0,k,s_2,N-k)
\end{aligned}
\]

have identical four-phase histograms.

Theorem N1 is the specialization

\[
d=3,\quad\alpha=0,\quad(s_0,s_2)=(1,2),\quad
N=n+3,\quad(p,k)=(3,1).
\]

### Proof

Restore a variable \(W\) for mode zero and put

\[
E=W+Y,\qquad T=W-Y,\qquad S=X+Z,\qquad D=X-Z.
\]

At \(q=i\), write

\[
A(E,S)=(E+S)^{s_0}(E-S)^{s_2}
=\sum_{m=0}^d a_mE^{d-m}S^m,
\]

\[
B_p(T,D)=(T+iD)^p(T-iD)^{N-p}.
\]

The three elementary coefficient formulas are

\[
\begin{aligned}
[T^m]B_p
&=(-1)^{N-p-m}i^{N-m}K_m(p;N)D^{N-m},\\
[W^\alpha Y^{d-\alpha}]E^{d-m}T^m
&=(-1)^mK_\alpha(m;d),\\
[X^kZ^{N-k}]S^mD^{N-m}
&=(-1)^{N-m-k}K_k(m;N).
\end{aligned}
\]

If \(C^{(\alpha)}_{p,k}\) is the resulting unlabelled coefficient,
every factor in its sum other than
\(K_m(p;N)K_k(m;N)\) is invariant under
\(p\leftrightarrow k\).  Termwise Krawtchouk duality therefore yields

\[
C^{(\alpha)}_{p,k}
=\frac{\binom Nk}{\binom Np}C^{(\alpha)}_{k,p}.
\]

The corresponding input-factorial multipliers are

\[
\frac{\alpha!(d-\alpha)!\,N!}{\binom Nk}
\quad\text{and}\quad
\frac{\alpha!(d-\alpha)!\,N!}{\binom Np},
\]

so the labelled evaluations agree at \(q=i\).  At \(q=-1\), both
generating products reduce to \((E+S)^d(E-S)^N\), and the same binomial
ratio is canceled by the factorials.  The \(q=1\) evaluations count all
labelled paths, and \(q=-i\) follows by conjugation.  Four-point Fourier
inversion proves the histogram identity. ∎

If

\[
\mathcal H_{d,N}(\alpha,k;s,p)
=
\operatorname{hist}\bigl(
(\alpha,k,d-\alpha,N-k),(s,p,d-s,N-p)
\bigr),
\]

then T4 and ordinary input/output exchange together give the fourfold
symmetry

\[
\mathcal H(\alpha,k;s,p)
=\mathcal H(\alpha,p;s,k)
=\mathcal H(s,k;\alpha,p)
=\mathcal H(s,p;\alpha,k).
\]

Thus the odd and even occupation sectors can be transposed independently,
although a generic instance is not related by any ordinary mode
permutation.

T4 is qualitatively stronger than the original affine observation: it
is an infinite parameterized equivalence between complete path-phase
distributions.  It transports every dark or bright transition, and
indeed its full phase-count profile, to a generally different
occupation pair.  A novelty check must still determine whether this is
known under a symmetric-power or multivariate-Krawtchouk formulation.

### Corollary T4a — T1 is in the cyclic reciprocity closure

For every \(a\geq0\), apply T4 with

\[
N=d=2a,\qquad k=a,\qquad p=2a,\qquad
(s_0,s_2)=(a,a).
\]

It identifies the histograms of

\[
(0,a,2a,a)\longrightarrow(a,2a,a,0)
\]

and

\[
(0,2a,2a,0)\longrightarrow(a,a,a,a).
\]

Independent rotations of the input and output preserve vanishing.  The
first transition is therefore equivalent for zero/nonzero purposes to
the T1 self-transition, while the second is equivalent to

\[
(0,0,2a,2a)\longrightarrow(a,a,a,a).
\]

The uniform output has a one-step cyclic stabilizer.  Applied in the
input/output-exchanged direction, the cyclic rule tests the weighted
mode sum of \((0,0,2a,2a)\):

\[
2(2a)+3(2a)=10a\equiv2a\pmod4.
\]

It forces a zero exactly when \(a\) is odd.  Thus T1/T2's parity line is
precisely a reciprocity image of standard cyclic suppression.

This also explains why the reflection-plane conjecture singles out
\(b=2a\).  After rotating the output of
\((0,a,b,a)\to(0,a,b,a)\), the T4 balance condition is

\[
b=s_0+s_2=2a.
\]

No off-line point in that self-transition plane enters this particular
cyclic reciprocity orbit.

### Corollary T4b — robustness across the \(4\times4\) Hadamard family

The same reciprocity is a polynomial identity for

\[
H(z)=
\begin{pmatrix}
1&1&1&1\\
1&z&-1&-z\\
1&-1&1&-1\\
1&-z&-1&z
\end{pmatrix}
\]

for arbitrary complex \(z\).  When \(|z|=1\), \(H(z)/2\) is unitary,
and \(H(i)/2=F_4\).

Indeed, the four row forms become

\[
E+S,\qquad T+zD,\qquad E-S,\qquad T-zD.
\]

The coefficient of \(T^m\) in the odd-row product gains a common factor
\(z^{N-m}\); every other step of the T4 proof is unchanged.  Thus the
two normalized physical amplitudes agree throughout the full dephased
complex-Hadamard family, not only at the Fourier point.

The scope is also sharply delimited.  A naive even/odd-sector swap for
\(F_8\) already fails with two particles, so T4 is not an automatic
parity law for all \(F_{2^m}\).  Its engine is the two-mode binary split
inside \(F_4\).

### Exact closure census

Closing the residual families under independent rotations, reflections,
input/output exchange, and T4 gives:

| particles | original residual families | closure components | residual families reaching a direct cyclic event |
|---:|---:|---:|---:|
| 4 | 3 | 3 | 1 |
| 5 | 8 | 3 | 0 |
| 6 | 10 | 6 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 33 | 23 | 1 |
| 9 | 72 | 40 | 0 |

The \(N=4\) family reaching the cyclic class is T1 at \(a=1\).  Thus
the closure does more than merge equivalent residual representatives:
it can convert a nominally unexplained event into a directly
symmetry-predicted one.  At \(N=5,6,9\), it substantially reduces the
number of components without by itself explaining their darkness.

The exact reproduction command is

```text
python3 scripts/analyze_reciprocity_census.py
```

The computer-assisted residue-class argument remains an independent
check, but it is no longer needed for the theorem.  Full parameters,
degree reasoning, negative searches, and reproduction work are recorded
in
[the \(N=11\) mining note](agent-n11-findings.md).

This suggests a second organizing mechanism: **isolated common roots of
affine amplitude quasipolynomials**.  It is structurally different from
the cyclic/reciprocity closure in the tested orbits, but it is not yet a
paper-level classification theorem.

## Directional leakage as a physical discriminator

The reciprocity result challenges another assumption: two zeros in the
same algebraic closure need not respond identically when the same
physical perturbation is applied to the laboratory output modes.

Append a calibrated lossless mixer after \(F_4\):

\[
U^X_{pq}(\epsilon)=e^{i\epsilon X_{pq}}F_4,\qquad
U^Y_{pq}(\epsilon)=e^{i\epsilon Y_{pq}}F_4,
\]

where

\[
X_{pq}=|p\rangle\langle q|+|q\rangle\langle p|,
\qquad
Y_{pq}=-i|p\rangle\langle q|+i|q\rangle\langle p|.
\]

For a dark event, exact ladder-operator differentiation expresses the
first leakage amplitude entirely through neighboring root-of-unity
permanents.  If \(Z_{r,t}\) is the unnormalized \(F_4\) permanent and

\[
D_{r,s}=2^N\sqrt{\prod_jr_j!\prod_ks_k!},
\]

then

\[
\mathcal A_X'(0)
=\frac{i}{D_{r,s}}
\left(s_qZ_{r,s+e_p-e_q}+s_pZ_{r,s-e_p+e_q}\right),
\]

\[
\mathcal A_Y'(0)
=\frac{1}{D_{r,s}}
\left(s_pZ_{r,s-e_p+e_q}-s_qZ_{r,s+e_p-e_q}\right).
\]

This gives a **directional leakage fingerprint**, rather than one
ambiguous scalar notion of robustness.

### Theorem P1 — an exact protected axis for every odd T1 member

**Proved.** For every positive odd \(a\), the transition

\[
(0,a,2a,a)\longrightarrow(0,a,2a,a)
\]

remains exactly dark under

\[
U^Y_{13}(\epsilon)=e^{i\epsilon Y_{13}}F_4
\]

for every real \(\epsilon\).

For the proof, put \(u=x+z\) and \(v=x-z\).  The rotated row pair has
the form

\[
L'_1L'_3=A(y^2+v^2)+Byv,
\]

while \(L_2=y-u\).  Exchange \(x\leftrightarrow z\) kills every term
with an odd power of \(v\).  In a surviving sector with \(2h\) factors
of \(Byv\), the remaining coefficient is a symmetric weight times

\[
K_{a,k}=[x^az^a](x-z)^{2k}(x+z)^{2a-2k}.
\]

The weight is invariant under \(k\leftrightarrow a-k\), whereas

\[
K_{a,a-k}=(-1)^aK_{a,k}.
\]

All sectors therefore cancel for odd \(a\), uniformly in
\(\epsilon\).

### Exact four-axis fingerprints

For three representative events, the leading target probability is:

| event | \(X_{12}\) | \(Y_{12}\) | \(X_{13}\) | \(Y_{13}\) |
|---|---:|---:|---:|---:|
| direct cyclic: \((1,1,1,1)\to(3,1,0,0)\) | exact | exact | exact | exact |
| reciprocity-cyclic: \((0,1,2,1)\to\) itself | \(\epsilon^2/64\) | \(25\epsilon^2/64\) | \(\epsilon^2/4\) | exact |
| isolated \(N=11\): \((0,1,3,7)\to(1,3,3,4)\) | \(315\epsilon^2/16384\) | \(315\epsilon^4/8192\) | \(315\epsilon^2/16384\) | \(315\epsilon^2/16384\) |

The quartic \(Y_{12}\) direction of the isolated event is an exact
second-order calculation, not a floating-point fit.  It also prevents
an over-simple narrative: an isolated arithmetic root can be flatter
than an infinite family along one direction.  What distinguishes the
classes is the complete directional exponent pattern.

The standard-library reproduction is

```text
python3 scripts/analyze_unitary_leakage.py
```

and the derivations and all six mixer pairs are recorded in
[the unitary-leakage note](agent-unitary-leakage.md).

This is experimentally meaningful in principle: forbidden-event
leakage has already been used to diagnose Fourier photonic circuits,
and programmable photonic processors with number-resolving detection
exist:

- [Crespi et al., Nature Communications 7,
  10469 (2016)](https://doi.org/10.1038/ncomms10469);
- [Dittel et al., Physical Review Letters 120,
  240404 (2018)](https://doi.org/10.1103/PhysRevLett.120.240404);
- [Arrazola et al., Nature 591,
  54--60 (2021)](https://doi.org/10.1038/s41586-021-03202-1).

The four-photon cyclic/reciprocity-cyclic comparison is the realistic
first experiment.  The eleven-photon row is a later benchmark.  Partial
distinguishability, mode-dependent loss, and reconstructed-unitary
uncertainty must still be added before claiming an experimentally
resolvable quartic signature.

## Revised contribution ladder

1. **Completed:** exact phase-histogram computation and prime-power
   cancellation certificate.
2. **Completed:** classification of the three four-photon residual
   families into two embedded two-mode effects and one
   reciprocity-cyclic event.
3. **Reclassified:** Theorem T1 is an infinite family of non-periodic
   dark self-transitions, but T4a places it in the reciprocity closure of
   the standard cyclic rule.
4. **Completed:** Theorem T2, the exact parity classification and closed
   coefficient formula.
5. **Completed:** lifting to arbitrary mode counts divisible by four.
6. **In progress:** T3a--T3e reduce Conjecture T3 to a linear wedge,
   add arithmetic and irreducibility structure, certify the conjecture
   for \(a\leq1000\), and certify the stronger irreducibility pattern
   for \(a\leq59\).
7. **Completed first multitype case study:** the \(N=11\) residue
   reduces to four isolated affine quasipolynomial-root classes.
8. **New structural theorem:** T4 upgrades one hidden \(N=11\) identity
   to an infinite sectorwise histogram reciprocity and explains the
   whole T1/T2 zero line as transported cyclic suppression.
9. **New physical theorem:** P1 proves an all-odd exact perturbation
   axis, while the four-axis leakage table distinguishes direct cyclic,
   reciprocity-cyclic, and isolated-root examples.
10. **Paper threshold:** confirm T4/P1 novelty and add realistic
   distinguishability/loss analysis, a T4 orbit classification, or a
   proof of T3/T3e.
11. **Master's-thesis threshold:** a substantial \(F_4\) mechanism
   classification, or a substantial partial classification together
   with extension to \(F_{2^d}\) and robustness analysis.

## Immediate experiments

1. Attack the weaker integral-root conjecture T3 directly using T3d
   divisibility and the reciprocity explanation of the line \(b=2a\).
   Revisit T3e only if new coefficient-valuation structure appears.
2. Extend the T4 closure census beyond \(N=9\) using stored residual
   representatives rather than repeating expensive full pair scans.
3. Search the \(N=5,6,8,9\) residue for repeated affine common factors.
4. Formalize reducibility under Fourier-valid dihedral operations and
   lower-dimensional tensor decompositions.
5. Add realistic noise floors to the exact leakage comparison of direct
   cyclic, reciprocity-cyclic, and isolated affine-root zeros.
6. Confirm the focused novelty audit through MathSciNet or Zentralblatt
   access before drafting a paper.

## Claim ledger

| ID | Claim | Status |
|---|---|---|
| R1 | First pilot family is an embedded balanced two-mode zero | Proved; known mechanism |
| R2 | Second pilot family is an embedded central-nodal-line zero | Proved; known mechanism |
| T1 | \((0,a,2a,a)\to(0,a,2a,a)\) is dark for every odd \(a\) | Proved; T4a places it in the cyclic reciprocity closure |
| T2 | Exact all-\(a\) coefficient formula | Proved using Krawtchouk duality |
| T2b | Every \(F_d\) zero lifts to \(F_m\) when \(d\mid m\) | Proved; elementary embedding |
| T3 | In the positive reflection plane, zeros occur exactly at odd \(a\), \(b=2a\) | Conjecture; exactly certified for \(a\leq1000\) and every \(b>0\) |
| T3a | Closed binomial sum, Bessel generating function, and recurrence for \(C_{a,b}\) | Proved |
| T3b | \(C_{a,b}>0\) for \(a\geq3,\ b\geq4a-3\), with explicit small-\(a\) bounds | Proved |
| T3c | Exact nonzero formula on \(b=2a-1\) | Proved |
| T3d | Monic integer polynomial structure and divisibility restrictions on integral roots | Proved |
| T3e | \(Q_a\) is irreducible for even \(a\); after the two known linear factors, irreducible for odd \(a\) | Conjecture in general; exactly certified for \(a\leq59\) |
| N1 | The two \(L_A/L_C\) affine lines have identical phase histograms | Proved directly by Krawtchouk duality |
| T4 | Sectorwise reciprocity preserves the complete \(F_4\) phase histogram | Proved |
| T4a | T1/T2's zero line is a reciprocity image of a cyclic-symmetry zero | Proved |
| T4b | Sectorwise reciprocity persists across the full \(4\times4\) complex-Hadamard family | Proved |
| P1 | Every odd T1 member remains exactly dark along the \(Y_{13}\) unitary rotation | Proved |
