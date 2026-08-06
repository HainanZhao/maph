# _001 portfolio screen — `NO_SELECTION`

This is a non-budgeted discovery decision. It does not allocate D001, create a
preregistration, or authorize executable work.

## Primary assessment

`OBSERVED`: C001 closed because its n=25 SAT scalability control had an
invalid UNSAT polarity, not because of an Erdős--Szekeres result. Its frozen
failure rule prohibits the canonical retry (`cycle100_control_outcome.md`).
The closure is an irreversible-status exception to the rolling pivot guard,
but not evidence that an underspecified successor should be selected.

The fresh source screen found no new source-cleared finite method family.
Epoch's current open-problems catalogue still lists Hadamard order 668 and the
small-Diophantine family as unsolved, but the former is a construction request
without a frozen structured family, while C98--C99 already exclude the current
Diophantine ansatz and direct tangent transfer. The catalogue says its bespoke
verifiers are not publicly available. Source:
<https://epoch.ai/frontiermath/open-problems>.

## Primary candidate comparison

| candidate | prior boundary | required delta | decision |
|---|---|---|---|
| square-preserving Diophantine tangent lift | C98 exact bounded ansatz no-hit; C99 finds an extra square-coordinate obstruction | explicit self-map of `w^2 = y^4 - 4x^3 + 8`, integrality/congruence invariant, and a bounded symbolic verifier | missing map; defer |
| Ryser component contraction | C72, C87, C88, C91 close local defect, absorption, greedy descent, and reciprocal trace routes | complete finite quotient plus reconstruction lemma for five-cover obstruction | missing state and transition; defer |
| LEM shuffle-polynomial gadget | C81--C83 and C93 close named realization families | explicit parametric gadget and exact majority-margin transition | missing family; defer |
| Hadamard-668 construction | C96 exclusion | source-backed structured construction family with a checkable small closure rule | missing family; defer |

## Tangent-plane bridge probe

`PROVED` (elementary exact algebra): the two tangent planes at the evident
integral points `(1, 0, +1)` and `(1, 0, -1)` contribute no further integral
point to `S: z^2 + y^2*z + x^3 - 2 = 0`.

At `P+ = (1, 0, 1)`, the tangent plane is `3*x + 2*z = 5`. An integral point
on it has `x = 2*n + 1` and `z = 1 - 3*n`, so substituting in `S` gives

```text
n^2*(8*n + 21) + (1 - 3*n)*y^2 = 0,
(3*n - 1)*y^2 = n^2*(8*n + 21).
```

Because `gcd(3*n - 1, n) = 1`, `3*n - 1` divides `8*n + 21`. But
`3*(8*n + 21) - 8*(3*n - 1) = 71`, so `3*n - 1` divides `71`. The only
integral possibilities are `n = 0, 24`; the first gives `P+`, while the
second gives `y^2 = 1728`, not a square. At `P- = (1, 0, -1)`, the tangent
plane `3*x - 2*z = 5` yields the same divisibility argument with the opposite
sign, and only `P-`.

This rejects only the obvious tangent-plane rational-curve engine.  It does
not show that `S(Z)` is finite, rule out another rational curve or
elliptic fibration, or change C98's exact bounded-ansatz boundary.

### Affine-line probe

`PROVED` (elementary exact algebra): neither evident integral point lies on an
affine rational line contained in `S`. For a line through `P+`, write

```text
x = 1 + a*t,  y = b*t,  z = 1 + c*t.
```

The coefficients of `t`, `t^2`, and `t^3` after substitution in `S` are
`2*c + 3*a`, `c^2 + b^2 + 3*a^2`, and `b^2*c + a^3`. The first two vanish
over the rationals only when `a = b = c = 0`: the first gives `c = -3*a`,
and the second becomes `12*a^2 + b^2 = 0`. For a line through `P-`, set
`z = -1 + c*t`; the first two coefficients are `-2*c + 3*a` and
`c^2 - b^2 + 3*a^2`. They imply `c = 3*a` and `b^2 = 12*a^2`, hence again
only the zero rational direction.

This rules out only line parametrizations through the two known integral
points. It leaves rational curves not through them, multisections, and all
integrality-preserving maps open.

## Oracle historical reconstruction

Oracle (`gpt-5.6-sol`, high effort) independently read `PROGRAM.md`, the
C80--C98 sealed artifact headers, C96/C97/C99 decisions, C001 outcome, and
`POSTMORTEMS.md`. It found the same historical gaps: C80, C94, C96, C97, C99,
and C001 are unsealed strategic records, so their named decision documents,
not chat history, constrain this screen.

Oracle first rejected activity bias: a finite verifier is not a new engine,
and C001 shows that even a published SAT interface is unusable if expected
polarity is not derived. It then tested that critique against the four
candidates above. Its artifact-cited exclusion map found no candidate with
all of: explicit input state; invariant/map/transition; smallest exact
verifier; mechanism falsifier; bounded resources; and a nonduplicating delta.
It therefore returns `NO_SELECTION`.

## Decision and bridge

`NO_SELECTION`. D001 remains reserved for the next genuinely selected problem.
The nearest design problem is now a non-tangent-plane square-preserving lift:
before a new selection, write an explicit input anchor, self-map,
denominator/congruence invariant, direct symbolic verifier, and a
resource-bounded falsifier. Do not reopen the C98 coefficient box, run a
large-integer search, or convert this missing bridge into a census.
