# Stage 6: how deep can a Lucas cover hide?

## Cycle 1 — test shallow coverage beyond the defect-one boundary

### Brainstorm

The primary-pseudoperfect examples were covered within three shifted digits.
Perhaps every reciprocal-supercritical \(M\) is covered within a small
universal number of digit levels.

### Work

An exhaustive exploratory scan through \(M\leq5000\) quickly found growing
record depths:

| \(M\) | multiplier \(t\) | latest first cover |
|---:|---:|---:|
| 30 | 1 | shifted digit 3 |
| 60 | 23 | shifted digit 4 |
| 150 | 3 | shifted digit 7 |
| 750 | 224 | shifted digit 9 |
| 4500 | 123 | shifted digit 11 |

The pattern suggested using powers of \(5\) to make the base-\(5\) test pass
completely while forcing long zero prefixes in bases \(2\) and \(3\).

### Result: an unbounded construction

Proposition 18 proves that for every requested depth \(H\), one can choose
\[
M=6\cdot5^a,\qquad t=6^h
\]
so that all prime bases pass at least \(H\) shifted digits. Therefore a
fixed-prefix proof cannot establish the stronger covering statement for all
reciprocal-supercritical \(M\).

For example, \(h=10,a=13\) gives
\[
M=7324218750,\qquad t=60466176.
\]
Base \(5\) passes completely, base \(2\) first fails at shifted digit 11,
and base \(3\) first fails at shifted digit 12.

## Cycle 2 — retain the prime-predecessor caveat

Proposition 18 does not guarantee that \(M-1\) is prime. Thus it does not
formally exclude a bounded-depth theorem in the exact setting of
Proposition 12.

Nevertheless, explicit prime-predecessor cases are already deep. The
strongest retained example from the current bounded search is
\[
M=63150,\qquad M-1=63149\ \text{prime},\qquad t=5126.
\]
Here
\[
M=2\cdot3\cdot5^2\cdot421,\qquad
D(\operatorname{rad}(M))=-451.
\]
The bases \(5\) and \(421\) pass completely, while bases \(2\) and \(3\)
both first fail at shifted digit 17.

This is finite evidence, not a proof of unbounded depth with prime
predecessors.

## Cycle 3 — exact third-digit algebra at the boundary

Proposition 19 derives the third-prefix residues for a
primary-pseudoperfect subset candidate. With
\[
\frac Mp=pc-1
\]
and a residual subset sum \(E\), both the upper and lower three-digit
prefixes are explicit quadratic expressions in \(c,E\) modulo \(p^3\).

This turns the three-digit primary-pseudoperfect conjecture into a finite
system of modular inequalities. It is suitable for port-by-port analysis,
although the unbounded construction shows that no analogous fixed system
can handle the stronger all-\(M\) conjecture.

## Strategic conclusion

The project now has two distinct proof regimes:

1. **Defect one:** primary pseudoperfect numbers have rigid subset sums and
   may admit a three-digit/port proof.
2. **Negative defect:** reciprocal-supercritical numbers can hide their
   first carry arbitrarily deep, so the main conjecture needs a global
   argument—likely defect descent, a full \(p\)-adic packing object, or an
   invariant using the entire digit tower.

The next repetition should investigate whether a common full witness
induces a positive-defect divisor or quotient. Such a descent would use all
digits automatically and would be compatible with Proposition 18.
