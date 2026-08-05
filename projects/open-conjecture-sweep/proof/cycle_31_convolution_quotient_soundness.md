# Cycle 31: exact convolution-quotient obstruction

## Claim boundary

`PROVED`: the sealed 1,390-atom partition for p199 base 4 / leaf 78 is not an
additive convolution quotient of \(\mathbb Z/2786\mathbb Z\).  This does not
exclude the leaf, rule out a refined partition or another convolution algebra,
or prove LRC(13).

## Criterion

For atoms \(A,B\), let

\[
r_{A,B}(x)=|\{(a,b)\in A\times B:a+b=x\pmod {2786}\}|.
\]

The atom-constant functions are closed under additive convolution exactly
when every \(r_{A,B}\) is constant on every target atom.  This is `PROVED`
because the atom indicators form a basis for that function space and
\(1_A*1_B=r_{A,B}\).

## First exact split

Both independent implementations reconstruct 1,390 atoms with sizes two
singletons, 1,386 negation pairs, and two six-point atoms.  `PROVED` by complete
finite replay: translation by either singleton permutes the atom partition, so
all 2,780 singleton profiles pass.

In the frozen lexicographic pair order, the first split is

\[
A=\{1,2785\}=\{\pm1\},\qquad
B=\{198,2588\}=\{\pm198\}.
\]

Their four sums are

\[
197,\ 199,\ 2587=-199,\ 2589=-197,
\]

each with multiplicity one.  But the target atom

\[
C=\{199,597,995,1791,2189,2587\}
\]

contains both \(199\), where \(r_{A,B}=1\), and \(597\), where
\(r_{A,B}=0\).  Therefore `PROVED` \(r_{A,B}\) is not constant on \(C\), so
the pointwise atom partition is not a convolution quotient.  Independent
enumerations agree that this is pair profile 198 after 395 exceptional-target
evaluations.

## Falsifiers

A frozen atom mismatch, a failed singleton profile, an earlier splitting pair,
or any direct representation count differing from the displayed four sums
invalidates the affected finite claim.  Refining \(C\) can remove this witness
and is outside the no-go boundary.
