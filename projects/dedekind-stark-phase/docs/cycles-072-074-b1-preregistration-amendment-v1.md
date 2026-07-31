# B1 preregistration amendment v1: signed-action convention

Recorded: 2026-07-31 UTC, before drafting the B1 manuscript and after
an exact reindexing audit of the frozen Fourier convention.

## Contained ambiguity

The original B1 preregistration wrote a signed right exponent action
but inherited the phase-clarification document's covariance factor for
a left group-ring action. These are inverse conventions.

For \(a=s\gamma^j\in\{\pm\gamma^j\}\), \(s\in\{\pm1\}\), define right
exponentiation by
\[
u^a=(u^{\gamma^j})^s,\qquad
\chi(a)=s\,i^j.
\]
Exact reindexing gives
\[
c_\chi(u^a)=\chi(a)^{-1}c_\chi(u).
\]
Define the left action by
\[
a\mathbin{\cdot}u:=u^{a^{-1}}.
\]
Then
\[
c_\chi(a\mathbin{\cdot}u)=\chi(a)c_\chi(u).
\]

## Effect on claims

`CONTAINED_NOTATIONAL_CORRECTION`: the membership statement
\[
L'(0,\chi)/c_\chi(\eta)\in\mu_4
\]
is unchanged. Inversion permutes the signed group
\(\{\pm\gamma^j\}\), so the existential formula
\(\chi(h)^{-1}\in\mu_4\) is also unchanged after \(h\) is named using
the pinned left action.

The B1 note must define both actions before using \(h\). It may not say
that the left-action covariance is a right-action covariance.

## Remaining frozen requirements

Every other requirement of
`docs/cycles-072-074-b1-preregistration.md` remains unchanged,
including the root-of-unity rider, three reverse-implication
propagation steps, source map, epistemic boundary, and prohibition on
submission or circulation.
