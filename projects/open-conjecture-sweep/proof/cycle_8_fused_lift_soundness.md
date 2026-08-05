# Cycle 8: fused first-lift soundness

## Definitions

Fix `k >= 2`, a prime `p`, and a positive integer `c` coprime to `p`.
Write `q=cp` and

\[
  F(k,p,c)=\pi_{q\to p} I(k,p,c).
\]

The Cycle-8 fused procedure first enumerates precisely the base members of
`I(k,p,1)` by the already certified cyclic bad-time-cover construction.  For
each completed base tuple `v`, it examines exactly the fiber

\[
  \pi_{q\to p}^{-1}(v)=\{v+p d: d\in\{0,\ldots,c-1\}^k\}
\]

and emits `v` precisely when a member of that fiber is `(k,p,c)`-improper.

## Retained-path invariant

The broad projection `F(k,p,c)` need not lie in `I(k,p,1)`: a `(k,p,c)`
witness has denominator `cp` and need not be a denominator-`p` witness.  The
required retained-path inclusion instead follows from the published
Proposition 3.1 with parent set `S=I(k,p,1)`: its lifted set is

\[
 S' = \pi_{cp\to p}^{-1}(I(k,p,1))\cap I(k,p,c),
\]

and it proves

\[
 J(k,p)\subseteq\pi_p S'.
\]

The fused enumerator tests the smaller intersection `S'` exactly: first it
requires the base point to be in `I(k,p,1)`, then it retains the base point if
one of its admissible fiber elements is in `I(k,p,c)`.  Thus its output is
exactly `pi_p S'`, and in particular contains `J(k,p)`.  It is deliberately
not asserted to equal `F(k,p,c)`, since an improper lifted point can project
outside `I(k,p,1)`.  The name `F` in the preregistration denotes the broader
published projection; the executable retained set is

\[
 F_1(k,p,c):=\pi_p\bigl(\pi_{cp\to p}^{-1}I(k,p,1)\cap I(k,p,c)\bigr).
\]

This correction of the interface is material: the program only needs the
proved inclusion `J(k,p) subseteq F_1(k,p,c)`.

## Orbit invariance

The set `F_1(k,p,c)` is invariant under coordinate permutations and coordinate
signs: both operations biject the lift fiber and preserve the gcd condition
and every distance `||a w_i/(cp)||`.

For multiplication by `a in Z_p^times`, choose by CRT a `b` satisfying
`b=a (mod p)` and `b=1 (mod c)`.  Then `b` is a unit modulo `cp` and maps the
fiber of `v` bijectively to the fiber of `av`.  Multiplication by a unit
permutes the denominator-`cp` times, hence preserves witness existence; as it
is one modulo `c`, it also preserves every gcd condition.  The same argument
at denominator `p` preserves membership in `I(k,p,1)`.  Therefore an l=1
orbit representative belongs to the fused retained set iff every equivalent
representative does.

## Exact predicate used by the program

For a lifted residue tuple `w` modulo `q`, form for each coordinate its bad
time mask

\[
 D_w=\{a\in\mathbb Z_q:(k+1)\min(a w\bmod q,\,q-a w\bmod q)<q\}.
\]

There is a denominator-`q` witness exactly when the union of the coordinate
masks is not all of `Z_q`.  The program declares `w` improper exactly when
that union is all of `Z_q` and no omission-index gcd condition holds.  This is
Definition 2.1 evaluated directly, including time zero.  A reported retained
base tuple carries a concrete digit vector `d` whose recomputed lifted tuple
satisfies this predicate.

## Scope

The raw `(3,11,4)` enumeration compares this implementation with all raw
tuples, so it verifies `F_1` on that finite instance.  The `(6,47,7)` run
tests the canonical-orbit form but does not establish any statement for
`(13,199,14)` or for the conjecture.
