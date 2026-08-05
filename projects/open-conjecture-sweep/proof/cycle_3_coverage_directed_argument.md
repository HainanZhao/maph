# Cycle 3 coverage-directed orbit argument

## Claim boundary

The argument below concerns only the finite cyclic translate-cover model frozen
for Cycle 3. It supplies the no-omission property needed by the proposed level
enumerator. It does not prove that the resulting frontier computation will fit
the frozen caps, that the Cycle-1 frontier census is independently complete, or
any (J(13,199))-empty or Lonely Runner claim.

## Definitions

Let (H) be the cyclic signed-unit group and let (C_x=B-x\subseteq H) be
the time set covered by center (x\in H). For a multiset (M\subseteq H), put

\[
 U(M)=\bigcup_{x\in M}C_x.
\]

Translation by (a\in H) sends (M) to (M+a) and (U(M)) to a translate
of (U(M)); in particular, full coverage is invariant. Let
\(\operatorname{can}(M)\) be the frozen lexicographically least sorted
translate of (M).

For canonical (A), if (U(A)\ne H), let (q(A)) be the least element of
(H\setminus U(A)). Its directed children are

\[
 \operatorname{can}(A\uplus\{x\})\qquad(q(A)\in C_x).
\]

If (U(A)=H), every (x\in H) is allowed. At each cardinality all equal
canonical children are merged before the next level is expanded.

## Retained-path lemma

**Lemma.** If a size-(k) multiset (S) covers (H), the directed level
construction reaches \(\operatorname{can}(S)\).

**Proof.** We construct prefixes while carrying the unused elements of a
translate of (S). Start with the empty prefix (A_0) and the full multiset
(S_0=S).

Suppose the construction has reached a canonical prefix (A_d), and after
the translations used to canonicalize earlier prefixes the multiset (S_d)
is a translate of (S) containing (A_d) as a submultiset. If (A_d) does
not cover (H), then (q(A_d)) is uncovered by every element of (A_d).
But (S_d) covers (H), so some element
\(x\in S_d\setminus A_d) satisfies (q(A_d)\in C_x). The directed rule
therefore emits

\[
 A_{d+1}=\operatorname{can}(A_d\uplus\{x\}).
\]

Apply the same canonicalizing translation to all of (S_d). The resulting
(S_{d+1}) is still a translate of (S), still covers (H), and contains
(A_{d+1}). If (A_d) already covers (H), the all-center clause permits
any unused element, and the same conclusion holds. Induction reaches a
size-(k) canonical translate of (S), necessarily
\(\operatorname{can}(S)\). Merging an emitted state with an equal canonical
state preserves its presence in the next level. ∎

## Authorized coverage bound

For a prefix (A), write (W=H\setminus U(A)), let
\(r=k-|A|\), and set

\[
 m(A)=\max_{x\in H}|C_x\cap W|.
\]

Any (r) additional centers cover at most (r m(A)) currently uncovered
times. Hence (|W|>r m(A)) rules out completion and is a sound pruning rule.
It depends only on translate-invariant cardinalities, so applying it to the
canonical representative cannot remove a cover orbit.

## Executable obligations

The implementation must still establish that its cyclic coordinates,
canonicalization, coverage masks, full-cover extension clause, level merge,
and counters implement these definitions. A naive small-instance oracle and
the two frozen tuple-set comparisons are required before the frontier run.
