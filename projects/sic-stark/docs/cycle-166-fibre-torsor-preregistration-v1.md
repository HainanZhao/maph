# Cycle 166 preregistration: fibre-resolved multiplier torsor

## Question and boundary

Can the exact all-characteristic AFK/Kopp multiplier ledger define a
fibre-resolved (C_6) transport torsor over the 36 characteristics, with an
anchor-preserving equivariant graph that avoids the pointwise quotient
falsified in Cycle 165?

This cycle tests a finite transport state space only. It does not define an
additive coefficient-to-logarithm map, an analytic continuation, a finite
part, AFK equality for a spectral coefficient, a Stark identity, fusion
continuity, or TCC. The multiplier is used as a frozen phase source, not as
evidence that it already transports the open analytic object.

The manifest below is the sole frozen specification. It derives a candidate
(C_6) transport from the independent 48th-root phase ledger, then checks
integrality, holonomy, the two anchors, and the minimal graph intertwining.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 166,
  "parameters": {
    "dimension": {
      "kind": "integer",
      "value": 6,
      "rationale": "The sealed section, Shintani action, and all-characteristic multiplier ledger are dimension-six conventions."
    },
    "base_and_section": {
      "kind": "expression",
      "value": "X=(Z/6Z)^2; lambda:X->C6 is the sealed Cycle-164 least-exponent section; anchors lambda(3,5)=1 and lambda(3,4)=2",
      "rationale": "The old quotient remains visible and the two pre-existing orientation anchors must persist."
    },
    "shintani_action": {
      "kind": "expression",
      "value": "T(a,b)=(5a+b,-a) mod 6",
      "rationale": "This is the pinned period-one action whose quotient descent failed in Cycle 165."
    },
    "multiplier_phase": {
      "kind": "expression",
      "value": "Phi(a,b)=zeta_48^p(a,b), p=24*(6+7*(1+a)*(1+b))-12-28*(a^2-5ab+b^2) mod 48",
      "rationale": "This is exactly the AFK phase representative in the Cycle-149 all-characteristic multiplier ledger."
    },
    "torsor_and_transport": {
      "kind": "expression",
      "value": "Y=XxC6; d(x)=(p(Tx)-p(x))/8 mod 6 when the numerator is divisible by 8; T_tilde(x,e)=(Tx,e+d(x))",
      "rationale": "The factor 8 is the fixed embedding zeta_6=zeta_48^8 and is determined before any row is evaluated."
    },
    "normalized_graph": {
      "kind": "expression",
      "value": "s(Tx)=s(x)+d(x); on an orbit containing (3,5) or (3,4), set s(anchor)=lambda(anchor); on every other T-orbit set s(lexicographically least point)=lambda(point); J(delta_x)=delta_(x,s(x))",
      "rationale": "This fixes the otherwise free orbit constants without output fitting and requires both established anchors to be preserved."
    },
    "multiplier_law": {
      "kind": "expression",
      "value": "M_A(delta_(x,e))=Phi(x)*delta_(x,e), with Phi(x)^2=(psi^-2 chi_x^-1)(A6) verified by the frozen Cycle-149 rational ledger",
      "rationale": "A6 fixes X modulo 6; this retains the certified multiplier law separately from the new T transport."
    },
    "intertwining_identity": {
      "kind": "expression",
      "value": "J*T_*=T_tilde*J; T_tilde^3=id_Y; M_A commutes with the right C6 fibre action",
      "rationale": "These are the smallest exact transport checks that distinguish a fibre-resolved torsor from the failed pointwise quotient."
    },
    "analytic_branch": {
      "kind": "not_applicable",
      "justification": "The calculation uses an exact root-of-unity multiplier representative and no logarithm or analytic continuation.",
      "rationale": "A branch choice would improperly turn a finite transport test into an unfrozen analytic operation."
    }
  },
  "resource_caps": {
    "characteristic_rows": {
      "kind": "integer",
      "value": 36,
      "rationale": "The independent multiplier ledger and the transport condition must be checked on the full frozen domain."
    },
    "torsor_fibre_size": {
      "kind": "integer",
      "value": 6,
      "rationale": "The full oriented C6 fibre is retained rather than quotienting through lambda."
    },
    "transport_states": {
      "kind": "integer",
      "value": 216,
      "rationale": "All XxC6 states are checked for the exact third-return identity."
    },
    "wall_seconds": {
      "kind": "integer",
      "value": 30,
      "rationale": "The finite exact state-space verification must not become an unbounded multiplier search."
    },
    "floating_point": {
      "kind": "not_applicable",
      "justification": "All phase exponents, residues, transport labels, and identities are exact modular integer arithmetic.",
      "rationale": "A numerical phase fit would invalidate the frozen multiplier law."
    }
  },
  "formula_families": [
    "Cycle-149 exact AFK/Kopp phase exponent modulo 48",
    "Cycle-164 oriented C6 section and Cycle-165 Shintani action",
    "C6 torsor transport from multiplier phase differences",
    "anchor-normalized graph section and exact finite intertwining"
  ],
  "selection_rule": [
    "Use the frozen phase formula, T direction, zeta_6=zeta_48^8 embedding, and anchor normalization exactly as stated.",
    "Enumerate all 36 base points and all 216 torsor states; do not discard a bad phase difference, orbit, fibre, or anchor.",
    "Do not use a continuous packet, Stark target, AFK endpoint value, or post-result multiplier adjustment to choose transport data."
  ],
  "failure_rule": [
    "Fail this named fibre-resolved multiplier-torsor engine if a phase difference is not divisible by 8, a T-orbit has nonzero C6 holonomy, the normalized graph is inconsistent or moves an anchor, T_tilde^3 is not the identity, or the frozen multiplier-square ledger fails.",
    "A passing finite transport construction is not an additive coefficient-to-logarithm operation, AFK-interface identification, Stark theorem, fusion theorem, or TCC identity.",
    "A failure is not a no-go for other fibre-resolved, higher-root, nonlinear, or analytic operations."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T16:10:28Z",
    "git_head": "ed0aef297f72fe589b2c5a6636098f2f6a429e4e",
    "git_state": " M ../../AGENTS.md\n?? discovery/cycle-166-fibre-torsor-working-ledger.md\n?? docs/cycle-166-fibre-torsor-preregistration-v1.md"
  },
  "input_paths": [
    "AGENTS.md",
    "PLAN.md",
    "artifacts/cycle-164-oriented-ray-monoid-section-v1.json",
    "artifacts/cycle-165-section-equivariance-v1.json",
    "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json",
    "discovery/cycle-165-section-equivariance-prototype-v1.json",
    "proof/verify_cycle_164_oriented_ray_monoid_section.py",
    "proof/verify_cycle_165_section_equivariance.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "certificates/dimension-six-cycle149-stabilizer_ledger.json",
    "scripts/dimension_six_shintani_cycle.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
