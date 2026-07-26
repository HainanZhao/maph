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

This is a new theorem of this project.  **Literature novelty is not yet
claimed.** A July 2026 paper studies generalized multiphoton zeros in
symmetric \(SU(N)\) beam splitters, principally for equal-occupation
coincidence outputs:

- [Alsing, Birrittella, and Kaulfuss, Phys. Rev. A 114,
  012409](https://doi.org/10.1103/bnzx-znhf).

T1 has a nonuniform output, so it is not obviously one of that paper's
central families, but the full paper and its references must be audited.

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

This is exactly verified for \(1\leq a\leq20\) and
\(0\leq b\leq80\).  Theorem T2 proves the claimed behavior on the line
\(b=2a\), but it does not exclude off-line integral zeros.

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
6. **Next theorem:** prove or falsify Conjecture T3.
7. **Next classification:** define reducibility formally and enumerate
   the first residual family that is neither cyclic nor reducible to a
   single \(SU(2)\) amplitude.
8. **Paper threshold:** at least T1/T2 plus a broader structural theorem
   or a mechanism-specific physical prediction.
9. **Master's-thesis threshold:** a substantial \(F_4\) mechanism
   classification, or a substantial partial classification together
   with extension to \(F_{2^d}\) and robustness analysis.

## Immediate experiments

1. Implement an exact test for collapse to two effective row or column
   types.
2. Reclassify all residual families through at least \(N=11\).
3. Search for affine occupation families among the irreducible residue.
4. Test whether the \(k\leftrightarrow a-k\) pairing generalizes to
   \((0,a,2b,a)\) or unequal input/output parameters.
5. Attack Conjecture T3 using Krawtchouk zero bounds and divisibility.
6. Determine whether nested Krawtchouk reduction extends to other
   reflection-symmetric input/output pairs.
7. Compare T1/T2 explicitly with every theorem in the 2026 symmetric
   \(SU(N)\) paper.

## Claim ledger

| ID | Claim | Status |
|---|---|---|
| R1 | First pilot family is an embedded balanced two-mode zero | Proved; known mechanism |
| R2 | Second pilot family is an embedded central-nodal-line zero | Proved; known mechanism |
| T1 | \((0,a,2a,a)\to(0,a,2a,a)\) is dark for every odd \(a\) | Proved here; novelty audit pending |
| T2 | Exact all-\(a\) coefficient formula | Proved using Krawtchouk duality |
| T2b | Every \(F_d\) zero lifts to \(F_m\) when \(d\mid m\) | Proved; elementary embedding |
| T3 | In the positive reflection plane, zeros occur exactly at odd \(a\), \(b=2a\) | Conjecture; verified for \(a\leq20,b\leq80\) |
| T4 | T1 is irreducible in an appropriate formal sense | Probably false if nested reductions count; definition still required |
