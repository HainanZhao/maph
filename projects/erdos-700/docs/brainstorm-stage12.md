# Stage 12: defect ports, Giuga boundaries, and deep pair geometry

## Cycle 1 — extend pair isolation exactly

The exact pass-mask scan now reaches \(M\leq300000\). Across all 12,572
reciprocal-supercritical cases:

\[
\lambda=1:6146,\qquad
\lambda=2:6421,\qquad
\lambda=3:5.
\]

The degree-three cases remain exactly
\[
2400,\quad4500,\quad14580,\quad33060,\quad46080.
\]
No full witness occurred, the three-step greedy selector never failed,
and the greedy pair intersection always had size at most one.

Thus both the adaptive three-base conjecture and pair isolation survive
this range. This is finite evidence, not a proof.

## Cycle 2 — connect reciprocal defect to a local digit

Proposition 25 gives an exact defect-port formula. Let
\[
R=\operatorname{rad}(M),\qquad D=D(R),\qquad p^a\parallel M,
\]
and set
\[
c_p=\frac{M}{p^{a-1}R}.
\]
Then the first shifted upper digit is
\[
\delta_p=(c_pD\bmod p),
\]
and \(t\) passes that digit precisely when
\[
(-\delta_pt\bmod p)\leq\delta_p.
\]

This formula isolates the roles cleanly:

- \(D\) supplies the global reciprocal state;
- \(c_p\) twists it by the exponents at the other primes;
- the resulting nonzero residue \(\delta_p\) determines the exact local
  port and its \(\delta_p+1\) allowed residues.

The implementation `near_multiple_defect_port` agrees with the direct
first-digit calculation for every \(4\leq M<250\) and every \(p\mid M\).

## Cycle 3 — identify the hardest boundary

For squarefree \(R\), defect \(D(R)=-1\) is exactly the Giuga identity
\[
\sum_{p\mid R}\frac1p-\frac1R=1.
\]
This connection is part of the broader
[\(\mu\)-Sondow framework](https://arxiv.org/abs/2111.14211).

At this boundary \(c_p=1\) and
\[
\delta_p=p-1.
\]
Therefore every residue class passes the first shifted digit in every
base. The first digit contains no covering information at all.

The first four Giuga benchmarks nevertheless have low full cover degree:

| \(R\) | Cover degree | Empty certificate |
|---:|---:|---|
| 30 | 1 | \(\{2\}\) |
| 858 | 2 | \(\{2,3\}\) |
| 1722 | 2 | \(\{2,3\}\) |
| 66198 | 1 | \(\{2\}\) |

These exact computations make Giuga radicals the natural adversarial
boundary family: the reciprocal excess is minimal and the first digit is
completely vacuous, yet higher digits still cover rapidly.

When the first digit is blind, Proposition 28 gives the next filter
explicitly. Writing
\[
\frac{M}{p^a}=1+pz,\qquad t=t_0+pt_1,
\]
the second digit passes precisely when
\[
(t_1+zt_0\bmod p)
\leq(-z-1+\mathbf1_{a=1}\bmod p).
\]
This is the first informative local condition for squarefree Giuga
radicals.

## Cycle 4 — rule out every fixed-depth strategy

Proposition 26 first shows that, for a fixed pair \(p,q\), the two
multipliers
\[
p^hq^h,\qquad2p^hq^h
\]
pass the first \(h\) digits in both bases whenever they fit in the
admissible interval.

Proposition 27 is much stronger. For any fixed depth \(H\), choose
\[
M=R^e
\]
where \(e\geq H\) is a common multiple of the orders of \(R/p\) modulo
\(p^H\). Then
\[
u_p(M-1)\equiv-1\pmod{p^H}
\]
for every \(p\mid R\). Hence every multiplier passes the first \(H\)
shifted digits in every base.

Taking \(R=30\) keeps the reciprocal sum supercritical. Therefore:

> No proof using a uniformly bounded digit depth can even reduce the
> candidate set, let alone prove pair isolation.

Any successful prefix argument must choose a depth growing with \(M\), or
must aggregate information across the complete digit boxes.

Proposition 29 also removes a distracting branch: the only
reciprocal-supercritical radical with exactly three primes is
\(\{2,3,5\}\). Hence the entire three-prime pair-isolation problem is the
single exponent family
\[
M=2^a3^b5^c.
\]

## Cycle 5 — adversarial kernels without the pair \(\{2,3\}\)

The positive-defect degree-four examples suggested crossing the reciprocal
threshold by adding moderate primes instead of immediately adding both
\(2\) and \(3\).

For
\[
M=2\cdot60515\cdot29=3509870,
\]
the defect is \(-3457\), but many pair intersections are already empty,
including \(\{2,5\}\), \(\{2,7\}\), and \(\{5,7\}\).

The squarefree nine-prime kernel
\[
(3,5,7,11,13,17,19,29,43)
\]
is also supercritical, but its exact pair boxes exceed the current cutoff.
A direct search through \(t\leq100000\) found no pair witness at all. This
does not resolve the full boxes, but it provides no indication that adding
moderate reciprocal mass preserves the degree-four diagonal.

## Cycle 6 — current primary-pseudoperfect boundary

The May 2026 preprint
[Port Fillings for Primary Pseudoperfect Numbers](https://arxiv.org/abs/2605.21518)
constructs
\[
N_9=5998279018951962402
\]
and proves \(N_9+1\) prime, yielding the inherited ten-factor primary
pseudoperfect number
\[
N_{10}
=35979351189199316534587473905773572006.
\]

Our independent analyzer found 255 admissible subset candidates for
\(N_9\); every candidate fails at the second shifted digit. Proposition 16
supplies a two-digit cover for \(N_{10}\) at its new prime \(N_9+1\).

Neither number currently feeds the strict near-multiple construction:
\[
29\mid N_9-1,\qquad5\mid N_{10}-1.
\]

## Cycle 7 — what existing theory does and does not provide

Casacuberta's
[work on covering Pascal rows](https://arxiv.org/abs/1906.07652)
is the closest direct analogue to Lucas cover degree. Its initial sieve
uses the fact that \(p^a\mid n\) forces divisibility whenever
\(p^a\nmid k\). Our sampled indices are \(k=Mt\), divisible by every
\(p^a\parallel M\), so the near-multiple problem lives precisely in the
exceptional progression left after that sieve.

Generic simultaneous no-carry intersections are not expected to be
isolated. The two-base central-binomial problem has abundant simultaneous
solutions, while even the exact three-base \(3,5,7\) problem remains open;
see the discussion and partial results of
[Croot--Mousavi--Schmidt](https://arxiv.org/abs/2201.11274).
This warns against proving pair isolation from multiplicative
independence alone. The special coupling
\[
A_p=\frac{M}{p^{v_p(M)}}(M-1)
\]
and the common defect state must do the work.

Furstenberg-type digit-fractal intersection theorems and finite-state
Markov methods suggest transfer-matrix algorithms, but presently miss the
required conclusion: our digit caps vary with position and \(M\), the
moduli grow with the digit length, and a dimension-zero bound does not
imply an intersection contains at most one integer.

## Cycle 8 — positive-certificate adversarial search

The new script `scripts/adversarial_certificate_search.py` searches from
the opposite direction. Instead of trying to exhaust every pair
intersection, it enumerates one feasible Lucas box by a balanced
meet-in-the-middle split and records explicit common witnesses.

This gives two one-sided falsification certificates:

- two distinct witnesses for every pair disprove pair isolation;
- one witness for every triple disproves the adaptive three-base cover.

The method correctly treats a resource-limited box as unresolved rather
than empty. It reproduces the known obstructions:

- \(M=2400\): pair counts \(1,1,2\);
- \(M=26187\): two witnesses for every pair and a witness for every
  triple;
- \(M=60515\): two witnesses for every pair.

For the complete exponent grid
\[
M=2^a3^b5^c,\qquad1\leq a,b,c\leq10,
\]
the reproducible baseline

```bash
python3 scripts/adversarial_certificate_search.py \
  --kernel 2 3 5 --exhaustive \
  --min-exponent 1 --max-exponent 10 \
  --max-side-values 100000 --max-candidates-per-base 50000
```

exactly certified pair isolation for 914 of the 1,000 vectors. Of the 86
unresolved cases, 78 had no feasible pivot and 8 hit the candidate cap.

Subsequent exact passes resolved all 86:

- 54 after raising the balanced-side cutoff from \(100000\) to \(500000\);
- all 8 candidate-truncated cases after raising the candidate cap;
- 13 more with balanced sides up to \(10^6\);
- 1 by choosing a lower-candidate alternate pivot;
- the final 10 with balanced sides up to \(4.2\times10^6\).

Thus every one of the 1,000 exponent vectors is now exactly certified
pair-isolated, with no unresolved cases and no counterexample.

The complete cube is reproducible in one run (about four minutes on the
development machine):

```bash
python3 scripts/adversarial_certificate_search.py \
  --kernel 2 3 5 --exhaustive \
  --min-exponent 1 --max-exponent 10 \
  --max-side-values 4200000 \
  --max-candidates-per-base 2100000 \
  --show-all-unresolved --progress-every 200
```

It reports 1,000 exact pair-isolation certificates, 1,000 exact
three-base-cover certificates, no infeasible pivot, and an empty
unresolved list.

The solver was hardened during this pass. A pivot stopped early by a
positive global counterexample is no longer labeled complete, feasible
pivots are ordered by their estimated compatible-candidate count, and a
completed pivot stops immediately once it certifies a pair intersection
of size at most one.

A deterministic random run over 1,000 exponent choices from seven
negative-defect kernels also found no positive counterexample. However,
815 cases had no feasible pivot at the selected cutoff, so that run is
mostly a stress test rather than 1,000 exact verifications.

## Cycle 9 — challenge the Giuga-boundary assumption

It was tempting to split the next proof entirely into the Giuga boundary
\(D=-1\) and the apparently easier region \(D\leq-2\). Proposition 27
shows that this is not a valid split for bounded-prefix arguments.

Proposition 30 makes the obstruction quantitative for every fixed
squarefree radical. If
\[
C_R=\operatorname{lcm}_{p\mid R}(p-1),\qquad
M_H=R^{C_RR^{H-1}},
\]
then every multiplier passes the first \(H\) digits in every base
\(p\mid R\). For supercritical \(R\), both the radical and its negative
defect stay fixed, while the required depth is
\(\Omega(\log\log M_H)\).

A particularly clean example far from the boundary is
\[
M_H=210^{210^{H-1}},\qquad H\geq3,
\]
Its radical is always \(210\), its defect is always
\[
D(210)=-37,
\]
yet every multiplier passes the first \(H\) shifted digits in all four
bases. Since
\[
H=1+\log_{210}\log_{210}M_H,
\]
universal prefix methods sometimes need depth of order
\(\log\log M\) merely to remove one candidate.

The useful distinction is therefore not simply \(D=-1\) versus
\(D\leq-2\): synchronized exponents create the same obstruction at every
fixed radical. The proof must detect how defect interacts with the entire
exponent-twisted digit tower.

Proposition 29 suggests a sharper intermediate conjecture: prove pair
isolation first for the complete three-prime family \(2^a3^b5^c\).
This is now recorded as the **three-prime core conjecture**. It is both
structurally exhaustive for three-prime supercritical radicals and
computationally approachable by the meet-in-the-middle solver.

## Cycle 10 — expose the exponent geometry

Corollary 31 gives the converse missing from the synchronized-exponent
construction. If \(p^a\parallel M\) and \(H\leq a\), then the first
\(H\) base-\(p\) digits are blind for every multiplier exactly when
\[
\frac{M}{p^a}\equiv1\pmod{p^H}.
\]
Thus total shallow blindness is an explicit simultaneous order problem,
not merely a sufficient construction.

On the diagonal \(M=30^e\), LTE solves that order problem sharply. For
\(H\geq5\), the least exponent producing \(H\) blind digits in all three
bases is
\[
e_H=2^{H-4}3^{H-2}5^{H-1}.
\]
The base-\(5\) prefix stops being blind at the next digit, so the length
\(H\) is exact.

Proposition 32 gives a complementary full-depth view. Holding
\(u=M/p^a\) fixed and increasing \(a\), the shifted upper base-\(p\)
digits split into a fixed low boundary block, an \(a\)-dependent corridor
of \(p-1\) digits, and a fixed high boundary block. This is the first
precise exponent-recursive structure found in the complete Lucas box.

Proposition 33 immediately challenges the easiest induction: with three
or more prime divisors, at most one base can enter this stabilized regime.
Two bases can never have fixed boundary blocks and growing wildcard
corridors simultaneously.

The creative next step is therefore to compress one wildcard corridor to
one transition while tracking the moving boundary in the other base. A
finite-state proof cannot use only a fixed prefix, but it may still
summarize an arbitrarily long unrestricted corridor exactly.

There is nevertheless an exact finite reduction at each chosen depth.
Proposition 35 shows that, once \(a,b,c\geq H\), all first-\(H\)
predicates for \(2^a3^b5^c\) are periodic in the exponent vector with
the sufficient common period
\[
P_H=\frac{30^{H-1}}2.
\]
The exponentially growing period explains why this does not contradict
the fixed-depth obstruction, but it supplies a finite torus on which
transfer-matrix guesses can be tested exhaustively.

## Cycle 11 — a sharper diagonal conjecture

The diagonal family reveals a useful tension. Exact meet-in-the-middle
enumeration gives
\[
\mathcal A_2\cap\mathcal A_3=\varnothing
\qquad(1\leq e\leq10,\ M=30^e).
\]
Every certification completed a pivot in base \(2\) or \(3\); completing
only base \(5\) was not treated as evidence about this pair.

The higher five cases are reproducible with:

```bash
python3 scripts/adversarial_certificate_search.py \
  --kernel 2 3 5 \
  --exponents 6 6 6 --exponents 7 7 7 --exponents 8 8 8 \
  --exponents 9 9 9 --exponents 10 10 10 \
  --max-side-values 5000000 --max-candidates-per-base 2000000
```

Meanwhile
\[
|\mathcal A_2|
=0,0,18,0,1,7,188,100,209,2
\]
over the same exponents. The intersection remains empty while the
individual set fluctuates violently, falsifying a monotone-cardinality
proof heuristic.

This motivates the **diagonal \(2\)-\(3\) empty-pair conjecture**:
\[
\mathcal A_2\cap\mathcal A_3=\varnothing
\quad\text{for every }M=30^e.
\]
It is stronger than pair isolation on the diagonal and is proved only
through \(e=10\). Its appeal is structural: Corollary 34 tells us how to
make the shared shallow prefix arbitrarily blind, so the conjectured
emptiness must be created by the terminal blocks exposed in Proposition
32.

## Next repetition

1. Prove or falsify the diagonal \(2\)-\(3\) empty-pair conjecture using
   the exact terminal blocks beyond the blind corridor.
2. Prove or falsify the three-prime core conjecture by extending the exact
   exponent cube and seeking an exponent-recursive argument.
3. Turn Proposition 32's wildcard corridor into a full-depth transfer
   matrix for a selected pair of bases.
4. Seek a defect-controlled upper bound for the smallest pair
   intersection, not merely for individual box entropy.
5. In the singleton case, exploit Proposition 24's rigid symmetric
   three- or four-point intersection.
6. Continue positive-certificate searches: two witnesses for every pair
   would disprove pair isolation without requiring any exhaustive empty
   box.
