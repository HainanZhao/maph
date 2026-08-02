# Cycle 174 preregistration: capacity-saturated bounded-slack transport

## Question and boundary

Cycle 173 closes only the forward direct map under its unit conservative strip
budget. This cycle asks whether its *exact row-local* error can be transported
with a fixed larger constant on depth-capacity-saturated edges. It may instead
retain a labelled dyadic capacity-deficit bank. It proves no actual population,
target-local packet, recurrence, density, or interval result.

## Frozen split and constants

Freeze `eta=1/2`. On a complete positive forward Cycle-167 edge, retain

```text
h_plus=q h/a,
qE-a=e,       |e|<=C_1/(KX),
y=1+alpha_ell<=Y,
qK<=H,
rho=h y/(aK)=h_plus y/(qK).                          (1)
```

The bound `Y` is fixed independently of `X` on the registered label range.
Partition without discarding labels:

```text
S_sat: qK>=H/2,
D_r: 2^(-(r+1))H < qK <= 2^(-r)H,  r=1,2,... .      (2)
```

The permitted saturated target strip constant is frozen as `C_0+4Y C_1`.
Neither `eta` nor this multiplier may be chosen after inspecting a row.

## Gates

1. Prove the exact target residual is the source residual minus
   `(h/a)y(qE-a)`, so its additional strip constant is `rho C_1`.
2. Prove `rho<=4Y` on `S_sat`; invoke the Cycle-67 propagation identity with
   the fixed constant `C_0+4Y C_1`, with no exponent loss.
3. On every `D_r`, retain all labels and prove `rho>=2^r y`; the branch is a
   quantitative capacity-deficit ledger, not a structural theorem.
4. State precisely that Cycle 170 may reuse the saturated edge with edge
   error constant `4Y C_1`, but no compatible population is supplied.

## Falsifier and advance condition

The falsifier is a legal saturated row with `rho>4Y`, a failure of the
constant-tracked Cycle-67 identity, or a deficit row assigned no dyadic label.
Advance by the exact saturated/deficit classifier only; a variable-in-`X`
slack or a discarded deficit bank is non-progress.
