# Stage 10: adaptive three-base covers

## Cycle 1 — make intersection order computable

The smallest-box engine now accepts any nonempty subset of the prime
divisors of \(M\). This lets us distinguish:

- a **complete empty** intersection, which is a rigorous finite
  certificate;
- an explicit surviving multiplier, which rigorously proves nonemptiness;
- an unresolved intersection, which supports no claim either way.

The generalized code exactly recovers the degree-three pattern at
\[
M=4500:
\quad
t_{\{2,3\}}=2,\quad
t_{\{2,5\}}=71,\quad
t_{\{3,5\}}=123,
\]
while the intersection of all three pass sets is empty.

## Cycle 2 — challenge invariants

The Lucas cover degree is not determined by the radical or by reciprocal
defect. The numbers
\[
30,\qquad90,\qquad2400
\]
all have radical \(30\) and defect \(-1\), but their cover degrees are
respectively \(1,2,3\).

Nor is the degree stable under multiplying all prime-power components by
one more copy of the radical. For example, the degree-three seed
\(4500=2^2 3^2 5^3\) becomes degree one at
\(135000=2^3 3^3 5^4\).

Thus exponent geometry, not only reciprocal mass, controls the
intersection pattern.

## Cycle 3 — search for degree four

For four or more prime bases, degree at least four requires a diagonal
family: every triple must have an explicit witness, while the full
intersection is empty.

The structured searches below found no such example:

| Prime kernel | Exponents | Complete empty full intersections | Largest number of witnessed triples |
|---|---:|---:|---:|
| \((2,3,5,7)\) | \(1,\ldots,4\) | 175 | 1 of 4 |
| \((2,3,5,11)\) | \(1,\ldots,4\) | 143 | 1 of 4 |
| \((2,3,7,41)\) | \(1,\ldots,3\) | 35 | 1 of 4 |
| \((2,5,7,11,13)\) | \(1,\ldots,2\) | 19 | 1 of 10 |

Every listed full intersection was killed by at least one completely
resolved triple. These are computational observations, not a universal
bound.

## Cycle 4 — a stronger working conjecture

Define the **three-base cover conjecture**:

> If
> \[
> \sum_{p\mid M}\frac1p>1,
> \]
> then there are prime divisors \(p,q,r\mid M\) such that no
> \(1\leq t\leq(M-1)/2\) passes all three shifted Lucas tests.

This is stronger than the reciprocal-threshold conjecture. An empty
three-base intersection is automatically an empty full intersection,
whether or not \(M-1\) is prime.

An exhaustive cover-degree scan through \(M\leq20000\) gave
\[
\lambda=1:454,\qquad \lambda=2:372,\qquad \lambda=3:3.
\]
The third degree-three example is
\[
14580=2^2 3^6 5.
\]
Its pair witnesses can be chosen as
\[
t_{\{2,3\}}=4617,\qquad
t_{\{2,5\}}=725,\qquad
t_{\{3,5\}}=671,
\]
and its three-way intersection is empty.

The compiled falsifier checked all 4,147 reciprocal-supercritical
\(M\leq100000\) and found an empty triple in every case. The closest case
by proportion of surviving triples was
\[
21300=2^2\cdot3\cdot5^2\cdot71.
\]
Two triples survive:
\[
\{2,5,71\}\text{ at }t=25,\qquad
\{3,5,71\}\text{ at }t=2403,
\]
while \(\{2,3,5\}\) and \(\{2,3,71\}\) are empty.

## Cycle 5 — falsify the fixed-triple shortcut

A tempting strengthening said that the three smallest prime divisors
always form an empty triple. It is false.

At
\[
M=33060=2^2\cdot3\cdot5\cdot19\cdot29,
\]
the multiplier \(t=65\) passes bases \(2,3,5,29\) and fails only base
\(19\). In particular, the three smallest bases have a common witness.
Nevertheless, the cover degree is still three; for example
\(\{2,3,19\}\) has empty intersection.

This counterexample shows that any three-base theorem must select its
triple adaptively from the digit geometry. Ordering the primes by size is
not enough.

## Cycle 6 — adversarial prime extensions

The family
\[
M=300q,\qquad q\leq2000\text{ prime},
\]
was searched because \(M=21300\) corresponds to the record \(q=71\).
Among 260 completely resolved empty full intersections, \(q=71\) remained
the unique best case, with two of four triples surviving.

Starting instead from the degree-three seed \(4500\) was less successful:
among 60 completely resolved \(4500q\) cases with \(q\leq500\), no triple
survived. This demonstrates that multiplying by a new prime changes all
old pass sets; it does not simply append one constraint.

## Next repetition

1. Optimize the compiled three-base falsifier and push well beyond
   \(100000\).
2. Search directly for the largest fraction of surviving triples, rather
   than only asking whether degree four occurs.
3. Develop an adaptive rule for selecting a killing triple. A promising
   greedy rule is: choose the sparsest single box, then the second base
   minimizing its surviving candidates, then a third base that covers the
   remainder.
4. Express that greedy rule in the finite CRT-box language and look for a
   defect-controlled inequality after three intersections.
5. Group Proposition 23's Fourier terms by supports contained in a chosen
   triple. The desired theorem is now low-dimensional, but the choice of
   the three dimensions must depend on \(M\).

The key discipline is to keep “some triple works” separate from “a fixed
or size-ordered triple works.” The latter has already been falsified.
