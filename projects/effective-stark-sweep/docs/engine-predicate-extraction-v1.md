# Engine predicate extraction v1

Date: 2026-07-29 UTC

Status: `FROZEN_FOR_ANCHOR_REPRODUCTION`

This memo extracts the decision predicates from the working Paper-I/II
scripts.  It is deliberately operational.  The historical labels
“(0-3),” “(0-6),” and “(0-9)” are retained for traceability, but no
census decision is made from those labels alone.

## Common Fourier input

Let \(G\) be the one-place ray group and \(R\) the exact residue/sign
class used in the zeta difference.  For each character \(\chi\), compute
the exact coefficient
\[
 1-\overline{\chi(R)}.
\]
The support is the set of characters for which this coefficient is
nonzero.  Character order is computed in the exact dual of the PARI
cyclic-coordinate presentation.  The engine decision sees this
certificate, not a floating approximation to an \(L\)-value.

## Engine A

Engine A passes only if:

1. every supported character has order one or two;
2. each nontrivial character field is constructed from its exact ray
   kernel and its conductor is checked;
3. `bnfcertify=1` for every base and character field used in the class
   number formula;
4. the relative regulator quotient is proved from an integral unit
   coordinate matrix, including torsion and the exact determinant
   index;
5. the analytic class-number formula gives the required
   \(L'(0,\chi)\) in the paper's ordinary-absolute-value convention;
6. the selected unit has exact minimal polynomial, norm, and oriented
   real embedding.

The dimension-four anchor realizes a single quadratic character.  The
dimension-eight ray-eight anchor realizes two; a bundle with two
characters is still one Engine-A verdict because no other theorem is
used.

## Engine B unit predicates

Write the full unit group as torsion times powers of certified
fundamental units and reduce it modulo the finite ideal.

`B03_POSITIVE_NOT_MINUS_ONE` means:

- enumerate the image of the totally positive unit subgroup modulo
  \(\mathfrak f\);
- certify that `-1` is not in that image.

`B06_NEGATIVE_NORM_NOT_ONE` means:

- enumerate all residue classes represented by norm-negative units,
  including torsion signs;
- certify that `1` is not in that image.

These are precisely the loops used at:

- \(\mathbb Q(\sqrt3),(5)\): positive units are powers of
  \(\beta=2+\sqrt3\), while norm-negative units do not exist;
- \(\mathbb Q(\sqrt2),(14)\): positive units are powers of
  \((1+\sqrt2)^2\), while signed odd powers cover the norm-negative
  classes;
- \(\mathbb Q(\sqrt5),(12)\): even powers of \(\phi\) are positive and
  signed odd powers are norm-negative.

Thus the presence of a norm-\(-1\) unit is not itself a failure.

## Engine B index predicate

Construct:

- \(A=\operatorname{Cl}_{\mathfrak f\infty_1\infty_2}(K)\);
- \(B=\ker(A\to\operatorname{Cl}_{\mathfrak f\infty_i}(K))\);
- the base-conjugation action \(\iota\) on \(A\);
- \(C=(\iota-1)A\), the commutator subgroup in the normal closure.

Compute the exact finite-group index
\[
 [H:H\cap\mathbb Q^{\rm ab}]=[\,\langle B,C\rangle:B\,].
\]
`B09_INDEX_TWO` means this index is exactly two.  The anchor scripts'
“distinct order-two subgroups” argument is the special case
\(|B|=|C|=2\), \(B\ne C\).

The script must also certify the relevant real-place splitting
condition from the inertia/decomposition data of the constructed
one-place field.  Signature alone may be recorded as a cross-check but
is not the deciding certificate.

## Engine B two-route consistency

Route 1:

1. derive Shintani's fixed subgroup from the exact conjugation action;
2. construct its fixed field;
3. identify the forced imaginary quadratic base \(k\) algebraically.

Route 2:

1. construct the candidate extension independently as a subfield of a
   ray field of \(k\);
2. compute its intrinsic conductor with `rnfconductor`;
3. require an exact \(K\)-compatible `nfisisom`, not merely an absolute
   \(\mathbb Q\)-isomorphism.

Any disagreement is `HALT_TWO_ROUTE_MISMATCH`, not `FRONTIER`.

For every ideal divisor \(\mathfrak d\) of the transfer conductor, print
\[
 (f_{\mathfrak d},h_{\mathfrak d},w(\mathfrak d),
   n(\mathfrak d),m_{\mathfrak d}).
\]
Here \(w(\mathfrak d)\) is computed from the roots of unity congruent to
one; it is never replaced by one by convention.  Use
\[
 m_{\mathfrak d}=
 \begin{cases}
 12h_k n(\mathfrak d),&\mathfrak d=\mathcal O_k,\\
 12f_{\mathfrak d}n(\mathfrak d),&\text{otherwise}.
 \end{cases}
\]
The safe exponent is the lcm of this full table and all real
distribution indices introduced by conductor induction.

## Engine B identification predicate

The Arb precision schedule is chosen before evaluation from the safe
exponent and the degree bound.  A case passes only if:

1. every analytic logarithm is an Arb ball;
2. each candidate root is isolated by an exact rational Sturm interval;
3. the ray field is identified over \(K\);
4. two split primes give exact Frobenius/Artin labels;
5. the upper height bound for the powered quotient is at most
   one-hundredth of the applicable lower bound;
6. degrees three and higher use Voutier; degree one uses
   \(\eta=\pm1\); degree two uses
   \(h(\eta)\ge\frac12\log\phi\);
7. positivity, or an independently certified exact phase, selects
   \(\eta=1\).

## Engine C

Engine C passes only if:

1. the one-place Fourier support has order four;
2. each character is lifted to the full two-place group before applying
   base conjugation;
3. the projective quotient has exact order two and its field is
   biquadratic with the real base and two imaginary quadratic
   subfields;
4. equality of the induced linear characters is proved on the normal
   closure—projective equality is insufficient;
5. the exact conductor and local Euler factors agree;
6. the candidate CM characters are an exhaustive inverse pair, and an
   exact separating Dirichlet coefficient chooses one;
7. Stark's imaginary-quadratic rank-one theorem applies with every
   finite member of \(S\) ramified, \(|S|\ge3\), and
   \(e=|\mu(E)|\) certified;
8. Arb lattice inversion isolates integral unit coordinates and exact
   common-normal-closure identities orient the packet.

The independent \(\mathbb Q(\sqrt{-30})\) reconstruction in the
dimension-eight anchor is a mandatory second check, not a second proof
engine.

## Failure semantics

An anchor mismatch is a halt.  A new census case that soundly fails an
engine predicate becomes `FRONTIER` only after later eligible engines
in the A--C--B decision order have also been tested.  Character order
at least three does not by itself block Engine B.  Failure to compute a
deciding object within the caps is never silently converted into a
mathematical failure.
