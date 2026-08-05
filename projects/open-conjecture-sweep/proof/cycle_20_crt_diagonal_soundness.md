# Cycle 20: exact CRT two-diagonal bad-time interface

## Claim

Let \(p,c\) be coprime positive integers, let \(q=pc\), and let
\(x\in\{0,\ldots,q-1\}\).  Write

\[
  x=x_p+p j,
  \qquad 0\le x_p<p,\quad 0\le j<c.
\]

Then

\[
 c\min(x,q-x)<q
 \quad\Longleftrightarrow\quad
 j=0\ \text{ or }\ (j=c-1\text{ and }x_p\ne0).
\]

Moreover, if \(x_c\) denotes the canonical residue of \(x\) modulo \(c\),
then \(j\) is determined from the CRT projections alone by

\[
 j\equiv p^{-1}(x_c-x_p)\pmod c,
 \qquad 0\le j<c.
\]

Thus for \(x\equiv as\pmod q\), the direct bad-time predicate can be
computed from

\[
 x_p\equiv (a\bmod p)(s\bmod p)\pmod p,
 \qquad
 x_c\equiv (a\bmod c)(s\bmod c)\pmod c
\]

without reconstructing \(x\) modulo \(q\).

## Proof

Because \(q=pc\), the direct inequality is equivalent to
\(\min(x,q-x)<p\).  If \(j=0\), then \(x=x_p\le p-1<p\), so the
inequality holds.  If \(j=c-1\), then

\[
 q-x=pc-(x_p+p(c-1))=p-x_p,
\]

which is strictly less than \(p\) exactly when \(x_p\ne0\).  Finally, if
\(1\le j\le c-2\), then \(x\ge p\), while

\[
 q-x=p(c-j)-x_p\ge 2p-(p-1)=p+1>p.
\]

Neither side is then strictly less than \(p\).  This proves the
equivalence, including the strict boundary case \(x_p=0,j=c-1\).

Reducing \(x=x_p+pj\) modulo \(c\) gives
\(x_c\equiv x_p+pj\pmod c\).  Since \(p\) and \(c\) are coprime,
\(p^{-1}\pmod c\) exists and yields the stated formula for the unique
canonical \(j\).  Substituting the two local products proves the final
assertion.  \(\square\)

## Claim boundary

`PROVED`: the equivalence above is an elementary theorem for coprime
\(p,c\).  It only factorizes the single-time bad predicate.  It does not
factorize the global simultaneous-cover problem, close any canonical leaf,
or prove \(LRC(13)\).
