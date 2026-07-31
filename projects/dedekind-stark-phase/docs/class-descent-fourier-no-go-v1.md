# Class descent and Fourier no-go

## Proposition

For the dimension-five anchor, the Kopp multiplier attached to a
positive lifted characteristic descends to its normalized ray class
\(A\in G\simeq C_8\). Let the descended value be \(m(A)\), and let
\(R=g^4\) be the sign class. Then

\[
m(RA)=m(A).
\]

Consequently, for every character in the differenced Stark support,

\[
\widehat m(\chi)
=\sum_{A\in G}\overline{\chi(A)}m(A)=0.
\]

## Exact computation

Each of the eight ray classes has exactly three nonzero
characteristics. The three exact multiplier exponents agree:

\[
\begin{array}{c|cccccccc}
A&0&1&2&3&4&5&6&7\\ \hline
\arg m(A)/(2\pi)&
11/20&7/20&19/20&3/20&11/20&7/20&19/20&3/20.
\end{array}
\]

This proves both literal class descent and \(R\)-invariance.

## Proof of Fourier cancellation

The differenced invariant is

\[
\zeta_{\mathfrak m}(s,A)-\zeta_{\mathfrak m}(s,RA).
\]

Its Fourier support consists exactly of characters satisfying
\(\chi(R)=-1\). Pair the terms indexed by \(A\) and \(RA\):

\[
\begin{aligned}
\overline{\chi(A)}m(A)
 +\overline{\chi(RA)}m(RA)
&=\overline{\chi(A)}m(A)
  \left(1+\overline{\chi(R)}\right)\\
&=0.
\end{aligned}
\]

Summing over the four pairs proves the proposition.

## Meaning

The class multiplier that descends is the square-level Kopp/AFK
multiplier. Its invariance under \(R\) forces it into the even Fourier
subspace, while the one-place difference occupies the odd Fourier
subspace. A nonzero phase resolvent therefore requires a choice of
square roots \(\nu(A)\) whose signs distinguish \(A\) from \(RA\).

Those signs are exactly the orientation data the proposed
Dedekind-sum formula was intended to derive. Choosing them from the
known Stark answer would be circular. A noncircular choice might instead
come from the full metaplectic/AFK transformation law, but that is new
structure outside the frozen squared-multiplier mechanism.

This is a no-go theorem for the frozen squared-multiplier mechanism,
not a theorem that no Dedekind-sum phase formula can exist.
