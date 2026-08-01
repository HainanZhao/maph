# Flat-monoid Fourier obstruction for Engine A

**Status:** `PROVED` (finite-algebra obstruction; not a no-go theorem for a
new monoid engine)
**Date:** 2026-08-01 UTC
**Claim boundary:** This note proves why ordinary finite-abelian-group
character Fourier inversion cannot simply be re-used for the full class of
non-coprime flat ray monoids. It does not prove that no generalized
semigroup spectral theory can work, and it does not assert that every AFK
stratum realizes the illustrative squared-prime local factor.

## Result

**PROVED:** In the squared-prime local example used by Kopp--Lagarias, the
complex monoid algebra has a nonzero square-zero element. Consequently it
is not a product of copies of \(\mathbb C\), and evaluations at ordinary
one-dimensional monoid characters cannot be a Fourier-inversion basis for
all monoid-indexed packets.

Kopp--Lagarias Appendix A, Example A.9 identifies the elementary case
\(\mathcal O=\mathbb Z\), \(\mathfrak m=p^2\mathbb Z\) with the finite
monoid
\[
 M=(\mathbb Z/p^2\mathbb Z,\,\cdot).
\]
Let \([a]\) denote the standard basis element of \(\mathbb C[M]\), and
put \(z=[p]-[0]\). Since \(p^2\equiv0\pmod{p^2}\) and \(p\cdot0=0\),
\[
 z^2=[p^2]-2[p\cdot0]+[0]^2=[0]-2[0]+[0]=0.
\]
The basis vectors \([p]\) and \([0]\) are distinct, so \(z\ne0\). Thus
\(\mathbb C[M]\) contains a nonzero nilpotent.

For a finite abelian group \(G\), by contrast, the character transform
identifies \(\mathbb C[G]\) with \(\prod_{\chi\in\widehat G}\mathbb C\);
this algebra is reduced and has no nonzero nilpotents. Therefore the group
Fourier inversion used in Engine A cannot be transferred verbatim to this
flat-monoid setting.

## Relevance and remaining theorem obligation

AFK's exact overlap index is the non-coprime flat/invertible monoid
identified in `tcc-sweep-engine-a-interface-scope-audit-v3.md`. The
squared-prime example proves that a putative all-order extension needs,
at minimum, a replacement for ordinary character support that handles
nonsemisimple (nilpotent/Jordan) directions. A declaration that all
ordinary monoid characters have order at most two would not control those
directions and hence would not establish the packet identity.

The remaining requirements are unchanged:

1. define a finite spectral object for the actual AFK monoid, including
   nonregular directions;
2. prove a label-preserving partial-zeta / Euler-factor transform into
   that object;
3. state and prove an exact analogue of complete quadratic support; and
4. provide a Tate-compatible regulator/unit closure.

Primary pin: Kopp--Lagarias December-2022 PDF SHA-256
`3fdf11b0a581a6499c653e45c4e5f6c5665f84b942c8d341e29313756537e1d0`,
Appendix A, Example A.9 p. 45.
