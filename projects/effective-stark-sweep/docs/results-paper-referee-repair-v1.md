# Results-paper referee repair

Status: submission hold.

## Seal-order verdict

Cycle 060 was committed as `d1d355a14a119da1499b07aa1748c56057bff9ce`
at 06:04:41 UTC.  The generic Engine-C W3 tranche entered Git in
`a0674aed115dcea9ce4878e2f09e245254aebd84` at 07:07:17 UTC.  The
first \(e=6\) tranche and the \(\mathbb Q(\sqrt6)\) auxiliary-prime
closure entered Git in
`0afdc1304dfb7f6f39fea791b2dc8f9438318642` at 08:41:02 UTC.  All
precede the first results-paper commit.  The paper did not front-run
unsealed results.

Seal ordering did not protect the meaning of the printed
\(\mathbb Q(\sqrt6)\) polynomial.  The v2 record printed the minimal
polynomial of a complex anti-unit, which has no real roots, as though
it were the positive packet.  The corrected exact bridge first divides
the isolated coordinates by \(4\) and \(6\) in the two certified free
unit lattices and then takes positive CM norms.  Both routes give
\[
x^8-8x^7+12x^6+8x^5-10x^4+8x^3+12x^2-8x+1.
\]
It has four positive roots and no negative roots.  The old polynomial,
the intermediate positive norms, and the identity
\(q_8^3=q_{12}^2\) remain printed in the correction certificate.

## Paper hierarchy

The uniform Engine-A theorem is promoted from a machinery proposition
to a main theorem.  Its proof is expanded using the exact logarithmic
unit lattice in signature \((2,1)\), including the embedded base-unit
vector, primitive relative norm-kernel vector, determinant index, and
regulator identity.  The theorem is independent of bulk computation;
the 1,560 eligible occurrences are applications to be verified.

The selected higher-order and CM cases form a second main theorem.
Each entry receives an engine route, polynomial or exact record
pointer, height data where applicable, and an epistemic-status label.
Historical priority is separated from mathematical status and is not
part of either theorem.

The introduction now prints an eight-item theorem inventory with a
status on every item:

1. the \(\mathbb Q(\sqrt7)\) order-six packet and
   \(\mathbb Q(\sqrt{14})\) replication;
2. the order-ten packet over \(\mathbb Q(\sqrt{33})\);
3. the ramified-prime-\(3\) control RQ-002057;
4. the uniform Engine-A theorem;
5. the two mathematically verified routes for RQ-000458, with the
   conservative process tag `DUAL_ROUTED`;
6. the generic \(\mathbb Q(\sqrt{35})\) closure beyond class number
   one;
7. the corrected \(\mathbb Q(\sqrt6)\), \(e=(8,12)\) closure; and
8. the absolute-abelian no-go lemma.

The \(\mathbb Q(\sqrt{35})\) class-number sentence has its own
independent PARI/GP 2.15.4 replay:
`artifacts/q35-base-class-numbers-v1.json`.

## Parity consistency audit

The historical 88 odd-index rows were proxy-derived and are not valid
tests of the parity lemma.  A fresh check was pre-registered against
the genuine 8,200-row index ledger and the independent exact Fourier
screen.  All 446 genuine odd-index rows above one have trivial sign
class and empty Fourier support.  There are zero exceptions.

Two failed software runs are preserved: one schema-key mismatch and
one escaped-regex parser failure.  Neither reached a mathematical
verdict.

## Scope and exposition

The paper is a theorem/results paper, not a census survey.  It says
explicitly that completeness counts and conductor trends remain for
the census paper.  The introduction will explain the structural arc:
Engine A is the uniform quadratic floor; Engine B crosses to higher
character orders under Shintani's index-two condition; Engine C gives
a disjoint CM route for quartic support; the two boundary lemmas show
why neither character order nor an absolutely abelian fourth route
explains the frontier.
