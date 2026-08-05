# Cycle 2 canonical-augmentation argument

## Exact cyclic-cover model

Fix an odd prime (p), put (h=(p-1)/2), and choose the least positive
primitive root (g) modulo (p). The map

\[
e\in \mathbb Z/h\mathbb Z\longmapsto [g^e]\in
\mathbb F_p^*/\{\pm1\}
\]

is a bijection. If (B) is the set of signed time classes failing the exact
Lonely Runner distance inequality, the bad times for speed class (x) are
(B-x): time (y) is bad precisely when (x+y\in B). Hence a size-(k)
speed multiset is in (I(k,p,1)) precisely when its (k) translates of
(B) cover the cyclic group. Translating every speed class translates the
covered-time set oppositely, so coverage is orbit invariant. This proves the
model used by the implementation.

## Canonical augmentation

For a multiset (M) in (mathbb Z/hmathbb Z), let
(operatorname{can}(M)) be the lexicographically least sorted translate.
For nonempty (M), define

\[
P(M)=\operatorname{can}(C\setminus\{\max C\}),\qquad
C=\operatorname{can}(M),
\]

where one copy of the maximum is deleted. This depends only on the translation
orbit of (M).

Starting from the empty multiset, generate every one-element extension of a
canonical parent (A), canonicalize the child, deduplicate equal canonical
children, and retain a child (C) exactly when (P(C)=A).

`PROVED`: this emits exactly one representative of every translation orbit at
every size. Induct on size. For existence, take an orbit with canonical member
(C), delete the prescribed maximum, and let (A=P(C)). By induction (A)
is emitted. Undoing the translation used to canonicalize the deleted parent
shows that one extension of (A) canonicalizes back to (C), and it passes
the parent test. For uniqueness, every accepted child is first canonicalized
and locally deduplicated, while its invariant parent orbit is unique; the
induction hypothesis supplies that parent only once.

## Authorized pruning

For a partial multiset with covered set (U), let

\[
m(U)=\max_x |(B-x)\setminus U|.
\]

If (r) slots remain, any completion covers at most (r,m(U)) additional
points, because each additional translate contributes at most (m(U)) points
relative to the current (U), even when overlaps among future translates are
ignored. Therefore pruning when

\[
|H\setminus U|>r,m(U)
\]

is `PROVED` sound. The implementation uses no other mathematical pruning.
This construction enumerates all orbit types rather than using Cycle 1's
uncovered-point branching; whether the quotient gain outweighs that loss is
the preregistered performance question, not a premise of the proof.
