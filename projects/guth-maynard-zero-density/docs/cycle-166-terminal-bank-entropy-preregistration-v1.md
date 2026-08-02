# Cycle 166 preregistration: terminal-bank entropy on the exponential curve

## Question and claim boundary

Starting from the `PROVED` Cycle-165 conditional fixed-beta four-anchor
classification, determine whether its labelled terminal witness multiplicity
can be bounded on the actual curve
`alpha_ell=exp(2pi ell/Delta)-1`, or whether the curve forces a new anchored
recurrence web. No census, density, interval, or E7/E9 skeleton gain is
preregistered.

The contradiction scale is the labelled four-anchor count
`X^(38/25-o(1))`, not the original census size `X^(16/25)`. Every selection
must retain its original `(beta,ell,h,j)` anchor labels and multiplicity.
Counting only distinct tuples, planes, fractions, or packets is
non-progress.

## Frozen state and terminal labels

Fix `eta=1/100`. A Cycle-165 rank-one witness retains ordered labels
`ell<ell'`, four anchor pairs, and its primitive relation

```text
|r alpha_ell-s alpha_ell'-t| <= 4 C_*/X.            (1)
```

Put `u=ell'-ell`, `E_u=exp(2pi u/Delta)`, and retain the projection fibre
of the four anchors over `(ell,u,r,s,t)`. Since
`1+alpha_(ell+u)=E_u(1+alpha_ell)`, (1) is exactly

```text
|(r-s E_u) exp(2pi ell/Delta)-(r-s+t)| <= 4 C_*/X.  (2)
```

Set `A=r-s E_u`. The transverse branch is
`|A|>=X^(-2/5+eta)`; the near-shift branch is its complement. The threshold
is frozen before any count: a unit increment of `ell` changes the left
analytic term in (2) by order `|A|/Delta`, which exceeds the strip error by
`X^eta` in the transverse branch.

Freeze the projection-fibre recurrence threshold
`F_proj=X^eta`: a canonical tuple with at least `F_proj` labelled *primitive*
four-anchor preimages is retained as a high-fibre anchored web. “Primitive”
means that, after the least common parameter is shifted to zero, the gcd of
the other three parameters is one. This is a structural output threshold, not
an assertion that it alone completes E7/E9.

Low-content rank-two witnesses retain
`(ell,ell',D,N,N',g,g')` and their complete four-anchor fibre. High-content
branches retain their actual seed and packet state
`(beta,h0,j0,ell,q,a,K_pkt)` together with all parent witnesses. These
three terminal states are never merged or deduplicated.

## First gate: rank-one exponential-shift compiler

Attempt to prove the following labelled alternative, with a fixed share and
all constants explicit:

1. the transverse rank-one witness multiplicity is at most
   `X^(38/25-eta)`; or
2. a fixed share of the rank-one bank lies in the near-shift branch and is
   retained as an anchored exponential-shift recurrence web, labelled by
   `(u,r,s,t,ell)` and its full anchor fibre; or
3. some projection fibre itself exceeds the preregistered recurrence
   threshold and is retained as a high-multiplicity anchored web.

The proof must account for the projection from four anchors to
`(u,r,s,t,ell)`: transversality alone only bounds the number of possible
`ell` for fixed `(u,r,s,t)`, and cannot justify discarding a large anchor
fibre. Exact overlap/circle-lift conventions are inherited from Cycle 165.

## Dependent gates in this same research block

After the rank-one gate, attempt the same entropy accounting for low-content
rational planes. Separately, group high-content seeded packets by their
complete packet state and either compile a fixed witness share through the
Cycle-67 recurrence to the E7/E9 skeleton interface, or retain a massed
packet obstruction. A packet with its beta seed removed is a failed row.

## Falsifier and stop rule

A legal `X^(38/25-o(1))` labelled terminal bank with low projection fibres,
transverse rank-one coefficients (or only dispersed near shifts), dispersed
low-content planes, and no packet-to-skeleton recurrence is an entropy
saturator. Preserve it as the outcome; do not weaken its multiplicity by
deduplication. Seal only after the rank-one, plane, and packet alternatives
have each received their registered accounting.

## Living amendment: anchored intersection parametrization

For a rank-one four-anchor witness, canonicalize the primitive direction and
translate its least parameter to zero. The four anchors then have
`h_i=h_0+r n_i`, `h'_i=h'_0+s n_i`, and
`j_i-j'_i=(j_0-j'_0)+t n_i`. The exact object behind a projection fibre is
therefore the common-parameter intersection

```text
{n: h_0+rn in H_ell, h'_0+sn in H_ell'}.
```

For any member of this set the label difference has the exact slope `t` once
`H/X` is below the frozen integer-forcing cutoff. The first proof task now
uses primitive fourth subsets, not raw `binom(|N|,4)`: raw subsets can have a
larger common parameter gcd and belong to a rescaled `(r,s,t)` state. Prove
the exact canonical accounting to primitive subsets, including base and
orientation labels; any nonuniqueness is retained as an additional web, not
normalized away.

## Living amendment: near shifts are exact shift packets

In the frozen near-shift branch, put `z=exp(2pi ell/Delta)` and
`B=r-s+t`. Equation (2) reads `|A z-B|<=4C_*/X`. On the fixed-proportion
label range, `z` is bounded above by a frozen constant. Since
`|A|<=X^(-2/5+eta)` with `eta<2/5`, integer forcing gives `B=0` for all
sufficiently large `X`. Therefore

```text
t=s-r,                  |r-s E_u|<=4C_*/X.          (3)
```

In particular `r,s` have the same nonzero sign. Reduce
`a/q=r/s` by `g_0=gcd(r,s)`. Then

```text
|q E_u-a|<=4C_*/(g_0 X),     q g_0=|s|<=H.           (4)
```

Thus every near-shift witness is a labelled rational approximation packet for
the exponential shift `E_u`, with its original beta anchor fibre retained.
Freeze the conservative structural depth `K_shift=floor(g_0/(8C_*))`; it
satisfies `|qE_u-a|<=1/(K_shift X)` and `qK_shift<=H` when positive. This
is a shift-web output, not yet an E7/E9 transport packet. Project near
witnesses to `(u,r,s)` (with `t=s-r` now determined). There are
`O(Delta H^2)` states. Thus either one such shift state has `F_proj` parent
witnesses and is massed, or the complete near-shift mass is at most
`X^(37/25+eta+o(1))`, below the registered threshold.

## Living amendment: transverse entropy closes after fibre retention

Assume every canonical rank-one projection fibre has fewer than
`F_proj=X^eta` primitive four-anchor witnesses. For fixed `(u,r,s,t)` in the
transverse branch, two distinct label indices would give

```text
|A| |exp(2pi(ell+1)/Delta)-exp(2pi ell/Delta)| <= 8C_*/X.
```

But the left side is `>>X^(-1+eta)` on the frozen label range, a
contradiction for large `X`. Thus `ell` is unique. Once `(ell,u,r,s)` is
fixed, the integer `t` is unique because the strip tolerance is below `1/2`.
There are `O(Delta H^2)=X^(37/25+o(1))` possible `(u,r,s)` projections, so
the full transverse labelled witness count is at most

```text
X^(37/25+eta+o(1)) <= X^(38/25-eta+o(1)),
```

where the final inequality uses the frozen `eta=1/100`. Formalize the
range constants and canonical-fibre definition in the proof record. Combined
with the high-fibre web and the exact near-shift packet, this resolves the
rank-one gate at the level of an inverse classification.

## Living amendment: seeded-packet state entropy

For a Cycle-165 high-content branch, replace its witness-dependent depth by
the canonical maximal safe depth determined by `(ell,a/q)`:

```text
K_max=min(floor(H/q), floor(C_pkt/(X |q alpha_ell-a|))).
```

The Cycle-165 certificate gives `K_max>=X^(6/25-o(1))`; the original base
row remains a fixed-beta seed, where `C_pkt` is the frozen Cycle-67 enlarged
strip constant. Group all parent witnesses by the complete
canonical packet state `(beta,ell,a,q,h_0,j_0,K_max)`. The depth is
determined by `(ell,a/q)`, so it adds no entropy coordinate. On the frozen
label range, `a=O(q)`, `q<=X^(1/5+o(1))`, and there are at most

```text
O(Delta * X^(2/5) * H)=X^(36/25+o(1))
```

such states. With the same fibre threshold `F_proj=X^eta`, either one packet
state is a massed seeded-packet obstruction/web, or the full high-content
witness mass is at most `X^(36/25+eta+o(1))`, strictly below
`X^(38/25-eta)` for `eta=1/100`. Both coordinate high-content branches are
included; a constant union factor is harmless. This is an E7/E9 input or
obstruction classification, not a skeleton bound.

## Living amendment: low planes induce exponential shift packets

For a low-content Cramer plane, retain its signed data and put
`R=D+N`, `S=D+N'`, where
`|D alpha_ell-N|,|D alpha_(ell+u)-N'|<=E_0` with
`E_0=O(C_*H/X)`. The exponential identity gives

```text
|S-E_u R| <= (1+E_u)E_0.                            (5)
```

On the fixed label range, `R,S` are nonzero and comparable to `D`. After
gcd reduction, (5) is a labelled rational approximation to `E_u`, carrying
the complete plane/anchor fibre. This is a new plane-to-shift compiler. Its
advance condition is not merely recording (5): either a high reduced content
feeds beta-preserving multiplicative transport, or a loop/fibre/divisibility
argument must bound the residual shift atlas or retain it as the registered
entropy saturator.

## Living amendment: low-plane shift-state entropy

Use the projection state `(u,R,S)`, retaining every plane and anchor in its
fibre. On the fixed range `|R|=O(H^2)`. Since the error in (5) is
`O(H/X)=o(1)`, for fixed `(u,R)` there is at most one integral `S`. Hence
there are only

```text
O(Delta H^2)=X^(37/25+o(1))
```

low-plane shift states. If none carries `F_proj=X^eta` parent witnesses, the
entire low-plane witness mass is at most
`X^(37/25+eta+o(1))<=X^(38/25-eta+o(1))`. Otherwise retain the massed
`(u,R,S)` fibre as the plane-induced anchored shift web. This is the
registered low-plane accounting; the optional multiplicative transport
engine may strengthen its high-fibre branch but is not needed for this
inverse classification.

## Living amendment: forced massed-web strength

Cycle 165 supplies `X^(38/25-o(1))` terminal witnesses. After the finite
terminal and rank-one sub-splits, one macro branch retains a fixed share. The
near-shift, transverse, and plane-induced shift projections each have at most
`X^(37/25+o(1))` states; the seeded-packet projection has at most
`X^(36/25+o(1))` states. Hence the relevant pigeonhole conclusion is stronger
than `F_proj`: a critical census forces either a rank-one or plane-induced
anchored shift state with `X^(1/25-o(1))` labelled parent witnesses, or a
seeded packet state with `X^(2/25-o(1))` parents. The proof record must keep
the finite branch constants and every parent label. This is a conditional
massed-web inverse, not a census bound or a density gain.
