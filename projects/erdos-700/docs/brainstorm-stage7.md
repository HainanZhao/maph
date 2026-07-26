# Stage 7: near-witnesses, variable depth, and CRT boxes

## Cycle 1 — try to break the conjecture inside the unbounded family

### Brainstorm

Proposition 18 gives
\[
M=6\cdot5^a,\qquad t=6^h
\]
whose Lucas failures can be postponed arbitrarily far. Search this family
directly for a multiplier that never fails in bases \(2\) or \(3\), since
base \(5\) already passes completely.

### Work

The reproducible script `scripts/search_power5_near_witnesses.py` checked
all construction pairs with \(2\leq a\leq500\):

- 89,405 pairs were tested;
- no full witness was found;
- the record was \(a=499,h=447\);
- base \(2\) first failed at shifted digit 453;
- base \(3\) first failed at shifted digit 448.

This is a bounded computation. It neither proves the family is always
covered nor proves the reciprocal-threshold conjecture.

### Prime-predecessor control

The exponents for which \(6\cdot5^a-1\) is a verified prime include
\[
0,1,2,5,11,28,65,72,361,479,494,\ldots
\]
according to
[OEIS A257790](https://oeis.org/A257790).

At the verified-prime exponent \(a=479\), the structured choice \(h=429\)
has:

- base \(5\): no Lucas failure;
- base \(2\): first failure at shifted digit 430;
- base \(3\): first failure at shifted digit 430.

Thus the prime-predecessor condition does not restore any small practical
depth bound. This is still only one finite example; it does not prove
unbounded depth among prime predecessors.

## Cycle 2 — test a naive Kraft weight

### Brainstorm

A first-failure cylinder at depth \(d\) in base \(p\) naturally has weight
approximately \(p^{-d}\). Perhaps summing such weights over \(p\mid M\)
recovers the reciprocal threshold.

### Work and obstruction

The power-\(5\) record examples make the single-path weight
\[
2^{-d_2}+3^{-d_3}
\]
arbitrarily tiny while \(\sum_{p\mid M}1/p=31/30\) remains fixed. Therefore
the depth of the particular first failure cannot by itself carry the needed
\(1/p\) mass.

A viable Kraft argument would have to collect the **entire family of
first-failure cylinders** for each prime, not assign one weight to the
observed path. This is a useful narrowing of the packing idea.

## Cycle 3 — compress the full towers into CRT boxes

Proposition 20 gives an exact finite formulation. For every \(p^a\parallel
M\), the allowed multipliers form a finite digit box
\(\mathcal T_p\) modulo a prime power \(Q_p\). A common witness is exactly a
point in
\[
\bigcap_{p\mid M}\mathcal T_p
\]
whose least representative lies between \(1\) and \((M-1)/2\).

The box size is explicit:
\[
|\mathcal T_p|=\prod_i(A_{p,i}+1),
\qquad A_p=\frac{M}{p^a}(M-1).
\]

The moduli \(Q_p\) are pairwise coprime, so the Chinese remainder theorem
turns a choice of one allowed residue from each box into a unique global
residue. The difficulty is no longer “infinitely many digit conditions”;
it is a **short representative problem for a highly structured CRT
product**.

## Strategic conclusion and next repetition

The most concrete next target is:

> If \(D(\operatorname{rad}(M))<0\), prove that every CRT combination from
> the Lucas boxes has least positive representative greater than
> \((M-1)/2\).

That statement is equivalent to the stronger all-\(M\) reciprocal cover.
For the original problem, it suffices under the additional condition that
\(M-1\) is prime.

Possible tools for the next cycle:

1. bound the discrepancy of each digit box inside intervals;
2. exploit the exact product formula for box sizes;
3. study the shortest CRT representative as a lattice problem;
4. search for a dual certificate—a linear combination of the prime-power
   congruences whose absolute value is too small to be nonzero;
5. compare the box entropy \(\sum\log|\mathcal T_p|\) with
   \(\log(M/2)\) and the defect \(D(\operatorname{rad}(M))\).
