# Index parity for nontrivial one-place packets

**Status:** `VERIFIED_THEOREM`  
**Scope:** genuine normal closures of one-place ray fields over real
quadratic fields  
**Role:** final optional addition to the frozen results paper

Let \(K/\mathbb Q\) be real quadratic, let
\(\mathfrak m=\mathfrak f\infty_2\), let \(H/K\) be its one-place ray
field, and let \(N/\mathbb Q\) be the normal closure of \(H\).  Put
\[
 G=\operatorname{Gal}(N/\mathbb Q),\qquad
 A=\operatorname{Gal}(N/K),\qquad
 B=\operatorname{Gal}(N/H).
\]
The image of \([G,G]\) in \(A/B=\operatorname{Gal}(H/K)\) has order
\[
 [H:H\cap\mathbb Q^{\rm ab}].
\]

**Lemma (index parity).** If the sign class \(R\) of the one-place
difference is nontrivial, then
\[
 2\mid[H:H\cap\mathbb Q^{\rm ab}].
\]
Equivalently, an odd Shintani index can occur only when the Fourier
support of the differenced invariant is empty.

**Proof.** Let \(c_1,c_2\in A\) be the real-place inertia involutions
in \(N/K\).  A lift of the nontrivial automorphism of \(K/\mathbb Q\)
interchanges the two real places, so \(c_1\) and \(c_2\) are conjugate
in \(G\).  Consequently
\[
 c_1c_2^{-1}\in [G,G].
\]
In the one-place quotient \(A/B\), the involution at the omitted real
place is trivial and the involution at the retained real place is the
sign class \(R\).  Thus the image of \(c_1c_2^{-1}\) in \(A/B\) is
\(R\).  If \(R\ne1\), this image has order two.  Hence the image of
\([G,G]\) in \(A/B\) has even order, proving the assertion.

For a finite abelian group, a nonidentity element \(R\) of order two
is detected by some character.  Therefore \(R=1\) is equivalent to
empty support for the characters satisfying \(\chi(R)=-1\), which
gives the final formulation. \(\square\)

This proof uses the actual normal closure.  A conjugation-coordinate
proxy at an unstable finite modulus is not sufficient to form
\([G,G]\), which is exactly why provenance rule R-13 applies to the
index predicate.
