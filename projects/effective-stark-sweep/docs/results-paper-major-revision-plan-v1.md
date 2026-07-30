# Results paper major-revision plan

Recorded: 2026-07-30 UTC

The v5 manuscript compiles and its recorded computations replay, but
it is not submission-ready. The hold is mathematical rather than
editorial. No Zenodo publication or external submission is permitted
from v5.

## Split

The first manuscript will contain Engines A and B only:

1. the uniform quadratic-support formula;
2. a standalone translation of Shintani's Theorems 1–2,
   Propositions 4–5, and equations (4), (6), (8), and (9) into the
   one-place notation;
3. an all-embeddings height-rigidity lemma;
4. the seven selected Shintani packets, with every modulus and packet
   polynomial printed;
5. the absolute-abelian no-go and index-parity lemmas.

The CM material is a second manuscript. It is held at major revision
until the relative cyclic-quartic hypotheses, the Fourier-to-CM-norm
bridge, and the auxiliary-prime valuation/uniqueness argument are
written and proved.

## Corrections required in the A/B paper

- Equation (9) must retain positive embedded values
  `|tau_1 u_chi|`, unless oriented positive representatives are fixed.
- The Shintani field `H`, transfer conductor, ray class numbers,
  congruence-root factor, distribution index, and real-side
  denominator must be defined before the safe exponent.
- The height proof must name the comparison field, enumerate all
  archimedean places, prove the candidate has modulus one at nonsplit
  embeddings, and derive the degree bound.
- Every use of a PARI class or unit group must state
  `bnfinit(P,1)` followed by full `bnfcertify(bnf)=1`; the flag-one
  quotient-only certification is insufficient.
- The no-go lemma must use the precise hypothesis that the one-place
  ray field is Galois and abelian over the rationals.

## CM gates

The relative Galois group used in the existing formulas is cyclic
quartic. Its internal involution `sigma^2` is not global complex
conjugation, since the latter acts nontrivially on the imaginary
quadratic base. The repaired theorem must distinguish those
automorphisms.

The Q(sqrt(6)) record currently certifies rational Euler polynomials,
two normalized analytic runs, and exact unit-lattice identities. It
does not yet print the individual auxiliary prime ideals, their local
characters, the group-ring Euler factors, or the finite valuations
needed to exclude residual S-unit ambiguity. The case remains outside
the proved theorem set until those data support a written uniqueness
argument.
