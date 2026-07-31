# Roblot phase clarification correction v2

Recorded: 2026-07-31 UTC.

## Correction

`CONTAINED_NOTATIONAL_CORRECTION`: version 1 wrote
\[
c_\chi(h\bar u)=\chi(h)c_\chi(\bar u)
\]
and later described this as a right-action convention without defining
the action of \(h\). With the frozen right exponent notation
\[
c_\chi(u)=\frac12\sum_{r=0}^3 i^r
\log|u^{\gamma^r}|,
\]
exact reindexing instead gives
\[
c_\chi(u^{s\gamma^j})
=s\,i^{-j}c_\chi(u)
=\chi(s\gamma^j)^{-1}c_\chi(u).
\]

The controlling left group-ring action is now defined explicitly by
\[
h\mathbin{\cdot}u:=u^{h^{-1}}.
\]
For this action,
\[
c_\chi(h\mathbin{\cdot}u)=\chi(h)c_\chi(u).
\]

## Claim impact

The mathematical claims are unchanged. Inversion permutes the signed
group \(\{\pm\gamma^j\}\), so:

- `PROVED`: in a certified case, if
  \(\bar\eta=h\mathbin{\cdot}\bar\epsilon\), then
  \[
  L'(0,\chi)/c_\chi(\eta)=\chi(h)^{-1}\in\mu_4;
  \]
- `PROVED`: under (A1)--(A3), membership of this ratio in \(\mu_4\)
  remains equivalent to the full rank-one Stark conjecture;
- `OBSERVED`: the retained five-control statement remains only the
  two-orientation numerical comparison against certified
  \(L'\)-balls.

The full corrected proofs, including
\(\mu(K)=\{\pm1\}\), even-component vanishing, conjugate-pair
determination, Fourier inversion, and inheritance of the abelian
square-root condition, are in
`paper/quartic-stark-phase-note.tex`.

## Evidence

- exact action audit:
  `artifacts/b1-action-convention-audit-v1.json`;
- preregistration amendment:
  `docs/cycles-072-074-b1-preregistration-amendment-v1.md`;
- source of the reindexing identity:
  `docs/gauge-ambiguity-lemma-v1.md`.

Version 1 remains preserved as the superseded record.
