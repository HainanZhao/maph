# Physics pivot: exact dark events in Fourier multiports

Date: 2026-07-26

## Executive decision

**Recommended research problem.** Classify exact zero-probability
many-boson transitions in discrete Fourier interferometers, beginning
with a necessary-and-sufficient classification for small prime-power
numbers of modes.

This is a focused open-ended problem in mathematical quantum optics.  It
does not require inventing a replacement for quantum mechanics.  The
potential new contribution is a sharper explanation of destructive
many-particle interference: dark events can arise from exact
**cyclotomic balance of path multiplicities**, even when the occupation
vectors have no cyclic symmetry that triggers the elementary selection
rule.

The literature-status claim must remain conservative.  Existing work
gives broad algebraic symmetry-based suppression laws, and published
expositions explicitly describe the familiar Fourier rule as sufficient
but not necessary.  We have not yet completed a literature review proving
that no equivalent classification of all residual zeros already exists.

### Literature anchors

- Tichy et al., [*Zero-Transmission Law for Multiport Beam
  Splitters*](https://doi.org/10.1103/PhysRevLett.104.220405) (2010),
  derives the Fourier multiport suppression law.
- Dittel et al., [*Totally Destructive Many-Particle
  Interference*](https://arxiv.org/abs/1801.07014) (2018), embeds the
  previously known suppression laws in a general permutation-symmetry
  framework.
- Tichy's tutorial, [*Interference of Identical
  Particles*](https://arxiv.org/abs/1312.4266), explicitly notes that the
  familiar Fourier condition is sufficient but not necessary and that
  few general properties of the relevant permanents are known.
- Navas-Merlo and García-Escartín,
  [*Symmetry tests for cyclic groups with quantum linear
  optics*](https://arxiv.org/abs/2607.11393) (2026), shows that cyclic
  symmetry and roots-of-unity tests remain an active topic.

## Why this transfers from the Erdős work

The Problem 700 investigation developed four useful habits and tools:

1. replace a large integer expression by local residue or valuation data;
2. use prime-power structure before attacking arbitrary moduli;
3. enumerate exact finite cases and preserve exceptional families;
4. distinguish a proved reduction from a computational conjecture.

For Fourier interference, a transition amplitude is a sum of roots of
unity with nonnegative integer multiplicities.  Prime-power mode counts
turn exact cancellation into a family of equalities between integer path
counts.  This is closer to the project's existing modular and
prime-power machinery than most famous open problems in physics.

## Physical and algebraic formulation

Let

\[
F_m(j,k)=m^{-1/2}\zeta_m^{jk},
\qquad
\zeta_m=e^{2\pi i/m}.
\]

For input and output occupation vectors
\(r=(r_0,\ldots,r_{m-1})\) and
\(s=(s_0,\ldots,s_{m-1})\), with
\(\sum r_i=\sum s_i=N\), the bosonic transition amplitude is a
normalization factor times the permanent of the repeated-row-and-column
submatrix of \(F_m\).

Group its \(N!\) labelled paths by phase.  If \(c_e(r,s)\) is the number
of paths with phase \(\zeta_m^e\), then

\[
\operatorname{per}F_m[r,s]
=m^{-N/2}\sum_{e=0}^{m-1}c_e(r,s)\zeta_m^e.
\]

The event is dark exactly when this cyclotomic sum is zero.

## First exact theorem

### Theorem P1 — prime-power histogram criterion

**Proved.** Let \(m=p^a\), where \(p\) is prime.  A transition is dark if
and only if, for every \(0\leq t<m/p\),

\[
c_t=c_{t+m/p}=\cdots=c_{t+(p-1)m/p}.
\]

### Proof

Put \(C(x)=\sum_{e=0}^{m-1}c_ex^e\).  The event is dark exactly when
\(C(\zeta_m)=0\), equivalently when the minimal polynomial
\(\Phi_m(x)\) divides \(C(x)\) over the rationals.  For a prime power,

\[
\Phi_{p^a}(x)
=1+x^{p^{a-1}}+\cdots+x^{(p-1)p^{a-1}}.
\]

Since \(\deg C<m\), the quotient has degree less than \(m/p\).  The
displayed coefficient equalities are therefore necessary and
sufficient. ∎

### Physical reading

At a prime-power number of modes, every dark amplitude decomposes into
regular \(p\)-gons of many-particle paths.  Ordinary symmetry laws are
one mechanism forcing these polygonal balances, but not evidently the
only one.  This is the proposed explanatory lens.

The theorem itself is an elementary cyclotomic fact; novelty is not
claimed.  Its usefulness is that it supplies an exact integer certificate
and suggests what a structural classification must explain.

## Pilot computation

The exact scan in `scripts/scan_fourier_suppression.py` gives, for
\(m=N=4\):

- 35 occupation vectors and 1,225 ordered input/output pairs;
- 193 exactly dark pairs;
- 113 dark pairs forced by the elementary cyclic-stabilizer rule, applied
  to either side;
- 80 residual pairs;
- only three residual families after independent input/output rotations
  and input/output exchange:

\[
\begin{aligned}
(0,0,2,2)&\longrightarrow(0,1,0,3),
&c&=(12,0,12,0),\\
(0,1,0,3)&\longrightarrow(0,1,2,1),
&c&=(12,0,12,0),\\
(0,1,2,1)&\longrightarrow(0,1,2,1),
&c&=(4,8,4,8).
\end{aligned}
\]

For \(m=4\), Theorem P1 says darkness is precisely
\(c_0=c_2\) and \(c_1=c_3\), which all three families satisfy.

**Status:** computational observation, exactly reproduced by integer
dynamic programming.  “Residual” means not detected by the deliberately
narrow cyclic rule implemented here; it does not yet mean absent from
every suppression law in the literature.

### Extended four-mode scan

The following table is an exact finite computation.  “Families” counts
residual events modulo independent rotations and input/output exchange.

| particles \(N\) | dark ordered pairs | cyclic-rule pairs | residual families |
|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 16 | 16 | 0 |
| 3 | 0 | 0 | 0 |
| 4 | 193 | 113 | 3 |
| 5 | 256 | 0 | 8 |
| 6 | 608 | 320 | 10 |
| 7 | 0 | 0 | 0 |
| 8 | 1,876 | 884 | 33 |
| 9 | 2,304 | 0 | 72 |
| 11 | 512 | 0 | 16 |

The omitted \(N=10\) row has not yet been run and is not needed for any
claim above.

## Creative working conjectures

### Conjecture P2 — carry-forced cyclotomic balance

For \(m=p^a\), a useful subclass of residual dark events can be recognized
without computing a permanent: base-\(p\) carry patterns in the
occupation multiplicities force the \(p\) phase-fiber counts in Theorem
P1 to be equinumerous.

This is deliberately schematic.  The next task is to formulate the
correct statistic and immediately try to falsify it.

### Conjecture P3 — finite generators at fixed mode count

For fixed prime-power \(m\), residual dark pairs, modulo rotations,
reflection, and input/output exchange, are generated by finitely many
primitive occupation moves under addition of uniform occupation layers.

This would turn isolated “accidental” cancellations into a small algebra
of dark-state constructions.  It may be false; scans at \(m=4\) with
larger \(N\) are the first test.

### Question P4 — robustness hierarchy

Do the phase-fiber certificates predict how a zero lifts under small
mode-phase errors or partial particle distinguishability?  If different
balance mechanisms lift at different perturbative orders, the
classification would have an experimentally meaningful consequence
rather than being only a list of exact zeros.

### Falsified conjecture P6a — the \(3\bmod4\) rule

The absence of zeros for \(N=3,7\) initially suggested that four-mode
Fourier transitions might never be dark for \(N\equiv3\pmod4\).

**Falsified.** At \(N=11\), 512 ordered dark pairs occur in 16 residual
equivalence families.  One representative is

\[
(0,1,3,7)\longrightarrow(1,3,2,5),
\qquad
c=(10281600,9676800,10281600,9676800).
\]

This is worth retaining because it prevents an attractive but incorrect
congruence explanation.

### Hypothesis P6b — Mersenne photon counts

**Weak conjecture.** For the four-mode Fourier matrix, no transition with
\(N=2^k-1\) bosons is exactly dark.

Evidence currently consists only of the complete scans at \(N=1,3,7\).
The next case \(N=15\) is not yet checked.  The reason to take the pattern
seriously, rather than curve-fit three data points, is that binary
carry structure is exceptional at \(2^k-1\).  A credible proof would have
to turn that observation into a nonvanishing statement for Gaussian-
integer permanents; at present there is no such argument.

## Next work cycle

1. Audit the general 2018 algebraic suppression framework and later
   papers; determine whether the three \(m=N=4\) families already have a
   standard group-theoretic explanation.
2. Independently verify the histogram program against direct complex
   permanents for small examples.
3. Add canonical reflection symmetry and scan \(m=4\) through feasible
   particle numbers; test Conjecture P3.
4. Derive closed formulas for the three pilot families and seek a
   combinatorial involution pairing paths whose phases differ by \(\pi\).
5. Optimize or algebraically prune the \(N=15\) scan to test Hypothesis
   P6b.
6. Extend to \(m=8\), where Theorem P1 requires balance separately in
   four two-element phase fibers.
7. Only after the literature audit, state a narrow theorem target such as
   a complete classification for \(m=4\).

## Claim ledger

| ID | Claim | Status |
|---|---|---|
| P1 | Prime-power histogram criterion | Proved here; elementary cyclotomic algebra |
| P2 | Carries force a structural subclass of balances | Conjectural and not yet precisely formulated |
| P3 | Fixed-\(m\) residual families have finite generators | Conjecture |
| P4 | Balance type controls perturbative robustness | Open question |
| P5 | The \(m=N=4\) scan has 193/113/80 counts and three residual families | Exact computational observation |
| P6a | No four-mode dark events for \(N=3\bmod4\) | Falsified at \(N=11\) |
| P6b | No four-mode dark events for \(N=2^k-1\) | Weak conjecture; checked only at \(N=1,3,7\) |

## Why not choose a famous grand problem

The 3D Ising model, turbulence, high-temperature superconductivity,
quantum gravity, and dark matter are genuinely important, but the current
project has no experimental data, field-theory machinery, or simulation
infrastructure that gives it leverage on them.  A new explanation there
would be speculation.  Fourier multiport suppression is small enough to
falsify ideas quickly, exact enough to support proofs, and directly tied
to measurable quantum interference.
