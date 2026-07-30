# Cycle 059 — general-\(e\) Engine-C normalization and orientation

**Banked:** 2026-07-30T05:42:40Z  
**Claim tag:** `VERIFIED_THEOREM`  
**Scope:** the torsion-invariant archimedean packet produced by Engine C.

## Result

The \(e=6\) gate does not require a new analytic formula.  The
normalization and orientation argument is uniform in
\[
e=|\mu(E)|,
\]
where \(E/k\) is the abelian character field over the imaginary
quadratic base.  In particular it applies to \(e=6,8,12\).

Let \(S\) contain the complex place and the finite conductor primes,
assume the hypotheses of Stark's proved imaginary-quadratic rank-one
theorem, and assume \(|S|\geq3\), so that its distinguished element is
a global unit.  Fix the ordinary complex modulus
\(|z|_{\rm ord}=\sqrt{z\bar z}\).  Stark's normalized complex-place
absolute value is
\[
|z|_w=|z|_{\rm ord}^{\,2}.
\]
Consequently Stark's formula
\[
\zeta'_{E/k,S}(0,g)=-\frac1e\log|g\varepsilon|_w
\]
becomes
\[
\boxed{\quad
\zeta'_{E/k,S}(0,g)
=-\frac2e\log|g\varepsilon|_{\rm ord}.
\quad}                                                    \tag{1}
\]
Thus the **forward class-log coefficient** is \(2/e\): if
\(\ell_g=\log|g\varepsilon|_{\rm ord}\), then
\[
\boxed{\qquad
\zeta'_{E/k,S}(0,g)=-\frac{2}{e}\,\ell_g,
\qquad
\ell_g=-\frac e2\,\zeta'_{E/k,S}(0,g).
\qquad}                                                   \tag{2}
\]
The second expression is the inverse recovery formula; \(e/2\) is
not itself the coefficient in Stark's class-log formula.

With the Paper-II Fourier convention,
\[
L'_{S}(0,\psi)
=-\frac2e\sum_{g\in G}\overline{\psi(g)}
       \ell_g.                                             \tag{3}
\]
For a primitive quartic character, write \(G=\langle\sigma\rangle\),
\(\overline{\psi(\sigma)}=-i\), and use the anti-unit relations
\(\ell_{\sigma^2}=-\ell_1\) and
\(\ell_{\sigma^3}=-\ell_\sigma\).  Then (3) becomes
\[
\boxed{\qquad
L'_S(0,\psi)
  =-\frac4e\bigl(\ell_1-i\ell_\sigma\bigr),
\qquad
\ell_1-i\ell_\sigma
  =-\frac e4 L'_S(0,\psi).
\qquad}                                                   \tag{4}
\]
Therefore the **forward direct-\(L'\) coefficient** is \(4/e\), while
\(-e/4\) is the inverse Fourier-lattice recovery coefficient, with
the displayed sign and character convention.

The coefficients and inverse factors needed by the census are:

| \(e\) | class forward \(2/e\) | class inverse \(-e/2\) | direct-\(L'\) forward \(4/e\) | direct-\(L'\) inverse \(-e/4\) |
|---:|---:|---:|---:|---:|
| 6 | \(1/3\) | \(-3\) | \(2/3\) | \(-3/2\) |
| 8 | \(1/4\) | \(-4\) | \(1/2\) | \(-2\) |
| 12 | \(1/6\) | \(-6\) | \(1/3\) | \(-3\) |

This proves the normalization part of the \(e=6\) lemma, and also the
previously requested written \(e=8\) analogue of Paper II's
normalization lemma.

An \(e=2\) class-log replay alone cannot distinguish the forward
coefficient \(2/e\) from the unsigned inverse magnitude \(e/2\),
because both equal one.  The nontrivial \(e\ge4\) normalization check
is the RQ-000458 \(e=4\) cross-route match; the
\(\mathbb Q(\sqrt{35})\) two-base agreement independently validates
the generic direct-\(L'\), orbit, and bridge implementation, while
remaining an \(e=2\) normalization case.

## What “orientation” can and cannot mean

Stark's unit is determined by (1) only modulo \(\mu(E)\).  This is not
a numerical defect: every \(\xi\in\mu(E)\) satisfies
\[
|g(\xi\varepsilon)|_{\rm ord}=|g\varepsilon|_{\rm ord}
\quad\text{and}\quad
N_{E/E^+}(\xi\varepsilon)=N_{E/E^+}(\varepsilon).
\]
No procedure using the Stark logarithms can select a literal member of
the \(e\)-element torsion coset.  A claim to resolve that literal
choice would therefore be unsound unless additional smoothing or a
congruence condition were introduced.

The corpus does not require such a choice.  Its objects
\(X_A=\exp Z'_{\mathfrak m}(0,A)\), and the CM-to-real bridge used to
identify them, depend only on the ordered ordinary magnitudes and the
positive CM norms.  The certifiable oriented object is
\[
\left(
  \psi,\ 
  [\varepsilon]\in\mathcal O_E^\times/\mu(E),\
  (\log|g\varepsilon|_{\rm ord})_{g\in G},\
  (N_{E/E^+}(g\varepsilon))_{g\in G}
\right),                                                  \tag{3}
\]
with \(G\) ordered by the exact Artin map.  Formula (3) is invariant
under all \(e\) root-of-unity multiples.

The Galois labeling in (3), which is the genuine orientation issue, is
fixed by the following finite exact procedure.

1. Enumerate the complete finite set \(\mathcal C\) of linear ray
   characters compatible with the certified conductor, kernel,
   projective quotient, and normal-closure reinduction.  Scalar twists
   are forbidden.
2. For each \(\psi\in\mathcal C\), compute exact Dirichlet
   coefficients \(a_n(\psi)\), including the certified local-factor
   convention.  Starting with the least admissible \(n\), append
   coefficients until
   \[
   \psi\longmapsto (a_n(\psi))_{n\in B}
   \]
   is injective on \(\mathcal C\).  Compare the source character with
   this exhaustive table.  Failure to obtain one unique match is a
   halt, not a choice made numerically.
3. Order the embeddings by the selected character's exact Artin
   generator.  If the input consists of class derivatives, apply the
   inverse formula in (2).  If it is the primitive quartic
   \(L'(0,\psi)\), apply the inverse Fourier formula in (4).  Perform
   the Arb logarithmic-lattice inversion in the torsion-free group
   \(\mathcal O_E^\times/\mu(E)\), and require a unique isolated
   integral orbit.
4. Use exact normal-closure identities to map the isolated orbit to
   the real packet.  The CM norm is positive.  The certified sign of
   its logarithm, together with the selected Artin label, distinguishes
   the packet root from its reciprocal; positivity alone is not used
   to make that distinction.

Distinct candidate Hecke characters have a separating coefficient
(equivalently, their complete \(L\)-series cannot have all
coefficients equal).  More importantly for a replay certificate, the
argument does not rely on an ineffective existence claim: the emitted
finite coefficient table itself proves injectivity on the enumerated
candidate set.  Paper II's two-element inverse-pair calculation and
RQ-000458 are the \(e=2\) and \(e=4\) instances of this exact
procedure.

## The \(e=6\) specialization

For \(e=6\), all unit-lattice arithmetic is performed in
\(\mathcal O_E^\times/\mu_6\).  Multiplication by \(\zeta_3\) is
therefore torsion, not a new lattice coordinate, and it fixes every
quantity in (3).  Reality and the positive CM norm remove spurious
non-real or negative representatives; the exact coefficient signature
and Artin action supply the Galois labels.

The base-field root count \(w_k\) must not be conflated with
\(e=|\mu(E)|\).  In class-number and \(|S|\)-bookkeeping,
\[
w_k=
\begin{cases}
6,&k=\mathbb Q(\sqrt{-3}),\\
4,&k=\mathbb Q(i),\\
2,&\text{otherwise},
\end{cases}
\]
while (1) always uses \(e\) of the character field.  In particular,
an \(e=6\) character field need not have
\(\mathbb Q(\sqrt{-3})\) as the selected quadratic base.  Every case
certificate must print both \(w_k\) and \(e\), certify
\(|S|\geq3\), and quotient the unit lattice by its exact torsion
subgroup.

This banks the general-\(e\) orientation lemma at theorem level.
Under the directive, the 457 \(e=6\) occurrences open only after the
sealed aligned-candidate validation, if such a candidate exists.

## Decision for \(e>6\)

**Decision: use the general-\(e\) lemma, including both \(e=8\) and
\(e=12\); do not demote the \(e=12\) route to an informal
cross-check.**

For the \(\mathbb Q(\sqrt6)\) packet, the
\(\mathbb Q(\sqrt{-2})\) route has class forward coefficient \(1/4\)
and direct-\(L'\) forward coefficient \(1/2\); the independent
\(\mathbb Q(\sqrt{-3})\) route has coefficients \(1/6\) and \(1/3\),
respectively, with \(w_k=6\).  Both routes must independently:

- select the linear ray character by an injective exact coefficient
  signature;
- isolate the unit orbit in the torsion quotient;
- identify the same Artin-labeled positive packet by exact
  normal-closure identities.

This discharges the old eightfold-orientation obligation at the correct
mathematical level: the invariant packet is uniquely oriented although
a literal Stark unit remains, necessarily, defined modulo \(\mu_8\).
The \(\mathbb Q(\sqrt6)\) case itself remains blocked until the
second-base reconstruction and same-packet comparison are banked.
No Arb promotion is made by this theory note.

## Source and replay anchors

- Stark's rank-one formula and uniqueness modulo roots of unity:
  Stark, *Adv. Math.* **35** (1980), 197–235,
  DOI `10.1016/0001-8708(80)90049-3`.
- Paper II, normalized imaginary-quadratic Stark resolvent:
  `paper/sic-stark-dimensions-seven-eight.tex`, SHA-256
  `9b2acaeb9114bfa404260c9ced0e38cefdcb9fc2089520c2fe90af9c9b9e4252`.
- Paper-II \(e=2\) orientation implementation:
  `scripts/certify_dimension_eight_cm_orientation.py`, SHA-256
  `38b5d7e319c72a0c5d35c0973a1c65fbd10a283e65b93850ccac7b853c02f82f`.
- RQ-000458 \(e=4\) independent orientation:
  `scripts/certify_rq000458_c_orientation.py`, SHA-256
  `204965d569e5dde84a0c69ed58f1646a1323180b72df0e35caa6e5af223466a1`.
- RQ-000458 identity, in plain text:
  \(K=\mathbb Q(\sqrt{14})\), modulus finite HNF
  `[[12,0],[0,6]]` of norm \(72\) with infinite component `[1,0]`,
  ray group \(C_4\times C_2\), and Fourier support orders exactly
  \(\{4\}\) (characters `[1,1]` and `[3,1]`).
- Exact census inventory:
  `artifacts/engine-c-e-inventory-v1.json`, SHA-256
  `a53be7591753b11fecdad2d96dca4479b99bbfaf732982fc1cf17dcf0ac5ef9b`.
- \(\mathbb Q(\sqrt6)\) exact condition, reinduction, and unit-lattice
  transcripts have SHA-256 values
  `9389c57c59844e2930852a26fbaefdcb37bd0e65e14ae70213c6a91112ea22cf`,
  `8a65f7f43426ec3de223b2c3ccf88d36a536d22d156e63aa8096318f264b3345`,
  and
  `fce556c45e4e26283d47569b93cc80a8347e0eaeddc8603fd162f55747929df1`.

## Boundary

This note proves the normalization and the finite orientation
procedure.  It does not certify a new packet by itself.  A case is
promoted only when its exact character enumeration, coefficient
signature, torsion quotient, Arb isolation, and exact packet bridge
are all present and replayable.  Literal representatives of a Stark
unit modulo roots of unity are not corpus claims.
