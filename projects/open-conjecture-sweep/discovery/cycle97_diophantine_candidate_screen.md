# C97 candidate screen: size-22 Diophantine equation

This is a candidate-selection packet, not an attack preregistration. It
authorizes no executable search.

## Source-defined lead

`OBSERVED` from Epoch AI's problem page and its full write-up: after direct
substitution resolved three of the nine equations of size at most 24, six
remain. The smallest survivor is

`P(x,y,z) = z^2 + y^2 z + x^3 - 2 = 0`.

The source's underlying finiteness problem asks for an infinite integer
solution set, while its exact benchmark verifier asks for three distinct
solutions with `|x| > 10^50`. The write-up reduces every listed equation to
the discriminant-square condition
`(y^2+a)^2 - 4P(x)`, and states that extensive small searches support
infinitude but do not prove it.

Sources: <https://epoch.ai/frontiermath/open-problems/small-diophantine> and
<https://epoch.ai/files/open-problems/small-diophantine.pdf>.

## Question and adversarial questioning

Question: can a new polynomial, elliptic, or norm-form mechanism prove
infinitely many solutions for the smallest surviving equation, beginning with
an exact three-solution gate that is not a repetition of the already solved
substitution families?

Question the questioning: the three-large-solutions prompt may reward a
lookup or interpolation artifact without advancing the infinitude problem.
Conversely, insisting on a complete infinitude proof before any bounded gate
would hide useful algebraic structure. The first gate must therefore freeze a
construction family whose identity can be proved symbolically, not merely
search large integers.

Hidden question: can the discriminant-square curve be placed on an explicit
elliptic or higher-genus model whose rational/integral points provide a
reusable family across all six residual equations?

## Alternatives screened

* The other five residual equations are structurally adjacent and should not
  be selected separately until the smallest equation's mechanism is known;
  otherwise this is six parallel substitutions, not one new engine.
* Book-Ramsey, Steiner, arithmetic Kakeya, Hadamard-668, Nivat, stretched LR,
  and finite-cyclic Fuglede are excluded or deferred in the C96 records for
  missing source-cleared finite method families.
* A raw search for `|x| > 10^50` is rejected: it has a verifier but no
  preregistered search cap or mathematical invariant.

## Candidate gate if Oracle selects it

State: an explicit integer-polynomial or norm-form map
`(u,v,...) -> (x,y,z)` for the size-22 equation. Invariant: symbolic
identity `P(x(u,...),y(u,...),z(u,...)) == 0`; exact verifier: integer
arithmetic plus three distinct outputs satisfying the size threshold and an
independent symbolic expansion. Falsifier: any coefficient mismatch or a
nonintegral parameter class. Stop: a proved nonconstant family establishes
infinitude for this equation; a bounded ansatz failure closes only that ansatz
and triggers a method pivot. No unbounded integer search.

The strongest flaw is that the source expressly expects a genuinely new
method, so a low-degree polynomial ansatz may be exhausted quickly and yield
only a routine no-go. Expected information gain is nevertheless higher than
another isolated benchmark object because a successful family would transfer
to the five neighboring equations.

## Oracle outcome

Oracle returned `NO_SELECTION`. The equation remains a preserved lead, not an
authorized attack: fixed degrees/forms, coefficient normalization or
exhaustive elimination bounds, and a nonduplication audit against the
published substitutions are required before preregistration.
