# Cycle 166 working decision summary v1

`SEALED`: the canonical record is
`artifacts/cycle-166-terminal-bank-entropy-v1.json`. This ledger remains the
compact decision history; the frozen gate is in
`docs/cycle-166-terminal-bank-entropy-preregistration-v1.md`.

## Frozen input and accounting

- `PROVED` input: Cycle 165 maps a critical fixed-beta census to
  `X^(38/25-o(1))` labelled four-anchor witnesses: rank one, rank-two low
  plane, or genuinely seeded high-content packet.
- Freeze `eta=1/100`, `F_proj=X^eta`, and the target
  `X^(38/25-eta)`. Count full labelled witness multiplicity only; beta-free,
  unanchored, or deduplicated outputs are non-progress.
- `OBSERVED` mentor decision: the session mentor approved this terminal-bank
  entropy block, requiring the full `X^(38/25)` ledger, all three states, and
  the exponential-shift split. Its falsifier is a critical low-fibre,
  dispersed terminal bank with no recurrence web.

## Rank-one compiler

Write `ell'=ell+u`, `E_u=exp(2pi u/Delta)`,
`A=r-sE_u`, and `B=r-s+t`. The fixed-beta relation is

```text
|A exp(2pi ell/Delta)-B| <= 4C_*/X.                 (1)
```

- `CONJECTURED` canonical fibre lemma: translate the least common parameter
  to zero. A rank-one witness is four points
  `(h_0+rn,h'_0+sn)` with exact label-difference slope `t`; its actual
  intersection fibre is the common set of admissible `n`. Raw
  `binom(|N|,4)` is invalid: parameter subsets of gcd greater than one belong
  to a rescaled `(r,s,t)` state. Use
  `Phi_3(N)=#{0<n1<n2<n3 in N:gcd(n1,n2,n3)=1}`. The finite prototype confirms
  this alias correction; signs/canonical overlap remain a proof obligation.
- `CONJECTURED` near shift: if `|A|<=X^(-2/5+eta)`, bounded exponential range
  forces integer `B=0`; hence `t=s-r` and `|r-sE_u|<=4C_*/X`. Reducing by
  `g_0=gcd(r,s)` gives a labelled rational shift packet
  `|qE_u-a|<=4C_*/(g_0X)`, `qg_0<=H`, with depth
  `floor(g_0/(8C_*))`. This is an anchored shift web.
- `CONJECTURED` near-state entropy: after `t=s-r`, there are only
  `O(Delta H^2)` shift states `(u,r,s)`. Therefore a nonmassed near branch
  has at most `X^(37/25+eta)=X^(149/100)` witnesses.
- `CONJECTURED` transverse entropy: absent a fibre of size `F_proj`, fixed
  `(u,r,s,t)` permits at most one `ell`, then `t` is unique. There are
  `O(Delta H^2)=X^(37/25+o(1))` projections, so transverse mass is at most
  `X^(37/25+eta)=X^(149/100) < X^(151/100)`.

`CONJECTURED` forced-web upgrade: Cycle 165's `X^(38/25-o(1))` total and
the finite terminal split imply a fixed-share macro branch. Rank-one and
plane shift states number `X^(37/25+o(1))`, so one has
`X^(1/25-o(1))` labelled parents; seeded packet states number
`X^(36/25+o(1))`, so one has `X^(2/25-o(1))`. This is stronger than the
preregistered `F_proj` web threshold.

## High-content packet compiler

`CONJECTURED`: canonicalize depth from `(ell,a/q)`, not Cramer content. Fixed
beta packet states `(ell,a,q,h0,j0,K_max)` number at most
`Delta * X^(2/5) * H=X^(36/25+o(1))`. Thus they either have a massed seeded
packet fibre, or total at most `X^(36/25+eta)=X^(29/20)`, below target. A
massed state keeps its beta seed and is the only valid E7/E9 handoff.

## Low-plane and new transport engine

`CONJECTURED` plane-to-shift compiler: from
`|D alpha_ell-N|,|D alpha_(ell+u)-N'|=O(H/X)`, define
`R=D+N`, `S=D+N'`. Then

```text
|S-E_u R|=O(H/X).                                   (2)
```

It is a labelled rational shift packet after gcd reduction; high shift
content is a web, while low content is a retained shift atlas. Its missing
discriminator is a loop/fibre/divisibility theorem, not a deduplicated count.

`CONJECTURED` shift-state entropy resolves that residual accounting: project
to `(u,R,S)`. Here `|R|=O(H^2)` and, for fixed `(u,R)`, (2) has at most one
integer `S` because `H/X=o(1)`. There are `O(Delta H^2)=X^(37/25+o(1))`
states. Thus either one contains `F_proj` parent witnesses and is a massed
plane-induced anchored shift web, or all low-plane mass is at most
`X^(37/25+eta)=X^(149/100)<X^(151/100)`. This removes the need for a separate
low-plane discrepancy theorem at this inverse stage.

`CONJECTURED` multiplicative beta transport: for
`|qE_u-a|<=C_1/(KX)`, a seed with `a|h` maps by
`h'=qh/a`, `j'=j+h-h'`, and has new strip error
`C/X+O(H/(aKX))`. It preserves beta but needs divisibility, h-range, and
`aK` balance. Those are registered obstruction branches.

## Seal evidence and next action

`OBSERVED`: `discovery/cycle_166_terminal_bank_entropy_probe.py` checks the
primitive-direction alias, integer-collapse ledger, exponent margins,
plane-to-shift elimination, and multiplicative transport in exact finite
models. It proves no exponential-curve count.

`PROVED`: the exact convention now canonically routes every tested small
rank-one four-subset under all input orderings, absorbs the parameter-gcd
rescaling alias, fixes signed nonzero plane states and the unique integer
choice, and gives first-coordinate priority to both-high witnesses. The
fresh-process builder and focused suite replayed before sealing.

`OBSERVED` companion seal checkpoint: `APPROVE SEAL`; no flaw remained within
the conditional boundary. Its falsifier is a legal Cycle-165 parent with
nonunique canonical routing, a signed-plane/unique-`S`/both-high violation,
or a failed entropy inequality. Adoption reason: the exact routing tests and
JSON-safe rational rendering close the only identified artifact gap.

Next: preregister one creative bridge for a retained massed web. The leading
candidate is the multiplicative beta-transport map, whose divisibility,
`h`-range, and `aK` balance conditions must be tested before any E7/E9 claim.
