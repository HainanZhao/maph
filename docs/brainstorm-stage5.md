# Stage 5: digit depth and inherited primary pseudoperfect numbers

This stage repeats the summarize–brainstorm–work cycle at the
primary-pseudoperfect boundary.

## Cycle 1 — is the second shifted digit always enough?

### Summary

Proposition 15 reduced every possible witness for primary pseudoperfect
\(M\) to a subset sum
\[
t=\sum_{p\in S}\frac{M}{p}.
\]
All candidates for \(M=6,42,1806,47058\) failed by the second shifted
Lucas digit in at least one prime base.

### Brainstorm

The identity \(M/p\equiv-1\pmod p\) completely determines the first shifted
digit. Write
\[
\frac Mp=pc_p-1.
\]
For a subset candidate, the second shifted digit can also be written
explicitly in terms of \(c_p\) and the remaining subset sum. This suggested
that two digits might cover every candidate.

### Work and falsification

The conjecture survives the unique primary pseudoperfect numbers with at
most six prime factors. It first fails for the seven-factor example
\[
M=52495396602
=2\cdot3\cdot11\cdot17\cdot101\cdot149\cdot3109.
\]
Among its 63 admissible subset candidates, exactly one passes the first two
shifted digits in every prime base:
\[
t=\frac M3+\frac M{17}=20586430040.
\]
It is nevertheless covered at the third shifted digit, with failures in
bases \(3,17,149,\) and \(3109\).

The eight-factor example has 127 candidates: 125 fail at the second shifted
digit and two fail at the third. Thus the two-digit conjecture is false,
but no tested candidate survives three shifted digits.

### 2026 literature update

The preprint
[Port Fillings for Primary Pseudoperfect Numbers](https://arxiv.org/abs/2605.21518)
constructs a nine-factor example
\[
N_9=5998279018951962402
\]
and proves \(N_9+1\) prime, producing an inherited ten-factor example.
Our exact computation checks all 255 admissible half-range subset
candidates for \(N_9\); all fail at the second shifted digit. Proposition
16 gives a two-digit cover for the inherited ten-factor example.

### Result

The right computational invariant is now **failure depth**, not merely
covered/uncovered. The script `scripts/analyze_primary_pseudoperfect.py`
reports the first-failure histogram and the deepest candidates.

## Cycle 2 — exploit inheritance

### Summary

Some primary pseudoperfect numbers arise from the one-prime inheritance
\[
K\longmapsto K(K+1)
\]
when \(K+1\) is prime.

### Brainstorm

For the new prime \(q=K+1\), the complementary factor is \(K=q-1\). This
is the simplest possible base-\(q\) digit block. Rather than bounding its
failure depth experimentally, calculate its first two shifted digits
exactly.

### Work

Proposition 16 proves that the new prime \(q\) kills every admissible
subset-sum candidate at the second shifted digit. Only the formal endpoints
\[
t=0,\qquad t=M-1
\]
pass those two digits, and neither is admissible.

This applies, for example, to the inheritance steps
\[
2\to6,\quad6\to42,\quad42\to1806,\quad
47058\to2214502422.
\]
It also applies to the ten-prime-factor example constructed in the May 2026
preprint
[Port Fillings for Primary Pseudoperfect Numbers](https://arxiv.org/abs/2605.21518).

The proposition is a genuine family theorem about digit covering. To turn a
member into a strict hit for Erdős Problem 700, one still needs \(M-1\) to
be prime.

## Cycle 3 — test the current primary-pseudoperfect frontier

The May 2026 preprint gives new nine- and ten-prime-factor examples beyond
the older list. Using its displayed factorizations:

| Prime factors | \(M\) | Candidates | Earliest-cover histogram |
|---:|---:|---:|---|
| 7 | \(52495396602\) | 63 | 62 at digit 2, 1 at digit 3 |
| 8 | \(8490421583559688410706771261086\) | 127 | 125 at digit 2, 2 at digit 3 |
| 9 | \(5998279018951962402\) | 255 | all at digit 2 |
| 10 | \(35979351189199316534587473905773572006\) | 511 | all at digit 2 |

Here “digit” means the shifted digit after the forced trailing zero; the
script prints both shifted and original positions. These are finite exact
Lucas computations.

### New conjecture

**Three-digit primary-pseudoperfect conjecture.** For every primary
pseudoperfect \(M\), every admissible subset candidate from Proposition 15
fails Lucas's criterion within its first three shifted digits in at least
one base \(p\mid M\).

This is deliberately stronger than merely asserting that a failure
eventually occurs. It holds for every currently exhibited
primary pseudoperfect number, but the sample is structurally sparse and
does not justify confidence by itself.

## Next repetition

1. Derive the third shifted digit in terms of
   \[
   M/p=-1+pc_p
   \]
   and a subset sum.
2. Separate inherited and port-primitive constructions. Proposition 16
   completely handles the former.
3. Test whether the port composition law preserves a bounded failure depth.
4. Look for a descent: a depth-three survivor for \(M\) may induce a
   forbidden residue pattern in the smaller port or prefix from which
   \(M\) was constructed.
5. Keep the reciprocal-threshold conjecture as the main route to the
   original infinite-family problem; the primary-pseudoperfect work is a
   structured boundary laboratory.

## Cycle 4 — replace reciprocal sums by an integer defect

### Summary

For \(R=\operatorname{rad}(M)\), introduce the squarefree arithmetic
derivative and its defect:
\[
\partial R=\sum_{p\mid R}\frac Rp,\qquad
D(R)=R-\partial R.
\]

### Work

Proposition 17 proves that \(D(R)=0\) is impossible. Therefore the two sides
of the reciprocal threshold are separated by an integer gap:
\[
\sum_{p\mid R}\frac1p>1\iff D(R)\leq-1,
\]
while primary pseudoperfect numbers occupy the closest possible layer below
the threshold:
\[
D(R)=1.
\]

Examples are
\[
D(30)=-1,\qquad D(1806)=1,\qquad
D(\operatorname{rad}(2088))=D(174)=23.
\]

### Result

The main conjecture is equivalently:

> A common near-multiple Lucas witness forces
> \(D(\operatorname{rad}(M))\geq1\).

This formulation is promising because the recent port framework also uses
the arithmetic derivative. A proof may be more naturally expressed as
defect descent or defect composition than as a packing argument involving
real-valued reciprocal sums.
